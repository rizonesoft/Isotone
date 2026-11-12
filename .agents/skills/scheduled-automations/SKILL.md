---
name: scheduled-automations
description: Add, change, remove, install, or debug a scheduled job in .conclave/automations/ (tasks.json, run.py, alert.py, install.ps1 for Windows Task Scheduler, and install.sh for systemd user timers). Use when a local PC check should run on a schedule, when an "Automation failed" email arrives, or when inspecting scheduled jobs.
---

# Scheduled Automations

Every local scheduled job lives in `.conclave/automations/tasks.json` (`\Isotone\` folder in Windows Task Scheduler). The installers register each task from `tasks.json`, the scheduler runs `python .conclave/automations/run.py <name>`, and `run.py` logs under `build/automations/<name>/` and alerts on failure. Read `.conclave/automations/README.md` for the full contract.

## Add or change a task

1. Keep `"folder": "\\Isotone\\"` in `.conclave/automations/tasks.json`, and prefix every task `name` with `isotone-`.
2. Implement the check as a deterministic repository script under `scripts/` that exits `0` when healthy, `1` when an actionable check failed, and `2` when an external source could not be reached (never `0` on unverified state), covered by unit tests under `scripts/tests/`.
3. Add the task entry to `tasks.json` (`name`, `description`, `command`, `trigger`, `timeout_minutes`) and document its row in `.conclave/automations/README.md`.
4. Verify `python -m unittest scripts/tests/test_automations.py`, run `python .conclave/automations/run.py <name>` once, and re-run `pwsh .conclave/automations/install.ps1` on Windows to sync Task Scheduler.

To remove a task, delete its entry from `tasks.json` and `.conclave/automations/README.md`, then re-run `pwsh .conclave/automations/install.ps1`.

## Debugging a failed task

1. Inspect `build/automations/<name>/last.json` and its referenced log file, then reproduce with `python .conclave/automations/run.py <name>`.
2. Self-heal the root cause at its owning layer (for example updating `native/toolchain.json` after a verified Visual Studio update when `check-local-tools.py` reports a pin mismatch); never weaken a check or inflate timeouts to silence a real failure.

## Rules

- `.conclave/automations/tasks.json` is the single source of truth; never register ad-hoc Task Scheduler entries outside it (except `Isotone run watchdog` managed by `python scripts/run-guard.py install`).
- Scheduled tasks must run 100% unattended with zero interactive prompts and zero secrets in `tasks.json`, argv, or logs.
- Checks that inspect public repository/dependency advisories belong in `.github/workflows/pins.yml`, while checks that require this PC (`check-local-tools.py`, `isotone-pr-merge`) belong in `tasks.json`.
