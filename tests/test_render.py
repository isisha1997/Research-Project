import unittest

from helpers import FakeResolver, claim, crossref_body, guide, source

from mii_guide.models import Audience, SourceTier
from mii_guide.render import BRAND, TIER_COLOR, Numbering, render_html, render_markdown
from mii_guide.verify import verify


class RenderTestCase(unittest.TestCase):
    def rendered(self, g=None, **kwargs):
        report = verify(g or guide())
        return render_markdown(report, **kwargs), render_html(report)


class TestNumbering(unittest.TestCase):
    def test_numbers_follow_order_of_first_citation(self):
        g = guide(
            sources=[source("a"), source("b"), source("c")],
            claims=[claim("c1", sources=["b"]), claim("c2", sources=["c", "b"])],
        )
        numbering = Numbering(g)
        self.assertEqual(numbering.of("b"), 1)
        self.assertEqual(numbering.of("c"), 2)

    def test_uncited_sources_get_no_number_and_stay_out_of_the_bibliography(self):
        g = guide(sources=[source("s1"), source("orphan")], claims=[claim("c1", sources=["s1"])])
        numbering = Numbering(g)
        self.assertIsNone(numbering.of("orphan"))
        self.assertEqual([s.id for _, s in numbering.ordered(g)], ["s1"])

    def test_a_source_cited_twice_keeps_one_number(self):
        g = guide(claims=[claim("c1", sources=["s1"]), claim("c2", sources=["s1"])])
        self.assertEqual(len(Numbering(g).ordered(g)), 1)


