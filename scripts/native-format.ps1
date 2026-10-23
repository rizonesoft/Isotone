#Requires -Version 7.2
<#
.SYNOPSIS
  Checks or fixes the format of the native C and C++ sources with the pinned clang-format (D00 T05 §4).
.DESCRIPTION
  The files are every first-party source under native/ the next commit would carry: tracked files plus untracked files
  git does not ignore (git ls-files --cached --others --exclude-standard), so build output and installed dependencies
  are never formatted and a new file awaiting staging is still checked. The list is read NUL-delimited and as UTF-8, so
  a name git would quote (any non-ASCII character) is checked like any other, and a tracked file deleted from the
  working tree is left out: there is nothing to format. -Check runs clang-format --dry-run --Werror and names each file
  that needs formatting; -Fix rewrites them in place. -Root points it at another repository (the tests' scratch one).
  The script enters scripts/dev-env.ps1 itself, so the clang-format that runs is the pinned one. Exit 0 clean, 1 a file
  needs formatting, 2 a usage or tool failure.
.EXAMPLE
  pwsh scripts/native-format.ps1 -Check
#>
[CmdletBinding()]
param([switch]$Check, [switch]$Fix, [string]$Root = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'

if ($Check -eq $Fix) {
  Write-Error 'native-format: pass exactly one of -Check and -Fix' -ErrorAction Continue
  exit 2
}
$root = (Resolve-Path $Root).Path

function Enter-NativeEnvironment {
  # Dot-sourced inside a function, so dev-env's parameters stay out of this script's scope; the environment it enters
  # is the process's.
  . (Join-Path $PSScriptRoot 'dev-env.ps1') -Arch x64
}
Enter-NativeEnvironment

$extensions = '.c', '.cc', '.cpp', '.cxx', '.h', '.hh', '.hpp', '.hxx', '.ixx', '.inl'
$encoding = [Console]::OutputEncoding
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
try { $listed = (git -C $root ls-files -z --cached --others --exclude-standard -- native) -join "`n" }
finally { [Console]::OutputEncoding = $encoding }
if ($LASTEXITCODE -ne 0) {
  Write-Error 'native-format: git ls-files failed' -ErrorAction Continue
  exit 2
}
$files = @($listed.Split([char]0, [StringSplitOptions]::RemoveEmptyEntries) |
  Where-Object { $extensions -contains [IO.Path]::GetExtension($_).ToLowerInvariant() } |
  Sort-Object -Unique |
  ForEach-Object { Join-Path $root $_ } |
  Where-Object { Test-Path -LiteralPath $_ -PathType Leaf })
if (-not $files) {
  Write-Error 'native-format: no C or C++ source under native/' -ErrorAction Continue
  exit 2
}

if ($Fix) {
  clang-format -i --style=file @files
  if ($LASTEXITCODE -ne 0) { exit 2 }
  "native-format: $($files.Count) file(s) formatted"
  exit 0
}

$failing = @()
foreach ($file in $files) {
  $out = clang-format --dry-run --Werror --style=file $file 2>&1
  if ($LASTEXITCODE -ne 0) {
    $failing += $file
    $out | Select-Object -First 3 | ForEach-Object { "$_" }
  }
}
foreach ($file in $failing) { "FAIL $([IO.Path]::GetRelativePath($root, $file)) needs clang-format" }
"native-format: $($files.Count) file(s) checked, $($failing.Count) need formatting"
exit $(if ($failing) { 1 } else { 0 })
