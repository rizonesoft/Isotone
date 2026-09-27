#Requires -Version 7.0
<#
.SYNOPSIS
  Builds the suite (Isotone.slnx) or a single app.
.DESCRIPTION
  -App All (default) builds every project in Isotone.slnx. -App Stilus|Pinxit|Albumen
  builds that app's startup project and its project references. Output lands in
  artifacts/bin/<Project>/<config>/ (UseArtifactsOutput, see Directory.Build.props).
.EXAMPLE
  pwsh scripts/build.ps1
  pwsh scripts/build.ps1 -Config Debug -App Stilus
#>
[CmdletBinding()]
param(
  [ValidateSet('Debug', 'Release')]
  [string]$Config = 'Release',
  [ValidateSet('All', 'Stilus', 'Pinxit', 'Albumen')]
  [string]$App = 'All',
  [switch]$Test
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/_common.ps1"

Push-Location $RepoRoot
try {
  if ($App -eq 'All') {
    $target = $Solution
  } else {
    $spec = Get-AppSpec $App
    if (-not $spec.Shipping) { throw "$App has no code yet (not shipping); nothing to build." }
    $target = Join-Path $RepoRoot $spec.Project
  }
  Write-Step "dotnet build $([IO.Path]::GetFileName($target)) -c $Config"
  Invoke-Native dotnet build $target -c $Config -nologo
  if ($Test) {
    Write-Step "dotnet test $([IO.Path]::GetFileName($Solution)) -c $Config"
    Invoke-Native dotnet test $Solution -c $Config --no-build -nologo
  }
  Write-Host "build.ps1: $App ($Config) OK" -ForegroundColor Green
} finally {
  Pop-Location
}
