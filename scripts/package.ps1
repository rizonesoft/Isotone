#Requires -Version 7.0
<#
.SYNOPSIS
  Packages an app (or the whole suite) into artifacts/dist/.
.DESCRIPTION
  Runs the native advisory release gate (scripts/check-native-advisories.py --release-gate)
  first so unmapped, unchecked, baseline-mismatch, and advisory blockers stay enforced
  (D00 T04 §3, D00 T06 §2). The native packaging path after the release gate is
  re-planned in D00 T07 §5.
#>
[CmdletBinding(DefaultParameterSetName = 'App')]
param(
  [Parameter(Mandatory, ParameterSetName = 'App')]
  [ValidateSet('Stilus', 'Gesso', 'Albumen')]
  [string]$App,
  [Parameter(Mandatory, ParameterSetName = 'Suite')]
  [switch]$Suite,
  [string]$Version,
  [string]$Runtime = 'win-x64',
  [switch]$SkipPublish,
  [switch]$NoZip
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/_common.ps1"

Write-Step 'native advisory release gate (scripts/check-native-advisories.py --release-gate)'
$global:LASTEXITCODE = 0
& python (Join-Path $PSScriptRoot 'check-native-advisories.py') '--release-gate'
if ($LASTEXITCODE -ne 0) {
  throw "package.ps1: native advisory release gate failed (exit $LASTEXITCODE); release blocked."
}

if (-not $Suite) {
  $null = Get-AppSpec $App
}

Write-Error "package.ps1: has no native packaging work yet; native release packaging is re-planned in D00 T07 §5." -ErrorAction Continue
exit 1
