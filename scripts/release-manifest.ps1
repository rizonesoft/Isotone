#Requires -Version 7.0
<#
.SYNOPSIS
  Writes the release body and the update feed for one release from artifacts/dist/.
.DESCRIPTION
  Binaries are distributed only from download.rizonesoft.com (operator decision
  2026-09-27); a GitHub release carries the notes, GitHub's source archives, the
  SHA-256 table, and links to the files. This script writes, under -OutDir:

    body.md                        the GitHub release body: the CHANGELOG notes (from
                                   -NotesFile, when it exists), Download links, the
                                   SHA-256 table, and the source link (the tag)
    update/<slug>.json             the update feed for a stable release, or
    update/<slug>-prerelease.json  the feed for a prerelease (a hyphenated version)
    files.txt                      the public URL of every file, one per line

  Layout on the storage: <base>/<prefix><slug>/<version>/<file>, the feed at
  <base>/<prefix>update/<feed>.json. <slug> is stilus, pinxit, albumen, or isotone (the
  suite). -KeyPrefix is empty for a release and 'drafts/' for a draft dry run, so a
  draft never touches the live paths or the live feed.

  It uploads nothing: release.yml uploads what it lists.
.EXAMPLE
  pwsh scripts/release-manifest.ps1 -Slug stilus -Name Stilus -Version 0.1.0 -Tag stilus-v0.1.0
#>
param(
  [Parameter(Mandatory)][ValidateSet('stilus', 'pinxit', 'albumen', 'isotone')][string]$Slug,
  [Parameter(Mandatory)][string]$Name,
  [Parameter(Mandatory)][string]$Version,
  [Parameter(Mandatory)][string]$Tag,
  [string]$BaseUrl = 'https://download.rizonesoft.com',
  [string]$SiteUrl = 'https://www.rizonesoft.com/',
  [string]$KeyPrefix = '',
  [string]$Dist,
  [string]$NotesFile,
  [string]$OutDir,
  [string]$Repository = 'rizonesoft/Isotone',
  # False when the files were not uploaded (a draft without storage configured):
  # the body then says so instead of offering links that do not resolve.
  [bool]$Uploaded = $true
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $Dist) { $Dist = Join-Path $repoRoot 'artifacts/dist' }
if (-not $OutDir) { $OutDir = Join-Path $repoRoot 'artifacts/release' }
if ($KeyPrefix -and -not $KeyPrefix.EndsWith('/')) { $KeyPrefix += '/' }
$BaseUrl = $BaseUrl.TrimEnd('/')

function Get-UtmUrl([string]$Url, [string]$Medium) {
  $sep = if ($Url.Contains('?')) { '&' } else { '?' }
  return "$Url${sep}utm_source=github&utm_medium=$Medium"
}

function Format-Size([long]$Bytes) {
  $inv = [Globalization.CultureInfo]::InvariantCulture
  if ($Bytes -ge 1MB) { return [string]::Format($inv, '{0:N1} MB', $Bytes / 1MB) }
  if ($Bytes -ge 1KB) { return [string]::Format($inv, '{0:N1} KB', $Bytes / 1KB) }
  return "$Bytes bytes"
}

$binaries = @(Get-ChildItem -LiteralPath $Dist -File | Where-Object { $_.Extension -in '.exe', '.zip' } |
    Sort-Object @{ Expression = { if ($_.Name -like '*-Setup.exe') { 0 } else { 1 } } }, Name)
if ($binaries.Count -eq 0) { throw "No installer or ZIP in $Dist" }
$sums = Join-Path $Dist 'SHA256SUMS'
if (-not (Test-Path -LiteralPath $sums)) { throw "SHA256SUMS missing in $Dist" }

