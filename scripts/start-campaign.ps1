#Requires -Version 7.2
<#
.SYNOPSIS
  Starts the unattended Isotone campaign in Google Antigravity (`agy`) or Claude Code (`claude`), or picks up a run
  whose session ended, in this window. Nothing else starts or resumes a run.
.DESCRIPTION
  Runs `python scripts/campaign_guard.py start --runner <Runner>`, which takes the session slot (one operating-system
  lock that every campaign session must hold), decides under it, and runs the session in this window until it ends:

  - No run is open: a new session starts under `/goal`, with the goal text campaign_guard.py holds for that runner
    (finish the plan through process-plan, every section stamped, acting autonomously, self-improving, self-healing,
    and building products that beat every competitor), with --dangerously-skip-permissions, on the runner's writer
    model from `scripts/panel_slots.py` (`WRITERS`: `gemini-4-carbon-medium` for agy, `opus` at `--effort medium` for claude).
    Claude Code signs in with the one-year `claude setup-token` token from the Conclave vault.
  - A run is open in this runner and its session died: that same session is resumed, so it still owns the run guard.
  - A run is open in the other runner: it is handed over to a fresh session in this runner, keeping its run file,
    phase, scope, and run id.
  - The slot is held (a campaign session is starting or running in another window), or any other Antigravity or
    Claude Code session is open in this folder or under it: nothing starts, because one session writes.

  A run starts only when you start it, here (operator decision 2026-11-12). Closing this window stops the session and
  everything it started: the session runs inside a job object that ends with the launcher. A crash or a reboot ends
  the session too, and nothing restarts it: there is no scheduled task, no watchdog, and no restart loop in this
  script. When the session ends, this script says how it ended and exits with its exit code; run it again when you
  want the run resumed. `python scripts/run-guard.py status` shows whether the run's session is live or ended.

  Before starting, this script removes the scheduled task "Isotone run watchdog" if an older version of it left one on
  this machine.

  The desktop shortcuts "Isotone Carbon campaign" (agy) and "Isotone Claude campaign" (claude) run this file. Stop the
  run by telling the session to stop: it ends the run through `campaign_guard.py end`, after which this script starts
  a new run instead of resuming that one.
.EXAMPLE
  pwsh -File scripts/start-campaign.ps1 -Runner claude
#>
[CmdletBinding()]
param(
  # The campaign runner: Antigravity on Gemini 4 Carbon (`agy`) or Claude Code (`claude`).
  [ValidateSet('agy', 'claude')]
  [string]$Runner = 'agy',
  # Creates or replaces both desktop shortcuts for this clone ("Isotone Carbon campaign" and "Isotone Claude
  # campaign"), then exits. A shortcut can only hold absolute paths, so every one is derived here from where this file
  # and this PowerShell actually are: run it again after moving the clone.
  [switch]$InstallShortcut
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

if ($InstallShortcut) {
  # Each shortcut carries the suite icon (Three Lights, docs/design/app-icons.md) with its runner's badge in the
  # corner, never an app's icon: a circle in the runner's colour with a white outline and the runner's mark in white.
  # The marks are the official Claude symbol and Google Gemini sparkle (path data from their Wikimedia Commons files,
  # Claude_AI_symbol.svg and Google_Gemini_icon_2025.svg), trademarks of Anthropic and Google, used only for this
  # machine's own launcher icons and shipped in nothing. The suite's committed raster is D00 T03 §3's to export, so
  # until then the icon is rendered here, per machine like the shortcut itself, from the committed SVGs by that
  # section's ladder and renderer (scripts/requirements-icons.txt): every size from the file the ladder names, at its
  # own pixel size. The badge carries its mark from 32 pixels up and its colour alone below that.
  $render = @'
import io, os, sys
import resvg_py
from PIL import Image, ImageDraw
MARKS = {
    "claude": ("0 0 100 100", "m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z"),
    "gemini": ("0 0 65 65", "M32.447 0c.68 0 1.273.465 1.439 1.125a38.904 38.904 0 001.999 5.905c2.152 5 5.105 9.376 8.854 13.125 3.751 3.75 8.126 6.703 13.125 8.855a38.98 38.98 0 005.906 1.999c.66.166 1.124.758 1.124 1.438 0 .68-.464 1.273-1.125 1.439a38.902 38.902 0 00-5.905 1.999c-5 2.152-9.375 5.105-13.125 8.854-3.749 3.751-6.702 8.126-8.854 13.125a38.973 38.973 0 00-2 5.906 1.485 1.485 0 01-1.438 1.124c-.68 0-1.272-.464-1.438-1.125a38.913 38.913 0 00-2-5.905c-2.151-5-5.103-9.375-8.854-13.125-3.75-3.749-8.125-6.702-13.125-8.854a38.973 38.973 0 00-5.905-2A1.485 1.485 0 010 32.448c0-.68.465-1.272 1.125-1.438a38.903 38.903 0 005.905-2c5-2.151 9.376-5.104 13.125-8.854 3.75-3.749 6.703-8.125 8.855-13.125a38.972 38.972 0 001.999-5.905A1.485 1.485 0 0132.447 0z"),
}
folder, target, fill, mark = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
ladder = {16: "-16", 20: "-16", 24: "-24", 30: "-24", 32: "-32", 40: "", 48: "", 64: "", 128: "", 256: ""}
def png(**kw):
    return Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(**kw)))).convert("RGBA")