class TestMarkdown(RenderTestCase):
    def test_every_claim_carries_a_visible_citation_marker(self):
        g = guide(sources=[source("s1"), source("s2")],
                  claims=[claim("c1", sources=["s1", "s2"])])
        md, _ = self.rendered(g)
        self.assertIn("[1][2]", md)

    def test_all_three_reader_layers_are_rendered_by_default(self):
        md, _ = self.rendered()
        for audience in Audience:
            self.assertIn(f"## {audience.value.title()} layer", md)

    def test_a_single_audience_can_be_rendered_alone(self):
        md, _ = self.rendered(audience=Audience.PUBLIC)
        self.assertIn("## Public layer", md)
        self.assertNotIn("## Technical layer", md)

    def test_the_public_layer_uses_plain_language(self):
        g = guide(claims=[claim("c1", statement="Anisotropic tensile behaviour.",
                                plain="It stretches unevenly.")])
        md, _ = self.rendered(g, audience=Audience.PUBLIC)
        self.assertIn("It stretches unevenly.", md)
        self.assertNotIn("Anisotropic", md)

    def test_the_public_layer_hides_evidence_metadata(self):
        md, _ = self.rendered(audience=Audience.PUBLIC)
        self.assertNotIn("scope:", md)

    def test_the_technical_layer_shows_tier_and_scope(self):
        md, _ = self.rendered(audience=Audience.TECHNICAL)
        self.assertIn("evidence: peer-reviewed", md)
        self.assertIn("scope: Cradle-to-gate", md)

    def test_a_claim_excluded_from_a_layer_does_not_appear_in_it(self):
        g = guide(claims=[claim("secret", audiences=["technical"],
                                statement="Only for specialists.")])
        md, _ = self.rendered(g, audience=Audience.PUBLIC)
        self.assertNotIn("Only for specialists.", md)

    def test_contested_topics_get_their_own_section_with_both_sides(self):
        g = guide(
            sources=[source("s1"), source("s2")],
            claims=[claim("pro", topic="is it circular", stance="supports", sources=["s1"]),
                    claim("con", topic="is it circular", stance="refutes", sources=["s2"])],
        )
        md, _ = self.rendered(g)
        self.assertIn("## Where the evidence disagrees", md)
        self.assertIn("Evidence for", md)
        self.assertIn("Evidence against", md)

    def test_uncontested_guides_omit_the_disagreement_section(self):
        md, _ = self.rendered()
        self.assertNotIn("Where the evidence disagrees", md)

    def test_the_bibliography_labels_every_source_with_its_tier(self):
        g = guide(sources=[source("s1", tier="company"), source("s2", tier="peer_reviewed")],
                  claims=[claim("c1", sources=["s1", "s2"])])
        md, _ = self.rendered(g)
        self.assertIn("[Company claim]", md)
        self.assertIn("[Peer-reviewed]", md)

    def test_the_bibliography_is_ordered_by_first_citation_not_by_tier(self):
        # The heading text must describe the order actually used, or the two disagree.
        g = guide(
            sources=[source("weak", tier="company"), source("strong", tier="peer_reviewed")],
            claims=[claim("c1", sources=["weak"]), claim("c2", sources=["strong", "weak"])],
        )
        md, html = self.rendered(g)
        self.assertLess(md.index("Title for weak"), md.index("Title for strong"))
        self.assertIn("order of first citation", md)
        self.assertIn("order of first citation", html)
        self.assertNotIn("strongest first", md)

    def test_an_offline_build_is_labelled_provisional_not_verified(self):
        md, html = self.rendered()
        self.assertIn("PROVISIONAL", md)
        self.assertIn("Provisional", html)

    def test_an_online_build_is_labelled_verified(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("Title for s1", 2020), None)})
        report = verify(guide(), resolver)
        self.assertIn("VERIFIED", render_markdown(report))
        self.assertIn("✓ resolved", render_markdown(report))

    def test_a_blocked_guide_says_so_at_the_top(self):
        report = verify(guide(claims=[claim("c1", sources=[])]))
        self.assertIn("BLOCKED", render_markdown(report))

    def test_warnings_are_carried_into_the_published_method_note(self):
        g = guide(sources=[source("s1", tier="trade_press")])
        md, html = self.rendered(g)
        self.assertIn("Open caveats carried into publication", md)
        self.assertIn("trade press", md)
        self.assertIn("Open caveats", html)

    def test_the_method_note_explains_all_four_gates(self):
        md, _ = self.rendered()
        for gate in ("Coverage", "Citations", "Tiering", "Consensus"):
            self.assertIn(f"**{gate}**", md)

    def test_output_ends_with_exactly_one_newline(self):
        md, _ = self.rendered()
        self.assertTrue(md.endswith("\n"))
        self.assertFalse(md.endswith("\n\n"))


class TestHtml(RenderTestCase):
    def test_output_is_a_complete_document(self):
        _, html = self.rendered()
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("</html>", html)
        self.assertIn("<meta name=\"viewport\"", html)

    def test_claim_text_is_escaped(self):
        g = guide(claims=[claim("c1", statement="Cotton <script>alert(1)</script> & flax")])
        _, html = self.rendered(g)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("&amp; flax", html)

    def test_source_titles_are_escaped(self):
        g = guide(sources=[source("s1", title="A <b>bold</b> claim")])
        _, html = self.rendered(g)
        self.assertNotIn("<b>bold</b>", html)

    def test_citations_link_to_their_bibliography_entry(self):
        _, html = self.rendered()
        self.assertIn("href=\"#src-1\"", html)
        self.assertIn("id=\"src-1\"", html)

    def test_the_brand_palette_is_used(self):
        _, html = self.rendered()
        for colour in BRAND.values():
            self.assertIn(colour, html)

    def test_every_tier_has_a_distinct_brand_colour(self):
        colours = list(TIER_COLOR.values())
        self.assertEqual(len(colours), len(set(colours)))
        self.assertEqual(set(TIER_COLOR), set(SourceTier))

    def test_the_page_supports_both_colour_schemes(self):
        _, html = self.rendered()
        self.assertIn("prefers-color-scheme: dark", html)
        self.assertIn("color-scheme: light dark", html)


if __name__ == "__main__":
    unittest.main()
