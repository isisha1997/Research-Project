# Research and sourcing

Everything governing how MII researches and cites a company evaluation: the standing sourcing rules, where the authoritative source lives for each claim type, how hard to search before writing an absence, and how to notice when sources disagree. Read "Sourcing rules," "Search protocol" and "Finding contradictions" in full before Topic 1; they govern behavior throughout the whole evaluation, and the sourcing rules also govern what you write, so keep them close while drafting too. "Where to look" is different: it is a lookup table organized by claim type, consulted topic by topic rather than absorbed upfront. Skim its section headers now so you know what is there, then return to the relevant one when you reach that topic.

Where one of these rules conflicts with a length or formatting instruction elsewhere, the rule in this file wins.

## Sourcing rules

Each rule below was earned from a real failure in a real MII evaluation that went to citation audit. The examples are from that audit.

### 1. Source tiers, and always use the highest available

Classify every source into exactly one tier:

| Tier | What belongs in it |
|---|---|
| `[Peer-reviewed / independent]` | Peer-reviewed literature, independent LCAs, independent test-house reports |
| `[MII direct review]` | MII's own direct review of company-supplied documentation that is not otherwise public, for example under NDA or on a video call per the company document's offer in `output-spec.md`. Cite what was reviewed, when, and how. Supports a Verified finding; the endnote records that the verification rests on MII's review, since a reader cannot check it independently. |
| `[Government/regulatory]` | Statutes, regulations, company registries, patent and trademark offices, regulatory databases |
| `[Standards body]` | ISO, ASTM, EN, SAE, certification schemes and their registries |
| `[Independent journalism]` | Bylined reporting by an outlet with editorial independence from the subject |
| `[Industry/self-reported]` | Company websites, press releases, sponsored and partner content, vendor profiles, trade-association material, self-maintained database profiles, industry-commissioned LCAs |
| `[MII search record]` | Not a source. A working-notes classification for a documented negative search. The documentation itself (database, exact query, identity variant used, date, result) is written into the negative finding's endnote text, described fully enough that a reader can reproduce or refute it. Use this rather than dressing a search up as a citation. |

**The tier is not printed as a bracketed tag on the endnote itself.** The scorecard's confidence rating is where reliability reaches the reader, at the level of the finding, and repeating a tier label on every one of what might be over a hundred endnotes would just duplicate what the confidence rating already says. Track each source's tier in your own working notes anyway: you need it to apply the confidence floor rule, to decide which source to cite when more than one covers a claim, and to check whether more than half the citation uses in the report are `[Industry/self-reported]` for the Note on Sources in `output-spec.md`, none of which work without it, even though the tag itself does not appear in the endnote text.

For any given claim, use the highest tier that exists. If a registry record or a peer-reviewed source covers the claim, a company web page is not an acceptable citation for it, even when the company page says the same thing. Two sources agreeing is only meaningful if they are independent of each other. When two sources agree, cite them both, with the highest tier first.

**Reclassification rules that override where a source was published.** An LCA commissioned or authored by a producer of the material under assessment is `[Industry/self-reported]` even in a peer-reviewed journal, so read funding statements and affiliations and say who paid. Self-reported indices such as Higg MSI are industry data. Sponsored content, brand-studio articles, vendor profiles and press releases are `[Industry/self-reported]` regardless of the masthead they appear under: a piece under a national newspaper's brand-studio path is an advertisement. Trade-association and brand publications are never evidence for an environmental claim. Blogs and marketing copy are not evidence at all.

**Why the tier still has to be tracked even though it is not printed on every citation.** Without tracking it, there is no way to tell whether a finding rests on a peer-reviewed LCA or a paid vendor profile beyond the scorecard's confidence rating, and that rating only tells the story at the level of the finding, not the individual source. One audited MII report carried 138 endnotes, of which 123 uses were company-controlled or company-supplied and none were peer-reviewed. No individual citation was dishonest. The pattern was invisible until someone counted the tiers, which is exactly why the Note on Sources still has to carry the count.

### 2. Aggregators are pointers, not sources

Tracxn, PitchBook, Crunchbase, YourStory, Vevolution, LinkedIn and similar are leads to follow, not citations. Use them to find the primary record, then cite the primary record. If you cannot access the primary record after trying, cite the aggregator instead and say in the endnote exactly what you tried, what you could not reach, and why.

For corporate facts, the statutory registry is required. See "Where to look," below, for the registry by jurisdiction.

Three specific hazards:

- **Self-maintained profiles.** YourStory, Vevolution, Crunchbase and most startup directories let the company write its own entry. A profile written in the first person ("after incubation at X, we incorporated our company") is company copy in a third-party wrapper. Flag it `[Industry/self-reported]`.
- **Robots and paywalls.** Tracxn is disallowed by robots.txt and cannot be retrieved by most tools. PitchBook shows a small public preview and paywalls the rest. If you cite either, say in the endnote exactly what was visible and what was not.
- **Client-side rendering.** Some profile pages return HTTP 200 with an empty body to a fetch tool, because the content loads by JavaScript. A page that returns 200 is not a page you have read. If the fields did not render, try to open it properly; if you still cannot, do not cite it, and add a pre-publication note for MII to check it manually.

### 3. Trace every claim to where it originates

A review, news article, NGO report, vendor profile or press release cited for a factual finding must be traced to the original study or record, and the claim verified against that. A number that acquires authority by repetition is the most common way a wrong figure survives into print.

When three outlets carry the same figure, you have one source, not three.

### 4. Verify before you cite

Before attaching a source to a claim, confirm the source contains that specific claim. Quote the supporting passage to yourself and check it says what you are about to say it says. On-topic, credible and adjacent is not the same as supporting.

Where a sentence makes several assertions, check that the cited sources cover all of them. If three sources are cited for a sentence containing five assertions, name which source carries which, or split the sentence. Partial coverage presented as full coverage is the single most common citation failure in this report type, and it is invisible to every reader who does not click through.

Two real examples:

- A report stated the company claims "zero effluent discharge, and zero waste", citing the company's Impact page. Those words are on the Material Story page. The Impact page does not contain either. The claim was true; the citation was wrong.
- A report quoted the phrases "patented formula" and "patented bio-scaffold", citing one page. That page contains the first phrase and not the second. The second is in a press release the report cites elsewhere.

Both are one-line fixes if caught during writing, and both are blockers if caught at audit.

From research time onward, this check has a visual counterpart: "Search protocol," below, and the screenshot folder specification in `output-spec.md`, set out capturing a screenshot of the passage at the same moment as the quote, so the verification survives after the page changes or disappears.

### 5. Quote company claims verbatim, and keep their qualifiers

