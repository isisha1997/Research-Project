import unittest

from helpers import FakeResolver, claim, crossref_body, guide, source

from mii_guide.resolve import CitationResolver
from mii_guide.verify import Gate, Severity, verify


class GateTestCase(unittest.TestCase):
    def findings(self, g, gate=None, severity=None, resolver=None):
        report = verify(g, resolver or CitationResolver(online=False))
        return [
            f for f in report.findings
            if (gate is None or f.gate is gate) and (severity is None or f.severity is severity)
        ]

    def assertBlocks(self, g, gate, subject=None, resolver=None):
        errors = self.findings(g, gate, Severity.ERROR, resolver)
        self.assertTrue(errors, f"expected a blocking {gate.value} finding, got none")
        if subject is not None:
            self.assertIn(subject, [f.subject for f in errors])
        return errors


class TestCoverageGate(GateTestCase):
    def test_a_claim_with_no_sources_blocks_publication(self):
        g = guide(claims=[claim("c1", sources=[])])
        self.assertBlocks(g, Gate.COVERAGE, "c1")
        self.assertFalse(verify(g).publishable)

    def test_a_claim_citing_an_undefined_source_blocks_publication(self):
        g = guide(claims=[claim("c1", sources=["ghost"])])
        errors = self.assertBlocks(g, Gate.COVERAGE, "c1")
        self.assertIn("ghost", errors[0].message)

    def test_a_guide_with_no_claims_blocks_publication(self):
        self.assertBlocks(guide(claims=[]), Gate.COVERAGE)

    def test_an_uncited_source_is_flagged_but_does_not_block(self):
        g = guide(sources=[source("s1"), source("orphan")], claims=[claim("c1", sources=["s1"])])
        report = verify(g)
        self.assertTrue(report.publishable)
        self.assertIn("orphan", [f.subject for f in report.infos])

    def test_a_missing_scope_qualifier_is_flagged_but_does_not_block(self):
        g = guide(claims=[claim("c1", scope=None)])
        report = verify(g)
        self.assertTrue(report.publishable)
        self.assertTrue(any(f.subject == "c1" and "scope" in f.message for f in report.infos))

    def test_coverage_ratio_counts_claims_with_resolvable_sources(self):
        g = guide(claims=[claim("c1", sources=["s1"]), claim("c2", sources=[])])
        self.assertAlmostEqual(verify(g).coverage(), 0.5)

    def test_every_finding_that_blocks_carries_a_hint(self):
        g = guide(claims=[claim("c1", sources=[])])
        for finding in verify(g).errors:
            self.assertTrue(finding.hint, f"{finding} has no hint for the author")


class TestCitationGate(GateTestCase):
    def test_a_malformed_doi_blocks_publication(self):
        g = guide(sources=[source("s1", doi="nonsense")])
        self.assertBlocks(g, Gate.CITATIONS, "s1")

    def test_a_source_with_no_locator_blocks_publication(self):
        g = guide(sources=[source("s1", doi=None, url=None)])
        errors = self.assertBlocks(g, Gate.CITATIONS, "s1")
        self.assertIn("neither a DOI, a URL, nor a standards designation", errors[0].message)

    def test_a_malformed_url_blocks_publication(self):
        g = guide(sources=[source("s1", doi=None, url="ftp://example.org/x")])
        self.assertBlocks(g, Gate.CITATIONS, "s1")

    def test_an_offline_run_reports_citations_as_unchecked(self):
        report = verify(guide())
        self.assertTrue(report.publishable)
        self.assertTrue(any("offline" in f.message for f in report.infos))
        self.assertEqual(report.resolutions["s1"].status, "unchecked")

    def test_a_doi_crossref_has_never_heard_of_blocks_publication(self):
        resolver = FakeResolver({"10.1000/s1": ("", "404")})
        errors = self.assertBlocks(guide(), Gate.CITATIONS, "s1", resolver=resolver)
        self.assertIn("fabricated", errors[0].message)

    def test_a_doi_resolving_to_a_different_title_blocks_publication(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("A Totally Different Paper", 2020), None)})
        errors = self.assertBlocks(guide(), Gate.CITATIONS, "s1", resolver=resolver)
        self.assertIn("different work", errors[0].message)

    def test_a_wrong_year_blocks_publication(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("Title for s1", 2005), None)})
        errors = self.assertBlocks(guide(), Gate.CITATIONS, "s1", resolver=resolver)
        self.assertIn("2005", errors[0].message)

    def test_a_one_year_drift_is_tolerated_as_print_versus_online(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("Title for s1", 2021), None)})
        report = verify(guide(), resolver)
        self.assertTrue(report.publishable)

    def test_a_matching_record_passes_cleanly(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("Title for s1", 2020), None)})
        report = verify(guide(), resolver)
        self.assertTrue(report.publishable)
        self.assertEqual(report.resolutions["s1"].status, "resolved")
        self.assertFalse(report.resolutions["s1"].metadata_conflict)

    def test_an_unreachable_registry_warns_rather_than_passing_silently(self):
        resolver = FakeResolver({"10.1000/s1": ("", "Connection refused")})
        report = verify(guide(), resolver)
        self.assertTrue(report.publishable)
        self.assertTrue(report.warnings)
        self.assertEqual(report.resolutions["s1"].status, "unreachable")

    def test_uncited_sources_are_not_sent_over_the_network(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("Title for s1", 2020), None)})
        g = guide(sources=[source("s1"), source("orphan")], claims=[claim("c1", sources=["s1"])])
        verify(g, resolver)
        self.assertFalse(any("orphan" in url for url in resolver.calls))

    def test_a_live_url_passes_without_metadata_checking(self):
        resolver = FakeResolver({"example.org": ("", None)})
        g = guide(sources=[source("s1", doi=None, url="https://example.org/report")])
        report = verify(g, resolver)
        self.assertTrue(report.publishable)
        self.assertEqual(report.resolutions["s1"].status, "resolved")

    def test_a_dead_url_blocks_publication(self):
        resolver = FakeResolver({"example.org": ("", "404")})
        g = guide(sources=[source("s1", doi=None, url="https://example.org/gone")])
        self.assertBlocks(g, Gate.CITATIONS, "s1", resolver=resolver)


