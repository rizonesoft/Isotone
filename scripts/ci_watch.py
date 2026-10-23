#!/usr/bin/env python3
"""Report every workflow whose latest completed run on main is red, scheduled runs included.

    python scripts/ci_watch.py              exit 0 when every workflow's latest completed run on main is green
    python scripts/ci_watch.py --json       the same as JSON: {"red": [...], "checked": <n>}
    python scripts/ci_watch.py --self-test  fixtures only; needs no network

A campaign reads back the CI run its own push started (`review-todo-section`), but scheduled and dispatched workflows
(the daily pins job, the nightly fuzz job, the design page) can turn red between pushes with nobody watching. This
script reads the recent runs on `main` with `gh run list`, keeps the newest completed run of each workflow, and names
each one whose conclusion is not `success`, `skipped`, or `neutral`: a red run that a later green run of the same
workflow superseded is not reported. `process-phase` runs it at every section boundary (operator question 2026-10-23,
"During the campaign, are we keeping an eye on CI runs and fixing red runs?"). A failed `gh` call is exit 2, never a
green report. Stdlib only.
"""
import argparse
import json
import subprocess
import sys

GREEN = {"success", "skipped", "neutral"}
FIELDS = "databaseId,workflowName,status,conclusion,createdAt,event,headSha,url"


def red_runs(runs):
    """The newest completed run of each workflow, when it is red, newest first."""
    latest = {}
    for run in sorted(runs, key=lambda r: r["createdAt"], reverse=True):
        if run.get("status") != "completed":
            continue
        latest.setdefault(run["workflowName"], run)
    red = [r for r in latest.values() if r.get("conclusion") not in GREEN]
    return sorted(red, key=lambda r: r["createdAt"], reverse=True), len(latest)


def fetch(limit):
    result = subprocess.run(["gh", "run", "list", "--branch", "main", "--limit", str(limit), "--json", FIELDS],
                            capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh exited {result.returncode}")
    return json.loads(result.stdout)


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
    print(f"ci_watch self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=100, help="How many recent runs on main to read")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    try:
        runs = fetch(args.limit)
    except (RuntimeError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
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
