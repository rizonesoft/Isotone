#!/usr/bin/env python3
"""Report every workflow whose latest completed run on main is red, scheduled runs included, and re-run one on demand.

    python scripts/ci_watch.py                       exit 0 when every active workflow's latest completed run on main
                                                     is green, 1 naming each red one, 2 when the runs cannot be read
    python scripts/ci_watch.py --json                the same as JSON: {"red": [...], "checked": <n>}
    python scripts/ci_watch.py --dispatch <file>     run that workflow on main now (`gh workflow run`) and wait for the
                                                     run it started: exit 0 green, 1 red, 2 unverifiable
    python scripts/ci_watch.py --self-test           fixtures only; needs no network

A campaign reads back the CI run its own push started (`review-todo-section`), but scheduled and dispatched workflows
(the daily pins job, the nightly fuzz job, the design page) can turn red between pushes with nobody watching, and a
repair push does not re-run them. This script lists the active workflows (`gh workflow list`), reads each one's recent
runs on `main` separately (`gh run list --workflow`, so one busy workflow cannot push another's red run out of a shared
limit), keeps the newest completed run of each, and names each one whose conclusion is not `success`, `skipped`, or
`neutral`: a red run that a later green run of the same workflow superseded is not reported. `--dispatch` is how a
repaired scheduled workflow proves itself green. `process-phase` runs both at every section boundary (operator
question 2026-10-23, "During the campaign, are we keeping an eye on CI runs and fixing red runs?"). A failed `gh` call
is exit 2, never a green report. Stdlib only.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import subprocess
import sys
import time

GREEN = {"success", "skipped", "neutral"}
FIELDS = "databaseId,workflowName,status,conclusion,createdAt,event,headSha,url"


def gh(args):
    """Run `gh` with these arguments and return its parsed JSON output (None when it prints nothing)."""
    result = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh {' '.join(args[:2])} exited {result.returncode}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def red_runs(runs):
    """The newest completed run of each workflow, when it is red, newest first; and how many workflows had one."""
    latest = {}
    for run in sorted(runs, key=lambda r: r["createdAt"], reverse=True):
        if run.get("status") != "completed":
            continue
        latest.setdefault(run["workflowName"], run)
    red = [r for r in latest.values() if r.get("conclusion") not in GREEN]
    return sorted(red, key=lambda r: r["createdAt"], reverse=True), len(latest)


def fetch(runner=gh, per_workflow=20):
    """Every active workflow's recent runs on main, read one workflow at a time."""
    runs = []
    for workflow in runner(["workflow", "list", "--json", "id,name,state,path"]) or []:
        if workflow.get("state") != "active":
            continue
        runs += runner(["run", "list", "--workflow", str(workflow["id"]), "--branch", "main",
                        "--limit", str(per_workflow), "--json", FIELDS]) or []
    return runs


