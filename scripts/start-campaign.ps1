#Requires -Version 7.2
<#
.SYNOPSIS
  Starts the unattended campaign, or picks a dead one up, in this window.
.DESCRIPTION
  Asks scripts/campaign_guard.py what to do (`launch`) and does it:

  - No run is open: a new Claude Code session starts under `/goal`, with the goal text campaign_guard.py holds
    (finish the plan through process-plan, every section stamped, aiming for the best app in its class), on the
    writer model .conclave/reviewers.toml pins, with --dangerously-skip-permissions.
  - A run is open and its session died: that same session is resumed, so it still owns the run guard.
  - A run is open and its session is alive, any other Claude Code session is open in this folder, or another
    launcher window is still open: nothing starts, because two writers on one tree is the worse failure.

  `launch` records the session id and flags, which is what lets the watchdog (scripts/run-guard.py watch, ticked every
  10 minutes by this repository's scheduled task) resume the run headless if this window is ever lost.

  The desktop shortcut "Isotone campaign" runs this file. Stop the run by telling the session to stop: it ends the
  run through `campaign_guard.py end`, after which neither the watchdog nor this script resumes it.
.EXAMPLE
  pwsh -File scripts/start-campaign.ps1
#>
[CmdletBinding()]
param(
  # Creates or replaces the desktop shortcut "Isotone campaign" for this clone, then exits. A shortcut can only hold
  # absolute paths, so every one is derived here from where this file and this PowerShell actually are: run it again
  # after moving the clone.
  [switch]$InstallShortcut
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

if ($InstallShortcut) {
  $link = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Isotone campaign.lnk'
  $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($link)
  $shortcut.TargetPath = (Get-Process -Id $PID).Path
  # No -NoExit: the window must close when the session ends, because the launch record holds its place for as
  # long as this process lives, and a window left open would keep the watchdog from resuming a dead session.
  $shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
  $shortcut.WorkingDirectory = $repo
  $shortcut.IconLocation = "$(Join-Path $repo 'resources\icons\stilus\stilus.ico'),0"
  $shortcut.Description = 'Start or resume the unattended Isotone campaign'
  $shortcut.Save()
  Write-Host "Shortcut written: $link -> $PSCommandPath"
  return
}

# The launch record names this process, so the place it reserves holds for exactly as long as this window lives:
# no second launcher and no watchdog tick starts a session while this one is starting or running its own.
$raw = python scripts/campaign_guard.py launch --launcher-pid $PID
if ($LASTEXITCODE -ne 0) { throw "campaign_guard.py launch failed (exit $LASTEXITCODE)" }
$plan = $raw | ConvertFrom-Json

if ($plan.action -eq 'live') {
  Write-Host "The campaign is already running in session $($plan.session). Nothing was started."
  Start-Sleep -Seconds 12
  return
}
if ($plan.action -eq 'busy') {
  Write-Host "Another Claude Code session is open in this folder ($($plan.sessions -join ', ')). One session writes, so nothing was started: close it, then run this again."
  Start-Sleep -Seconds 12
  return
}
if ($plan.action -eq 'starting') {
  Write-Host "Session $($plan.session) is being started by another launcher window. Nothing was started."
  Start-Sleep -Seconds 12
  return
}

# Everything from here runs with the launch held, so it all sits inside one cleanup: whatever fails or ends, the
# place this launcher holds is freed, and a shell left open never keeps the watchdog from resuming an open run.
try {
$scheduled = (python scripts/run-guard.py status | Select-Object -Skip 1 | Out-String | ConvertFrom-Json).watchdog
if ($scheduled -ne 'own task') {
  # Without the scheduled tick nothing resumes a session that dies, so the launcher puts it in place. A task left
  # pointing at a folder this clone moved away from (STALE) is replaced the same way.
  python scripts/run-guard.py install
  if ($LASTEXITCODE -ne 0) { Write-Warning 'The watchdog task could not be created, so a session that dies will not be resumed.' }
}

# The language-server plugin is found through a per-machine registration that holds this folder's absolute path
# (Claude Code documents no relative form), so a clone that is new or has moved is registered here, from where this
# file actually is.
$marketplace = Join-Path $repo 'tools\claude-plugins'
$listed = claude plugin marketplace list 2>&1 | Out-String
if (-not $listed.Contains($marketplace)) {
  if ($listed -match 'isotone-tools') { claude plugin marketplace remove isotone-tools | Out-Null }
  claude plugin marketplace add $marketplace | Out-Null
  claude plugin install isotone-lsp@isotone-tools --scope project | Out-Null
  Write-Host "Registered the isotone-tools plugin folder at $marketplace."
}

$flags = @($plan.args)
  if ($plan.action -eq 'start') {
    Write-Host "Starting the Isotone campaign (session $($plan.session))."
    & claude --session-id $plan.session @flags --name 'Isotone campaign' $plan.prompt
  } else {
    Write-Host "Resuming the Isotone campaign (session $($plan.session))."
    & claude --resume $plan.session @flags $plan.prompt
  }
} finally {
  python scripts/campaign_guard.py launch-done --launcher-pid $PID | Out-Null
}
