# Output specification

Read before building. Three deliverables, all handed to the user, named exactly:

| Deliverable | File or folder name |
|---|---|
| **(a) The analysis report** | `MII Company Analysis Report_[Company Name].docx` — the master document MII edits; PDF for distribution is exported from Word after MII's edits, never generated separately |
| **(b) The company document** | `MII Company Analysis Report_[Company Name]_Questions.docx` |
| **(c) The source screenshot folder** | `MII Company Analysis Report_[Company Name]_Source Screenshots/` |

**(a) The analysis report**, for MII's audiences: what MII found, fully cited, structured as (a-1) through (a-8) below and containing nothing beyond them. Every sentence of visible text is written for the report's external audience, investors and brands. Nothing in the visible text addresses MII, evaluates MII's own research practice, or explains why a finding matters to MII specifically or "to this report type." That content is a pre-publication note, never body prose. This principle governs the whole report; (a-6) below names the specific ways it tends to get broken.

**(b) The company document**: sent to the company by email before publication, giving them the opportunity to review the report and MII's questions and respond. It contains the contradictions and gaps this research found, with enough in each entry that the company can find the issue and understand why it matters, plus the standard documents to request. This is its own file, handed over separately from (a), not a section within it.

**(c) The source screenshot folder**: one image per cited passage, so a reviewer can see where a fact sits without re-running the research.

This file holds the full structure, formatting and house style for all three. `SKILL.md` holds the workflow that produces the material each of these draws on.

## (a) The analysis report

**One `.docx`, built with the `docx` skill under the fixed design below, never freestyled.** The Word file is the master document: MII makes its edits there, and the distribution copy is a PDF exported from Word after those edits, which locks the layout and embeds the fonts. Fixed reader-facing text is reproduced word for word in every report: the About paragraph, the disclaimer, the section captions, the confidence key definitions and the risk-table footnote line. Add no sections, delete none, reorder none, restyle none.

The structure is closed at (a-1) through (a-8) below, matching the template exactly.

**The design** mirrors MII's report template: two typefaces, hairline rules, bar-meter confidence. Both fonts are free Google fonts; embed them in the `.docx` (Word's font embedding) so the file renders identically on machines without them installed.

| Element | Spec |
|---|---|
| Page | US Letter, 1" margins, page number centered in the footer, 8pt Libre Franklin |
| Typefaces | **Newsreader** for all body text, headings, findings, endnotes; **Libre Franklin semibold, uppercase, letter-spaced** for every label: kicker, cover field names, tile labels, table headers, grid cell headings, confidence labels, the words "Confidence key" and "Milestones" |
| Body text | 11pt Newsreader `#2B2F3A`, 1.15 line spacing, 8pt space after paragraphs, left-aligned, no first-line indent |
| Cover | MII logo (`assets/mii-logo.png` in this skill); kicker "COMPANY ANALYSIS REPORT"; company name 28pt bold `#283D6B`; descriptor italic gray; label + value lines for dates and prepared-by; About paragraph and disclaimer at 9.5pt gray |
| Section headings (a-2)–(a-8) | 17pt bold `#283D6B` with a navy bottom rule, each starting a new page |
| Topic headings | Number in Libre Franklin bold `#9A2866`, name 13.5pt bold `#283D6B` |
| Material/jurisdiction subheadings | 11.5pt bold italic `#9A2866` |
| Confidence rendering | Bar meters, four segments: filled `#283D6B` (`#9A2866` for Unconfirmed and Not Established), empty `#DBE0EA`; Verified 4, Likely 3, Unconfirmed 2, Not Established 1; label beneath in Libre Franklin matching the fill colour |
| Scorecard | No cell fills: Libre Franklin header row over a 1.25pt navy rule, hairline `#E1E6EF` row rules, unsplittable rows, header repeating across page breaks, bar meter + label in the Confidence column |
| Company at a Glance | 3×3 hairline-bordered tiles: label, bold navy value 13pt, gray sub-note |
| Assessment grid | 2×2 table ruled in `#CFD5E2`, Libre Franklin navy cell headings |
| Milestones | Two-column, year in Libre Franklin bold `#9A2866`, hairline row rules |
| Funding and Risk tables | Same treatment as the scorecard |
| Endnotes | 9pt Newsreader, hanging indent, number in Libre Franklin bold `#9A2866`, numbered by position |

