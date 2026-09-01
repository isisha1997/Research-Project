import io
import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from helpers import FakeResolver, crossref_body

from mii_guide.audit import audit, infer_tier
from mii_guide.cli import main
from mii_guide.extract import (
    Extracted, ExtractionError, Reference, extract, find_references,
)
from mii_guide.models import SourceTier
from mii_guide.resolve import CitationResolver


class ExtractTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)

    def write(self, name, body):
        path = self.root / name
        path.write_text(body, encoding="utf-8")
        return path


class TestReferenceFinding(unittest.TestCase):
    def refs(self, text, **kwargs):
        return find_references(Extracted(text, "md", **kwargs))

    def test_finds_a_bare_doi(self):
        found = self.refs("See 10.1016/j.marpolbul.2016.09.025 for detail.")
        self.assertEqual([(r.kind, r.raw) for r in found],
                         [("doi", "10.1016/j.marpolbul.2016.09.025")])

    def test_strips_trailing_sentence_punctuation(self):
        self.assertEqual(self.refs("(10.1000/abc).")[0].raw, "10.1000/abc")
        self.assertEqual(self.refs("see 10.1000/abc, and more")[0].raw, "10.1000/abc")

    def test_a_doi_org_link_is_recorded_once_as_a_doi(self):
        found = self.refs("https://doi.org/10.1000/abc")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].kind, "doi")

    def test_the_same_reference_twice_is_recorded_once(self):
        self.assertEqual(len(self.refs("10.1000/abc and again 10.1000/abc")), 1)

    def test_records_the_line_number(self):
        self.assertEqual(self.refs("intro\nmiddle\nsee 10.1000/abc")[0].line, 3)

    def test_keeps_the_context_line_for_later_comparison(self):
        found = self.refs("Napper and Thompson (2016). Release of fibres. 10.1000/abc")
        self.assertIn("Napper", found[0].context)

    def test_hyperlink_targets_are_found_even_when_invisible_in_the_text(self):
        found = self.refs("Read the study.", linked_urls=["https://example.org/study"])
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].from_hyperlink)

    def test_a_document_with_no_references_yields_none(self):
        self.assertEqual(self.refs("Plain prose with no citations at all."), [])


