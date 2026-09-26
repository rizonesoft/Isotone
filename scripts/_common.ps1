# Shared helpers for scripts/*.ps1. Dot-source it: . "$PSScriptRoot/_common.ps1"
Set-StrictMode -Version Latest

$script:RepoRoot = Split-Path -Parent $PSScriptRoot
$script:Apps = Import-PowerShellDataFile (Join-Path $PSScriptRoot 'apps.psd1')
$script:Solution = Join-Path $script:RepoRoot 'Photon.slnx'

function Write-Step([string]$Message) {
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Invoke-Native {
  # Runs a native command and throws on a non-zero exit code. Deliberately a
  # simple function (no param block) so flags like -o reach the command as-is.
  $file, $rest = $args
  & $file @rest
  if ($LASTEXITCODE -ne 0) { throw "$file $($rest -join ' ') failed with exit code $LASTEXITCODE" }
}

function Get-AppSpec([string]$App) {
  if (-not $script:Apps.ContainsKey($App)) {
    throw "Unknown app '$App'. Known: $($script:Apps.Keys -join ', ')"
  }
  return $script:Apps[$App]
}

function Get-ShippingApps {
  return @($script:Apps.Keys | Where-Object { $script:Apps[$_].Shipping } | Sort-Object)
}

function Get-AppVersion {
  # Asks MinVer (through MSBuild) for the version of an app's project, using the
  # app's tag prefix. Returns the SemVer string, e.g. 1.2.3 or 0.0.0-alpha.0.5.
  param([Parameter(Mandatory)][string]$Project, [Parameter(Mandatory)][string]$TagPrefix)
  $path = Join-Path $script:RepoRoot $Project
  $out = & dotnet msbuild $path -nologo -v:q -t:MinVer "-p:MinVerTagPrefix=$TagPrefix" -getProperty:MinVerVersion 2>&1
  if ($LASTEXITCODE -ne 0) { throw "MinVer version query failed for ${Project}: $out" }
  $version = ($out | Where-Object { $_ -match '^\d+\.\d+\.\d+' } | Select-Object -Last 1)
  if (-not $version) { throw "MinVer returned no version for ${Project}: $out" }
  return $version.Trim()
}

function Get-FileVersion([string]$SemVer) {
  # Four-part Win32 file version: Major.Minor.Patch.<CI run number or 0>.
  $core = ($SemVer -split '[-+]')[0]
  $build = 0
  if ($env:GITHUB_RUN_NUMBER) { $build = [int]$env:GITHUB_RUN_NUMBER % 65536 }
  return "$core.$build"
}

function Get-IsccMajor([string]$Path) {
  # ISCC.exe has no version resource; its banner names the major version
  # ("Inno Setup 7 Command-Line Compiler"). Run without arguments it prints the
  # banner and usage, then exits non-zero; only the banner matters here.
  # The whole output is read (no Select-Object -First, which stops the pipeline
  # early and can abort a caller's loop under $ErrorActionPreference = 'Stop').
  $major = 0
  try {
    $text = (& $Path 2>&1 | ForEach-Object { "$_" }) -join "`n"
    if ($text -match 'Inno Setup (\d+) Command-Line Compiler') { $major = [int]$Matches[1] }
  } catch { }
  $global:LASTEXITCODE = 0
  return $major
}

function Find-Iscc {
  # Inno Setup 7 is required: installer/common.iss uses SetupArchitecture=x64 and
  # WizardStyle=modern dynamic, which Inno Setup 6 rejects. $env:ISCC wins when it
  # points at an Inno 7 compiler; Inno 6 installs are skipped, never used.
  $candidates = @(
    $env:ISCC,
    (Join-Path $env:ProgramFiles 'Inno Setup 7\ISCC.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 7\ISCC.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 7\ISCC.exe')
  )
  $cmd = Get-Command ISCC.exe -ErrorAction SilentlyContinue
  if ($cmd) { $candidates += $cmd.Source }
  foreach ($c in $candidates) {
    if ($c -and (Test-Path $c) -and (Get-IsccMajor $c) -ge 7) { return $c }
  }
  throw 'ISCC.exe (Inno Setup 7.1 or newer) not found. Run tools/provision.ps1 or set $env:ISCC.'
}