Pre-publication notes are real anchored margin comments: build the document first with zero pre-publication content in visible text, then add each note with the `docx` skill's comment tooling, anchored to the exact sentence, cell or endnote it concerns, and the checks comment anchored to the company name on the cover. Verify before delivering: `word/comments.xml` contains one `<w:comment>` per note and `word/document.xml` one matching anchor for each, counted directly, not assumed.

**(a-1) Cover.** The MII logo, the fixed kicker "Company Analysis Report", the company name, and a one-line descriptor of what the company makes and which next-gen material category it belongs to, written as a plain factual noun phrase with no marketing adjectives. Then the research-completed and intended-publication dates, the prepared-by line, the fixed contents block, and these two paragraphs, both **VERBATIM** in every report:

> The Material Innovation Initiative (MII) is a nonprofit think tank accelerating the development of environmentally preferable, animal-free next-gen materials for the fashion, automotive, and home goods industries. MII provides investors, brands, and scientists with research and analysis on next-gen material technologies and the companies developing them. This report is part of that work: a fully cited evaluation built with the discipline of a due diligence review, asking the questions we would want answered if we were in your position.

> The information provided in this report is for general information purposes only. The Material Innovation Initiative is not a registered investment adviser and cannot transact business as an investment adviser or give investment advice. Any document or information created or shared by MII does not constitute advice concerning the value of any security or the advisability of buying, selling or otherwise investing in any security. In addition, any legal reference in this report is provided for general information only and reflects MII's understanding as of the research date stated above. Nothing in this report is a legal opinion or a substitute for advice from qualified counsel licensed in the relevant jurisdiction, and no reader should act or refrain from acting on the basis of it without obtaining such advice. All information in this report is provided in good faith; however, we make no representation or warranty regarding the accuracy or completeness of this information. If you would like to contact us about the contents of this report, please email info@materialinnovation.org.

**(a-2) Note on Sources.** Placed here, at the front, because a reader reaching the scorecard needs to already know how sources are graded. State: which categories were treated as company-reported (sponsored content, vendor profiles, press releases, self-maintained database profiles); that negative findings reflect searches on a named date and should be re-verified; any retrieval limitation that affects the findings, including database search tools that could not be operated; and, if more than half the citation uses in the report are `[Industry/self-reported]`, say so and explain why. For a pre-validation company that is often legitimate and unavoidable; it still has to be visible to the reader rather than something they would have to count for themselves.

**(a-3) Company at a Glance.** Two tile panels on the same page. Every figure in both restates a cited finding from the Findings section and keeps its endnote number; the panels introduce nothing new. Leave a tile blank rather than estimating: an empty tile is itself a finding, and usually corresponds to a Not Established row in the scorecard; an estimated one is fabrication. Do not add a caption explaining the panels; the tiles carry their own labels.

The first panel is the company panel: incorporated, headquarters, headcount, disclosed funding, production stage, major clients, certified biobased content, technology readiness, environmental impact. Where the registered office differs from the stated headquarters, the headquarters tile carries the headquarters and its subtitle names the registered office, so both appear without a second tile.

The second panel is headed **Sourcing Details** and carries the material's commercial and physical specification, drawn from the company's MII Sourcing Hub data sheet where one exists: material name, biomimicry, price, minimum order quantity, lead time, sample availability, production capacity, production location, width, roll length, thickness, weight, colours, embossing and texture options, and tanning method. Add or drop cells to match what the source actually provides rather than padding to fill the grid. Close the panel with one italic line stating that these figures are company-reported to the Hub and not verified by MII, naming any exception that MII has verified independently.

Where a company has no Sourcing Hub sheet, omit the second panel entirely rather than filling it from marketing copy.

**The biomimicry cell names the incumbent material being mimicked, not whether biomimicry is used.** "Yes" is not an answer, because every next-gen material in scope mimics something and the useful information is which thing. Name the incumbent the material is engineered to replace: leather, wool, silk, fur, down, or the synthetic it competes against where that is the closer comparator (acrylic for wool, polyester for silk). Use the same incumbent that Performance vs. Incumbent benchmarks against, so the two do not disagree. Where a company positions one material against more than one incumbent, name the primary one and let that topic carry the rest.

