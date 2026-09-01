import unittest

from helpers import claim, guide, source

from mii_guide.models import (
    Audience, Claim, Guide, Source, SourceTier, Stance, is_doi, normalize_doi, squash,
)


class TestSourceTier(unittest.TestCase):
    def test_ranks_strongest_first(self):
        self.assertLess(SourceTier.PEER_REVIEWED.rank, SourceTier.COMPANY.rank)

    def test_only_top_three_tiers_are_primary_evidence(self):
        self.assertTrue(SourceTier.PEER_REVIEWED.is_primary_evidence)
        self.assertTrue(SourceTier.INSTITUTIONAL.is_primary_evidence)
        self.assertFalse(SourceTier.INDUSTRY_LCA.is_primary_evidence)
        self.assertFalse(SourceTier.COMPANY.is_primary_evidence)

    def test_parses_aliases_and_spacing(self):
        self.assertIs(SourceTier.parse("peer-reviewed"), SourceTier.PEER_REVIEWED)
        self.assertIs(SourceTier.parse("MARKETING"), SourceTier.COMPANY)
        self.assertIs(SourceTier.parse("Industry LCA"), SourceTier.INDUSTRY_LCA)
        self.assertIs(SourceTier.parse(SourceTier.REGULATOR), SourceTier.REGULATOR)

    def test_rejects_unknown_tier_with_a_useful_message(self):
        with self.assertRaises(ValueError) as ctx:
            SourceTier.parse("vibes")
        self.assertIn("peer_reviewed", str(ctx.exception))

    def test_tier_is_mandatory(self):
        with self.assertRaises(ValueError):
            SourceTier.parse(None)


class TestDoi(unittest.TestCase):
    def test_strips_every_common_prefix(self):
        for raw in ("10.1000/abc", "https://doi.org/10.1000/abc", "doi:10.1000/abc",
                    "http://dx.doi.org/10.1000/abc", "DOI:10.1000/abc"):
            self.assertEqual(normalize_doi(raw), "10.1000/abc", raw)

    def test_recognizes_wellformed_dois_only(self):
        self.assertTrue(is_doi("10.1016/j.envpol.2017.10.057"))
        self.assertFalse(is_doi("not-a-doi"))
        self.assertFalse(is_doi("11.1000/abc"))


class TestSource(unittest.TestCase):
    def test_prefers_doi_over_url_as_locator(self):
        s = Source.from_dict(source("s1", doi="10.1000/x", url="https://example.org"))
        self.assertEqual(s.locator, "https://doi.org/10.1000/x")

    def test_falls_back_to_url_when_no_doi(self):
        s = Source.from_dict(source("s1", doi=None, url="https://example.org"))
        self.assertEqual(s.locator, "https://example.org")

    def test_citation_abbreviates_long_author_lists(self):
        s = Source.from_dict(source("s1", authors=["A", "B", "C", "D"]))
        self.assertIn("A et al.", s.citation())

    def test_an_et_al_author_does_not_produce_a_double_period(self):
        s = Source.from_dict(source("s1", authors=["Glombikova, V.", "B", "C", "D"]))
        self.assertIn("Glombikova, V. et al. (", s.citation())
        self.assertNotIn("..", s.citation())

    def test_citation_handles_missing_year(self):
        s = Source.from_dict(source("s1", year=None))
        self.assertIn("(n.d.)", s.citation())

    def test_rejects_unknown_fields_rather_than_ignoring_them(self):
        with self.assertRaises(ValueError) as ctx:
            Source.from_dict({"id": "s1", "tier": "company", "title": "T", "tiers": "typo"})
        self.assertIn("tiers", str(ctx.exception))

    def test_requires_title(self):
        with self.assertRaises(ValueError):
            Source.from_dict({"id": "s1", "tier": "company", "title": "  "})


