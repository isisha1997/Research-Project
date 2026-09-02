---
name: "company-material-evaluation"
description: "Research and write a Material Innovation Initiative Company & Material Evaluation: a fully-cited assessment of a next-gen materials company and its materials for investors, brand executives, and MII's internal team. Covers company fundamentals, material technology, performance vs. incumbent, sustainability and LCA status, scalability, cost, regulatory exposure, IP, traction, funding, risks, and a contradiction-driven company document. Only use this skill when explicitly asked to as it is cost intensive."
---

# Company & Material Evaluation

Produce Material Innovation Initiative's evaluation of a next-gen materials company and the materials it makes. Three deliverables, all of them handed over:

1. **The analysis report**, for MII's audiences: what MII found about the company and its materials, fully cited, with pre-publication notes anchored at the exact point in the document each one concerns.
2. **The company document**, handed to the company directly: the contradictions this research found, turned into questions, plus the standard documents to request.
3. **The source screenshot folder**, one image per cited passage, showing where in the source the fact actually sits.

`references/output-spec.md` is the single source of truth for what each of these contains, how it is structured, and how it is formatted. Read it before building anything, and do not infer structure from anything said here: this list names the deliverables, it does not specify them.

The audiences for the analysis report are investors deciding whether to fund, brand executives in sourcing, sustainability, R&D and procurement deciding whether to adopt, and MII's internal team tracking the industry. All three will act on what this report says, so the analysis has to hold.

## What makes this report hard

Most companies you evaluate will be pre-validation. They will have published no peer-reviewed science, no third-party LCA, and no test data. Nearly everything you can find will be the company describing itself.

That is a legitimate finding, not an obstacle. The report's job in that situation is to characterise the claims accurately, make the reliance on company sources visible, rate confidence honestly, and put the burden where it belongs, in the questions MII asks the company directly.

What destroys a report like this is (1) falsely citing a source, (2) making up a source or fact, (3) stamping "Verified" on company sourced facts, or (4) writing a sweeping negative finding with no record of what was searched. Those are the failures this skill exists to prevent, and each has a rule in `references/research-and-sourcing.md` earned from a real audit of a real MII report.

## Step 0: Confirm scope

Establish these before researching. Ask only what you cannot infer.

- **The company.**
- **The company's country of incorporation.** This is important as it usually defines which country you should be searching for the company's documents, patents, financials, and other corporate documents. It may also affect what laws the company is obligated to follow.
- **The material.** Some companies have multiple materials and we may not want to do an analysis on all of them. First search for all of the materials produced by that company, note the incumbent material each competes against (bovine leather, virgin polyester, down, wool), evaluate whether any use animal-based products (defined as anything in the production process which comes from an animal, including byproducts), and evaluate whether the material is likely better than the incumbent for the environment. Then: (1) if it has no animal-based inputs and is better for the environment than the incumbent in at least one respect, recommend to the user that we evaluate it; (2) if whether it uses animal-based inputs or its environmental impact is unclear, explain the facts to the user and ask for clarity on whether to review that material; or (3) if it clearly uses animal-based inputs, or is clearly not better for the environment than the incumbent in any respect, say so and do not recommend evaluating it unless the user directs otherwise.
- **The intended publication date.** Assume the date the report goes to the company for review is within a few days of completing the skill, and that the publication date is a month after the date of running the skill. Everything time-sensitive (laws, standards, certifications, company status, funding, capacity) must be current as of publication, not as of your research date. State your research date in the report and flag whatever will need re-checking if publication slips.
- **Whether a browser or screenshot-capable tool is available in this session.** If not, say so to the user before starting research: the source screenshot folder cannot be built on web search and web fetch alone. The evaluation can still proceed on the other two deliverables; declare the gap once, up front, per "When you cannot complete a step," below, rather than letting the tool limitation go unstated and the whole folder quietly disappear.

