"""The verification gates that stand between a draft and a publishable guide.

Four gates, each answering one question a reader would ask:

  G1 coverage     - is every claim attached to a source?
  G2 citations    - do those sources exist, and do they say what we said?
  G3 tiering      - how strong is the evidence, and is anything resting on marketing?
  G4 consensus    - where sources disagree, does the guide admit it?

Gates report findings rather than raising. ERROR findings block publication;
WARN findings publish with the caveat printed in the guide itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .models import Audience, Claim, Guide, SourceTier, Stance
from .resolve import CitationResolver, Resolution


class Severity(Enum):
    ERROR = "error"
    WARN = "warn"
    INFO = "info"

    @property
    def blocks_publication(self) -> bool:
        return self is Severity.ERROR


class Gate(Enum):
    COVERAGE = "coverage"
    CITATIONS = "citations"
    TIERING = "tiering"
    CONSENSUS = "consensus"


@dataclass
class Finding:
    gate: Gate
    severity: Severity
    message: str
    subject: str | None = None   # claim id or source id the finding is about
    hint: str | None = None      # what the author should do about it

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate.value,
            "severity": self.severity.value,
            "subject": self.subject,
            "message": self.message,
            "hint": self.hint,
        }

    def __str__(self) -> str:
        where = f" [{self.subject}]" if self.subject else ""
        return f"{self.severity.value.upper():5} {self.gate.value}{where}: {self.message}"


@dataclass
class Contradiction:
    """A topic on which the cited sources do not agree."""

    topic: str
    supporting: list[Claim] = field(default_factory=list)
    refuting: list[Claim] = field(default_factory=list)
    mixed: list[Claim] = field(default_factory=list)

    @property
    def is_live(self) -> bool:
        """A real disagreement, not merely a topic with several claims on it."""
        sides = sum(1 for group in (self.supporting, self.refuting) if group)
        return sides > 1 or bool(self.mixed and (self.supporting or self.refuting))

    def all_claims(self) -> list[Claim]:
        return [*self.supporting, *self.refuting, *self.mixed]

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "supporting": [c.id for c in self.supporting],
            "refuting": [c.id for c in self.refuting],
            "mixed": [c.id for c in self.mixed],
        }


@dataclass
class VerificationReport:
    guide: Guide
    findings: list[Finding] = field(default_factory=list)
    resolutions: dict[str, Resolution] = field(default_factory=dict)
    contradictions: list[Contradiction] = field(default_factory=list)
    online: bool = False

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.WARN]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.INFO]

    @property
    def publishable(self) -> bool:
        return not self.errors

    def findings_for(self, subject: str) -> list[Finding]:
        return [f for f in self.findings if f.subject == subject]

    def tier_distribution(self) -> dict[SourceTier, int]:
        counts: dict[SourceTier, int] = {}
        for source in self.guide.sources.values():
            counts[source.tier] = counts.get(source.tier, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: kv[0].rank))

    def coverage(self) -> float:
        """Share of claims carrying at least one resolvable source."""
        if not self.guide.claims:
            return 0.0
        covered = sum(1 for c in self.guide.claims if self.guide.sources_for(c))
        return covered / len(self.guide.claims)

    def summary(self) -> dict[str, Any]:
        return {
            "guide": self.guide.slug,
            "title": self.guide.title,
            "material": self.guide.material,
            "publishable": self.publishable,
            "online": self.online,
            "claims": len(self.guide.claims),
            "sources": len(self.guide.sources),
            "coverage": round(self.coverage(), 4),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "infos": len(self.infos),
            "contradictions": len([c for c in self.contradictions if c.is_live]),
            "registered_sources": sum(
                1 for s in self.guide.sources.values() if s.is_registered),
            "withheld_claims": sum(
                1 for c in self.guide.claims if c.status == "withheld"),
            "tiers": {t.name.lower(): n for t, n in self.tier_distribution().items()},
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "findings": [f.to_dict() for f in self.findings],
            "contradictions": [c.to_dict() for c in self.contradictions if c.is_live],
            "resolutions": {k: v.to_dict() for k, v in self.resolutions.items()},
        }


def verify(guide: Guide, resolver: CitationResolver | None = None) -> VerificationReport:
    """Run every gate over `guide` and return the combined report."""
    resolver = resolver or CitationResolver(online=False)
    report = VerificationReport(guide=guide, online=resolver.online)

    report.findings.extend(check_coverage(guide))
    resolutions, citation_findings = check_citations(guide, resolver)
    report.resolutions = resolutions
    report.findings.extend(citation_findings)
    report.findings.extend(check_tiering(guide))
    contradictions, consensus_findings = check_consensus(guide)
    report.contradictions = contradictions
    report.findings.extend(consensus_findings)

    report.findings.sort(key=lambda f: (_severity_rank(f.severity), f.gate.value, f.subject or ""))
    return report


# -- G1: every claim maps to a source --------------------------------------

def check_coverage(guide: Guide) -> list[Finding]:
    findings: list[Finding] = []

    if not guide.claims:
        findings.append(Finding(
            Gate.COVERAGE, Severity.ERROR,
            "the guide has no claims, so there is nothing to verify",
            hint="add at least one claim before publishing",
        ))

    for claim in guide.claims:
        if not claim.sources:
            findings.append(Finding(
                Gate.COVERAGE, Severity.ERROR,
                "claim has no sources, so it cannot appear in a verifiable guide",
                subject=claim.id,
                hint="attach a source id, or delete the claim",
            ))
            continue

        for source_id in claim.sources:
            if source_id not in guide.sources:
                findings.append(Finding(
                    Gate.COVERAGE, Severity.ERROR,
                    f"claim cites source {source_id!r}, which is not defined in this guide",
                    subject=claim.id,
                    hint=f"add {source_id!r} to the sources list, or correct the reference",
                ))

        if claim.status == "withheld":
            findings.append(Finding(
                Gate.COVERAGE, Severity.INFO,
                "claim is published with its figure withheld pending confirmation",
                subject=claim.id,
                hint="confirm the value from the held text, then set status: published",
            ))

        if not claim.scope:
            findings.append(Finding(
                Gate.COVERAGE, Severity.INFO,
                "claim has no scope qualifier, so a reader cannot see its boundaries",
                subject=claim.id,
                hint="add `scope:` naming the system boundary, geography, or timeframe",
            ))

    for source_id in sorted(set(guide.sources) - guide.cited_source_ids()):
        findings.append(Finding(
            Gate.COVERAGE, Severity.INFO,
            "source is defined but no claim cites it",
            subject=source_id,
            hint="cite it from a claim, or remove it to keep the bibliography honest",
        ))

    return findings


# -- G2: citations resolve and match ---------------------------------------

def check_citations(
    guide: Guide, resolver: CitationResolver
) -> tuple[dict[str, Resolution], list[Finding]]:
    findings: list[Finding] = []
    cited = guide.cited_source_ids()
    to_check = [s for sid, s in guide.sources.items() if sid in cited]
    resolutions = resolver.resolve_all(to_check)

    for source_id, resolution in sorted(resolutions.items()):
        if resolution.status == "malformed":
            findings.append(Finding(
                Gate.CITATIONS, Severity.ERROR, resolution.detail, subject=source_id,
                hint="give the source a resolvable DOI or an http(s) URL",
            ))
        elif resolution.status == "not_found":
            findings.append(Finding(
                Gate.CITATIONS, Severity.ERROR, resolution.detail, subject=source_id,
                hint="confirm the reference by hand; a reference that does not resolve "
                     "must not be cited",
            ))
        elif resolution.status == "unreachable":
            findings.append(Finding(
                Gate.CITATIONS, Severity.WARN, resolution.detail, subject=source_id,
                hint="re-run the check; if it stays unreachable, verify the source manually",
            ))
        elif resolution.metadata_conflict:
            findings.append(Finding(
                Gate.CITATIONS, Severity.ERROR, resolution.detail, subject=source_id,
                hint="correct the stored title or year to match the registry record",
            ))
        elif resolution.status == "registered":
            source = guide.sources[source_id]
            if not source.held:
                findings.append(Finding(
                    Gate.CITATIONS, Severity.ERROR,
                    f"{source.designation} cannot be resolved by machine and does not say "
                    "where the controlled copy is held",
                    subject=source_id,
                    hint="add `held:` naming who holds the purchased text and when it was "
                         "obtained; an unresolvable source with no custody trail is not a "
                         "citation, it is a claim about a citation",
                ))
            else:
                findings.append(Finding(
                    Gate.CITATIONS, Severity.INFO,
                    f"{source.designation} is a registered source: not machine-checkable, "
                    f"held at {source.held}",
                    subject=source_id,
                ))
        elif resolution.status == "unchecked":
            findings.append(Finding(
                Gate.CITATIONS, Severity.INFO,
                "citation was checked structurally only (offline run)",
                subject=source_id,
                hint="re-run with --online before publishing",
            ))

    for source_id in sorted(cited & set(guide.sources)):
        source = guide.sources[source_id]
        if source.is_registered:
            continue  # a held standard has a custody trail instead of an accessed date
        if source.tier is not SourceTier.COMPANY and not source.accessed:
            findings.append(Finding(
                Gate.CITATIONS, Severity.INFO,
                "source has no `accessed` date, so the guide cannot show when a human last read it",
                subject=source_id,
                hint="add `accessed: YYYY-MM-DD`",
            ))

    return resolutions, findings


# -- G3: source quality tiering --------------------------------------------

def check_tiering(guide: Guide) -> list[Finding]:
    findings: list[Finding] = []

    for claim in guide.claims:
        sources = guide.sources_for(claim)
        if not sources:
            continue  # already an error from G1

        strongest = min(sources, key=lambda s: s.tier.rank).tier

        if strongest is SourceTier.COMPANY:
            findings.append(Finding(
                Gate.TIERING, Severity.ERROR,
                "claim rests only on company self-published material",
                subject=claim.id,
                hint="add independent evidence, or restate the claim as "
                     "\"the company states that ...\" so the reader sees whose claim it is",
            ))
        elif strongest is SourceTier.TRADE_PRESS:
            findings.append(Finding(
                Gate.TIERING, Severity.WARN,
                "claim rests only on trade press, which reports evidence rather than producing it",
                subject=claim.id,
                hint="cite the study or filing the article is reporting on",
            ))
        elif not strongest.is_primary_evidence:
            findings.append(Finding(
                Gate.TIERING, Severity.WARN,
                f"strongest evidence for this claim is {strongest.label.lower()}, "
                "which is not independent primary evidence",
                subject=claim.id,
                hint="add a peer-reviewed, regulator, or institutional source",
            ))

        quantitative = _looks_quantitative(claim.statement)
        if quantitative and strongest.rank > SourceTier.INSTITUTIONAL.rank:
            findings.append(Finding(
                Gate.TIERING, Severity.WARN,
                "claim carries a number but no primary-evidence source to stand behind it",
                subject=claim.id,
                hint="numbers travel further than caveats; cite the study the figure comes from",
            ))

    return findings


# -- G4: contradiction and consensus ---------------------------------------

def check_consensus(guide: Guide) -> tuple[list[Contradiction], list[Finding]]:
    findings: list[Finding] = []
    contradictions: list[Contradiction] = []

    for topic, claims in sorted(guide.topics().items()):
        contradiction = Contradiction(
            topic=topic,
            supporting=[c for c in claims if c.stance is Stance.SUPPORTS],
            refuting=[c for c in claims if c.stance is Stance.REFUTES],
            mixed=[c for c in claims if c.stance is Stance.MIXED],
        )
        contradictions.append(contradiction)

        if contradiction.is_live:
            findings.append(Finding(
                Gate.CONSENSUS, Severity.INFO,
                f"sources disagree on {topic!r}; the guide will present both sides "
                "rather than resolving them",
                subject=topic,
            ))

            # Cherry-picking check: if a reader layer sees only one side of a live
            # disagreement, that layer misleads even though the guide as a whole does not.
            for audience in Audience:
                visible = [c for c in contradiction.all_claims() if audience in c.audiences]
                if not visible:
                    continue
                stances = {c.stance for c in visible}
                if stances <= {Stance.SUPPORTS} or stances <= {Stance.REFUTES}:
                    findings.append(Finding(
                        Gate.CONSENSUS, Severity.ERROR,
                        f"the {audience.value} layer shows only one side of a contested topic",
                        subject=topic,
                        hint=f"include an opposing or mixed claim in the {audience.value} "
                             "layer, or drop the topic from that layer entirely",
                    ))

        corroborating = {s for c in claims for s in c.sources}
        if len(claims) > 1 and len(corroborating) == 1:
            findings.append(Finding(
                Gate.CONSENSUS, Severity.WARN,
                f"every claim on {topic!r} traces back to a single source",
                subject=topic,
                hint="find independent corroboration, or say in the guide that "
                     "the evidence base is one study",
            ))

    return contradictions, findings


# -- helpers ---------------------------------------------------------------

def _looks_quantitative(statement: str) -> bool:
    """A rough test for statements that carry a figure a reader could quote."""
    return any(ch.isdigit() for ch in statement)


def _severity_rank(severity: Severity) -> int:
    return {Severity.ERROR: 0, Severity.WARN: 1, Severity.INFO: 2}[severity]
