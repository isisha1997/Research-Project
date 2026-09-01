"""Render a verified guide to Markdown and HTML.

Prose is generated from claims, never written alongside them. That is what
makes the coverage gate meaningful: there is no path by which a sentence
reaches the page without a source attached to it.

Every guide carries all three reader layers, so a brand strategist and a
materials scientist read the same evidence at different depths rather than
reading two documents that can drift apart.
"""

from __future__ import annotations

import html
from datetime import date

from .models import Audience, Claim, Guide, Source, SourceTier
from .verify import Contradiction, VerificationReport

# Material Innovation Initiative brand palette.
BRAND = {
    "primary": "#9A2866",
    "secondary": "#A4BAB7",
    "deep": "#283D6B",
    "amber": "#F1B95E",
    "coral": "#E59B85",
    "sage": "#76988B",
}

TIER_COLOR = {
    SourceTier.PEER_REVIEWED: BRAND["deep"],
    SourceTier.REGULATOR: BRAND["sage"],
    SourceTier.INSTITUTIONAL: BRAND["secondary"],
    SourceTier.INDUSTRY_LCA: BRAND["amber"],
    SourceTier.TRADE_PRESS: BRAND["coral"],
    SourceTier.COMPANY: BRAND["primary"],
}

AUDIENCE_BLURB = {
    Audience.PUBLIC: "Plain language, no background assumed.",
    Audience.INDUSTRY: "For brand, sourcing, and investment decisions.",
    Audience.TECHNICAL: "Full technical statements, scope qualifiers, and evidence tiers.",
}


class Numbering:
    """Stable reference numbers, assigned in order of first citation."""

    def __init__(self, guide: Guide) -> None:
        self._numbers: dict[str, int] = {}
        for claim in guide.claims:
            for source_id in claim.sources:
                if source_id in guide.sources and source_id not in self._numbers:
                    self._numbers[source_id] = len(self._numbers) + 1

    def of(self, source_id: str) -> int | None:
        return self._numbers.get(source_id)

    def ordered(self, guide: Guide) -> list[tuple[int, Source]]:
        pairs = [(n, guide.sources[sid]) for sid, n in self._numbers.items() if sid in guide.sources]
        return sorted(pairs, key=lambda pair: pair[0])


# -- Markdown ---------------------------------------------------------------

def render_markdown(report: VerificationReport, audience: Audience | None = None) -> str:
    """Render the guide. With `audience`, render that layer only."""
    guide = report.guide
    numbering = Numbering(guide)
    layers = [audience] if audience else list(Audience)
    out: list[str] = []

    out.append(f"# {guide.title}")
    out.append("")
    out.append(f"**Material:** {guide.material}")
    if guide.updated:
        out.append(f"  ·  **Updated:** {guide.updated}")
    out.append("")
    out.append(_markdown_status(report))
    out.append("")

    if guide.summary:
        out.append("## In brief")
        out.append("")
        out.append(guide.summary.strip())
        out.append("")

    for layer in layers:
        claims = [c for c in guide.claims if layer in c.audiences]
        if not claims:
            continue
        out.append(f"## {layer.value.title()} layer")
        out.append("")
        out.append(f"*{AUDIENCE_BLURB[layer]}*")
        out.append("")
        for section in guide.sections():
            in_section = [c for c in claims if c.section == section]
            if not in_section:
                continue
            out.append(f"### {section}")
            out.append("")
            for claim in in_section:
                out.append(_markdown_claim(guide, claim, layer, numbering))
                out.append("")

    live = [c for c in report.contradictions if c.is_live]
    if live:
        out.append("## Where the evidence disagrees")
        out.append("")
        out.append(
            "These questions are contested in the literature. The guide reports the "
            "disagreement rather than choosing a side."
        )
        out.append("")
        for contradiction in live:
            out.append(_markdown_contradiction(guide, contradiction, numbering))
            out.append("")

    out.append("## Sources")
    out.append("")
    out.append("Numbered in order of first citation. The label on each source is its "
               "evidence tier; see the note below on how tiers are assigned.")
    out.append("")
    for number, source in numbering.ordered(guide):
        resolution = report.resolutions.get(source.id)
        mark = _resolution_mark(resolution)
        held = f" · held: {source.held}" if source.held else ""
        out.append(f"{number}. **[{source.tier.label}]** {source.citation()}{held} {mark}")
    out.append("")

    out.append(_markdown_method(report))
    return "\n".join(out).rstrip() + "\n"


