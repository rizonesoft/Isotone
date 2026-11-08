#Requires -Version 7.2
<#
.SYNOPSIS
  Stages or executes the cross-built ARM64 CTest suites (arm64-debug, arm64-release, arm64-asan) with candidate-identity
  and path-contract verification (D00 T05 §8).
.DESCRIPTION
  With -StageProducer, runs on the x64 producer after building the ARM64 presets: enters scripts/dev-env.ps1 -Arch arm64,
  stages clang_rt.asan_dynamic-aarch64.dll into artifacts/native/arm64-asan-runtime/, computes the SHA-256 digest of
  every built ARM64 executable and DLL, and writes artifacts/native/arm64-artifact.json recording the producer commit,
  workspace path, CMAKE_ROOT, and artifact digest.

  Without -StageProducer, runs on the ARM64 test machine (or with -VerifyOnly in preflight tests): checks
  PROCESSOR_ARCHITECTURE, enters scripts/dev-env.ps1 -Arch arm64, verifies artifacts/native/arm64-artifact.json against
  the target commit and recomputed artifact digest (D00-T05-S5-PR9), verifies that every preset's recorded CMAKE_ROOT and
  workspace path match the machine's bundled CMake and checkout without installing CMake (D00-T05-S5-PR8), checks every
  recorded absolute path in CTestTestfile.cmake and *_include.cmake before discovery runs (D00-T05-S6-PR11), executes
  CTest through the shared test presets (D00-T05-S7-PR3, D00-T05-S5-PR5), and writes artifacts/native/arm64-test-receipt.json.