class TestRegisteredSources(GateTestCase):
    """Paywalled standards: identified by number, resolvable by no machine."""

    def registered(self, **overrides):
        data = {"id": "s1", "tier": "regulator", "title": "Standard test method",
                "designation": "ASTM D6571-22", "held": "MII register, 2026-03"}
        data.update(overrides)
        return guide(sources=[data])

    def test_a_designation_is_not_treated_as_a_locator(self):
        g = self.registered()
        self.assertIsNone(g.sources["s1"].locator)
        self.assertTrue(g.sources["s1"].is_registered)

    def test_a_held_standard_publishes_without_being_machine_checkable(self):
        report = verify(self.registered())
        self.assertTrue(report.publishable)
        self.assertEqual(report.resolutions["s1"].status, "registered")

    def test_a_standard_with_no_custody_trail_blocks_publication(self):
        errors = self.assertBlocks(self.registered(held=None), Gate.CITATIONS, "s1")
        self.assertIn("where the controlled copy is held", errors[0].message)

    def test_a_registered_source_is_never_sent_over_the_network(self):
        resolver = FakeResolver({})
        verify(self.registered(), resolver)
        self.assertEqual(resolver.calls, [])

    def test_a_designation_alongside_a_doi_is_not_registered(self):
        g = self.registered(doi="10.1000/abc")
        self.assertFalse(g.sources["s1"].is_registered)

    def test_registered_sources_are_not_asked_for_an_accessed_date(self):
        report = verify(self.registered(accessed=None))
        self.assertFalse(any("accessed" in f.message for f in report.infos))

    def test_the_summary_counts_registered_sources(self):
        self.assertEqual(verify(self.registered()).summary()["registered_sources"], 1)


class TestWithheldClaims(GateTestCase):
    """The guide's own rule: print no figure until it is confirmed."""

    def test_a_withheld_claim_publishes_and_is_counted(self):
        g = guide(claims=[claim("c1", status="withheld")])
        report = verify(g)
        self.assertTrue(report.publishable)
        self.assertEqual(report.summary()["withheld_claims"], 1)
        self.assertTrue(any("figure withheld" in f.message for f in report.infos))

    def test_an_unknown_status_is_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            guide(claims=[claim("c1", status="maybe")])
        self.assertIn("withheld", str(ctx.exception))

    def test_claims_default_to_published(self):
        self.assertEqual(verify(guide()).summary()["withheld_claims"], 0)


class TestTieringGate(GateTestCase):
    def test_a_claim_resting_only_on_marketing_blocks_publication(self):
        g = guide(sources=[source("s1", tier="company")])
        errors = self.assertBlocks(g, Gate.TIERING, "c1")
        self.assertIn("company self-published", errors[0].message)

    def test_marketing_is_acceptable_alongside_independent_evidence(self):
        g = guide(
            sources=[source("marketing", tier="company"), source("study", tier="peer_reviewed")],
            claims=[claim("c1", sources=["marketing", "study"])],
        )
        self.assertTrue(verify(g).publishable)

    def test_trade_press_alone_warns_but_publishes(self):
        g = guide(sources=[source("s1", tier="trade_press")])
        report = verify(g)
        self.assertTrue(report.publishable)
        self.assertTrue(any(f.gate is Gate.TIERING and f.subject == "c1"
                            for f in report.warnings))

    def test_industry_lca_alone_warns_that_it_is_not_independent(self):
        g = guide(sources=[source("s1", tier="industry_lca")])
        warnings = self.findings(g, Gate.TIERING, Severity.WARN)
        self.assertTrue(any("primary evidence" in f.message for f in warnings))

    def test_a_number_without_primary_evidence_warns(self):
        g = guide(
            sources=[source("s1", tier="industry_lca")],
            claims=[claim("c1", statement="Emissions fall by 42 percent.")],
        )
        warnings = self.findings(g, Gate.TIERING, Severity.WARN)
        self.assertTrue(any("carries a number" in f.message for f in warnings))

    def test_a_number_backed_by_primary_evidence_does_not_warn(self):
        g = guide(claims=[claim("c1", statement="Emissions fall by 42 percent.")])
        warnings = self.findings(g, Gate.TIERING, Severity.WARN)
        self.assertFalse(any("carries a number" in f.message for f in warnings))

    def test_institutional_evidence_passes_the_tiering_gate(self):
        g = guide(sources=[source("s1", tier="institutional")])
        self.assertFalse(self.findings(g, Gate.TIERING, Severity.WARN))


