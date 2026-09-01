"""Core data model for verifiable material-innovation education guides.

The model is deliberately claim-centric. A guide is not prose with citations
bolted on; it is a set of claims, each of which must carry the sources that
support it. Prose is generated from the claims, so an unsourced sentence is
structurally impossible rather than merely discouraged.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable


class SourceTier(Enum):
    """Evidence strength, strongest first.

    Rank is used for ordering and for the "weakest evidence" gate; the label
    is what a reader sees next to a claim.
    """

    PEER_REVIEWED = (1, "Peer-reviewed", "Peer-reviewed journal article or meta-analysis")
    REGULATOR = (2, "Regulator / standard", "Regulator, standards body, or government agency")
    INSTITUTIONAL = (3, "Institutional", "NGO, academic institution, or intergovernmental report")
    INDUSTRY_LCA = (4, "Industry LCA", "Industry or third-party life-cycle assessment")
    TRADE_PRESS = (5, "Trade press", "Trade or general press reporting")
    COMPANY = (6, "Company claim", "Company marketing, website, or self-published material")

    def __init__(self, rank: int, label: str, description: str) -> None:
        self.rank = rank
        self.label = label
        self.description = description

    @property
    def is_primary_evidence(self) -> bool:
        """Tiers that can carry a claim on their own."""
        return self.rank <= 3

    @classmethod
    def parse(cls, value: Any) -> "SourceTier":
        if isinstance(value, cls):
            return value
        if value is None:
            raise ValueError("source tier is required")
        key = str(value).strip().upper().replace("-", "_").replace(" ", "_")
        aliases = {
            "PEER_REVIEW": "PEER_REVIEWED",
            "JOURNAL": "PEER_REVIEWED",
            "STANDARD": "REGULATOR",
            "GOVERNMENT": "REGULATOR",
            "NGO": "INSTITUTIONAL",
            "ACADEMIC": "INSTITUTIONAL",
            "LCA": "INDUSTRY_LCA",
            "PRESS": "TRADE_PRESS",
            "NEWS": "TRADE_PRESS",
            "MARKETING": "COMPANY",
            "BRAND": "COMPANY",
        }
        key = aliases.get(key, key)
        try:
            return cls[key]
        except KeyError as exc:
            valid = ", ".join(t.name.lower() for t in cls)
            raise ValueError(f"unknown source tier {value!r}; expected one of: {valid}") from exc


class Stance(Enum):
    """How a claim relates to the proposition named by its topic."""

    SUPPORTS = "supports"
    REFUTES = "refutes"
    MIXED = "mixed"
    NEUTRAL = "neutral"

    @classmethod
    def parse(cls, value: Any) -> "Stance":
        if isinstance(value, cls):
            return value
        if value is None:
            return cls.NEUTRAL
        try:
            return cls(str(value).strip().lower())
        except ValueError as exc:
            valid = ", ".join(s.value for s in cls)
            raise ValueError(f"unknown stance {value!r}; expected one of: {valid}") from exc


class Audience(Enum):
    """Reader layers. One guide is rendered for all of them."""

    PUBLIC = "public"
    INDUSTRY = "industry"
    TECHNICAL = "technical"

    @classmethod
    def parse(cls, value: Any) -> "Audience":
        if isinstance(value, cls):
            return value
        try:
            return cls(str(value).strip().lower())
        except ValueError as exc:
            valid = ", ".join(a.value for a in cls)
            raise ValueError(f"unknown audience {value!r}; expected one of: {valid}") from exc


DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")


def squash(value: Any) -> Any:
    """Collapse YAML block-scalar whitespace so text renders inline.

    Guide specs use folded scalars for readability, which leaves newlines and
    run-on indentation in the string. Rendering happens in several places, so
    normalizing at parse time is the only way to keep them consistent.
    """
    if value is None:
        return None
    return " ".join(str(value).split()) or None


@dataclass
class Source:
    """A citable reference. `tier` is mandatory: untiered evidence is not evidence."""

    id: str
    tier: SourceTier
    title: str
    year: int | None = None
    authors: list[str] = field(default_factory=list)
    container: str | None = None          # journal, publisher, or issuing body
    doi: str | None = None
    url: str | None = None
    accessed: str | None = None           # ISO date the source was last checked by a human
    note: str | None = None

    def __post_init__(self) -> None:
        if not self.id or not str(self.id).strip():
            raise ValueError("source id is required")
        self.id = str(self.id).strip()
        if not self.title or not str(self.title).strip():
            raise ValueError(f"source {self.id!r}: title is required")
        self.title = squash(self.title)
        self.tier = SourceTier.parse(self.tier)
        if self.doi:
            self.doi = normalize_doi(self.doi)
        if self.year is not None:
            self.year = int(self.year)

    @property
    def locator(self) -> str | None:
        """The best machine-checkable handle for this source."""
        if self.doi:
            return f"https://doi.org/{self.doi}"
        return self.url

    def citation(self) -> str:
        """Human-readable reference line."""
        bits: list[str] = []
        if self.authors:
            if len(self.authors) > 3:
                bits.append(f"{self.authors[0]} et al.")
            else:
                bits.append(", ".join(self.authors))
        bits.append(f"({self.year})" if self.year else "(n.d.)")
        bits.append(self.title.rstrip("."))
        if self.container:
            bits.append(self.container)
        line = ". ".join(b for b in bits if b)
        if self.locator:
            line = f"{line}. {self.locator}"
        return line

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Source":
        known = {f for f in ("id", "tier", "title", "year", "authors", "container", "doi", "url", "accessed", "note")}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"source {data.get('id')!r}: unknown field(s): {', '.join(sorted(unknown))}")
        authors = data.get("authors") or []
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(";") if a.strip()]
        return cls(
            id=data.get("id"),
            tier=data.get("tier"),
            title=data.get("title"),
            year=data.get("year"),
            authors=list(authors),
            container=data.get("container"),
            doi=data.get("doi"),
            url=data.get("url"),
            accessed=data.get("accessed"),
            note=data.get("note"),
        )


@dataclass
class Claim:
    """A single assertion the guide makes, plus the sources that carry it.

    `statement` is the technical phrasing; `plain` is the same assertion for a
    non-specialist reader. Both are rendered from the same claim so the two
    audience layers cannot drift apart.
    """

    id: str
    statement: str
    sources: list[str] = field(default_factory=list)
    plain: str | None = None
    topic: str | None = None              # groups claims that speak to one proposition
    stance: Stance = Stance.NEUTRAL
    scope: str | None = None              # the qualifier that keeps the claim honest
    section: str = "Findings"
    audiences: list[Audience] = field(default_factory=lambda: list(Audience))

    def __post_init__(self) -> None:
        if not self.id or not str(self.id).strip():
            raise ValueError("claim id is required")
        self.id = str(self.id).strip()
        if not self.statement or not str(self.statement).strip():
            raise ValueError(f"claim {self.id!r}: statement is required")
        self.statement = squash(self.statement)
        self.plain = squash(self.plain)
        self.scope = squash(self.scope)
        self.stance = Stance.parse(self.stance)
        self.sources = [str(s).strip() for s in (self.sources or []) if str(s).strip()]
        self.audiences = [Audience.parse(a) for a in (self.audiences or list(Audience))]
        if self.topic:
            self.topic = str(self.topic).strip().lower()

    def text_for(self, audience: Audience) -> str:
        if audience is Audience.PUBLIC and self.plain:
            return self.plain
        return self.statement

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Claim":
        known = {"id", "statement", "sources", "plain", "topic", "stance", "scope", "section", "audiences"}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"claim {data.get('id')!r}: unknown field(s): {', '.join(sorted(unknown))}")
        return cls(
            id=data.get("id"),
            statement=data.get("statement"),
            sources=data.get("sources") or [],
            plain=data.get("plain"),
            topic=data.get("topic"),
            stance=data.get("stance"),
            scope=data.get("scope"),
            section=data.get("section") or "Findings",
            audiences=data.get("audiences") or list(Audience),
        )


@dataclass
class Guide:
    """A material education guide: metadata, sources, and claims."""

    slug: str
    title: str
    material: str
    summary: str | None = None
    sources: dict[str, Source] = field(default_factory=dict)
    claims: list[Claim] = field(default_factory=list)
    section_order: list[str] = field(default_factory=list)
    reviewers: list[str] = field(default_factory=list)
    updated: str | None = None

    def source_for(self, source_id: str) -> Source | None:
        return self.sources.get(source_id)

    def sources_for(self, claim: Claim) -> list[Source]:
        found = [self.sources[s] for s in claim.sources if s in self.sources]
        return sorted(found, key=lambda s: (s.tier.rank, s.id))

    def strongest_tier(self, claim: Claim) -> SourceTier | None:
        resolved = self.sources_for(claim)
        return min((s.tier for s in resolved), key=lambda t: t.rank) if resolved else None

    def sections(self) -> list[str]:
        """Declared order first, then any remaining sections in first-seen order."""
        seen = [c.section for c in self.claims]
        ordered = [s for s in self.section_order if s in seen]
        for s in seen:
            if s not in ordered:
                ordered.append(s)
        return ordered

    def claims_in(self, section: str, audience: Audience | None = None) -> list[Claim]:
        return [
            c for c in self.claims
            if c.section == section and (audience is None or audience in c.audiences)
        ]

    def topics(self) -> dict[str, list[Claim]]:
        grouped: dict[str, list[Claim]] = {}
        for claim in self.claims:
            if claim.topic:
                grouped.setdefault(claim.topic, []).append(claim)
        return grouped

    def cited_source_ids(self) -> set[str]:
        return {s for c in self.claims for s in c.sources}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Guide":
        if not isinstance(data, dict):
            raise ValueError("guide must be a mapping at the top level")
        missing = [k for k in ("slug", "title", "material") if not data.get(k)]
        if missing:
            raise ValueError(f"guide is missing required field(s): {', '.join(missing)}")

        sources: dict[str, Source] = {}
        for raw in data.get("sources") or []:
            source = Source.from_dict(raw)
            if source.id in sources:
                raise ValueError(f"duplicate source id: {source.id!r}")
            sources[source.id] = source

        claims: list[Claim] = []
        seen_ids: set[str] = set()
        for raw in data.get("claims") or []:
            claim = Claim.from_dict(raw)
            if claim.id in seen_ids:
                raise ValueError(f"duplicate claim id: {claim.id!r}")
            seen_ids.add(claim.id)
            claims.append(claim)

        return cls(
            slug=str(data["slug"]).strip(),
            title=str(data["title"]).strip(),
            material=str(data["material"]).strip(),
            summary=squash(data.get("summary")),
            sources=sources,
            claims=claims,
            section_order=list(data.get("section_order") or []),
            reviewers=list(data.get("reviewers") or []),
            updated=data.get("updated"),
        )


def normalize_doi(value: str) -> str:
    """Strip the many prefixes a DOI arrives wrapped in, down to `10.xxxx/yyy`."""
    doi = str(value).strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/",
                   "http://dx.doi.org/", "doi:", "DOI:"):
        if doi.lower().startswith(prefix.lower()):
            doi = doi[len(prefix):]
            break
    return doi.strip()


def is_doi(value: str) -> bool:
    return bool(DOI_RE.match(normalize_doi(value)))


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out
