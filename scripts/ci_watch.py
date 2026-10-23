#!/usr/bin/env python3
"""Report every workflow whose latest completed run on main is red, scheduled runs included, and re-run one on demand.

    python scripts/ci_watch.py                       exit 0 when every active workflow's latest completed run on main
                                                     is green, 1 naming each red one, 2 when the runs cannot be read
    python scripts/ci_watch.py --json                the same as JSON: {"red": [...], "checked": <n>}
    python scripts/ci_watch.py --dispatch <file> [--field name=value ...]
                                                     run that workflow on main now (`gh workflow run`, with the
                                                     inputs the failed run used) and wait for the run it started:
                                                     exit 0 green, 1 red, 2 unverifiable
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
from urllib.parse import urlsplit
from datetime import datetime, timedelta, timezone
import json
import os
import re
import subprocess
import sys
import time

GREEN = {"success", "skipped", "neutral"}
FIELDS = "databaseId,workflowDatabaseId,workflowName,status,conclusion,createdAt,event,headSha,url"
# The repository every call is bound to comes from origin, never from an inherited GH_REPO.
# owner/name, exactly, as a GitHub path holds it.
REPO_PATH = re.compile(r"^(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$")
# scp-like ssh, the one remote form urlsplit cannot parse.
SCP_REMOTE = re.compile(r"^git@github\.com:(?P<path>[^/?#]+/[^/?#]+)$")
# A pull request run says nothing about main, even from a fork's branch named main. Every other event is kept, so
# no workflow that runs on main (check_suite among them) is silently left out.
PR_EVENTS = {"pull_request", "pull_request_target", "pull_request_review", "pull_request_review_comment"}
# Widening windows per workflow: a red run on main behind many pull request runs is still found.
WINDOWS = (20, 100, 500, 1000)
# More workflows than gh lists by default (50) must never drop one from the watch.
WORKFLOW_LIMIT = "1000"


def origin_repo(url):
    """`github.com/owner/name` from a GitHub remote URL (https, ssh, or scp-like), or None. The URL is parsed, not
    pattern-matched, so a look-alike host, a host hidden behind `#@` or `?@`, or a path that merely contains
    github.com never names a repository; the host is named in the result because a hostless `--repo` resolves against
    GH_HOST or gh's default host."""
    url = (url or "").strip()
    scp = SCP_REMOTE.match(url)
    if scp:
        path = scp.group("path")
    else:
        try:
            parts = urlsplit(url)
            host = parts.hostname
        except ValueError:
            return None
        if parts.scheme not in ("https", "ssh") or host != "github.com" or parts.query or parts.fragment \
                or (parts.port not in (None, 443, 22)):
            return None
        path = parts.path.lstrip("/")
    match = REPO_PATH.match(path)
    return f"github.com/{match.group('repo')}" if match else None


def gh_command(args, repo):
    """The argv and environment for one `gh` call bound to `repo`: `--repo` on the command, and an inherited GH_REPO
    and GH_HOST removed, so neither monitoring nor a repair dispatch can reach another repository or server."""
    env = {k: v for k, v in os.environ.items() if k not in ("GH_REPO", "GH_HOST")}
    return ["gh", *args, "--repo", repo], env


def bound(repo):
    """A runner for `fetch` and `dispatch_and_wait` whose every `gh` call names `repo`."""
    return lambda args: gh(args, repo)


def gh(args, repo):
    """Run `gh` bound to `repo` and return its stdout as text; each caller parses what it expects."""
    argv, env = gh_command(args, repo)
    result = subprocess.run(argv, capture_output=True, text=True, timeout=120, env=env)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh {' '.join(args[:2])} exited {result.returncode}")
    return result.stdout


def gh_json(runner, args):
    text = runner(args)
    return json.loads(text) if text and text.strip() else None


def red_runs(runs):
    """The newest completed run of each workflow, when it is red, newest first; and how many workflows had one."""
    latest = {}
    for run in sorted(runs, key=lambda r: r["createdAt"], reverse=True):
        if run.get("status") != "completed" or run.get("event") in PR_EVENTS:
            continue
        # Keyed by the workflow's identity: two workflows may share a display name.
        latest.setdefault(run.get("workflowDatabaseId") or run["workflowName"], run)
    red = [r for r in latest.values() if r.get("conclusion") not in GREEN]
    return sorted(red, key=lambda r: r["createdAt"], reverse=True), len(latest)