#>
[CmdletBinding()]
param(
  [Alias('WorkspaceRoot')]
  [string]$Root = (Split-Path -Parent $PSScriptRoot),
  [string]$Commit = '',
  [string]$ExpectedArch = 'ARM64',
  [switch]$StageProducer,
  [switch]$VerifyOnly,
  [switch]$SkipDevEnv
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $Root).Path)
$nativeDir = (Join-Path $repoRoot 'native').Replace('\', '/')
$artifactsRoot = Join-Path $repoRoot 'artifacts/native'
$manifestPath = Join-Path $artifactsRoot 'arm64-artifact.json'
$receiptPath = Join-Path $artifactsRoot 'arm64-test-receipt.json'
$runtimeDir = Join-Path $artifactsRoot 'arm64-asan-runtime'
$presets = @('arm64-debug', 'arm64-release', 'arm64-asan')

function Enter-Arm64Environment {
  . (Join-Path $PSScriptRoot 'dev-env.ps1') -Arch arm64
}

function Get-BundledCMakeRoot {
  $probe = Join-Path ([IO.Path]::GetTempPath()) "isotone-cmake-root-$PID.cmake"
  try {
    Set-Content -LiteralPath $probe -Value 'message(STATUS "CMAKE_ROOT=${CMAKE_ROOT}")' -Encoding utf8NoBOM
    $out = @(cmake -P $probe 2>&1 | ForEach-Object { "$_" })
    foreach ($line in $out) {
      if ($line -match '^--\s*CMAKE_ROOT=(.+)$') {
        return $Matches[1].Trim().Replace('\', '/')
      }
    }
    throw "run-arm64-tests: could not read CMAKE_ROOT from cmake -P"
  }
  finally {
    Remove-Item -LiteralPath $probe -Force -ErrorAction SilentlyContinue
  }
}

function Get-CacheEntry([string]$CacheFile, [string]$Key) {
  foreach ($line in Get-Content -LiteralPath $CacheFile) {
    if ($line -match "^$([Regex]::Escape($Key)):[^=]*=(.*)$") {
      return $Matches[1].Trim().Replace('\', '/')
    }
  }
  return $null
}

function Get-Arm64ArtifactFiles {
  $map = [ordered]@{}
  $folders = @($presets | ForEach-Object { Join-Path $artifactsRoot $_ }) + @($runtimeDir)
  $allFiles = @()
  foreach ($folder in $folders) {
    if (-not (Test-Path -LiteralPath $folder)) { continue }
    $items = Get-ChildItem -LiteralPath $folder -Recurse -File | Where-Object {
      $_.Extension -in @('.exe', '.dll') -and $_.FullName -notmatch '[\\/]CMakeFiles[\\/][^\\/]+[\\/]CompilerId'
    }
    $allFiles += $items
  }
  foreach ($file in ($allFiles | Sort-Object FullName)) {
    $rel = [IO.Path]::GetRelativePath($artifactsRoot, $file.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    $map[$rel] = $hash
  }
  $lines = ($map.GetEnumerator() | ForEach-Object { "$($_.Key):$($_.Value)`n" }) -join ''
  $bytes = [Text.Encoding]::UTF8.GetBytes($lines)
  $sha = [Security.Cryptography.SHA256]::HashData($bytes)
  $digest = ([BitConverter]::ToString($sha)).Replace('-', '').ToLowerInvariant()
  return [pscustomobject]@{
    Files  = $map
    Digest = $digest
  }
}

if (-not $SkipDevEnv) {
  Enter-Arm64Environment
}

if (-not $Commit) {
  $Commit = (git -C $repoRoot rev-parse HEAD 2>&1 | Out-String).Trim()
}

if ($StageProducer) {
  foreach ($preset in $presets) {
    $cache = Join-Path $artifactsRoot "$preset/CMakeCache.txt"
    if (-not (Test-Path -LiteralPath $cache)) {
      Write-Error "run-arm64-tests: preset $preset is not configured at $cache"
      exit 1
    }
  }
  New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null
  $vcBin = Join-Path $env:VCToolsInstallDir 'bin'
  $candidates = @(
    (Join-Path $vcBin 'Hostx64/arm64/clang_rt.asan_dynamic-aarch64.dll'),
    (Join-Path $vcBin 'HostArm64/arm64/clang_rt.asan_dynamic-aarch64.dll')
  )
  $asanDll = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
  if (-not $asanDll) {
    Write-Error "run-arm64-tests: clang_rt.asan_dynamic-aarch64.dll not found under $vcBin"
    exit 1
  }
  Copy-Item -LiteralPath $asanDll -Destination (Join-Path $runtimeDir 'clang_rt.asan_dynamic-aarch64.dll') -Force
  $firstCache = Join-Path $artifactsRoot 'arm64-debug/CMakeCache.txt'
  $recordedWorkspace = Get-CacheEntry $firstCache 'CMAKE_HOME_DIRECTORY'
  $recordedCMakeRoot = Get-CacheEntry $firstCache 'CMAKE_ROOT'
  $computed = Get-Arm64ArtifactFiles
  if ($computed.Files.Count -eq 0) {
    Write-Error 'run-arm64-tests: no ARM64 executables or DLLs found to stage'
    exit 1
  }
  $manifest = [ordered]@{
    schema          = 1
    commit          = $Commit
    workspace       = $recordedWorkspace
    cmake_root      = $recordedCMakeRoot
    artifact_digest = $computed.Digest
    files           = $computed.Files
  }
  $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8NoBOM
  Write-Host "run-arm64-tests: staged $($computed.Files.Count) file(s), commit $Commit, digest $($computed.Digest)"
  exit 0
}

Write-Host "PROCESSOR_ARCHITECTURE=$($env:PROCESSOR_ARCHITECTURE)"
if ($env:PROCESSOR_ARCHITECTURE -ne $ExpectedArch) {
  Write-Host "run-arm64-tests: host architecture mismatch: found '$($env:PROCESSOR_ARCHITECTURE)', expected '$ExpectedArch'"
  exit 1
}

if (-not (Test-Path -LiteralPath $manifestPath)) {
  Write-Host "run-arm64-tests: missing artifact manifest at $manifestPath"
  exit 1
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($manifest.commit -ne $Commit) {
  Write-Host "run-arm64-tests: commit mismatch: manifest recorded '$($manifest.commit)', expected '$Commit'"
  exit 1
}
$computed = Get-Arm64ArtifactFiles
if ($computed.Digest -ne $manifest.artifact_digest) {
  Write-Host "run-arm64-tests: artifact digest mismatch: computed '$($computed.Digest)', manifest recorded '$($manifest.artifact_digest)'"
  exit 1
}

$runnerCMakeRoot = Get-BundledCMakeRoot
foreach ($preset in $presets) {
  $presetDir = Join-Path $artifactsRoot $preset
  $cache = Join-Path $presetDir 'CMakeCache.txt'
  if (-not (Test-Path -LiteralPath $cache)) {
    Write-Host "run-arm64-tests: missing CMakeCache.txt for $preset at $cache"
    exit 1
  }
  $cacheRoot = Get-CacheEntry $cache 'CMAKE_ROOT'
  if (-not $cacheRoot -or -not $cacheRoot.Equals($runnerCMakeRoot, [StringComparison]::OrdinalIgnoreCase)) {
    Write-Host "run-arm64-tests: CMAKE_ROOT mismatch in ${preset}: producer recorded '$cacheRoot', runner has '$runnerCMakeRoot'"
    exit 1
  }
  $cacheHome = Get-CacheEntry $cache 'CMAKE_HOME_DIRECTORY'
  $normalizedCacheHome = if ($cacheHome -and (Test-Path -LiteralPath $cacheHome)) {
    [IO.Path]::GetFullPath($cacheHome).Replace('\', '/')
  } else {
    $cacheHome
  }
  if (-not $normalizedCacheHome -or -not $normalizedCacheHome.Equals($nativeDir, [StringComparison]::OrdinalIgnoreCase)) {
    Write-Host "run-arm64-tests: workspace path mismatch in ${preset}: producer recorded '$cacheHome', runner has '$nativeDir'"
    exit 1
  }

  $cmakeFiles = @(Get-ChildItem -LiteralPath $presetDir -Recurse -File | Where-Object {
    $_.Name -eq 'CTestTestfile.cmake' -or $_.Name -like '*_include.cmake'
  } | Sort-Object FullName)
  if ($cmakeFiles.Count -eq 0) {
    Write-Host "run-arm64-tests: no CTestTestfile.cmake found in $presetDir"
    exit 1
  }
  foreach ($file in $cmakeFiles) {
    $relFile = [IO.Path]::GetRelativePath($repoRoot, $file.FullName).Replace('\', '/')
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
      $cleaned = $line -replace '\[=*\[(.*?)\]=*\]', '"$1"'
      $matchesFound = [Regex]::Matches($cleaned, '(?<![A-Za-z0-9_])([A-Za-z]:/[^"''\r\n;)]+)')
      foreach ($m in $matchesFound) {
        $recorded = $m.Groups[1].Value.Trim()
        # Generated *_tests.cmake files and -DWORK scratch directories are created at test time; their parent folder must exist.
        $checkPath = if ($recorded -match '\]_tests\.cmake$' -or $line -match "-DWORK=$([Regex]::Escape($recorded))") {
          Split-Path -Parent $recorded
        } else {
          $recorded
        }
        if (-not (Test-Path -LiteralPath $checkPath)) {
          Write-Host "run-arm64-tests: missing recorded path in ${relFile}: '$recorded' does not exist on this machine"
          exit 1
        }
      }
    }
  }
}

Write-Host "run-arm64-tests: preflight ok (commit $Commit, digest $($computed.Digest), CMAKE_ROOT $runnerCMakeRoot)"
if ($VerifyOnly) {
  exit 0
}

$allPassed = $true
$presetResults = [ordered]@{}
Push-Location (Join-Path $repoRoot 'native')
try {
  foreach ($preset in $presets) {
    $presetDir = Join-Path $artifactsRoot $preset
    $junitPath = Join-Path $presetDir "junit-$preset.xml"
    if ($preset -eq 'arm64-asan') {
      Write-Host "run-arm64-tests: arm64-asan environment ASAN_OPTIONS=halt_on_error=1:detect_leaks=0:log_path=asan.log PATH prepends $runtimeDir"
    }
    Write-Host "run-arm64-tests: running ctest --preset $preset --timeout 300 --output-junit $junitPath"
    ctest --preset $preset --timeout 300 --output-junit $junitPath
    $code = $LASTEXITCODE
    $presetResults[$preset] = ($code -eq 0)
    if ($code -ne 0) {
      $allPassed = $false
    }
  }
}
finally {
  Pop-Location
}

$asanReports = @(Get-ChildItem -LiteralPath (Join-Path $artifactsRoot 'arm64-asan') -Recurse -File -Filter 'asan.log.*' -ErrorAction SilentlyContinue)
$probeReportFound = $false
foreach ($report in $asanReports) {
  $text = Get-Content -LiteralPath $report.FullName -Raw
  if ($text -match 'SUMMARY: AddressSanitizer: heap-buffer-overflow [^\r\n]*asan_probe_test\.cpp') {
    Write-Host "ASAN_OPTIONS=halt_on_error=1:detect_leaks=0:log_path=asan.log"
    Write-Host $Matches[0]
    $probeReportFound = $true
  }
}
if (-not $probeReportFound) {
  Write-Host 'run-arm64-tests: arm64-asan did not retain the expected asan_probe heap-buffer-overflow report'
  $allPassed = $false
}

$receipt = [ordered]@{
  schema                 = 1
  commit                 = $Commit
  artifact_digest        = $computed.Digest
  processor_architecture = $env:PROCESSOR_ARCHITECTURE
  cmake_root             = $runnerCMakeRoot
  workspace              = $nativeDir
  presets                = $presetResults
  passed                 = $allPassed
  timestamp              = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
}
$receipt | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $receiptPath -Encoding utf8NoBOM

if (-not $allPassed) {
  Write-Host 'run-arm64-tests: one or more ARM64 test presets failed'
  exit 1
}
Write-Host "run-arm64-tests: all ARM64 test presets passed (receipt written to $receiptPath)"
exit 0
