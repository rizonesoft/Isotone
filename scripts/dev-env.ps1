#Requires -Version 7.2
<#
.SYNOPSIS
  Enters the pinned native toolchain (native/toolchain.json) and refuses any other.
.DESCRIPTION
  Locates Visual Studio with vswhere (the pinned version range and every pinned component), enters its developer
  environment through vcvarsall.bat with -vcvars_ver=<pinned toolset> and the pinned Windows SDK for the target
  architecture (Launch-VsDevShell.ps1 has no toolset selector, so it cannot honour a pin), sets VCPKG_ROOT to the
  bundled vcpkg, and verifies what the environment actually runs: the version cl reports, VCToolsVersion, the Windows
  SDK, and the --version of cmake, ninja, clang-tidy, clang-format, clang-cl, and vcpkg.

  Dot-sourced (. scripts/dev-env.ps1 -Arch x64), it leaves the session in that environment and throws on a mismatch.
  -Run { ... } (or its text, from another process) runs a block inside it and returns the block's exit code. -Check prints one line per item
  (`<item> pinned <value> found <value> ok|MISMATCH`) and exits 1 on any mismatch or missing component.
  -PinFile reads another pin (the tests' fixtures).
.EXAMPLE
  pwsh scripts/dev-env.ps1 -Check -Arch arm64
#>
[CmdletBinding()]
param(
  [ValidateSet('x64', 'arm64')][string]$Arch = 'x64',
  [string]$PinFile = (Join-Path (Split-Path -Parent $PSScriptRoot) 'native\toolchain.json'),
  [switch]$Check,
  # A script block, or its text when the script runs in its own process (pwsh -File ... -Run 'cmake --preset x64').
  [object]$Run
)
$ErrorActionPreference = 'Stop'

$Pin = Get-Content -Raw $PinFile | ConvertFrom-Json
$VsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
$Rows = [System.Collections.Generic.List[object]]::new()

function Add-Row([string]$Item, [string]$Pinned, [string]$Found) {
  $Rows.Add([pscustomobject]@{ Item = $Item; Pinned = $Pinned; Found = $Found; Ok = ($Pinned -eq $Found) })
}

function Get-HostArch {
  if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64' -or $env:PROCESSOR_ARCHITEW6432 -eq 'ARM64') { return 'arm64' }
  return 'x64'
}

# vcvarsall's architecture argument: host first, then the target when it differs (x64_arm64 cross-compiles).
function Get-VcvarsArch([string]$HostArch, [string]$Target) {
  if ($HostArch -eq $Target) { return $Target }
  return "${HostArch}_$Target"
}

# The first version-shaped token after a marker in a tool's output, or 'none' when the output has none.
function Read-Version([string[]]$Text, [string]$Pattern) {
  $m = [regex]::Match(($Text -join "`n"), $Pattern)
  if ($m.Success) { return $m.Groups[1].Value }
  return 'none'
}

function Invoke-Tool([string]$Name, [string[]]$ToolArgs) {
  $cmd = Get-Command $Name -CommandType Application -ErrorAction Ignore | Select-Object -First 1
  if (-not $cmd) { return @() }
  # cl prints its banner on stderr; every tool's output is read whole.
  return @(& $cmd.Source @ToolArgs 2>&1 | ForEach-Object { "$_" })
}

# 1. Visual Studio: the pinned range, with every pinned component.
$range = $Pin.visual_studio.version_range
$vs = & $VsWhere -version $range -latest -products * -requires $Pin.visual_studio.components -property installationPath
if (-not $vs) {
  foreach ($component in $Pin.visual_studio.components) {
    $has = & $VsWhere -version $range -latest -products * -requires $component -property installationPath
    Add-Row "component $component" 'installed' ($(if ($has) { 'installed' } else { 'missing' }))
  }
  $any = & $VsWhere -version $range -latest -products * -property installationVersion
  Add-Row 'Visual Studio' $range ($(if ($any) { "$any (components missing)" } else { 'none in range' }))
}
else {
  Add-Row 'Visual Studio' $range $range
  foreach ($component in $Pin.visual_studio.components) { Add-Row "component $component" 'installed' 'installed' }

  # 2. Enter the pinned toolset and SDK through vcvarsall, and import its environment into this process.
  $vcvars = Join-Path $vs 'VC\Auxiliary\Build\vcvarsall.bat'
  $vcArch = Get-VcvarsArch (Get-HostArch) $Arch
  $dump = & cmd.exe /d /c "`"$vcvars`" $vcArch $($Pin.windows_sdk) -vcvars_ver=$($Pin.msvc.toolset) >nul 2>&1 && set"
  $entered = $LASTEXITCODE -eq 0 -and ($dump | Where-Object { $_ -like 'VCToolsVersion=*' })
  if (-not $entered) {
    Add-Row 'MSVC toolset' $Pin.msvc.toolset "not installed (vcvarsall $vcArch could not enter it)"
  }
  else {
    foreach ($line in $dump) {
      $i = $line.IndexOf('=')
      if ($i -gt 0) { Set-Item -Path "env:$($line.Substring(0, $i))" -Value $line.Substring($i + 1) }
    }
    $env:VCPKG_ROOT = Join-Path $vs 'VC\vcpkg'

    # 3. What the environment actually runs.
    Add-Row 'MSVC toolset' $Pin.msvc.toolset $env:VCToolsVersion
    $banner = Invoke-Tool 'cl' @()
    Add-Row 'MSVC compiler' $Pin.msvc.compiler (Read-Version $banner 'Version (\d+\.\d+\.\d+)')
    $clTarget = Read-Version $banner 'Version \S+ for (\w+)'
    Add-Row 'MSVC target' ($(if ($Arch -eq 'arm64') { 'ARM64' } else { 'x64' })) $clTarget
    Add-Row 'Windows SDK' $Pin.windows_sdk ("$env:WindowsSDKVersion".TrimEnd('\'))
    Add-Row 'cmake' $Pin.cmake (Read-Version (Invoke-Tool 'cmake' @('--version')) 'cmake version (\S+)')
    Add-Row 'ninja' $Pin.ninja (Read-Version (Invoke-Tool 'ninja' @('--version')) '^(\S+)')
    Add-Row 'clang-tidy' $Pin.llvm.'clang-tidy' (Read-Version (Invoke-Tool 'clang-tidy' @('--version')) 'LLVM version (\S+)')
    Add-Row 'clang-format' $Pin.llvm.'clang-format' (Read-Version (Invoke-Tool 'clang-format' @('--version')) 'clang-format version (\S+)')
    Add-Row 'clang-cl' $Pin.llvm.'clang-cl' (Read-Version (Invoke-Tool 'clang-cl' @('--version')) 'clang version (\S+)')
    Add-Row 'vcpkg' $Pin.vcpkg (Read-Version (Invoke-Tool 'vcpkg' @('--version')) 'program version (\S+)')
  }
}

$bad = @($Rows | Where-Object { -not $_.Ok })
if ($Check) {
  foreach ($r in $Rows) {
    Write-Output ('{0} pinned {1} found {2} {3}' -f $r.Item, $r.Pinned, $r.Found, $(if ($r.Ok) { 'ok' } else { 'MISMATCH' }))
  }
  Write-Output ("dev-env: {0} {1}: {2} checked, {3} mismatch" -f $Arch, $PinFile, $Rows.Count, $bad.Count)
  exit $(if ($bad.Count) { 1 } else { 0 })
}
if ($bad.Count) {
  throw ("dev-env: the toolchain does not match the pin: " + (($bad | ForEach-Object { "$($_.Item) pinned $($_.Pinned) found $($_.Found)" }) -join '; '))
}
if ($Run) {
  $block = if ($Run -is [scriptblock]) { $Run } else { [scriptblock]::Create([string]$Run) }
  & $block
  exit $LASTEXITCODE
}
