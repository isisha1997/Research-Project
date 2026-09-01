import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import helpers  # noqa: F401  (puts the package on sys.path)

from mii_guide.cli import main
from mii_guide.loader import GuideLoadError, discover, load_guide

REPO = Path(__file__).resolve().parent.parent

GOOD = """
slug: good
title: Good Guide
material: Test material
claims:
  - id: c1
    statement: A sourced statement.
    scope: Cradle-to-gate
    sources: [s1]
sources:
  - id: s1
    tier: peer_reviewed
    title: A Real Paper
    year: 2020
    doi: 10.1000/real
"""

BAD = """
slug: bad
title: Bad Guide
material: Test material
claims:
  - id: c1
    statement: An unsourced statement.
    sources: []
sources: []
"""


class CliTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)

    def write(self, name, body):
        path = self.root / name
        path.write_text(body, encoding="utf-8")
        return path

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(argv))
        return code, out.getvalue(), err.getvalue()


class TestVerifyCommand(CliTestCase):
    def test_a_clean_guide_exits_zero(self):
        path = self.write("good.yaml", GOOD)
        code, out, _ = self.run_cli("verify", str(path), "--no-cache")
        self.assertEqual(code, 0)
        self.assertIn("PASS", out)

    def test_a_guide_with_errors_exits_one(self):
        path = self.write("bad.yaml", BAD)
        code, out, _ = self.run_cli("verify", str(path), "--no-cache")
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("no sources", out)

    def test_strict_mode_fails_on_warnings_too(self):
        path = self.write("warn.yaml", GOOD.replace("peer_reviewed", "trade_press"))
        self.assertEqual(self.run_cli("verify", str(path), "--no-cache")[0], 0)
        self.assertEqual(self.run_cli("verify", str(path), "--no-cache", "--strict")[0], 1)

    def test_json_output_is_machine_readable(self):
        path = self.write("good.yaml", GOOD)
        code, out, _ = self.run_cli("verify", str(path), "--no-cache", "--json")
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(payload[0]["summary"]["guide"], "good")
        self.assertTrue(payload[0]["summary"]["publishable"])

    def test_a_directory_is_expanded_to_every_spec_inside(self):
        self.write("good.yaml", GOOD)
        self.write("bad.yaml", BAD)
        code, out, _ = self.run_cli("verify", str(self.root), "--no-cache")
        self.assertEqual(code, 1)
        self.assertIn("PASS", out)
        self.assertIn("FAIL", out)

    def test_a_missing_file_is_reported_rather_than_traced(self):
        code, _, err = self.run_cli("verify", str(self.root / "nope.yaml"), "--no-cache")
        self.assertEqual(code, 2)
        self.assertIn("no such file", err)

    def test_invalid_yaml_is_reported_with_the_filename(self):
        path = self.write("broken.yaml", "slug: [unclosed\n")
        code, _, err = self.run_cli("verify", str(path), "--no-cache")
        self.assertEqual(code, 2)
        self.assertIn("broken.yaml", err)

    def test_a_schema_violation_names_the_offending_field(self):
        path = self.write("wrong.yaml", GOOD.replace("tier: peer_reviewed", "tier: excellent"))
        code, _, err = self.run_cli("verify", str(path), "--no-cache")
        self.assertEqual(code, 2)
        self.assertIn("excellent", err)


class TestBuildCommand(CliTestCase):
    def test_a_clean_guide_renders_every_format(self):
        path = self.write("good.yaml", GOOD)
        out_dir = self.root / "dist"
        code, _, _ = self.run_cli("build", str(path), "--out", str(out_dir), "--no-cache")
        self.assertEqual(code, 0)
        for name in ("good.md", "good.html", "good.report.json"):
            self.assertTrue((out_dir / name).exists(), name)

    def test_a_blocked_guide_is_not_rendered(self):
        path = self.write("bad.yaml", BAD)
        out_dir = self.root / "dist"
        code, _, err = self.run_cli("build", str(path), "--out", str(out_dir), "--no-cache")
        self.assertEqual(code, 1)
        self.assertFalse((out_dir / "bad.md").exists())
        self.assertIn("not rendered", err)

    def test_allow_unverified_renders_a_blocked_guide_with_the_warning_intact(self):
        path = self.write("bad.yaml", BAD)
        out_dir = self.root / "dist"
        code, _, _ = self.run_cli("build", str(path), "--out", str(out_dir),
                                  "--no-cache", "--allow-unverified")
        self.assertEqual(code, 1)  # still a failure, but the draft is on disk to work from
        self.assertIn("BLOCKED", (out_dir / "bad.md").read_text())

    def test_formats_can_be_selected(self):
        path = self.write("good.yaml", GOOD)
        out_dir = self.root / "dist"
        self.run_cli("build", str(path), "--out", str(out_dir), "--no-cache", "--format", "md")
        self.assertTrue((out_dir / "good.md").exists())
        self.assertFalse((out_dir / "good.html").exists())

    def test_an_unknown_format_is_rejected(self):
        path = self.write("good.yaml", GOOD)
        code, _, err = self.run_cli("build", str(path), "--out", str(self.root / "d"),
                                    "--no-cache", "--format", "pdf")
        self.assertEqual(code, 2)
        self.assertIn("pdf", err)

    def test_a_single_audience_can_be_built(self):
        path = self.write("good.yaml", GOOD)
        out_dir = self.root / "dist"
        self.run_cli("build", str(path), "--out", str(out_dir), "--no-cache",
                     "--format", "md", "--audience", "public")
        body = (out_dir / "good.md").read_text()
        self.assertIn("Public layer", body)
        self.assertNotIn("Technical layer", body)


