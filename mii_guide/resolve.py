"""Citation resolution: does the reference exist, and does it say what we said?

This is the gate that catches hallucinated and dead references. It runs in
three modes:

  offline  - structural checks only (DOI shape, URL shape). No network.
  online   - resolve DOIs against Crossref and probe URLs over HTTP.
  cached   - online, but a previous result is reused when still fresh.

Every network result is written to a cache file so a rerun of the same guide
does not re-hit Crossref, and so a verification run is reproducible offline.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from .models import Source, is_doi, normalize_doi

CROSSREF_API = "https://api.crossref.org/works/"
USER_AGENT = (
    "mii-guide/1.0 (Material Innovation Initiative; citation verification; "
    "mailto:info@materialinnovation.org)"
)
DEFAULT_TIMEOUT = 20
TITLE_MATCH_THRESHOLD = 0.82
CACHE_TTL_SECONDS = 60 * 60 * 24 * 30  # a month; citations are not fast-moving


@dataclass
class Resolution:
    """The outcome of checking one source's locator."""

    source_id: str
    locator: str | None
    ok: bool
    status: str                       # resolved | unreachable | not_found | unchecked | malformed
    detail: str = ""
    title_match: float | None = None  # 0..1 similarity against the registry title
    year_match: bool | None = None
    registry_title: str | None = None
    registry_year: int | None = None
    checked_at: float | None = None

    @property
    def metadata_conflict(self) -> bool:
        """True when the reference resolves but its metadata disagrees with ours."""
        if not self.ok:
            return False
        if self.title_match is not None and self.title_match < TITLE_MATCH_THRESHOLD:
            return True
        return self.year_match is False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ResolverStats:
    checked: int = 0
    from_cache: int = 0
    network_calls: int = 0
    failures: int = 0


