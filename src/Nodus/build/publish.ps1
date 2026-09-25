# Bezier Publish Script
# Usage: .\build\publish.ps1 [-Configuration Release|Debug] [-Runtime win-x64]

param(
    [ValidateSet("Debug", "Release")]
    [string]$Configuration = "Release",
    [string]$Runtime = "win-x64"
)

$ErrorActionPreference = "Stop"
$SolutionRoot = Split-Path -Parent $PSScriptRoot
$PublishPath = Join-Path $SolutionRoot "artifacts\publish\$Runtime"

Push-Location $SolutionRoot

try {
    Write-Host "Publishing Bezier.Desktop ($Configuration, $Runtime)..." -ForegroundColor Cyan
    
    dotnet publish Bezier.Desktop/Bezier.Desktop.csproj `
        --configuration $Configuration `
        --runtime $Runtime `
        --self-contained true `
        --output $PublishPath

    Write-Host "Published to: $PublishPath" -ForegroundColor Green
    Write-Host "Publish completed successfully!" -ForegroundColor Green
}
finally {
    Pop-Location
}
