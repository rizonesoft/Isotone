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
        """alert.send takes the From line (RectoPDF's WinUI notifier once called it with three arguments)."""
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


RC2_SDK, RC2_RT = "11.0.100-rc.2.26504.105", "11.0.0-rc.2.26504.105"
RC3_SDK, RC3_RT = "11.0.100-rc.3.26560.101", "11.0.0-rc.3.26560.101"
GA_SDK, GA_RT = "11.0.100", "11.0.0"


def feed(latest_sdk, latest_runtime):
    releases = [{"sdk": {"version": s}, "runtime": {"version": r}}
                for s, r in ((GA_SDK, GA_RT), (RC3_SDK, RC3_RT), (RC2_SDK, RC2_RT))]
    return {"channel-version": "11.0", "latest-sdk": latest_sdk, "latest-runtime": latest_runtime,
            "releases": releases}


class DotnetFixture(GitRepo):
    PROPS = ('<Project>\n  <!-- (11.0.0-rc.2 until .NET 11 GA) -->\n  <ItemGroup>\n'
             f'    <PackageVersion Include="Microsoft.Extensions.Hosting" Version="{RC2_RT}" />\n'
             f'    <PackageVersion Include="Microsoft.Extensions.DependencyInjection" Version="{RC2_RT}" />\n'
             '    <PackageVersion Include="Serilog" Version="4.4.0" />\n  </ItemGroup>\n</Project>\n')

    def setUp(self):
        super().setUp()
        self.mod = load("check-dotnet-pin")
        self.write("global.json", json.dumps({"sdk": {"version": RC2_SDK, "allowPrerelease": True,
                                                      "rollForward": "disable"}}, indent=2) + "\n")
        self.write("Directory.Packages.props", self.PROPS)
        self.write("docs/dev/build.md", f"| .NET SDK | {RC2_SDK} (exact) |\npinned (11.0.100-rc.2) and 11.0.100-rc.20 stays\n")
        self.write("CHANGELOG.md", f"SDK {RC2_SDK} pinned\n")
        self.commit()

    def fetcher(self, latest_sdk, latest_runtime, listed=True):
        def fetch(url):
            if "release-metadata" in url:
                return feed(latest_sdk, latest_runtime)
            return {"versions": [latest_runtime] if listed else []}
        return fetch


