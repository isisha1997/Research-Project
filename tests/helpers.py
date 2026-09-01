"""Shared fixtures. Guides are built from dicts so each test states its own setup."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mii_guide.models import Guide  # noqa: E402
from mii_guide.resolve import CitationResolver  # noqa: E402


def source(sid: str, tier: str = "peer_reviewed", **overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": sid,
        "tier": tier,
        "title": f"Title for {sid}",
        "year": 2020,
        "doi": "10.1000/" + sid,
        "accessed": "2026-01-01",
    }
    data.update(overrides)
    return {k: v for k, v in data.items() if v is not None}


def claim(cid: str, sources: list[str] | None = None, **overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": cid,
        "statement": f"Statement for {cid}.",
        "scope": "Cradle-to-gate",
        "sources": sources if sources is not None else ["s1"],
    }
    data.update(overrides)
    return data


def guide(sources: list[dict] | None = None, claims: list[dict] | None = None,
          **overrides: Any) -> Guide:
    data: dict[str, Any] = {
        "slug": "test-guide",
        "title": "Test Guide",
        "material": "Test material",
        "sources": sources if sources is not None else [source("s1")],
        "claims": claims if claims is not None else [claim("c1")],
    }
    data.update(overrides)
    return Guide.from_dict(data)


class FakeResolver(CitationResolver):
    """An online resolver whose network layer is scripted per URL substring."""

    def __init__(self, responses: dict[str, tuple[str, str | None]]) -> None:
        super().__init__(online=True, cache_path=None, delay=0.0)
        self.responses = responses
        self.calls: list[str] = []

    def _get(self, url: str, head: bool = False) -> tuple[str, str | None]:
        # DOIs arrive percent-encoded in the Crossref path; match on the plain form.
        import urllib.parse
        plain = urllib.parse.unquote(url)
        self.calls.append(plain)
        # This method *is* the transport under test, so it owns the counter that
        # the real _get would otherwise increment.
        self.stats.network_calls += 1
        for needle, response in self.responses.items():
            if needle in plain:
                return response
        return "", "404"


def crossref_body(title: str, year: int) -> str:
    import json
    return json.dumps({
        "message": {"title": [title], "issued": {"date-parts": [[year]]}}
    })
