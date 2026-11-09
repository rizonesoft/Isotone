"""The pin automations: the shared notifier and proposer, and every check script with fake sources.

Ported in shape from RectoPDF's `tests/scripts/test_pin_automations.py` (2026-10-21). Git-backed cases build a
throwaway repository with an isolated git configuration, so the operator's global settings (signing, hooks, default
branch) never apply and nothing outside the temp folder changes. The last class holds the workspace check that every
settings hook runs a script that exists, which lived in test_automations.py before that file took only the automations tests.
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), REPO / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pin_proposal = load("lib/pin_proposal")


def completed(returncode, stdout=""):
    """A stand-in for subprocess.run's result."""
    return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr="")


class Mailbox:
    def __init__(self):
        self.sent = []

    def __call__(self, root, subject, body, dry_run=False):
        self.sent.append((subject, body))


class FakeGh:
    """Records gh calls and answers the list queries the pin modes make."""

    def __init__(self, prs="[]", issues="[]", runs="[]"):
        self.calls, self.prs, self.issues, self.runs = [], prs, issues, runs

    def __call__(self, *args, cwd):
        self.calls.append(args)
        if args[:2] == ("pr", "list"):
            return self.prs
        if args[:2] == ("issue", "list"):
            return self.issues
        if args[:2] == ("run", "list"):
            return self.runs
        if args[:2] in (("pr", "create"), ("issue", "create")):
            return "https://github.com/example/repo/1\n"
        return ""

    def made(self, *prefix):
        return [c for c in self.calls if c[:len(prefix)] == prefix]


