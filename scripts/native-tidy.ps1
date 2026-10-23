#Requires -Version 7.2
<#
.SYNOPSIS
  Runs the pinned clang-tidy over every native translation unit in the x64 Debug compile database (D00 T05 §4).
.DESCRIPTION
  Enters scripts/dev-env.ps1, configures and builds the x64-debug preset (the compile database comes from configuring,
  and the generated build id header from building), then runs clang-tidy -p <build folder> on every translation unit
  under native/ that the database lists, in parallel, with native/.clang-tidy (every warning an error). Names each
  translation unit with a diagnostic and its first diagnostics. Exit 0 clean, 1 a diagnostic, 2 a build or tool failure.
.EXAMPLE
  pwsh scripts/native-tidy.ps1
#>
[CmdletBinding()]
param([string]$Preset = 'x64-debug')
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$buildDir = Join-Path $root "artifacts\native\$Preset"

function Enter-NativeEnvironment {
  # Dot-sourced inside a function, so dev-env's parameters stay out of this script's scope; the environment it enters
  # is the process's.
  . (Join-Path $PSScriptRoot 'dev-env.ps1') -Arch x64
}
Enter-NativeEnvironment

Push-Location (Join-Path $root 'native')
try {
  $configure = cmake --preset $Preset 2>&1
  if ($LASTEXITCODE -ne 0) { $configure | Select-Object -Last 10 | ForEach-Object { "$_" }; "native-tidy: configuring $Preset failed"; exit 2 }
  $build = cmake --build --preset $Preset 2>&1
  if ($LASTEXITCODE -ne 0) { $build | Select-Object -Last 10 | ForEach-Object { "$_" }; "native-tidy: building $Preset failed"; exit 2 }
}
finally { Pop-Location }

$native = (Join-Path $root 'native') + [IO.Path]::DirectorySeparatorChar
$units = @(Get-Content -Raw (Join-Path $buildDir 'compile_commands.json') | ConvertFrom-Json |
  ForEach-Object { [IO.Path]::GetFullPath($_.file) } |
  Where-Object { $_.StartsWith($native, [StringComparison]::OrdinalIgnoreCase) } |
  Sort-Object -Unique)
if (-not $units) { "native-tidy: no translation unit under native/ in $buildDir"; exit 2 }

$results = $units | ForEach-Object -ThrottleLimit ([Environment]::ProcessorCount) -Parallel {
  $out = clang-tidy -p $using:buildDir --quiet $_ 2>&1 | ForEach-Object { "$_" }
  [pscustomobject]@{ File = $_; Code = $LASTEXITCODE; Diagnostics = @($out | Where-Object { $_ -match ': (warning|error): ' }) }
}
$failing = @($results | Where-Object { $_.Code -ne 0 -or $_.Diagnostics })
foreach ($r in $failing | Sort-Object File) {
  "FAIL $([IO.Path]::GetRelativePath($root, $r.File)) (exit $($r.Code))"
  $r.Diagnostics | Select-Object -First 10 | ForEach-Object { "  $_" }
}
"native-tidy: $($units.Count) translation unit(s), $($failing.Count) with diagnostics"
exit $(if ($failing) { 1 } else { 0 })