def _markdown_claim(guide: Guide, claim: Claim, audience: Audience, numbering: Numbering) -> str:
    refs = "".join(f"[{numbering.of(s)}]" for s in claim.sources if numbering.of(s))
    withheld = " **[figure withheld pending confirmation]**" if claim.status == "withheld" else ""
    line = f"- {claim.text_for(audience)}{withheld} {refs}".rstrip()
    if audience is not Audience.PUBLIC:
        tier = guide.strongest_tier(claim)
        meta: list[str] = []
        if tier:
            meta.append(f"evidence: {tier.label.lower()}")
        if claim.scope:
            meta.append(f"scope: {claim.scope}")
        if meta:
            line += f"\n  <sub>{' · '.join(meta)}</sub>"
    return line


def _markdown_contradiction(guide: Guide, contradiction: Contradiction, numbering: Numbering) -> str:
    lines = [f"**{contradiction.topic}**", ""]
    for label, claims in (
        ("Evidence for", contradiction.supporting),
        ("Evidence against", contradiction.refuting),
        ("Mixed or conditional", contradiction.mixed),
    ):
        if not claims:
            continue
        lines.append(f"*{label}:*")
        for claim in claims:
            refs = "".join(f"[{numbering.of(s)}]" for s in claim.sources if numbering.of(s))
            lines.append(f"- {claim.statement} {refs}".rstrip())
        lines.append("")
    return "\n".join(lines).rstrip()


def _markdown_status(report: VerificationReport) -> str:
    summary = report.summary()
    state = _state_label(report)
    mode = "online citation checks" if report.online else "offline structural checks"
    return (
        f"> **{state}** — {summary['claims']} claims, {summary['sources']} sources, "
        f"{summary['coverage'] * 100:.0f}% claim coverage, "
        f"{summary['errors']} errors / {summary['warnings']} warnings ({mode})."
    )


def _markdown_method(report: VerificationReport) -> str:
    lines = [
        "## How this guide was verified",
        "",
        "Every sentence above is generated from a claim record that carries its own "
        "sources; prose without a source cannot enter the document. Before publication "
        "the guide passes four gates:",
        "",
        "1. **Coverage** — every claim maps to at least one defined source.",
        "2. **Citations** — every DOI resolves against Crossref and its title and year "
        "match what we stored; every URL returns a live response.",
        "3. **Tiering** — every source is ranked by evidence strength, and no claim may "
        "rest on company self-published material alone.",
        "4. **Consensus** — where sources disagree, the disagreement is surfaced, and no "
        "reader layer may show only one side of a contested topic.",
        "",
    ]
    if report.warnings:
        lines.append("**Open caveats carried into publication:**")
        lines.append("")
        for finding in report.warnings:
            subject = f"`{finding.subject}` — " if finding.subject else ""
            lines.append(f"- {subject}{finding.message}")
        lines.append("")
    return "\n".join(lines)


def _state_label(report: VerificationReport) -> str:
    """A guide that never had its citations resolved is not a verified guide."""
    if not report.publishable:
        return "BLOCKED"
    return "VERIFIED" if report.online else "PROVISIONAL"


def _resolution_mark(resolution) -> str:
    if resolution is None:
        return ""
    if resolution.status == "resolved" and not resolution.metadata_conflict:
        return "✓ resolved"
    if resolution.status == "registered":
        return "◆ registered - held copy, not machine-checkable"
    if resolution.status == "unchecked":
        return "· not yet checked online"
    return f"⚠ {resolution.status.replace('_', ' ')}"


# -- HTML -------------------------------------------------------------------