class TestNewCommand(CliTestCase):
    def test_the_scaffold_it_writes_is_itself_loadable(self):
        code, _, _ = self.run_cli("new", "bio-leather", "--dir", str(self.root))
        self.assertEqual(code, 0)
        path = self.root / "bio-leather.yaml"
        self.assertTrue(path.exists())
        guide = load_guide(path)
        self.assertEqual(guide.slug, "bio-leather")
        self.assertEqual(len(guide.claims), 1)

    def test_it_refuses_to_overwrite_an_existing_spec(self):
        self.run_cli("new", "bio-leather", "--dir", str(self.root))
        code, _, err = self.run_cli("new", "bio-leather", "--dir", str(self.root))
        self.assertEqual(code, 2)
        self.assertIn("already exists", err)

    def test_slugs_are_normalized(self):
        self.run_cli("new", "Bio Leather", "--dir", str(self.root))
        self.assertTrue((self.root / "bio-leather.yaml").exists())


class TestSourcesCommand(CliTestCase):
    def test_it_lists_sources_with_their_tier_and_use(self):
        path = self.write("good.yaml", GOOD)
        code, out, _ = self.run_cli("sources", str(path))
        self.assertEqual(code, 0)
        self.assertIn("Peer-reviewed", out)
        self.assertIn("cited", out)

    def test_it_can_isolate_what_rests_on_marketing(self):
        self.write("good.yaml", GOOD)
        self.write("promo.yaml", GOOD.replace("slug: good", "slug: promo")
                   .replace("peer_reviewed", "company"))
        code, out, _ = self.run_cli("sources", str(self.root), "--tier", "company")
        self.assertEqual(code, 0)
        self.assertIn("promo", out)
        self.assertNotIn("good", out)

    def test_uncited_sources_are_marked_unused(self):
        path = self.write("orphan.yaml", GOOD + """
  - id: s2
    tier: company
    title: Never cited
    url: https://example.org
""")
        _, out, _ = self.run_cli("sources", str(path))
        self.assertIn("unused", out)


class TestNoCommand(CliTestCase):
    def test_bare_invocation_prints_help_and_exits_two(self):
        code, out, _ = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn("usage", out.lower())


class TestLoader(CliTestCase):
    def test_json_specs_load_too(self):
        path = self.root / "g.json"
        path.write_text(json.dumps({
            "slug": "j", "title": "J", "material": "M",
            "sources": [{"id": "s1", "tier": "company", "title": "T", "url": "https://a.org"}],
            "claims": [{"id": "c1", "statement": "S", "sources": ["s1"]}],
        }), encoding="utf-8")
        self.assertEqual(load_guide(path).slug, "j")

    def test_invalid_json_is_reported_with_the_filename(self):
        path = self.root / "g.json"
        path.write_text("{nope", encoding="utf-8")
        with self.assertRaises(GuideLoadError) as ctx:
            load_guide(path)
        self.assertIn("g.json", str(ctx.exception))

    def test_discovery_finds_specs_recursively_and_ignores_other_files(self):
        (self.root / "nested").mkdir()
        self.write("b.yaml", GOOD)
        (self.root / "nested" / "a.yml").write_text(GOOD, encoding="utf-8")
        self.write("notes.txt", "ignored")
        found = [p.name for p in discover(self.root)]
        self.assertEqual(sorted(found), ["a.yml", "b.yaml"])

    def test_discovery_order_is_stable_across_runs(self):
        (self.root / "nested").mkdir()
        self.write("b.yaml", GOOD)
        (self.root / "nested" / "a.yml").write_text(GOOD, encoding="utf-8")
        # Sorted by full path, so a rebuild never reshuffles the output.
        self.assertEqual(discover(self.root), discover(self.root))
        self.assertEqual([p.name for p in discover(self.root)], ["b.yaml", "a.yml"])

    def test_discovery_rejects_a_path_that_is_not_a_directory(self):
        with self.assertRaises(GuideLoadError):
            discover(self.write("g.yaml", GOOD))


class TestShippedGuides(unittest.TestCase):
    def test_every_guide_in_the_repository_passes_the_offline_gates(self):
        paths = discover(REPO / "guides")
        self.assertTrue(paths, "no guides found in guides/")
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["verify", str(REPO / "guides"), "--no-cache"])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
