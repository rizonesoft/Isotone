#Requires -Version 7.2
<#
.SYNOPSIS
  Runs the pinned clang-tidy over every native translation unit in the x64 Debug compile database (D00 T05 §4).
.DESCRIPTION
  Enters scripts/dev-env.ps1, configures and builds the x64-debug preset (the compile database comes from configuring,
  and the generated build id header from building), then runs clang-tidy -p <build folder> on every translation unit
  under native/ that the database lists, in parallel, with native/.clang-tidy (every warning an error). Names each
  translation unit with a diagnostic and its first diagnostics. -Root points it at another tree (the tests' scratch
  one), and -SkipBuild uses the compile database as it is. Exit 0 clean, 1 a diagnostic, 2 a build or tool failure or
  no translation unit to check.
.EXAMPLE
  pwsh scripts/native-tidy.ps1
#>
[CmdletBinding()]
param(
  [string]$Preset = 'x64-debug',
  [string]$Root = (Split-Path -Parent $PSScriptRoot),
  [switch]$SkipBuild,
  [int]$MaxJobs = 0
)
$ErrorActionPreference = 'Stop'
# GetFullPath expands an 8.3 short name (C:\Users\DERICK~1) to the long one, as it does for every compile database
# path below, so both sides of the under-native/ comparison take the same form.
$root = [IO.Path]::GetFullPath((Resolve-Path $Root).Path)
$buildDir = Join-Path $root "artifacts\native\$Preset"

function Enter-NativeEnvironment {
  # Dot-sourced inside a function, so dev-env's parameters stay out of this script's scope; the environment it enters
  # is the process's.
  . (Join-Path $PSScriptRoot 'dev-env.ps1') -Arch x64
}
Enter-NativeEnvironment

if (-not $SkipBuild) {
  Push-Location (Join-Path $root 'native')
  try {
    $configure = cmake --preset $Preset 2>&1
    if ($LASTEXITCODE -ne 0) { $configure | Select-Object -Last 10 | ForEach-Object { "$_" }; "native-tidy: configuring $Preset failed"; exit 2 }
    $build = cmake --build --preset $Preset 2>&1
    if ($LASTEXITCODE -ne 0) { $build | Select-Object -Last 10 | ForEach-Object { "$_" }; "native-tidy: building $Preset failed"; exit 2 }
  }
  finally { Pop-Location }
}

$database = Join-Path $buildDir 'compile_commands.json'
if (-not (Test-Path $database)) { "native-tidy: no compile database at $database"; exit 2 }
$native = (Join-Path $root 'native') + [IO.Path]::DirectorySeparatorChar
$entries = @(Get-Content -Raw $database | ConvertFrom-Json)
$unitMap = @{}
foreach ($e in $entries) {
  $full = [IO.Path]::GetFullPath($e.file, $buildDir)
  if ($full.StartsWith($native, [StringComparison]::OrdinalIgnoreCase) -and -not $unitMap.ContainsKey($full)) {
    $unitMap[$full] = $buildDir
  }
}
if ($Preset -eq 'x64-debug') {
  $relBuildDir = Join-Path $root 'artifacts\native\x64-release'
  $relDatabase = Join-Path $relBuildDir 'compile_commands.json'
  if (-not $SkipBuild -and (Test-Path (Join-Path $root 'native\benchmarks\CMakeLists.txt'))) {
    Push-Location (Join-Path $root 'native')
    try {
      $configure = cmake --preset x64-release 2>&1
      if ($LASTEXITCODE -ne 0) { $configure | Select-Object -Last 10 | ForEach-Object { "$_" }; "native-tidy: configuring x64-release failed"; exit 2 }
      $build = cmake --build --preset x64-release 2>&1
      if ($LASTEXITCODE -ne 0) { $build | Select-Object -Last 10 | ForEach-Object { "$_" }; "native-tidy: building x64-release failed"; exit 2 }
    }
    finally { Pop-Location }
  }
  if (Test-Path $relDatabase) {
    $relEntries = @(Get-Content -Raw $relDatabase | ConvertFrom-Json)
    foreach ($e in $relEntries) {
      $full = [IO.Path]::GetFullPath($e.file, $relBuildDir)
      if ($full.StartsWith($native, [StringComparison]::OrdinalIgnoreCase) -and -not $unitMap.ContainsKey($full)) {
        $unitMap[$full] = $relBuildDir
      }
    }
  }
}
$units = @($unitMap.Keys | Sort-Object -Unique)
if (-not $units) { "native-tidy: no translation unit under native/ in $database"; exit 2 }

# WORKAROUND: clang-cl does not implement MSVC's /Zc:preprocessor and /external:anglebrackets, which the database carries
# for cl; left in, it reports them unused, and the database's /WX makes that an error before any check runs. Removing
# exactly these two keeps the unused-argument error live for any other switch clang-cl does not know.
$removed = @('--removed-arg=/Zc:preprocessor', '--removed-arg=/external:anglebrackets')
$throttle = if ($MaxJobs -gt 0) {
  $MaxJobs
} elseif ($env:ISOTONE_TIDY_JOBS -match '^\d+$' -and [int]$env:ISOTONE_TIDY_JOBS -gt 0) {
  [int]$env:ISOTONE_TIDY_JOBS
} else {
  [Math]::Clamp([Environment]::ProcessorCount - 2, 1, 8)
}
$results = $units | ForEach-Object -ThrottleLimit $throttle -Parallel {
  $unitBuildDir = ($using:unitMap)[$_]
  $out = clang-tidy -p $unitBuildDir --quiet @using:removed $_ 2>&1 | ForEach-Object { "$_" }
  # A diagnostic is `file:line:col: error: ...` or, for a command-line problem, `error: ...` at the start of the line.
  [pscustomobject]@{ File = $_; Code = $LASTEXITCODE; Diagnostics = @($out | Where-Object { $_ -match '(^|: )(warning|error): ' }) }
}
$failing = @($results | Where-Object { $_.Code -ne 0 -or $_.Diagnostics })
foreach ($r in $failing | Sort-Object File) {
  "FAIL $([IO.Path]::GetRelativePath($root, $r.File)) (exit $($r.Code))"
  $r.Diagnostics | Select-Object -First 10 | ForEach-Object { "  $_" }
}
"native-tidy: $($units.Count) translation unit(s), $($failing.Count) with diagnostics"
exit $(if ($failing) { 1 } else { 0 })
