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
        "files": [{"path": "Directory.Packages.props", "changeType": "MODIFIED"}], "changedFiles": 1, "createdAt": f"2026-10-2{number}T00:00:00Z",
    }
    base.update(over)
    return base


class FakeGit:
    def __init__(self, status="", head=HEAD, remote=HEAD, pull_fails=False, branch="refs/heads/main",
                 fetch_fails=False, origin="https://github.com/rizonesoft/Isotone.git", detached=False, broken=False,
                 changed=()):
        self.calls, self.status, self.head, self.remote, self.pull_fails = [], status, head, remote, pull_fails
        self.branch, self.fetch_fails, self.origin = branch, fetch_fails, origin
        # `symbolic-ref -q HEAD` fails both on a detached HEAD and in a broken repository; `rev-parse --verify`
        # tells them apart.
        self.detached, self.broken = detached, broken
        # What `git diff --name-only <a> <b>` lists.
        self.changed = list(changed)

    def __call__(self, *args, cwd=None):
        self.calls.append(args)
        if args[0] == "symbolic-ref":
            if self.detached or self.broken:
                raise mp.Failed("git symbolic-ref -q HEAD failed: ", 1 if self.detached else 128)
            return self.branch + "\n"
        if args[:2] == ("diff", "--name-only"):
            assert "-z" in args and "--no-renames" in args, args
            return "".join(f + "\0" for f in self.changed)
        if args[:2] == ("rev-parse", "--verify") and self.broken:
            raise mp.Failed("git rev-parse --verify -q HEAD failed: not a git repository")
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
                 off_main=False, already_merged=(), unknown_views=0, pending_field="mergeable", runs=None,
                 main_runs=None):
        self.calls, self.prs = [], prs
        self.merge_fails, self.lands, self.view_fails = merge_fails, lands, view_fails
        self.retarget, self.elsewhere, self.off_main = retarget, elsewhere, off_main
        self.merged = {str(n) for n in already_merged}
        self.views: dict[str, int] = {}
        # GitHub's lazy mergeability: the first `unknown_views` reads of each pull request answer UNKNOWN.
        self.unknown_views, self.pending_field, self.runs = unknown_views, pending_field, runs
        # main's newest push run per workflow file; green unless a test says otherwise.
        self.main_runs = main_runs or {}

    def _pr(self, n):
        return next(p for p in self.prs if str(p["number"]) == str(n))

    def __call__(self, *args, cwd=None):
        self.calls.append(args)
        if args[:2] == ("pr", "list"):
            # Like GitHub: filter by label first, then keep the newest `--limit`.
            found = [p for p in self.prs if str(p["number"]) not in self.merged]
            if "--label" in args:
                label = args[args.index("--label") + 1]
                found = [p for p in found if label in {l.get("name") for l in p.get("labels") or []}]
            found.sort(key=lambda p: p.get("createdAt", ""), reverse=True)
            return json.dumps(found[:int(args[args.index("--limit") + 1])] if "--limit" in args else found)
        if args[:2] == ("pr", "view"):
            if self.view_fails:
                raise mp.Failed("gh pr view failed: connection reset")
            p = self._pr(args[2])
            self.views[args[2]] = self.views.get(args[2], 0) + 1
            merged = args[2] in self.merged
            # A retarget lands between the listing (first read) and the final re-read.
            retargeted = self.retarget if self.views[args[2]] >= 2 else None
            base = retargeted or ("release" if merged and self.elsewhere else p["baseRefName"])
            limit = (self.unknown_views.get(args[2], 0) if isinstance(self.unknown_views, dict) else self.unknown_views)
            pending = {self.pending_field: "UNKNOWN"} if self.views[args[2]] <= limit else {}
            return json.dumps(dict(p, baseRefName=base, state="MERGED" if merged else "OPEN", **pending,
                                   mergeCommit={"oid": ("f" if self.off_main else "c") * 40} if merged else None))
        if args[:2] == ("run", "list") and "--branch" in args:
            wf = args[args.index("--workflow") + 1]
            return json.dumps(self.main_runs.get(wf, [{"status": "completed", "conclusion": "success",
                                                       "url": f"https://example.invalid/{wf}", "headSha": HEAD}]))
        if args[:2] == ("run", "list") and self.runs is not None:
            return json.dumps(self.runs.get(args[args.index("--commit") + 1], []))
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
        self._wait, mp.MERGEABLE_WAIT = mp.MERGEABLE_WAIT, 0

    def tearDown(self):
        mp.MERGEABLE_WAIT = self._wait
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

    def test_a_rename_or_copy_is_refused(self):
        for kind in ("RENAMED", "COPIED"):
            with self.subTest(kind=kind):
                ok, why = self.reason(files=[{"path": "old-global.json", "changeType": kind}])
                self.assertEqual((ok, "renames or copies" in why), (False, True))

    def test_every_expected_workflow_must_have_reported(self):
        # A pins pull request changing scripts needs build and plan-gates; build alone is not enough.
        ok, why = self.reason(author={"login": "app/github-actions"}, headRefName="pins/x", labels=[{"name": "pins"}],
                              files=[{"path": "scripts/check-local-tools.py", "changeType": "MODIFIED"}])
        self.assertEqual((ok, "workflow plan-gates has not reported" in why), (False, True))
        both = [{"__typename": "CheckRun", "name": n, "status": "COMPLETED", "conclusion": "SUCCESS", "workflowName": w}
                for n, w in (("build-windows", "build"), ("plan-gates", "plan-gates"))]
        self.assertTrue(self.reason(files=[{"path": "scripts/x.py", "changeType": "MODIFIED"}], statusCheckRollup=both)[0])

    def test_every_expected_workflow_run_must_have_completed_green(self):
        p = pr(files=[{"path": "scripts/x.py", "changeType": "MODIFIED"}])
        def runs(*items):
            return lambda *a, cwd=None: json.dumps([{"workflowName": w, "status": s, "conclusion": c, "createdAt": at}
                                                    for w, s, c, at in items])
        cases = [
            (runs(("build", "completed", "success", "1")), False, "plan-gates has no run"),
            (runs(("build", "completed", "success", "1"), ("plan-gates", "in_progress", "", "1")), False, "in_progress"),
            (runs(("build", "completed", "success", "1"), ("plan-gates", "completed", "failure", "1")), False, "failure"),
            (runs(("build", "completed", "success", "1"), ("plan-gates", "completed", "failure", "1"),
                  ("plan-gates", "completed", "success", "2")), True, ""),
        ]
        for fake, want, needle in cases:
            with self.subTest(needle=needle):
                ok, why = mp.workflows_green(p, "github.com/rizonesoft/Isotone", REPO, fake)
                self.assertEqual((ok, needle in why), (want, True))

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

    def test_local_checks_follow_the_fetch(self):
        git = FakeGit()
        real = git.__call__

        def switch_during_fetch(*args, cwd=None):
            out = real(*args, cwd=cwd)
            if args[0] == "fetch":
                git.branch, git.status = "refs/heads/work", " M x" + chr(10)
            return out
        gh = FakeGh([pr(1)])
        code, out = self.call(["run", "--campaign"], gh, switch_during_fetch)
        self.assertEqual((code, gh.merges(), "refs/heads/work" in out), (2, [], True))

    def test_a_failed_workflow_run_lookup_stops_the_run(self):
        gh = FakeGh([pr(1), pr(2)])
        real = gh.__call__
        calls = []

        def runs_fail_once(*args, cwd=None):
            if args[:2] == ("run", "list") and "--commit" in args:
                calls.append(args)
                if len(calls) == 1:
                    raise mp.Failed("gh run list failed: connection reset")
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], runs_fail_once, FakeGit())
        self.assertEqual((code, gh.merges(), "cannot read the pull requests or their workflow runs" in out), (1, [], True))

    def test_a_mergeability_still_being_computed_is_read_again(self):
        # D00-T01-S12-F43: right after a stamp push GitHub answers UNKNOWN until its computation finishes.
        gh = FakeGh([pr(1)], unknown_views=2)
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges())), (0, 1), out)

    def test_a_mergeability_never_computed_stays_refused(self):
        gh = FakeGh([pr(1)], unknown_views=99)
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "mergeable is unknown" in out, gh.views["1"]), (0, [], True, 1 + mp.MERGEABLE_TRIES))

    def test_only_the_pull_request_to_merge_waits_for_mergeability(self):
        # Independent review round 18: pull requests that cannot qualify are read once, whatever their mergeability.
        humans = [pr(n, author={"login": "someone"}, createdAt=f"2026-10-01T00:00:{n:02d}Z") for n in range(3, 28)]
        gh = FakeGh(humans + [pr(1)], unknown_views=1)
        sleeps = []
        saved = mp.time.sleep
        mp.time.sleep = sleeps.append
        try:
            code, out = self.call(["run", "--campaign"], gh, FakeGit())
        finally:
            mp.time.sleep = saved
        self.assertEqual((code, len(gh.merges()), [n for n in range(3, 28) if str(n) in gh.views],
                          len(sleeps) <= 2 * mp.MERGEABLE_TRIES), (0, 1, [], True), out)

    def test_a_merge_state_still_being_computed_is_read_again(self):
        # Independent review round 19: `pending` covers mergeStateStatus as well as mergeable.
        gh = FakeGh([pr(1)], unknown_views=1, pending_field="mergeStateStatus")
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges())), (0, 1), out)

    def test_the_re_read_follows_the_workflow_verdicts(self):
        # Independent review round 19: #1 passes eligibility but its build is red, #2 is still being computed.
        wf = self.root / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "build.yml").write_text("name: build" + chr(10) + "on:" + chr(10) + "  pull_request:" + chr(10), encoding="utf-8")
        run = lambda c: [{"workflowName": "build", "status": "completed", "conclusion": c, "createdAt": "1"}]
        gh = FakeGh([pr(1), pr(2)], unknown_views={"2": 1},
                    runs={pr(1)["headRefOid"]: run("failure"), pr(2)["headRefOid"]: run("success")})
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, [c[2] for c in gh.merges()]), (0, ["2"]), out)

    def test_newer_unlabelled_pull_requests_never_hide_a_bump(self):
        # Independent review round 21: 120 newer human pull requests and one old green Dependabot bump.
        humans = [pr(n, author={"login": "someone"}, labels=[], createdAt=f"2026-10-25T00:{n // 60:02d}:{n % 60:02d}Z")
                  for n in range(10, 130)]
        gh = FakeGh(humans + [pr(1)])
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, [c[2] for c in gh.merges()]), (0, ["1"]), out)

    def test_the_pending_pick_skips_a_red_workflow(self):
        # Independent review round 20: both pending, #1's build red, #2's green: #2 is the one re-read and merged.
        wf = self.root / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "build.yml").write_text("name: build" + chr(10) + "on:" + chr(10) + "  pull_request:" + chr(10), encoding="utf-8")
        run = lambda c: [{"workflowName": "build", "status": "completed", "conclusion": c, "createdAt": "1"}]
        gh = FakeGh([pr(1), pr(2)], unknown_views=1,
                    runs={pr(1)["headRefOid"]: run("failure"), pr(2)["headRefOid"]: run("success")})
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, [c[2] for c in gh.merges()]), (0, ["2"]), out)

    def test_the_reserve_is_checked_again_right_before_the_merge(self):
        import time
        saved = mp._deadline
        mp._deadline = time.monotonic() + mp.MERGE_RESERVE + 60

        def spends_the_budget():
            mp._deadline = time.monotonic() + 1
        gh = FakeGh([pr(1)])
        try:
            code, line = mp.merge_one(pr(1), "github.com/rizonesoft/Isotone", self.root, gh, FakeGit(), ok_validate,
                                      ready_fn=spends_the_budget)
        finally:
            mp._deadline = saved
        self.assertEqual((code, gh.merges(), "time budget" in line, (self.root / mp.BLOCKED).exists()), (1, [], True, False))

    def test_a_spent_budget_issues_no_merge(self):
        saved = mp.RUN_BUDGET
        mp.RUN_BUDGET = mp.MERGE_RESERVE - 1
        try:
            gh = FakeGh([pr(1)])
            code, out = self.call(["run", "--campaign"], gh, FakeGit())
        finally:
            mp.RUN_BUDGET = saved
        self.assertEqual((code, gh.merges(), "time budget" in out, (self.root / mp.BLOCKED).exists()), (1, [], True, False))

    def test_a_red_main_stops_the_run_before_any_merge(self):
        # D00 T01 §15: the newest build run on main failed, so nothing merges and the task's email fires.
        for flags in (["--task"], ["--campaign"]):
            with self.subTest(flags=flags):
                red = {"build.yml": [{"status": "completed", "conclusion": "failure", "url": "https://x/run/9",
                                      "headSha": HEAD}]}
                gh = FakeGh([pr(1)], main_runs=red)
                code, out = self.call(["run", *flags], gh, FakeGit())
                self.assertEqual((code, gh.merges(), "build run concluded failure: https://x/run/9" in out),
                                 (1, [], True))

    def test_a_red_main_is_reported_with_nothing_eligible(self):
        # D00 T01 §15: the hourly task reads main's CI on every run, so its own red merge surfaces on the next one.
        red = {"plan.yml": [{"status": "completed", "conclusion": "failure", "url": "https://x/run/8", "headSha": HEAD}]}
        gh = FakeGh([], main_runs=red)
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, "plan-gates run concluded failure" in out), (1, True))

    def test_a_running_main_build_is_a_busy_clone(self):
        running = {"build.yml": [{"status": "in_progress", "conclusion": "", "url": "https://x/run/7", "headSha": HEAD}]}
        for flags, want in ((["--task"], 0), (["--campaign"], 2)):
            with self.subTest(flags=flags):
                gh = FakeGh([pr(1)], main_runs=running)
                code, out = self.call(["run", *flags], gh, FakeGit())
                self.assertEqual((code, gh.merges(), "is in_progress" in out), (want, [], True))

    def test_main_with_no_run_to_read_is_a_failure(self):
        gh = FakeGh([pr(1)], main_runs={"build.yml": []})
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "no build push run" in out), (1, [], True))

    def run_on(self, sha, status="completed", conclusion="success", n=1):
        return [{"status": status, "conclusion": conclusion, "url": f"https://x/run/{n}", "headSha": sha,
                 "createdAt": f"2026-10-22T00:00:{n:02d}Z"}]

    def test_a_build_on_an_older_commit_does_not_clear_head(self):
        # Independent review round 1: main's head has no build yet, only an older commit does.
        gh = FakeGh([pr(1)], main_runs={"build.yml": self.run_on("b" * 40)})
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "has not started yet" in out), (2, [], True))

    def test_an_older_plan_gates_run_counts_only_when_the_changes_miss_its_paths(self):
        wf = self.root / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "plan.yml").write_text("name: plan-gates" + chr(10) + "on:" + chr(10) + "  push:" + chr(10)
                                     + "    paths:" + chr(10) + "      - 'todo/**'" + chr(10), encoding="utf-8")
        runs = {"plan.yml": self.run_on("b" * 40)}
        for changed, want, merges in ((["docs/user/x.md"], 0, 1), (["todo/x.md"], 2, 0)):
            with self.subTest(changed=changed):
                gh = FakeGh([pr(1)], main_runs=runs)
                code, out = self.call(["run", "--campaign"], gh, FakeGit(changed=changed))
                self.assertEqual((code, len(gh.merges())), (want, merges), out)

    def test_a_non_ascii_or_moved_path_still_meets_the_filter(self):
        # Independent review round 2: -z leaves names unquoted, --no-renames lists a move's old side.
        wf = self.root / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "plan.yml").write_text("name: plan-gates" + chr(10) + "on:" + chr(10) + "  push:" + chr(10)
                                     + "    paths:" + chr(10) + "      - 'scripts/**'" + chr(10), encoding="utf-8")
        for changed in (["scripts/caf" + chr(233) + ".py"], ["archive/check.py", "scripts/check.py"]):
            with self.subTest(changed=changed):
                gh = FakeGh([pr(1)], main_runs={"plan.yml": self.run_on("b" * 40)})
                code, out = self.call(["run", "--campaign"], gh, FakeGit(changed=changed))
                self.assertEqual((code, gh.merges()), (2, []), out)

    def test_the_clone_is_judged_after_main_ci_at_the_merge(self):
        # Independent review round 2: a checkout detached during the final CI read never reaches the merge.
        git = FakeGit()
        gh = FakeGh([pr(1)])
        real = gh.__call__
        reads = []

        def detach_on_final_ci(*args, cwd=None):
            if args[:2] == ("run", "list") and "--branch" in args:
                reads.append(args)
                if len(reads) > len(mp.MAIN_WORKFLOWS):
                    git.detached = True
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], detach_on_final_ci, git)
        self.assertEqual((code, gh.merges(), "a detached HEAD" in out), (0, [], True))

    def test_main_moving_while_its_ci_is_read_refuses_the_merge(self):
        git = FakeGit()
        gh = FakeGh([pr(1)])
        real = gh.__call__
        reads = []

        def advance_on_final_ci(*args, cwd=None):
            out = real(*args, cwd=cwd)
            if args[:2] == ("run", "list") and "--branch" in args:
                reads.append(args)
                if len(reads) == 2 * len(mp.MAIN_WORKFLOWS):
                    git.head = git.remote = "e" * 40
            return out
        code, out = self.call(["run", "--campaign"], advance_on_final_ci, git)
        self.assertEqual((code, gh.merges(), "main moved" in out), (2, [], True))

    def test_the_trigger_reader_answers_cautiously(self):
        # Independent review round 3: a flow sequence is read, and what cannot be read counts as every change.
        on = "name: x" + chr(10) + "on:" + chr(10) + "  push:" + chr(10)
        cases = [
            (on + "    paths: ['scripts/**', \"todo/**\"]" + chr(10), (True, ["scripts/**", "todo/**"])),
            (on + "    paths:" + chr(10) + "      - 'scripts/**'" + chr(10), (True, ["scripts/**"])),
            (on + "    paths: []" + chr(10), (True, None)),
            (on + "    paths: scripts/**" + chr(10), (True, None)),
            (on + "    paths:" + chr(10) + "      - 'scripts/**'" + chr(10) + "      - '!scripts/x'" + chr(10), (True, None)),
            ("name: x" + chr(10) + "on: [push, pull_request]" + chr(10), (True, None)),
            ("name: x" + chr(10) + "on: workflow_dispatch" + chr(10), (False, None)),
            ("name: x" + chr(10) + "on:" + chr(10) + "  workflow_dispatch:" + chr(10) + "jobs:" + chr(10)
             + "  push:" + chr(10) + "    runs-on: x" + chr(10), (False, None)),
            # Independent review round 4: a column-0 comment never ends the block, and one unreadable entry voids
            # the whole filter.
            ("on:" + chr(10) + "  workflow_dispatch:" + chr(10) + "# CI on pushes" + chr(10) + "  push:" + chr(10)
             + "    paths:" + chr(10) + "      - 'scripts/**'" + chr(10), (True, ["scripts/**"])),
            # A trailing comment is a comment: the whole filter is read, never part of it.
            (on + "    paths:" + chr(10) + "      - 'scripts/**'" + chr(10) + "      - 'todo/**' # plans" + chr(10),
             (True, ["scripts/**", "todo/**"])),
            (on + "    paths-ignore:" + chr(10) + "      - 'docs/**'" + chr(10), (True, None)),
            (on + "    paths: ['scripts/**', todo/** extra]" + chr(10), (True, None)),
            ("on:" + chr(10) + "  push: {}" + chr(10), (True, None)),
            (on + "    branches: [main]" + chr(10), (True, None)),
            # Independent review round 5: glob syntax `_glob_re` does not implement voids the filter.
            (on + "    paths: ['scripts/[a-z]*.py']" + chr(10), (True, None)),
            (on + "    paths: ['scripts/**/*.py']" + chr(10), (True, None)),
            (on + "    paths: ['*.jsx?']" + chr(10), (True, None)),
            (on + "    paths: ['docs/*.md', '.gitattributes', '**']" + chr(10), (True, ["docs/*.md", ".gitattributes", "**"])),
            # Independent review round 6: YAML aliases and anchors are outside the whitelist, so the block is unsure.
            ("env: {FILTER: &filter 'scripts/**'}" + chr(10) + on + "    paths: [*filter]" + chr(10), (True, None)),
            ("on: &triggers" + chr(10) + "  pull_request:" + chr(10) + "    branches: [main]" + chr(10), (True, None)),
            (on + "    paths:" + chr(10) + "      - *filter" + chr(10), (True, None)),
            # Independent review round 7: "does not run" only from a block read in full.
            (chr(0xFEFF) + "on:" + chr(10) + "  push:" + chr(10) + "    paths: ['scripts/**']" + chr(10), (True, ["scripts/**"])),
            ("on:" + chr(10) + "- push" + chr(10) + "- pull_request" + chr(10), (True, None)),
            ("name: x" + chr(10) + "jobs:" + chr(10) + "  a:" + chr(10) + "    runs-on: x" + chr(10), (True, None)),
            ("on:" + chr(10) + "  pull_request:" + chr(10), (False, None)),
            # The whitelist covers the whole block: a line it does not know, even under another event, voids it.
            ("on:" + chr(10) + "  pull_request:" + chr(10) + "    types: !!seq [opened]" + chr(10) + "  push:" + chr(10)
             + "    paths: ['scripts/**']" + chr(10), (True, None)),
            ("on:" + chr(10) + "  schedule:" + chr(10) + "    - cron: '3 4 * * *'" + chr(10) + "  push:" + chr(10)
             + "    branches: [main]" + chr(10) + "    paths: ['scripts/**']" + chr(10), (True, ["scripts/**"])),
        ]
        for text, want in cases:
            with self.subTest(text=text):
                self.assertEqual(mp._trigger(text, "push"), want)

    def test_a_red_from_a_checkout_that_left_main_is_a_quiet_refusal(self):
        # Independent review round 3: detached onto a commit whose runs failed while the pull requests were read.
        git = FakeGit()
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def detach_onto_red(*args, cwd=None):
            if args[:2] == ("pr", "list"):
                git.detached = True
                gh.main_runs = {"build.yml": self.run_on(HEAD, conclusion="failure", n=6)}
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], detach_onto_red, git)
        self.assertEqual((code, gh.merges(), "a detached HEAD" in out), (0, [], True))

    def test_a_red_read_at_the_start_waits_for_the_clone_too(self):
        # Independent review round 4: detached while the first CI read finds red: a busy clone, no email.
        git = FakeGit()
        gh = FakeGh([pr(1)], main_runs={"build.yml": self.run_on(HEAD, conclusion="failure", n=4)})
        real = gh.__call__

        def detach_on_ci(*args, cwd=None):
            if args[:2] == ("run", "list") and "--branch" in args:
                git.detached = True
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], detach_on_ci, git)
        self.assertEqual((code, gh.merges(), "a detached HEAD" in out), (0, [], True))

    def test_main_ci_is_read_again_right_before_the_merge(self):
        # Independent review round 1: main turns red while the pull requests are read.
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def red_after_listing(*args, cwd=None):
            if args[:2] == ("pr", "list"):
                gh.main_runs = {"build.yml": self.run_on(HEAD, conclusion="failure", n=5)}
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--campaign"], red_after_listing, FakeGit())
        self.assertEqual((code, gh.merges(), "concluded failure" in out), (1, [], True))

    def test_a_checkout_detached_before_the_final_preflight_stays_quiet(self):
        git = FakeGit()
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def detach_on_list(*args, cwd=None):
            if args[:2] == ("pr", "list"):
                git.detached = True
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], detach_on_list, git)
        self.assertEqual((code, gh.merges(), "a detached HEAD" in out), (0, [], True))

    def test_a_red_build_outranks_a_running_plan_gates(self):
        runs = {"plan.yml": self.run_on(HEAD, status="in_progress", conclusion=""),
                "build.yml": self.run_on(HEAD, conclusion="failure", n=2)}
        gh = FakeGh([pr(1)], main_runs=runs)
        code, out = self.call(["run", "--task"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "build run concluded failure" in out), (1, [], True))

    def test_a_detached_checkout_is_a_quiet_refusal(self):
        # D00-T01-S12-F44: a detached HEAD is a busy clone, never a failure email.
        for flags, want in ((["--task"], 0), (["--campaign"], 2)):
            with self.subTest(flags=flags):
                gh = FakeGh([pr(1)])
                code, out = self.call(["run", *flags], gh, FakeGit(detached=True))
                self.assertEqual((code, gh.merges(), "a detached HEAD" in out), (want, [], True))

    def test_a_symbolic_ref_timeout_is_not_a_detached_head(self):
        # Independent review round 6: only symbolic-ref's own exit 1 means detached; a timeout stays a failure.
        def timed_out(*args, cwd=None):
            if args[0] == "symbolic-ref":
                raise mp.Failed("git symbolic-ref -q HEAD failed: timed out after 300s", 124)
            return FakeGit()(*args, cwd=cwd)
        gh = FakeGh([pr(1)])
        code, out = self.call(["run", "--task"], gh, timed_out)
        self.assertEqual((code, gh.merges()), (1, []))

    def test_a_broken_repository_is_still_a_failure(self):
        gh = FakeGh([pr(1)])
        code, out = self.call(["run", "--task"], gh, FakeGit(broken=True))
        self.assertEqual((code, gh.merges()), (1, []))

    def test_recover_settles_and_never_merges(self):
        gh = FakeGh([pr(1)])
        code, out = self.call(["recover"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), "no unresolved merge" in out), (0, [], True))
        mp._block(self.root, 1, "merge issued, not yet verified")
        code, out = self.call(["recover"], FakeGh([pr(1)], already_merged=[1]), FakeGit())
        self.assertEqual((code, (self.root / mp.BLOCKED).exists()), (0, False))
        mp._block(self.root, 2, "merge issued, not yet verified")
        gh = FakeGh([pr(2), pr(3)])
        code, out = self.call(["recover"], gh, FakeGit())
        self.assertEqual((code, gh.merges(), (self.root / mp.BLOCKED).exists()), (3, [], True))

    def test_a_tree_dirtied_while_github_is_read_refuses_the_merge(self):
        git = FakeGit()
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def dirty_on_list(*args, cwd=None):
            if args[:2] == ("pr", "list"):
                git.status = " M src/edit.cs\n"
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--campaign"], dirty_on_list, git)
        # A busy clone at the final preflight stays a busy clone (exit 2 here), never a failure (D00 T01 §15).
        self.assertEqual((code, gh.merges(), "uncommitted changes" in out,
                          (self.root / mp.BLOCKED).exists()), (2, [], True, False))

    def test_a_tree_dirtied_during_the_merge_skips_the_pull_and_holds(self):
        git = FakeGit()
        gh = FakeGh([pr(1)])
        real = gh.__call__

        def dirty_on_merge(*args, cwd=None):
            out = real(*args, cwd=cwd)
            if args[:2] == ("pr", "merge"):
                git.status = " M src/edit.cs\n"
            return out
        code, out = self.call(["run", "--campaign"], dirty_on_merge, git)
        self.assertEqual((code, len(gh.merges()), [c for c in git.calls if c[0] == "pull"],
                          (self.root / mp.BLOCKED).exists()), (3, 1, [], True))

    def test_a_merge_error_that_reads_open_keeps_the_intent_and_stops(self):
        # A refusal and a timeout look the same from here: the request may still land, so it is never "nothing
        # changed" (independent review round 8).
        gh = FakeGh([pr(1), pr(2)], merge_fails=True)
        code, out = self.call(["run", "--campaign"], gh, FakeGit())
        self.assertEqual((code, len(gh.merges()), "may still land" in out, (self.root / mp.BLOCKED).exists()),
                         (3, 1, True, True))

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
            if args[:2] == ("pr", "view") and gh.views.get(args[2], 0) >= 2:
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
                         (3, True, [], True))
        code, _out = self.call(["run", "--campaign"], FakeGh([pr(1), pr(2)]), FakeGit())
        self.assertEqual(code, 3)
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
        for body in ("{truncated", "[]", '{"why": "no pr"}', '{"pr": 1, "issued_at": NaN}', '{"pr": 1, "issued_at": "x"}',
                     '{"pr": 1}', '{"pr": 1, "issued_at": Infinity}', '{"pr": 1, "issued_at": 1' + '0' * 400 + '}',
                     '{"pr": true, "issued_at": 0}'):
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

    def test_a_record_with_a_null_reason_still_recovers_safely(self):
        (self.root / "build").mkdir(exist_ok=True)
        (self.root / mp.BLOCKED).write_text('{"pr": 1, "issued_at": 0, "why": null}', encoding="utf-8")
        code, out = self.call(["run", "--task"], FakeGh([pr(1)], view_fails=True), FakeGit())
        self.assertEqual((code, "cannot be read" in out), (3, True))

    def test_an_unexpected_error_in_recovery_is_exit_three(self):
        mp._block(self.root, 1, "merge issued, not yet verified")
        gh = FakeGh([pr(1)], already_merged=[1])
        real = gh.__call__

        def broken(*args, cwd=None):
            if args[:2] == ("pr", "view"):
                raise TypeError("unexpected")
            return real(*args, cwd=cwd)
        code, out = self.call(["run", "--task"], broken, FakeGit())
        self.assertEqual((code, "TypeError" in out), (3, True))

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