def dispatch_and_wait(workflow, runner=gh, now=lambda: datetime.now(timezone.utc), sleep=time.sleep,
                      timeout=3600, poll=20):
    """Start `workflow` on main and wait for the run it started. Returns (exit code, run or reason)."""
    started = now() - timedelta(seconds=60)  # tolerate clock skew between this machine and GitHub
    runner(["workflow", "run", workflow, "--ref", "main"])
    deadline = now() + timedelta(seconds=timeout)
    while now() < deadline:
        runs = runner(["run", "list", "--workflow", workflow, "--branch", "main", "--event", "workflow_dispatch",
                       "--limit", "5", "--json", FIELDS]) or []
        mine = sorted((r for r in runs if datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00")) >= started),
                      key=lambda r: r["createdAt"])
        if mine and mine[0].get("status") == "completed":
            run = mine[0]
            return (0 if run.get("conclusion") in GREEN else 1), run
        sleep(poll)
    return 2, f"no completed workflow_dispatch run of {workflow} within {timeout} s"


def self_test():
    failed = cases = 0

    def check(name, got, want):
        nonlocal failed, cases
        cases += 1
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got!r}, want {want!r}")

    def run(n, wf, when, conclusion, status="completed", event="schedule"):
        return {"databaseId": n, "workflowName": wf, "status": status, "conclusion": conclusion, "createdAt": when,
                "event": event, "headSha": "a" * 40, "url": f"https://example/{n}"}

    runs = [run(1, "pins", "2026-10-20T00:00:00Z", "failure"), run(2, "pins", "2026-10-21T00:00:00Z", "success"),
            run(3, "fuzz", "2026-10-21T01:00:00Z", "failure"), run(4, "fuzz", "2026-10-20T01:00:00Z", "success"),
            run(5, "build", "2026-10-21T02:00:00Z", None, status="in_progress", event="push"),
            run(6, "build", "2026-10-21T01:30:00Z", "success", event="push"),
            run(7, "pages", "2026-10-21T03:00:00Z", "cancelled"), run(8, "plan", "2026-10-21T03:00:00Z", "skipped")]
    red, checked = red_runs(runs)
    check("a red run superseded by a green one is not reported", [r["databaseId"] for r in red], [7, 3])
    check("each workflow is counted once", checked, 5)
    check("an in-progress run does not hide the last completed one", any(r["workflowName"] == "build" for r in red),
          False)
    check("all green reports nothing", red_runs([run(1, "pins", "2026-10-21T00:00:00Z", "success")])[0], [])
    check("timed_out is red", [r["databaseId"] for r in red_runs([run(9, "x", "2026-10-21T00:00:00Z", "timed_out")])[0]],
          [9])

    # Runs are read per workflow: a hundred green build runs cannot push the one red pins run out of view.
    def per_workflow_runner(args):
        if args[:2] == ["workflow", "list"]:
            return [{"id": 1, "name": "build", "state": "active", "path": ".github/workflows/build.yml"},
                    {"id": 2, "name": "pins", "state": "active", "path": ".github/workflows/pins.yml"},
                    {"id": 3, "name": "old", "state": "disabled_manually", "path": ".github/workflows/old.yml"}]
        workflow = args[args.index("--workflow") + 1]
        if workflow == "1":
            return [run(100 + i, "build", f"2026-10-22T{i % 24:02d}:00:00Z", "success", event="push") for i in range(100)]
        if workflow == "2":
            return [run(9, "pins", "2026-10-20T00:00:00Z", "failure")]
        raise AssertionError("a disabled workflow was read")
    red, checked = red_runs(fetch(per_workflow_runner))
    check("a red workflow behind a busy one is still reported", [r["workflowName"] for r in red], ["pins"])
    check("disabled workflows are skipped", checked, 2)

    # --dispatch: start the run, then wait for the run it started, not an older one.
    clock = [datetime(2026, 10, 23, 12, 0, 0, tzinfo=timezone.utc)]

    def fake_now():
        return clock[0]

    def fake_sleep(seconds):
        clock[0] += timedelta(seconds=seconds)

    def dispatcher(outcome):
        polls = [0]

        def runner(args):
            if args[:2] == ["workflow", "run"]:
                return None
            polls[0] += 1
            old = run(1, "pins", "2026-10-22T00:00:00Z", "success", event="workflow_dispatch")
            if polls[0] < 3 or outcome is None:
                return [old]
            return [run(2, "pins", "2026-10-23T12:00:30Z", outcome, event="workflow_dispatch"), old]
        return runner
    check("a dispatched run that goes green exits 0",
          dispatch_and_wait("pins.yml", dispatcher("success"), fake_now, fake_sleep)[0], 0)
    check("a dispatched run that goes red exits 1",
          dispatch_and_wait("pins.yml", dispatcher("failure"), fake_now, fake_sleep)[0], 1)
    check("an older green run never answers for the dispatched one",
          dispatch_and_wait("pins.yml", dispatcher(None), fake_now, fake_sleep, timeout=300)[0], 2)
    print(f"ci_watch self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--per-workflow", type=int, default=20, help="How many recent runs on main to read per workflow")
    parser.add_argument("--dispatch", metavar="WORKFLOW", help="Run this workflow on main and wait for its verdict")
    parser.add_argument("--timeout", type=int, default=3600, help="With --dispatch, seconds to wait for the run")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    try:
        if args.dispatch:
            code, outcome = dispatch_and_wait(args.dispatch, timeout=args.timeout)
            if args.json:
                print(json.dumps({"exit": code, "run": outcome}, indent=2))
            elif code == 2:
                print(f"ci_watch: {outcome}")
            else:
                print(f"{'GREEN' if code == 0 else 'RED'} {outcome['workflowName']} run {outcome['databaseId']}: "
                      f"{outcome['conclusion']} {outcome['url']}")
            return code
        runs = fetch(per_workflow=args.per_workflow)
    except (RuntimeError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}) if args.json else f"ci_watch: could not read runs: {exc}")
        return 2
    red, checked = red_runs(runs)
    if args.json:
        print(json.dumps({"red": red, "checked": checked}, indent=2))
    else:
        for r in red:
            print(f"RED {r['workflowName']} run {r['databaseId']} ({r['event']}, {r['createdAt']}): {r['conclusion']} "
                  f"{r['url']}")
        print(f"ci_watch: {checked} workflow(s) checked, {len(red)} red")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