**(a-4) MII Recommendation.** Two to five paragraphs on the main advantages of the materials and company, and MII's main concerns. The recommendation itself is MII's own analysis and does not need its own citation, in the same way a risk ranking is treated as an assessment elsewhere in this skill; any specific figure restated here still carries a citation, per Sourcing Rule 10. This section is extremely important, since MII's reputation rests on it and it is the section that gets quoted most.

Below it, **the MII assessment grid**, the template's fixed four-cell layout: Strengths, Weaknesses, Opportunities, Threats. Two to four entries per cell, each traceable to a cited finding in this report. A weakness is not the same as an unverified claim: an unverified claim belongs in Open Questions and the company document, not in the Weaknesses cell. The Threats cell carries the risk analysis for the whole report: the three to five biggest risks to the company and the material, ranked. That selection and ranking is MII's own analysis and does not itself need a citation, in line with how a risk ranking is treated as an assessment elsewhere in this skill, but every factual claim supporting a risk must be traceable to a cited finding in the Findings section. Treat this cell as the most important in the grid, since MII's reputation rests on it and it is the part that gets quoted most; where more than four risks are worth stating, the surplus belongs in Open Questions rather than being compressed out. Like the recommendation, the grid carries no citations of its own, and any specific figure restated in it keeps its endnote.

**(a-5) The scorecard.** Columns: `Topic | Finding | Confidence`. One row per topic, ten rows, in topic order, except that Topic 5 is split across five rows, one per fixed subheading (Water Use, Emissions, Chemical Use, Biobased Content, End of Life), each with its own finding and its own confidence rating. Fourteen rows in total.

The rows are grouped under the five section headings set out in `SKILL.md`: **A. The Company** (topics 1 to 2), **B. The Material** (3 to 4), **C. Sustainability** (5a to 5e), **D. Commercial Readiness** (6 to 8), **E. Legal Position** (9 to 10). Each heading is a full-width row spanning all three columns, carrying the section letter and title, ruled beneath. The grouping exists so the reader can see the confidence pattern by area rather than as one undifferentiated list. Do not add a section-level verdict or a blended confidence rating: collapsing five ratings into one is exactly what splitting Sustainability was meant to prevent. Because topic numbers run sequentially through the section order, they read top to bottom without gaps; if you ever reorder the topics, renumber them in `SKILL.md` at the same time rather than leaving the scorecard non-sequential.

Per-assertion sourcing: where a Finding cell contains more than one assertion, attach the endnote number to each assertion inside the cell, not as a block at the end of the row. A reader must be able to tell which source supports which assertion without leaving the table. If that is unworkable for a topic, split it across rows. This matters more than it sounds: in the audited report, a single row asserted five things and carried three endnotes at the end, and three of the five turned out to be unsupported by any of them.

Confidence is rendered by the template's bar meters and labels, four levels: Verified, Likely, Unconfirmed, Not Established. A Verified rating can rest on an independent source, a public record, or MII's own inspection of the primary evidence; the endnote records which, per the Verified definition in `SKILL.md`. The confidence key printed below the table is fixed template text carrying the reader-facing definitions; the operative definitions and the floor rule live in `SKILL.md`, and every row is checked against those before submitting.

**(a-6) Findings**, one section per topic, ten topics in the order set in `SKILL.md`, carrying the same five section headings as the scorecard and in the same order, with Topic 5 carrying the five fixed subheadings set out there, in plain factual prose citing sources by endnote. This is the only per-topic content in the report; do not also produce a separate condensed "executive summary" pass over the same ten topics; one well-written pass replaces both. Compression is the enemy of qualifiers: keep hedges and tense exactly as the source has them even where it costs a few words.

State findings as facts, not as commentary on the finding. "Production-capacity and funding-round figures are internally consistent across independent trade outlets" is the finding. A sentence explaining that this consistency is unusual, or typical, or "exactly the kind of thing this report type exists to surface," is not a finding; it is commentary on the evaluation itself, and it does not belong in body text under any circumstance (see House style, below).

Where sources disagree, state the disagreement as a fact with the sources endnoted. Match the weight of the treatment to the weight of the discrepancy: a minor variance, an imprecise headcount range, a rounding difference, a credential described slightly differently in two informal mentions, belongs in the endnote, not a body sentence. Give body-text space to a discrepancy only when it is substantial enough to bear on the recommendation.

Two fixed tables ride inside topics; fill them under these rules:

