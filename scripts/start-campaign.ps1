#Requires -Version 7.2
<#
.SYNOPSIS
  Starts the unattended campaign, or picks a dead one up, in this window.
.DESCRIPTION
  Runs `python scripts/campaign_guard.py start`, which takes the session slot (one operating-system lock that every
  campaign session must hold), decides under it, and runs the session in this window until it ends:

  - No run is open: a new Claude Code session starts under `/goal`, with the goal text campaign_guard.py holds
    (finish the plan through process-plan, every section stamped, aiming for the best app in its class), on the
    writer model .conclave/reviewers.toml pins, with --dangerously-skip-permissions.
  - A run is open and its session died: that same session is resumed, so it still owns the run guard.
  - The slot is held (a campaign session is starting or running, here or under the watchdog), or any other Claude
    Code session is open in this folder or under it: nothing starts, because one session writes.

  Each session, started here or resumed by the watchdog, signs in with the one-year token `start` reads from the
  Conclave vault ("Claude Code OAuth token (1 year, setup-token)"); a vault that cannot be read never stops a start.

  `start` records the session id and flags, which is what lets the watchdog (scripts/run-guard.py watch, ticked every
  10 minutes by this repository's scheduled task) resume the run headless if this window is ever lost.

  Before that, this script puts the two per-machine things in place, each derived from where this file is: the
  watchdog's scheduled task, and Claude Code's registration of the plugin folder.

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
  # The shortcut carries the suite icon (Three Lights, docs/design/app-icons.md), never an app's. Its committed
  # raster is D00 T03 §3's to export, so until then the icon is rendered here, per machine like the shortcut itself,
  # from the committed SVGs by that section's ladder and renderer (scripts/requirements-icons.txt): every size from
  # the file the ladder names, at its own pixel size.
  $icon = Join-Path $env:LOCALAPPDATA 'Isotone\isotone-campaign.ico'
  New-Item -ItemType Directory -Force (Split-Path -Parent $icon) | Out-Null
  @'
import io, os, sys
import resvg_py
from PIL import Image
folder, target = sys.argv[1], sys.argv[2]
ladder = {16: "-16", 20: "-16", 24: "-24", 30: "-24", 32: "-32", 40: "", 48: "", 64: "", 128: "", 256: ""}
frames = [Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(
    svg_path=os.path.join(folder, f"isotone{name}.svg"), width=size, height=size)))).convert("RGBA")
    for size, name in ladder.items()]
frames[-1].save(target + ".tmp", format="ICO", sizes=[(n, n) for n in ladder], append_images=frames[:-1])
os.replace(target + ".tmp", target)
'@ | python - (Join-Path $repo 'resources\icons\isotone') $icon
  if ($LASTEXITCODE -ne 0) { throw 'The suite icon could not be rendered: run tools/provision.ps1 (its pydeps leg installs scripts/requirements-icons.txt), then this again.' }

  $link = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Isotone campaign.lnk'
  $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($link)
  $shortcut.TargetPath = (Get-Process -Id $PID).Path
  $shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
  $shortcut.WorkingDirectory = $repo
  $shortcut.IconLocation = "$icon,0"
  $shortcut.Description = 'Start or resume the unattended Isotone campaign'
  $shortcut.Save()
  Write-Host "Shortcut written: $link -> $PSCommandPath"
  return
}

# Without the scheduled tick nothing resumes a session that dies, so the launcher puts it in place. A task left
# pointing at a folder this clone moved away from (STALE) is replaced the same way.
$scheduled = (python scripts/run-guard.py status | Select-Object -Skip 1 | Out-String | ConvertFrom-Json).watchdog
if ($scheduled -ne 'own task') {
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
  if ($LASTEXITCODE -ne 0) { Write-Warning "The plugin folder $marketplace could not be registered, so this session has no language servers." }
  else { Write-Host "Registered the isotone-tools plugin folder at $marketplace." }
}
# Enabled in the project settings is not installed on this machine: the plugin's own state is checked on its own.
$plugin = claude plugin list --json | Out-String | ConvertFrom-Json | Where-Object { $_.id -eq 'isotone-lsp@isotone-tools' -and $_.enabled } | Select-Object -First 1
if (-not $plugin) {
  claude plugin install isotone-lsp@isotone-tools --scope project | Out-Null
  if ($LASTEXITCODE -ne 0) { Write-Warning 'The isotone-lsp plugin could not be installed, so this session has no language servers.' }
}

python scripts/campaign_guard.py start
$code = $LASTEXITCODE
if ($code -eq 3) { Start-Sleep -Seconds 12 }  # nothing was started: leave the reason on screen before the window closes
exit $code
