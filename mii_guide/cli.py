"""Command line interface: verify guide specs, and build them into guides.

    mii-guide verify guides/                 # offline structural pass
    mii-guide verify guides/ --online        # resolve every DOI and URL
    mii-guide build guides/recycled-polyester.yaml --out dist/ --online
    mii-guide new bio-based-leather          # scaffold a new spec
    mii-guide sources guides/ --tier company # audit what rests on marketing
    mii-guide audit report.docx --online     # check an existing document's citations

Exit codes: 0 clean, 1 verification errors, 2 bad input or usage.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import audit as audit_document
from .extract import SUPPORTED, ExtractionError
from .loader import GuideLoadError, discover, load_guide
from .models import Audience, SourceTier
from .render import render_html, render_markdown
from .resolve import CitationResolver
from .verify import Severity, VerificationReport, verify

DEFAULT_CACHE = Path(".mii-guide-cache.json")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    try:
        return args.handler(args)
    except GuideLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:  # pragma: no cover
        print("interrupted", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mii-guide",
        description="Build verifiable material-innovation education guides.",
    )
    sub = parser.add_subparsers(dest="command")

    verify_cmd = sub.add_parser("verify", help="run the verification gates over guide specs")
    _add_common(verify_cmd)
    verify_cmd.add_argument("--json", action="store_true", help="emit the report as JSON")
    verify_cmd.add_argument("--strict", action="store_true",
                            help="treat warnings as failures too")
    verify_cmd.set_defaults(handler=cmd_verify)

    build_cmd = sub.add_parser("build", help="verify, then render guides to disk")
    _add_common(build_cmd)
    build_cmd.add_argument("--out", default="dist", help="output directory (default: dist)")
    build_cmd.add_argument("--format", default="md,html,json",
                           help="comma-separated: md, html, json (default: all three)")
    build_cmd.add_argument("--audience", choices=[a.value for a in Audience],
                           help="render only one reader layer in the Markdown output")
    build_cmd.add_argument("--allow-unverified", action="store_true",
                           help="render even when verification found errors "
                                "(the output is watermarked BLOCKED)")
    build_cmd.set_defaults(handler=cmd_build)

    new_cmd = sub.add_parser("new", help="scaffold a new guide spec")
    new_cmd.add_argument("slug", help="short identifier, e.g. recycled-polyester")
    new_cmd.add_argument("--title", help="guide title")
    new_cmd.add_argument("--material", help="material name")
    new_cmd.add_argument("--dir", default="guides", help="where to write it (default: guides)")
    new_cmd.set_defaults(handler=cmd_new)

    sources_cmd = sub.add_parser("sources", help="list every source and its evidence tier")
    sources_cmd.add_argument("paths", nargs="+", help="guide files or directories")
    sources_cmd.add_argument("--tier", help="show only this tier (e.g. company, peer_reviewed)")
    sources_cmd.set_defaults(handler=cmd_sources)

    audit_cmd = sub.add_parser(
        "audit",
        help="check the citations in an existing document (.md/.docx/.pdf/.html)",
    )
    audit_cmd.add_argument("paths", nargs="+", help="documents to audit")
    audit_cmd.add_argument("--online", action="store_true",
                           help="resolve DOIs against Crossref and probe URLs over HTTP")
    audit_cmd.add_argument("--cache", default=str(DEFAULT_CACHE), help="citation cache file")
    audit_cmd.add_argument("--no-cache", action="store_true",
                           help="ignore and do not write the cache")
    audit_cmd.add_argument("--json", action="store_true", help="emit the report as JSON")
    audit_cmd.add_argument("--facts-only", action="store_true",
                           help="hide heuristic flags and show only established problems")
    audit_cmd.set_defaults(handler=cmd_audit)

    return parser


def _add_common(cmd: argparse.ArgumentParser) -> None:
    cmd.add_argument("paths", nargs="+", help="guide files or directories")
    cmd.add_argument("--online", action="store_true",
                     help="resolve DOIs against Crossref and probe URLs over HTTP")
    cmd.add_argument("--cache", default=str(DEFAULT_CACHE),
                     help=f"citation cache file (default: {DEFAULT_CACHE})")
    cmd.add_argument("--no-cache", action="store_true", help="ignore and do not write the cache")


# -- commands ---------------------------------------------------------------

def cmd_verify(args: argparse.Namespace) -> int:
    reports = _run(args)
    if args.json:
        print(json.dumps([r.to_dict() for r in reports], indent=2))
    else:
        for report in reports:
            _print_report(report)
    return _exit_code(reports, strict=args.strict)


def cmd_build(args: argparse.Namespace) -> int:
    formats = {f.strip().lower() for f in args.format.split(",") if f.strip()}
    unknown = formats - {"md", "html", "json"}
    if unknown:
        print(f"error: unknown format(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    reports = _run(args)
    audience = Audience.parse(args.audience) if args.audience else None
    written: list[Path] = []

    for report in reports:
        _print_report(report)
        if not report.publishable and not args.allow_unverified:
            print(f"  not rendered: fix the {len(report.errors)} error(s) above, "
                  f"or pass --allow-unverified\n", file=sys.stderr)
            continue
        slug = report.guide.slug
        if "md" in formats:
            path = out_dir / f"{slug}.md"
            path.write_text(render_markdown(report, audience), encoding="utf-8")
            written.append(path)
        if "html" in formats:
            path = out_dir / f"{slug}.html"
            path.write_text(render_html(report), encoding="utf-8")
            written.append(path)
        if "json" in formats:
            path = out_dir / f"{slug}.report.json"
            path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
            written.append(path)

    for path in written:
        print(f"wrote {path}")
    return _exit_code(reports, strict=False)


def cmd_new(args: argparse.Namespace) -> int:
    slug = args.slug.strip().lower().replace(" ", "-")
    target = Path(args.dir) / f"{slug}.yaml"
    if target.exists():
        print(f"error: {target} already exists", file=sys.stderr)
        return 2
    target.parent.mkdir(parents=True, exist_ok=True)
    title = args.title or f"What the evidence says about {slug.replace('-', ' ')}"
    material = args.material or slug.replace("-", " ")
    target.write_text(_scaffold(slug, title, material), encoding="utf-8")
    print(f"wrote {target}")
    print("Next: fill in sources and claims, then run "
          f"`mii-guide verify {target} --online`")
    return 0


def cmd_sources(args: argparse.Namespace) -> int:
    wanted = SourceTier.parse(args.tier) if args.tier else None
    guides = [load_guide(p) for p in _expand(args.paths)]
    rows: list[tuple[str, str, str, str]] = []
    for guide in guides:
        cited = guide.cited_source_ids()
        for source in sorted(guide.sources.values(), key=lambda s: (s.tier.rank, s.id)):
            if wanted and source.tier is not wanted:
                continue
            use = "cited" if source.id in cited else "unused"
            rows.append((guide.slug, source.tier.label, source.id, f"{source.title} ({use})"))

    if not rows:
        print("no sources matched")
        return 0
    widths = [max(len(r[i]) for r in rows) for i in range(3)]
    for row in rows:
        print(f"{row[0]:<{widths[0]}}  {row[1]:<{widths[1]}}  {row[2]:<{widths[2]}}  {row[3]}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    cache = None if args.no_cache else Path(args.cache)
    resolver = CitationResolver(online=args.online, cache_path=cache)
    reports = []
    for raw in args.paths:
        try:
            reports.append(audit_document(Path(raw), resolver))
        except ExtractionError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps([r.to_dict() for r in reports], indent=2))
    else:
        for report in reports:
            _print_audit(report, facts_only=args.facts_only)
    return 1 if any(r.errors for r in reports) else 0


def _print_audit(report, facts_only: bool) -> None:
    summary = report.summary()
    state = "CLEAN" if report.clean else "PROBLEMS"
    print(f"{state}  {summary['document']}  —  {summary['references']} references "
          f"({summary['dois']} DOIs, {summary['urls']} URLs), "
          f"{summary['errors']} errors, {summary['warnings']} warnings")

    if summary["extraction"] != "full":
        print("  ! extraction was best-effort: a clean result here is not proof of a "
              "clean document")
    if not report.online:
        print("  ! offline run: references were checked for shape only, not resolved")

    for finding in report.findings:
        if facts_only and finding.kind != "fact":
            continue
        location = f" (line {finding.line})" if finding.line else ""
        print(f"  {finding}{location}")
        if finding.hint and finding.severity != "info":
            print(f"        → {finding.hint}")

    tiers = summary["tiers"]
    if tiers:
        print("  tiers (inferred from domain, confirm by hand): "
              + ", ".join(f"{k}={v}" for k, v in tiers.items()))
    print()


# -- plumbing ---------------------------------------------------------------

def _run(args: argparse.Namespace) -> list[VerificationReport]:
    paths = _expand(args.paths)
    if not paths:
        raise GuideLoadError("no guide specs found in the given paths")
    cache = None if args.no_cache else Path(args.cache)
    resolver = CitationResolver(online=args.online, cache_path=cache)
    return [verify(load_guide(p), resolver) for p in paths]


def _expand(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            found.extend(discover(path))
        else:
            found.append(path)
    return found


def _print_report(report: VerificationReport) -> None:
    summary = report.summary()
    state = "PASS" if report.publishable else "FAIL"
    print(f"{state}  {summary['guide']}  —  {summary['claims']} claims, "
          f"{summary['sources']} sources, {summary['coverage'] * 100:.0f}% coverage")
    for finding in report.findings:
        if finding.severity is Severity.INFO and report.publishable:
            # Keep the default output actionable; INFO detail lives in --json.
            continue
        print(f"  {finding}")
        if finding.hint and finding.severity is not Severity.INFO:
            print(f"        → {finding.hint}")
    print()


def _exit_code(reports: list[VerificationReport], strict: bool) -> int:
    if any(r.errors for r in reports):
        return 1
    if strict and any(r.warnings for r in reports):
        return 1
    return 0


def _scaffold(slug: str, title: str, material: str) -> str:
    return f"""# Guide spec for {material}.
# Prose is generated from these claims, so every sentence that reaches the page
# carries its sources with it. Run `mii-guide verify` before publishing.

slug: {slug}
title: "{title}"
material: "{material}"
summary: >
  One paragraph a non-specialist can read and come away with the honest answer.
updated: "YYYY-MM-DD"
reviewers: []

section_order:
  - What it is
  - Environmental performance
  - Trade-offs
  - What is still unknown

sources:
  - id: example-2024
    tier: peer_reviewed        # peer_reviewed | regulator | institutional |
                               # industry_lca | trade_press | company
    title: "Full title exactly as published"
    authors: ["Surname, A.", "Surname, B."]
    year: 2024
    container: "Journal Name"
    doi: "10.xxxx/xxxxx"
    accessed: "YYYY-MM-DD"

claims:
  - id: c1
    section: What it is
    statement: "The technical statement, as a specialist would phrase it."
    plain: "The same statement, for a reader with no background."
    scope: "The system boundary, geography, or timeframe that keeps it honest."
    sources: [example-2024]
    topic: null                # set a shared topic to group competing claims
    stance: neutral            # supports | refutes | mixed | neutral
    audiences: [public, industry, technical]
"""
