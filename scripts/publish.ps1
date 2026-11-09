#Requires -Version 7.0
<#
.SYNOPSIS
  Publishes one app into artifacts/publish/<App>/<Runtime>/.
.DESCRIPTION
  Retired during C# removal (D00 T06 §2). Native CMake distribution staging is
  re-planned in D00 T07 §5.
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

$null = Get-AppSpec $App
Write-Error "publish.ps1: has no native work yet; native publish and release packaging are re-planned in D00 T07 §5." -ErrorAction Continue
exit 1