Then scope the subject: list the materials the company produces and the MII user approved for inclusion; the target vertical for each (fashion, automotive, home goods); the specific applications within it (footwear, couches, rugs, wallets); the incumbent each competes against (bovine leather, virgin polyester, down, wool); and the production locations for each material (where unclear, all production locations for the company), since this defines what laws the company is subject to, including labor and environmental laws. Where the company makes more than one material, run topics 2 through 9 separately for each; the other topics are company-level.

## The order of work

1. Scope, as above.
2. **Corporate spine first.** Pull the statutory registry record before anything else. It is free, authoritative, and it frequently disagrees with the company's own website, which gives you your first contradictions and shapes the rest of the research. See "Where to look" in `references/research-and-sourcing.md`.
3. Research the ten topics. Run them in parallel where you can. Keep a running set of working notes on contradictions as you find them (see "Finding contradictions," below), and capture the source screenshot the moment you read the source, alongside the quote (see the search protocol in `references/research-and-sourcing.md`).
4. Write the analysis report as one `.docx` with the `docx` skill, under the fixed design in section (a) of `references/output-spec.md`, never freestyled: the spec fixes the structure at (a-1) through (a-8), the typefaces, the palette, and all fixed reader-facing text. Apply the confidence scale honestly, and add a pre-publication note (a real anchored margin comment) wherever the writing surfaces something MII should check or decide before this goes out. Write the note where you notice the issue, not from memory at the end.
5. Build the company document from the working notes on contradictions, not from a generic template.
6. Run the pre-submission checks.

## Finding contradictions

Keep a running set of working notes from the first search to the last: every time two sources disagree, or a company claim cannot be squared with a primary record, or a figure fails to reconcile, log what the company says, what the other source says, why it matters, and the question it generates. This is the material the company document is built from.

`references/research-and-sourcing.md` gives the eight recurring types with worked examples, and the tone to write them in (contradictions are not accusations). Read it before you start Topic 1, because knowing what you are looking for is what makes you find it. The entry format, and how entries become the company document, are in `references/output-spec.md`.

## Sourcing, search and where to look

These govern everything else. Where a rule in `references/research-and-sourcing.md` conflicts with a length or formatting instruction, that file wins.

The short version of the sourcing rules, in full detail with worked examples in `references/research-and-sourcing.md`:

1. **Use the highest available source tier.** If a registry record or a peer-reviewed source covers a claim, a company web page is not an acceptable citation for it.
2. **Aggregators are pointers, not sources.** Tracxn, PitchBook, Crunchbase, YourStory, Vevolution, LinkedIn. Follow them to the primary record and cite that.
3. **Trace every claim to where it originates.** A number repeated by three outlets is still one number.
4. **Verify before you cite.** Confirm the source contains the specific claim. On-topic and credible is not the same as supporting.
5. **Quote company claims verbatim and keep their qualifiers.** "Will be available" is not "is available".
6. **Report what complicates the story,** including from sources you are already citing.
7. **Negative findings must document the search:** which database, what query, what date, what result.
8. **Legal citations need article-level locators and an applicability check.**
9. **Archive every web citation** at the time of research.
10. **Every number, law, superlative, causal claim, company-status claim and negative existence claim carries a citation,** wherever it appears, including in the scorecard.

`references/research-and-sourcing.md` also covers where the authoritative source lives for each claim type ("Where to look") and how hard to search before concluding a source does not exist ("Search protocol"). Read the sourcing rules, search protocol and contradiction-hunting sections in full before Topic 1; "Where to look" is a lookup table to consult topic by topic rather than read upfront.

## Confidence ratings

Four levels. The template's confidence key prints the reader-facing definitions; these are the operative ones.