class DotnetPinTests(DotnetFixture):
    def test_the_newest_release_is_current(self):
        self.assertEqual(self.mod.main(["check"], fetch=self.fetcher(RC2_SDK, RC2_RT), root=self.root), 0)

    def test_a_newer_release_candidate_is_behind(self):
        self.assertEqual(self.mod.main(["check"], fetch=self.fetcher(RC3_SDK, RC3_RT), root=self.root), 1)

    def test_a_pin_the_feed_does_not_list_cannot_be_checked(self):
        self.write("global.json", json.dumps({"sdk": {"version": "11.0.100-rc.9.1.1"}}))
        self.assertEqual(self.mod.main(["check"], fetch=self.fetcher(RC3_SDK, RC3_RT), root=self.root), 2)

    def test_an_unreadable_feed_cannot_be_checked(self):
        self.assertEqual(self.mod.main(["check"], fetch=lambda url: {}, root=self.root), 2)

    def test_the_rewrite_moves_the_sdk_the_tracking_packages_and_the_quoted_docs_only(self):
        changed = self.mod.rewrite_tree(self.root, RC2_SDK, RC3_SDK, RC2_RT, RC3_RT)
        self.assertEqual(sorted(changed), ["Directory.Packages.props", "docs/dev/build.md", "global.json"])
        pin = json.loads((self.root / "global.json").read_text(encoding="utf-8"))["sdk"]
        self.assertEqual((pin["version"], pin["allowPrerelease"], pin["rollForward"]), (RC3_SDK, True, "disable"))
        props = (self.root / "Directory.Packages.props").read_text(encoding="utf-8")
        self.assertEqual(props.count(RC3_RT), 2)
        self.assertIn('"Serilog" Version="4.4.0"', props)
        self.assertIn("(11.0.0-rc.3 until", props)
        docs = (self.root / "docs/dev/build.md").read_text(encoding="utf-8")
        self.assertIn(RC3_SDK, docs)
        self.assertIn("(11.0.100-rc.3)", docs)
        self.assertIn("11.0.100-rc.20 stays", docs, "a longer version that starts with the short form is not touched")
        self.assertIn(RC2_SDK, (self.root / "CHANGELOG.md").read_text(encoding="utf-8"), "records are never rewritten")

    def test_the_ga_move_drops_allow_prerelease(self):
        self.mod.rewrite_tree(self.root, RC2_SDK, GA_SDK, RC2_RT, GA_RT)
        pin = json.loads((self.root / "global.json").read_text(encoding="utf-8"))["sdk"]
        self.assertEqual(pin, {"version": GA_SDK, "rollForward": "disable"})
        self.assertIn(f'Version="{GA_RT}"', (self.root / "Directory.Packages.props").read_text(encoding="utf-8"))

    def test_short_forms(self):
        self.assertEqual(self.mod.short(RC2_SDK), "11.0.100-rc.2")
        self.assertEqual(self.mod.short(RC2_RT), "11.0.0-rc.2")
        self.assertEqual(self.mod.short(GA_SDK), GA_SDK)

    def test_pr_mode_pushes_the_branch_opens_a_pr_and_dispatches_ci(self):
        origin = self.with_origin()
        gh = FakeGh()
        self.assertEqual(self.mod.main(["pr"], fetch=self.fetcher(RC3_SDK, RC3_RT), root=self.root, run_gh=gh), 0)
        branch = f"pins/dotnet-{RC3_SDK}"
        pushed = self.git("show", f"{branch}:global.json", cwd=origin)
        self.assertIn(RC3_SDK, pushed)
        (create,) = gh.made("pr", "create")
        self.assertIn("build: pin the .NET 11.0 SDK " + RC3_SDK, create)
        self.assertEqual([c[2] for c in gh.made("workflow", "run")], ["build.yml", "plan.yml"])
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD"), "main")
        self.assertIn(RC2_SDK, (self.root / "global.json").read_text(encoding="utf-8"), "main is left alone")

    def test_a_ga_pr_names_the_section_that_owns_the_move(self):
        self.with_origin()
        gh = FakeGh()
        self.assertEqual(self.mod.main(["pr"], fetch=self.fetcher(GA_SDK, GA_RT), root=self.root, run_gh=gh), 0)
        (create,) = gh.made("pr", "create")
        self.assertIn("GA SDK 11.0.100", create[create.index("--title") + 1])
        self.assertIn("D00 T02 §8", create[create.index("--body") + 1])

    def test_a_version_with_any_existing_pr_is_never_proposed_again(self):
        origin = self.with_origin()
        gh = FakeGh(prs='[{"number": 7, "state": "CLOSED"}]')
        self.assertEqual(self.mod.main(["pr"], fetch=self.fetcher(RC3_SDK, RC3_RT), root=self.root, run_gh=gh), 0)
        self.assertEqual(gh.made("pr", "create"), [])
        self.assertEqual(self.git("branch", "--list", "pins/*", cwd=origin), "")

    def test_packages_nuget_does_not_list_yet_propose_nothing(self):
        origin = self.with_origin()
        gh = FakeGh()
        fetch = self.fetcher(RC3_SDK, RC3_RT, listed=False)
        self.assertEqual(self.mod.main(["pr"], fetch=fetch, root=self.root, run_gh=gh), 1)
        self.assertEqual(gh.made("pr", "create"), [])
        self.assertEqual(self.git("branch", "--list", "pins/*", cwd=origin), "")


