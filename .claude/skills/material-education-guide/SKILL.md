---
name: material-education-guide
description: Research and build a verifiable education guide for a next-gen material, where every published sentence is generated from a claim that carries its own sources. Also reviews and fact-checks documents that already exist. Use when asked for an education guide, explainer, or fact-checked briefing on a material (e.g. "build an education guide on mycelium leather"); when asked to verify, fix, or update a guide spec in guides/; or when asked to check, review, or audit the citations in an existing report, draft, or Word/PDF document. Produces a YAML claim spec that passes four automated gates - coverage, citation resolution, source tiering, and contradiction surfacing - then renders it to Markdown and HTML.
---

# Material education guide

Build an education guide whose correctness is enforced by code rather than by care.

The pipeline in this repository inverts the usual order. You do not write prose and
then add citations; you write **claims**, each carrying its sources, and the prose is
generated from them. An unsourced sentence cannot reach the page, because there is no
code path that puts one there.

## The four gates

A guide is publishable only when it passes all four. `mii-guide verify` runs them.

| Gate | Blocks publication when |
|---|---|
| **Coverage** | a claim has no sources, or cites a source the guide does not define |
| **Citations** | a DOI does not resolve, or resolves to a different title or year |
| **Tiering** | a claim rests only on company self-published material |
| **Consensus** | one reader layer shows only one side of a contested topic |

Warnings do not block, but they are printed into the published guide as open caveats,
so shipping with them is a visible choice rather than a silent one.

## Workflow

### 1. Scaffold

```bash
python -m mii_guide new <slug> --title "..." --material "..."
```

### 2. Research, then write claims — not prose

For each thing the guide will say, write one claim. Give it:

- `statement` — the technical phrasing, as a specialist would put it.
- `plain` — the same assertion for a reader with no background. Not a simplification
  that changes the meaning; the same claim in ordinary words.
- `scope` — the qualifier that keeps it honest: system boundary, geography, timeframe.
  A claim without scope is where misleading guides start.
- `sources` — the ids that carry it.
- `audiences` — which reader layers see it. Default is all three.

**Never invent a citation.** If you cannot name a specific real source, do not write
the claim. A DOI you are not certain of is worse than no claim, because the citation
gate is what readers will trust. Where you are unsure, cite the source you *do* have
and let the tiering gate report the evidence as weak.

**Do not set `accessed:`** unless a person has actually opened the source. It is an
attestation, not metadata.

### 3. Tier every source honestly

`peer_reviewed` › `regulator` › `institutional` › `industry_lca` › `trade_press` › `company`

Tier by what the source *is*, not by how much you want the claim to stand. A company
LCA is `industry_lca` or `company` even when it is rigorous. The tier is how a reader
judges the claim, so inflating it defeats the whole document.

### 4. Surface disagreement instead of resolving it

Where the literature genuinely disagrees, give the competing claims a shared `topic`
and opposing `stance` values (`supports` / `refutes` / `mixed`). The renderer builds a
"Where the evidence disagrees" section from them.

The consensus gate will block you if a contested topic reaches one reader layer with
only one side visible. That is deliberate: a public layer that shows only the
favourable half of a contested question misleads even when the technical layer is
complete. Either include an opposing claim in that layer, or drop the topic from it.

### 5. Verify, then build

```bash
python -m mii_guide verify guides/<slug>.yaml --online   # resolve every DOI and URL
python -m mii_guide build guides/<slug>.yaml --out dist/ --online
```

Iterate until `verify` exits 0. Do not reach for `--allow-unverified` to get an output
file; it watermarks the guide BLOCKED and still exits non-zero.

If `--online` cannot reach Crossref (a sandboxed or policy-restricted network), say so
plainly and label the result provisional. An offline pass checks structure only — it
is not evidence that the citations exist, and the renderer labels it `PROVISIONAL`
rather than `VERIFIED` for exactly that reason.

### 6. Report what is still weak

When you hand the guide over, state: how many claims rest on non-primary evidence,
which topics are contested, and which citations were not confirmed online. The
verification report (`--json`) has all of it. A guide whose weaknesses are stated is
more useful than one that hides them.

## Reviewing a document that already exists

When the user brings a finished document rather than asking for a new guide, the
work splits in two, and the split must stay visible in what you report.

### Mechanical half: run the audit

```bash
python -m mii_guide audit <file> --online
```

Reads `.md`, `.txt`, `.html`, `.docx`, `.pdf`. It resolves every DOI and URL and
reports dead links, DOIs Crossref has never heard of, references whose line
describes a different work from the one the DOI points to, and the evidence tier
of each domain.

**Check the extraction confidence before reporting anything.** If the run says
`best-effort`, a clean result is not a clean document — say so, and ask for a
`.docx` export or install `pypdf`.

### Reading half: extract the claims yourself

The audit deliberately does not judge whether a sentence needs a citation. Read
the document and report:

- assertions carrying no source, especially ones with a number in them
- claims resting only on company self-published material
- contested questions presented as settled
- claims stated without the scope that makes them true (a cradle-to-gate figure
  presented as a whole-life figure is the classic case)

**Label these as your reading, not as gate results.** The audit's findings are
facts about references; yours are judgments about prose. Presenting them as the
same kind of thing makes the facts worth less.

If the document is worth maintaining, offer to convert it into a guide spec so it
becomes re-checkable — citations rot, and finished prose cannot be re-verified.

## Relationship to `what-the-science-says`

That skill writes a prose report for publication. This one produces a structured,
machine-verifiable claim base and renders from it. Use this when the guide must be
re-checkable later — citations rot, and a spec can be re-verified on a schedule where
finished prose cannot.
