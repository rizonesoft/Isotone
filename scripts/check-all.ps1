#Requires -Version 7.0
<#
.SYNOPSIS
  Runs every local gate: build (Debug and Release), tests, and the plan tooling.
.DESCRIPTION
  1. dotnet build Isotone.slnx -c Debug and -c Release (skipped with -SkipBuild)
  2. dotnet test Isotone.slnx (-Config, default Release)
  3. python scripts/todo-graph.py self-test
  4. python scripts/todo-graph.py validate
  5. python scripts/todo-graph.py plan --check
  6. python scripts/todo-claims.py
  7. python scripts/todo-findings.py --check
  8. python scripts/todo-runs.py --check
  9. python scripts/campaign_guard.py --self-test
  10. python scripts/build-design-site.py --check (docs/design/index.html is current), then
      python scripts/build-app-icons.py --check (the app icon SVGs match their generator)
  11. python scripts/design-lint.py --self-test
  12. python scripts/design-lint.py --baseline docs/design/.lint-baseline.json
      (no new design-contract violation in the UI sources; standards/design-contract.md)
  13. python scripts/panel_slots.py --self-test
  14. python scripts/panel_slots.py validate (the reviewer pin, the delegate pin,
      and the .claude/agents definitions; standards/delegation.md)
  15. python scripts/review-dispatch.py --check-pin (the reviewer pin loads under
      the dispatcher's rules)
  16. python scripts/tests/test_review_dispatch.py (the dispatcher's routing,
      read-only invocations, records, and --keep, with fake reviewer CLIs)
  17. python scripts/weakening-scan.py --self-test
  18. python scripts/tests/test_automations.py (the scheduled tasks, their
      runner, alert, and installers; .conclave/automations/README.md)
  19. python scripts/tests/test_pin_automations.py (the pin checks and the
      settings hook scripts)
  20. python scripts/tests/test_merge_prs.py (the dependency pull request
      merger, D00 T01 §12)
  21. python scripts/ci_watch.py --self-test (the section-boundary watch over
      every workflow's latest run on main, scheduled ones included)
  22. python scripts/tests/test_build_props.py (a WPF temporary project shares
      its parent's artifacts folders, D00 T02 §3; asks the pinned SDK)
  23. The native stages (skipped with -SkipNative), each inside scripts/dev-env.ps1
      where it builds or inspects, its full output in build/check-all/<stage>.log:
      native toolchain (dev-env.ps1 -Check for x64 and arm64); native x64-debug,
      x64-release, and x64-asan (cmake --workflow: configure, build, test); native
      arm64-debug, arm64-release, and arm64-asan (configure and build: an ARM64
      test runs on ARM64, D00 T05 §8); native x64-dist and arm64-dist; native
      analyze (x64-analyze and arm64-analyze); native std (native-std-check.py
      over every preset folder); native pe (native-pe-check.py over every preset
      folder); native format (native-format.ps1 -Check); native tidy
      (native-tidy.ps1); native artifacts (native-artifact-gate.py --policy
      shipping --require-built: Debug, Release, analyze, and dist); native
      artifacts asan (--policy asan --require-built); native asan-coverage
      (--asan-coverage --require-built); and the native Python gates, the
      self-tests of native-std-check.py, native-pe-check.py, and
      native-artifact-gate.py, then test_dev_env.py, test_native_format.py,
      test_native_tidy.py, and test_native_asan.py.
  A python gate whose script is absent is skipped with a warning. Every gate
  runs even after an earlier failure; the exit code is 1 when any gate failed.
.EXAMPLE
  pwsh scripts/check-all.ps1
  pwsh scripts/check-all.ps1 -SkipBuild
  pwsh scripts/check-all.ps1 -SkipNative
#>
[CmdletBinding()]
param(
  [switch]$SkipBuild,
  [switch]$SkipNative,
  [ValidateSet('Debug', 'Release')]
  [string]$Config = 'Release'
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/_common.ps1"

$results = [System.Collections.Generic.List[object]]::new()

function Invoke-Gate([string]$Name, [scriptblock]$Body) {
  Write-Step $Name
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $status = 'PASS'
  try {
    $global:LASTEXITCODE = 0
    & $Body
    if ($LASTEXITCODE -ne 0) { $status = "FAIL (exit $LASTEXITCODE)" }
  } catch {
    $status = "FAIL ($($_.Exception.Message))"
  }
  $results.Add([pscustomobject]@{ Gate = $Name; Status = $status; Seconds = [math]::Round($sw.Elapsed.TotalSeconds, 1) })
}

function Invoke-PythonGate([string]$Name, [string]$Script, [string[]]$Arguments) {
  $path = Join-Path $RepoRoot "scripts/$Script"
  if (-not (Test-Path $path)) {
    Write-Warning "check-all: $Script not found; skipping '$Name'"
    $results.Add([pscustomobject]@{ Gate = $Name; Status = 'SKIP (script absent)'; Seconds = 0 })
    return
  }
  $py = $script:Python
  Invoke-Gate $Name ({ & $py $path @Arguments }.GetNewClosure())
}

function Invoke-NativeGate([string]$Name, [string[]]$Command) {
  # The stage's full output goes to build/check-all/<stage>.log; a failing stage prints its last lines.
  $log = Join-Path $RepoRoot "build/check-all/$($Name -replace '[^\w-]+', '-').log"
  New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
  Invoke-Gate $Name ({
      & $Command[0] @($Command | Select-Object -Skip 1) *> $log
      if ($LASTEXITCODE -ne 0) { Get-Content $log -Tail 15 | Write-Host; Write-Host "check-all: full log $log" }
    }.GetNewClosure())
}

function Invoke-InNative([string]$Name, [string]$Arch, [string]$Block) {
  Invoke-NativeGate $Name @('pwsh', '-NoProfile', '-File', (Join-Path $RepoRoot 'scripts/dev-env.ps1'), '-Arch', $Arch,
    '-Run', $Block)
}

$script:Python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command python3 -ErrorAction SilentlyContinue) { 'python3' } else { $null }

Push-Location $RepoRoot
try {
  if (-not $SkipBuild) {
    Invoke-Gate 'build Debug' { dotnet build $Solution -c Debug -nologo }
    Invoke-Gate 'build Release' { dotnet build $Solution -c Release -nologo }
  }
  $noBuild = @()
  if (-not $SkipBuild) { $noBuild = @('--no-build') }
  Invoke-Gate "test $Config" { dotnet test $Solution -c $Config -nologo @noBuild }

  if ($script:Python) {
    Invoke-PythonGate 'todo-graph self-test' 'todo-graph.py' @('self-test')
    Invoke-PythonGate 'todo-graph validate' 'todo-graph.py' @('validate')
    Invoke-PythonGate 'todo-graph plan --check' 'todo-graph.py' @('plan', '--check')
    Invoke-PythonGate 'todo-claims' 'todo-claims.py' @()
    Invoke-PythonGate 'todo-findings --check' 'todo-findings.py' @('--check')
    Invoke-PythonGate 'todo-runs --check' 'todo-runs.py' @('--check')
    Invoke-PythonGate 'campaign_guard self-test' 'campaign_guard.py' @('--self-test')
    Invoke-PythonGate 'design site --check' 'build-design-site.py' @('--check')
    Invoke-PythonGate 'app icons --check' 'build-app-icons.py' @('--check')
    Invoke-PythonGate 'design-lint self-test' 'design-lint.py' @('--self-test')
    Invoke-PythonGate 'design-lint baseline' 'design-lint.py' @('--baseline', 'docs/design/.lint-baseline.json')
    Invoke-PythonGate 'panel_slots self-test' 'panel_slots.py' @('--self-test')
    Invoke-PythonGate 'panel_slots validate' 'panel_slots.py' @('validate')
    Invoke-PythonGate 'reviewer pin' 'review-dispatch.py' @('--check-pin')
    Invoke-PythonGate 'review-dispatch tests' 'tests/test_review_dispatch.py' @()
    Invoke-PythonGate 'weakening-scan self-test' 'weakening-scan.py' @('--self-test')
    Invoke-PythonGate 'automations tests' 'tests/test_automations.py' @()
    Invoke-PythonGate 'pin automations tests' 'tests/test_pin_automations.py' @()
    Invoke-PythonGate 'merge prs tests' 'tests/test_merge_prs.py' @()
    Invoke-PythonGate 'ci_watch self-test' 'ci_watch.py' @('--self-test')
    Invoke-PythonGate 'completion_check self-test' 'completion_check.py' @('--self-test')
    Invoke-PythonGate 'build props tests' 'tests/test_build_props.py' @()
  } else {
    Write-Warning 'check-all: python not found on PATH; skipping plan gates'
    $results.Add([pscustomobject]@{ Gate = 'python gates'; Status = 'SKIP (no python)'; Seconds = 0 })
  }

  if (-not $SkipNative) {
    $devEnv = Join-Path $RepoRoot 'scripts/dev-env.ps1'
    Invoke-NativeGate 'native toolchain' @('pwsh', '-NoProfile', '-Command',
      "& '$devEnv' -Check -Arch x64; `$a = `$LASTEXITCODE; & '$devEnv' -Check -Arch arm64; exit [Math]::Max(`$a, `$LASTEXITCODE)")
    foreach ($preset in 'x64-debug', 'x64-release', 'x64-asan', 'arm64-debug', 'arm64-release', 'arm64-asan', 'x64-dist', 'arm64-dist') {
      $arch = $preset.Split('-')[0]
      Invoke-InNative "native $preset" $arch "Push-Location native; cmake --workflow --preset $preset; `$c = `$LASTEXITCODE; Pop-Location; exit `$c"
    }
    Invoke-NativeGate 'native analyze' @('pwsh', '-NoProfile', '-Command',
      "& '$devEnv' -Arch x64 -Run 'Push-Location native; cmake --preset x64-analyze; `$c = `$LASTEXITCODE; if (-not `$c) { cmake --build --preset x64-analyze; `$c = `$LASTEXITCODE }; Pop-Location; exit `$c'; `$a = `$LASTEXITCODE; " +
      "& '$devEnv' -Arch arm64 -Run 'Push-Location native; cmake --preset arm64-analyze; `$c = `$LASTEXITCODE; if (-not `$c) { cmake --build --preset arm64-analyze; `$c = `$LASTEXITCODE }; Pop-Location; exit `$c'; exit [Math]::Max(`$a, `$LASTEXITCODE)")
    $presetFolders = @((Get-Content -Raw (Join-Path $RepoRoot 'native/CMakePresets.json') | ConvertFrom-Json).configurePresets |
      Where-Object { -not ($_.PSObject.Properties['hidden'] -and $_.hidden) } | ForEach-Object { "artifacts/native/$($_.name)" })
    if ($script:Python) {
      Invoke-NativeGate 'native std' (@($script:Python, (Join-Path $RepoRoot 'scripts/native-std-check.py')) + $presetFolders)
      Invoke-InNative 'native pe' 'x64' ("python scripts/native-pe-check.py $($presetFolders -join ' '); exit `$LASTEXITCODE")
    }
    Invoke-NativeGate 'native format' @('pwsh', '-NoProfile', '-File', (Join-Path $RepoRoot 'scripts/native-format.ps1'), '-Check')
    Invoke-NativeGate 'native tidy' @('pwsh', '-NoProfile', '-File', (Join-Path $RepoRoot 'scripts/native-tidy.ps1'))
    Invoke-InNative 'native artifacts' 'x64' 'python scripts/native-artifact-gate.py --policy shipping --require-built; exit $LASTEXITCODE'
    Invoke-InNative 'native artifacts asan' 'x64' 'python scripts/native-artifact-gate.py --policy asan --require-built; exit $LASTEXITCODE'
    Invoke-InNative 'native asan-coverage' 'x64' 'python scripts/native-artifact-gate.py --asan-coverage --require-built; exit $LASTEXITCODE'
    if ($script:Python) {
      Invoke-PythonGate 'native-std-check self-test' 'native-std-check.py' @('--self-test')
      Invoke-PythonGate 'native-pe-check self-test' 'native-pe-check.py' @('--self-test')
      Invoke-PythonGate 'native-artifact-gate self-test' 'native-artifact-gate.py' @('--self-test')
      Invoke-PythonGate 'dev-env tests' 'tests/test_dev_env.py' @()
      Invoke-PythonGate 'native format tests' 'tests/test_native_format.py' @()
      Invoke-PythonGate 'native tidy tests' 'tests/test_native_tidy.py' @()
      Invoke-PythonGate 'native asan tests' 'tests/test_native_asan.py' @()
    }
  } else {
    $results.Add([pscustomobject]@{ Gate = 'native stages'; Status = 'SKIP (-SkipNative)'; Seconds = 0 })
  }
} finally {
  Pop-Location
}

$results | Format-Table -AutoSize | Out-String | Write-Host
$failed = @($results | Where-Object { $_.Status -like 'FAIL*' })
if ($failed.Count -gt 0) {
  Write-Host "check-all: $($failed.Count) gate(s) failed" -ForegroundColor Red
  exit 1
}
Write-Host 'check-all: all gates passed' -ForegroundColor Green
exit 0
