# Bezier Build Script
# Usage: .\build\build.ps1 [-Configuration Release|Debug] [-Clean]

param(
    [ValidateSet("Debug", "Release")]
    [string]$Configuration = "Release",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$SolutionRoot = Split-Path -Parent $PSScriptRoot
$ArtifactsPath = Join-Path $SolutionRoot "artifacts"

Push-Location $SolutionRoot

try {
    if ($Clean) {
        Write-Host "Cleaning artifacts..." -ForegroundColor Cyan
        if (Test-Path $ArtifactsPath) {
            Remove-Item -Recurse -Force $ArtifactsPath
        }
        dotnet clean
    }

    Write-Host "Building solution ($Configuration)..." -ForegroundColor Cyan
    dotnet build --configuration $Configuration

    Write-Host "Running tests..." -ForegroundColor Cyan
    dotnet test --configuration $Configuration --no-build

    Write-Host "Build completed successfully!" -ForegroundColor Green
}
finally {
    Pop-Location
}
