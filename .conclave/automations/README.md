# Isotone automations

Every scheduled job for Isotone lives here: the task list in `tasks.json`, the runner, the failure alert, and the Task Scheduler installer. Adapted from the Rizonetech automations (operator request, 2026-10-19); Isotone runs on Windows, so the tasks are Windows Task Scheduler tasks under `\Isotone\` where Rizonetech's are systemd user units.

## What runs

| Task | When (local time) | Runs | Fails when |
| --- | --- | --- | --- |
| `isotone-delegate-probe` | Monday 07:00 | `scripts/panel_slots.py delegate-probe` | the `sonnet` alias no longer serves the pinned delegate model at the pinned effort (`.conclave/reviewers.toml` needs a re-pin) |
| `isotone-vulnerable-packages` | Monday 07:15 | `scripts/check-vulnerable-packages.py` | a NuGet package in `Isotone.slnx`, direct or transitive, has a published advisory, or the restore or the report fails |
| `isotone-dotnet-ga` | Monday 07:30 | `scripts/check-sdk-ga.py` | the .NET 11 GA SDK is out while `global.json` still pins a release candidate, so `D00 T02 §8` is ready (a newer release candidate is printed, not failed) |

Every task starts when available: a run missed while this PC was off fires at the next chance, as systemd's `Persistent=true` does. A start while the task still runs is ignored, the execution limit is five minutes past the task's timeout, and the weekly tasks carry a five-minute random delay. Tasks run only while the operator is logged on, so no password is stored.

## When a run fails

Task Scheduler starts `pythonw.exe .conclave/automations/run.py <name>`. The runner writes the run's output to `build/automations/<name>/<UTC>.log` (the newest 20 kept) and its outcome to `build/automations/<name>/last.json`. On a non-zero exit or a timeout it calls `alert.py`, which emails `rizonetech@gmail.com` the task, its exit, and the tail of that run's log.

- It sends through SMTP2GO from `website@rizonetech.com`, the verified sender the Rizonetech automations use (Rizonesoft is a brand of Rizonetech).
- The key is read at send time from the Conclave vault item "Rizonetech SMTP2GO (website mail)" through `conclave-op` in WSL. Nothing is stored here, and there is no `.env`.
- SMTP2GO answers a refused send with HTTP 200 and `succeeded: 0`; the alert treats that as a failure.
- The runner exits with the command's code (124 on a timeout), or 3 when the alert could not be sent, with the reason appended to the run's log, so Task Scheduler's Last Run Result shows every failure.

## Install and inspect

```powershell
pwsh .conclave/automations/install.ps1              # idempotent; re-run after editing tasks.json
pwsh .conclave/automations/install.ps1 -Uninstall   # remove every \Isotone\ task
Get-ScheduledTask -TaskPath '\Isotone\' | Get-ScheduledTaskInfo | Format-Table TaskName, NextRunTime, LastRunTime, LastTaskResult
Start-ScheduledTask -TaskPath '\Isotone\' -TaskName isotone-dotnet-ga   # run one now
python .conclave/automations/run.py isotone-dotnet-ga                   # or run it in this console
python .conclave/automations/alert.py isotone-dotnet-ga --dry-run       # preview the alert for its last run
python scripts/tests/test_automations.py
```

The installer reads `tasks.json` and registers every task it lists; a task under `\Isotone\` that the file no longer lists is removed.

## Adding an automation

1. Add an entry to `tasks.json`: an `isotone-` name, a description, the command (a script in this repository, `python` first), a trigger (`{"weekly": "<Day>", "at": "HH:MM"}` or `{"at_logon_delay_minutes": N, "every_minutes": N}`), and `timeout_minutes`.
2. Add its row to the table above; `scripts/tests/test_automations.py` fails until the table and the file agree.
3. Run the tests, then the installer.