class VulnerableTests(GitRepo):
    def setUp(self):
        super().setUp()
        self.mod = load("check-vulnerable-packages")

    def report(self, vulnerable):
        package = {"id": "Pkg", "resolvedVersion": "1.0.0",
                   "vulnerabilities": [{"severity": "High", "advisoryurl": "https://x/1"}] if vulnerable else []}
        path = self.root / "report.json"
        path.write_text(json.dumps({"projects": [{"path": "src/A/A.csproj", "frameworks": [
            {"framework": "net11.0-windows", "topLevelPackages": [], "transitivePackages": [package]}]}]}),
            encoding="utf-8")
        return str(path)

    def test_a_clean_report_passes_and_a_vulnerable_one_fails(self):
        self.assertEqual(self.mod.main(["check", "--report", self.report(False)]), 0)
        self.assertEqual(self.mod.main(["check", "--report", self.report(True)]), 1)

    def test_problems_or_no_projects_are_unverified(self):
        self.assertEqual(self.mod.verdict({"problems": [{"text": "x"}], "projects": [{}]})[0], 2)
        self.assertEqual(self.mod.verdict({"projects": []})[0], 2)

    def test_the_transitive_finding_names_its_package_and_kind(self):
        report = json.loads(Path(self.report(True)).read_text(encoding="utf-8"))
        self.assertEqual(self.mod.findings(report), ["A.csproj (net11.0-windows): Pkg 1.0.0 High https://x/1 (transitive)"])

    def test_issue_mode_files_once_and_a_clean_run_resolves(self):
        gh = FakeGh()
        self.assertEqual(self.mod.main(["issue", "--report", self.report(True)], root=self.root, run_gh=gh), 0)
        (create,) = gh.made("issue", "create")
        title = create[create.index("--title") + 1]
        self.assertIn("pins:vulnerable-packages", create)
        gh = FakeGh(issues=json.dumps([{"number": 4, "title": title, "state": "OPEN"}]))
        self.assertEqual(self.mod.main(["issue", "--report", self.report(True)], root=self.root, run_gh=gh), 0)
        self.assertEqual(gh.made("issue", "create"), [])
        gh = FakeGh(issues='[{"number": 4}]')
        self.assertEqual(self.mod.main(["issue", "--report", self.report(False)], root=self.root, run_gh=gh), 0)
        self.assertEqual([c[2] for c in gh.made("issue", "close")], ["4"])


class LocalToolsTests(GitRepo):
    def setUp(self):
        super().setUp()
        self.mod = load("check-local-tools")
        self.write("global.json", json.dumps({"sdk": {"version": RC2_SDK}}))
        self.commit()
        self.versions = {"codex": "codex-cli 0.162.1", "claude": "2.1.305 (Claude Code)",
                         "dotnet": f"10.0.402 [C:\\sdk]\n{RC2_SDK} [C:\\sdk]\n"}

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

    def test_everything_current_passes(self):
        self.versions["codex"] = "codex-cli 0.163.0"
        self.assertEqual(self.call("check"), 0)

    def test_a_missing_cli_or_sdk_is_a_finding_never_a_pass(self):
        self.versions["codex"] = "codex-cli 0.163.0"
        self.assertEqual(self.call("check", which=lambda n: None if n == "claude" else self.which(n)), 1)
        self.versions["dotnet"] = "10.0.402 [C:\\sdk]\n"
        self.assertIn("lacks the pinned .NET SDK", self.mod.dotnet_findings(self.root, self.fake_run, self.which)[0])

    def test_python_behind_its_minor_or_patch_is_reported(self):
        releases = [{"name": "Python 3.15.0"}, {"name": "Python 3.14.8"}]
        self.assertIn("newest stable minor 3.15", self.mod.python_findings(releases, (3, 14, 8))[0])
        self.assertIn("latest patch 3.14.8", self.mod.python_findings(releases[1:], (3, 14, 4))[0])
        self.assertEqual(self.mod.python_findings(releases[1:], (3, 14, 8)), [])

    def test_an_unreadable_source_cannot_check(self):
        self.assertEqual(self.call("check", fetch=lambda url: {} if "npm" in url else []), 2)


