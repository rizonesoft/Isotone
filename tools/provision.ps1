#Requires -Version 5.1
<#
.SYNOPSIS
  Verifies and repairs the developer toolchain for the Isotone Graphics Suite.
.DESCRIPTION
  Legs:
    sdk     the .NET SDK pinned in global.json (exact version, rollForward disable;
            a prerelease pin such as 11.0.100-rc.1 is matched exactly too).
            Accepts a machine-wide install; otherwise repair downloads it, verifies
            the SHA512 sidecar, and unpacks it to .tools/dotnet-win-x64.
    inno    Inno Setup 7 (ISCC.exe), version >= $MinInno. Repair installs it with
            winget (JRSoftware.InnoSetup.7), falling back to the pinned official
            installer ($InnoVersion, SHA256 verified). Chocolatey has no Inno 7.
    hooks   git core.hooksPath = tools/githooks and tools/githooks/pre-commit present.
    python  Python 3 on PATH (plan gates in scripts/check-all.ps1).
  -Verify runs the checks only: exit 0 when all legs are green, 1 otherwise.
  Without -Verify, failing legs are repaired, then verified again.
  Run: pwsh tools/provision.ps1 [-Verify] [-SkipInno]
#>
[CmdletBinding()]
param(
  [switch]$Verify,
  [switch]$SkipInno
)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Root = Split-Path -Parent $PSScriptRoot
$Rid = 'win-x64'
$LocalSdk = Join-Path $Root ".tools\dotnet-$Rid"
$MinInno = [version]'7.1.0'
$InnoVersion = '7.1.0'
$InnoWingetId = 'JRSoftware.InnoSetup.7'
$InnoInstallerUrl = "https://github.com/jrsoftware/issrc/releases/download/is-$($InnoVersion -replace '\.', '_')/innosetup-$InnoVersion-x64.exe"
$InnoInstallerSha256 = '0362A383ED217D4C4239B5933866DD96D3EB2102737DA92F80F6057A4B40DF2F'

function Get-PinnedSdkVersion {
  return (Get-Content (Join-Path $Root 'global.json') -Raw | ConvertFrom-Json).sdk.version
}

function Test-SdkLeg {
  $want = Get-PinnedSdkVersion
  if (-not $want) { return @{ Name = 'sdk'; Ok = $false; Detail = 'no sdk.version in global.json' } }
  $pattern = '^' + [regex]::Escape($want) + ' '
  $local = Join-Path $LocalSdk 'dotnet.exe'
  if (Test-Path $local) {
    if (@(& $local --list-sdks 2>$null) -match $pattern) {
      return @{ Name = 'sdk'; Ok = $true; Detail = "$want in .tools (set DOTNET_ROOT=$LocalSdk and prepend it to PATH)" }
    }
  }
  $cmd = Get-Command dotnet -ErrorAction SilentlyContinue
  if ($cmd -and (@(& $cmd.Source --list-sdks 2>$null) -match $pattern)) {
    return @{ Name = 'sdk'; Ok = $true; Detail = "$want ($($cmd.Source))" }
  }
  return @{ Name = 'sdk'; Ok = $false; Detail = "SDK $want not installed" }
}

