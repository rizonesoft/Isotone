#!/usr/bin/env python3
"""Merge one eligible dependency pull request, only when the clone is level with GitHub (D00 T01 §12).

    python scripts/merge_prs.py check                # preflight and the eligible list; merges nothing; exit 0
    python scripts/merge_prs.py run [--campaign]     # preflight, then at most one merge
    python scripts/merge_prs.py run --task           # the scheduled task: a busy clone exits 0, never alerts

The operator asked on 2026-10-21 to "merge PRs inside the loop, at section boundaries", replacing the automations
README's "Nothing merges by itself". `process-plan` and `process-phase` run `run --campaign` after each stamp push's
green CI read-back, the one moment the clone is level with GitHub; the scheduled task `isotone-pr-merge` runs
`run --task` when no campaign does.

Preflight refuses, naming the reason, unless the checked-out branch is `main`, the working tree is clean, the local
`HEAD` equals the fetched `origin/main`, and no section is in progress (an open section carrying `> **Started:**`
without its `Verified:` stamp). Without `--campaign` it also refuses while a campaign runs: the run guard
`build/claude-campaign-guard.json` exists, or Claude Code's scheduler lock `.claude/scheduled_tasks.lock` names a live
process. Outside a campaign the whole run, preflight to validate, holds the run guard's own lock
(`build/claude-campaign-guard.lock`), so a campaign cannot start while a merge is under way: its `acquire` waits and
then asks to retry. `--campaign` is the in-loop call, whose caller is the campaign itself and already owns the clone.

A pull request is eligible when its author is Dependabot, or the pins workflow on a `pins/` branch; it carries
`dependencies` or `pins`; it targets `main` and is not a draft; it has at least one check and every check passed
(`SUCCESS`, `SKIPPED` or `NEUTRAL`, none pending or failing); GitHub reports it `MERGEABLE` and `CLEAN`; and its full
list of changed files was read (a list shorter than `changedFiles` is refused). A .NET SDK pin (a `pins/dotnet-` branch,
or a change to `global.json`) is never eligible: `D00 T02 §8` owns it.

Every GitHub call names the repository `origin` points at (`gh --repo <owner>/<name>`), so `GH_REPO` or a second
remote can never redirect a merge away from the clone preflight checked. The merge is
`gh pr merge <n> --rebase --delete-branch --match-head-commit <head sha>`, so history stays linear and a branch that
moved since it was read is refused; then `git pull --ff-only origin main` and `python scripts/todo-graph.py validate`.
One merge per run, oldest pull request first.

Exit codes for `run`: 0 when a merge landed and the clone validates, or nothing was eligible; 1 when nothing changed on
GitHub but something failed (a refused merge, a git or gh command that failed); 2 when preflight refused (with
`--task`, a busy clone exits 0 instead, because a campaign running or a section in progress is the task doing its job,
and only a real failure reaches the failure email); 3 when the merge landed on GitHub but the pull or `validate` then
failed, so `main` moved and the clone must be reconciled before any other work.

A merge the script made stays unverified in `build/merge-prs-health.json` until its own CI is read (D00 T01 §16): every
later `run` or `recover` reads it first, and while it is pending nothing else merges (a busy clone); a red, a read that
fails, or a merge still unread two hours on is exit 1. A guarding workflow on `main` that has not read green for two
hours is exit 1 too, so a stuck or disabled workflow cannot stop merging in silence.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BOT_AUTHORS = {"app/dependabot", "dependabot[bot]"}
PINS_AUTHORS = {"app/github-actions", "github-actions[bot]"}
LABELS = {"dependencies", "pins"}
PASSING = {"SUCCESS", "SKIPPED", "NEUTRAL"}
FIELDS = ("number,author,labels,baseRefName,isDraft,headRefName,headRefOid,mergeable,mergeStateStatus,"
          "statusCheckRollup,files,changedFiles,createdAt")
STARTED_RE = re.compile(r"^>\s*\*\*Started:\*\*", re.M)
# origin must be github.com itself, over HTTPS or SSH; any other host (an Enterprise server, a look-alike name) is
# refused (independent review round 2).
REMOTE_RE = re.compile(r"^(?:https://(?:[^@/]+@)?github\.com/|ssh://git@github\.com/|git@github\.com:)"
                       r"(?P<owner>[A-Za-z0-9_.-]+)/(?P<name>[A-Za-z0-9_.-]+?)(?:\.git)?/?$")
NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0  # CREATE_NO_WINDOW: a scheduled run opens no console
# Every git and gh call is bounded, and an intent record whose pull request still reads OPEN is cleared only after
# SETTLE_SECONDS, three times the bound on any call: a merge issued by a run that was killed cannot land after the
# record that guards it is gone (independent review round 7). While an intent settles, every run exits 3, so the loop
# holds new section work for at most that window (round 9); a shorter window would risk a late landing.
COMMAND_TIMEOUT = 300
SETTLE_SECONDS = 900
# GitHub computes `mergeable` lazily: the first read after `main` moves starts the computation and answers UNKNOWN,
# and a stamp push has always just moved `main`. An UNKNOWN answer is read again, a bounded number of times, before
# it counts (D00-T01-S12-F43: the first boundary run read both pull requests once and merged nothing). Only the one
# pull request a run would merge is read again, so the waits stay within the scheduled task's timeout however many
# pull requests are open (independent review round 18): at most two re-reads of MERGEABLE_TRIES each per run.
MERGEABLE_TRIES = 6
MERGEABLE_WAIT = 5.0
# One deadline for the whole run (independent review round 19): every command's timeout and every wait is capped by
# the time left, so a run ends inside the scheduled task's 600-second timeout however slow GitHub is, and a merge is
# issued only while MERGE_RESERVE seconds remain for the merge, the pull, and validate.
RUN_BUDGET = 540
# The workflows that guard `main` itself, read at the start of every run (D00 T01 §15): a merge onto a red `main` is
# refused, and the hourly task's next run reports a red its own merge caused, since it cannot wait out a build.
MAIN_WORKFLOWS = (("plan-gates", "plan.yml"), ("build", "build.yml"))
# A guarding workflow that has not read green for this long alerts (exit 1) instead of reading as a busy clone, so a
# stuck or disabled workflow cannot stop merging in silence (D00 T01 §16). The timer is per workflow, kept across
# heads in HEALTH, and only a green read clears it, so frequent pushes cannot reset it.
PENDING_ALERT_SECONDS = 2 * 3600
HEALTH = Path("build") / "merge-prs-health.json"


def _clock() -> float:
    return time.time()
MERGE_RESERVE = 120
_deadline: float | None = None


def _remaining() -> float:
    return float("inf") if _deadline is None else _deadline - time.monotonic()


class Refused(Exception):
    """Preflight refused: the clone is busy or not level with GitHub. Not a failure."""


class Failed(Exception):
    """A git or gh command failed: a real failure, which always exits nonzero. `returncode` is the command's exit
    status when one ran (124 for a timeout), so a caller can tell a documented status from any other failure."""

    def __init__(self, message: str, returncode: int | None = None):
        super().__init__(message)
        self.returncode = returncode


def _kill_tree(proc: subprocess.Popen) -> None:
    """Stop a timed-out command and everything it started, so no descendant keeps the output pipes (and the locks
    this run holds) open past the bound (independent review round 11)."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, timeout=30,
                           creationflags=NO_WINDOW)
        else:
            import signal
            os.killpg(proc.pid, signal.SIGKILL)
    except (OSError, subprocess.TimeoutExpired):
        # Best effort: the process may already be gone. The caller still reports the timeout as a failure (124).
        pass
    try:
        proc.kill()
    except OSError:
        # Already exited; nothing is hidden, the timeout result stands.
        pass