class TimeoutTests(unittest.TestCase):
    def test_the_run_deadline_caps_each_command(self):
        import time
        saved = mp._deadline
        mp._deadline = time.monotonic() + 2
        try:
            start = time.monotonic()
            done = mp._run([sys.executable, "-c", "import time; time.sleep(20)"], REPO)
            took = time.monotonic() - start
            mp._deadline = time.monotonic() - 1
            spent = mp._run([sys.executable, "-c", "print(1)"], REPO)
        finally:
            mp._deadline = saved
        self.assertEqual((done.returncode, took < 15, spent.returncode, "budget is spent" in spent.stderr),
                         (124, True, 124, True), took)

    def test_a_timed_out_command_is_stopped_with_its_children(self):
        import time
        saved = mp.COMMAND_TIMEOUT
        mp.COMMAND_TIMEOUT = 1
        try:
            code = ("import subprocess, sys, time; "
                    "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)']); time.sleep(20)")
            start = time.monotonic()
            done = mp._run([sys.executable, "-c", code], REPO)
            took = time.monotonic() - start
        finally:
            mp.COMMAND_TIMEOUT = saved
        self.assertEqual((done.returncode, took < 15), (124, True), took)


class RealTreeTests(unittest.TestCase):
    def test_the_real_tree_reads_its_sections_without_error(self):
        self.assertIsInstance(mp.sections_in_progress(REPO), list)


if __name__ == "__main__":
    unittest.main()
