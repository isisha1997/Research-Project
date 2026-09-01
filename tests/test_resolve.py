import json
import tempfile
import unittest
from pathlib import Path

from helpers import FakeResolver, crossref_body, source

from mii_guide.models import Source
from mii_guide.resolve import CitationResolver, title_similarity


class TestTitleSimilarity(unittest.TestCase):
    def test_ignores_case_punctuation_and_spacing(self):
        self.assertEqual(
            title_similarity("Life-Cycle Assessment: Of Leather",
                             "life cycle assessment of leather"),
            1.0,
        )

    def test_separates_different_papers(self):
        self.assertLess(
            title_similarity("Microfibre release from washing machines",
                             "Carbon accounting in cement production"),
            0.5,
        )


class TestOfflineResolution(unittest.TestCase):
    def resolve(self, **overrides):
        return CitationResolver(online=False).resolve(Source.from_dict(source("s1", **overrides)))

    def test_structurally_valid_sources_are_marked_unchecked_not_passed(self):
        result = self.resolve()
        self.assertEqual(result.status, "unchecked")
        self.assertIn("--online", result.detail)

    def test_a_malformed_doi_is_caught_without_a_network_call(self):
        self.assertEqual(self.resolve(doi="10.x/bad").status, "malformed")

    def test_a_source_with_no_locator_is_malformed(self):
        self.assertEqual(self.resolve(doi=None, url=None).status, "malformed")

    def test_a_non_http_url_is_malformed(self):
        self.assertEqual(self.resolve(doi=None, url="mailto:a@b.c").status, "malformed")

    def test_an_unchecked_resolution_is_not_a_metadata_conflict(self):
        self.assertFalse(self.resolve().metadata_conflict)


class TestCache(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.cache = Path(self.dir.name) / "cache.json"
        self.addCleanup(self.dir.cleanup)

    def resolver(self, responses, **kwargs):
        r = FakeResolver(responses)
        r.cache_path = self.cache
        r._cache = r._load_cache()
        for key, value in kwargs.items():
            setattr(r, key, value)
        return r

    def test_a_second_run_reuses_the_cached_result(self):
        body = crossref_body("Title for s1", 2020)
        first = self.resolver({"10.1000/s1": (body, None)})
        first.resolve_all([Source.from_dict(source("s1"))])
        self.assertEqual(first.stats.network_calls, 1)

        second = self.resolver({"10.1000/s1": (body, None)})
        result = second.resolve(Source.from_dict(source("s1")))
        self.assertEqual(second.stats.network_calls, 0)
        self.assertEqual(second.stats.from_cache, 1)
        self.assertEqual(result.status, "resolved")

    def test_a_cached_record_still_rechecks_our_metadata_against_it(self):
        body = crossref_body("Title for s1", 2020)
        self.resolver({"10.1000/s1": (body, None)}).resolve_all([Source.from_dict(source("s1"))])

        # The cached registry record is unchanged, but our stored title now differs.
        second = self.resolver({})
        result = second.resolve(Source.from_dict(source("s1", title="A Different Paper")))
        self.assertEqual(second.stats.network_calls, 0)
        self.assertTrue(result.metadata_conflict)

    def test_an_expired_entry_is_refetched(self):
        body = crossref_body("Title for s1", 2020)
        first = self.resolver({"10.1000/s1": (body, None)})
        first.resolve_all([Source.from_dict(source("s1"))])

        second = self.resolver({"10.1000/s1": (body, None)}, ttl=0)
        second.resolve(Source.from_dict(source("s1")))
        self.assertEqual(second.stats.network_calls, 1)

    def test_a_corrupt_cache_is_treated_as_empty_rather_than_crashing(self):
        self.cache.write_text("{not json", encoding="utf-8")
        resolver = self.resolver({"10.1000/s1": (crossref_body("Title for s1", 2020), None)})
        self.assertEqual(resolver._cache, {})
        self.assertEqual(resolver.resolve(Source.from_dict(source("s1"))).status, "resolved")

    def test_failures_are_cached_too_so_reruns_stay_reproducible(self):
        first = self.resolver({"10.1000/s1": ("", "404")})
        first.resolve_all([Source.from_dict(source("s1"))])
        stored = json.loads(self.cache.read_text())
        self.assertFalse(stored["10.1000/s1"]["ok"])
        self.assertEqual(stored["10.1000/s1"]["status"], "not_found")

    def test_no_cache_path_means_nothing_is_written(self):
        resolver = FakeResolver({"10.1000/s1": (crossref_body("Title for s1", 2020), None)})
        resolver.resolve_all([Source.from_dict(source("s1"))])
        self.assertFalse(self.cache.exists())


class TestUrlProbe(unittest.TestCase):
    def test_a_head_rejection_falls_back_to_a_get_before_failing(self):
        class HeadRejecting(FakeResolver):
            def _get(self, url, head=False):
                if head:
                    return "", "405"
                return "", None

        resolver = HeadRejecting({})
        result = resolver.resolve(Source.from_dict(source("s1", doi=None, url="https://a.org/x")))
        self.assertEqual(result.status, "resolved")


if __name__ == "__main__":
    unittest.main()