- **Milestones** (Topic 1, Company Fundamentals): documented dates only, one endnote per entry. Omit rows rather than inferring dates.
- **Funding rounds** (Topic 2, Financial Health & Funding): `Round | Date | Amount | Named investors | Source`, where the Source cell carries the endnote number. The Total disclosed row sums disclosed amounts only.

Companies with more than one material repeat the per-material subheading structure in topics 2 through 9, per `SKILL.md`.

Four things that do not belong anywhere in the analysis report's visible text, each a way the principle in (a) above tends to get broken:

- A "Questions for the company" subsection under any topic, or a per-topic document-request list. That content lives in the company document, per (b) below, and in the one consolidated Open Questions for Direct Verification section, (a-7), reframed for investors and brands.
- A "Contradictions" subsection under any topic. Contradictions become questions in the company document, and, where one bears on a load-bearing claim, a pre-publication note at that claim.
- An "MII commentary" subsection, or anything performing the same function under another name.
- A "note on the scope of this evaluation," or any front-matter section explaining the report's own limitations to MII. Limitations that affect a specific finding are pre-publication notes at that finding; a limitation affecting the whole evaluation is a single pre-publication note at the top of the report, not visible text.

**(a-7) Open Questions for Direct Verification.** A top-level section, built from the Threats cell of the MII assessment grid, the working notes on contradictions, and missing documentation. It mirrors the substance of the company document, reframed for investors and brands to put to the company directly: "Ask [Company Name] which of its published capacity figures is current," not "Your FAQ states." Two subsections, exactly these headings:

**Questions to Ask.** Numbered, one per open working-notes entry plus any question the Threats cell generates, ordered by what most affects the recommendation. Each states what the public record shows, with its endnotes, before the question.

**Documents to Request.** The standard asks as a numbered checklist, the same list as the company document's Documents Requested section. Items involving test data, LCA or certification must name the underlying document, not a summary: a summary of a test report is not a test report.

**(a-8) Endnotes**, numbered in first-use order. Each carries: full source details (author or publisher, title, outlet, date), direct URL, access date, archive URL captured at research time, and an article/section/page locator where the source is a legal instrument or long document. Where retrieval was partial, say what was visible and what was not. Endnotes supporting a negative finding carry the search documentation itself: database, exact query, identity variant used, date, and result, per Sourcing Rule 7.

Repeat sources use "see note N" cross-references.

### Pre-publication notes

Every report leaves things unsettled: a figure the company has not confirmed, a regulation whose status could shift before publication, an archive that needs re-capturing, a contradiction still unresolved. Flag these where they occur, at the exact sentence, cell, or endnote they concern, as you write, not reconstructed from memory at the end.

Add a note wherever one of these is true:

- The finding is Unconfirmed or Likely on a claim that matters to the recommendation, and MII should try to close the gap with the company before this goes out.
- The fact is time-sensitive (a regulation's status, a funding round, a capacity figure, a company's operating status) and could change between the research date and publication.
- The claim traces to an entry in the company document that is still open. Reference the question number there so a reader can find the underlying evidence.
- A required step was blocked: an archive that would not capture, a source that would not screenshot, a search that could not reach its coverage floor. See `SKILL.md`'s "When you cannot complete a step."
- The finding sits somewhere with outsized reach, such as the recommendation paragraph, the scorecard, or the risk section, where a wrong or stale confidence rating travels furthest.

Write what MII needs to do, not just what is uncertain. "Unconfirmed; ask the company to substantiate, see company document Q4" is a note someone can close. "Uncertain" is not.

**Format.** Build the report in two passes, not one.

First, build the document completely (cover through endnotes) with zero pre-publication content anywhere in the visible text. A note conceived while drafting this pass still becomes a second-pass comment; it does not get written into the first pass as a sentence to fix later, a caveat, or an aside.

Second, add each note as a real anchored margin comment with the `docx` skill's comment tooling, attached to the exact sentence, cell or endnote it concerns. The pre-submission check results from `SKILL.md` are one comment anchored to the company name on the cover.

**Verify the notes actually landed before delivering.** Having intended them is not sufficient; check the XML directly: `word/comments.xml` contains one `<w:comment>` per note, and `word/document.xml` contains one matching anchor for each, counted, not assumed. A note smoothed into visible prose so it reads as part of the report is the failure this section exists to prevent; a note missing entirely is the second.