class TestExtractors(ExtractTestCase):
    def test_markdown_is_read_in_full(self):
        path = self.write("a.md", "# Title\n\nSee 10.1000/abc\n")
        result = extract(path)
        self.assertTrue(result.is_complete)
        self.assertIn("10.1000/abc", result.text)

    def test_html_tags_are_stripped_and_hrefs_captured(self):
        path = self.write("a.html", '<p>Body <a href="https://example.org/x">link</a></p>')
        result = extract(path)
        self.assertNotIn("<p>", result.text)
        self.assertIn("https://example.org/x", result.linked_urls)

    def test_html_script_contents_are_not_treated_as_prose(self):
        path = self.write("a.html", "<script>var doi='10.9999/fake';</script><p>Body</p>")
        self.assertNotIn("10.9999/fake", extract(path).text)

    def test_docx_text_and_hyperlink_targets_are_both_recovered(self):
        path = self.root / "a.docx"
        document = ('<w:document><w:body>'
                    '<w:p><w:r><w:t>Recycled polyester sheds fibres.</w:t></w:r></w:p>'
                    '<w:p><w:r><w:t>See 10.1000/abc</w:t></w:r></w:p>'
                    '</w:body></w:document>')
        rels = ('<Relationships><Relationship Id="rId1" '
                'Target="https://example.org/study" TargetMode="External"/></Relationships>')
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", document)
            z.writestr("word/_rels/document.xml.rels", rels)
        result = extract(path)
        self.assertIn("Recycled polyester sheds fibres.", result.text)
        self.assertIn("https://example.org/study", result.linked_urls)
        self.assertTrue(result.is_complete)

    def test_docx_footnotes_endnotes_and_comments_are_all_read(self):
        # Citations live in footnotes as often as in body text, and in a document
        # under review they live in the comments. Reading only the body returned
        # "no references found" on a document full of them.
        path = self.root / "a.docx"
        def para(text):
            return f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml",
                       f"<w:document><w:body>{para('Body prose here.')}</w:body></w:document>")
            z.writestr("word/footnotes.xml",
                       f"<w:footnotes>{para('Footnote cite 10.1000/foot')}</w:footnotes>")
            z.writestr("word/endnotes.xml",
                       f"<w:endnotes>{para('Endnote cite 10.1000/end')}</w:endnotes>")
            z.writestr("word/comments.xml",
                       f"<w:comments>{para('Reviewer suggests 10.1000/comment')}</w:comments>")
            z.writestr("word/header1.xml",
                       f"<w:hdr>{para('See 10.1000/header')}</w:hdr>")
        found = {r.raw: r.part for r in find_references(extract(path))}
        self.assertEqual(set(found), {"10.1000/foot", "10.1000/end",
                                      "10.1000/comment", "10.1000/header"})
        # Where a citation lives is part of the finding: a DOI a reviewer proposed
        # in a comment is not a citation the document makes.
        self.assertEqual(found["10.1000/comment"], "comments")
        self.assertEqual(found["10.1000/foot"], "footnotes")

    def test_docx_records_which_parts_it_read(self):
        path = self.root / "a.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml",
                       "<w:document><w:body><w:p><w:r><w:t>Body.</w:t>"
                       "</w:r></w:p></w:body></w:document>")
            z.writestr("word/comments.xml",
                       "<w:comments><w:p><w:r><w:t>A note.</w:t></w:r></w:p></w:comments>")
        result = extract(path)
        self.assertIn("body", result.note)
        self.assertIn("comments", result.note)
        self.assertIn("[comments]", result.text)

    def test_docx_hyperlinks_in_footnotes_are_captured_too(self):
        path = self.root / "a.docx"
        rels = ('<Relationships><Relationship Id="rId1" '
                'Target="https://example.org/foot" TargetMode="External"/></Relationships>')
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml",
                       "<w:document><w:body><w:p><w:r><w:t>Body.</w:t>"
                       "</w:r></w:p></w:body></w:document>")
            z.writestr("word/footnotes.xml",
                       "<w:footnotes><w:p><w:r><w:t>see study</w:t></w:r></w:p></w:footnotes>")
            z.writestr("word/_rels/footnotes.xml.rels", rels)
        self.assertIn("https://example.org/foot", extract(path).linked_urls)

    def test_docx_paragraphs_become_separate_lines(self):
        path = self.root / "a.docx"
        document = ('<w:document><w:body>'
                    '<w:p><w:r><w:t>First.</w:t></w:r></w:p>'
                    '<w:p><w:r><w:t>Second 10.1000/abc</w:t></w:r></w:p>'
                    '</w:body></w:document>')
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", document)
        # Line numbers index the extracted text, which opens with a "[body]" marker.
        found = find_references(extract(path))[0]
        self.assertEqual(found.line, 3)
        self.assertEqual(found.part, "body")

    def test_a_zip_that_is_not_a_docx_is_rejected_clearly(self):
        path = self.root / "a.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("hello.txt", "not a word file")
        with self.assertRaises(ExtractionError) as ctx:
            extract(path)
        self.assertIn("not a Word document", str(ctx.exception))

    def test_a_corrupt_docx_is_reported_not_traced(self):
        path = self.write("a.docx", "definitely not a zip")
        with self.assertRaises(ExtractionError):
            extract(path)

    def test_an_unsupported_format_names_what_is_supported(self):
        path = self.write("a.rtf", "x")
        with self.assertRaises(ExtractionError) as ctx:
            extract(path)
        self.assertIn(".docx", str(ctx.exception))

    def test_a_missing_file_is_reported(self):
        with self.assertRaises(ExtractionError):
            extract(self.root / "nope.md")

    def test_a_pdf_read_without_a_library_is_marked_best_effort(self):
        path = self.root / "a.pdf"
        path.write_bytes(b"%PDF-1.4\n/URI (https://example.org/x)\n"
                         b"(Cited 10.1000/abc) Tj\n%%EOF")
        result = extract(path)
        try:
            import pypdf  # noqa: F401
            self.skipTest("pypdf is installed, so the fallback path is not exercised")
        except ImportError:
            pass
        self.assertEqual(result.confidence, "best_effort")
        self.assertIn("not proof of absence", result.note)
        self.assertIn("https://example.org/x", result.linked_urls)

    def test_a_file_that_is_not_a_pdf_is_rejected(self):
        path = self.root / "a.pdf"
        path.write_bytes(b"just some bytes")
        with self.assertRaises(ExtractionError):
            extract(path)


