#!/usr/bin/env python3
"""The run guard's view from outside the session: what the campaign run is, and whether its session is still there.

    python scripts/run-guard.py status      the run, its session (live or ended), and whether an old task is left
    python scripts/run-guard.py uninstall   remove the scheduled task an older clone left behind

Nothing restarts or resumes a run on its own (operator decision 2026-11-12). A run starts only when the operator
starts it (scripts/start-campaign.ps1), closing its window stops it, and a crash or a reboot ends it. This file once
installed and ticked the run watchdog, a scheduled task that resumed a dead session; `watch` and `install` are gone
and are refused, so a task left on a machine starts nothing, and `uninstall` removes it. `status` only reads: a
session that is gone is reported as ended, with how the operator resumes the run. The rules live in
scripts/campaign_guard.py. Stdlib only.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True  # the guard's own cache files must not read as progress in the tree it reports on
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import campaign_guard as guard

ROOT = guard.REPO
REMOVED = ("watch", "install")  # the watchdog's tick and the task that scheduled it


def say(text: str) -> None:
    if sys.stdout is not None:
        print(text)


def scheduler() -> str:
    """Whether the removed watchdog's scheduled task still exists on this machine: MISSING is the expected answer, and
    LEFTOVER means an older clone installed it (it starts nothing now; `uninstall` removes it)."""
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    own = subprocess.run(["schtasks", "/Query", "/TN", guard.WATCH_TASK], capture_output=True, text=True,
                         errors="replace", creationflags=flags)
    return "MISSING" if own.returncode != 0 else "LEFTOVER"


def status() -> int:
    try:
        run = guard.read_guard(ROOT)
        session = guard.session_state(ROOT)
    except (guard.GuardError, OSError) as error:
        run, session = {"error": str(error)}, {"error": str(error)}
    say("active" if run else "inactive")
    say(json.dumps({"guard": run, "session": session, "watchdog": scheduler()}, indent=2))
    return 0


def uninstall() -> int:
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    done = subprocess.run(["schtasks", "/Delete", "/F", "/TN", guard.WATCH_TASK], capture_output=True, text=True,
                          errors="replace", creationflags=flags)
    say((done.stdout or done.stderr).strip())
    return done.returncode


COMMANDS = {"status": status, "uninstall": uninstall}


def main(argv: list[str]) -> int:
    if len(argv) == 1 and argv[0] in REMOVED:
        if sys.stderr is not None:  # a leftover task runs this under pythonw, which has no stderr
            print(f"run-guard: `{argv[0]}` was removed on 2026-11-12: nothing restarts or resumes a run on its own. "
                  "Start or resume it yourself with scripts/start-campaign.ps1.", file=sys.stderr)
        return 2
    if len(argv) != 1 or argv[0] not in COMMANDS:
        if sys.stderr is not None:
            print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    return COMMANDS[argv[0]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