class TestConsensusGate(GateTestCase):
    def contested(self, **overrides):
        pro = dict(topic="is it circular", stance="supports", sources=["s1"])
        con = dict(topic="is it circular", stance="refutes", sources=["s2"])
        pro.update(overrides.get("pro", {}))
        con.update(overrides.get("con", {}))
        return guide(
            sources=[source("s1"), source("s2")],
            claims=[claim("pro", **pro), claim("con", **con)],
        )

    def test_opposing_stances_are_recorded_as_a_live_contradiction(self):
        report = verify(self.contested())
        live = [c for c in report.contradictions if c.is_live]
        self.assertEqual(len(live), 1)
        self.assertEqual(live[0].topic, "is it circular")
        self.assertEqual([c.id for c in live[0].supporting], ["pro"])
        self.assertEqual([c.id for c in live[0].refuting], ["con"])

    def test_a_live_contradiction_does_not_block_publication(self):
        self.assertTrue(verify(self.contested()).publishable)

    def test_agreement_on_a_topic_is_not_a_contradiction(self):
        g = guide(
            sources=[source("s1"), source("s2")],
            claims=[claim("a", topic="t", stance="supports", sources=["s1"]),
                    claim("b", topic="t", stance="supports", sources=["s2"])],
        )
        self.assertFalse([c for c in verify(g).contradictions if c.is_live])

    def test_a_mixed_claim_alongside_a_stance_counts_as_contested(self):
        g = guide(
            sources=[source("s1"), source("s2")],
            claims=[claim("a", topic="t", stance="supports", sources=["s1"]),
                    claim("b", topic="t", stance="mixed", sources=["s2"])],
        )
        self.assertTrue([c for c in verify(g).contradictions if c.is_live])

    def test_showing_one_side_only_to_one_reader_layer_blocks_publication(self):
        g = self.contested(con={"audiences": ["technical"]})
        errors = self.assertBlocks(g, Gate.CONSENSUS, "is it circular")
        self.assertTrue(any("public layer" in f.message for f in errors))
        self.assertTrue(any("industry layer" in f.message for f in errors))

    def test_dropping_a_contested_topic_from_a_layer_entirely_is_allowed(self):
        g = self.contested(
            pro={"audiences": ["technical"]}, con={"audiences": ["technical"]},
        )
        self.assertTrue(verify(g).publishable)

    def test_a_topic_resting_on_one_source_warns(self):
        g = guide(claims=[claim("a", topic="t", sources=["s1"]),
                          claim("b", topic="t", sources=["s1"])])
        warnings = self.findings(g, Gate.CONSENSUS, Severity.WARN)
        self.assertTrue(any("single source" in f.message for f in warnings))

    def test_independent_corroboration_does_not_warn(self):
        g = guide(sources=[source("s1"), source("s2")],
                  claims=[claim("a", topic="t", sources=["s1"]),
                          claim("b", topic="t", sources=["s2"])])
        self.assertFalse(self.findings(g, Gate.CONSENSUS, Severity.WARN))


class TestReport(unittest.TestCase):
    def test_summary_is_json_serializable(self):
        import json
        report = verify(guide())
        json.dumps(report.to_dict())

    def test_findings_are_ordered_most_severe_first(self):
        g = guide(sources=[source("s1", tier="company"), source("orphan")],
                  claims=[claim("c1", sources=["s1"], scope=None)])
        severities = [f.severity.value for f in verify(g).findings]
        self.assertEqual(severities, sorted(severities, key=lambda s:
                                            {"error": 0, "warn": 1, "info": 2}[s]))

    def test_tier_distribution_is_ordered_strongest_first(self):
        g = guide(sources=[source("weak", tier="company"), source("strong", tier="peer_reviewed")],
                  claims=[claim("c1", sources=["weak", "strong"])])
        ranks = [t.rank for t in verify(g).tier_distribution()]
        self.assertEqual(ranks, sorted(ranks))

    def test_findings_can_be_looked_up_by_subject(self):
        g = guide(claims=[claim("c1", sources=[])])
        self.assertTrue(verify(g).findings_for("c1"))


if __name__ == "__main__":
    unittest.main()
