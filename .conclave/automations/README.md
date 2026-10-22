# Isotone automations

Every scheduled job that must run on this machine lives here: the task list in `tasks.json`, the runner, the failure alert, and the installers for Windows Task Scheduler (`install.ps1`) and systemd user timers (`install.sh`). Everything in this folder is Isotone's own. Isotone runs on Windows, so the tasks are Task Scheduler tasks under `\Isotone\`.

Repository pins are not kept here (operator request 2026-10-21, the RectoPDF shape). The daily GitHub workflow `.github/workflows/pins.yml` keeps them on their newest releases, and Dependabot keeps NuGet packages and GitHub Actions current, both documented below. Only the checks that need this PC (its CLIs, its Python, its installed .NET SDK, and its Claude login) run from this folder.

There is no WinUI 3 pin: Isotone is WPF only, and AGENTS.md refuses any other UI framework, so there is no `Microsoft.WindowsAppSDK` package to keep current.

## What runs here

| Task | When (local time) | Runs | Emails you when | Fails when |
| --- | --- | --- | --- | --- |
| `isotone-delegate-probe` | Monday 07:00 | `scripts/panel_slots.py delegate-probe` | (fails instead) | the `sonnet` alias no longer serves the pinned delegate model at the pinned effort (`DELEGATE` in `scripts/panel_slots.py` needs a re-pin) |
| `isotone-local-tools` | Monday 07:05 | `scripts/check-local-tools.py notify` | this PC's `codex` CLI (which runs every review round), `claude` CLI, or Python is behind its newest stable release, or this PC lacks the SDK `global.json` pins (once per finding) | npm, python.org or `global.json` cannot be read |
| `isotone-pr-merge` | every 60 minutes, from 15 minutes after logon | `scripts/merge_prs.py run --task` | (fails instead) | a merge, the pull after it, or `validate` failed, or `main`'s newest `plan-gates` or `build` push run failed (read at the start of every run, so a red the task's own merge caused alerts on its next run and nothing merges onto it); a refused preflight (a campaign running, a section in progress, a dirty, detached, or unsynced clone, or `main`'s CI still running) exits 0 and only logs |

A weekly task starts when available: a run missed while this PC was off fires at the next chance, with a five-minute random delay. A start while the task still runs is ignored, and a run is stopped five minutes past its timeout. Tasks run only while the operator is logged on, so no password is stored.

## What runs on GitHub

| Check | Daily at 05:17 UTC | Becomes |
| --- | --- | --- |
| .NET SDK (`global.json`) with the Microsoft.Extensions.* packages that track its runtime | `scripts/check-dotnet-pin.py pr` | a pull request on `pins/dotnet-<sdk>` for each newer release of the pinned channel: the next .NET 11 release candidate now, the GA SDK the day it ships (that PR is `D00 T02 §8`'s file edits; run its gates on the branch) |
| Vulnerable NuGet packages, direct or transitive | `scripts/check-vulnerable-packages.py issue` | one issue labelled `pins:vulnerable-packages` per vulnerable set; closed automatically on the first clean run |
| NuGet packages in `Directory.Packages.props` | Dependabot (`.github/dependabot.yml`), daily | a Dependabot pull request per group (Microsoft, SkiaSharp, testing, Serilog, minor and patch) |
| GitHub Actions | Dependabot, daily | a Dependabot pull request bumping each pinned SHA and its tag comment |

Every pull request from the pins workflow has `build.yml` and `plan.yml` dispatched on its branch, so its checks show on the PR before you merge. A version that already has a pull request, open, merged or closed, is never proposed again: closing a PR declines that version. Green pull requests merge at section boundaries (operator request 2026-10-21, "merge PRs inside the loop, at section boundaries", which replaced "Nothing merges by itself"): `scripts/merge_prs.py` merges one at a time, oldest first, by rebase with `--match-head-commit`, then pulls fast-forward and runs `validate`. It merges only when the working tree is clean, `HEAD` equals `origin/main`, and no section is in progress; only a Dependabot pull request or a pins-workflow one on a `pins/` branch, labelled `dependencies` or `pins`, targeting `main`, not a draft, with every check passed, every workflow its changed paths should trigger completed green on its head commit (`build` always, `plan-gates` when its path filter matches), no file renamed or copied, and GitHub reporting it mergeable and clean. A .NET SDK pin is never merged this way: it is `D00 T02 §8`'s section work. `process-plan` and `process-phase` run it after each stamp push; the `isotone-pr-merge` task runs it when no campaign does. A failure stops the run and leaves that pull request, and every one after it, for you; the intent to merge is recorded in `build/merge-prs-blocked.json` before the merge is issued and cleared only once it is verified, so a merge left unverified, unreconciled, or red stops every later run (exit 3, the failure email) until GitHub shows it never happened, or shows it merged into `main` with the clone level and `validate` green. The `.NET` rule (operator, 2026-10-21): the pin is the newest SDK in Microsoft's release metadata for the pinned channel (`latest-sdk` in `https://builds.dotnet.microsoft.com/dotnet/release-metadata/11.0/releases.json`), with `rollForward: disable`, and the Microsoft.Extensions.* packages that equal the pinned runtime move with it after nuget.org lists them. Dependabot ignores those packages, so the SDK check is their one owner.

The workflow needs the repository setting "Allow GitHub Actions to create and approve pull requests" (enabled 2026-10-21, with the default token permission left read-only; recorded in `D99 T01 §2`).

## How you hear about it

- **A pin moved:** a GitHub pull request labelled `dependencies` and `pins`, from the pins workflow or Dependabot. GitHub notifies you as for any PR. Merge it when its checks are green.
- **Something needs your decision:** a GitHub issue labelled `pins` and `pins:<check>`. It closes itself once the finding is gone, and closing it yourself dismisses that finding.
- **Something on this PC is behind:** an email from "Isotone automations" (`website@rizonetech.com`, through SMTP2GO) to `rizonetech@gmail.com`, titled "Isotone: ... is available", sent once per new finding.
- **A check broke:** on GitHub, a failed `pins` run, which GitHub emails to whoever last edited the schedule; on this PC, an email titled "Automation failed: <task> on <host>" with the log tail and how to run it again, repeated on every failing run until fixed.

No PR, issue or email means everything is current. `gh pr list --label pins`, `gh issue list --label pins` and the `Get-ScheduledTask` line below show the state at any time.

## When a run fails

Task Scheduler starts `pythonw.exe .conclave/automations/run.py <name>`. The runner writes the run's output to `build/automations/<name>/<UTC>.log` (the newest 20 kept) and its outcome to `build/automations/<name>/last.json`. On a non-zero exit or a timeout it calls `alert.py`, which emails `rizonetech@gmail.com` the task, its exit, the tail of that run's log, and how to run it again.

- It sends through SMTP2GO from `website@rizonetech.com`, the verified Rizonetech sender (Rizonesoft is a brand of Rizonetech), as "Isotone automations".
- The key is read at send time from the Conclave vault item "Rizonetech SMTP2GO (website mail)" through `conclave-op` in WSL. Nothing is stored here, and there is no `.env`.
- SMTP2GO answers a refused send with HTTP 200 and `succeeded: 0`; the alert treats that as a failure.
- The runner exits with the command's code (124 on a timeout, 126 when it cannot start), or 3 when the alert could not be sent, with the reason appended to the run's log, so Task Scheduler's Last Run Result shows every failure.

A notice email ("is available") is recorded as the git ref `refs/isotone-notice/<key>` after it is sent, so it goes out once; `git for-each-ref refs/isotone-notice` lists them, and deleting one sends that notice again.

## Install and inspect

```powershell
pwsh .conclave/automations/install.ps1              # idempotent; re-run after editing tasks.json
pwsh .conclave/automations/install.ps1 -Uninstall   # remove every \Isotone\ task
Get-ScheduledTask -TaskPath '\Isotone\' | Get-ScheduledTaskInfo | Format-Table TaskName, NextRunTime, LastRunTime, LastTaskResult
Start-ScheduledTask -TaskPath '\Isotone\' -TaskName <name>   # run one now
python .conclave/automations/run.py <name>                      # or run it in this console
python .conclave/automations/alert.py <name> --dry-run          # preview the alert for its last run
python scripts/tests/test_automations.py
python scripts/tests/test_pin_automations.py
```

The installer reads `tasks.json` and registers every task it lists; a task under `\Isotone\` that the file no longer lists is removed (2026-10-21 removed `isotone-vulnerable-packages` and `isotone-dotnet-ga`, which moved to the pins workflow, and `isotone-conclave-kits`, when Isotone stopped tracking the Conclave SDK).

## Adding an automation

A check of a repository pin belongs in `.github/workflows/pins.yml` (a `pr` or `issue` mode through `scripts/lib/pin_proposal.py`). Only a check that needs this machine belongs here:

1. Add an entry to `tasks.json`: an `isotone-` name, a one-line description, the command (a script in this repository, `python` first), a trigger (`{"weekly": "<Day>", "at": "HH:MM"}` or `{"at_logon_delay_minutes": N, "every_minutes": N}`), and `timeout_minutes`.
2. Add its row to the table above; `scripts/tests/test_automations.py` fails until the table and the file agree.
3. Run the tests, then the installer.
