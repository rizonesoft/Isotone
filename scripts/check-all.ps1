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
  10. python scripts/build-design-site.py --check (docs/design/index.html is current)
  11. python scripts/design-lint.py --self-test
  12. python scripts/design-lint.py --baseline docs/design/.lint-baseline.json
      (no new design-contract violation in the UI sources; standards/design-contract.md)
  A python gate whose script is absent is skipped with a warning. Every gate
  runs even after an earlier failure; the exit code is 1 when any gate failed.
.EXAMPLE
  pwsh scripts/check-all.ps1
  pwsh scripts/check-all.ps1 -SkipBuild
#>
[CmdletBinding()]
param(
  [switch]$SkipBuild,
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
    Invoke-PythonGate 'design-lint self-test' 'design-lint.py' @('--self-test')
    Invoke-PythonGate 'design-lint baseline' 'design-lint.py' @('--baseline', 'docs/design/.lint-baseline.json')
  } else {
    Write-Warning 'check-all: python not found on PATH; skipping plan gates'
    $results.Add([pscustomobject]@{ Gate = 'python gates'; Status = 'SKIP (no python)'; Seconds = 0 })
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
