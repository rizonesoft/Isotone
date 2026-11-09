#Requires -Version 7.0
<#
.SYNOPSIS
  Builds the suite or a single app.
.DESCRIPTION
  Retired during C# removal (D00 T06 §2). The native CMake build runs through
  scripts/dev-env.ps1 and scripts/check-all.ps1; this wrapper is re-planned for
  the native release and build path in D00 T07 §5.
#>
[CmdletBinding()]
param(
  [ValidateSet('Debug', 'Release')]
  [string]$Config = 'Release',
  [ValidateSet('All', 'Stilus', 'Gesso', 'Albumen')]
  [string]$App = 'All',
  [switch]$Test
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/_common.ps1"

Write-Error "build.ps1: has no native work yet; native build and release scripts are re-planned in D00 T07 §5 (use scripts/dev-env.ps1 and cmake --preset / ctest --preset, or pwsh scripts/check-all.ps1)." -ErrorAction Continue
exit 1
