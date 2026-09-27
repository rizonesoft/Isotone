#Requires -Version 7.0
<#
.SYNOPSIS
  Publishes and packages an app (or the whole suite) into artifacts/dist/.
.DESCRIPTION
  Per app (-App):   <App>-<version>-<rid>-Setup.exe and <App>-<version>-<rid>-Portable.zip
  Suite (-Suite):   Photon-<version>-<rid>-Setup.exe and Photon-<version>-<rid>-Portable.zip
                    (one component / folder per shipping app)
  -Version defaults to the MinVer version for the app's tag prefix (photon-v for
  the suite). The installer gets /DAppVersion=<SemVer> and /DAppFileVersion=
  <Major.Minor.Patch.RunNumber>. -SkipPublish reuses artifacts/publish as-is.
  When $env:PHOTON_SITE_URL is set (the release workflow passes the repository
  variable), it becomes the installer's publisher and updates URL (/DPublisherUrl);
  otherwise installer/common.iss uses https://www.rizonesoft.com/.
.EXAMPLE
  pwsh scripts/package.ps1 -App Nodus
  pwsh scripts/package.ps1 -App Imago -Version 0.2.0
  pwsh scripts/package.ps1 -Suite -Version 1.0.0
#>
[CmdletBinding(DefaultParameterSetName = 'App')]
param(
  [Parameter(Mandatory, ParameterSetName = 'App')]
  [ValidateSet('Nodus', 'Imago', 'Lumen')]
  [string]$App,
  [Parameter(Mandatory, ParameterSetName = 'Suite')]
  [switch]$Suite,
  [string]$Version,
  [string]$Runtime = 'win-x64',
  [switch]$SkipPublish,
  [switch]$NoZip
)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/_common.ps1"
Add-Type -AssemblyName System.IO.Compression.FileSystem

$dist = Join-Path $RepoRoot 'artifacts/dist'
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$iscc = Find-Iscc

function New-PortableZip([string]$Source, [string]$Destination) {
  if (Test-Path $Destination) { Remove-Item -Force $Destination }
  [IO.Compression.ZipFile]::CreateFromDirectory($Source, $Destination, [IO.Compression.CompressionLevel]::Optimal, $false)
}

function Invoke-Iscc([string]$Script, [string]$SemVer, [string[]]$Extra = @()) {
  $fileVersion = Get-FileVersion $SemVer
  $isccArgs = @(
    '/Q',
    "/DAppVersion=$SemVer",
    "/DAppFileVersion=$fileVersion",
    "/DRuntime=$Runtime",
    "/DOutputDir=$dist"
  )
  if ($env:PHOTON_SITE_URL) { $isccArgs += "/DPublisherUrl=$($env:PHOTON_SITE_URL)" }
  $isccArgs = $isccArgs + $Extra + @((Join-Path $RepoRoot $Script))
  Write-Step "ISCC $Script ($SemVer, file $fileVersion)"
  Invoke-Native $iscc @isccArgs
}

$produced = @()
if ($Suite) {
  $shipping = Get-ShippingApps
  if (-not $Version) { $Version = Get-AppVersion -Project $Apps[$shipping[0]].Project -TagPrefix 'photon-v' }
  foreach ($a in $shipping) {
    if (-not $SkipPublish) { & "$PSScriptRoot/publish.ps1" -App $a -Runtime $Runtime -Version $Version }
  }
  Invoke-Iscc 'installer/Suite.iss' $Version
  $produced += Join-Path $dist "Photon-$Version-$Runtime-Setup.exe"
  if (-not $NoZip) {
    $stage = Join-Path $RepoRoot "artifacts/publish/Photon/$Runtime"
    if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
    New-Item -ItemType Directory -Force -Path $stage | Out-Null
    foreach ($a in $shipping) { Copy-Item -Recurse (Join-Path $RepoRoot "artifacts/publish/$a/$Runtime") (Join-Path $stage $a) }
    $zip = Join-Path $dist "Photon-$Version-$Runtime-Portable.zip"
    Write-Step "zip $zip"
    New-PortableZip $stage $zip
    $produced += $zip
  }
} else {
  $spec = Get-AppSpec $App
  if (-not $spec.Shipping) { throw "$App is not shipping yet (no code); package refused." }
  if (-not $Version) { $Version = Get-AppVersion -Project $spec.Project -TagPrefix $spec.TagPrefix }
  if (-not $SkipPublish) { & "$PSScriptRoot/publish.ps1" -App $App -Runtime $Runtime -Version $Version }
  Invoke-Iscc $spec.Installer $Version
  $produced += Join-Path $dist "$App-$Version-$Runtime-Setup.exe"
  if (-not $NoZip) {
    $zip = Join-Path $dist "$App-$Version-$Runtime-Portable.zip"
    Write-Step "zip $zip"
    New-PortableZip (Join-Path $RepoRoot "artifacts/publish/$App/$Runtime") $zip
    $produced += $zip
  }
}

foreach ($f in $produced) {
  if (-not (Test-Path $f)) { throw "expected output missing: $f" }
  $item = Get-Item $f
  Write-Host ("package.ps1: {0} ({1:N1} MB)" -f $item.FullName, ($item.Length / 1MB)) -ForegroundColor Green
}