class GitRepo(unittest.TestCase):
    """A temp repository on branch main with an isolated git configuration."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "repo"
        self.root.mkdir()
        empty = Path(self._tmp.name) / "gitconfig"
        empty.write_text("", encoding="utf-8")
        env = {"GIT_CONFIG_GLOBAL": str(empty), "GIT_CONFIG_NOSYSTEM": "1", "GIT_AUTHOR_NAME": "t",
               "GIT_AUTHOR_EMAIL": "t@example.invalid", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@example.invalid"}
        self._env = mock.patch.dict(os.environ, env)
        self._env.start()
        self.git("init", "-q", "-b", "main")

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd or self.root, capture_output=True, text=True,
                              check=True).stdout.strip()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "fixture")

    def ref_exists(self, ref):
        return subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=self.root).returncode == 0

    def with_origin(self):
        origin = Path(self._tmp.name) / "origin.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
        self.git("remote", "add", "origin", str(origin))
        self.git("push", "-q", "origin", "main")
        return origin


class NotifierTests(GitRepo):
    def test_notify_passes_the_automations_sender(self):
        """alert.send takes the From line (an earlier notifier once called it with three arguments)."""
        calls = []
        fake = types.ModuleType("alert")
        fake.key = lambda: "k"
        fake.sender = lambda folder: f"{folder.strip(chr(92))} automations <x@example.invalid>"
        fake.send = lambda api_key, subject, body, from_: calls.append((api_key, subject, body, from_))
        pin_proposal.notify(REPO, "subject", "body", alert_module=fake)
        self.assertEqual(calls, [("k", "subject", "body", "Isotone automations <x@example.invalid>")])

    def test_a_notice_goes_out_once_and_a_failed_send_is_retried(self):
        self.write("x", "x")
        self.commit()

        def broken(*_):
            raise OSError("smtp down")
        self.assertEqual(pin_proposal.notice(root=self.root, key="k1", subject="s", body="b", mail=broken), 1)
        self.assertFalse(self.ref_exists("refs/isotone-notice/k1"))
        mail = Mailbox()
        for _ in range(2):
            self.assertEqual(pin_proposal.notice(root=self.root, key="k1", subject="s", body="b", mail=mail), 0)
        self.assertEqual(len(mail.sent), 1)
        self.assertTrue(self.ref_exists("refs/isotone-notice/k1"))


class LocalToolsTests(GitRepo):
    def setUp(self):
        super().setUp()
        self.mod = load("check-local-tools")
        self.write("README.md", "fixture\n")
        self.commit()
        self.versions = {"codex": "codex-cli 0.162.1", "claude": "2.1.305 (Claude Code)"}

    def fetch(self, url):
        if "python.org" in url:
            return [{"name": "Python 3.14.4"}, {"name": "Python 3.13.9"}]
        return {"version": {"%40openai%2Fcodex": "0.163.0"}.get(url.split("/")[-2], "0.163.0")
                if "codex" in url else "2.1.305"}

    def fake_run(self, argv, **kwargs):
        name = Path(argv[0]).name
        return completed(0, self.versions[name])

    def which(self, name):
        return name if name in self.versions else None

    def call(self, mode, mail=None, **kw):
        return self.mod.main([mode], fetch=kw.get("fetch", self.fetch), root=self.root, run=self.fake_run,
                             which=kw.get("which", self.which), local=kw.get("local", (3, 14, 4)),
                             mail=mail or Mailbox())

    def test_a_behind_cli_is_found_and_announced_once(self):
        self.assertEqual(self.call("check"), 1)
        found = self.mod.cli_findings(self.fetch, self.fake_run, self.which)
        self.assertEqual(found, ["the codex CLI 0.162.1 is behind @openai/codex 0.163.0"])
        mail = Mailbox()
        self.assertEqual(self.call("notify", mail), 0)
        self.assertEqual(self.call("notify", mail), 0)
        self.assertEqual([s for s, _ in mail.sent], ["Isotone: a newer tool is available on this PC"])

    def test_everything_current_passes_without_global_json(self):
        self.assertFalse((self.root / "global.json").exists())
        self.versions["codex"] = "codex-cli 0.163.0"
        self.assertEqual(self.call("check"), 0)

    def test_a_missing_cli_is_a_finding_never_a_pass(self):
        self.versions["codex"] = "codex-cli 0.163.0"
        self.assertEqual(self.call("check", which=lambda n: None if n == "claude" else self.which(n)), 1)

    def test_python_behind_its_minor_or_patch_is_reported(self):
        releases = [{"name": "Python 3.15.0"}, {"name": "Python 3.14.8"}]
        self.assertIn("newest stable minor 3.15", self.mod.python_findings(releases, (3, 14, 8))[0])
        self.assertIn("latest patch 3.14.8", self.mod.python_findings(releases[1:], (3, 14, 4))[0])
        self.assertEqual(self.mod.python_findings(releases[1:], (3, 14, 8)), [])

    def test_an_unreadable_source_cannot_check(self):
        self.assertEqual(self.call("check", fetch=lambda url: {} if "npm" in url else []), 2)


class ReviewRound3Tests(GitRepo):
    """The independent review round 3 findings (2026-10-21) for pin_proposal and pins.yml."""

    def setUp(self):
        super().setUp()
        self.write("pin.txt", "1.0.0\n")
        self.commit()

    def test_propose_pr_pushes_branch_opens_pr_and_dispatches_ci(self):
        origin = self.with_origin()
        gh = FakeGh()

        def rewrite(root):
            (Path(root) / "pin.txt").write_text("1.1.0\n", encoding="utf-8")
            return ["pin.txt"]

        self.assertEqual(pin_proposal.propose_pr(
            root=self.root, branch="pins/tool-1.1.0", rewrite=rewrite, checks=lambda _: [],
            title="build: pin tool 1.1.0", body="bumps tool", run_gh=gh), 0)
        pushed = self.git("show", "pins/tool-1.1.0:pin.txt", cwd=origin)
        self.assertEqual(pushed, "1.1.0")
        (create,) = gh.made("pr", "create")
        self.assertIn("build: pin tool 1.1.0", create)
        self.assertEqual([c[2] for c in gh.made("workflow", "run")], ["build.yml", "plan.yml"])
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD"), "main")
        self.assertEqual((self.root / "pin.txt").read_text(encoding="utf-8"), "1.0.0\n")

    def test_a_version_with_any_existing_pr_is_never_proposed_again(self):
        origin = self.with_origin()
        gh = FakeGh(prs='[{"number": 7, "state": "CLOSED"}]')
        self.assertEqual(pin_proposal.propose_pr(
            root=self.root, branch="pins/tool-1.1.0", rewrite=lambda _: ["pin.txt"], checks=lambda _: [],
            title="build: pin tool 1.1.0", body="bumps tool", run_gh=gh), 0)
        self.assertEqual(gh.made("pr", "create"), [])
        self.assertEqual(self.git("branch", "--list", "pins/*", cwd=origin), "")

    def test_an_open_pr_without_ci_gets_it_dispatched(self):
        self.with_origin()
        gh = FakeGh(prs='[{"number": 9, "state": "OPEN"}]')
        self.assertEqual(pin_proposal.propose_pr(
            root=self.root, branch="pins/tool-1.1.0", rewrite=lambda _: ["pin.txt"], checks=lambda _: [],
            title="build: pin tool 1.1.0", body="bumps tool", run_gh=gh), 0)
        self.assertEqual([c[2] for c in gh.made("workflow", "run")], ["build.yml", "plan.yml"])
        gh = FakeGh(prs='[{"number": 9, "state": "OPEN"}]', runs='[{"databaseId": 1}]')
        pin_proposal.propose_pr(
            root=self.root, branch="pins/tool-1.1.0", rewrite=lambda _: ["pin.txt"], checks=lambda _: [],
            title="build: pin tool 1.1.0", body="bumps tool", run_gh=gh)
        self.assertEqual(gh.made("workflow", "run"), [])

    def test_a_returning_finding_supersedes_the_newer_open_issue(self):
        issues = json.dumps([{"number": 7, "title": "A", "state": "CLOSED", "labels": [{"name": "pins:resolved"}]},
                             {"number": 8, "title": "A and B", "state": "OPEN", "labels": []}])
        gh = FakeGh(issues=issues)
        pin_proposal.file_issue(root=self.root, check="x", title="A", body="b", run_gh=gh)
        self.assertEqual([c[2] for c in gh.made("issue", "reopen")], ["7"])
        self.assertEqual([c[2] for c in gh.made("issue", "close")], ["8"])

    def test_a_superseded_finding_that_returns_reopens_its_issue(self):
        older = json.dumps([{"number": 7, "title": "A", "state": "OPEN", "labels": []}])
        gh = FakeGh(issues=older)
        pin_proposal.file_issue(root=self.root, check="x", title="A and B", body="b", run_gh=gh)
        self.assertIn(("issue", "edit", "7", "--add-label", "pins:resolved"), gh.calls)
        back = json.dumps([{"number": 7, "title": "A", "state": "CLOSED", "labels": [{"name": "pins:resolved"}]}])
        gh = FakeGh(issues=back)
        pin_proposal.file_issue(root=self.root, check="x", title="A", body="b", run_gh=gh)
        self.assertEqual([c[2] for c in gh.made("issue", "reopen")], ["7"])

    def test_a_resolved_finding_that_returns_reopens_its_issue_and_a_dismissed_one_stays(self):
        resolved = json.dumps([{"number": 5, "title": "t", "state": "CLOSED", "labels": [{"name": "pins:resolved"}]}])
        gh = FakeGh(issues=resolved)
        pin_proposal.file_issue(root=self.root, check="x", title="t", body="b", run_gh=gh)
        self.assertEqual([c[2] for c in gh.made("issue", "reopen")], ["5"])
        dismissed = json.dumps([{"number": 5, "title": "t", "state": "CLOSED", "labels": []}])
        gh = FakeGh(issues=dismissed)
        pin_proposal.file_issue(root=self.root, check="x", title="t", body="b", run_gh=gh)
        self.assertEqual(gh.made("issue", "reopen") + gh.made("issue", "create"), [])
        gh = FakeGh(issues='[{"number": 6}]')
        pin_proposal.resolve_issues(root=self.root, check="x", message="m", run_gh=gh)
        self.assertEqual(gh.made("issue", "edit"), [("issue", "edit", "6", "--add-label", "pins:resolved")])

    def test_each_pins_job_holds_only_its_permissions(self):
        workflow = (REPO / ".github" / "workflows" / "pins.yml").read_text(encoding="utf-8")
        for job_name in ("native-advisories",):
            job = workflow.split(f"\n  {job_name}:\n", 1)[1]
            block = job.split("permissions:\n", 1)[1].split("\n    steps:", 1)[0]
            with self.subTest(job=job_name):
                self.assertEqual(sorted(line.strip() for line in block.splitlines() if line.strip()),
                                 ["contents: read", "issues: write"])


class NativeAdvisoriesTests(unittest.TestCase):
    class FakeRoot:
        def __init__(self, files=None, rel=""):
            self._files = {} if files is None else files
            self._rel = rel.strip("/")

        def __truediv__(self, part):
            p = str(part).replace("\\", "/").strip("/")
            return NativeAdvisoriesTests.FakeRoot(self._files, f"{self._rel}/{p}".strip("/"))

        def is_file(self):
            return self._rel in self._files

        def read_text(self, encoding="utf-8"):
            if self._rel not in self._files:
                raise OSError(f"No such file: {self._rel}")
            return self._files[self._rel]

        def write_text(self, content, encoding="utf-8"):
            self._files[self._rel] = content

        def __str__(self):
            return f"virtual-repo/{self._rel}" if self._rel else "virtual-repo"

    def setUp(self):
        self.root = self.FakeRoot()
        self.mod = load("check-native-advisories")
        self.base_sha = "9eec002df1cd109f8f104cd966a763daf9751489"
        self.write("native/vcpkg.json", json.dumps({
            "name": "isotone",
            "version-semver": "0.0.0",
            "builtin-baseline": self.base_sha,
            "dependencies": [],
            "features": {"test": {"dependencies": ["gtest"]}},
        }, indent=2) + "\n")
        self.write("native/vcpkg-configuration.json", json.dumps({
            "$schema": "https://raw.githubusercontent.com/microsoft/vcpkg-tool/main/docs/vcpkg-configuration.schema.json",
        }, indent=2) + "\n")
        self.baseline_file = str(REPO / "scripts" / "tests" / "fixtures" / "osv" / "baseline-committed.json")

    def write(self, rel, content):
        (self.root / rel).write_text(content, encoding="utf-8")

    def table(self, *rows):
        cols = self.mod.DEPS_LINT.COLUMNS
        head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
        return "# Register\n\n" + head + "".join("| " + " | ".join(r) + " |\n" for r in rows)

    def test_clean_and_vulnerable_and_unmapped_issue_mode(self):
        gtest_row = [
            "GoogleTest", "gtest", "1.18.0", "BSD-3-Clause", "u", "yes", "none", "x64, arm64",
            "https://github.com/google/googletest", "v1.18.0", "osv-git:https://github.com/google/googletest@v1.18.0",
            "no", "tests", "direct", "D00 T05 §2", "static", "none",
        ]
        clean_reg = self.table(gtest_row)
        self.write("docs/dev/native-libraries.md", clean_reg)
        clean_osv = str(REPO / "scripts" / "tests" / "fixtures" / "osv" / "clean.json")
        with mock.patch.object(self.mod, "default_resolve_tag", return_value="a" * 40):
            self.assertEqual(self.mod.main(
                ["check", "--baseline-file", self.baseline_file, "--osv-fixture", clean_osv],
                root=self.root), 0)

        unmapped_row = [
            "GoogleTest", "gtest", "1.18.0", "BSD-3-Clause", "u", "yes", "none", "x64, arm64",
            "https://github.com/google/googletest", "v1.18.0", "none: build-time helper, not linked",
            "no", "tests", "direct", "D00 T05 §2", "static", "none",
        ]
        self.write("docs/dev/native-libraries.md", self.table(unmapped_row))
        gh = FakeGh()
        self.assertEqual(self.mod.main(
            ["issue", "--baseline-file", self.baseline_file, "--osv-fixture", clean_osv],
            root=self.root, run_gh=gh), 1)
        (create,) = gh.made("issue", "create")
        self.assertIn("pins:native-advisories-unmapped", create)
        title = create[create.index("--title") + 1]

        self.write("docs/dev/native-libraries.md", clean_reg)
        gh2 = FakeGh(issues=json.dumps([{
            "number": 12,
            "title": title,
            "state": "OPEN",
            "labels": [{"name": "pins"}, {"name": "pins:native-advisories-unmapped"}],
        }]))
        with mock.patch.object(self.mod, "default_resolve_tag", return_value="a" * 40):
            self.assertEqual(self.mod.main(
                ["issue", "--baseline-file", self.baseline_file, "--osv-fixture", clean_osv],
                root=self.root, run_gh=gh2), 0)
        self.assertIn("12", [c[2] for c in gh2.made("issue", "close")])


class WorkspaceHooks(unittest.TestCase):
    def test_every_hook_script_exists(self):
        settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
        commands = [h["command"] for entries in settings["hooks"].values() for entry in entries for h in entry["hooks"]]
        scripts = [m for c in commands for m in re.findall(r"'(scripts|hooks)', '([\w.-]+\.(?:py|ps1))'", c)]
        self.assertTrue(scripts, commands)
        for folder, name in scripts:
            path = REPO / "scripts" / name if folder == "scripts" else REPO / ".claude" / "hooks" / name
            with self.subTest(script=name):
                self.assertTrue(path.is_file(), path)

    def test_the_pins_workflow_runs_only_scripts_that_exist(self):
        workflow = (REPO / ".github" / "workflows" / "pins.yml").read_text(encoding="utf-8")
        for script in re.findall(r"run: python3? (scripts/[\w.-]+\.py)", workflow):
            with self.subTest(script=script):
                self.assertTrue((REPO / script).is_file(), script)


if __name__ == "__main__":
    unittest.main()