class TestTierInference(unittest.TestCase):
    def tier(self, url):
        return infer_tier(Reference(url, "url", 1, ""))

    def test_a_doi_is_treated_as_peer_reviewed(self):
        self.assertIs(infer_tier(Reference("10.1000/abc", "doi", 1, "")),
                      SourceTier.PEER_REVIEWED)

    def test_publishers_regulators_and_institutions_are_recognised(self):
        self.assertIs(self.tier("https://www.sciencedirect.com/x"), SourceTier.PEER_REVIEWED)
        self.assertIs(self.tier("https://echa.europa.eu/x"), SourceTier.REGULATOR)
        self.assertIs(self.tier("https://textileexchange.org/x"), SourceTier.INSTITUTIONAL)
        self.assertIs(self.tier("https://www.voguebusiness.com/x"), SourceTier.TRADE_PRESS)

    def test_subdomains_match_their_parent(self):
        self.assertIs(self.tier("https://pubs.acs.org/doi/x"), SourceTier.PEER_REVIEWED)

    def test_academic_and_government_tlds_are_recognised_generically(self):
        self.assertIs(self.tier("https://cam.ac.uk/x"), SourceTier.INSTITUTIONAL)
        self.assertIs(self.tier("https://www.canada.gov/x"), SourceTier.REGULATOR)

    def test_an_unknown_domain_stays_unclassified_rather_than_guessed(self):
        self.assertIsNone(self.tier("https://acme-materials.com/our-impact"))

    def test_a_lookalike_domain_does_not_match(self):
        self.assertIsNone(self.tier("https://notepa.gov.example.com/x"))