def frame(size, name):
    tile = png(svg_path=os.path.join(folder, f"isotone{name}.svg"), width=size, height=size)
    scale = 4  # drawn large and reduced, so the badge's edge is smooth at every size
    big = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    r = round(size * scale * 0.24)
    cx = cy = size * scale - r - max(1, round(size * scale * 0.01))
    ring = max(scale, round(size * scale * 0.025))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white")
    d.ellipse((cx - r + ring, cy - r + ring, cx + r - ring, cy + r - ring), fill=fill)
    if size >= 32:
        box, path = MARKS[mark]
        side = round(r * 1.15)
        logo = png(svg_string=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}"><path fill="#fff" d="{path}"/></svg>',
                   width=side, height=side)
        big.alpha_composite(logo, (cx - side // 2, cy - side // 2))
    tile.alpha_composite(big.resize((size, size), Image.LANCZOS))
    return tile
frames = [frame(size, name) for size, name in ladder.items()]
frames[-1].save(target + ".tmp", format="ICO", sizes=[(n, n) for n in ladder], append_images=frames[:-1])
os.replace(target + ".tmp", target)
'@
  $desktop = [Environment]::GetFolderPath('Desktop')
  $icons = Join-Path $env:LOCALAPPDATA 'Isotone'
  New-Item -ItemType Directory -Force $icons | Out-Null
  $shortcuts = @(
    @{ Runner = 'agy'; Name = 'Isotone Carbon campaign'; Icon = 'isotone-campaign-carbon.ico'; Fill = '#4C8DF6'; Mark = 'gemini'
       Description = 'Start or resume the unattended Isotone campaign in Google Antigravity on Gemini 4 Carbon' },
    @{ Runner = 'claude'; Name = 'Isotone Claude campaign'; Icon = 'isotone-campaign-claude.ico'; Fill = '#D97757'; Mark = 'claude'
       Description = 'Start or resume the unattended Isotone campaign in Claude Code' }
  )
  foreach ($s in $shortcuts) {
    $icon = Join-Path $icons $s.Icon
    $render | python - (Join-Path $repo 'resources\icons\isotone') $icon $s.Fill $s.Mark
    if ($LASTEXITCODE -ne 0) { throw 'The shortcut icon could not be rendered: run tools/provision.ps1 (its pydeps leg installs scripts/requirements-icons.txt), then this again.' }
    $link = Join-Path $desktop "$($s.Name).lnk"
    $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($link)
    $shortcut.TargetPath = (Get-Process -Id $PID).Path
    $shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$PSCommandPath`" -Runner $($s.Runner)"
    $shortcut.WorkingDirectory = $repo
    $shortcut.IconLocation = "$icon,0"
    $shortcut.Description = $s.Description
    $shortcut.Save()
    Write-Host "Shortcut written: $link -> $PSCommandPath -Runner $($s.Runner)"
  }
  # The single shortcut and icon this script wrote before the runners split (2026-11-12) start agy without saying so.
  @((Join-Path $desktop 'Isotone campaign.lnk'), (Join-Path $icons 'isotone-campaign.ico')) | Where-Object { Test-Path -LiteralPath $_ } | Remove-Item
  return
}

# Nothing resumes a session that dies (operator decision 2026-11-12). The scheduled task an older version of this
# script installed for that is removed when it is still here; it could start nothing any more, and it should not tick.
$scheduled = (python scripts/run-guard.py status | Select-Object -Skip 1 | Out-String | ConvertFrom-Json).watchdog
if ($scheduled -ne 'MISSING') {
  python scripts/run-guard.py uninstall
  if ($LASTEXITCODE -ne 0) { Write-Warning 'The old watchdog task could not be removed. It starts nothing; remove it in Task Scheduler ("Isotone run watchdog").' }
}

if (-not (Get-Command $Runner -ErrorAction SilentlyContinue)) {
  $cli = @{ agy = 'The Google Antigravity CLI (agy)'; claude = 'The Claude Code CLI (claude)' }[$Runner]
  throw "$cli is not on PATH. Install or add $Runner to PATH, then run this again."
}

python scripts/campaign_guard.py start --runner $Runner
$code = $LASTEXITCODE
# The session is over and this script ends with it: nothing here starts another, after a clean exit or a crash.
# Nothing was started (3) or the session ended on an error: the reason campaign_guard.py printed stays on screen
# before the window closes.
if ($code -ne 0) { Start-Sleep -Seconds 12 }
exit $code