Where a company claim is load-bearing, quote it. Preserve hedges, tense and scope exactly.

- "commercial sheets **will be** available" is not "commercial sheets are available"
- "managed in-house **or within a closely integrated supply chain**" is not "managed in-house"
- "**up to** 2%" is not "2%"
- an announcement dated 1 April is not "Q1"

Compression pressure is what causes this. A summary written for a time-pressed executive drops the qualifier because the qualifier makes the sentence longer. In a commercial-readiness assessment, the tense of "will be available" is the finding. If the source hedges, the report hedges.

**Watch definition drift especially hard in Topic 5.** Each of these has a narrow technical meaning in the source and a broad implication in ordinary use: recyclable, biodegradable, compostable, bio-based, natural, vegan, closed loop, circular, plastic-free, carbon negative. Identify which definition the source is using and which one the report would be trading on.

The clearest real case: asked "Is the material biodegradable?", a company FAQ answered only with bio-based content ("98 to 100% bio-based"). Bio-based describes where the feedstock came from. Biodegradable describes what happens at end of life. They are unrelated properties, and answering one question with the other is a move worth reporting in itself.

### 6. Report what complicates the story

Where a source you are already citing contains a figure that cuts against your framing, report it.

- If a vendor profile gives both a current output figure and an aspirational one, give both. One audited report took "target: 20% of India's bovine leather" from a paragraph that also said the pilot plant currently produces 1%, then asserted two sections later that actual utilisation was not public.
- If a funding database shows deal rows you are not counting, say they exist.
- Read discussion and limitations sections, not just abstracts and headline tables.

Before submitting, check the report against itself. Where two sections give different figures for the same property, either reconcile them or surface the inconsistency as a finding about the company and log it as a contradiction. Two different bio-based percentages four sections apart, both accurately cited, is still a defect.

### 7. Negative findings must document the search

"No X was found" is a claim and needs evidence like any other. Every negative finding records: which specific database or source was searched, the query used, the identity variant used, the date, and the result. This documentation lives in the negative finding's own endnote, since the tier tag is not printed and the endnote text is the only place a reader can see what the negative rests on.

**A search of one set of databases may never be cited to support a different negative claim.** Certification registries do not hold REACH registrations, chemical safety dossiers, flammability certificates, LCAs or test reports, and must not be cited as evidence for their absence. In the audited report, a single endnote documenting searches of five sustainability certification registries was cited to support the absence of REACH registration, SVHC screening, chemical-safety documentation, flammability certification, a published LCA, and third-party testing. Five separate blockers, one root cause.

**Distinguish these two statements and always write the first:**

- "The company publishes no X, and MII found none in [named sources] searched on [date]." Verifiable.
- "No X exists." Not verifiable, and usually wrong.

Where a category of document is routinely held confidentially (test reports, chemical inventories, customer contracts, OEM specifications), say so. Its absence from public sources is weak evidence that it does not exist, and a reader deciding whether to sample the material needs to know that.

**Be honest about search tools you could not operate.** Several registries cannot be queried by URL: OEKO-TEX search is a JavaScript modal, USDA BioPreferred times out its session, GOTS injects results by JavaScript, IP India's trademark search is captcha and OTP gated. If you could not complete a database query, say that the negative rests on site-restricted web search rather than a completed query. Do not write "searched" for something you could not search. In those cases, add a pre-publication note for MII to conduct the search manually.

### 8. Legal and standards citations need locators and an applicability check

Never cite a whole statute, regulation, directive or standard. Cite the article, section or clause: `16 CFR §260.8(c)`, not "16 CFR Part 260"; `Reg (EU) 2024/1781, Art. 9`, not "the ESPR".

For every legal instrument you invoke, establish and state five things:

1. **Jurisdictional applicability**. Ensure the law applies to the company. 
2. **Current status** as of the publication date: in force, amended, repealed, stalled, withdrawn, or still a proposal.
3. **Whether it binds this product category yet, and by what mechanism.** Framework regulations frequently impose nothing directly and require delegated or implementing acts first. Check whether one exists for this product category, and if not, when it is expected.
4. **The date it applies from,** which is usually not the date it entered into force.
5. **What it actually requires,** quoted. Never infer the obligation from the instrument's name or reputation.

This rule exists because naming a regulation in a research brief invites writing about it from memory. The audited report told brand executives that the EU Ecodesign for Sustainable Products Regulation and the Digital Product Passport "will require exactly the verified LCA and traceability data" the company lacks. Checked against the consolidated text: ESPR Art. 3(1) makes every obligation conditional on delegated acts adopted under Art. 4; no delegated act exists for textiles, footwear or leather; footwear is only under study; leather is not a listed product group; and the phrase "verified LCA" is not an obligation anywhere in the Regulation. The claim was confident, specific, plausible, and wrong, and a brand could have acted on it.

**Before claiming a regulatory trend in either direction, check what changed in the last twelve months.** The same report said incumbent leather faced "rising regulatory pressure" in the same month the European Commission adopted a delegated act removing leather from the scope of the EU Deforestation Regulation. Pressure comes off as well as on.

### 9. Archive everything

Every web citation carries a live-status check, an access date, and an archive URL captured at the time of research.

Company web pages, vendor profiles and investor sites are edited and taken down without notice. An unarchived citation to one is worthless the moment it changes, and you will not be told that it changed. In the audited report, the cited website of the company's lead disclosed institutional investor had become a parked domain listed for sale. The citation was unrecoverable, and the fact that the fund's site had gone dark was itself a finding the report had missed.

This is a different safeguard from the source screenshot folder set out in `output-spec.md`: the archive preserves the whole page for the record; the screenshot is the fast, human-readable version for a reviewer who wants to see where a fact sits without opening either the live page or the archive. Do both.

Re-run a link check immediately before publication and note any source that has moved, changed or gone dark.

### 10. What must carry a citation

Every one of the following, wherever it appears, including in summaries, risk sections, scorecard cells and conclusions:

- any number, percentage, quantity, currency figure, date or unit
- any named law, regulation, standard, certification or test method
- any statement about what a body requires, permits, found or believes
- any superlative or comparative ("the largest", "most next-gen leathers", "the two biggest criticisms")
- any causal claim about health, emissions, water, land, labour or waste
- any statement about a named company's operations, funding, customers or status
- **every negative existence claim**, which is the one most often left bare

Also watch two near-misses: an endnote sitting on the adjacent sentence while the sentence carrying the number has none, and a general "see [4]" where endnote 4 is a 300-page document cited with no locator.

