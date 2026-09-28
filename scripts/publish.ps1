#Requires -Version 7.0
<#
.SYNOPSIS
  Publishes one app as a self-contained, single-folder, ReadyToRun build.
.DESCRIPTION
  Output: artifacts/publish/<App>/<Runtime>/ (symbols moved to
  artifacts/publish/<App>/<Runtime>-symbols/ so installers and ZIPs ship without
  them). MinVerTagPrefix is passed as a global property, so every project in the
  app's closure, including shared libraries, carries the app's version. -Version
  overrides MinVer (MinVerVersionOverride) for re-builds of a known version.
.EXAMPLE
  pwsh scripts/publish.ps1 -App Stilus
  pwsh scripts/publish.ps1 -App Gesso -Runtime win-arm64
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)]
  [ValidateSet('Stilus', 'Gesso', 'Albumen')]
  [string]$App,
  [string]$Runtime = 'win-x64',
  [ValidateSet('Debug', 'Release')]
  [string]$Config = 'Release',
  [string]$Version,
  [switch]$NoReadyToRun
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/_common.ps1"

$spec = Get-AppSpec $App
if (-not $spec.Shipping) { throw "$App is not shipping yet (no code); publish refused." }

$project = Join-Path $RepoRoot $spec.Project
$out = Join-Path $RepoRoot "artifacts/publish/$App/$Runtime"
$symbols = "$out-symbols"
foreach ($dir in @($out, $symbols)) {
  if (Test-Path $dir) { Remove-Item -Recurse -Force $dir }
}

$props = @(
  "-p:MinVerTagPrefix=$($spec.TagPrefix)",
  '-p:SelfContained=true',
  '-p:PublishSingleFile=false',
  "-p:PublishReadyToRun=$((-not $NoReadyToRun).ToString().ToLowerInvariant())",
  '-p:SatelliteResourceLanguages=en'
)
if ($Version) { $props += "-p:MinVerVersionOverride=$Version" }

Push-Location $RepoRoot
try {
  Write-Step "publish $App ($Config, $Runtime, self-contained)"
  Invoke-Native dotnet publish $project -c $Config -r $Runtime -o $out -nologo @props

  $pdbs = @(Get-ChildItem $out -Filter *.pdb -Recurse)
  if ($pdbs.Count -gt 0) {
    New-Item -ItemType Directory -Force -Path $symbols | Out-Null
    $pdbs | Move-Item -Destination $symbols -Force
  }
  $exe = Join-Path $out $spec.Exe
  if (-not (Test-Path $exe)) { throw "publish produced no $($spec.Exe) in $out" }
  $size = (Get-ChildItem $out -Recurse -File | Measure-Object Length -Sum).Sum / 1MB
  $ver = (Get-Item $exe).VersionInfo
  Write-Host ("publish.ps1: {0} {1} (file {2}) -> {3} ({4:N1} MB)" -f $App, $ver.ProductVersion, $ver.FileVersion, $out, $size) -ForegroundColor Green
} finally {
  Pop-Location
}