Where the deliverable is Markdown or a Google Doc draft instead of `.docx`, mark each note inline in a form that cannot be mistaken for report prose: `[MII PRE-PUB: ...]`, immediately after the sentence it concerns.

This is a judgement call about what MII should still do, distinct from the mechanical pre-submission checks in `SKILL.md`'s "Before you submit": those are a pass/fail run Claude performs on itself, this is MII's judgement. A report can pass every mechanical check and still carry five open pre-publication notes; that is the expected state for a pre-validation company, not a failure of the report.

## (b) The company document

MII works to support the next-gen materials industry and thus would like to help material companies resolve the issues we found during this analysis. This document is sent to the company by email, alongside the report, before publication: the company gets the opportunity to review both and respond, and MII updates the report before it goes out. So every entry must carry enough that the company can (1) find the issue MII is pointing at and (2) understand why it matters. It should be framed in a helpful tone: investors and clients will likely discover these issues during due diligence, and we want to help the company resolve them and make their record as clean and persuasive as possible.

**Why contradiction-driven.** The questions a company cannot deflect are the ones that quote its own material back to it. "Please share your LCA" gets a brochure. "Your FAQ says 98 to 100% bio-based and your August vendor profile says 99.7%, which is current?" gets an answer, or gets a silence that is itself informative, or surfaces an honest oversight MII can help fix. A generic document could be written before the research starts; that is the tell that it has failed. Everything in the Questions section should be impossible to write without having done the work.

**Tone.** Contradictions are not accusations, and the document should not read as though it caught someone. Most have dull explanations: a registered office in a different city from the stated headquarters usually just means the founder registered the company where the plant is. Write neutrally, state both sources, and ask. The value to MII is that it asks rather than guesses, and that the company can see the discrepancy exists and respond. Frame it as MII helping them prepare before others catch them in their due diligence.

### Working notes: the entry format

Keep a running set of notes from the first search to the last, one entry per discrepancy. This is internal working material, not a delivered file; it exists to be turned into the Questions section below.

| Field | Content |
|---|---|
| **What the company says** | Verbatim quote, with source and locator |
| **What the other source says** | Verbatim quote, with source and locator |
| **Type** | See "Finding contradictions" in `research-and-sourcing.md` for the eight recurring types, with worked examples |
| **Why it matters** | One sentence on what turns on it |
| **Question** | The question as it will appear in the Questions section |

Nothing gets dropped for being awkward or minor. A discrepancy with a dull explanation still belongs: "we asked and the answer was mundane" is a finding, and "nobody noticed" is not.

**When an entry resolves before the document is finalised** (the company answered it on an earlier call, or MII found the primary record after all), it does not need a question. Update the finding and its confidence rating in the analysis report instead, and keep the entry in the working notes as the record of how it was resolved.

**When an entry is still open at draft time**, it becomes a question below, and, where it affects a claim prominent in the analysis report (the recommendation, the scorecard, a risk), it also earns a pre-publication note there cross-referencing this document's question number.

### Structure

**1. Title block.**

> Questions for [Company Name]
> Prepared alongside the MII Company Analysis Report on [Company Name]
> Material Innovation Initiative, [date]

**2. Introduction. VERBATIM boilerplate, identical in every report, slots filled per report:**

> MII has completed its Company Analysis Report on [Company Name], and before we publish we want to give you the opportunity to review it and respond. This document lists what we could not verify from public sources, the places where public information about [Company Name] is inconsistent, and the documents that would settle each item. We are sharing it because investors and brands are likely to find these same issues in their own due diligence, and resolving them now makes your record cleaner and more persuasive. Please send corrections, documents, or responses by [date], and we will update the report before publication. We would also be happy to set up a call to discuss any item.

**3. Questions.** Numbered, ordered by what MII most needs to know, with anything that would change the recommendation first. Each entry carries four elements, in this order:

- **What we observed.** The verbatim quotes from both sides of the discrepancy, each with its source named inline: publisher or page title, URL, and date accessed. The company must be able to click through to the exact passage.
- **Where it appears in the report.** The topic section of the analysis report the issue affects, so the company can read it in context, since they are reviewing both documents together.
- **Why it matters.** One or two sentences on what turns on it, framed around the company's own credibility: what an investor or brand running due diligence would conclude, or which claim becomes unsupportable, if it stands unresolved. If it is a contradiction, explain that consistency leads to credibility.
- **The ask.** The specific question, or the specific document that settles it, named precisely: laboratory, standard, date, and result for a test report; application and grant numbers with jurisdictions for a patent.