def fetch(runner, per_workflow=20):
    """Every active workflow's recent completed runs on main, read one workflow at a time. A workflow whose window
    holds no run about main itself (only pull request runs) is read again in a wider window, up to the largest, until
    one is found or its history ends, so pull request runs can never push main's latest run out of view."""
    runs = []
    for workflow in gh_json(runner, ["workflow", "list", "--limit", WORKFLOW_LIMIT, "--json",
                                     "id,name,state,path"]) or []:
        if workflow.get("state") != "active":
            continue
        for window in sorted({max(per_workflow, 1), *WINDOWS}):
            got = gh_json(runner, ["run", "list", "--workflow", str(workflow["id"]), "--branch", "main",
                                   "--status", "completed", "--limit", str(window), "--json", FIELDS]) or []
            if any(r.get("event") not in PR_EVENTS for r in got) or len(got) < window or window == max(WINDOWS):
                runs += got
                break
    return runs


RUN_URL = re.compile(r"/actions/runs/(\d+)")


def dispatch_and_wait(workflow, runner, now=lambda: datetime.now(timezone.utc), sleep=time.sleep,
                      timeout=3600, poll=20, fields=()):
    """Start `workflow` on main with `fields` as its inputs and wait for exactly the run it started.
    Returns (exit code, run or reason).

    The run is the one `gh workflow run` names by URL in its output. When gh names no run (the GitHub CLI can return a
    dispatch without run details), no listed run can be proved to be this one, so the result is unverifiable (exit 2),
    never a guess: an older or a concurrent run can never answer for a repair."""
    args = ["workflow", "run", workflow, "--ref", "main"]
    for field in fields:
        args += ["-f", field]
    output = runner(args) or ""
    match = RUN_URL.search(output)
    if not match:
        return 2, (f"gh did not name the run it started for {workflow}, so the run cannot be identified; "
                   f"use a GitHub CLI that prints the created run's URL")
    run_id = match.group(1)
    deadline = now() + timedelta(seconds=timeout)
    while now() < deadline:
        run = gh_json(runner, ["run", "view", run_id, "--json", FIELDS])
        if run and run.get("status") == "completed":
            # Only success proves a repair: skipped or neutral ran nothing that could fail, and campaign_guard's
            # repair close accepts only success.
            if run.get("conclusion") == "success":
                return 0, run
            if run.get("conclusion") in ("skipped", "neutral"):
                return 2, f"the dispatched run {run_id} of {workflow} ended {run.get('conclusion')}, which proves nothing"
            return 1, run
        sleep(poll)
    return 2, f"the dispatched run {run_id} of {workflow} did not complete within {timeout} s"