class TestAudit(ExtractTestCase):
    def audit(self, body, responses=None, name="doc.md"):
        path = self.write(name, body)
        resolver = (FakeResolver(responses) if responses is not None
                    else CitationResolver(online=False))
        return audit(path, resolver)

    def test_a_fabricated_doi_is_an_error_and_a_fact(self):
        report = self.audit("Smith (2020). A study. 10.1000/fake",
                            {"10.1000/fake": ("", "404")})
        self.assertFalse(report.clean)
        error = report.errors[0]
        self.assertEqual(error.kind, "fact")
        self.assertIn("fabricated", error.message)

    def test_a_dead_url_is_an_error(self):
        report = self.audit("See https://example.org/gone", {"example.org": ("", "404")})
        self.assertFalse(report.clean)
        self.assertIn("404", report.errors[0].message)

    def test_a_resolving_doi_is_clean(self):
        report = self.audit("See 10.1000/real",
                            {"10.1000/real": (crossref_body("A Real Paper", 2020), None)})
        self.assertTrue(report.clean)

    def test_an_unreachable_check_warns_rather_than_reporting_clean_silently(self):
        report = self.audit("See 10.1000/x", {"10.1000/x": ("", "Connection refused")})
        self.assertTrue(report.warnings)
        self.assertEqual(report.warnings[0].kind, "fact")

    def test_a_doi_pointing_at_a_different_work_is_flagged_as_heuristic(self):
        body = ("Napper, I.E. and Thompson, R.C. (2016). Release of synthetic microplastic "
                "fibres from domestic washing machines. 10.1000/wrong")
        report = self.audit(body, {"10.1000/wrong": (
            crossref_body("Carbon accounting methods for cement production", 2016), None)})
        flags = [f for f in report.findings if f.kind == "heuristic"]
        self.assertTrue(any("different work" in f.message for f in flags))

    def test_a_matching_reference_line_is_not_flagged(self):
        body = ("Napper, I.E. and Thompson, R.C. (2016). Release of synthetic microplastic "
                "fibres from domestic washing machines. 10.1000/right")
        report = self.audit(body, {"10.1000/right": (crossref_body(
            "Release of synthetic microplastic fibres from domestic washing machines",
            2016), None)})
        self.assertFalse(any("different work" in f.message for f in report.findings))

    def test_a_reference_entry_that_wraps_across_lines_is_not_flagged(self):
        # Reference lists wrap. Comparing only the line carrying the DOI made
        # correct citations look like mismatches.
        body = ("Napper, I.E. and Thompson, R.C. (2016). Release of synthetic microplastic\n"
                "plastic fibres from domestic washing machines: effects of fabric type and\n"
                "washing conditions. Marine Pollution Bulletin. 10.1000/right\n")
        report = self.audit(body, {"10.1000/right": (crossref_body(
            "Release of synthetic microplastic plastic fibres from domestic washing "
            "machines: Effects of fabric type and washing conditions", 2016), None)})
        self.assertFalse(any("different work" in f.message for f in report.findings))

    def test_a_wrapped_entry_whose_doi_points_elsewhere_is_still_flagged(self):
        body = ("Napper, I.E. and Thompson, R.C. (2016). Release of synthetic microplastic\n"
                "plastic fibres from domestic washing machines: effects of fabric type and\n"
                "washing conditions. Marine Pollution Bulletin. 10.1000/wrong\n")
        report = self.audit(body, {"10.1000/wrong": (crossref_body(
            "Carbon accounting methods for cement production in the European Union",
            2016), None)})
        self.assertTrue(any("different work" in f.message for f in report.findings))

    def test_a_bare_inline_doi_never_triggers_the_title_check(self):
        report = self.audit("As shown previously 10.1000/x.", {"10.1000/x": (
            crossref_body("Something Else Entirely", 2016), None)})
        self.assertFalse(any("different work" in f.message for f in report.findings))

    def test_an_uncited_figure_is_flagged_as_heuristic_only(self):
        body = ("Introduction paragraph here.\n\n"
                "Recycled polyester cuts emissions by 45 percent compared with virgin "
                "polyester across the whole supply chain.\n")
        report = self.audit(body)
        flags = [f for f in report.heuristics if "figure appears" in f.message]
        self.assertTrue(flags)
        self.assertEqual(flags[0].severity, "info")
        self.assertTrue(report.clean)  # a heuristic flag never blocks

    def test_figures_inside_word_comments_are_not_flagged(self):
        # Comments are annotations about the text, not the text. Flagging a
        # reviewer's own note for citing nothing is noise.
        path = self.root / "a.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml",
                       "<w:document><w:body><w:p><w:r><w:t>Plain prose, no numbers.</w:t>"
                       "</w:r></w:p></w:body></w:document>")
            z.writestr("word/comments.xml",
                       "<w:comments><w:p><w:r><w:t>Reviewer: the 45 percent figure here "
                       "needs a source before publication.</w:t></w:r></w:p></w:comments>")
        report = audit(path, CitationResolver(online=False))
        self.assertFalse(any("figure appears" in f.message for f in report.heuristics))

    def test_figures_in_footnotes_are_still_flagged(self):
        path = self.root / "a.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml",
                       "<w:document><w:body><w:p><w:r><w:t>Body.</w:t>"
                       "</w:r></w:p></w:body></w:document>")
            z.writestr("word/footnotes.xml",
                       "<w:footnotes><w:p><w:r><w:t>Emissions fall by 45 percent across "
                       "the whole supply chain in every scenario.</w:t></w:r></w:p></w:footnotes>")
        report = audit(path, CitationResolver(online=False))
        self.assertTrue(any("figure appears" in f.message for f in report.heuristics))

    def test_a_figure_near_a_citation_is_not_flagged(self):
        body = ("Emissions fall by 45 percent under this boundary.\n"
                "Source: Smith (2020), 10.1000/abc\n")
        report = self.audit(body)
        self.assertFalse(any("figure appears" in f.message for f in report.heuristics))

    def test_a_document_with_no_references_warns_rather_than_reporting_clean(self):
        report = self.audit("Prose with no citations whatsoever in it.")
        self.assertTrue(any("no DOIs or URLs" in f.message for f in report.warnings))

    def test_unrecognised_domains_are_reported_as_untiered(self):
        report = self.audit("See https://acme-materials.com/impact")
        self.assertTrue(any("does not recognise" in f.message for f in report.findings))
        self.assertEqual(report.tier_counts().get("unclassified"), 1)

    def test_facts_and_heuristics_are_kept_separable(self):
        body = ("Smith (2020). A study of things. 10.1000/fake\n\n\n\n\n"
                "Elsewhere, emissions fall by 45 percent across the supply chain "
                "under every scenario tested.\n")
        report = self.audit(body, {"10.1000/fake": ("", "404")})
        self.assertTrue(report.facts)
        self.assertTrue(report.heuristics)
        self.assertTrue(all(f.kind == "fact" for f in report.facts))

    def test_findings_are_ordered_errors_first_then_facts_before_heuristics(self):
        body = ("Smith (2020). A study of things. 10.1000/fake\n\n\n\n\n"
                "Emissions fall by 45 percent across the whole supply chain here.\n")
        report = self.audit(body, {"10.1000/fake": ("", "404")})
        self.assertEqual(report.findings[0].severity, "error")

    def test_a_best_effort_extraction_warns_that_clean_is_not_conclusive(self):
        path = self.root / "a.pdf"
        path.write_bytes(b"%PDF-1.4\nnothing useful here\n%%EOF")
        try:
            import pypdf  # noqa: F401
            self.skipTest("pypdf is installed, so the fallback path is not exercised")
        except ImportError:
            pass
        report = audit(path, CitationResolver(online=False))
        self.assertTrue(any("best-effort" in f.message for f in report.warnings))

    def test_the_report_is_json_serializable(self):
        report = self.audit("See 10.1000/x")
        json.dumps(report.to_dict())

    def test_the_summary_records_extraction_confidence(self):
        self.assertEqual(self.audit("See 10.1000/x").summary()["extraction"], "full")


