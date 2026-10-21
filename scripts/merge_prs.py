#!/usr/bin/env python3
"""Merge one eligible dependency pull request, only when the clone is level with GitHub (D00 T01 §12).

    python scripts/merge_prs.py check                # preflight and the eligible list; merges nothing; exit 0
    python scripts/merge_prs.py run [--campaign]     # preflight, then at most one merge
    python scripts/merge_prs.py run --task           # the scheduled task: a refused preflight exits 0, never alerts

The operator asked on 2026-10-21 to "merge PRs inside the loop, at section boundaries", replacing the automations
README's "Nothing merges by itself". `process-plan` and `process-phase` run `run --campaign` after each stamp push's
green CI read-back, the one moment the clone is level with GitHub; the scheduled task `isotone-pr-merge` runs `run`
when no campaign does.

Preflight refuses, naming the reason, unless the working tree is clean, the local `HEAD` equals the fetched
`origin/main`, and no section is in progress (an open section carrying `> **Started:**` without its `Verified:`
stamp). Without `--campaign` it also refuses while a campaign runs: the run guard `build/claude-campaign-guard.json`
exists, or Claude Code's scheduler lock `.claude/scheduled_tasks.lock` names a live process. `--campaign` is the
in-loop call, whose caller is the campaign itself.

A pull request is eligible when its author is Dependabot, or the pins workflow on a `pins/` branch; it carries
`dependencies` or `pins`; it targets `main` and is not a draft; it has at least one check and every check passed
(`SUCCESS`, `SKIPPED` or `NEUTRAL`, none pending or failing); and GitHub reports it `MERGEABLE` and `CLEAN`. A .NET SDK
pin (a `pins/dotnet-` branch, or a change to `global.json`) is never eligible: `D00 T02 §8` owns it.

The merge is `gh pr merge <n> --rebase --delete-branch --match-head-commit <head sha>`, so history stays linear and a
branch that moved since it was read is refused; then `git pull --ff-only origin main` and
`python scripts/todo-graph.py validate`. One merge per run, oldest pull request first; the first failure stops the
run, names itself, and leaves every remaining pull request for the operator. Exit codes: `run` 0 when a merge landed
or nothing was eligible, 1 on a failed merge, pull, or validate, 2 when preflight refused. With `--task` (the
`isotone-pr-merge` task) a refused preflight exits 0: a campaign running or a section in progress is the task doing
its job, and only a real failure reaches the failure email.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BOT_AUTHORS = {"app/dependabot", "dependabot[bot]"}
PINS_AUTHORS = {"app/github-actions", "github-actions[bot]"}
LABELS = {"dependencies", "pins"}
PASSING = {"SUCCESS", "SKIPPED", "NEUTRAL"}
FIELDS = ("number,author,labels,baseRefName,isDraft,headRefName,headRefOid,mergeable,mergeStateStatus,"
          "statusCheckRollup,files,createdAt")
STARTED_RE = re.compile(r"^>\s*\*\*Started:\*\*", re.M)


class Refused(Exception):
    """Preflight refused; the message names why."""


def _run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")


def git(*args: str, cwd: Path = ROOT) -> str:
    done = _run(["git", *args], cwd)
    if done.returncode != 0:
        raise Refused(f"git {' '.join(args)} failed: {(done.stderr or done.stdout).strip()[:200]}")
    return done.stdout


def gh(*args: str, cwd: Path = ROOT) -> str:
    done = _run(["gh", *args], cwd)
    if done.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {(done.stderr or done.stdout).strip()[:200]}")
    return done.stdout


def _graph(root: Path):
    name = "todo_graph_for_merge"
    spec = importlib.util.spec_from_file_location(name, root / "scripts" / "todo-graph.py")
    module = importlib.util.module_from_spec(spec)
    # The graph's dataclasses look their module up in sys.modules while it loads.
    sys.modules[name] = module
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def sections_in_progress(root: Path, graph=None) -> list[str]:
    """Every open section carrying `> **Started:**` without its stamp, as 'DNN TNN §N'."""
    graph = graph or _graph(root)
    found = []
    for todo in graph.load_todos():
        text = (root / todo.path).read_text(encoding="utf-8")
        parts = re.split(r"(?m)^## (\d+)\. ", text)
        for i in range(1, len(parts) - 1, 2):
            num, body = int(parts[i]), parts[i + 1]
            section = todo.sections.get(num)
            if section is None or section.moved or section.status == "x" or num in todo.verified_sections:
                continue
            if STARTED_RE.search(body):
                found.append(f"D{todo.domain.split('-')[0]} T{todo.number} §{num}")
    return found


def _live_pid(pid) -> bool:
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    if os.name == "nt":
        done = _run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], ROOT)
        return str(pid) in done.stdout
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def campaign_active(root: Path) -> str | None:
    """Why a campaign is running, or None. The run guard is the signal; a scheduler lock held by a live process is a
    second reason (it means some session has scheduled jobs, which may be a campaign's heartbeat)."""
    if (root / "build" / "claude-campaign-guard.json").exists():
        return "a campaign run holds the guard build/claude-campaign-guard.json"
    lock = root / ".claude" / "scheduled_tasks.lock"
    try:
        data = json.loads(lock.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if isinstance(data, dict) and _live_pid(data.get("pid")):
        return f"a Claude Code session (pid {data.get('pid')}) holds .claude/scheduled_tasks.lock"
    return None


def preflight(root: Path, campaign: bool, git_fn=git, graph=None, active_fn=campaign_active) -> None:
    if not campaign:
        why = active_fn(root)
        if why:
            raise Refused(f"{why}; the loop merges at its section boundaries")
    if git_fn("status", "--porcelain", cwd=root).strip():
        raise Refused("the working tree has uncommitted changes")
    git_fn("fetch", "--quiet", "origin", "main", cwd=root)
    head = git_fn("rev-parse", "HEAD", cwd=root).strip()
    remote = git_fn("rev-parse", "origin/main", cwd=root).strip()
    if head != remote:
        raise Refused(f"HEAD {head[:12]} is not origin/main {remote[:12]}: push or pull first")
    busy = sections_in_progress(root, graph)
    if busy:
        raise Refused(f"a section is in progress: {', '.join(busy)}")


def _checks_pass(pr: dict) -> tuple[bool, str]:
    checks = pr.get("statusCheckRollup") or []
    if not checks:
        return False, "no checks have run"
    for check in checks:
        result = check.get("conclusion") or check.get("state") or ""
        status = check.get("status", "COMPLETED")
        if status != "COMPLETED" and check.get("__typename") == "CheckRun":
            return False, f"check {check.get('name')} is {status.lower()}"
        if result.upper() not in PASSING:
            return False, f"check {check.get('name') or check.get('context')} is {result.lower() or 'pending'}"
    return True, ""


def eligible(pr: dict) -> tuple[bool, str]:
    """(eligible, the first reason it is not)."""
    author = (pr.get("author") or {}).get("login", "")
    branch = pr.get("headRefName", "")
    if author in BOT_AUTHORS:
        pass
    elif author in PINS_AUTHORS and branch.startswith("pins/"):
        pass
    else:
        return False, f"author {author or 'unknown'} is neither Dependabot nor the pins workflow"
    labels = {l.get("name", "") for l in pr.get("labels") or []}
    if not labels & LABELS:
        return False, "carries neither dependencies nor pins"
    if branch.startswith("pins/dotnet-") or any(f.get("path") == "global.json" for f in pr.get("files") or []):
        return False, "a .NET SDK pin is D00 T02 §8's section work"
    if pr.get("baseRefName") != "main":
        return False, f"targets {pr.get('baseRefName')}, not main"
    if pr.get("isDraft"):
        return False, "is a draft"
    ok, why = _checks_pass(pr)
    if not ok:
        return False, why
    if pr.get("mergeable") != "MERGEABLE":
        return False, f"mergeable is {str(pr.get('mergeable')).lower()}"
    if pr.get("mergeStateStatus") != "CLEAN":
        return False, f"merge state is {str(pr.get('mergeStateStatus')).lower()}"
    return True, ""


def open_prs(gh_fn=gh, root: Path = ROOT) -> list[dict]:
    prs = json.loads(gh_fn("pr", "list", "--state", "open", "--base", "main", "--limit", "50", "--json", FIELDS,
                           cwd=root) or "[]")
    return sorted(prs, key=lambda p: (p.get("createdAt", ""), p.get("number", 0)))


def merge_one(pr: dict, root: Path, gh_fn=gh, git_fn=git, validate_fn=None) -> tuple[bool, str]:
    """Merge one pull request, pull, and validate; (ok, the line for the run file)."""
    n, sha = pr["number"], pr["headRefOid"]
    try:
        gh_fn("pr", "merge", str(n), "--rebase", "--delete-branch", "--match-head-commit", sha, cwd=root)
    except RuntimeError as error:
        return False, f"merge_prs: #{n} not merged: {error}"
    try:
        git_fn("pull", "--ff-only", "origin", "main", cwd=root)
    except Refused as error:
        return False, f"merge_prs: #{n} merged, but the pull failed: {error}"
    validate_fn = validate_fn or (lambda r: _run([sys.executable, "scripts/todo-graph.py", "validate"], r))
    done = validate_fn(root)
    if done.returncode != 0:
        return False, f"merge_prs: #{n} merged and pulled, but validate is red: {(done.stdout or '').strip()[-200:]}"
    head = git_fn("rev-parse", "HEAD", cwd=root).strip()
    return True, f"merge_prs: merged #{n} ({pr.get('headRefName')}) by rebase; main is {head[:12]}"


def main(argv: list[str] | None = None, root: Path = ROOT, gh_fn=gh, git_fn=git, graph=None,
         active_fn=campaign_active, validate_fn=None) -> int:
    parser = argparse.ArgumentParser(description="Merge one eligible dependency pull request at a safe moment.")
    parser.add_argument("mode", choices=("check", "run"))
    parser.add_argument("--campaign", action="store_true", help="the in-loop call: skip the active-campaign refusal")
    parser.add_argument("--task", action="store_true", help="the scheduled task: a refused preflight exits 0")
    args = parser.parse_args(argv)
    try:
        preflight(root, args.campaign, git_fn, graph, active_fn)
        preflight_line = "preflight: ok"
    except Refused as error:
        preflight_line = f"preflight: refused: {error}"
        if args.mode == "run":
            print(f"merge_prs: {preflight_line}")
            return 0 if args.task else 2
    try:
        prs = open_prs(gh_fn, root)
    except (RuntimeError, ValueError) as error:
        print(f"merge_prs: cannot list pull requests: {error}", file=sys.stderr)
        return 1
    verdicts = [(pr, *eligible(pr)) for pr in prs]
    if args.mode == "check":
        print(f"merge_prs: {preflight_line}")
        for pr, ok, why in verdicts:
            print(f"  #{pr['number']} {'eligible' if ok else 'not eligible: ' + why}")
        if not verdicts:
            print("  no open pull requests")
        return 0
    ready = [pr for pr, ok, _why in verdicts if ok]
    if not ready:
        print("merge_prs: nothing eligible" + "".join(f"; #{pr['number']} {why}" for pr, ok, why in verdicts if not ok))
        return 0
    ok, line = merge_one(ready[0], root, gh_fn, git_fn, validate_fn)
    print(line, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