class ReviewRound3Tests(DotnetFixture):
    """The independent review round 3 findings (2026-10-21), one case each where code changed."""

    def test_only_whole_versions_are_replaced_and_the_badge_moves(self):
        self.write("README.md", f"[badge](https://img.shields.io/badge/.NET-11.0.100--rc.2-512BD4)\n"
                                f"111.0.100-rc.2.26504.105 and {RC2_SDK}+build42 stay; {RC2_SDK} moves.\n")
        self.mod.rewrite_tree(self.root, RC2_SDK, RC3_SDK, RC2_RT, RC3_RT)
        text = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn(".NET-11.0.100--rc.3-512BD4", text)
        self.assertIn("111.0.100-rc.2.26504.105", text)
        self.assertIn(f"{RC2_SDK}+build42", text)
        self.assertIn(f"{RC3_SDK} moves", text)

    def test_a_longer_version_with_a_letter_or_hyphen_suffix_is_left_alone(self):
        self.write("Directory.Packages.props", self.PROPS.replace(
            "</ItemGroup>", f'<PackageVersion Include="Custom" Version="{RC2_RT}-private" />\n  </ItemGroup>'))
        self.mod.rewrite_tree(self.root, RC2_SDK, GA_SDK, RC2_RT, GA_RT)
        props = (self.root / "Directory.Packages.props").read_text(encoding="utf-8")
        self.assertIn(f'"Custom" Version="{RC2_RT}-private"', props)
        self.assertEqual(props.count(f'Version="{GA_RT}"'), 2)

    def test_a_ga_badge_moves_to_the_next_ga_and_an_rc_mention_stays(self):
        self.write("README.md", "[b](https://img.shields.io/badge/.NET-11.0.100-512BD4?logo=dotnet)\n"
                                "[c](https://img.shields.io/badge/old-11.0.100--rc.2-gray)\n")
        self.mod.rewrite_tree(self.root, GA_SDK, "11.0.101", GA_RT, "11.0.1")
        text = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn(".NET-11.0.101-512BD4?logo", text)
        self.assertIn("old-11.0.100--rc.2-gray", text, "a different, longer version in a badge is left alone")

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

    def test_agents_md_is_rewritten_with_the_docs(self):
        self.write("AGENTS.md", f"the SDK {RC2_SDK} is pinned\n")
        self.assertIn("AGENTS.md", self.mod.rewrite_tree(self.root, RC2_SDK, RC3_SDK, RC2_RT, RC3_RT))

    def test_a_ga_pr_lists_the_prerelease_prose_left_for_the_section(self):
        self.with_origin()
        gh = FakeGh()
        self.assertEqual(self.mod.main(["pr"], fetch=self.fetcher(GA_SDK, GA_RT), root=self.root, run_gh=gh), 0)
        (create,) = gh.made("pr", "create")
        body = create[create.index("--body") + 1]
        self.assertIn("Prose that still describes a prerelease pin", body)

    def test_an_interrupted_rewrite_leaves_the_old_file_whole(self):
        path = self.root / "global.json"
        before = path.read_bytes()
        with mock.patch.object(Path, "replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.mod.write_atomic(path, b"{}")
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual([p.name for p in self.root.iterdir() if p.name.endswith(".tmp")], [])

    def test_a_feed_older_than_the_pin_proposes_nothing(self):
        self.write("global.json", json.dumps({"sdk": {"version": RC3_SDK}}))
        gh = FakeGh()
        self.assertEqual(self.mod.main(["pr"], fetch=self.fetcher(RC2_SDK, RC2_RT), root=self.root, run_gh=gh), 2)
        self.assertEqual(gh.made("pr", "create"), [])
        self.assertLess(self.mod.sdk_key(RC2_SDK), self.mod.sdk_key(RC3_SDK))
        self.assertLess(self.mod.sdk_key(RC3_SDK), self.mod.sdk_key(GA_SDK))

    def test_an_open_pr_without_ci_gets_it_dispatched(self):
        self.with_origin()
        gh = FakeGh(prs='[{"number": 9, "state": "OPEN"}]')
        self.assertEqual(self.mod.main(["pr"], fetch=self.fetcher(RC3_SDK, RC3_RT), root=self.root, run_gh=gh), 0)
        self.assertEqual([c[2] for c in gh.made("workflow", "run")], ["build.yml", "plan.yml"])
        gh = FakeGh(prs='[{"number": 9, "state": "OPEN"}]', runs='[{"databaseId": 1}]')
        self.mod.main(["pr"], fetch=self.fetcher(RC3_SDK, RC3_RT), root=self.root, run_gh=gh)
        self.assertEqual(gh.made("workflow", "run"), [])

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

    def test_the_vulnerability_restore_does_not_fail_on_the_audit(self):
        self.assertIn("-p:NuGetAudit=false", load("check-vulnerable-packages").RESTORE)

    def test_each_pins_job_holds_only_its_permissions(self):
        workflow = (REPO / ".github" / "workflows" / "pins.yml").read_text(encoding="utf-8")
        job = workflow.split("\n  vulnerable-packages:\n", 1)[1]
        block = job.split("permissions:\n", 1)[1].split("\n    steps:", 1)[0]
        self.assertEqual(sorted(line.strip() for line in block.splitlines() if line.strip()),
                         ["contents: read", "issues: write"])


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
