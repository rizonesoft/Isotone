#!/usr/bin/env python3
"""Tests for scripts/drift-check.py that need a real Git index, and for the workflow that runs it.

What they prove (D00 T01 §10): the commit hook's file set is the index's own, so a staged deletion is not scanned,
a staged rename is scanned at its new path only, a partially staged file is judged by its staged half, and an
untracked file is not scanned; and the plan-gates workflow has no path filter, so a change to any file the gate
reads runs it, with the GitHub comparison limited to pushes to main.

Run: python scripts/tests/test_drift_check.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_spec = importlib.util.spec_from_file_location("drift_check", ROOT / "scripts" / "drift-check.py")
assert _spec is not None and _spec.loader is not None
dc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = dc
_spec.loader.exec_module(dc)

OLD = "Oldapp"  # an invented retired name: this file names nothing the project has retired
FACTS = {
    "schema": 1,
    "suite": {"name": "Newsuite", "slug": "newsuite", "tag_prefix": "newsuite-v"},
    "apps": [{"name": "Newapp", "slug": "newapp", "tag_prefix": "newapp-v", "role": "Editor"}],
    "repository": {"slug": "owner/Newsuite", "description": "Newsuite.", "topics": ["graphics"],
                   "homepage": "https://example.invalid/"},
    "readme": {"path": "README.md", "opening_line": "Creative apps on one shared core."},
    "versions": [],
    "retired": {"names": [{"word": OLD, "replacement": "Newapp", "date": "2026-01-01"}], "phrases": []},
    "allow": {"paths": [], "quotes": [], "patterns": [], "counts": []},
}


class IndexFileSet(unittest.TestCase):
    """The hook checks out the index and passes `git ls-files -z`; these do the same in a throwaway repository."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="isotone-drift-repo-"))
        self.export = Path(tempfile.mkdtemp(prefix="isotone-drift-export-"))
        self.git("init", "-q")
        self.write("README.md", "# Newsuite\n\nCreative apps on one shared core.\n")
        self.write("docs/facts.json", json.dumps(FACTS))
        self.write("docs/clean.md", "Newapp.\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)
        shutil.rmtree(self.export, ignore_errors=True)

    def git(self, *argv: str) -> bytes:
        done = subprocess.run(["git", "-C", str(self.repo), "-c", "user.email=test@example.invalid", "-c", "user.name=test",
                               "-c", "commit.gpgsign=false", "-c", "core.hooksPath=.git/no-hooks", "-c", "core.autocrlf=false",
                               *argv], capture_output=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr.decode(errors="replace"))
        return done.stdout

    def write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def staged_findings(self) -> list[str]:
        """What the hook sees: the index checked out to a folder with no repository, and the index's file list."""
        shutil.rmtree(self.export, ignore_errors=True)
        self.export.mkdir()
        self.git("checkout-index", "-a", f"--prefix={self.export.as_posix()}/")
        listing = self.export.parent / (self.export.name + ".files")
        listing.write_bytes(self.git("ls-files", "-z"))
        try:
            return [f.render() for f in dc.tree_findings(self.export, str(listing))]
        finally:
            listing.unlink()

    def test_a_staged_addition_is_scanned_and_an_untracked_file_is_not(self):
        self.write("docs/new.md", f"The {OLD} editor.\n")
        self.write("scratch.md", f"{OLD} in a scratch file nobody staged.\n")
        self.assertEqual(self.staged_findings(), [], "nothing is staged yet")
        self.git("add", "docs/new.md")
        found = self.staged_findings()
        self.assertEqual(len(found), 1, found)
        self.assertTrue(found[0].startswith("docs/new.md:1:retired-name:"), found[0])

    def test_a_staged_deletion_is_not_scanned(self):
        self.write("docs/old.md", f"{OLD}\n")
        self.git("add", "docs/old.md")
        self.git("commit", "-q", "-m", "a file that names it")
        self.assertEqual(len(self.staged_findings()), 1)
        self.git("rm", "-q", "docs/old.md")
        self.assertEqual(self.staged_findings(), [], "the commit will not hold the file")
        # `git diff --cached --name-only` would have listed it, which is why the hook does not use that list.
        self.assertIn(b"docs/old.md", self.git("diff", "--cached", "--name-only"))
        self.assertNotIn(b"docs/old.md", self.git("ls-files", "-z"))

    def test_a_staged_rename_is_scanned_at_its_new_path_only(self):
        self.write("docs/old.md", f"{OLD}\n")
        self.git("add", "docs/old.md")
        self.git("commit", "-q", "-m", "a file that names it")
        self.git("mv", "docs/old.md", "docs/renamed.md")
        found = self.staged_findings()
        self.assertEqual(len(found), 1, found)
        self.assertTrue(found[0].startswith("docs/renamed.md:1:retired-name:"), found[0])

    def test_a_partially_staged_file_is_judged_by_its_staged_half(self):
        self.write("docs/clean.md", f"Newapp.\nThe {OLD} editor.\n")
        self.git("add", "docs/clean.md")
        self.write("docs/clean.md", "Newapp.\nThe Newapp editor.\n")  # fixed in the work tree, not staged
        found = self.staged_findings()
        self.assertEqual(len(found), 1, "the staged content still names it")
        self.assertTrue(found[0].startswith("docs/clean.md:2:retired-name:"), found[0])
        self.git("add", "docs/clean.md")
        self.write("docs/clean.md", f"Newapp.\nThe {OLD} editor.\n")  # broken in the work tree, not staged
        self.assertEqual(self.staged_findings(), [], "the staged content is clean")

    def test_the_default_run_lists_the_repositorys_tracked_files(self):
        self.write("scratch.md", f"{OLD}\n")
        self.assertEqual([f.render() for f in dc.tree_findings(self.repo, None)], [], "an untracked file is not scanned")
        self.git("add", "scratch.md")
        self.assertEqual(len(dc.tree_findings(self.repo, None)), 1)


class Wiring(unittest.TestCase):
    def test_the_workflow_runs_for_every_file_the_gate_reads(self):
        text = (ROOT / ".github" / "workflows" / "plan.yml").read_text(encoding="utf-8")
        triggers = text[text.index("\non:\n"):text.index("\npermissions:")]
        self.assertRegex(triggers, r"\n  push:\n    branches: \[main\]\n")
        self.assertRegex(triggers, r"\n  pull_request:\n    branches: \[main\]\n")
        # The drift gate reads every tracked text file, so any path filter would let some change skip it.
        self.assertNotIn("paths:", triggers)
        self.assertNotIn("paths-ignore:", triggers)

    def test_the_workflow_runs_the_gate_and_compares_github_on_main_only(self):
        text = (ROOT / ".github" / "workflows" / "plan.yml").read_text(encoding="utf-8")
        for command in ("python3 scripts/drift-check.py --self-test", "python3 scripts/drift-check.py\n",
                        "python3 scripts/tests/test_drift_check.py", "python3 scripts/todo-claims.py --quiet"):
            self.assertIn(command, text)
        step = re.search(r"      - name: [^\n]*\n((?:        [^\n]*\n)*?)        run: python3 scripts/drift-check\.py --check-github\n", text)
        self.assertIsNotNone(step)
        assert step is not None
        self.assertIn("if: github.event_name == 'push' && github.ref == 'refs/heads/main'", step.group(1))
        self.assertIn("GH_TOKEN: ${{ github.token }}", step.group(1))

    def test_the_hook_passes_the_index_file_list(self):
        hook = (ROOT / "tools" / "githooks" / "pre-commit").read_text(encoding="utf-8")
        self.assertIn('git ls-files -z > "$WORK.files"', hook)
        self.assertIn('scripts/drift-check.py --files-from "$WORK.files"', hook)
        self.assertNotIn("git diff --cached --name-only", hook)
        self.assertNotIn("\r", hook, "the hook keeps LF line endings")

    def test_the_real_facts_file_is_whole(self):
        facts, problems = dc.load_facts(ROOT)
        self.assertEqual([p.render() for p in problems], [])
        assert facts is not None
        self.assertEqual([app["slug"] for app in facts["apps"]], ["stilus", "gesso", "albumen", "tinctura", "capio", "folium"])
        self.assertEqual(len(facts["repository"]["topics"]), 10)
        self.assertLessEqual(len(facts["repository"]["description"]), 350, "GitHub's limit for a description")
        for app in facts["apps"]:
            self.assertEqual(app["tag_prefix"], app["slug"] + "-v")


if __name__ == "__main__":
    unittest.main(verbosity=1)