- **Verified**: corroborated by a primary record, or by two or more independent sources of which at least one is peer-reviewed, government, standards-body or independent journalism; or MII has directly reviewed the underlying documentation itself, for example under NDA or on a video call per the company document's offer in `references/output-spec.md`, even where that documentation is not publicly available. Because these bases differ in whether a reader can check them, **the endnote must record which basis the rating rests on**. Where it is MII's own review, cite the review as the source: what was reviewed, the date, and how, so the reader can see the verification rests on MII's attestation rather than a record they can check themselves.
- **Likely**: a single credible independent source, or a self-reported claim that is plausible and consistent with independent evidence.
- **Unconfirmed**: company-claimed only, with no independent corroboration found.
- **Not Established**: MII searched for this and could not confirm it either way, on a search that met its coverage floor per the search protocol in `references/research-and-sourcing.md`. This is not the same as Unconfirmed: Unconfirmed is a claim the company makes that only company sources support; Not Established is MII's own documented absence of a finding, and it requires the same floor a negative finding always requires, not merely one query.

**The floor rule, which overrides everything else.** A finding whose only sources are company-controlled or company-supplied is **Unconfirmed**, however many company pages repeat it and however plausible it is. Company websites, press releases, sponsored articles, vendor profiles and self-maintained database profiles do not corroborate each other. They are one source wearing different hats. **MII's direct review of the primary document is the one way a company-sourced document escapes this floor without public corroboration:** the finding rates Verified because MII actually inspected the document itself, not because the company repeated its own claim, and the endnote records that basis.

This rule exists because the most damaging error in this report type is a "Verified" stamp on marketing copy. The scorecard is the part that gets copied out and forwarded on its own, and a wrong confidence label there travels further than any sentence in the body.

Before submitting, walk the scorecard and check that no row is rated above what its sources permit.

## The ten topics

For each: state the finding, the confidence level, and the source. Where you cannot find public information, say so explicitly, document the search that failed, and add a pre-publication note flagging it for MII to close out or re-run closer to publication. Where the company makes multiple materials, run topics 2 through 9 separately for each.

The topics are grouped into five sections. The section order below is the order they appear in both the scorecard and the Findings section, and the topic numbers run sequentially through it. Keep them in this order: renumbering later breaks every cross-reference in the company document.

### A. The Company

