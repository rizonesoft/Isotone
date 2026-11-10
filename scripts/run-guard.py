#!/usr/bin/env python3
"""The run watchdog's schedule: the scheduled task that ticks the campaign guard from outside the session.

    python scripts/run-guard.py watch       one scheduled tick: resume a dead campaign session, never beside a live one
    python scripts/run-guard.py status      the run, the last tick, and whether the task is installed
    python scripts/run-guard.py install     add the scheduled task "<folder> run watchdog" for `watch`
    python scripts/run-guard.py uninstall   remove it

The rules live in scripts/campaign_guard.py (`watch`); this file only owns the schedule and the tick record. The file
name, the task name, and the four commands match the run guards of the machine's other repositories, so whatever
schedules those can schedule this one. Stdlib only.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True  # the guard's own cache files must not read as progress in the tree it watches
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import campaign_guard as guard

ROOT = guard.REPO
TICK = os.path.join(ROOT, "build", "claude-campaign-last-tick.json")


def say(text: str) -> None:
    if sys.stdout is not None:  # pythonw, as the scheduled task runs it, has no stdout
        print(text)


def record(result: str, ok: bool) -> None:
    os.makedirs(os.path.dirname(TICK), exist_ok=True)
    guard._write_json(TICK, {"at": guard._utc_now(), "ok": ok, "result": result})


def watch() -> int:
    try:
        result = guard.watch(ROOT)
    except Exception as error:  # a tick that failed says so and starts nothing; the next one tries again
        record(repr(error), False)
        say(f"watch failed: {error!r}")
        return 1
    record(result, True)
    say(result)
    return 0


def scheduler() -> str:
    """Whether the scheduled task that runs `watch` exists and names this file. A scheduled task can only hold an
    absolute path, so a clone that moved leaves a task pointing at the old folder: that reads STALE, and `install`
    (which replaces the task) repairs it."""
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    own = subprocess.run(["schtasks", "/Query", "/TN", guard.WATCH_TASK, "/XML"], capture_output=True, text=True,
                         errors="replace", creationflags=flags)
    if own.returncode != 0:
        return "MISSING"
    return "own task" if os.path.abspath(__file__).lower() in own.stdout.lower() else "STALE"


def status() -> int:
    try:
        run = guard.read_guard(ROOT)
    except guard.GuardError as error:
        run = {"error": str(error)}
    say("active" if run else "inactive")
    say(json.dumps({"guard": run, "last_tick": guard._read_json(TICK) or None, "watchdog": scheduler()}, indent=2))
    return 0


def install() -> int:
    python = sys.executable
    windowless = os.path.join(os.path.dirname(python), "pythonw.exe")
    runner = windowless if os.path.exists(windowless) else python
    action = f'"{runner}" "{os.path.abspath(__file__)}" watch'
    done = subprocess.run(["schtasks", "/Create", "/F", "/TN", guard.WATCH_TASK, "/SC", "MINUTE", "/MO",
                           str(guard.WATCH_MINUTES), "/IT", "/TR", action], capture_output=True, text=True)
    say((done.stdout or done.stderr).strip())
    return done.returncode


def uninstall() -> int:
    done = subprocess.run(["schtasks", "/Delete", "/F", "/TN", guard.WATCH_TASK], capture_output=True, text=True)
    say((done.stdout or done.stderr).strip())
    return done.returncode


def main(argv: list[str]) -> int:
    commands = {"watch": watch, "status": status, "install": install, "uninstall": uninstall}
    if len(argv) != 1 or argv[0] not in commands:
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    return commands[argv[0]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