def _run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess:
    limit = min(COMMAND_TIMEOUT, _remaining())
    if limit < 1:
        return subprocess.CompletedProcess(argv, 124, "", "the run's time budget is spent")
    proc = subprocess.Popen(argv, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            encoding="utf-8", errors="replace", creationflags=NO_WINDOW,
                            start_new_session=(os.name != "nt"))
    try:
        out, err = proc.communicate(timeout=limit)
        return subprocess.CompletedProcess(argv, proc.returncode, out, err)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        try:
            out, err = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            out, err = "", ""
        return subprocess.CompletedProcess(argv, 124, out or "", f"timed out after {int(limit)}s")


def git(*args: str, cwd: Path = ROOT) -> str:
    done = _run(["git", *args], cwd)
    if done.returncode != 0:
        raise Failed(f"git {' '.join(args)} failed: {(done.stderr or done.stdout).strip()[:200]}", done.returncode)
    return done.stdout


def gh(*args: str, cwd: Path = ROOT) -> str:
    done = _run(["gh", *args], cwd)
    if done.returncode != 0:
        raise Failed(f"gh {' '.join(args)} failed: {(done.stderr or done.stdout).strip()[:200]}")
    return done.stdout


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their module up in sys.modules while it loads.
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
    graph = graph or _load("todo_graph_for_merge", root / "scripts" / "todo-graph.py")
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
    guard = root / "build" / "claude-campaign-guard.json"
    if guard.exists():
        try:
            doc = json.loads(guard.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            doc = None  # unreadable: a campaign may hold it, so the cautious answer is yes
        # A guard `end` marked ended is no campaign, even when the deletes after the mark never ran (D00 T01 §13);
        # only the mark `end` writes counts, judged by the guard's own test, and anything else is read the cautious way.
        ended = doc.get("ended") if isinstance(doc, dict) else None
        # The guard's code beside this script, the same checkout, decides what an ended mark is.
        rule = _load("campaign_guard_for_merge", Path(__file__).resolve().parent / "campaign_guard.py")
        if not rule.ended_mark_ok(ended):
            return "a campaign run holds the guard build/claude-campaign-guard.json"
    lock = root / ".claude" / "scheduled_tasks.lock"
    try:
        data = json.loads(lock.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if isinstance(data, dict) and _live_pid(data.get("pid")):
        return f"a Claude Code session (pid {data.get('pid')}) holds .claude/scheduled_tasks.lock"
    return None


@contextlib.contextmanager
def clone_lock(root: Path):
    """Hold the run guard's own lock for a whole run outside a campaign, so `campaign_guard.py acquire` cannot start a
    campaign while a merge is under way. A lock another change holds is a busy clone, not a failure."""
    guard = _load("campaign_guard_for_merge", root / "scripts" / "campaign_guard.py")
    try:
        lock = guard._Lock(str(root), wait=0.5)
        lock.__enter__()
    except guard.GuardError as error:
        raise Refused(f"the run guard's lock is held ({error})") from None
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


@contextlib.contextmanager
def merge_lock(root: Path):
    """One merge run at a time, campaign or task: an operating-system lock on `build/merge-prs.lock`, held from the
    recovery check to the verified merge, so no run can resolve or clear another run's intent record while that merge
    is in flight (independent review round 6). A held lock is a busy clone, not a failure."""
    path = root / "build" / "merge-prs.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        if os.name == "nt":
            import msvcrt
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            except OSError:
                raise Refused("another merge run holds build/merge-prs.lock") from None
        else:
            import fcntl
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise Refused("another merge run holds build/merge-prs.lock") from None
        try:
            yield
        finally:
            if os.name == "nt":
                import msvcrt
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def repository(root: Path, git_fn=git) -> str:
    """'github.com/<owner>/<name>' from origin's URL; every GitHub call names it with its host, so neither GH_REPO nor
    GH_HOST can redirect a merge to another repository or server."""
    url = git_fn("remote", "get-url", "origin", cwd=root).strip()
    m = REMOTE_RE.search(url)
    if not m:
        # Userinfo in a URL is a credential: it never reaches a log or the failure email (independent review round 4).
        shown = re.sub(r"(?<=://)[^@/]+@", "***@", url)
        raise Failed(f"origin {shown!r} is not a GitHub repository")
    return f"github.com/{m.group('owner')}/{m.group('name')}"


BLOCKED = Path("build") / "merge-prs-blocked.json"


def blocked(root: Path) -> dict | None:
    """The record a merge left when main may have moved under a red or unsynced clone, or None. Only a missing file
    means no record: an unreadable or malformed one still blocks (independent review round 5), as a record whose pull
    request cannot be named, which only the operator clears."""
    path = root / BLOCKED
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return {"pr": None, "why": f"the record cannot be read ({error.__class__.__name__})"}
    pr = record.get("pr") if isinstance(record, dict) else None
    if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
        return {"pr": None, "why": "the record names no pull request"}
    try:
        issued = float(record.get("issued_at"))
    except (TypeError, ValueError, OverflowError):
        issued = math.nan
    if not math.isfinite(issued):
        # A missing, non-numeric, or non-finite time (NaN, infinity, an integer past float range) cannot be aged, so
        # it can never settle (rounds 9 and 10).
        return {"pr": None, "why": "the record carries no usable issue time"}
    why = record.get("why")
    return {"pr": pr, "issued_at": issued, "why": why if isinstance(why, str) else "no reason recorded"}


def _block(root: Path, pr: int, why: str) -> None:
    path = root / BLOCKED
    path.parent.mkdir(parents=True, exist_ok=True)
    earlier = blocked(root)
    issued = earlier.get("issued_at") if earlier and earlier.get("pr") == pr else None
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({"pr": pr, "why": why, "issued_at": issued or time.time()}, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _branch(root: Path, git_fn) -> str:
    """The checked-out branch ref, or "" on a detached HEAD. `git symbolic-ref -q HEAD` exits 1, silently, exactly
    when HEAD is not a symbolic ref; that status with a HEAD that still resolves to a commit reads as detached (a busy
    clone), and every other failure (a fatal 128, a timeout's 124) stays a failure (D00 T01 §15, D00-T01-S12-F44,
    independent review round 6)."""
    try:
        return git_fn("symbolic-ref", "-q", "HEAD", cwd=root).strip()
    except Failed as error:
        if error.returncode != 1:
            raise
        try:
            git_fn("rev-parse", "--verify", "-q", "HEAD", cwd=root)
        except Failed:
            raise error from None
        return ""


def _push_paths(root: Path, file: str, head: str, git_fn) -> list[str] | None:
    """The push `paths` filter of `.github/workflows/<file>` as committed at `head` (the commit being judged, never
    the checkout, which a busy clone may hold changed: D00 T01 §16, independent review round 1), or None when it has
    none or cannot be read (then every change counts as one that triggers it)."""
    try:
        return _trigger(git_fn("show", f"{head}:.github/workflows/{file}", cwd=root), "push")[1]
    except Failed:
        return None


def _ci_verdict(name: str, file: str, repo: str, root: Path, head: str, gh_fn, git_fn,
                superseded_ok: bool = False) -> tuple[str, str]:
    """("green" | "pending" | "red", why) for one guarding workflow at `head` (D00 T01 §15, independent review round
    1): its push run on `head` decides; with none, the newest push run on an ancestor decides only when the changes
    since it miss the workflow's push paths (a path-filtered workflow need not run on every commit), and otherwise
    the run for `head` is still to come."""
    try:
        runs = json.loads(gh_fn("run", "list", "--repo", repo, "--branch", "main", "--event", "push", "--workflow",
                                file, "--limit", "30", "--json", "status,conclusion,url,headSha,createdAt",
                                cwd=root) or "[]")
    except ValueError as error:
        raise Failed(f"main's {name} runs cannot be read: {error}") from None
    if not runs:
        # No history at all is a workflow that never runs on main (removed, renamed, or disabled), never lag. It reads
        # as red, but it is no evidence, so it never moves the health record (D00 T01 §16, independent review round 2).
        return "unknown", f"main has no {name} push run to read, so its CI cannot be judged"
    runs = sorted(runs, key=lambda r: r.get("createdAt", ""), reverse=True)
    run = next((r for r in runs if r.get("headSha") == head), None)
    if run is None:
        older = next((r for r in runs if r.get("headSha") and _is_ancestor(git_fn, root, r["headSha"], head)), None)
        if older is None:
            return "pending", f"main's {name} has no push run on {head[:12]} or any commit before it yet"
        # Every path any commit in the range touched, never the endpoints' diff, which hides an edit a later commit
        # reverted (D00 T01 §16, independent review round 2). NUL-separated paths are never quoted, and with renames
        # off a moved file lists both its sides, so every path the push touched meets the filter (D00 T01 §15).
        changed = [f for f in git_fn("log", "--name-only", "-z", "--no-renames", "-m", "--format=",
                                     f"{older['headSha']}..{head}", cwd=root).split("\0") if f.strip()]
        if f".github/workflows/{file}" in changed:
            # The older run ran another definition of the workflow: it never stands in for the head (D00 T01 §16).
            return "pending", f"main's {name} workflow changed since its last run; its run for {head[:12]} is to come"
        paths = _push_paths(root, file, head, git_fn)
        if paths is None or any(_glob_re(p).match(f) for p in paths for f in changed):
            return "pending", f"main's {name} run for {head[:12]} has not started yet"
        run = older
    if superseded_ok and run.get("headSha") == head and run.get("conclusion") == "cancelled":
        # A merged commit's own run cancelled by a later push to main (`concurrency: cancel-in-progress`): the first
        # later run on main that finished reads the merge in its place (D00 T01 §16, independent review round 2).
        later = [r for r in reversed(runs) if r.get("headSha") not in (None, head)
                 and r.get("createdAt", "") > run.get("createdAt", "") and _is_ancestor(git_fn, root, head, r["headSha"])]
        done = next((r for r in later if r.get("status") == "completed" and r.get("conclusion") != "cancelled"), None)
        if done is None:
            return "pending", f"main's {name} run on {head[:12]} was cancelled by a later push whose run has not finished"
        run = done
    if run.get("status") != "completed":
        return "pending", f"main's {name} run is {run.get('status')}: {run.get('url')}"
    if run.get("conclusion") != "success":
        return "red", f"main's {name} run concluded {run.get('conclusion')}: {run.get('url')}"
    return "green", ""


def _instant(value, now: float) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value <= now


def _read_health(root: Path, now: float) -> dict:
    path = root / HEALTH
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"pending_since": {}, "merged": None}
    except (OSError, ValueError) as error:
        raise Failed(f"{HEALTH} cannot be read ({error}); check main's CI and the last merge, then delete it") from None
    merged = doc.get("merged") if isinstance(doc, dict) else None
    if merged is not None and not (isinstance(merged, dict) and isinstance(merged.get("sha"), str)
                                   and re.fullmatch(r"[0-9a-f]{40}", merged["sha"])
                                   and isinstance(merged.get("pr"), int) and not isinstance(merged["pr"], bool)
                                   and _instant(merged.get("at"), now)):
        raise Failed(f"{HEALTH} names an unverified merge it cannot describe; check main's CI and the last merge, "
                     f"then delete it")
    since = doc.get("pending_since") if isinstance(doc, dict) else None
    # A timer that is not a finite past instant (NaN, Infinity, or a time to come) would never reach the bound, so it
    # is damage, never a timer (independent review round 1).
    if not isinstance(since, dict) or not all(_instant(v, now) for v in since.values()):
        raise Failed(f"{HEALTH} is malformed; check main's CI and the last merge, then delete it")
    return {"pending_since": dict(since), "merged": merged}


def _write_health(root: Path, record: dict) -> None:
    path = root / HEALTH
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(record, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _age_pending(root: Path, verdicts: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """The verdicts with each workflow's pending time applied and recorded (D00 T01 §16): the first pending read of a
    workflow starts its timer, a green read clears it, and a pending past PENDING_ALERT_SECONDS reads as red. The
    verdicts must be main's own head's, and `judge` ages them only after every read it needs has succeeded, so a
    failed read, or a checkout that left main, never moves the record (independent review round 1)."""
    now = _clock()
    record = _read_health(root, now)
    if any(state == "unknown" for _name, state, _why in verdicts):
        # No evidence is not a reading: nothing moves (D00 T01 §16, independent review round 2).
        return verdicts
    since = dict(record["pending_since"])
    out = []
    for name, state, why in verdicts:
        if state == "green":
            since.pop(name, None)
        elif state == "pending":
            first = since.setdefault(name, now)
            if now - first >= PENDING_ALERT_SECONDS:
                state, why = "red", (f"{why}; main's {name} has not read green for {int((now - first) // 60)} minutes, "
                                     f"past the {PENDING_ALERT_SECONDS // 3600}-hour bound: a stuck or disabled workflow")
        out.append((name, state, why))
    if since != record["pending_since"]:
        _write_health(root, {**record, "pending_since": since})
    return out


def _record_merge(root: Path, commit: str, n) -> None:
    """Record a landed merge as unverified until its own CI is read (D00 T01 §16). One at a time: a different
    unverified merge already recorded is never overwritten."""
    now = _clock()
    record = _read_health(root, now)
    held = record["merged"]
    if held is not None and held["sha"] != commit:
        raise Failed(f"the merge of #{held['pr']} at {held['sha'][:12]} is still unverified")
    if held is None:
        _write_health(root, {**record, "merged": {"sha": commit, "pr": n, "at": now}})


def settle_merge(root: Path, repo: str, gh_fn, git_fn) -> str | None:
    """Read the CI of the last merge this script made, before anything else (D00 T01 §16). None when no merge is
    unverified; the line to print when this read verified it; Refused while it is pending inside the bound (nothing
    else merges meanwhile); Failed on a red, on no run evidence, past the bound, or when it cannot be read, and only
    a green or a red clears the record."""
    now = _clock()
    record = _read_health(root, now)
    held = record["merged"]
    if held is None:
        return None
    sha, n = held["sha"], held["pr"]
    git_fn("fetch", "--quiet", "origin", "+refs/heads/main:refs/remotes/origin/main", cwd=root)
    verdicts = [(name, *_ci_verdict(name, file, repo, root, sha, gh_fn, git_fn, superseded_ok=True))
                for name, file in MAIN_WORKFLOWS]
    state, why = _combined(verdicts)
    if any(s == "unknown" for _name, s, _why in verdicts):
        raise Failed(f"the merge of #{n} at {sha[:12]} cannot be read: {why}")
    if state == "pending":
        if now - held["at"] >= PENDING_ALERT_SECONDS:
            raise Failed(f"the merge of #{n} at {sha[:12]} is still unread {int((now - held['at']) // 60)} minutes on, "
                         f"past the {PENDING_ALERT_SECONDS // 3600}-hour bound: {why}")
        raise Refused(f"the merge of #{n} at {sha[:12]} is not read yet ({why}); nothing else merges until it is")
    _write_health(root, {**record, "merged": None})
    if state == "red":
        raise Failed(f"the merge of #{n} at {sha[:12]} reads red: {why}; repair main")
    return f"merge_prs: the merge of #{n} at {sha[:12]} reads green"


def _verdicts(repo: str, root: Path, head: str, gh_fn, git_fn) -> list[tuple[str, str, str]]:
    """(workflow, state, why) for every guarding workflow at `head`; it raises when GitHub cannot be read."""
    return [(name, *_ci_verdict(name, file, repo, root, head, gh_fn, git_fn)) for name, file in MAIN_WORKFLOWS]


def _combined(verdicts: list[tuple[str, str, str]]) -> tuple[str, str]:
    """Every workflow is read before the state is chosen, so a red one outranks one still running (D00 T01 §15,
    independent review round 1)."""
    for state in ("red", "pending"):
        found = [why for _name, s, why in verdicts if s == state or (state == "red" and s == "unknown")]
        if found:
            return state, "; ".join(found)
    return "green", ""


def judge(root: Path, repo: str, campaign: bool, git_fn, gh_fn, graph, active_fn, record: bool = False,
          task: bool = False) -> None:
    """The one judgment before every listing and every merge (D00 T01 §15): main's CI first (the slow GitHub reads),
    then the preflight (one fetch and the local checks back to back), and only then the CI's verdict, so nothing
    local is trusted across a GitHub read and a red is never reported for a clone the preflight refuses (independent
    review rounds 2 to 4). A head that moved since its CI was read is a busy clone. GitHub rebases onto the base as
    it is when `gh pr merge` runs; the instant between this judgment and that call is the window no client closes,
    and the landed check and validate after the merge read the result."""
    head = git_fn("rev-parse", "HEAD", cwd=root).strip()
    verdicts = _verdicts(repo, root, head, gh_fn, git_fn)
    try:
        preflight(root, campaign, git_fn, graph, active_fn)
    except Refused as busy:
        # The scheduled task still reports a red main when the clone is busy for a local reason (uncommitted work, a
        # detached checkout, a section in progress), judged on main's own fetched head, never on whatever the
        # checkout holds; a running campaign reads CI itself, so it is left alone (D00 T01 §16). Only main's head
        # ages the pending timers, and only once its read succeeded (independent review round 1).
        if task and not active_fn(root):
            try:
                origin = git_fn("rev-parse", "origin/main", cwd=root).strip()
            except Failed:
                raise busy from None
            main = verdicts if origin == head else _verdicts(repo, root, origin, gh_fn, git_fn)
            ostate, owhy = _combined(_age_pending(root, main) if record else main)
            if ostate == "red":
                raise Failed(f"{owhy}; repair main (nothing merges, the clone is busy: {busy})") from None
        raise
    now = git_fn("rev-parse", "HEAD", cwd=root).strip()
    if now != head:
        raise Refused(f"main moved from {head[:12]} to {now[:12]} while its CI was read")
    # The preflight passed, so HEAD is origin/main as just fetched: these are main's own verdicts.
    state, why = _combined(_age_pending(root, verdicts) if record else verdicts)
    if state == "red":
        raise Failed(f"{why}; repair main before any merge")
    if state == "pending":
        raise Refused(why)


def preflight(root: Path, campaign: bool, git_fn=git, graph=None, active_fn=campaign_active) -> None:
    if not campaign:
        why = active_fn(root)
        if why:
            raise Refused(f"{why}; the loop merges at its section boundaries")
    # The one slow call goes first, and every local check follows it back to back, so nothing local is judged and
    # then trusted across a network wait (independent review round 13). An explicit destination, so origin/main is
    # updated whatever remote.origin.fetch says (round 3): the comparison below is against the commit just fetched.
    git_fn("fetch", "--quiet", "origin", "+refs/heads/main:refs/remotes/origin/main", cwd=root)
    branch = _branch(root, git_fn)
    if branch != "refs/heads/main":
        raise Refused(f"the checked-out branch is {branch or 'a detached HEAD'}, not main")
    if git_fn("status", "--porcelain", cwd=root).strip():
        raise Refused("the working tree has uncommitted changes")
    head = git_fn("rev-parse", "HEAD", cwd=root).strip()
    remote = git_fn("rev-parse", "origin/main", cwd=root).strip()
    if head != remote:
        raise Refused(f"HEAD {head[:12]} is not origin/main {remote[:12]}: push or pull first")
    busy = sections_in_progress(root, graph)
    if busy:
        raise Refused(f"a section is in progress: {', '.join(busy)}")


def _glob_re(pattern: str) -> re.Pattern:
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(f"^{out}$")


# The glob shapes `_glob_re` matches exactly as GitHub does: literal path characters, `*` inside one segment, and
# `**` only as a whole trailing segment (or the whole pattern). Any other syntax GitHub supports (`?`, `[...]`, `+`,
# `**` mid-pattern) makes the filter unsure (independent review round 5).
_SUPPORTED_GLOB_RE = re.compile(r"^(?:\*\*|(?:[A-Za-z0-9._-]|\*(?!\*))+(?:/(?:[A-Za-z0-9._-]|\*(?!\*))+)*(?:/\*\*)?)$")
# The whitelist for every content line of the `on:` block (independent review round 6 replaced per-shape patches):
# a scalar is a quoted string with no `#` (and, double-quoted, no escape: independent review round 8) or a plain
# token that cannot open a YAML alias, anchor, or tag; a flow
# sequence holds scalars only. Any line outside these shapes makes the whole block unsure.
_SCALAR = r"""(?:'[^'#]*'|"[^"#\\]*"|[A-Za-z0-9_./-][A-Za-z0-9_./*-]*)"""
_FLOW = rf"\[\s*(?:{_SCALAR}\s*(?:,\s*{_SCALAR}\s*)*)?\]"
_VALUE = rf"(?:{_SCALAR}|{_FLOW}|\{{\s*\}})"
_KEY_LINE_RE = re.compile(rf"^\s+([A-Za-z_][\w-]*)\s*:(?:\s+({_VALUE}))?\s*(?:#.*)?$")
_ITEM_LINE_RE = re.compile(rf"^\s+-\s+({_SCALAR})\s*(?:#.*)?$")
_ITEM_KEY_LINE_RE = re.compile(rf"^\s+-\s+[A-Za-z_][\w-]*\s*:(?:\s+{_VALUE})?\s*(?:#.*)?$")
_SCALAR_RE = re.compile(_SCALAR)


def _unquote(value: str) -> str:
    return value[1:-1] if value[:1] in "'\"" else value


def _flow_items(value: str) -> list[str]:
    return [_unquote(m.group(0)) for m in _SCALAR_RE.finditer(value[1:-1])]


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _trigger(text: str, event: str) -> tuple[bool, list[str] | None]:
    """(the workflow runs on `event`, that event's `paths` filter or None) under a whitelist grammar that fails
    closed (independent review rounds 3 to 6): None means every change triggers it, and it is the answer for any
    shape this reader does not fully recognise, so both callers read an unsure filter the cautious way (the pull
    request must show the workflow; an older run never stands in for the head's).

    The grammar: a top-level `on:` key that is bare or names events as a plain scalar or a flow sequence of them;
    its block runs to the next content line at column 0 (blank and comment lines never end it), and every content
    line in it is a key line, a list item, or a list item that is a key, with scalars that cannot open a YAML alias,
    anchor, or tag. The event is one of the block's top keys with no inline value, and under it an optional `paths:`
    key holds a flow sequence or a block list of globs, every one in the shapes `_glob_re` matches exactly. Anything
    else (`paths-ignore` included) is unsure: the workflow runs, on every change. "Does not run" is answered only
    when the `on:` block was read in full and the event is not in it: a missing `on:`, an empty block, or a
    sequence at column 0 under it is unsure too (independent review round 7)."""
    lines = text.lstrip("\ufeff").splitlines()

    def content(line: str) -> bool:
        return bool(line.strip()) and not line.lstrip().startswith("#")

    top = next((i for i, l in enumerate(lines) if re.match(r"""^(on|'on'|"on")\s*:""", l)), None)
    if top is None:
        return True, None
    inline = re.sub(r"\s+#.*$", "", lines[top].split(":", 1)[1]).strip()
    if inline:
        if re.fullmatch(_SCALAR, inline):
            return _unquote(inline) == event, None
        if re.fullmatch(_FLOW, inline):
            return event in _flow_items(inline), None
        return True, None
    end = next((i for i in range(top + 1, len(lines)) if content(lines[i]) and not lines[i][0].isspace()), len(lines))
    block = [i for i in range(top + 1, end) if content(lines[i])]
    if not block:
        return True, None
    if not all(_KEY_LINE_RE.match(lines[i]) or _ITEM_LINE_RE.match(lines[i]) or _ITEM_KEY_LINE_RE.match(lines[i])
               for i in block):
        return True, None
    base = min(_indent(lines[i]) for i in block)
    tops = {_KEY_LINE_RE.match(lines[i]).group(1): i for i in block
            if _indent(lines[i]) == base and _KEY_LINE_RE.match(lines[i])}
    if any(_indent(lines[i]) == base and not _KEY_LINE_RE.match(lines[i]) for i in block):
        return True, None
    if event not in tops:
        return False, None
    start = tops[event]
    if _KEY_LINE_RE.match(lines[start]).group(2):
        return True, None
    under = [i for i in block if i > start]
    stop = next((k for k, i in enumerate(under) if _indent(lines[i]) <= base), len(under))
    children = under[:stop]
    if not children:
        return True, None
    child = min(_indent(lines[i]) for i in children)
    keys = {}
    for i in children:
        if _indent(lines[i]) == child:
            m = _KEY_LINE_RE.match(lines[i])
            if m is None:
                return True, None
            keys[m.group(1)] = i
    if "paths-ignore" in keys or "paths" not in keys:
        return True, None
    at = keys["paths"]
    value = _KEY_LINE_RE.match(lines[at]).group(2)
    if value:
        if not re.fullmatch(_FLOW, value):
            return True, None
        paths = _flow_items(value)
    else:
        paths = []
        for i in children:
            if i <= at:
                continue
            if _indent(lines[i]) <= _indent(lines[at]):
                break
            m = _ITEM_LINE_RE.match(lines[i])
            if m is None:
                return True, None
            paths.append(_unquote(m.group(1)))
    if not paths or not all(_SUPPORTED_GLOB_RE.match(p) for p in paths):
        return True, None
    return True, paths


def expected_workflows(root: Path, files: list[str]) -> list[str]:
    """The workflow names GitHub should run for a pull request changing `files`: every workflow under
    `.github/workflows/` triggered on pull requests whose `paths` filter, if any, matches a changed file."""
    names = []
    for wf in sorted((root / ".github" / "workflows").glob("*.yml")):
        text = wf.read_text(encoding="utf-8")
        runs, paths = _trigger(text, "pull_request")
        if not runs:
            continue
        if paths is not None and not any(_glob_re(pat).match(f) for pat in paths for f in files):
            continue
        m = re.search(r"(?m)^name:\s*(.+?)\s*$", text)
        names.append(m.group(1).strip("'\"") if m else wf.stem)
    return names


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


def identity(pr: dict) -> tuple[bool, str]:
    """(a bot's dependency pull request, the reason it is not): the author, branch, and labels the listing carries."""
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
    return True, ""


def eligible(pr: dict, root: Path = ROOT) -> tuple[bool, str]:
    """(eligible, the first reason it is not)."""
    ok, why = identity(pr)
    if not ok:
        return False, why
    branch = pr.get("headRefName", "")
    files = pr.get("files") or []
    if not isinstance(pr.get("changedFiles"), int) or len(files) < pr["changedFiles"]:
        # The file list GitHub returns is capped; an incomplete one could hide a global.json change.
        return False, f"its file list is incomplete ({len(files)} of {pr.get('changedFiles')} files read)"
    if branch.startswith("pins/dotnet-") or any(f.get("path") == "global.json" for f in files):
        return False, "a .NET SDK pin is D00 T02 §8's section work"
    if any(str(f.get("changeType", "")).upper() not in ("ADDED", "MODIFIED", "DELETED") for f in files):
        # A rename or copy hides its old path from this list, so a renamed global.json could pass; neither bot
        # renames files, so any such change waits for a person (independent review round 11).
        return False, "it renames or copies a file, which the bots never do"
    if pr.get("baseRefName") != "main":
        return False, f"targets {pr.get('baseRefName')}, not main"
    if pr.get("isDraft"):
        return False, "is a draft"
    ok, why = _checks_pass(pr)
    if not ok:
        return False, why
    # Every workflow that should have run for these files must have reported, not only the ones that did: a pins
    # pull request whose plan-gates dispatch failed must not merge on build alone (independent review round 7).
    ran = {c.get("workflowName") for c in pr.get("statusCheckRollup") or [] if c.get("workflowName")}
    missing = [w for w in expected_workflows(root, [f.get("path", "") for f in files]) if w not in ran]
    if missing:
        return False, f"workflow {', '.join(missing)} has not reported on it"
    if pr.get("mergeable") != "MERGEABLE":
        return False, f"mergeable is {str(pr.get('mergeable')).lower()}"
    if pr.get("mergeStateStatus") != "CLEAN":
        return False, f"merge state is {str(pr.get('mergeStateStatus')).lower()}"
    return True, ""


def workflows_green(pr: dict, repo: str, root: Path, gh_fn=gh) -> tuple[bool, str]:
    """(every expected workflow's latest run on the head commit completed with success, the first reason not).

    A workflow run concludes `success` only when all its jobs did, so a job that has not reported cannot hide behind
    another job's green check (independent review round 11)."""
    runs = json.loads(gh_fn("run", "list", "--repo", repo, "--commit", pr["headRefOid"], "--limit", "50",
                            "--json", "workflowName,status,conclusion,createdAt", cwd=root) or "[]")
    latest: dict[str, dict] = {}
    for run in sorted(runs, key=lambda r: r.get("createdAt", "")):
        latest[run.get("workflowName", "")] = run
    for name in expected_workflows(root, [f.get("path", "") for f in pr.get("files") or []]):
        run = latest.get(name)
        if run is None:
            return False, f"workflow {name} has no run on its head commit"
        if run.get("status") != "completed" or run.get("conclusion") != "success":
            return False, f"workflow {name} is {run.get('status')}/{run.get('conclusion') or 'pending'}"
    return True, ""


def pending(pr: dict) -> bool:
    """Whether GitHub is still computing this pull request's mergeability (either field reads UNKNOWN)."""
    return "UNKNOWN" in (pr.get("mergeable"), pr.get("mergeStateStatus"))


def view_pr(n, repo: str, root: Path, gh_fn=gh, tries: int = 1) -> dict:
    """One pull request as GitHub reports it now: while `pending`, it is read again, up to `tries` reads in all,
    MERGEABLE_WAIT seconds apart and never past the run's deadline; a last pending answer stands (eligibility
    refuses it)."""
    for attempt in range(tries):
        pr = json.loads(gh_fn("pr", "view", str(n), "--repo", repo, "--json", FIELDS + ",state", cwd=root) or "{}")
        if not pending(pr) or attempt == tries - 1 or _remaining() < MERGEABLE_WAIT + MERGE_RESERVE:
            return pr
        time.sleep(MERGEABLE_WAIT)
    return pr


def pending_only(pr: dict, repo: str, root: Path, gh_fn=gh) -> bool:
    """Whether GitHub's unfinished mergeability computation is all that keeps this pull request from merging: every
    other rule holds, its workflow runs included (independent review round 20)."""
    return (pending(pr) and eligible(dict(pr, mergeable="MERGEABLE", mergeStateStatus="CLEAN"), root)[0]
            and workflows_green(pr, repo, root, gh_fn)[0])


def open_prs(repo: str, gh_fn=gh, root: Path = ROOT) -> list[dict]:
    """The open pull requests on main, oldest first. The listing's author, branch, and labels settle `identity`, so
    only a bot's dependency pull request is read again with `view_pr` (the listing reports mergeability as UNKNOWN
    until GitHub computes it, and viewing is what makes it compute); every other one is never read in detail
    (independent review round 19)."""
    # GitHub filters by label before it applies the limit, so newer pull requests without a dependency label can
    # never crowd an old green bump out of the listing (independent review round 21).
    seen: dict = {}
    for label in sorted(LABELS):
        for p in json.loads(gh_fn("pr", "list", "--repo", repo, "--state", "open", "--base", "main", "--label", label,
                                  "--limit", "100", "--json", "number,author,headRefName,labels,createdAt",
                                  cwd=root) or "[]"):
            seen[p["number"]] = p
    listed = list(seen.values())
    prs = [view_pr(p["number"], repo, root, gh_fn) if identity(p)[0] else p for p in listed]
    return sorted(prs, key=lambda p: (p.get("createdAt", ""), p.get("number", 0)))


def _verdict(pr: dict, repo: str, root: Path, gh_fn) -> tuple[dict, bool, str]:
    """(the pull request, fully eligible, the first reason not): `eligible`, then its workflow runs on its head."""
    ok, why = eligible(pr, root)
    if ok:
        ok, why = workflows_green(pr, repo, root, gh_fn)
    return pr, ok, why


def merge_one(pr: dict, repo: str, root: Path, gh_fn=gh, git_fn=git, validate_fn=None,
              ready_fn=None) -> tuple[int, str]:
    """Merge one pull request, pull, and validate; (exit code, the line for the run file).

    The intent is recorded before the merge is issued (`build/merge-prs-blocked.json`) and cleared only once the merge
    is verified or proven never to have happened, so a process killed at any point after the merge leaves the record,
    and no later run merges until `resolve_block` has checked the recorded pull request on GitHub (independent review
    round 4). Every failure after the merge was issued is exit 3.
    """
    n = pr["number"]
    if _remaining() < MERGE_RESERVE:
        return 1, f"merge_prs: #{n} not merged, the run's time budget leaves too little to merge and verify"
    # Re-read the pull request at the last moment and judge it whole again: a base retargeted, a head pushed, a label
    # removed, or a check gone red since the listing is refused, because `gh pr merge` acts on the pull request as it
    # is now (independent review rounds 3 and 4).
    try:
        now = view_pr(n, repo, root, gh_fn, tries=MERGEABLE_TRIES)
    except (Failed, ValueError) as error:
        return 1, f"merge_prs: #{n} not merged, its state cannot be read: {error}"
    ok, why = eligible(now, root)
    if ok:
        try:
            ok, why = workflows_green(now, repo, root, gh_fn)
        except (Failed, ValueError) as error:
            ok, why = False, f"its workflow runs cannot be read: {error}"
    if not ok or now.get("headRefOid") != pr["headRefOid"] or now.get("state") != "OPEN":
        return 1, (f"merge_prs: #{n} not merged, it changed since it was read: "
                   f"{why or 'head ' + str(now.get('headRefOid'))[:12] + ', ' + str(now.get('state')).lower()}")
    # The clone is judged again at the last moment too: an edit, a branch switch, a local commit, or a section started
    # while GitHub was being read refuses the merge, because the locks keep out merge runs, not editors or git
    # (independent review round 12). `ready_fn` is the preflight itself.
    # A refusal here is still a busy clone and propagates as one (exit 0 with --task, 2 otherwise); main's CI is
    # judged again too, bound to the head the merge would land on (D00 T01 §15, independent review round 1).
    if ready_fn is not None:
        try:
            ready_fn()
        except Failed as error:
            return 1, f"merge_prs: #{n} not merged, the clone or main's CI changed while it was read: {error}"
    # The reserve again, right before the intent and the merge: the re-reads and the preflight above spend the
    # budget too (independent review round 20).
    if _remaining() < MERGE_RESERVE:
        return 1, f"merge_prs: #{n} not merged, the run's time budget leaves too little to merge and verify"
    try:
        _block(root, n, "merge issued, not yet verified")
    except OSError as error:
        return 1, f"merge_prs: #{n} not merged, the intent record cannot be written: {error}"
    try:
        code, line = _merge_and_verify(now, repo, root, gh_fn, git_fn, validate_fn)
    except (Failed, OSError) as error:
        # Any failure once the merge is issued, a launch or file error included, may have left main moved: exit 3,
        # never the "nothing changed" exit 1 (independent review round 5).
        code, line = 3, f"merge_prs: #{n} merge was issued, then an operation failed ({error}); check it before any other work"
    try:
        if code == 0:
            (root / BLOCKED).unlink(missing_ok=True)
        else:
            # Once the merge is issued, only a verified merge clears the intent; everything else keeps it.
            _block(root, n, line)
    except OSError:
        # The intent record written before the merge is still there, so the next run resolves it from GitHub.
        pass
    return code, line


def _merge_and_verify(pr: dict, repo: str, root: Path, gh_fn, git_fn, validate_fn) -> tuple[int, str]:
    n, sha = pr["number"], pr["headRefOid"]
    try:
        gh_fn("pr", "merge", str(n), "--repo", repo, "--rebase", "--delete-branch", "--match-head-commit", sha,
              cwd=root)
    except Failed as error:
        # gh merges first and deletes the branch after, so an error does not prove nothing changed (independent
        # review round 2): read the pull request back and decide from its state.
        state = _state(n, repo, root, gh_fn)
        if state is None:
            return 3, (f"merge_prs: #{n} merge reported an error ({error}) and its state cannot be read back: the "
                       f"outcome is unknown; check the pull request and reconcile main before any other work")
        if state.get("state") != "MERGED":
            # An error on an issued merge (a timeout included) does not cancel the request: GitHub may still apply
            # it, so the intent stays and settles, and the caller hears "may have moved", never "nothing changed"
            # (independent review round 8).
            return 3, (f"merge_prs: #{n} merge was issued and reported an error ({error}); it reads "
                       f"{str(state.get('state')).lower()} now but may still land, so its intent settles for "
                       f"{SETTLE_SECONDS // 60} minutes; reconcile main before any other work")
    unsteady = _clone_unsteady(root, git_fn)
    if unsteady:
        return 3, (f"merge_prs: #{n} merge was issued, but the clone changed during it ({unsteady}), so the pull was "
                   f"skipped; reconcile (git pull --ff-only origin main, then validate) before any other work")
    try:
        git_fn("pull", "--ff-only", "origin", "main", cwd=root)
    except Failed as error:
        return 3, (f"merge_prs: #{n} MERGED on GitHub, but the pull failed, so main moved and the clone is behind: "
                   f"{error}; reconcile (git pull --ff-only origin main, then validate) before any other work")
    verdict, commit = _landed(n, repo, root, gh_fn, git_fn)
    if verdict:
        return 3, f"merge_prs: #{n} {verdict}; check it before any other work"
    done = _validate(root, validate_fn)
    if done.returncode != 0:
        return 3, (f"merge_prs: #{n} MERGED and pulled, but validate is red on main: "
                   f"{(done.stdout or '').strip()[-200:]}; repair main before any other work")
    try:
        _record_merge(root, commit, n)
    except (Failed, OSError) as error:
        # The intent stays, so the next run's recovery records the merge before anything else (D00 T01 §16).
        return 3, f"merge_prs: #{n} MERGED and validated, but it cannot be recorded as unverified: {error}"
    head = git_fn("rev-parse", "HEAD", cwd=root).strip()
    return 0, (f"merge_prs: merged #{n} ({pr.get('headRefName')}) by rebase into main; main is {head[:12]}; its CI is "
               f"read on the next run")


def _clone_unsteady(root: Path, git_fn) -> str | None:
    """Why the clone is no longer the one the merge was judged against (off main or dirty), or None."""
    branch = _branch(root, git_fn)
    if branch != "refs/heads/main":
        return f"the checked-out branch is {branch or 'a detached HEAD'}"
    if git_fn("status", "--porcelain", cwd=root).strip():
        return "the working tree has uncommitted changes"
    return None


def _state(n, repo: str, root: Path, gh_fn) -> dict | None:
    try:
        return json.loads(gh_fn("pr", "view", str(n), "--repo", repo, "--json", "baseRefName,state,mergeCommit",
                                cwd=root) or "{}")
    except (Failed, ValueError):
        return None


def _landed(n, repo: str, root: Path, gh_fn, git_fn) -> tuple[str | None, str]:
    """(None, the merge commit) when the pull request merged into main and its merge commit is on the local HEAD;
    else (what is wrong, "")."""
    after = _state(n, repo, root, gh_fn)
    if after is None:
        return "merged, but its destination cannot be read back", ""
    commit = (after.get("mergeCommit") or {}).get("oid", "")
    on_main = bool(commit) and _is_ancestor(git_fn, root, commit, "HEAD")
    if after.get("state") != "MERGED" or after.get("baseRefName") != "main" or not on_main:
        return (f"did not land on main as read back (state {str(after.get('state')).lower()}, base "
                f"{after.get('baseRefName')}, merge commit {commit[:12] or 'none'} on main: {on_main})"), ""
    return None, commit


def _validate(root: Path, validate_fn):
    validate_fn = validate_fn or (lambda r: _run([sys.executable, "scripts/todo-graph.py", "validate"], r))
    return validate_fn(root)


def _is_ancestor(git_fn, root: Path, commit: str, ref: str) -> bool:
    try:
        git_fn("merge-base", "--is-ancestor", commit, ref, cwd=root)
        return True
    except Failed:
        return False


def resolve_block(root: Path, repo: str, gh_fn, git_fn, validate_fn) -> str | None:
    """None when no earlier merge is unresolved, or when the recorded one is now resolved (the record is cleared);
    else why this run must not merge.

    Resolution is read from GitHub, not inferred from a green tree (independent review round 4): a pull request still
    open or closed unmerged never changed anything; a merged one is resolved only when it merged into main, its merge
    commit is on the freshly fetched main, the clone is level with that main, and validate passes.
    """
    record = blocked(root)
    if record is None:
        return None
    n = record.get("pr")
    if n is None:
        return (f"{record.get('why')} at {BLOCKED.as_posix()}: verify main by hand, then delete the record")
    state = _state(n, repo, root, gh_fn)
    if state is None:
        return f"an earlier merge (#{n}) is unresolved and its state cannot be read: {record.get('why', '')[:160]}"
    if state.get("state") in ("OPEN", "CLOSED"):
        # Not merged now does not prove it never will be: a merge issued by a killed run may still be in flight.
        # The record clears only once SETTLE_SECONDS have passed since the merge was issued; until then the clone is
        # busy, not failed (independent review round 7).
        if time.time() - record["issued_at"] < SETTLE_SECONDS:
            # Unresolved, not busy: exit 3 holds new section work until it settles (independent review round 9).
            return (f"an earlier merge of #{n} still reads {state.get('state').lower()} and may be in flight; it "
                    f"settles {SETTLE_SECONDS // 60} minutes after it was issued")
        (root / BLOCKED).unlink(missing_ok=True)
        return None
    try:
        git_fn("fetch", "--quiet", "origin", "+refs/heads/main:refs/remotes/origin/main", cwd=root)
        level = git_fn("rev-parse", "HEAD", cwd=root).strip() == git_fn("rev-parse", "origin/main", cwd=root).strip()
    except Failed as error:
        return f"an earlier merge (#{n}) is unresolved and main cannot be read: {error}"
    if not level:
        return f"an earlier merge (#{n}) moved main and this clone is not level with it; reconcile, then validate"
    try:
        dirty = git_fn("status", "--porcelain", cwd=root).strip()
    except Failed as error:
        return f"an earlier merge (#{n}) is unresolved and the tree cannot be read: {error}"
    if dirty:
        # Validation must judge the committed main, not an uncommitted repair (independent review round 5).
        return f"an earlier merge (#{n}) is unresolved and the working tree has uncommitted changes; commit the repair first"
    verdict, commit = _landed(n, repo, root, gh_fn, git_fn)
    if verdict:
        return f"an earlier merge (#{n}) {verdict}"
    if _validate(root, validate_fn).returncode != 0:
        return f"an earlier merge (#{n}) left main red: validate fails; repair main"
    try:
        _record_merge(root, commit, n)
    except (Failed, OSError) as error:
        return f"an earlier merge (#{n}) landed but cannot be recorded as unverified: {error}"
    (root / BLOCKED).unlink(missing_ok=True)
    return None


def _work(args, root: Path, gh_fn, git_fn, graph, active_fn, validate_fn) -> int:
    if args.mode == "run" and not args.campaign:
        # A running campaign owns the clone and any intent record it has written: the scheduled run leaves both
        # alone and refuses before touching recovery (independent review round 6).
        why = active_fn(root)
        if why:
            raise Refused(f"{why}; the loop merges at its section boundaries")
    if args.mode in ("run", "recover") and blocked(root) is not None:
        # An unresolved earlier merge outranks every busy-clone refusal: it may have moved main, so it is a failure
        # that alerts until it is resolved, never a quiet exit 0, and a recovery that itself fails is exit 3 too.
        try:
            stuck = resolve_block(root, repository(root, git_fn), gh_fn, git_fn, validate_fn)
        except Exception as error:  # noqa: BLE001 -- while an intent exists, any failure blocks (round 10)
            stuck = f"an earlier merge is unresolved and its recovery failed: {error.__class__.__name__}: {error}"
        if stuck:
            print(f"merge_prs: not merging: {stuck}", file=sys.stderr)
            return 3
    if args.mode in ("run", "recover"):
        # The last merge's own CI before anything else, the clone busy or not (D00 T01 §16): pending is a busy clone
        # (nothing else merges), and a red, no evidence, or a merge unread past the bound is exit 1.
        try:
            line = settle_merge(root, repository(root, git_fn), gh_fn, git_fn)
        except Refused as error:
            if args.mode == "run":
                raise
            line = f"merge_prs: recover: {error}"
        if line:
            print(line)
    if args.mode == "recover":
        # Recovery only, never a merge: a campaign settles what an earlier run left before its first or resumed
        # section, and a merge there would land with no CI read-back before section work (independent review round 13).
        print("merge_prs: recover: no unresolved merge")
        return 0
    try:
        repo = repository(root, git_fn)
        # Main's own CI and the clone, whether or not anything turns out eligible: the hourly task learns of a red
        # its earlier merge caused on its next run, and never merges onto it (D00 T01 §15).
        judge(root, repo, args.campaign, git_fn, gh_fn, graph, active_fn, record=args.mode == "run",
              task=args.task)
        preflight_line = "preflight: ok"
    except Refused as error:
        preflight_line = f"preflight: refused: {error}"
        if args.mode == "run":
            print(f"merge_prs: {preflight_line}")
            return 0 if args.task else 2
        repo = None
    except Failed as error:
        if args.mode == "run":
            print(f"merge_prs: not merging: {error}", file=sys.stderr)
            return 1
        preflight_line = f"preflight: failed: {error}"
        repo = None
    try:
        repo = repo or repository(root, git_fn)
        prs = open_prs(repo, gh_fn, root)
    except (Failed, ValueError) as error:
        print(f"merge_prs: cannot list pull requests: {error}", file=sys.stderr)
        return 1
    try:
        verdicts = [_verdict(pr, repo, root, gh_fn) for pr in prs]
        if not any(ok for _pr, ok, _why in verdicts):
            # Only once nothing is fully eligible, the oldest pull request held solely by GitHub's unfinished
            # computation is read again (rounds 18 and 19); no other one waits.
            i = next((k for k, (pr, _ok, _why) in enumerate(verdicts) if pending_only(pr, repo, root, gh_fn)), None)
            if i is not None:
                again = view_pr(verdicts[i][0]["number"], repo, root, gh_fn, tries=MERGEABLE_TRIES)
                verdicts[i] = _verdict(again, repo, root, gh_fn)
    except (Failed, ValueError) as error:
        # A lookup that fails is a failed command, not an ineligible pull request: it stops the run with exit 1
        # (the task's failure email), and no other pull request merges past it (GPT panel round 2).
        print(f"merge_prs: cannot read the pull requests or their workflow runs: {error}", file=sys.stderr)
        return 1
    if args.mode == "check":
        print(f"merge_prs: {preflight_line} ({repo})")
        if blocked(root) is not None:
            print(f"  blocked by an unresolved earlier merge: {blocked(root)}")
        for pr, ok, why in verdicts:
            print(f"  #{pr['number']} {'eligible' if ok else 'not eligible: ' + why}")
        if not verdicts:
            print("  no open pull requests labelled dependencies or pins")
        return 0
    ready = [pr for pr, ok, _why in verdicts if ok]
    if not ready:
        print("merge_prs: nothing eligible" + "".join(f"; #{pr['number']} {why}" for pr, ok, why in verdicts if not ok))
        return 0
    code, line = merge_one(ready[0], repo, root, gh_fn, git_fn, validate_fn,
                           ready_fn=lambda: judge(root, repo, args.campaign, git_fn, gh_fn, graph, active_fn,
                                                  record=True, task=args.task))
    print(line, file=sys.stdout if code == 0 else sys.stderr)
    return code


def main(argv: list[str] | None = None, root: Path = ROOT, gh_fn=gh, git_fn=git, graph=None,
         active_fn=campaign_active, validate_fn=None, lock_fn=clone_lock, run_lock_fn=merge_lock) -> int:
    parser = argparse.ArgumentParser(description="Merge one eligible dependency pull request at a safe moment.")
    parser.add_argument("mode", choices=("check", "run", "recover"),
                        help="check lists; run merges at most one; recover only settles an earlier merge's intent")
    parser.add_argument("--campaign", action="store_true", help="the in-loop call: skip the active-campaign refusal")
    parser.add_argument("--task", action="store_true", help="the scheduled task: a busy clone exits 0")
    args = parser.parse_args(argv)
    global _deadline
    _deadline = time.monotonic() + RUN_BUDGET
    try:
        if args.mode == "check":
            return _work(args, root, gh_fn, git_fn, graph, active_fn, validate_fn)
        with run_lock_fn(root):
            if args.campaign or args.mode == "recover":
                return _work(args, root, gh_fn, git_fn, graph, active_fn, validate_fn)
            with lock_fn(root):
                return _work(args, root, gh_fn, git_fn, graph, active_fn, validate_fn)
    except Refused as error:
        print(f"merge_prs: preflight: refused: {error}")
        return 0 if args.task else 2
    except Failed as error:
        print(f"merge_prs: {error}", file=sys.stderr)
        return 1
    finally:
        _deadline = None


if __name__ == "__main__":
    sys.exit(main())