1. **Company Fundamentals**: lead with the statutory registry record: registration number, incorporation date, registered office, current directors with appointment dates. Then founding year, HQ, production locations (if you can't find production locations and they are producing materials, add it to the questions to ask the company; if they are not producing, add a question on whether they have made any determination on where they will build production locations, or their production plans, e.g. comanufacturing), employee count, ownership structure, leadership bios (background, prior ventures or exits, technical expertise; one paragraph for the CEO and one for the CTO; if there are additional C-suite or prominent business leaders, give the user a summary and ask whether they should also get their own paragraph), scientific advisory board. Where the registered office differs from the stated headquarters, report both and say which is which.

2. **Financial Health & Funding**: total raised, rounds and dates, named investors, reported revenue or profitability milestones, paid-up versus authorised share capital, runway signals (layoffs, facility openings or closures, leadership departures). Paid-up capital is often the single most informative free number on an early-stage company. Check that the investors still exist and still operate; a lead investor whose website has gone dark is a finding.

### B. The Material

3. **Material Technology**: feedstock, production process, what makes it differentiated or defensible, current stage (lab, pilot, commercial).

4. **Performance vs. Incumbent**: how it compares on the attributes that matter for the vertical. Fashion: hand-feel, drape, abrasion, colorfastness, water resistance. Automotive: flammability rating, UV and heat resistance, flex-fatigue, FMVSS or regional compliance. Home goods: durability, cleanability, colorfastness, flammability. Separate independent test data from company-reported. Where the company claims testing but publishes no reports, say exactly that, since it is a different and more useful finding than "no data was located".

### C. Sustainability

5. **Sustainability & Environmental Impact**: report this topic under five fixed subheadings, in this order, in both the Findings section and the scorecard. Give each its own finding and its own confidence rating; a company can be well evidenced on one and silent on another, and a single blended rating hides that.

   **Water Use**: consumption in processing and in feedstock cultivation, against the incumbent, with the comparison basis stated.
   **Emissions**: carbon footprint against the incumbent, naming scope, system boundary, functional unit and reference year. Existence and scope of an LCA (cradle-to-gate vs cradle-to-grave, ISO 14040/14044 or EU PEF alignment) belongs here, and state whether any LCA is third-party verified, self-reported or absent.
   **Chemical Use**: chemical inputs and toxicity, effluent and discharge, and any restricted-substance screening.
   **Biobased Content**: percentage bio-based by variant, the feedstock it derives from, and whether any figure is certified (for example to ASTM D6866).
   **End of Life**: biodegradability, compostability, recyclability and the actual end-of-life pathway, each against a named standard where one is claimed.

   Certifications relevant to any of the five are reported under the subheading they evidence. Watch the vocabulary throughout: bio-based is not biodegradable, recyclable is not recycled, plastic-free is not non-toxic, and a claim about one subheading is not evidence about another.

### D. Commercial Readiness

6. **Scalability & Manufacturing Readiness**: current capacity, announced expansions and timelines, manufacturing partners or licensees, feedstock supply chain and geographic concentration, readiness level if inferable. Recompute the arithmetic: daily output times operating days should reconcile with the annual figure, and when it does not, that gap is a finding.

7. **Cost & Commercial Viability**: price vs incumbent if disclosed or estimable, cost-reduction roadmap, minimum order quantities, lead times.

8. **Commercial Traction & Partnerships**: named brand partners, pilots or customers by vertical, geographic markets, publicly reported offtake or supply agreements.

### E. Legal Position

9. **IP & Competitive Landscape**: patents filed or granted, trade secret or exclusivity claims, positioning against two or three named competitors and against the incumbent. Check the trademark too: a company using the ® symbol with no registration you can find is worth a line.

10. **Regulatory & Compliance Landscape**: covers two different questions, because they bind different jurisdictions.

   **Production location: labor, environmental and chemical-registration law**, binding wherever the company manufactures (the production location(s) established in Topic 1). Establish which of the production country's labor law, environmental and discharge law, and chemical-registration regime (China's IECSC, Japan's CSCL, South Korea's K-REACH, or the narrower instruments that apply in a jurisdiction like India, per "Chemical and safety compliance" in `references/research-and-sourcing.md`) actually bind this company's operations, and what each requires. Where no usable public source exists for a jurisdiction, say so explicitly rather than treating silence as compliance.

   **Point of sale: what can be in the finished product and how it can be marketed**, binding wherever the product is sold, regardless of where it was made. Do not assume the instruments below apply; establish which actually bind this product category as of the publication date, per sourcing rule 8. Default to checking EU and US instruments, since most MII evaluation targets are aiming at those markets regardless of where they manufacture, and add another market's rules where research shows the company specifically targets it too. Worth checking, not worth assuming: EU Ecodesign for Sustainable Products Regulation and the Digital Product Passport, Directive (EU) 2024/825, the proposed Green Claims Directive, the EU Deforestation Regulation, extended producer responsibility schemes, national leather and fibre labelling laws, REACH, CPSIA, and the vertical-specific flammability standards.

   For every instrument in either part, state whether it applies, from when, and what it requires. Check what changed in the last twelve months before claiming a trend in either direction, because regulatory pressure comes off as well as on.

**Open Questions for Direct Verification is not a topic.** It is a top-level section of the analysis report, built after the topics from the Threats cell of the MII assessment grid, the working notes on contradictions, and missing documentation. It mirrors the substance of the company document, reframed for investors and brands to put to the company directly. Its structure (two subsections: Questions to Ask, and Documents to Request) is specified in `references/output-spec.md`, section (a-7).

## Output

`references/output-spec.md` holds the full structure for all three deliverables: the analysis report, the company document, and the source screenshot folder, including the pre-publication notes and how to anchor them.

Hand over all three as files. Do not summarise them in chat instead of delivering them, and do not leave the screenshot folder behind as working material.

House style, brand colours and file format are all in `references/output-spec.md`; they are the same rules regardless of which of the three deliverables you are building.

## When you cannot complete a step

Three situations come up often enough to have a standard response, and all three are handled by declaring the gap rather than working around it.