$folderUrl = "$BaseUrl/$KeyPrefix$Slug/$Version"
$files = foreach ($f in $binaries) {
  $kind = if ($f.Name -like '*-Setup.exe') { 'installer' } elseif ($f.Name -like '*-Portable.zip') { 'portable' } else { 'other' }
  $runtime = if ($f.Name -match '-(win-(?:x64|arm64))-') { $Matches[1] } else { '' }
  [ordered]@{
    name    = $f.Name
    kind    = $kind
    runtime = $runtime
    url     = "$folderUrl/$($f.Name)"
    sha256  = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    size    = $f.Length
  }
}
# Every hash in the feed and the body must be the hash SHA256SUMS states.
$listed = @{}
foreach ($line in Get-Content -LiteralPath $sums) {
  if ($line -match '^([0-9a-f]{64})\s+\*?(.+)$') { $listed[$Matches[2].Trim()] = $Matches[1] }
}
foreach ($f in $files) {
  if ($listed[$f.name] -ne $f.sha256) { throw "SHA256SUMS does not match $($f.name)" }
}

$prerelease = $Version.Contains('-')
$installer = $files | Where-Object { $_.kind -eq 'installer' -and $_.runtime -eq 'win-x64' } | Select-Object -First 1
if (-not $installer) { $installer = $files | Select-Object -First 1 }
$repoUrl = "https://github.com/$Repository"
$feedName = if ($prerelease) { "$Slug-prerelease" } else { $Slug }

$feed = [ordered]@{
  schema     = 1
  app        = $Slug
  name       = $Name
  version    = $Version
  prerelease = $prerelease
  date       = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')
  tag        = $Tag
  url        = $installer.url
  sha256     = $installer.sha256
  size       = $installer.size
  notes      = "$repoUrl/releases/tag/$Tag"
  page       = $SiteUrl
  source     = "$repoUrl/tree/$Tag"
  sha256sums = "$folderUrl/SHA256SUMS"
  files      = @($files)
}

New-Item -ItemType Directory -Force -Path (Join-Path $OutDir 'update') | Out-Null
$feedPath = Join-Path $OutDir "update/$feedName.json"
$feed | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $feedPath -Encoding utf8NoBOM

$urls = @($files | ForEach-Object { $_.url }) + "$folderUrl/SHA256SUMS"
$urls | Set-Content -LiteralPath (Join-Path $OutDir 'files.txt') -Encoding utf8NoBOM

$body = [System.Collections.Generic.List[string]]::new()
$notes = if ($NotesFile -and (Test-Path -LiteralPath $NotesFile)) { (Get-Content -LiteralPath $NotesFile -Raw).Trim() } else { '' }
if ($notes) { $body.Add($notes) }
else { $body.Add("No CHANGELOG section names ``$Tag``; see the [commits]($repoUrl/commits/$Tag).") }
$body.Add('')
$body.Add('## Download')
$body.Add('')
$site = Get-UtmUrl $SiteUrl 'release'
if ($Uploaded) {
  $body.Add("Official builds are published only on [rizonesoft.com]($site), served from ``download.rizonesoft.com``. This release has no attached binaries; download them here:")
} else {
  $body.Add("**Draft dry run: these files were not uploaded** (the distribution storage is not configured). A published release offers them at these addresses; the files of this run are in the workflow run's ``dist-$Tag`` artifact.")
}
$body.Add('')
foreach ($f in $files) { $body.Add("- [$($f.name)]($($f.url)) ($(Format-Size $f.size))") }
$body.Add("- [SHA256SUMS]($folderUrl/SHA256SUMS)")
$body.Add('')
$body.Add('## SHA-256')
$body.Add('')
$body.Add('| File | SHA-256 |')
$body.Add('| ---- | ------- |')
foreach ($f in $files) { $body.Add("| ``$($f.name)`` | ``$($f.sha256)`` |") }
$body.Add('')
$body.Add('Check a download before you run it: `(Get-FileHash <file> -Algorithm SHA256).Hash` must equal the value above.')
$body.Add('')
$body.Add('## Source code')
$body.Add('')
$body.Add("The complete source of this release is the tag [``$Tag``]($repoUrl/tree/$Tag); GitHub's source code archives below are that tag. Free software under the [GNU General Public License v3.0]($repoUrl/blob/$Tag/LICENSE).")
$body.Add('')
$body.Add('Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. Rizonesoft is a brand of Rizonetech (Pty) Ltd.')
$body -join "`n" | Set-Content -LiteralPath (Join-Path $OutDir 'body.md') -Encoding utf8NoBOM

Write-Host "body.md, update/$feedName.json, and files.txt written to $OutDir ($($files.Count) files under $folderUrl)"
