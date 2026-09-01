# MII Guide

Build education guides about next-generation materials where correctness is enforced
by code rather than by care.

## The idea

Most fact-checked writing works like this: draft the prose, then attach citations to
it. The citations are a layer on top, and nothing stops a sentence from losing its
source in an edit.

This pipeline inverts that. A guide is a set of **claims**, each carrying its own
sources. The prose is *generated* from the claims. There is no code path that puts an
unsourced sentence on the page, so "every claim is sourced" is a structural property
of the document rather than a promise about the editing process.

Four gates then run before anything is published.

| Gate | Question it answers | Blocks publication when |
|---|---|---|
| **Coverage** | Is every claim attached to a source? | a claim has no sources, or cites one the guide never defines |
| **Citations** | Do those sources exist, and say what we said? | a DOI does not resolve, or resolves to a different title or year |
| **Tiering** | How strong is the evidence? | a claim rests only on company self-published material |
| **Consensus** | Where sources disagree, do we admit it? | one reader layer shows only one side of a contested topic |

Errors block. Warnings publish, but they are printed into the guide itself as open
caveats — shipping with a weakness is a visible choice, not a silent one.

## Quick start

```bash
pip install -e .          # add --no-build-isolation on a host without a package index

mii-guide verify guides/                      # structural pass, no network
mii-guide verify guides/ --online             # resolve every DOI and URL
mii-guide build guides/recycled-polyester.yaml --out dist/ --online
```

`verify` exits 0 when clean, 1 when a gate blocks, 2 on bad input — so it drops
straight into CI.

Without installing:

```bash
python -m mii_guide verify guides/
```

## Commands

| Command | Purpose |
|---|---|
| `mii-guide verify PATH... [--online] [--json] [--strict]` | run the gates; `--strict` fails on warnings too |
| `mii-guide build PATH... --out DIR [--format md,html,json] [--audience public]` | verify, then render |
| `mii-guide new SLUG` | scaffold a guide spec |
| `mii-guide sources PATH... [--tier company]` | audit what the guide rests on |

`--online` resolves DOIs against Crossref and probes URLs. Results are cached in
`.mii-guide-cache.json` for 30 days, so reruns are fast and reproducible offline.

## Writing a guide

```yaml
slug: recycled-polyester
title: "Recycled Polyester: What the Evidence Actually Supports"
material: "Recycled polyester (rPET) in apparel and footwear"

sources:
  - id: napper-thompson-2016
    tier: peer_reviewed
    title: "Release of synthetic microplastic plastic fibres from domestic washing machines"
    authors: ["Napper, I.E.", "Thompson, R.C."]
    year: 2016
    container: "Marine Pollution Bulletin"
    doi: "10.1016/j.marpolbul.2016.09.025"

claims:
  - id: microfibre-shedding
    section: What it does not do
    statement: "Synthetic textiles release microfibres during domestic laundering..."
    plain: "Clothes made from it still shed tiny plastic fibres in the wash."
    scope: "Domestic washing of polyester fabrics"
    sources: [napper-thompson-2016]
    audiences: [public, industry, technical]
```

### Evidence tiers

`peer_reviewed` › `regulator` › `institutional` › `industry_lca` › `trade_press` › `company`

The first three count as independent primary evidence. A claim resting only on
`company` sources is blocked; the fix is either independent evidence or restating it
as *"the company states that…"* so the reader can see whose claim it is.

### Reader layers

One guide, three layers — `public`, `industry`, `technical`. Each claim declares which
layers it appears in, and `plain` supplies the non-specialist wording. Because both
phrasings live on the same claim record, the layers cannot drift apart the way two
separate documents would.

### Contested topics

Give competing claims a shared `topic` and opposing `stance` values:

```yaml
  - id: circularity-supports
    topic: "does bottle-to-textile recycling advance circularity"
    stance: supports
    # ...
  - id: circularity-refutes
    topic: "does bottle-to-textile recycling advance circularity"
    stance: refutes
```

The renderer builds a *"Where the evidence disagrees"* section from these. The
consensus gate blocks publication if a contested topic reaches any reader layer with
only one side visible — a public layer showing only the favourable half misleads even
when the technical layer is complete.

## `scope` matters

Every claim should carry the qualifier that keeps it honest — system boundary,
geography, timeframe. *"Lower emissions"* is where misleading guides begin;
*"lower emissions, cradle-to-gate fibre production only, excluding dyeing and use
phase"* is a claim a reader can actually check. A missing `scope` is reported as an
INFO finding on every claim.

## `accessed` is an attestation

Set `accessed:` only when a person has actually opened the source. It is the guide's
record that a human looked, not a metadata field to fill in for completeness.

## Provisional vs. verified

An offline run checks structure only — DOI shape, URL shape, coverage, tiering,
consensus. It is **not** evidence that the citations exist. Guides built without
`--online` are labelled `PROVISIONAL` rather than `VERIFIED`, and each source is
marked *not yet checked online*.

> **The shipped example has not passed the online gate.** This repository was built in
> a sandbox whose egress policy blocks `api.crossref.org`, so the references in
> `guides/recycled-polyester.yaml` are unconfirmed. Run
> `mii-guide verify guides/ --online` on a network that can reach Crossref before
> treating that guide as verified, and add `accessed:` dates only for sources someone
> has actually read.

## Development

```bash
python -m unittest discover -s tests -t tests
```

136 tests, no third-party test dependency. Network access is faked in tests, so the
suite runs offline and deterministically.

### Layout

```
mii_guide/
  models.py    Claim, Source, Guide, tiers, stances, reader layers
  loader.py    YAML/JSON specs -> Guide, with errors that name the file
  resolve.py   Crossref + HTTP citation resolution, cached
  verify.py    the four gates
  render.py    Markdown and HTML output in MII brand colours
  cli.py       verify / build / new / sources
guides/        guide specs
tests/         136 tests
.claude/skills/material-education-guide/   Claude Code skill wrapper
```

## Using it from Claude Code

The skill at `.claude/skills/material-education-guide/` walks through researching a
material, writing claims, tiering sources honestly, and iterating until the gates
pass. Ask for *"an education guide on mycelium leather"* and it will follow that loop.
