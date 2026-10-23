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
  -PinFile reads another pin (the tests' fixtures); -VsWhere another vswhere (the tests' stand-ins); -TripletDir and
  -SdkInclude other triplets and SDK folders. -Check also refuses an overlay triplet whose toolset version is not the
  pin's, and a Windows SDK newer than the pinned one, because vcpkg builds each dependency with the newest installed.
.EXAMPLE
  pwsh scripts/dev-env.ps1 -Check -Arch arm64
#>
[CmdletBinding()]
param(
  [ValidateSet('x64', 'arm64')][string]$Arch = 'x64',
  [string]$PinFile = (Join-Path (Split-Path -Parent $PSScriptRoot) 'native\toolchain.json'),
  # The installer's vswhere; the tests point it at a missing path or a stand-in that reports a chosen installation.
  [string]$VsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe",
  # The overlay triplets and the Windows SDK include folder; the tests point them at fixtures.
  [string]$TripletDir = (Join-Path (Split-Path -Parent $PSScriptRoot) 'native\triplets'),
  [string]$SdkInclude = "${env:ProgramFiles(x86)}\Windows Kits\10\Include",
  [switch]$Check,
  # A script block, or its text when the script runs in its own process (pwsh -File ... -Run 'cmake --preset x64').
  [object]$Run
)
$ErrorActionPreference = 'Stop'

$Pin = Get-Content -Raw $PinFile | ConvertFrom-Json
$Rows = [System.Collections.Generic.List[object]]::new()