The question numbers here are the numbers pre-publication notes in the analysis report cross-reference.

**4. Documents Requested.** Open with this **VERBATIM boilerplate:**

> Where a document is confidential, MII can still serve as a verifying source: we can enter into an NDA, or review the document on a video call, and rate the finding "Verified" in the published report rather than "Unconfirmed," with the endnote recording that the verification rests on MII's direct review. This gives you the credibility of verification while you choose who sees your data.

Then the standard asks as a numbered checklist, ordered for a diligence call. Items involving test data, LCA or certification must request the underlying document, not a summary: a summary of a test report is not a test report. Cover composition and bio-based content certification, IP filing numbers and jurisdictions, third-party performance testing per vertical, the full LCA with scope and verifier, end-of-life and biodegradation test data, chemical inventory and REACH/ZDHC status, capacity and capex, pricing and MOQ, customers and references, financials and runway, and team and advisory depth.

**Citations in this document are inline only: no endnotes, no Note on Sources.** The reader is the company itself; the document is used by email and on calls, and each entry already carries everything needed to locate its sources. Do not add an endnote apparatus, a source inventory, or any evidence-grading front matter to this document.

## (c) The source screenshot folder

One image per cited passage, delivered alongside the analysis report, so a reviewer can see where a fact actually sits on the page without re-running the search or trusting the endnote at face value. This is a different safeguard from the archive URL required by Sourcing Rule 9: the archive preserves the whole page in case it changes; the screenshot shows a human, at a glance, the specific location the citation rests on. Do both.

Capture the screenshot at the same time as the quote, while the source is open, per the search protocol in `research-and-sourcing.md`. Reconstructing it later from memory or a fresh visit is the same failure Sourcing Rule 4 exists to prevent, applied to an image instead of a quote: the page may have changed, and you would be screenshotting a different page than the one you actually read.

### What to capture

One image per distinct passage a claim rests on, not one per URL. The same page cited for two different facts in two different sections gets two screenshots if the facts sit in different places on the page, and one if they sit in the same paragraph or table. The test is whether a second screenshot would show a reviewer something the first one does not.

The image should let someone locate the fact without already knowing where it is:

- If the passage fits on one screen, capture the full page (or the full visible viewport), so the reviewer also sees the surrounding navigation, heading or byline that confirms what site they are looking at.
- If the page is long, scroll or zoom to the specific section first so the passage is legible, but keep a heading, breadcrumb or URL in frame where the tool allows it.
- Where the tool supports it, zoom into the region containing the fact rather than shrinking an entire long page down to where the text is unreadable.
- For a PDF, capture or export the specific page, not the whole document.
- For a paywalled or partially rendered page, screenshot whatever is actually visible, the same view Sourcing Rule 2 already requires you to describe in the endnote. A screenshot of a paywall notice is itself evidence of what MII could and could not see.

An actual visual highlight or box around the exact sentence is a bonus where the tool makes that easy.

### Folder and naming

One folder per report, delivered alongside it, named per the table at the top of this file: `MII Company Analysis Report_[Company Name]_Source Screenshots/`.

Inside, name each file by the endnote number it supports, followed by a short slug: `014-mca-registry-cin.png`, `027-vendor-profile-capacity.png`. This keeps the folder sorted in citation order and makes cross-referencing from the endnote list immediate.

Where one endnote is reused for a different passage than its first use (a "see note N" cross-reference to a new location on the same page), give the second screenshot the same number with a letter suffix: `014a-mca-registry-directors.png`.

### The manifest

Include a short `manifest.md` or `manifest.csv` in the folder, one row per screenshot: filename, endnote number, the claim it supports in a few words, and the URL. The image is the primary evidence, not this file, but the manifest is what makes the folder usable by someone who has the report open and is not yet cross-referencing endnote by endnote. It is also where a named gap (below) gets recorded.

### When a screenshot cannot be captured

This is not rare, and it is not a reason to skip the citation. It is a reason to say so, the same way an unreachable archive already gets said. A session-gated registry portal, a document that only opens as a forced download, a page that never finishes rendering, or an environment with no browser or screenshot tool at all are all the same situation: name it.