class TestClaim(unittest.TestCase):
    def test_public_layer_prefers_plain_language(self):
        c = Claim.from_dict(claim("c1", plain="Simple words."))
        self.assertEqual(c.text_for(Audience.PUBLIC), "Simple words.")
        self.assertEqual(c.text_for(Audience.TECHNICAL), "Statement for c1.")

    def test_public_layer_falls_back_to_the_technical_statement(self):
        c = Claim.from_dict(claim("c1"))
        self.assertEqual(c.text_for(Audience.PUBLIC), "Statement for c1.")

    def test_defaults_to_every_audience(self):
        self.assertEqual(set(Claim.from_dict(claim("c1")).audiences), set(Audience))

    def test_stance_defaults_to_neutral(self):
        self.assertIs(Claim.from_dict(claim("c1")).stance, Stance.NEUTRAL)

    def test_topic_is_normalized_for_grouping(self):
        c = Claim.from_dict(claim("c1", topic="  Is It Circular?  "))
        self.assertEqual(c.topic, "is it circular?")

    def test_blank_source_ids_are_dropped(self):
        self.assertEqual(Claim.from_dict(claim("c1", sources=["s1", "  ", ""])).sources, ["s1"])


class TestSquash(unittest.TestCase):
    def test_collapses_yaml_block_scalar_whitespace(self):
        self.assertEqual(squash("a\n  b\n\n  c\n"), "a b c")

    def test_empty_text_becomes_none(self):
        self.assertIsNone(squash("   \n  "))
        self.assertIsNone(squash(None))


class TestGuide(unittest.TestCase):
    def test_rejects_duplicate_ids(self):
        with self.assertRaises(ValueError):
            guide(sources=[source("s1"), source("s1")])
        with self.assertRaises(ValueError):
            guide(claims=[claim("c1"), claim("c1")])

    def test_requires_slug_title_and_material(self):
        with self.assertRaises(ValueError) as ctx:
            Guide.from_dict({"slug": "s"})
        self.assertIn("title", str(ctx.exception))

    def test_sources_for_a_claim_come_back_strongest_first(self):
        g = guide(
            sources=[source("weak", tier="company"), source("strong", tier="peer_reviewed")],
            claims=[claim("c1", sources=["weak", "strong"])],
        )
        self.assertEqual([s.id for s in g.sources_for(g.claims[0])], ["strong", "weak"])
        self.assertIs(g.strongest_tier(g.claims[0]), SourceTier.PEER_REVIEWED)

    def test_missing_source_references_are_skipped_not_crashed(self):
        g = guide(claims=[claim("c1", sources=["s1", "ghost"])])
        self.assertEqual([s.id for s in g.sources_for(g.claims[0])], ["s1"])

    def test_declared_section_order_wins_then_first_seen_order(self):
        g = guide(
            claims=[claim("c1", section="Later"), claim("c2", section="Extra"),
                    claim("c3", section="First")],
            section_order=["First", "Later"],
        )
        self.assertEqual(g.sections(), ["First", "Later", "Extra"])

    def test_sections_ignores_declared_names_with_no_claims(self):
        g = guide(claims=[claim("c1", section="Only")], section_order=["Ghost", "Only"])
        self.assertEqual(g.sections(), ["Only"])

    def test_claims_in_filters_by_audience(self):
        g = guide(claims=[
            claim("c1", section="S", audiences=["technical"]),
            claim("c2", section="S", audiences=["public", "technical"]),
        ])
        self.assertEqual([c.id for c in g.claims_in("S", Audience.PUBLIC)], ["c2"])
        self.assertEqual(len(g.claims_in("S", Audience.TECHNICAL)), 2)

    def test_topics_groups_only_claims_that_declare_one(self):
        g = guide(claims=[claim("c1", topic="t"), claim("c2", topic="t"), claim("c3")])
        self.assertEqual(list(g.topics()), ["t"])
        self.assertEqual(len(g.topics()["t"]), 2)


if __name__ == "__main__":
    unittest.main()
