"""scripts/merge_prs.py (D00 T01 §12): the preflight, the eligibility rules, one merge per run, and the stop on failure.

Every git and gh call goes through a fake, so nothing touches a repository or GitHub; the in-progress check reads a
fixture TODO file through a fake graph.
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("merge_prs", REPO / "scripts" / "merge_prs.py")
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)

HEAD = "a" * 40


def pr(number=1, **over):
    base = {
        "number": number, "author": {"login": "app/dependabot"}, "labels": [{"name": "dependencies"}],
        "baseRefName": "main", "isDraft": False, "headRefName": f"dependabot/nuget/x-{number}",
        "headRefOid": f"{number:040d}", "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN",
        "statusCheckRollup": [{"__typename": "CheckRun", "name": "build-windows", "status": "COMPLETED",
                               "conclusion": "SUCCESS", "workflowName": "build"}],
        "files": [{"path": "Directory.Packages.props"}], "changedFiles": 1, "createdAt": f"2026-10-2{number}T00:00:00Z",
    }
    base.update(over)
    return base


class FakeGit:
    def __init__(self, status="", head=HEAD, remote=HEAD, pull_fails=False, branch="refs/heads/main",
                 fetch_fails=False, origin="https://github.com/rizonesoft/Isotone.git"):
        self.calls, self.status, self.head, self.remote, self.pull_fails = [], status, head, remote, pull_fails
        self.branch, self.fetch_fails, self.origin = branch, fetch_fails, origin

    def __call__(self, *args, cwd=None):
        self.calls.append(args)
        if args[0] == "symbolic-ref":
            return self.branch + "\n"
        if args[:3] == ("remote", "get-url", "origin"):
            return self.origin + "\n"
        if args[0] == "fetch" and self.fetch_fails:
            raise mp.Failed("git fetch --quiet origin main failed: could not read from remote")
        if args[0] == "status":
            return self.status
        if args[:2] == ("rev-parse", "HEAD"):
            return self.head + "\n"
        if args[:2] == ("rev-parse", "origin/main"):
            return self.remote + "\n"
        if args[0] == "pull" and self.pull_fails:
            raise mp.Failed("git pull --ff-only origin main failed: not a fast-forward")
        if args[:2] == ("merge-base", "--is-ancestor") and args[2] == "f" * 40:
            raise mp.Failed("not an ancestor")
        return ""


class FakeGh:
    """A tiny model of GitHub: each listed pull request is OPEN on main until a merge lands it.

    `merge_fails` makes `pr merge` report an error; `lands` says whether the merge landed anyway (the branch delete
    failed after it). `view_fails` makes every `pr view` fail. `retarget` moves the pull request's base before the
    merge; `elsewhere` makes a landed merge report another base; `off_main` gives it a merge commit not on main.
    """

    def __init__(self, prs, merge_fails=False, lands=False, view_fails=False, retarget=None, elsewhere=False,
                 off_main=False, already_merged=()):
        self.calls, self.prs = [], prs
        self.merge_fails, self.lands, self.view_fails = merge_fails, lands, view_fails
        self.retarget, self.elsewhere, self.off_main = retarget, elsewhere, off_main
        self.merged = {str(n) for n in already_merged}

    def _pr(self, n):
        return next(p for p in self.prs if str(p["number"]) == str(n))

    def __call__(self, *args, cwd=None):
        self.calls.append(args)
        if args[:2] == ("pr", "list"):
            return json.dumps([p for p in self.prs if str(p["number"]) not in self.merged])
        if args[:2] == ("pr", "view"):
            if self.view_fails:
                raise mp.Failed("gh pr view failed: connection reset")
            p = self._pr(args[2])
            merged = args[2] in self.merged
            base = self.retarget or ("release" if merged and self.elsewhere else p["baseRefName"])
            return json.dumps(dict(p, baseRefName=base, state="MERGED" if merged else "OPEN",
                                   mergeCommit={"oid": ("f" if self.off_main else "c") * 40} if merged else None))
        if args[:2] == ("pr", "merge"):
            if not self.merge_fails or self.lands:
                self.merged.add(args[2])
            if self.merge_fails:
                raise mp.Failed("gh pr merge failed: could not delete the branch")
        return ""

    def merges(self):
        return [c for c in self.calls if c[:2] == ("pr", "merge")]


class FakeGraph:
    """load_todos() over one fixture file: section 1 stamped, 2 open with Started, 3 open without."""

    def __init__(self, root: Path, started_open=True):
        self.root = root
        body = ("# TODO\n\n## 1. Done\n\n> **Started:** 2026-10-21T00:00:00Z\n\n> **Verified:** x\n\n"
                "## 2. Open\n\n" + ("> **Started:** 2026-10-21T01:00:00Z\n\n" if started_open else "") + "Text.\n\n"
                "## 3. Untouched\n\nText.\n")
        (root / "todo").mkdir(parents=True, exist_ok=True)
        (root / "todo" / "TODO-01-x.md").write_text(body, encoding="utf-8")

    def load_todos(self):
        sec = lambda status: types.SimpleNamespace(status=status, moved="")
        return [types.SimpleNamespace(path="todo/TODO-01-x.md", domain="00-workspace", number="01",
                                      sections={1: sec("x"), 2: sec(" "), 3: sec(" ")}, verified_sections={1})]


def ok_validate(_root):
    return subprocess.CompletedProcess([], 0, "0 fatal\n", "")


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def call(self, argv, gh_fn, git_fn, graph=None, active=lambda r: None, validate=ok_validate,
             lock=lambda root: contextlib.nullcontext(), run_lock=lambda root: contextlib.nullcontext()):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = mp.main(argv, root=self.root, gh_fn=gh_fn, git_fn=git_fn,
                           graph=graph or FakeGraph(self.root, started_open=False), active_fn=active,
                           validate_fn=validate, lock_fn=lock, run_lock_fn=run_lock)
        return code, out.getvalue() + err.getvalue()


class PreflightTests(Base):
    def test_a_dirty_tree_refuses(self):
        code, out = self.call(["run"], FakeGh([pr()]), FakeGit(status=" M x\n"))
        self.assertEqual((code, "uncommitted changes" in out), (2, True))

    def test_a_head_off_origin_main_refuses(self):
        code, out = self.call(["run"], FakeGh([pr()]), FakeGit(head="b" * 40))
        self.assertEqual((code, "is not origin/main" in out), (2, True))

    def test_a_section_in_progress_refuses_naming_it(self):
        code, out = self.call(["run"], FakeGh([pr()]), FakeGit(), graph=FakeGraph(self.root, started_open=True))
        self.assertEqual((code, "D00 T01 §2" in out, "§1" in out.split("progress:")[1]), (2, True, False))

    def test_an_active_campaign_refuses_unless_the_campaign_calls(self):
        active = lambda r: "a campaign run holds the guard"
        code, out = self.call(["run"], FakeGh([pr()]), FakeGit(), active=active)
        self.assertEqual((code, "holds the guard" in out), (2, True))
        gh = FakeGh([pr()])
        code, out = self.call(["run", "--campaign"], gh, FakeGit(), active=active)
        self.assertEqual((code, len(gh.merges())), (0, 1))

    def test_the_guard_file_and_a_live_scheduler_lock_count_as_a_campaign(self):
        (self.root / "build").mkdir()
        (self.root / "build" / "claude-campaign-guard.json").write_text("{}", encoding="utf-8")
        self.assertIn("guard", mp.campaign_active(self.root))
        (self.root / "build" / "claude-campaign-guard.json").unlink()
        (self.root / ".claude").mkdir()
        lock = self.root / ".claude" / "scheduled_tasks.lock"
        lock.write_text(json.dumps({"pid": __import__("os").getpid()}), encoding="utf-8")
        self.assertIn("scheduled_tasks.lock", mp.campaign_active(self.root))
        lock.write_text(json.dumps({"pid": 0}), encoding="utf-8")
        self.assertIsNone(mp.campaign_active(self.root))

    def test_the_scheduled_task_exits_zero_on_a_refusal_so_no_alert_is_sent(self):
        active = lambda r: "a campaign run holds the guard"
        gh = FakeGh([pr()])
        code, out = self.call(["run", "--task"], gh, FakeGit(), active=active)
        self.assertEqual((code, "refused" in out, gh.merges()), (0, True, []))

    def test_a_branch_other_than_main_refuses(self):
        code, out = self.call(["run", "--campaign"], FakeGh([pr()]), FakeGit(branch="refs/heads/topic"))
        self.assertEqual((code, "refs/heads/topic, not main" in out), (2, True))

    def test_a_failed_fetch_is_a_failure_even_for_the_task(self):
        code, out = self.call(["run", "--task"], FakeGh([pr()]), FakeGit(fetch_fails=True))
        self.assertEqual((code, "could not read from remote" in out), (1, True))

    def test_a_held_clone_lock_is_a_busy_refusal(self):
        @contextlib.contextmanager
        def held(root):
            raise mp.Refused("the run guard's lock is held")
            yield
        gh = FakeGh([pr()])
        code, out = self.call(["run", "--task"], gh, FakeGit(), lock=held)
        self.assertEqual((code, "lock is held" in out, gh.merges()), (0, True, []))

    def test_the_real_clone_lock_refuses_while_the_guard_lock_is_held(self):
        (self.root / "scripts").mkdir()
        shutil.copy(REPO / "scripts" / "campaign_guard.py", self.root / "scripts" / "campaign_guard.py")
        guard = mp._load("campaign_guard_test_copy", self.root / "scripts" / "campaign_guard.py")
        with guard._Lock(str(self.root)):
            with self.assertRaises(mp.Refused):
                with mp.clone_lock(self.root):
                    pass
        with mp.clone_lock(self.root):
            pass

    def test_check_reports_and_merges_nothing(self):
        gh = FakeGh([pr(1), pr(2, isDraft=True)])
        code, out = self.call(["check"], gh, FakeGit(status=" M x\n"))
        self.assertEqual((code, "refused" in out, "#1 eligible" in out, "#2 not eligible: is a draft" in out,
                          gh.merges()), (0, True, True, True, []))


class EligibilityTests(unittest.TestCase):
    def reason(self, **over):
        return mp.eligible(pr(**over))

    def test_a_green_dependabot_pull_request_is_eligible(self):
        self.assertEqual(self.reason(), (True, ""))

    def test_the_pins_workflow_counts_only_on_a_pins_branch(self):
        self.assertTrue(self.reason(author={"login": "app/github-actions"}, headRefName="pins/vulnerable-x",
                                    labels=[{"name": "pins"}])[0])
        self.assertIn("neither Dependabot", self.reason(author={"login": "app/github-actions"})[1])

    def test_each_refusal_names_its_reason(self):
        cases = [
            ({"author": {"login": "someone"}}, "neither Dependabot"),
            ({"labels": [{"name": "github_actions"}]}, "neither dependencies nor pins"),
            ({"headRefName": "pins/dotnet-11.0.100"}, ".NET SDK pin"),
            ({"files": [{"path": "global.json"}]}, ".NET SDK pin"),
            ({"baseRefName": "release"}, "targets release"),
            ({"isDraft": True}, "draft"),
            ({"statusCheckRollup": []}, "no checks"),
            ({"statusCheckRollup": [{"__typename": "CheckRun", "name": "b", "status": "IN_PROGRESS", "conclusion": ""}]}, "in_progress"),
            ({"statusCheckRollup": [{"__typename": "CheckRun", "name": "b", "status": "COMPLETED", "conclusion": "FAILURE"}]}, "failure"),
            ({"statusCheckRollup": [{"__typename": "StatusContext", "context": "c", "state": "PENDING"}]}, "pending"),
            ({"mergeable": "CONFLICTING"}, "conflicting"),
            ({"mergeable": "UNKNOWN"}, "unknown"),
            ({"mergeStateStatus": "BEHIND"}, "behind"),
        ]
        for over, needle in cases:
            with self.subTest(over=over):
                ok, why = self.reason(**over)
                self.assertEqual((ok, needle in why), (False, True), why)

    def test_an_incomplete_file_list_is_refused(self):
        ok, why = self.reason(changedFiles=150)
        self.assertEqual((ok, "file list is incomplete (1 of 150" in why), (False, True))
        self.assertIn("incomplete", self.reason(changedFiles=None)[1])

    def test_every_expected_workflow_must_have_reported(self):
        # A pins pull request changing scripts needs build and plan-gates; build alone is not enough.
        ok, why = self.reason(author={"login": "app/github-actions"}, headRefName="pins/x", labels=[{"name": "pins"}],
                              files=[{"path": "scripts/check-local-tools.py"}])
        self.assertEqual((ok, "workflow plan-gates has not reported" in why), (False, True))
        both = [{"__typename": "CheckRun", "name": n, "status": "COMPLETED", "conclusion": "SUCCESS", "workflowName": w}
                for n, w in (("build-windows", "build"), ("plan-gates", "plan-gates"))]
        self.assertTrue(self.reason(files=[{"path": "scripts/x.py"}], statusCheckRollup=both)[0])

    def test_the_expected_workflows_follow_the_path_filters(self):
        self.assertEqual(mp.expected_workflows(REPO, ["Directory.Packages.props"]), ["build"])
        self.assertEqual(mp.expected_workflows(REPO, ["todo/README.md"]), ["build", "plan-gates"])

    def test_skipped_and_neutral_checks_pass(self):
        rollup = [{"__typename": "CheckRun", "name": "a", "status": "COMPLETED", "conclusion": "SKIPPED",
                   "workflowName": "build"},
                  {"__typename": "CheckRun", "name": "b", "status": "COMPLETED", "conclusion": "NEUTRAL"},
                  {"__typename": "StatusContext", "context": "c", "state": "SUCCESS"}]
        self.assertTrue(self.reason(statusCheckRollup=rollup)[0])


class MergeTests(Base):
    def test_one_merge_per_run_oldest_first_with_the_exact_call(self):
        gh, git = FakeGh([pr(2), pr(1)]), FakeGit()
        code, out = self.call(["run", "--campaign"], gh, git)
        self.assertEqual(code, 0)
        self.assertEqual(gh.merges(), [("pr", "merge", "1", "--repo", "github.com/rizonesoft/Isotone", "--rebase",
                                        "--delete-branch", "--match-head-commit", f"{1:040d}")])
        listing = [c for c in gh.calls if c[:2] == ("pr", "list")][0]
        self.assertEqual(listing[2:4], ("--repo", "github.com/rizonesoft/Isotone"))
        self.assertIn(("pull", "--ff-only", "origin", "main"), git.calls)
        self.assertIn("merged #1", out)

    def test_nothing_eligible_merges_nothing_and_says_why(self):
        gh = FakeGh([pr(1, mergeable="CONFLICTING")])
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "nothing eligible; #1 mergeable is conflicting" in out), (0, [], True))

    def test_a_refused_merge_stops_and_leaves_the_rest(self):
        gh = FakeGh([pr(1), pr(2)], merge_fails=True)
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges()), "#1 not merged" in out), (1, 1, True))

    def test_a_failed_pull_after_a_merge_is_its_own_outcome(self):
        code, out = self.call(["run", "--campaign"], FakeGh([pr(1)]), FakeGit(pull_fails=True))
        self.assertEqual((code, "MERGED on GitHub, but the pull failed" in out, "reconcile" in out,
                          (self.root / mp.BLOCKED).exists()), (3, True, True, True))

    def test_a_red_validate_after_a_merge_is_its_own_outcome(self):
        red = lambda r: subprocess.CompletedProcess([], 1, "1 fatal\n", "")
        code, out = self.call(["run", "--campaign"], FakeGh([pr(1)]), FakeGit(), validate=red)
        self.assertEqual((code, "validate is red on main" in out), (3, True))

    def test_every_github_call_names_the_origin_repository(self):
        gh = FakeGh([pr(1)])
        self.call(["run", "--campaign"], gh, FakeGit(origin="git@github.com:someone/Fork.git"))
        self.assertTrue(gh.calls and all("--repo" in c and c[c.index("--repo") + 1] == "github.com/someone/Fork" for c in gh.calls))

    def test_an_origin_that_is_not_github_fails(self):
        for origin in ("https://example.com/x.git", "https://notgithub.com/rizonesoft/Isotone.git",
                       "https://github.example.com/rizonesoft/Isotone.git", "git@ghe.corp:rizonesoft/Isotone.git"):
            with self.subTest(origin=origin):
                gh = FakeGh([pr(1)])
                code, out = self.call(["run", "--campaign"], gh, FakeGit(origin=origin))
                self.assertEqual((code, "is not a GitHub repository" in out, gh.merges()), (1, True, []))

    def test_a_merge_error_after_the_merge_landed_carries_on_to_reconcile(self):
        gh, git = FakeGh([pr(1)], merge_fails=True, lands=True), FakeGit()
        code, out = self.call(["run", "--campaign"], gh, git)
        self.assertEqual((code, ("pull", "--ff-only", "origin", "main") in git.calls, "merged #1" in out), (0, True, True))

    def test_a_merge_error_with_an_unreadable_state_blocks(self):
        gh = FakeGh([pr(1)], merge_fails=True)
        real = gh.__call__

        def view_fails_after_merge(*args, cwd=None):
            if args[:2] == ("pr", "view") and gh.merges():
                raise mp.Failed("gh pr view failed: connection reset")
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--campaign"], view_fails_after_merge, FakeGit())
        self.assertEqual((code, "outcome is unknown" in out), (3, True))

    def test_a_base_retargeted_since_the_listing_is_refused(self):
        gh = FakeGh([pr(1)], retarget="release")
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "changed since it was read: targets release" in out), (1, [], True))

    def test_a_merge_that_landed_elsewhere_or_off_main_blocks(self):
        for kind in ("elsewhere", "off_main"):
            with self.subTest(kind=kind):
                code, out = self.call(["run", "--campaign"], FakeGh([pr(1)], **{kind: True}), FakeGit())
                self.assertEqual((code, "did not land on main" in out), (3, True))
                (self.root / mp.BLOCKED).unlink()

    def test_the_final_reread_rechecks_eligibility(self):
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def label_removed(*args, cwd=None):
            out = real(*args, cwd=cwd)
            if args[:2] == ("pr", "view"):
                return json.dumps(dict(json.loads(out), labels=[]))
            return out
        code, out = self.call(["run", "--campaign"], label_removed, FakeGit())
        self.assertEqual((code, gh.merges(), "neither dependencies nor pins" in out), (1, [], True))

    def test_the_intent_is_recorded_before_the_merge_is_issued(self):
        seen = []
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def watch(*args, cwd=None):
            if args[:2] == ("pr", "merge"):
                seen.append((self.root / mp.BLOCKED).exists())
            return real(*args, cwd=cwd)
        code, _out = self.call(["run", "--campaign"], watch, FakeGit())
        self.assertEqual((code, seen, (self.root / mp.BLOCKED).exists()), (0, [True], False))

    def test_an_open_intent_settles_before_it_clears(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        gh = FakeGh([pr(1), pr(2)])
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, "may be in flight" in out, gh.merges(), (self.root / mp.BLOCKED).exists()),
                         (0, True, [], True))
        record = json.loads((self.root / mp.BLOCKED).read_text(encoding="utf-8"))
        record["issued_at"] -= mp.SETTLE_SECONDS + 1
        (self.root / mp.BLOCKED).write_text(json.dumps(record), encoding="utf-8")
        gh = FakeGh([pr(1), pr(2)])
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges())), (0, 1))

    def test_a_record_left_by_a_killed_run_blocks_until_github_shows_it_resolved(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        # the merge landed elsewhere: stays blocked even though validate is green
        code, out = self.call(["run", "--task"], FakeGh([pr(1), pr(2)], already_merged=[1], elsewhere=True), FakeGit())
        self.assertEqual((code, "did not land on main" in out, (self.root / mp.BLOCKED).exists()), (3, True, True))
        # the merge never happened and the record has settled: it clears and the run goes on
        record = json.loads((self.root / mp.BLOCKED).read_text(encoding="utf-8"))
        record["issued_at"] -= mp.SETTLE_SECONDS + 1
        (self.root / mp.BLOCKED).write_text(json.dumps(record), encoding="utf-8")
        gh = FakeGh([pr(1), pr(2)])
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges())), (0, 1))

    def test_a_record_with_an_unlevel_clone_alerts_instead_of_refusing_quietly(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        code, out = self.call(["run", "--task"], FakeGh([pr(1)], already_merged=[1]), FakeGit(remote="b" * 40))
        self.assertEqual((code, "not level" in out), (3, True))

    def test_a_failure_after_the_merge_is_exit_three(self):
        git = FakeGit()
        real = git.__call__

        def head_fails(*args, cwd=None):
            if args[:2] == ("rev-parse", "HEAD") and any(c[0] == "pull" for c in git.calls):
                raise mp.Failed("git rev-parse HEAD failed")
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--campaign"], FakeGh([pr(1)]), head_fails)
        self.assertEqual((code, (self.root / mp.BLOCKED).exists()), (3, True))

    def test_recovery_judges_the_committed_main_not_an_uncommitted_repair(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        gh = FakeGh([pr(1), pr(2)], already_merged=[1])
        code, out = self.call(["run", "--task"], gh, FakeGit(status=" M repaired.md\n"))
        self.assertEqual((code, "uncommitted changes" in out, gh.merges(), (self.root / mp.BLOCKED).exists()),
                         (3, True, [], True))

    def test_a_malformed_record_blocks_until_the_operator_clears_it(self):
        (self.root / "build").mkdir(exist_ok=True)
        for body in ("{truncated", "[]", '{"why": "no pr"}'):
            with self.subTest(body=body):
                (self.root / mp.BLOCKED).write_text(body, encoding="utf-8")
                gh = FakeGh([pr(2)])
                code, out = self.call(["run", "--task"], gh, FakeGit())
                self.assertEqual((code, gh.merges(), "delete the record" in out), (3, [], True))

    def test_an_os_error_after_the_merge_is_exit_three(self):
        git = FakeGit()
        real = git.__call__

        def denied(*args, cwd=None):
            if args[0] == "pull":
                raise PermissionError("access denied")
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--campaign"], FakeGh([pr(1)]), denied)
        self.assertEqual((code, "access denied" in out, (self.root / mp.BLOCKED).exists()), (3, True, True))

    def test_the_task_never_touches_a_running_campaigns_intent(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        gh = FakeGh([pr(1), pr(2)])
        code, out = self.call(["run", "--task"], gh, FakeGit(), active=lambda r: "a campaign run holds the guard")
        self.assertEqual((code, (self.root / mp.BLOCKED).exists(), [c for c in gh.calls if c[:2] == ("pr", "view")]),
                         (0, True, []))

    def test_a_failed_recovery_is_exit_three(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        git = FakeGit()
        real = git.__call__

        def origin_fails(*args, cwd=None):
            if args[:2] == ("remote", "get-url"):
                raise mp.Failed("git remote get-url origin failed")
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], FakeGh([pr(1)], already_merged=[1]), origin_fails)
        self.assertEqual((code, "recovery failed" in out), (3, True))

    def test_the_real_merge_lock_allows_one_run_at_a_time(self):
        with mp.merge_lock(self.root):
            with self.assertRaises(mp.Refused):
                with mp.merge_lock(self.root):
                    pass
        with mp.merge_lock(self.root):
            pass

    def test_an_origin_with_credentials_is_redacted(self):
        code, out = self.call(["run", "--campaign"], FakeGh([pr(1)]),
                              FakeGit(origin="https://user:FAKE_SECRET@example.com/owner/repo.git"))
        self.assertEqual((code, "FAKE_SECRET" in out, "***@example.com" in out), (1, False, True))

    def test_the_fetch_names_its_destination(self):
        git = FakeGit()
        self.call(["run", "--campaign"], FakeGh([pr(1)]), git)
        self.assertIn(("fetch", "--quiet", "origin", "+refs/heads/main:refs/remotes/origin/main"), git.calls)

    def test_a_red_main_after_a_merge_blocks_every_later_merge_until_it_validates(self):
        red = lambda r: subprocess.CompletedProcess([], 1, "1 fatal\n", "")
        code, _out = self.call(["run", "--campaign"], FakeGh([pr(1), pr(2)]), FakeGit(), validate=red)
        self.assertEqual((code, (self.root / mp.BLOCKED).exists()), (3, True))
        gh = FakeGh([pr(1), pr(2)], already_merged=[1])
        code, out = self.call(["run", "--task"], gh, FakeGit(), validate=red)
        self.assertEqual((code, gh.merges(), "left main red" in out), (3, [], True))
        gh = FakeGh([pr(1), pr(2)], already_merged=[1])
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges()), (self.root / mp.BLOCKED).exists()), (0, 1, False))


class RealTreeTests(unittest.TestCase):
    def test_the_real_tree_reads_its_sections_without_error(self):
        self.assertIsInstance(mp.sections_in_progress(REPO), list)


if __name__ == "__main__":
    unittest.main()