def render_html(report: VerificationReport) -> str:
    guide = report.guide
    numbering = Numbering(guide)
    summary = report.summary()
    esc = html.escape

    parts: list[str] = []
    parts.append(f"<!doctype html>\n<html lang=\"en\">\n<head>")
    parts.append("<meta charset=\"utf-8\">")
    parts.append("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    parts.append(f"<title>{esc(guide.title)}</title>")
    parts.append(f"<style>{_css()}</style>")
    parts.append("</head>\n<body>")

    state_class = "ok" if report.publishable else "blocked"
    state_text = _state_label(report).replace("_", " ").title()
    parts.append("<header class=\"masthead\">")
    parts.append("<p class=\"eyebrow\">Material Innovation Initiative · Education Guide</p>")
    parts.append(f"<h1>{esc(guide.title)}</h1>")
    parts.append(f"<p class=\"material\">{esc(guide.material)}"
                 + (f" · Updated {esc(str(guide.updated))}" if guide.updated else "") + "</p>")
    parts.append(f"<p class=\"status {state_class}\"><strong>{state_text}</strong> · "
                 f"{summary['claims']} claims · {summary['sources']} sources · "
                 f"{summary['coverage'] * 100:.0f}% coverage · "
                 f"{summary['errors']} errors · {summary['warnings']} warnings</p>")
    parts.append("</header>")
    parts.append("<main>")

    if guide.summary:
        parts.append("<section class=\"brief\"><h2>In brief</h2>"
                     f"<p>{esc(guide.summary.strip())}</p></section>")

    for layer in Audience:
        claims = [c for c in guide.claims if layer in c.audiences]
        if not claims:
            continue
        parts.append(f"<section class=\"layer layer-{layer.value}\">")
        parts.append(f"<h2>{esc(layer.value.title())} layer</h2>")
        parts.append(f"<p class=\"blurb\">{esc(AUDIENCE_BLURB[layer])}</p>")
        for section in guide.sections():
            in_section = [c for c in claims if c.section == section]
            if not in_section:
                continue
            parts.append(f"<h3>{esc(section)}</h3><ul class=\"claims\">")
            for claim in in_section:
                parts.append(_html_claim(guide, claim, layer, numbering))
            parts.append("</ul>")
        parts.append("</section>")

    live = [c for c in report.contradictions if c.is_live]
    if live:
        parts.append("<section class=\"disagreement\"><h2>Where the evidence disagrees</h2>")
        parts.append("<p>These questions are contested. The guide reports the disagreement "
                     "rather than choosing a side.</p>")
        for contradiction in live:
            parts.append("<div class=\"contradiction\">")
            parts.append(f"<h3>{esc(contradiction.topic)}</h3>")
            for label, claims, css in (
                ("Evidence for", contradiction.supporting, "for"),
                ("Evidence against", contradiction.refuting, "against"),
                ("Mixed or conditional", contradiction.mixed, "mixed"),
            ):
                if not claims:
                    continue
                parts.append(f"<h4 class=\"side {css}\">{label}</h4><ul class=\"claims\">")
                for claim in claims:
                    parts.append(_html_claim(guide, claim, Audience.TECHNICAL, numbering))
                parts.append("</ul>")
            parts.append("</div>")
        parts.append("</section>")

    parts.append("<section class=\"sources\"><h2>Sources</h2>")
    parts.append("<p>Numbered in order of first citation. The label on each source is its "
                 "evidence tier.</p><ol class=\"biblio\">")
    for number, source in numbering.ordered(guide):
        resolution = report.resolutions.get(source.id)
        link = (f"<a href=\"{esc(source.locator)}\">{esc(source.locator)}</a>"
                if source.locator else "")
        parts.append(
            f"<li id=\"src-{number}\">{_tier_chip(source.tier)} "
            f"<span class=\"cite\">{esc(_citation_without_locator(source))}</span> {link} "
            f"<span class=\"resolution {_resolution_class(resolution)}\">"
            f"{esc(_resolution_mark(resolution))}</span></li>"
        )
    parts.append("</ol></section>")

    parts.append(_html_method(report))
    parts.append("</main>")
    parts.append(f"<footer><p>Generated {date.today().isoformat()} by the MII guide "
                 "verification pipeline. Every claim above passed the coverage, citation, "
                 "tiering, and consensus gates.</p></footer>")
    parts.append("</body>\n</html>")
    return "\n".join(parts)


def _html_claim(guide: Guide, claim: Claim, audience: Audience, numbering: Numbering) -> str:
    esc = html.escape
    refs = " ".join(
        f"<a class=\"ref\" href=\"#src-{numbering.of(s)}\">{numbering.of(s)}</a>"
        for s in claim.sources if numbering.of(s)
    )
    tier = guide.strongest_tier(claim)
    withheld = ('<span class="withheld">figure withheld pending confirmation</span>'
                if claim.status == "withheld" else "")
    meta = ""
    if audience is not Audience.PUBLIC:
        bits = []
        if tier:
            bits.append(_tier_chip(tier))
        if claim.scope:
            bits.append(f"<span class=\"scope\">scope: {esc(claim.scope)}</span>")
        if bits:
            meta = f"<div class=\"meta\">{' '.join(bits)}</div>"
    return (f"<li><span class=\"statement\">{esc(claim.text_for(audience))}</span> "
            f"{withheld} <span class=\"refs\">{refs}</span>{meta}</li>")


def _html_method(report: VerificationReport) -> str:
    esc = html.escape
    parts = ["<section class=\"method\"><h2>How this guide was verified</h2>"]
    parts.append(
        "<p>Every sentence above is generated from a claim record that carries its own "
        "sources; prose without a source cannot enter the document. Before publication "
        "the guide passes four gates:</p><ol class=\"gates\">"
        "<li><strong>Coverage</strong> — every claim maps to at least one defined source.</li>"
        "<li><strong>Citations</strong> — every DOI resolves against Crossref and its title "
        "and year match what we stored; every URL returns a live response.</li>"
        "<li><strong>Tiering</strong> — every source is ranked by evidence strength, and no "
        "claim may rest on company self-published material alone.</li>"
        "<li><strong>Consensus</strong> — where sources disagree, the disagreement is "
        "surfaced, and no reader layer may show only one side of a contested topic.</li>"
        "</ol>"
    )
    if report.warnings:
        parts.append("<h3>Open caveats carried into publication</h3><ul class=\"caveats\">")
        for finding in report.warnings:
            subject = f"<code>{esc(finding.subject)}</code> — " if finding.subject else ""
            parts.append(f"<li>{subject}{esc(finding.message)}</li>")
        parts.append("</ul>")
    parts.append("</section>")
    return "".join(parts)


def _tier_chip(tier: SourceTier) -> str:
    color = TIER_COLOR[tier]
    return (f"<span class=\"chip\" style=\"--chip:{color}\" "
            f"title=\"{html.escape(tier.description)}\">{html.escape(tier.label)}</span>")


def _citation_without_locator(source: Source) -> str:
    citation = source.citation()
    if source.locator and citation.endswith(source.locator):
        citation = citation[: -len(source.locator)].rstrip(". ")
    return citation


def _resolution_class(resolution) -> str:
    if resolution is None:
        return "none"
    if resolution.status == "resolved" and not resolution.metadata_conflict:
        return "ok"
    return "unchecked" if resolution.status == "unchecked" else "bad"


def _css() -> str:
    return f"""
:root {{
  --primary: {BRAND['primary']};
  --secondary: {BRAND['secondary']};
  --deep: {BRAND['deep']};
  --amber: {BRAND['amber']};
  --coral: {BRAND['coral']};
  --sage: {BRAND['sage']};
  --ink: #1b1f2a;
  --muted: #5c6474;
  --bg: #ffffff;
  --panel: #f7f6f4;
  --rule: #e4e2df;
  color-scheme: light dark;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --ink:#eceef3; --muted:#a4acbd; --bg:#14161d; --panel:#1c1f28; --rule:#2c313d; }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--bg); color: var(--ink);
  font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}}
main, .masthead, footer {{ max-width: 62rem; margin: 0 auto; padding: 0 1.5rem; }}
.masthead {{ padding-top: 3rem; padding-bottom: 1.5rem; border-bottom: 3px solid var(--primary); }}
.eyebrow {{
  margin: 0; color: var(--primary); font-size: .75rem; font-weight: 700;
  letter-spacing: .12em; text-transform: uppercase;
}}
h1 {{ margin: .4rem 0 .3rem; font-size: 2.3rem; line-height: 1.15; letter-spacing: -.02em; }}
.material {{ margin: 0 0 1rem; color: var(--muted); }}
.status {{
  display: inline-block; margin: 0; padding: .5rem .9rem; border-radius: .4rem;
  font-size: .875rem; background: var(--panel); border-left: 4px solid var(--sage);
}}
.status.blocked {{ border-left-color: var(--primary); }}
h2 {{ margin: 2.5rem 0 .6rem; font-size: 1.4rem; letter-spacing: -.01em; }}
h3 {{ margin: 1.6rem 0 .5rem; font-size: 1.08rem; color: var(--deep); }}
@media (prefers-color-scheme: dark) {{ h3 {{ color: var(--secondary); }} }}
h4 {{ margin: 1rem 0 .3rem; font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; }}
.blurb, .brief p {{ color: var(--muted); }}
.layer {{ padding: 1.25rem 1.5rem; margin-top: 1.5rem; background: var(--panel); border-radius: .6rem; }}
ul.claims {{ list-style: none; margin: 0; padding: 0; }}
ul.claims > li {{ padding: .6rem 0; border-bottom: 1px solid var(--rule); }}
ul.claims > li:last-child {{ border-bottom: none; }}
.refs {{ white-space: nowrap; }}
a.ref {{
  display: inline-block; min-width: 1.25rem; padding: 0 .3rem; margin-left: .15rem;
  border-radius: .25rem; background: var(--deep); color: #fff; font-size: .7rem;
  font-weight: 700; text-align: center; text-decoration: none; vertical-align: super;
}}
.meta {{ margin-top: .35rem; font-size: .78rem; color: var(--muted); }}
.chip {{
  display: inline-block; padding: .1rem .5rem; border-radius: 1rem;
  background: color-mix(in srgb, var(--chip) 16%, transparent);
  border: 1px solid var(--chip);
  /* The lighter brand tones are unreadable as text on a light panel, so the pure
     hue carries the border and fill while the label is darkened toward the ink. */
  color: color-mix(in srgb, var(--chip) 72%, var(--ink));
  font-size: .7rem; font-weight: 700; letter-spacing: .03em;
}}
@media (prefers-color-scheme: dark) {{
  .chip {{ color: color-mix(in srgb, var(--chip) 60%, #ffffff); }}
}}
.scope {{ margin-left: .4rem; }}
.withheld {{
  display: inline-block; padding: .05rem .45rem; border-radius: .25rem;
  background: color-mix(in srgb, var(--amber) 22%, transparent);
  border: 1px solid var(--amber); font-size: .7rem; font-weight: 700;
  color: color-mix(in srgb, var(--amber) 70%, var(--ink));
}}
.contradiction {{ padding: 1rem 1.25rem; margin: 1rem 0; border-left: 4px solid var(--amber); background: var(--panel); border-radius: 0 .5rem .5rem 0; }}
.side.for {{ color: var(--sage); }}
.side.against {{ color: var(--primary); }}
.side.mixed {{ color: var(--amber); }}
ol.biblio {{ padding-left: 1.4rem; }}
ol.biblio li {{ padding: .5rem 0; border-bottom: 1px solid var(--rule); }}
ol.biblio a {{ color: var(--deep); word-break: break-word; }}
@media (prefers-color-scheme: dark) {{ ol.biblio a {{ color: var(--secondary); }} }}
.resolution {{ font-size: .75rem; color: var(--muted); }}
.resolution.ok {{ color: var(--sage); }}
.resolution.bad {{ color: var(--primary); font-weight: 700; }}
.method {{ margin-top: 2.5rem; padding: 1.25rem 1.5rem; background: var(--panel); border-radius: .6rem; }}
ol.gates li, ul.caveats li {{ margin: .4rem 0; }}
footer {{ margin: 3rem auto; padding-top: 1.25rem; border-top: 1px solid var(--rule); color: var(--muted); font-size: .82rem; }}
"""