function Install-Sdk {
  $version = Get-PinnedSdkVersion
  $base = "https://builds.dotnet.microsoft.com/dotnet/Sdk/$version/dotnet-sdk-$version-$Rid"
  $work = Join-Path ([IO.Path]::GetTempPath()) ('isotone-sdk-' + [Guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $work | Out-Null
  try {
    $zip = Join-Path $work 'sdk.zip'
    $sidecar = Join-Path $work 'sdk.sha512'
    Write-Host "provision: downloading .NET SDK $version"
    Invoke-WebRequest -Uri "$base.zip" -OutFile $zip -UseBasicParsing
    Invoke-WebRequest -Uri "$base.zip.sha512" -OutFile $sidecar -UseBasicParsing
    $expected = ((Get-Content $sidecar -Raw) -split '\s+')[0].ToUpperInvariant()
    $actual = (Get-FileHash -Path $zip -Algorithm SHA512).Hash
    if ($actual -ne $expected) { throw "provision: SHA512 mismatch for $base.zip" }
    if (Test-Path $LocalSdk) { Remove-Item -Recurse -Force $LocalSdk }
    New-Item -ItemType Directory -Path $LocalSdk | Out-Null
    Expand-Archive -Path $zip -DestinationPath $LocalSdk
    Write-Host "provision: .NET SDK $version ready in $LocalSdk"
  } finally {
    Remove-Item -Recurse -Force $work -ErrorAction SilentlyContinue
  }
}

function Find-InnoSetup {
  $keys = @(
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 7_is1',
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 7_is1',
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 7_is1'
  )
  foreach ($k in $keys) {
    $p = Get-ItemProperty $k -ErrorAction SilentlyContinue
    if ($p -and $p.InstallLocation) {
      $exe = Join-Path $p.InstallLocation 'ISCC.exe'
      if (Test-Path $exe) { return @{ Exe = $exe; Version = $p.DisplayVersion } }
    }
  }
  $paths = @(
    $env:ISCC,
    (Join-Path $env:ProgramFiles 'Inno Setup 7\ISCC.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 7\ISCC.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 7\ISCC.exe')
  ) | Where-Object { $_ -and (Test-Path $_) }
  if ($paths) { return @{ Exe = @($paths)[0]; Version = $null } }
  return $null
}

function Test-InnoLeg {
  if ($SkipInno) { return @{ Name = 'inno'; Ok = $true; Detail = 'skipped (-SkipInno)' } }
  $inno = Find-InnoSetup
  if (-not $inno) { return @{ Name = 'inno'; Ok = $false; Detail = 'Inno Setup 7 (ISCC.exe) not found' } }
  if (-not $inno.Version) { return @{ Name = 'inno'; Ok = $true; Detail = "$($inno.Exe) (version unknown)" } }
  $v = [version](($inno.Version -split '[^\d\.]')[0])
  if ($v -lt $MinInno) { return @{ Name = 'inno'; Ok = $false; Detail = "Inno Setup $v is older than $MinInno" } }
  return @{ Name = 'inno'; Ok = $true; Detail = "Inno Setup $v ($($inno.Exe))" }
}

function Install-Inno {
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    & winget install --id $InnoWingetId -e --version $InnoVersion --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -eq 0) { return }
  }
  # Fallback: the official installer from the jrsoftware/issrc release, hash-pinned.
  $exe = Join-Path ([IO.Path]::GetTempPath()) "innosetup-$InnoVersion-x64.exe"
  try {
    Write-Host "provision: downloading Inno Setup $InnoVersion"
    Invoke-WebRequest -Uri $InnoInstallerUrl -OutFile $exe -UseBasicParsing
    $actual = (Get-FileHash -Path $exe -Algorithm SHA256).Hash
    if ($actual -ne $InnoInstallerSha256) { throw "provision: SHA256 mismatch for $InnoInstallerUrl" }
    $p = Start-Process -FilePath $exe -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/SP-' -Wait -PassThru
    if ($p.ExitCode -eq 0) { return }
    Write-Warning "provision: Inno Setup installer exited $($p.ExitCode)"
  } catch {
    Write-Warning $_
  } finally {
    Remove-Item -Force $exe -ErrorAction SilentlyContinue
  }
  Write-Warning 'provision: install Inno Setup 7 manually from https://jrsoftware.org/isdl.php'
}

function Test-HooksLeg {
  $res = @()
  $cfg = ''
  try { $cfg = ((& git -C $Root config core.hooksPath 2>$null) -join "`n").Trim() } catch { }
  $res += @{ Name = 'hooks path'; Ok = ($cfg -eq 'tools/githooks'); Detail = $(if ($cfg) { "core.hooksPath = '$cfg'" } else { 'core.hooksPath unset' }) }
  $pre = Join-Path $Root 'tools/githooks/pre-commit'
  $res += @{ Name = 'hooks pre-commit'; Ok = (Test-Path $pre); Detail = $(if (Test-Path $pre) { 'present' } else { 'missing (restore: git checkout -- tools/githooks/pre-commit)' }) }
  return $res
}

function Repair-Hooks {
  $cfg = ''
  try { $cfg = ((& git -C $Root config core.hooksPath 2>$null) -join "`n").Trim() } catch { }
  if ($cfg -and $cfg -ne 'tools/githooks') {
    Write-Warning "provision: core.hooksPath points at '$cfg'; left alone (unset it to let provision re-wire)"
    return
  }
  & git -C $Root config core.hooksPath 'tools/githooks'
  Write-Host 'provision: core.hooksPath = tools/githooks'
}

function Test-PythonLeg {
  foreach ($name in @('python', 'python3')) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) {
      $v = (& $cmd.Source --version 2>&1) -join ' '
      if ($v -match 'Python 3\.') { return @{ Name = 'python'; Ok = $true; Detail = $v.Trim() } }
    }
  }
  return @{ Name = 'python'; Ok = $false; Detail = 'Python 3 not on PATH (install from python.org or winget Python.Python.3.14)' }
}

function Test-All {
  $r = @()
  $r += Test-SdkLeg
  $r += Test-InnoLeg
  $r += Test-HooksLeg
  $r += Test-PythonLeg
  return $r
}

function Show-Results($Results) {
  foreach ($r in $Results) {
    $verdict = if ($r.Ok) { 'OK' } else { 'FAULT' }
    Write-Host "provision: $($r.Name): $verdict ($($r.Detail))"
  }
  $ok = @($Results | Where-Object { $_.Ok }).Count
  Write-Host "provision: $ok/$($Results.Count) green"
  return ($ok -eq $Results.Count)
}

$results = @(Test-All)
if (-not $Verify) {
  $faults = @($results | Where-Object { -not $_.Ok } | ForEach-Object { $_.Name })
  if ($faults -contains 'sdk') { Install-Sdk }
  if ($faults -contains 'inno') { Install-Inno }
  if ($faults -contains 'hooks path') { Repair-Hooks }
  if ($faults.Count -gt 0) { $results = @(Test-All) }
}
if (Show-Results $results) { exit 0 } else { exit 1 }