def evidence_line(run):
    """The read-back line `campaign_guard.py repair close --evidence` accepts for a dispatched run."""
    return (f"ci-watch: {run['headSha']} {run['workflowName']} {run['conclusion']} run {run['databaseId']} "
            f"{run['url']}")


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
            return json.dumps([{"id": 1, "name": "build", "state": "active", "path": ".github/workflows/build.yml"},
                               {"id": 2, "name": "pins", "state": "active", "path": ".github/workflows/pins.yml"},
                               {"id": 3, "name": "old", "state": "disabled_manually", "path": ".github/workflows/old.yml"}])
        workflow = args[args.index("--workflow") + 1]
        queued = [run(500 + i, "pins" if workflow == "2" else "build", f"2026-10-23T{i % 24:02d}:00:00Z", None,
                      status="queued") for i in range(20)]
        if "--status" not in args or args[args.index("--status") + 1] != "completed":
            # Without the completed filter, twenty newer queued runs fill the limit and hide the red one.
            return json.dumps(queued)
        if workflow == "1":
            return json.dumps([run(100 + i, "build", f"2026-10-22T{i % 24:02d}:00:00Z", "success", event="push")
                               for i in range(100)])
        if workflow == "2":
            return json.dumps([run(9, "pins", "2026-10-20T00:00:00Z", "failure")])
        raise AssertionError("a disabled workflow was read")
    red, checked = red_runs(fetch(per_workflow_runner))
    check("a red workflow behind a busy one is still reported", [r["workflowName"] for r in red], ["pins"])
    check("disabled workflows are skipped", checked, 2)

    # --dispatch waits for exactly the run it started.
    clock = [datetime(2026, 10, 23, 12, 0, 0, tzinfo=timezone.utc)]

    def fake_now():
        return clock[0]

    def fake_sleep(seconds):
        clock[0] += timedelta(seconds=seconds)

    def dispatcher(outcome, prints_url=True, concurrent=False):
        clock[0] = datetime(2026, 10, 23, 12, 0, 0, tzinfo=timezone.utc)  # each case dispatches at 12:00:00
        polls = [0]
        mine = run(77, "pins", "2026-10-23T12:00:30Z", outcome, event="workflow_dispatch")
        older = run(1, "pins", "2026-10-23T11:59:30Z", "success", event="workflow_dispatch")
        other = run(78, "pins", "2026-10-23T12:00:40Z", "success", event="workflow_dispatch")

        def runner(args):
            if args[:2] == ["workflow", "run"]:
                # gh 2.102 prints the created run's URL as plain text, never JSON.
                return "https://github.com/o/r/actions/runs/77\n" if prints_url else ""
            polls[0] += 1
            done = polls[0] >= 3 and outcome is not None
            current = dict(mine, status="completed" if done else "in_progress", conclusion=outcome if done else None)
            if args[:2] == ["run", "view"]:
                if args[2] != "77":
                    raise AssertionError("viewed a run other than the one gh named")
                return json.dumps(current)
            listed = [older, current] + ([other] if concurrent else [])
            return json.dumps(listed)
        return runner
    check("a dispatched run that goes green exits 0",
          dispatch_and_wait("pins.yml", dispatcher("success"), fake_now, fake_sleep)[0], 0)
    check("a dispatched run that goes red exits 1, even beside an earlier green one",
          dispatch_and_wait("pins.yml", dispatcher("failure"), fake_now, fake_sleep)[0], 1)
    check("a run that never completes is unverifiable",
          dispatch_and_wait("pins.yml", dispatcher(None), fake_now, fake_sleep, timeout=300)[0], 2)
    check("with a URL, the named run answers even beside a concurrent one",
          dispatch_and_wait("pins.yml", dispatcher("failure", concurrent=True), fake_now, fake_sleep)[0], 1)
    check("without a URL, no listed run answers: unverifiable, never a guess",
          dispatch_and_wait("pins.yml", dispatcher("success", prints_url=False), fake_now, fake_sleep)[0], 2)
    sent = []

    inner = dispatcher("success")

    def recording(args):
        sent.append(args)
        return inner(args)
    dispatch_and_wait("release.yml", recording, fake_now, fake_sleep, fields=("tag=stilus-v0.1.0-rc.1",))
    check("workflow inputs reach gh workflow run", sent[0][-2:], ["-f", "tag=stilus-v0.1.0-rc.1"])
    green = dispatch_and_wait("pins.yml", dispatcher("success"), fake_now, fake_sleep)[1]
    check("the evidence line is the one campaign_guard repair close accepts",
          evidence_line(green).startswith(f"ci-watch: {'a' * 40} pins success run 77 "), True)
    twins = [dict(run(1, "checks", "2026-10-22T00:00:00Z", "success"), workflowDatabaseId=10),
             dict(run(2, "checks", "2026-10-21T00:00:00Z", "failure"), workflowDatabaseId=11)]
    check("two workflows sharing a name are kept apart", [r["databaseId"] for r in red_runs(twins)[0]], [2])
    check("an https remote names its host and repository", origin_repo("https://github.com/rizonesoft/Isotone.git"),
          "github.com/rizonesoft/Isotone")
    check("an ssh remote names its host and repository", origin_repo("git@github.com:rizonesoft/Isotone.git\n"),
          "github.com/rizonesoft/Isotone")
    check("a remote that is not GitHub names none", origin_repo("https://example.com/a/b.git"), None)
    check("a look-alike host names none", origin_repo("https://notgithub.com/rizonesoft/Isotone.git"), None)
    check("github.com inside another host's path names none",
          origin_repo("https://example.com/github.com/rizonesoft/Isotone.git"), None)
    for spoof in ("https://example.com#@github.com/rizonesoft/Isotone.git",
                  "https://example.com?@github.com/rizonesoft/Isotone.git"):
        check(f"a host hidden behind {spoof[19:21]} names none", origin_repo(spoof), None)
    check("a GitHub URL carrying a fragment names none", origin_repo("https://github.com/rizonesoft/Isotone.git#main"), None)
    check("a check_suite run on main is watched",
          [r["databaseId"] for r in red_runs([run(7, "suite", "2026-10-22T00:00:00Z", "failure", event="check_suite")])[0]],
          [7])

    def pr_flood(args):
        if args[:2] == ["workflow", "list"]:
            return json.dumps([{"id": 1, "name": "build", "state": "active", "path": ".github/workflows/build.yml"}])
        limit = int(args[args.index("--limit") + 1])
        history = [run(100 + i, "build", f"2026-10-22T{i % 24:02d}:{i % 60:02d}:00Z", "success", event="pull_request")
                   for i in range(20)] + [run(1, "build", "2026-10-21T00:00:00Z", "failure", event="push")]
        return json.dumps(history[:limit])
    check("a red push behind twenty pull request runs is still found",
          [r["databaseId"] for r in red_runs(fetch(pr_flood))[0]], [1])
    masked = [run(1, "build", "2026-10-22T00:00:00Z", "failure", event="push"),
              run(2, "build", "2026-10-22T01:00:00Z", "success", event="pull_request")]
    check("a green pull request run never hides a red push on main", [r["databaseId"] for r in red_runs(masked)[0]], [1])
    saved = {k: os.environ.get(k) for k in ("GH_REPO", "GH_HOST")}
    os.environ.update({"GH_REPO": "example/other", "GH_HOST": "github.corp.example"})
    try:
        argv, env = gh_command(["run", "list"], "github.com/rizonesoft/Isotone")
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    check("every gh call names the bound host and repository", argv[-2:], ["--repo", "github.com/rizonesoft/Isotone"])
    check("an inherited GH_REPO never reaches gh", "GH_REPO" in env, False)
    check("an inherited GH_HOST never reaches gh", "GH_HOST" in env, False)

    def many_workflows(args):
        if args[:2] == ["workflow", "list"]:
            limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 50
            flows = [{"id": n, "name": f"w{n}", "state": "active", "path": f".github/workflows/w{n}.yml"}
                     for n in range(1, 52)]
            return json.dumps(flows[:limit])
        workflow = int(args[args.index("--workflow") + 1])
        return json.dumps([dict(run(workflow, f"w{workflow}", "2026-10-22T00:00:00Z",
                                    "failure" if workflow == 51 else "success"), workflowDatabaseId=workflow)])
    red, checked = red_runs(fetch(many_workflows))
    check("a 51st workflow is still watched", ([r["workflowName"] for r in red], checked), (["w51"], 51))
    for ending in ("skipped", "neutral"):
        check(f"a dispatched run that ends {ending} proves nothing",
              dispatch_and_wait("pins.yml", dispatcher(ending), fake_now, fake_sleep)[0], 2)
    print(f"ci_watch self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--per-workflow", type=int, default=20, help="How many recent runs on main to read per workflow")
    parser.add_argument("--dispatch", metavar="WORKFLOW", help="Run this workflow on main and wait for its verdict")
    parser.add_argument("--timeout", type=int, default=3600, help="With --dispatch, seconds to wait for the run")
    parser.add_argument("--field", action="append", default=[], metavar="NAME=VALUE",
                        help="With --dispatch, a workflow input, as the failed run was started with (repeatable)")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    remote = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    repo = origin_repo(remote.stdout) if remote.returncode == 0 else None
    if not repo:
        print(json.dumps({"error": "origin is not a GitHub repository"}) if args.json
              else "ci_watch: origin is not a GitHub repository; nothing to watch")
        return 2
    runner = bound(repo)
    try:
        if args.dispatch:
            code, outcome = dispatch_and_wait(args.dispatch, runner, timeout=args.timeout, fields=args.field)
            if args.json:
                print(json.dumps({"exit": code, "run": outcome}, indent=2))
            elif code == 2:
                print(f"ci_watch: {outcome}")
            else:
                print(evidence_line(outcome))
            return code
        runs = fetch(runner, per_workflow=args.per_workflow)
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