Analytical judgements that are yours rather than a source's are welcome, and often the most valuable content in the report. Label them as MII's assessment rather than presenting them as findings. A technology readiness level, a risk ranking, a "largest adoption barrier" call and a market-pricing comparison are assessments. If MII holds proprietary data that supports one, cite MII's own work.

## Where to look

Consult this section as you reach each topic rather than reading it start to finish upfront: it is a lookup table, organized by claim type, of the primary record for each and the aggregator traps to avoid. You always need the authoritative source rather than the convenient one.

### Corporate facts

Pull the statutory record before anything else. It is free or cheap, authoritative, and it routinely disagrees with company profiles. First look for the country of incorporation for the jurisdiction. Then look for the proper register in that country. Examples:

| Jurisdiction | Register | Cite by |
|---|---|---|
| India | Ministry of Corporate Affairs (MCA) | CIN |
| UK | Companies House | Company number |
| US | Secretary of State of the state of incorporation | Entity number |
| EU | National business register (Handelsregister, RCS, Registro Imprese, KvK…) | National registration number |
| Netherlands | KvK | KvK number |
| Singapore | ACRA | UEN |
| China | National Enterprise Credit Information Publicity System (NECIPS / GSXT), State Administration for Market Regulation | Unified Social Credit Code (USCC) |

**What the register gives you, free:** incorporation date, registered office, current and former directors with appointment and resignation dates, authorised and paid-up share capital, charges, filing history, and current status.

**Paid-up share capital deserves special attention.** On an early-stage company it is often the single most informative number available, and it is almost never reported. A company announcing a large plant while showing paid-up capital equivalent to a few hundred dollars tells you something the funding databases do not.

**Indian companies specifically.** The MCA record itself is behind a light paywall for documents, but the core fields are reproduced free by several aggregators that pull directly from MCA filings: ZaubaCorp, Tofler, TheCompanyCheck, IndiaFilings, Falcon eBiz. Cross-check two of them, and cite the MCA record by CIN with the aggregator noted as the retrieval route. Financial statement values (form AOC-4) usually are paywalled; if a revenue figure matters, either buy the filing or attribute the figure to whoever reported it and say MII could not verify it independently, and add a pre-publication note for MII to request the filing from the company directly.

**Chinese companies specifically.** GSXT (gsxt.gov.cn) is free but has real access hazards: real-name authentication requiring a Chinese mobile number since November 2021, a Chinese-only interface, and frequent blocks on non-mainland IP addresses. Where GSXT itself cannot be operated, Qichacha and Tianyancha aggregate the same underlying registry data, plus litigation and change-history, and are the standard fallback: cross-check two and cite GSXT with the aggregator noted as the retrieval route, the same pattern as the Indian aggregators above. Both also gate full detail behind a Chinese-phone signup, so say what was visible for free and what was not.

**When you can't find corporate facts.** Keep searching, using the aggregator cross-check pattern under "Indian companies specifically" above as the model: find who reproduces the registry data, cross-check two of them, and cite the register itself with the aggregator noted as the retrieval route.

### Patents and trademarks

- **Patents:** Google Patents and USPTO Patent Public Search for US and international; Espacenet for European; the national office for local filings. For India, InPASS, noting that it is frequently unreachable. For China, CNIPA's Patent Search and Analysis System and its China and Global Patent Examination Information Inquiry service are free and interface in English (and several other languages), unlike India's InPASS, and cover Chinese filings with the same publication-lag caveat as any office. Justia's inventor index is a useful positive control: search the inventor name and see whether a page exists at all and what is on it.
- **Trademarks:** USPTO TESS, EUIPO eSearch, IP India (public search is captcha and OTP gated, so say so if you could not operate it), WIPO Global Brand Database.
- **Worth checking every time:** a company using ® with no registration you can find. It is a small finding but a real one, and it belongs in the company document next to the patent question.

### Certifications

First, note which certifications the company claims it has and cite as company reported. Then search the scheme's own registry. For example:

| Scheme | Registry | Notes |
|---|---|---|
| OEKO-TEX | Buying Guide | Search is a JavaScript modal with no query URL |
| GOTS | Certified suppliers database | Results injected by JavaScript |
| Cradle to Cradle | Certified products registry | Per-product pages are crawlable |
| USDA BioPreferred | Catalog | JSF session-based, times out |
| B Corp | Find a B Corp directory | Per-company pages are crawlable |
| ZDHC | Gateway | Chemical conformance, not product certification |
| bluesign | System partners | |

Several of these cannot be queried by URL. If you could not complete a database query, say the negative rests on site-restricted web search rather than a completed query, and do not write "searched".

**None of these registries holds REACH registrations, chemical safety dossiers, flammability certificates, LCAs or test reports.** A search of them can never support a negative finding about any of those. When a company claims certifications and you cannot find them, add a pre-publication note for MII to search manually, and if MII still cannot find them, to ask the company for a copy.

### Chemical and safety compliance

Start from what Step 0 already captured: the company's production location(s), and, once Topic 8, Commercial Traction & Partnerships, or the company's own statements establish it, its target market(s). Two different jurisdictional questions follow, and they are not the same question.

**Production location governs labor law, environmental and discharge law, and the chemical-registration regime the factory itself must comply with to manufacture.** These bind wherever the material is actually made, regardless of where the finished product is later sold. Check each country where the company manufactures.

**Point of sale governs what can be in the finished product when it reaches a buyer.** These bind wherever the product is sold, regardless of where it was made. This part of the search is fairly consistent across reports, because most MII evaluation targets are trying to sell into EU and/or US markets whatever their production location: default to checking both, and add another market only where research shows the company specifically targets it too.

**Chemical-registration regimes at the production location:**

- **China:** the Inventory of Existing Chemical Substances in China (IECSC), maintained by the Ministry of Ecology and Environment under MEE Order No. 12 (widely called "China REACH"). A substance not on IECSC generally requires registration before manufacture or import. This is a separate inventory from REACH's; EU registration status tells you nothing about IECSC status, and vice versa.
- **Japan:** the Chemical Substances Control Law (CSCL, commonly called Kashinho), jointly administered by METI, MHLW and MOE, with its own existing- and new-substance inventory.
- **South Korea:** K-REACH (Act on Registration and Evaluation of Chemicals), with its own inventory (KECL), following broadly the same registration logic as EU REACH but as a fully separate system.
- **India:** no single India-wide REACH equivalent exists. Restricted-substance rules are narrower and sit in specific instruments, for example the Environment (Protection) Act notification banning listed azo dyes in textiles and leather, enforced through pre-shipment certification on import rather than a general chemical registration regime. "No India-wide chemical registration law was found" is a legitimate finding here, provided you say what you checked, not a sign the search fell short.
- **Global first pass:** OECD eChemPortal searches across many of the national inventories above at once, including ECHA REACH, US, Japan and Korea sources, hosted by ECHA on OECD's behalf. Useful to see what exists before going to the national source, not a substitute for checking that source directly.