Record the gap in the manifest against that endnote number, with the reason, and add a pre-publication note at the citation in the analysis report. A folder with three named gaps and a manifest that explains them is a complete deliverable. A folder that silently skips three numbers is not, because a reviewer cannot tell a skipped citation from a missing file.

Where no browser or screenshot tool is available for the whole evaluation, say that once, up front, rather than repeating it at every one of what might be over a hundred endnotes.

### What this does not require

Negative findings have no single passage to screenshot, since the finding is the absence of a result. A screenshot of an empty search-results page is welcome corroborating evidence where it is easy to get, but it is not a floor requirement the way it is for an affirmative citation: Sourcing Rule 7 already sets what a documented negative finding needs.

**Findings verified by MII's private review must never be screenshotted.** Where MII has reviewed a document privately (NDA, video call), including any excerpt or image of it in the folder would defeat the confidentiality the company was promised. Cite MII's own review in the endnote instead, per the Verified definition in `SKILL.md`, and record in the manifest that the citation has no screenshot because the source is confidential, not because capture failed. That distinction matters: a capture failure is a gap to close before publication, and a confidentiality exclusion is not.

## House style

- **No em-dashes in body prose.** Use commas, colons, parentheses or full stops. En-dashes in page and number ranges (221–239) are correct and must not be converted to hyphens. Titles and passages quoted from sources keep their original punctuation.
- **Locators.** Both `.docx` deliverables carry page numbers in the footer; the numbered sections and question numbers serve as citation locators. In a Markdown draft, the numbered sections above serve as the locators.
- **Never fabricate or estimate** a figure, certification, quote or date. Where you estimate or infer, label it as an estimate or inference and show the basis.
- **Label MII's own judgements** as assessments rather than findings. A technology readiness level, a risk ranking, a "largest barrier" call and a market-pricing comparison are assessments.
- Prose and paragraphs. Tables for the scorecard and any comparison. Numbered lists for the company document and the Open Questions section.
- Avoid "genuinely", "honestly", "straightforward", "notably", "crucially", "it is worth noting".
- **Never comment on the evaluation's own methodology, MII's research practice, or how typical or unusual a finding is "for this report type."** No "which is not the typical finding for this report type," "which is an unusual and encouraging pattern," "exactly the kind of finding this report type exists to surface," or anything performing the same function. State the finding. If the observation about typicality or research practice genuinely matters to someone, it is a pre-publication note, not body text; usually it does not matter to the reader at all and should simply be cut.
- Use the Oxford comma.
- Before delivering, run the `paragraph-structure` skill and then the `prose-compression` skill on the finished draft.

## Brand colours

Primary `#9A2866`; secondary `#A4BAB7` and `#283D6B`; tertiary `#F1B95E`, `#E59B85`, `#76988B`.

The analysis report's palette is fixed by the design table in (a); never restyle it. Apply the same typefaces and palette to the company document; it goes out under MII's name too.

**Colour applies to built documents only:** `.docx`, PDF, HTML. If the deliverable is Markdown or a Google Doc draft, write plain Markdown and skip the colour. Never inline `<h2 style="color:...">` or similar into a Markdown file to fake it; it renders as literal tag soup in most viewers and breaks the review pass.

## File format

Both the analysis report and the company document are Word (`.docx`) via the `docx` skill: the report because it is MII's editing master (PDF for distribution is exported from Word after edits), the company document because it is emailed to the company and `.docx` is what they respond to in comments.

After building, verify: every in-text citation number matches its endnote; pre-publication notes are real anchored comments per the verification step in "Pre-publication notes"; and run the mechanical checks: no em-dashes in body prose, every endnote cited at least once, first citations in strictly ascending order with no gaps, and all deliverables named exactly per the table at the top of this file.

## A note on cost

This report takes longer and costs more than an unstructured version of the same task, by roughly 60 to 80 per cent in testing, before adding screenshot capture. The extra goes on registry retrieval, verifying claims against source text before citing them, documenting negative searches, and a screenshot for every distinct cited passage, captured while the source is open rather than revisited afterwards. That is the work, and it is what separates a report MII can publish under its own name from one that has to be repaired at audit. Do not economise on it, but do keep the research proportionate: ten properly sourced findings beat thirty loosely sourced ones.