class CitationResolver:
    """Resolves source locators, with an on-disk cache and polite rate limiting."""

    def __init__(
        self,
        online: bool = False,
        cache_path: str | Path | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        delay: float = 0.34,          # Crossref asks for <= 50 req/s; we go far slower
        ttl: int = CACHE_TTL_SECONDS,
    ) -> None:
        self.online = online
        self.timeout = timeout
        self.delay = delay
        self.ttl = ttl
        self.cache_path = Path(cache_path) if cache_path else None
        self.stats = ResolverStats()
        self._cache: dict[str, dict[str, Any]] = self._load_cache()
        self._last_call = 0.0

    # -- cache -------------------------------------------------------------

    def _load_cache(self) -> dict[str, dict[str, Any]]:
        if not self.cache_path or not self.cache_path.exists():
            return {}
        try:
            data = json.loads(self.cache_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}  # a corrupt cache is a cold cache, never a crash

    def save_cache(self) -> None:
        if not self.cache_path:
            return
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(self._cache, indent=2, sort_keys=True), encoding="utf-8"
        )

    def _cached(self, key: str) -> dict[str, Any] | None:
        entry = self._cache.get(key)
        if not entry:
            return None
        checked_at = entry.get("checked_at") or 0
        if time.time() - checked_at > self.ttl:
            return None
        return entry

    # -- public API --------------------------------------------------------

    def resolve(self, source: Source) -> Resolution:
        self.stats.checked += 1
        locator = source.locator

        if not locator:
            return Resolution(
                source.id, None, ok=False, status="malformed",
                detail="source has neither a DOI nor a URL, so nothing can be verified",
            )

        if source.doi and not is_doi(source.doi):
            return Resolution(
                source.id, locator, ok=False, status="malformed",
                detail=f"{source.doi!r} is not a well-formed DOI (expected 10.xxxx/suffix)",
            )

        if not source.doi and not _looks_like_url(source.url or ""):
            return Resolution(
                source.id, locator, ok=False, status="malformed",
                detail=f"{source.url!r} is not a well-formed http(s) URL",
            )

        if not self.online:
            return Resolution(
                source.id, locator, ok=True, status="unchecked",
                detail="structurally valid; run with --online to confirm it resolves",
            )

        cache_key = normalize_doi(source.doi) if source.doi else (source.url or "")
        cached = self._cached(cache_key)
        if cached is not None:
            self.stats.from_cache += 1
            return _resolution_from_cache(source, locator, cached)

        result = self._probe_doi(source) if source.doi else self._probe_url(source)
        self._cache[cache_key] = {
            "ok": result.ok,
            "status": result.status,
            "detail": result.detail,
            "registry_title": result.registry_title,
            "registry_year": result.registry_year,
            "checked_at": time.time(),
        }
        if not result.ok:
            self.stats.failures += 1
        return result

    def resolve_all(self, sources: list[Source]) -> dict[str, Resolution]:
        results = {s.id: self.resolve(s) for s in sources}
        self.save_cache()
        return results

    # -- probes ------------------------------------------------------------

    def _probe_doi(self, source: Source) -> Resolution:
        url = CROSSREF_API + urllib.parse.quote(source.doi, safe="")
        body, error = self._get(url)
        if error:
            status = "not_found" if error == "404" else "unreachable"
            detail = (
                "Crossref has no record of this DOI - the reference may be fabricated"
                if status == "not_found"
                else f"could not reach Crossref: {error}"
            )
            return Resolution(source.id, source.locator, ok=False, status=status,
                              detail=detail, checked_at=time.time())
        try:
            message = json.loads(body).get("message", {})
        except json.JSONDecodeError:
            return Resolution(source.id, source.locator, ok=False, status="unreachable",
                              detail="Crossref returned a response that was not JSON",
                              checked_at=time.time())

        titles = message.get("title") or []
        registry_title = titles[0] if titles else None
        registry_year = _crossref_year(message)
        return _compare(source, registry_title, registry_year)

    def _probe_url(self, source: Source) -> Resolution:
        body, error = self._get(source.url, head=True)
        if error:
            # Some servers reject HEAD; fall back to a ranged GET before failing.
            body, error = self._get(source.url, head=False)
        if error:
            status = "not_found" if error == "404" else "unreachable"
            detail = (
                "the URL returns 404 - the page has moved or never existed"
                if status == "not_found"
                else f"could not reach the URL: {error}"
            )
            return Resolution(source.id, source.locator, ok=False, status=status,
                              detail=detail, checked_at=time.time())
        return Resolution(source.id, source.locator, ok=True, status="resolved",
                          detail="URL is live; title and year are not machine-checkable "
                                 "for a bare web page, so confirm them by hand",
                          checked_at=time.time())

    def _get(self, url: str, head: bool = False) -> tuple[str, str | None]:
        self._throttle()
        self.stats.network_calls += 1
        request = urllib.request.Request(
            url,
            method="HEAD" if head else "GET",
            headers={"User-Agent": USER_AGENT, "Accept": "application/json, */*"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                if head:
                    return "", None
                return response.read().decode("utf-8", errors="replace"), None
        except urllib.error.HTTPError as exc:
            return "", str(exc.code)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return "", str(getattr(exc, "reason", exc))

    def _throttle(self) -> None:
        elapsed = time.time() - self._last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_call = time.time()


# -- helpers ---------------------------------------------------------------

def _compare(source: Source, registry_title: str | None, registry_year: int | None) -> Resolution:
    """Score our stored metadata against what the registry actually holds."""
    title_match = title_similarity(source.title, registry_title) if registry_title else None
    year_match = None
    if source.year is not None and registry_year is not None:
        # Online-first / print-later publication routinely shifts the year by one.
        year_match = abs(source.year - registry_year) <= 1

    detail = "DOI resolves and metadata matches"
    if title_match is not None and title_match < TITLE_MATCH_THRESHOLD:
        detail = (
            f"DOI resolves, but to a different work: registry title is "
            f"{registry_title!r} (similarity {title_match:.2f})"
        )
    elif year_match is False:
        detail = f"DOI resolves, but the registry year is {registry_year}, not {source.year}"

    return Resolution(
        source.id, source.locator, ok=True, status="resolved", detail=detail,
        title_match=title_match, year_match=year_match,
        registry_title=registry_title, registry_year=registry_year,
        checked_at=time.time(),
    )


def _resolution_from_cache(source: Source, locator: str, entry: dict[str, Any]) -> Resolution:
    if entry.get("ok") and source.doi:
        result = _compare(source, entry.get("registry_title"), entry.get("registry_year"))
        result.checked_at = entry.get("checked_at")
        return result
    return Resolution(
        source.id, locator, ok=bool(entry.get("ok")),
        status=entry.get("status", "unchecked"), detail=entry.get("detail", ""),
        registry_title=entry.get("registry_title"), registry_year=entry.get("registry_year"),
        checked_at=entry.get("checked_at"),
    )


def title_similarity(ours: str, theirs: str) -> float:
    """Similarity of two titles, insensitive to case, punctuation, and spacing."""
    return SequenceMatcher(None, _normalize_title(ours), _normalize_title(theirs)).ratio()


def _normalize_title(value: str) -> str:
    cleaned = "".join(ch.lower() if (ch.isalnum() or ch.isspace()) else " " for ch in value)
    return " ".join(cleaned.split())


def _crossref_year(message: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (message.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            try:
                return int(parts[0][0])
            except (TypeError, ValueError):
                continue
    return None


def _looks_like_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