**Labor and environmental/discharge law at the production location** rarely has a single searchable index outside a handful of countries. Check the production country's own labor ministry and environmental ministry sites for factory-level requirements, and treat ILO country profiles as orientation rather than a citable compliance record. Where no usable public source exists for a jurisdiction, say that explicitly rather than letting silence read as clean.

**Restricted substances used in manufacturing:** ZDHC MRSL conformance is company-declared; check the ZDHC Gateway. This is an industry-wide standard rather than a jurisdiction-specific law, and it is often the only benchmark available where local environmental or occupational-chemical law is hard to find or unpublished in English.

**Chemical and safety rules governing the finished product, at the point of sale:**

- **REACH registration:** ECHA registered substances database.
- **SVHC:** ECHA Candidate List.
- **US:** EPA TSCA inventory; CPSIA for children's products.
- **Flammability:** FMVSS 302 is 49 CFR 571.302. Cal TB 117-2013 for furniture. BS 5852 and EN 1021-1/-2 in the UK and EU. GB 8410 in China, for automotive interiors, broadly analogous to FMVSS 302 in what it tests, and relevant here where China is itself a target market rather than only a production location; searchable via the National Standard Full-Text Open System (openstd.samr.gov.cn, full text of mandatory GB standards) or the National Public Service Platform for Standards Information (std.samr.gov.cn, bibliographic search with English keyword support). ISO 3795 internationally. These are test standards, and conformance is demonstrated by a test-house report that is almost never published. Absence from public sources is weak evidence; say so.

### LCA and environmental data

- **Published LCAs:** the company's own site first, then Google Scholar, then EPD registries, then the incubator or research institute if the company came out of one. EPD registries are region-specific rather than one global list: EPD International, EPD Norge and IBU cover much of Europe; SuMPO EPD (formerly EcoLeaf) is Japan's equivalent, third-party verified under the same ISO 14025 framework and searchable at ecoleaf-label.jp. Check the program operator relevant to the company's home market or its largest customer market, not only the European ones, since a company selling mainly into Japan may never have registered with a European operator at all. China's EPD landscape is more fragmented, organised by industry (steel and aluminium each have their own scheme, for example) rather than one general registry; where a Chinese company claims an EPD, ask which program operator issued it rather than assuming a Western search will surface it.
- **Read the funding statement.** An LCA commissioned or authored by a producer of the material is industry data even in a peer-reviewed journal.
- **Check scope before comparing anything.** Cradle-to-gate against cradle-to-grave is not a comparison. Different functional units, allocation methods, electricity grids or reference years make two numbers from two studies uncomparable, and presenting them as a comparison invents a finding.
- **Higg MSI and similar indices are self-reported industry data,** never independent.

### Funding and investors

- **Primary:** the register (share allotments, charges), regulatory filings where they exist, and the investor's own announcement.
- **Secondary:** PitchBook, Crunchbase, Tracxn, Dealroom. Treat as pointers. PitchBook's public preview often shows a total raised figure and a list of deal types with amounts withheld; that visible total is citable if you say what was visible and what was paywalled.
- **Check the investors still exist.** Visit the fund's site, check the register where applicable, and look for recent activity. A dead investor website is a finding; add a pre-publication note for MII to evaluate its importance.

### Financial health and solvency signals

Most MII evaluation targets are private, so the numbers a public-market investor pulls from EDGAR mostly do not exist for them. Use the proxies below, and do not manufacture the missing ratios.

**What is public for a private target:**

| Signal | Where | Notes |
|---|---|---|
| Paid-up and authorized capital | The statutory register — see *Corporate facts*, above | Often the single most informative number on an early-stage company. |
| Secured debt and liens | UCC-1/UCC-3 filings, state Secretary of State (US); equivalent charges registers elsewhere (Companies House "charges" tab for UK, MCA charges for India) | Shows what is pledged as collateral and to whom. A facility secured against IP or inventory is a real signal even with no financial statements attached. |
| Litigation | PACER (US federal), state court dockets, equivalent national court search systems | Look for supplier, customer, and IP disputes, not only headline lawsuits. |
| Patent/trademark maintenance status | USPTO/Espacenet/national office, per *Patents and trademarks*, above | A lapsed patent on a company's core technology (missed maintenance fee) is a de facto negative funding signal. Check status, not just existence. |
| Regulatory enforcement | EPA ECHO, OSHA establishment search, FTC, state AG press releases (industry-dependent) | US-centric; searchable enforcement databases at this level of detail are rare outside the US. Where no equivalent exists for the company's jurisdiction, say that rather than treating the absence of enforcement history as clean. |

**What funding databases give you, and what they don't:** Crunchbase, PitchBook, Tracxn, and Dealroom (see *Funding and investors*, above) show raise totals and round dates but essentially never show revenue, margin, or burn. Treat any of those figures sourced only to an aggregator as unverified and say so.

**Customer concentration** is almost never publicly disclosed for a private company. If a company names anchor customers in press releases or on its site, that is `[Industry/self-reported]` and tells you about marketing choices, not revenue share. Do not infer concentration from it.

**If the target, or a major investor in it, is a public company**, EDGAR carries a different set of numbers entirely:

| Filing | What it gives you |
|---|---|
| 10-K / 10-Q | Revenue, gross margin, revenue growth, cash and cash equivalents, burn rate (cash flow statement + MD&A), debt load |
| Forms 3, 4, 5 | Insider (officer/director/large holder) purchases and sales |
| 13F | Institutional ownership |
| DEF 14A (proxy) | Executive compensation, related-party transactions |
| 10-K, Item 3 | Legal proceedings |

Cite the filing and item/section, not "the 10-K," per Sourcing Rule 8, above.

### Regulation

Which jurisdiction's law is relevant depends on what the specific regulation governs, the same distinction set out in full in "Chemical and safety compliance," above: a law about factory conditions, discharge or workplace chemical exposure binds the production location; a law about what a product must contain, disclose or avoid to be sold binds the target market. Everything below (EU, pending EU legislation, US, national labelling) is point-of-sale regulation, and the EU/US default from that section applies here too.

