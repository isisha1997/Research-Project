"""Audit a finished document's citations.

This is the half of review that needs no interpretation. It asks only questions
with checkable answers: does this DOI resolve, does it resolve to the work the
reference line describes, is this link dead, what kind of source is it.

Findings are split into two classes and the report never blurs them:

  FACT      established by resolving the reference (a DOI Crossref has never
            heard of is a fact about the DOI, not an opinion about the document)
  HEURISTIC a pattern worth a human's attention, which may be a false alarm

Judging whether a sentence needs a citation at all is a reading task, not a
mechanical one, and it deliberately lives outside this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .extract import Extracted, Reference, extract, find_references
from .models import Source, SourceTier
from .resolve import CitationResolver, Resolution, title_similarity

# Domains that identify what a source *is*. Inference is a starting point for a
# human, never a substitute for tiering the source by hand.
DOMAIN_TIERS: list[tuple[tuple[str, ...], SourceTier]] = [
    (("doi.org", "sciencedirect.com", "springer.com", "link.springer.com", "nature.com",
      "wiley.com", "onlinelibrary.wiley.com", "tandfonline.com", "mdpi.com", "acs.org",
      "rsc.org", "sagepub.com", "cambridge.org", "oup.com", "academic.oup.com",
      "plos.org", "frontiersin.org", "pubs.acs.org", "iopscience.iop.org",
      "pubmed.ncbi.nlm.nih.gov", "ncbi.nlm.nih.gov"), SourceTier.PEER_REVIEWED),
    (("europa.eu", "echa.europa.eu", "efsa.europa.eu", "epa.gov", "ftc.gov", "gov.uk",
      "iso.org", "cen.eu", "astm.org", "oecd.org", "legislation.gov.uk", "acm.nl"),
     SourceTier.REGULATOR),
    (("unep.org", "un.org", "wri.org", "worldbank.org", "ellenmacarthurfoundation.org",
      "textileexchange.org", "wwf.org", "iucn.org", "quantis.com"), SourceTier.INSTITUTIONAL),
    (("businessoffashion.com", "voguebusiness.com", "wwd.com", "just-style.com",
      "sourcingjournal.com", "fashionunited.com", "reuters.com", "bloomberg.com",
      "ft.com", "theguardian.com", "nytimes.com"), SourceTier.TRADE_PRESS),
]

ACADEMIC_TLDS = (".edu", ".ac.uk", ".edu.au", ".ac.jp")
GOV_SUFFIXES = (".gov", ".gov.uk", ".gov.au", ".gc.ca", ".govt.nz", ".gov.in", ".gouv.fr")

# A sentence carrying a figure a reader could quote.
FIGURE_PATTERN = re.compile(
    r"\b\d[\d,.]*\s?(%|percent|per cent|kg|tonnes?|tons?|litres?|liters?|"
    r"MJ|kWh|CO2e?|times|x)\b", re.IGNORECASE,
)


@dataclass
class AuditFinding:
    severity: str        # error | warn | info
    kind: str            # fact | heuristic
    message: str
    subject: str | None = None
    line: int | None = None
    hint: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity, "kind": self.kind, "subject": self.subject,
            "line": self.line, "message": self.message, "hint": self.hint,
        }

    def __str__(self) -> str:
        where = f" [{self.subject}]" if self.subject else ""
        tag = "" if self.kind == "fact" else " (heuristic)"
        return f"{self.severity.upper():5}{where}: {self.message}{tag}"


@dataclass
class AuditReport:
    path: Path
    extracted: Extracted
    references: list[Reference] = field(default_factory=list)
    resolutions: dict[str, Resolution] = field(default_factory=dict)
    findings: list[AuditFinding] = field(default_factory=list)
    inferred_tiers: dict[str, SourceTier | None] = field(default_factory=dict)
    online: bool = False

    @property
    def errors(self) -> list[AuditFinding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[AuditFinding]:
        return [f for f in self.findings if f.severity == "warn"]

    @property
    def facts(self) -> list[AuditFinding]:
        return [f for f in self.findings if f.kind == "fact"]

    @property
    def heuristics(self) -> list[AuditFinding]:
        return [f for f in self.findings if f.kind == "heuristic"]

    @property
    def clean(self) -> bool:
        """No established problems. Says nothing about what extraction missed."""
        return not self.errors

    def tier_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for tier in self.inferred_tiers.values():
            key = tier.name.lower() if tier else "unclassified"
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))

    def summary(self) -> dict[str, Any]:
        return {
            "document": str(self.path),
            "format": self.extracted.fmt,
            "extraction": self.extracted.confidence,
            "online": self.online,
            "references": len(self.references),
            "dois": sum(1 for r in self.references if r.kind == "doi"),
            "urls": sum(1 for r in self.references if r.kind == "url"),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "heuristic_flags": len(self.heuristics),
            "clean": self.clean,
            "tiers": self.tier_counts(),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "extraction_note": self.extracted.note,
            "findings": [f.to_dict() for f in self.findings],
            "references": [
                {
                    "raw": r.raw, "kind": r.kind, "line": r.line,
                    "from_hyperlink": r.from_hyperlink,
                    "inferred_tier": (self.inferred_tiers.get(r.key).name.lower()
                                      if self.inferred_tiers.get(r.key) else None),
                    "resolution": (self.resolutions[r.key].to_dict()
                                   if r.key in self.resolutions else None),
                }
                for r in self.references
            ],
        }


def audit(path: str | Path, resolver: CitationResolver | None = None) -> AuditReport:
    path = Path(path)
    resolver = resolver or CitationResolver(online=False)
    extracted = extract(path)
    references = find_references(extracted)
    report = AuditReport(path=path, extracted=extracted, references=references,
                         online=resolver.online)

    if not extracted.is_complete:
        report.findings.append(AuditFinding(
            "warn", "fact",
            f"the document was read best-effort: {extracted.note}",
            hint="install pypdf, or export the document to .docx or .md, then re-run",
        ))

    if not references:
        report.findings.append(AuditFinding(
            "warn", "fact", "no DOIs or URLs were found in this document",
            hint="either the document cites nothing checkable, or the extractor could "
                 "not read it; confirm which before treating this as a clean result",
        ))

    for reference in references:
        report.inferred_tiers[reference.key] = infer_tier(reference)

    report.findings.extend(_check_references(references, report, resolver))
    report.findings.extend(_flag_unsourced_figures(extracted, references))

    order = {"error": 0, "warn": 1, "info": 2}
    report.findings.sort(key=lambda f: (order[f.severity], f.kind != "fact", f.subject or ""))
    return report


def _check_references(references, report, resolver) -> list[AuditFinding]:
    findings: list[AuditFinding] = []

    for reference in references:
        source = _as_source(reference)
        resolution = resolver.resolve(source)
        report.resolutions[reference.key] = resolution

        if resolution.status == "malformed":
            findings.append(AuditFinding(
                "error", "fact", f"{reference.raw} is not a well-formed reference",
                reference.raw, reference.line or None,
                hint="correct the DOI or URL in the document",
            ))
        elif resolution.status == "not_found":
            findings.append(AuditFinding(
                "error", "fact",
                ("this DOI does not exist in Crossref - the reference may be fabricated"
                 if reference.kind == "doi" else "this URL returns 404"),
                reference.raw, reference.line or None,
                hint="find the real reference, or remove the citation",
            ))
        elif resolution.status == "unreachable":
            findings.append(AuditFinding(
                "warn", "fact", f"could not be checked: {resolution.detail}",
                reference.raw, reference.line or None,
                hint="re-run when the network allows, or confirm the source by hand",
            ))
        elif resolution.status == "resolved" and resolution.registry_title:
            mismatch = _title_mismatch(reference, resolution)
            if mismatch is not None:
                findings.append(AuditFinding(
                    "warn", "heuristic",
                    f"the reference line describes a different work from the one this DOI "
                    f"resolves to (registry title: {resolution.registry_title!r})",
                    reference.raw, reference.line or None,
                    hint="a DOI copied from the wrong row of a reference list looks "
                         "exactly like this; confirm the pairing",
                ))

    resolver.save_cache()

    unclassified = [r for r in references if report.inferred_tiers.get(r.key) is None]
    if unclassified:
        findings.append(AuditFinding(
            "info", "heuristic",
            f"{len(unclassified)} reference(s) are from domains this tool does not "
            "recognise, so their evidence tier is unknown",
            hint="tier them by hand; an unrecognised domain is often a company site",
        ))

    company_like = [r for r, t in report.inferred_tiers.items() if t is SourceTier.COMPANY]
    if company_like:
        findings.append(AuditFinding(
            "info", "fact",
            f"{len(company_like)} reference(s) are company self-published material",
            hint="check that no substantive claim rests on these alone",
        ))
    return findings


def _flag_unsourced_figures(extracted: Extracted, references) -> list[AuditFinding]:
    """Lines carrying a quotable figure with no citation nearby.

    A heuristic, and an imprecise one: a figure cited two sentences earlier is a
    false alarm. It is here because an unsourced number is the single most
    quoted and most damaging thing a guide can contain.
    """
    cited_lines = {r.line for r in references if r.line}
    nearby = {line + offset for line in cited_lines for offset in (-2, -1, 0, 1, 2)}
    findings: list[AuditFinding] = []

    for lineno, line in enumerate(extracted.text.splitlines(), 1):
        if lineno in nearby or not FIGURE_PATTERN.search(line):
            continue
        stripped = line.strip()
        if len(stripped) < 40:
            continue  # headings, table cells, and stray numbers
        findings.append(AuditFinding(
            "info", "heuristic",
            f"a figure appears with no citation within two lines: {stripped[:120]!r}",
            line=lineno,
            hint="confirm the number is sourced; numbers travel further than caveats",
        ))

    if len(findings) > 15:
        extra = len(findings) - 15
        findings = findings[:15]
        findings.append(AuditFinding(
            "info", "heuristic",
            f"and {extra} more line(s) with uncited figures - see --json for the full list",
        ))
    return findings


def infer_tier(reference: Reference) -> SourceTier | None:
    """Guess what kind of source this is from its domain. A guess, not a verdict."""
    if reference.kind == "doi":
        return SourceTier.PEER_REVIEWED
    host = (urlparse(reference.raw).netloc or "").lower()
    if not host:
        return None
    host = host[4:] if host.startswith("www.") else host
    for domains, tier in DOMAIN_TIERS:
        if any(host == d or host.endswith("." + d) for d in domains):
            return tier
    # Suffix match, never substring: "notepa.gov.example.com" is not a government site.
    if host.endswith(ACADEMIC_TLDS):
        return SourceTier.INSTITUTIONAL
    if host.endswith(GOV_SUFFIXES):
        return SourceTier.REGULATOR
    return None


def _as_source(reference: Reference) -> Source:
    """Wrap a bare reference so the existing resolver can check it."""
    return Source(
        id=reference.raw,
        tier=SourceTier.COMPANY,   # unused by resolution; the audit infers tiers separately
        title=reference.context or reference.raw,
        doi=reference.raw if reference.kind == "doi" else None,
        url=reference.raw if reference.kind == "url" else None,
    )


def _title_mismatch(reference: Reference, resolution: Resolution) -> bool | None:
    """Compare a bibliography-style line against the title the DOI resolves to.

    Returns None when the context is not a reference line worth comparing, so a
    bare inline DOI never produces a false alarm.
    """
    context = reference.block or reference.context
    if reference.from_hyperlink or len(context) < 60:
        return None
    if not re.search(r"\b(19|20)\d{2}\b", context):
        return None  # no year: probably prose, not a reference entry

    registry = resolution.registry_title or ""
    words = [w for w in re.findall(r"[a-z]{5,}", registry.lower())]
    if len(words) < 3:
        return None  # too short a title to judge

    haystack = context.lower()
    hits = sum(1 for w in set(words) if w in haystack)
    return None if hits / len(set(words)) >= 0.4 else True