class TestAuditCommand(ExtractTestCase):
    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_a_document_with_checkable_citations_exits_zero_offline(self):
        path = self.write("doc.md", "See 10.1000/abc and https://example.org/x")
        code, out, _ = self.run_cli("audit", str(path), "--no-cache")
        self.assertEqual(code, 0)
        self.assertIn("CLEAN", out)

    def test_a_malformed_reference_exits_one(self):
        path = self.write("doc.md", "See https://doi.org/10.x/broken")
        code, out, _ = self.run_cli("audit", str(path), "--no-cache")
        self.assertEqual(code, 1)
        self.assertIn("PROBLEMS", out)

    def test_an_offline_run_says_the_references_were_not_resolved(self):
        path = self.write("doc.md", "See 10.1000/abc")
        _, out, _ = self.run_cli("audit", str(path), "--no-cache")
        self.assertIn("offline run", out)

    def test_facts_only_hides_heuristic_flags(self):
        body = "Emissions fall by 45 percent across the entire supply chain, every year.\n"
        path = self.write("doc.md", body)
        _, full, _ = self.run_cli("audit", str(path), "--no-cache")
        _, facts, _ = self.run_cli("audit", str(path), "--no-cache", "--facts-only")
        self.assertIn("figure appears", full)
        self.assertNotIn("figure appears", facts)

    def test_json_output_is_machine_readable(self):
        path = self.write("doc.md", "See 10.1000/abc")
        code, out, _ = self.run_cli("audit", str(path), "--no-cache", "--json")
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(payload[0]["summary"]["dois"], 1)

    def test_an_unreadable_document_is_reported_not_traced(self):
        path = self.write("doc.rtf", "x")
        code, _, err = self.run_cli("audit", str(path), "--no-cache")
        self.assertEqual(code, 2)
        self.assertIn(".docx", err)

    def test_several_documents_can_be_audited_at_once(self):
        a = self.write("a.md", "See 10.1000/abc")
        b = self.write("b.md", "See 10.1000/def")
        _, out, _ = self.run_cli("audit", str(a), str(b), "--no-cache")
        self.assertIn("a.md", out)
        self.assertIn("b.md", out)


if __name__ == "__main__":
    unittest.main()