- **EU:** EUR-Lex, using the consolidated text rather than the original OJ version, so you see amendments. Check the ELI identifier and the "in force" status. For framework regulations, find the delegated and implementing acts and the working plan, since the framework itself often imposes nothing.
- **Pending EU legislation:** the European Parliament Legislative Train records status, dates and whether a proposal has stalled or been withdrawn. Check it before describing anything as forthcoming law.
- **US:** eCFR for regulations, Federal Register for pending rules.
- **India:** India Code (indiacode.nic.in), the official Government of India repository. Free, in English, searchable by short title, act number, year and ministry, and covers both central and state legislation with subordinate rules, notifications and orders linked from the parent act. Useful for production-location law (India's labor and environmental statutes) as well as point-of-sale law, since it is a general repository rather than one or the other.
- **China:** there is no single English-language consolidated code comparable to EUR-Lex or eCFR. National standards (GB, GB/T) are searchable at std.samr.gov.cn (bibliographic records, English keyword search) and openstd.samr.gov.cn (full text of mandatory GB standards); broader statutes sit with the relevant ministry and are usually easiest to locate via a specialist regulatory-tracking service (for example REACH24H or CIRS Group's China updates) used as a pointer to the primary text, the same way Tracxn or PitchBook are pointers rather than citations for corporate facts, per sourcing rule 2.
- **National labelling laws:** the ICT/leather-council labelling legislation database is a useful index for leather terminology rules by country.
- **Where no consolidated index exists for a jurisdiction,** say so, and cite the specific ministry, agency or gazette notice rather than a general "the law requires" sentence with no locator. Sourcing rule 8 still applies in full regardless of how hard the primary text was to find.

### Company claims

The company's own properties are the right source for what the company claims, and the wrong source for whether the claim is true. Capture all of them and archive each:

Main site (home, about, material or technology, impact or sustainability, FAQ, contact), any second brand site, LinkedIn company page, press releases and newsroom, conference and trade-fair listings, and any sponsored or partner content, which is `[Industry/self-reported]` regardless of the masthead.

Read the FAQ closely. It is usually where the most specific and most testable claims live, and where terminology drift shows up most clearly.

## Search protocol

Read this in full before Topic 1. "Where to look," above, tells you which source is authoritative for a claim, and you will return to it topic by topic; this section tells you how hard to look before you are allowed to conclude the source does not exist, and it applies to every topic from the start.

The two failures this section prevents are different from the sourcing failures above, and they are harder to see. A report can cite everything correctly, rate everything honestly, document every search it ran, and still be wrong, because it ran one search where five were needed and then described the gap in impeccable prose. A well-documented negative finding looks exactly like a well-researched one. Nothing downstream in this skill can tell them apart, which is why the discipline has to sit here, at the point of searching.

### Why a documented negative is not the same as a completed search

Sourcing Rule 7, above, requires every negative finding to name the database, the query and the date. That rule is right, and it is not enough on its own, because it is satisfiable by a single failed query. "We searched InPASS on 14 August 2026 and found no patent filings" passes rule 7, passes the pre-submission checks, and reads as diligence. If the filing exists under the company's legal name rather than its brand name, that sentence is false, and MII has published it.

The asymmetry to keep in mind: a false positive gets caught. Someone clicks the endnote and the source does not say what the report claims. A false negative never gets caught, because there is no link to click. The company knows, and MII finds out on the call, which is the worst place to find out.

So the rule this section adds is a floor, not a ceiling:

**A negative finding rests on the minimum coverage for its claim type, or it is not a finding yet. Where you cannot reach that floor, the honest output is "we could not complete this search", not "we searched and found nothing".** Those are different sentences with different meanings, and the confidence ratings already distinguish them: the first is Not Established, the second is a pre-publication note, never a finding.

### Step 1: Build the identity block before Topic 1

This is the single highest-value ten minutes in the whole evaluation, and skipping it is the most common cause of a false negative.

Search engines and patent, trademark and regulatory registers index by **legal entity name** and by **natural person name**. They do not index by brand. A company trading as "Banofi" may hold its filings under a private limited entity name that shares no words with the brand, and a search of any patent index for the brand returns a clean, fast, confident nothing. That nothing is indistinguishable from an absence unless you already knew to search something else.

You will have pulled the statutory registry record already, because the order of work puts it first. Before you run a single topic search, extract from it and write down:

| Field | Where it comes from | Why it matters |
|---|---|---|
| **Exact legal entity name** | Registry record, character for character | The applicant name on any filing |
| **Registration number** | CIN, company number, UEN, entity number | Unambiguous key; some registers search by it only |
| **Former names and dates** | Registry filing history | Filings made under the old name stay under the old name |
| **Brand and material names** | Company site, packaging, press | Trademark searches; rarely patent searches |
| **Founder and director full names** | Registry, with appointment dates | Inventor and applicant fields; often the only route in |
| **Name transliteration variants** | Judgement | Indian, Chinese, Korean and Arabic names transliterate several ways; a register holds one spelling |
| **Registered office and operating site** | Registry vs company site | Jurisdiction for filings, consents and local press |
| **Domains** | Site, WHOIS where informative | Second brand sites, dead microsites |
| **Parent, subsidiary or predecessor entities** | Registry, funding announcements | IP is frequently held by a different entity from the one that trades |

That last row deserves attention on its own. Early-stage companies often assign IP to a founder personally, to a predecessor entity, or to a holding company in another jurisdiction. A patent search against the trading entity alone will miss all three, and the miss is invisible.

**Every subsequent search in the evaluation runs against this block, not against the brand name.** When you record a search in the search record, record which variant you used. A search record that shows twelve queries all using the brand name documents one search performed twelve times.

### Step 2: The escalation ladder

Run this for any claim where the first attempt comes back empty. Stop as soon as you find the thing; you are not obliged to complete the ladder when the answer arrives on rung one.

**This stopping rule does not discharge the coverage floors below.** The floors are coverage requirements rather than stopping rules, and they exist because a second filing can sit under a different name or field from the first. Finding one patent under the entity name does not excuse the inventor-field and founder-name searches.

1. **Primary register, primary name.** The authoritative source from "Where to look," above, queried with the legal entity name.
2. **Primary register, other identity-block variants.** Former names, founder and director names, parent and predecessor entities, registration number.
3. **Mirrors and aggregating indexes of the same register.** Where the official register is captcha-gated, JavaScript-only, session-broken or simply down, a third-party mirror queries the same underlying data. This rung is not optional and it is not a lesser substitute: for several registers it is the only route that works from a tool. See the per-claim table below for the mirrors that matter.
4. **Independent indexes covering the same jurisdiction.** For patents this means a different patent office's worldwide collection, not a different page of the same one.
5. **Adjacent artefact.** The thing itself may be unreachable while its trace is public: an official gazette or journal, a grant or consent list, an EPD registry entry, a tender record, a court or opposition filing.
6. **Company-side corroboration, read as a pointer only.** A press release naming a filing number is not evidence the filing exists, but it gives you a number to search on rung one. Follow it back down the ladder.

**A negative recorded on rung 1 alone is not a finding. It is an unfinished search.** The rungs exist because each one fails for a different reason, so failing one tells you very little about the others.

### Step 3: Minimum coverage by claim type

Before writing Not Established (see the confidence ratings in `SKILL.md` for how this is distinct from Unconfirmed), the search must have covered at least the following. Where the floor is not met, write that the search could not be completed, say what blocked it, and add a pre-publication note for MII to complete the search manually. This applies to every claim type below, whichever specific tool or portal is the one that would not cooperate.

#### Patents

The highest-risk category in this report type, and the one where a false negative does the most damage, because "we found no patents" sits next to a company claiming a patented technology and reads as a serious finding.

**Floor: at least three independent indexes, at least three identity-block variants including the founders' personal names, and the national office search or its published journal or gazette where one exists.**

- Google Patents, Espacenet worldwide, WIPO Patentscope and Lens.org are independent of each other and cover most national collections. Two of them disagreeing is informative; one of them empty is not. They are not by themselves coverage of a domestic Indian, Chinese or Korean filing, which reaches them with lag and sometimes as a bibliographic stub, which is why the national route is part of the floor.
- Search by **applicant/assignee** and by **inventor** separately. These are different fields and a filing missing from one appears in the other.
- The national office and its journal are **part of the floor, not an optional extra**, because they are where a domestic filing appears first. Where the office's own search is unreachable, which InPASS routinely is, its failure does not discharge this part of the floor: the journal does. India's Patent Office Journal is weekly, public and carries published applications that a flaky search interface never surfaces.
- Attempt the national office search anyway (InPASS for India), and record the attempt whether or not it succeeds. Never let its failure alone stand as the negative; escalate to rung 3 and 4.

**Three distinctions to hold, because collapsing them produces a wrong finding in either direction:**

- **Filed is not granted.** An application is not a patent. A company saying "patented" on the strength of a pending application is a contradiction worth logging, not evidence of a grant.
- **Not published is not not filed.** Applications publish eighteen months after the priority date almost everywhere. A filing made ten months ago is invisible to every index listed above and genuinely exists. Where the company was founded recently, say this explicitly rather than reporting an absence: the correct sentence names the eighteen-month window and states that a recent filing would not yet appear.
- **Not found under this name is not not filed.** Which is what the identity block is for.

#### Trademarks

**Floor: the official register plus at least one mirror, plus WIPO Global Brand Database, under the mark as written and the legal entity as applicant.**

IP India's public search is captcha and OTP gated and usually cannot be operated from a tool. Queryable mirrors carry the same registry data and are the route that works. WIPO's Global Brand Database covers national collections as well as Madrid filings. A ® with no registration you can find is a finding worth reporting, but only after the mirror has been tried, because the official register being unqueryable is the normal case rather than the exception.

#### Corporate facts

**Floor: the statutory register itself, and where its document layer is paywalled, two independent aggregators that reproduce filings.**

For India the core MCA fields are reproduced free by ZaubaCorp, Tofler, TheCompanyCheck, IndiaFilings and Falcon eBiz. Cross-check two, cite the MCA record by CIN, and note the retrieval route. Two aggregators agreeing on a paid-up capital figure they both pull from the same filing is one source, not two, so say where the number originates.

#### Published LCA, test reports and certifications

**Floor: the scheme's own registry where one exists, plus Google Scholar, plus the EPD registries, plus the incubator or research institute the company came out of.**

Note the asymmetry "Where to look" already flags and this floor enforces: certification registries hold certifications. They are not evidence about REACH, chemical dossiers, flammability certificates, LCAs or test reports, and a search of them can never be cited for the absence of any of those. Each of those needs its own floor and its own search record entry.

Where a document type is routinely confidential, which covers most test reports and chemical inventories, meeting the floor still only supports "not public", never "does not exist". Write the weaker sentence.

#### Funding and investors

**Floor: the register's share allotment and charge filings, plus the investor's own announcement, plus a live-status check on every named investor's site.**

The live check is cheap and reproducible, and a lead investor's domain that now parks or redirects is a finding in its own right.

#### Regulation

**Floor: the consolidated text on the official source, the in-force status, and a check for delegated or implementing acts covering this product category.**

Never a floor met by secondary commentary. Sourcing Rule 8, above, governs what you then write; this floor governs whether you looked. Check the Legislative Train for anything described as forthcoming, and check the last twelve months of amendments before describing a trend in either direction.

### Step 4: The search record

Every search goes in your working search record, kept as you go, whether it succeeded or failed. Failed searches are the ones that carry weight downstream, because they are what a negative finding rests on, but recording only failures makes the record impossible to audit for coverage.

One numbered row each:

| # | Claim it bears on | Source or database | Exact query string | Identity variant used | Date | Rung | Result |
|---|---|---|---|---|---|---|---|

The **identity variant** and **rung** columns are what make coverage visible at a glance. Note that nothing downstream checks them for you: `citation-audit` verifies that cited sources support their claims, which is the opposite failure, and it has no instrument for judging whether a search went deep enough. Coverage is checked here or not at all. Twelve rows at rung 1 under one name variant is a thin search that looks thorough until you add those two columns, at which point it is obvious.

When you write a Not Established finding, cite the specific row numbers that establish its floor. A Not Established that cannot point at rows meeting its floor has not earned the rating.

### Step 5: Capture the quote and the screenshot when you read the source, not later

This belongs to the protocol rather than to the writing stage, because it only works if it happens while the page is open.

Sourcing Rule 4, above, governs verification; this is where the evidence card it depends on actually gets filled, because that is a research-time action rather than a writing-time one. Each card carries: the exact quote supporting the claim, the source and locator, and a screenshot of the passage, per the screenshot folder specification in `output-spec.md`. All three are filled while the page is open, not reconstructed afterwards.

The reason for capturing rather than intending: checking a citation later means reopening a page you have already read, at a point where a hundred and thirty of them exist and re-reading them all is not going to happen. So it does not happen, and the check gets attested rather than performed. Capturing the quote and the screenshot while the page is open costs seconds and makes the later check unnecessary, because the evidence is already sitting next to the claim.

It also catches the specific failure that recurs in this report type. When the passage is pasted next to the sentence being written, a claim the source does not quite make becomes obvious immediately, and a qualifier the summary dropped is visible in the quotation. "Will be available" cannot silently become "is available" when the words are sitting there. The screenshot catches the same failure a different way: if you cannot point at the sentence in the image, the citation has not actually been verified, whatever the quote field says.

**A claim whose evidence card has an empty quote field, or no matching screenshot, cannot be written.** Either open the source and fill both, or write the claim as one MII could not verify.

Two cards where one might seem enough: where a sentence makes several assertions, each assertion needs its own card, and its own screenshot if the assertions sit in different places on the page, or an explicit note of which card carries which. Partial coverage presented as full coverage is the failure Sourcing Rule 4 exists to stop, and cards, screenshots included, are what make it visible.

### The checklist

Copy this into your working notes at the start of the research and tick items as you complete them. It is here because the failures above are all failures of omission, and omissions are hard to notice from the inside. A list you are visibly working through is harder to skip than a standard you are trying to remember.

```
Research coverage:
- [ ] Registry record pulled, identity block built and written down
- [ ] Former names, founder names and any parent or predecessor entity captured
- [ ] Every topic search run against identity-block variants, not the brand name alone
- [ ] Patents: 3+ independent indexes, applicant and inventor fields, 3+ name variants including a founder's personal name
- [ ] Patents: national office attempted and its published journal or gazette checked
- [ ] Patents: filed vs granted, and the 18-month publication window, addressed explicitly
- [ ] Trademarks: official register attempted, mirror queried, WIPO checked
- [ ] Every certification, LCA and test claim searched against its own floor, not a shared one
- [ ] Every named investor live-status checked
- [ ] Every regulation checked for in-force status and delegated acts
- [ ] Search record complete, with identity variant and rung columns filled
- [ ] Every Not Established points at search-record rows that meet its floor
- [ ] Every intended citation has an evidence card with a verbatim quote and a screenshot
- [ ] Searches that could not be completed are recorded as such, not as completed searches
```

### A blocker is an escalation, not an exit

A stress test of this protocol found the one cheap way out that remains, and it is worth naming so you recognise it in yourself. Every floor below can be discharged by writing "we ran this search but could not reach its coverage floor" and logging a blocker. That sentence is honest, it is sanctioned, and it costs nothing. A researcher under time pressure can produce a fully compliant evaluation in which most of the work has been converted into paperwork, and every individual sentence in it is true.

So three rules bound it.

**A blocker is only available after the ladder is exhausted, and it records which rungs were tried.** "Could not reach the floor" following one query is not a blocker, it is an unstarted search. The blocker entry names each rung attempted and how it failed, which is also what tells the person picking it up where to resume.

**A topic that received no search at all is not a blocker on that topic; it is unfinished work, and it is a more serious problem than a documented blocker.** A blocker means MII tried and hit a real limit. A topic skipped for time or scope reasons has not been researched, and writing it up in blocker language, such as "MII did not attempt this topic in this session," makes an incomplete evaluation read like a diligently-flagged gap when it is actually a missing topic. Where a genuine constraint (time, session length, tool availability) means a topic cannot be researched at all, raise it as its own named limitation on the whole evaluation in a pre-publication note at the top of the report, and say it directly to the person who commissioned the work, rather than filing it as one blocker row among several lower down. It does not go in the recommendation or anywhere else in the report's visible text, which is written for the external reader, not for MII. Do not represent a report as a completed first-pass draft if any of the ten topics received zero searches.

**A blocker on a load-bearing claim stops publication rather than travelling with the report.** Patents where the company advertises patented technology, an LCA where the company markets a carbon figure, a certification the company displays: these are the claims a reader acts on. Where the floor was not met on one of them, the report is not publishable, and it carries a pre-publication note at that exact claim saying so in those words. Blockers on peripheral claims can travel.

**Count the blockers and say the number.** Report the count in a pre-publication note (see `output-spec.md`), alongside the count of completed searches. One or two blockers in an evaluation is ordinary and reflects registers that genuinely cannot be operated. A report where blockers outnumber completed searches has not researched the company, whatever its prose suggests, and the count is the only thing that makes that visible at a glance. Where that is the state of the work, say so to the person who commissioned it before delivering, rather than handing over a document whose blocker list is the actual finding.

The test of whether you are escalating or exiting is simple. An escalation names the next thing someone could do. An exit names only what could not be done.

### When the floor cannot be met

Say so precisely, and let the confidence ratings do their work. Not Established already separates a completed search that found nothing from a search that could not be run, and this protocol gives you a third thing worth stating: a search that was run but could not reach its floor.

- "We searched Google Patents, Espacenet and Lens.org on [date] under the legal entity name, both founder names and the former entity name, and found no filings." A completed search meeting its floor. Not Established, and a real finding.
- "InPASS could not be operated on [date]; the negative below rests on Google Patents, Espacenet and Lens.org." Floor met by other rungs. Say which rung carried it.
- "We could not complete a trademark search: IP India is captcha-gated and the mirror returned no results page." Floor not met. Record it as a pre-publication blocker under the same rule that governs archive capture, and do not write a negative finding on it.

The third sentence is the one that takes discipline, because it is an admission rather than a finding and there is always a temptation to round it up to the first. Rounding up is how a report ends up asserting something MII never established, which is the failure this entire skill is built to prevent.

## Finding contradictions

Read this before starting Topic 1 too. Knowing what you are hunting is what makes you find it, and it is what turns the company document (see `output-spec.md`) from generic into something the company cannot deflect. "Please share your LCA" gets a brochure. "Your FAQ says 98 to 100% bio-based and your August vendor profile says 99.7%, which is current?" gets an answer, or gets a silence that is itself informative. A generic document could be written before the research starts; that is the tell. Hunt for these deliberately rather than waiting for them to surface.

### Tone

Contradictions are not accusations, and neither the working notes nor the company document should read as though they caught someone. Most have dull explanations. A registered office in a different city from the stated headquarters usually means the founder registered the company where the plant is. Two different bio-based percentages usually means one page was updated and another was not. Write in a tone that signals MII is here to help, not to catch anyone out.

Write them neutrally, state both sources, and ask. The value to MII is that it asks rather than guesses, and that a reader can see the discrepancy exists and judge for themselves.

### 1. Registry versus self-reported

The statutory record disagrees with the company's own description of itself. Almost always worth checking first, because the registry is free and authoritative and nobody looks.

**Real example.** A report stated "registered with RoC Kanpur; headquarters listed as Kolkata, West Bengal", citing a startup database and a self-maintained profile. The MCA record gives the registered office as B-55 Block C-1 Shashtripuram, Agra, Uttar Pradesh, which is also what makes RoC Kanpur coherent, since Kanpur is the RoC for Uttar Pradesh. Agra is India's principal footwear manufacturing cluster, which is materially relevant to a supply-chain assessment. The report had built an interview question around the apparent Kanpur/Kolkata mystery that the registry already answered.

**Look for:** registered office vs stated HQ, incorporation date vs claimed founding year, directors on the register vs the team page, paid-up capital vs claimed funding, company status vs claimed operations.

**Question shape:** state both records, then ask which applies to what, and explain why it matters.

> Your MCA record gives the registered office as [address] and lists RoC [x], while your company profiles list [city] as headquarters and the plant address is not disclosed. Where is each function actually located, and which address should MII use?

### 2. Source versus source

Two external sources give different figures for the same thing.

**Real example.** One announcement gave phase-1 output of 1,000 sqm per day scaling to 1 million sqm per year. A vendor profile four months later gave 6 million square feet per year, which is about 560,000 sqm, and a target of 20% of India's bovine leather production. Three capacity figures, none reconciling.

**Question shape:** put the figures side by side with their dates, sources, and ask which is current.

> Published capacity figures for your facility include 1,000 sqm/day (April 2025), 1 million sqm/year at full scale (April 2025), and 6 million sq ft/year, about 560,000 sqm (August 2025). Which is current, what is actual output today, and what explains the difference between the annual figures?

### 3. Company versus itself

Two of the company's own pages, or a page and a press release, disagree. These are the most useful of all, because there is no third party to blame and no ambiguity about whose claim it is.

**Real example.** The FAQ said 98 to 100% bio-based. A vendor profile in the company's own voice said 99.7%. Both were accurately cited in the report, four sections apart, and the report never noticed.

**Look for:** percentages, capacity, founding dates, team size, certifications, and the same property described differently on the main brand site and a second brand site.

**Question shape:** name both figures and ask for the test that settles it.

> Your FAQ states the material is 98 to 100% bio-based; an August 2025 vendor profile states 99.7%. Which is current, and can you provide an ASTM D6866 radiocarbon report?

### 4. Claim versus absence of evidence

The company asserts something has been done, and publishes nothing showing it.

This is distinct from "we found no data". The company saying "extensively tested" while publishing no test report is a stronger and more useful finding than silence, because it establishes that reports should exist and can be requested by name.

**Real example.** The FAQ said the material "has been extensively tested to ensure that it meets the durability of animal leather", and a press release said "robust testing underlines the material's ability to withstand stringent operational standards". The report's performance section stated flatly that no third-party test data was located, and never mentioned that testing was claimed.

**Look for:** "extensively tested", "certified", "patented", "verified", "proven", "clinically shown", and any use of ® or ™ you cannot corroborate in a register.

**Question shape:** quote the claim, then ask for the artefact by name.

> Your FAQ states the material "has been extensively tested to ensure that it meets the durability of animal leather". Please provide those test reports: laboratory, standard, date, sample, and result. If testing was internal, say so.

> Your Material Story page refers to a "patented formula" and an April 2025 press release to a "patented bio-scaffold". MII located no granted patent or published application in Google Patents or USPTO under the company or founder names. Please provide application and grant numbers with jurisdictions, or confirm the protection is trade-secret based.

### 5. Arithmetic that does not work

Figures that cannot both be true. Recompute everything; this is the cheapest finding in the report and it is often the most substantive.

**Real example.** 1,000 sqm per day and 1 million sqm per year. Continuous operation at 1,000 sqm/day gives roughly 365,000 sqm/year. Reaching 1 million requires nearly tripling daily output, which the announcement did not mention. The report reproduced both figures without doing the multiplication.

**Look for:** daily output against annual capacity, unit conversions (sq ft to sqm, kg to tonnes, lakh and crore to USD), percentages that do not sum, funding totals against the sum of disclosed rounds, revenue against claimed customer counts, and capex implied by a plant against disclosed capital.

**Question shape:** show the arithmetic, then ask what closes the gap.

> At 1,000 sqm/day and continuous operation, annual output is about 365,000 sqm. Reaching 1 million sqm/year implies roughly tripling daily throughput. What increase in line count or output rate closes that gap, on what timeline, and what capex does it require?

### 6. Timeline conflicts

Origin stories that do not line up.

**Real example.** The About page timeline placed inception in 2020. A company press release described the founder's work on leather alternatives beginning in 2015, a planned direct-to-consumer brand, and B2B partnerships with defence and safety footwear by 2017. The report cited both sources and reconciled neither, while also asserting that no prior ventures were publicly documented.

**Look for:** founding year vs incorporation date vs "journey began" narratives, prototype dates, first-sale dates, plant commissioning vs announcement, and gaps that suggest an earlier entity.

**Question shape:** lay out the dates and ask for the sequence.

> Your About page dates inception to 2020, while an April 2025 press release describes work on leather alternatives from 2015 and B2B partnerships from 2017. Were there prior entities, ventures or products before the 2021 incorporation, and what became of them?

### 7. Terminology drift

The company answers a question about one property with evidence about a different one, or uses a term whose technical meaning is narrower than the impression it creates.

**Real example.** Asked directly "Is Eori Vegan Leather Biodegradable?", the FAQ answer addressed only bio-based content and optional non-biodegradable additives. The word biodegradable appeared in the question and in the phrase "non-biodegradable content", and nowhere as an assertion. Bio-based is about feedstock origin; biodegradable is about end of life.

**Look for:** bio-based answering biodegradable, recyclable answering recycled, plastic-free answering non-toxic, carbon negative with no boundary or verifier, compostable with no standard named, "natural" doing undefined work, and any claim about a property where the evidence offered is about a different property.

**Question shape:** name the substitution, then ask for the right evidence.

> Your FAQ answers the biodegradability question with bio-based content, which is a different property. Please provide biodegradation or compostability test data against a named standard (ISO 20200, ASTM D5511, ASTM D6400), including the conditions tested, and confirm whether the claim covers the variants containing the optional 2% non-biodegradable additive.

### 8. Status decay

Something that was true when it was published is no longer true, or a cited third party has changed state.

**Real example.** The report described a named venture fund as the company's largest institutional investor and cited the fund's website. By publication the domain redirected to a GoDaddy for-sale parking page. The fund's site had gone dark, which bears directly on an assessment of the company's backing.

**Look for:** investor websites and funds, cited certifications with expiry dates, superseded standards, repealed or amended regulations, plants announced but never confirmed operational, named partners who have since exited, and any press release older than about eighteen months.

**Question shape:** state what changed and ask what it means.

> Public sources list [Fund] as your lead institutional investor from [date]. As of [date] the fund's website is no longer live. Is [Fund] still an active shareholder, are they participating in future rounds, and who currently sits on your cap table?

How each entry gets logged, turned into a question, and delivered is in `output-spec.md`, under "The company document."