function Add-Row([string]$Item, [string]$Pinned, [string]$Found, [object]$Ok = $null) {
  $isOk = if ($null -eq $Ok) { $Pinned -eq $Found } else { [bool]$Ok }
  $Rows.Add([pscustomobject]@{ Item = $Item; Pinned = $Pinned; Found = $Found; Ok = $isOk })
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

# A bundled tool's row: its version, and that the binary PATH resolves is the selected installation's own, never a
# standalone copy (a WinGet Ninja, a separately installed CMake or LLVM) that happens to come first.
function Add-BundledToolRow([string]$Item, [string]$Pinned, [string]$Name, [string]$Pattern, [string]$Under) {
  $cmd = Get-Command $Name -CommandType Application -ErrorAction Ignore | Select-Object -First 1
  if (-not $cmd) { Add-Row $Item $Pinned 'not on PATH'; return }
  $found = Read-Version (Invoke-Tool $Name @('--version')) $Pattern
  if ($cmd.Source.StartsWith($Under, [StringComparison]::OrdinalIgnoreCase)) { Add-Row $Item $Pinned $found; return }
  Add-Row $Item $Pinned "$found from $($cmd.Source), not the selected installation" $false
}

# vcvarsall prepends to these each time it runs, so a second entry in one process would grow them until cmd.exe
# refuses the line; every entry starts from the values the first entry found, kept in the process environment so a
# nested entry (a dot-sourced re-entry, a -Run that enters again) sees them too.
$Accumulated = 'PATH', 'INCLUDE', 'LIB', 'LIBPATH', 'EXTERNAL_INCLUDE'
$Unset = '::unset::'
function Restore-PreEntryEnvironment {
  foreach ($name in $Accumulated) {
    $saved = "ISOTONE_DEVENV_PRE_$name"
    $now = [Environment]::GetEnvironmentVariable($name)
    if ($null -eq [Environment]::GetEnvironmentVariable($saved)) {
      [Environment]::SetEnvironmentVariable($saved, $(if ($now) { $now } else { $Unset }))
    }
    $pre = [Environment]::GetEnvironmentVariable($saved)
    [Environment]::SetEnvironmentVariable($name, $(if ($pre -eq $Unset) { $null } else { $pre }))
  }
}

# 1. Visual Studio: one installation, the newest in the pinned range that holds every pinned component itself (vswhere
# -requires matches all of them in one instance). A component in a second installation does not count: the developer
# environment is entered from one installation. When none qualifies, the newest in range is reported, to name what it
# lacks.
$range = $Pin.visual_studio.version_range
$vs = $null
if (-not (Test-Path $VsWhere)) {
  Add-Row 'Visual Studio Installer' 'installed' "missing ($VsWhere): install Visual Studio 2026 first" $false
}
else {
  $query = @('-version', $range, '-products', '*', '-include', 'packages', '-format', 'json')
  $complete = @(& $VsWhere @query -requires @($Pin.visual_studio.components) | ConvertFrom-Json) |
    Sort-Object { [version]$_.installationVersion } -Descending | Select-Object -First 1
  $install = if ($complete) { $complete } else { @(& $VsWhere @query -latest | ConvertFrom-Json) | Select-Object -First 1 }
  if (-not $install) {
    Add-Row 'Visual Studio' $range 'none in range' $false
  }
  else {
    # The selected installation, by path: provision prints its repair commands against exactly this one.
    Add-Row 'Visual Studio' $range "$($install.installationVersion) at $($install.installationPath)" $true
    $ids = [System.Collections.Generic.HashSet[string]]::new([string[]]@($install.packages | ForEach-Object { $_.id }))
    $complete = $true
    foreach ($component in $Pin.visual_studio.components) {
      $has = $ids.Contains($component)
      $complete = $complete -and $has
      Add-Row "component $component" 'installed' ($(if ($has) { 'installed' } else { 'missing' }))
    }
    if ($complete) { $vs = $install.installationPath }
  }
}
if ($vs) {
  # 2. Enter the pinned toolset and SDK through vcvarsall, and import its environment into this process.
  $vcvars = Join-Path $vs 'VC\Auxiliary\Build\vcvarsall.bat'
  $vcArch = Get-VcvarsArch (Get-HostArch) $Arch
  Restore-PreEntryEnvironment
  $dump = & cmd.exe /d /c "`"$vcvars`" $vcArch $($Pin.windows_sdk) -vcvars_ver=$($Pin.msvc.toolset) >nul 2>&1 && set"
  $entered = $LASTEXITCODE -eq 0 -and ($dump | Where-Object { $_ -like 'VCToolsVersion=*' })
  if (-not $entered) {
    if (-not (Test-Path (Join-Path $SdkInclude $Pin.windows_sdk))) {
      # vcvarsall cannot enter a Windows SDK that is not installed; name the SDK, not the toolset it never reached.
      Add-Row 'Windows SDK' $Pin.windows_sdk 'not installed'
    }
    else {
      Add-Row 'MSVC toolset' $Pin.msvc.toolset "not installed (vcvarsall $vcArch could not enter it)"
    }
  }
  else {
    foreach ($line in $dump) {
      $i = $line.IndexOf('=')
      if ($i -gt 0) { Set-Item -Path "env:$($line.Substring(0, $i))" -Value $line.Substring($i + 1) }
    }
    $env:VCPKG_ROOT = Join-Path $vs 'VC\vcpkg'
    # The selected installation's bundled tools come first: vcvarsall appends their folders, so a standalone copy
    # earlier on PATH would otherwise run instead.
    $llvmHost = if ((Get-HostArch) -eq 'arm64') { 'ARM64' } else { 'x64' }
    $bundled = @(
      (Join-Path $vs 'Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin'),
      (Join-Path $vs 'Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja'),
      (Join-Path $vs "VC\Tools\Llvm\$llvmHost\bin"),
      (Join-Path $vs 'VC\vcpkg'))
    $env:PATH = (@($bundled) + @($env:PATH -split ';' | Where-Object { $_ -and $_ -notin $bundled })) -join ';'

    # cl adds the options in CL before and _CL_ after its own command line on every run (Microsoft Learn, "CL
    # environment variables"), so a developer's `_CL_=/std:c++20` would override the pinned standard and `/nologo`
    # would hide the banner read below. The pinned environment takes its options from the build description only;
    # native/cmake/CheckCompilerEnvironment.cmake refuses them again at configure and on every build.
    foreach ($name in 'CL', '_CL_') {
      $value = [Environment]::GetEnvironmentVariable($name)
      if ($value) {
        [Console]::Error.WriteLine("dev-env: cleared $name=$value (MSVC would add it to every compile)")
        [Environment]::SetEnvironmentVariable($name, $null)
      }
    }

    # 3. What the environment actually runs.
    Add-Row 'MSVC toolset' $Pin.msvc.toolset $env:VCToolsVersion
    $banner = Invoke-Tool 'cl' @()
    Add-Row 'MSVC compiler' $Pin.msvc.compiler (Read-Version $banner 'Version (\d+\.\d+\.\d+)')
    $clTarget = Read-Version $banner 'Version \S+ for (\w+)'
    Add-Row 'MSVC target' ($(if ($Arch -eq 'arm64') { 'ARM64' } else { 'x64' })) $clTarget
    # vcvarsall sets WindowsSDKVersion to the version it was asked for even when that SDK is not installed, so the
    # row reads the version back only when its include folder exists.
    $sdkFound = "$env:WindowsSDKVersion".TrimEnd('\')
    if ($sdkFound -and -not (Test-Path (Join-Path $SdkInclude $sdkFound))) { $sdkFound = "$sdkFound (not installed)" }
    Add-Row 'Windows SDK' $Pin.windows_sdk $sdkFound
    Add-BundledToolRow 'cmake' $Pin.cmake 'cmake' 'cmake version (\S+)' $vs
    Add-BundledToolRow 'ninja' $Pin.ninja 'ninja' '^(\S+)' $vs
    Add-BundledToolRow 'clang-tidy' $Pin.llvm.'clang-tidy' 'clang-tidy' 'LLVM version (\S+)' $vs
    Add-BundledToolRow 'clang-format' $Pin.llvm.'clang-format' 'clang-format' 'clang-format version (\S+)' $vs
    Add-BundledToolRow 'clang-cl' $Pin.llvm.'clang-cl' 'clang-cl' 'clang version (\S+)' $vs
    Add-BundledToolRow 'vcpkg' $Pin.vcpkg 'vcpkg' 'program version (\S+)' $vs
  }
}

# 4. What vcpkg builds dependencies with, which the environment above does not govern: each port runs its own vcvarsall,
# with the toolset version its triplet names and the newest Windows SDK installed (vcpkg "Triplet files").
foreach ($triplet in @(Get-ChildItem $TripletDir -Filter 'isotone-*.cmake' -ErrorAction Ignore)) {
  $m = Select-String -Path $triplet.FullName -Pattern 'set\(VCPKG_PLATFORM_TOOLSET_VERSION\s+([^\s)]+)\)' | Select-Object -First 1
  Add-Row "triplet $($triplet.BaseName) toolset" $Pin.msvc.toolset ($(if ($m) { $m.Matches[0].Groups[1].Value } else { 'none' }))
}
$sdks = @(Get-ChildItem $SdkInclude -Directory -ErrorAction Ignore | Where-Object { $_.Name -match '^10\.0\.\d+\.\d+$' } |
  Sort-Object { [version]$_.Name } -Descending)
Add-Row 'Windows SDK newest installed' $Pin.windows_sdk ($(if ($sdks) { $sdks[0].Name } else { 'none' }))

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