**You could not verify something the report would normally assert.** Say so, and assert nothing. "MII could not verify, and therefore does not assert, the status of X" is a stronger and more honest sentence than a confident claim built from memory, and it earns a pre-publication note where someone can close it. This applies with particular force to regulation, where writing from general knowledge produces statements that are specific, plausible and wrong.

**A tool or environment limit blocked a required step,** most commonly archive capture. Record it as a named pre-publication note rather than silently skipping it. A report that says "archive capture was not possible; capture before publication" is publishable after one action. A report that quietly omits archives looks complete and is not.

**No browser tool was available to capture a source screenshot,** or a specific source could not be screenshotted (a session-gated portal, a document that only opens as a download, a page that never finishes rendering). Say so in a pre-publication note at that citation, and record the gap in the screenshot folder's manifest rather than leaving a silent hole in the numbering. A folder missing three screenshots with named reasons is usable; a folder that skips three numbers with no explanation looks like a mistake in the report rather than a mistake in the record. Where no browser tool is available for the whole evaluation, say that once, at the top, rather than repeating it at every citation.

## Before you submit

Run these. Report the results in chat when handing over the deliverables, and attach one pre-publication comment anchored at the top of the analysis report listing any check that did not pass and any named blocker. The results are never a visible section of the report: the report's structure is closed at (a-1) through (a-8), and visible text never addresses MII. This is a mechanical self-check, separate from the pre-publication notes: those are judgement calls for MII to make, this is a pass/fail run you perform yourself.

1. Every claim in sourcing rule 10 carries a citation, including negative existence claims and every cell of the scorecard.
2. Every citation was checked against the source's actual text, not its title or subject.
3. Every endnote carries full source details, an access date and an archive URL.
4. No finding is rated above what its sources permit, and the confidence floor rule has been applied.
5. Every legal citation has an article-level locator, and its status and applicability as of the publication date are stated.
6. Every negative finding names the databases searched, the queries and the dates.
7. Figures are internally consistent across sections, or the inconsistency is surfaced as a finding.
8. All arithmetic and unit conversions recomputed.
9. All URLs live; anything dead replaced or flagged.
10. Every working-notes contradiction entry appears as a question in the company document and, reframed for investors and brands, in the report’s Open Questions for Direct Verification section.
11. Every endnote has a matching screenshot in the folder, or a named reason it does not.
12. Every pre-publication note is placed in the text with sufficient information that MII knows what to check or the risk of the statement.
13. Exactly three files exist: the analysis report, the company document, and the source screenshot folder (or a declared blocker for the folder). No fourth file, such as an "internal," "working," or "notes" document, has been created or handed over. The search record, evidence cards, working notes on contradictions, and the identity block are all working material used to build the three deliverables, and none of them is delivered on its own.
14. The analysis report matches the structure specified in `references/output-spec.md`, sections (a-1) through (a-8), with no sections added beyond it, no placeholder text remaining, and no fixed reader-facing text reworded.
15. If any of the ten topics received zero searches, that is raised in a pre-publication note at the top of the report and said directly to the person who commissioned the work, not written into the recommendation or any other visible text.
16. Before calling the analysis report finished, search its own visible text for a per-topic "Questions for the company" subsection, "Contradictions" as a subsection heading, "MII commentary," "note on the scope," and "internal document." None of these belong in the analysis report's visible text; the consolidated Open Questions for Direct Verification section, (a-7), is the one legitimate home for questions in the report. Where any appears, the content has been misplaced: move it to the company document if it is a question or document request, convert it to a pre-publication note if it is a judgement call for MII, or cut it if it adds nothing beyond the finding itself.
17. No sentence in the analysis report breaks the house-style rule in `references/output-spec.md` against commenting on the evaluation's own methodology, MII's research practice, or how typical a finding is.
18. The report `.docx` contains one `<w:comment>` per pre-publication note in `word/comments.xml`, with a matching anchor for each in `word/document.xml`, checked by count per "Pre-publication notes" in `references/output-spec.md`, not assumed. No pre-publication text appears in visible report prose.
