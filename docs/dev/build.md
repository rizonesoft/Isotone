# Building, packaging, and CI

How the Photon Graphics Suite builds from the repository root: one solution, one build configuration, one package version list.

## Toolchain

| Tool | Version | Notes |
| ---- | ------- | ----- |
| .NET SDK | 10.0.400 (exact) | Pinned in `global.json` with `rollForward: disable`. |
| PowerShell | 7.x | All `scripts/*.ps1` require `pwsh`. |
| Inno Setup | 6.4 or newer | Only for installers. CI installs the pinned Chocolatey package 6.7.1. |
| Python | 3.x | Plan gates (`scripts/todo-graph.py` and friends). |

`tools/provision.ps1` checks all of this and repairs what it can:

```powershell
pwsh tools/provision.ps1 -Verify   # report only; exit 1 on any fault
pwsh tools/provision.ps1           # repair, then verify
```

Repairs: downloads the pinned SDK into `.tools/dotnet-win-x64` (SHA512 verified) when no matching SDK is installed, installs Inno Setup through Chocolatey (winget fallback), and sets `git config core.hooksPath tools/githooks`. A hooks path that already points somewhere else is left alone.

## One build configuration

| File | Role |
| ---- | ---- |
| `global.json` | SDK pin. |
| `Photon.slnx` | Every project: Nodus, Imago, and their tests. |
| `Directory.Build.props` | Shared settings: nullable, implicit usings, `LangVersion` latest, deterministic, SourceLink, strict analyzers, `UseArtifactsOutput`, company and copyright, repository URL, MinVer. |
| `Directory.Build.targets` | Four-part `FileVersion` (see [versioning](versioning.md)). |
| `Directory.Packages.props` | Central package management: every package version, once. |
| `nuget.config` | nuget.org only, with package source mapping. |
| `.editorconfig` | Formatting, naming, and analyzer severities for the whole tree. |
| `tests/Photon.runsettings` | Test results location and the test quarantine list. |
| `src/Nodus/Directory.Build.props`, `src/Imago/Directory.Build.props` | Thin overlays: import the root file, set the app's MinVer tag prefix and product name, and hold the legacy relaxations listed below. |

Nothing else configures the build. The nested `global.json`, `Directory.Packages.props`, `nuget.config`, `.editorconfig`, `.gitignore`, `.gitattributes`, legacy `.sln` files, and per-app CI workflows from the imports were removed.

### Output layout

`UseArtifactsOutput` puts all output under `artifacts/` (gitignored):

| Path | Contents |
| ---- | -------- |
| `artifacts/bin/<Project>/<config>/` | Build output |
| `artifacts/obj/<Project>/` | Intermediate files |
| `artifacts/publish/<App>/<rid>/` | Self-contained publish output (`scripts/publish.ps1`) |
| `artifacts/publish/<App>/<rid>-symbols/` | PDBs split out of the publish folder |
| `artifacts/dist/` | Installers, portable ZIPs, `SHA256SUMS` |
| `artifacts/TestResults/` | Test results |

The repository-root `build/` folder is a gitignored scratch area used by the Claude automation (for example `build/todo-cache.json`). Do not put tracked files there.

## Everyday commands

```powershell
dotnet build Photon.slnx                     # Debug build of everything
dotnet test Photon.slnx                      # all tests
pwsh scripts/build.ps1 -Config Release       # same, scripted (-App Nodus|Imago, -Test)
pwsh scripts/check-all.ps1                   # every gate (below)
pwsh scripts/publish.ps1 -App Nodus          # self-contained publish
pwsh scripts/package.ps1 -App Nodus          # installer and portable ZIP
pwsh scripts/package.ps1 -Suite              # suite installer and ZIP
```

`scripts/apps.psd1` is the app manifest the scripts read: project path, exe name, tag prefix, installer script, and whether the app ships.

### check-all.ps1

Runs, in order, and reports a table at the end (exit 1 if any gate failed):

1. `dotnet build Photon.slnx -c Debug` and `-c Release` (skip with `-SkipBuild`)
2. `dotnet test Photon.slnx -c <Config>` (default Release)
3. `python scripts/todo-graph.py self-test`
4. `python scripts/todo-graph.py validate`
5. `python scripts/todo-graph.py plan --check`
6. `python scripts/todo-claims.py`
7. `python scripts/todo-findings.py --check`
8. `python scripts/todo-runs.py --check`
9. `python scripts/campaign_guard.py --self-test`

A Python gate whose script is missing is skipped with a warning rather than failed.

## Publishing and packaging

`scripts/publish.ps1 -App <App> [-Runtime win-x64] [-Version x.y.z]` publishes self-contained, single-folder, ReadyToRun output. No .NET runtime is needed on the target machine. Publishing passes the app's `MinVerTagPrefix` as a global property, so every project in the app's closure gets the app's version.

`scripts/package.ps1 -App <App> [-Version x.y.z]` publishes, then produces in `artifacts/dist/`:

- `<App>-<version>-win-x64-Setup.exe` (Inno Setup, `installer/<App>.iss`)
- `<App>-<version>-win-x64-Portable.zip`

`scripts/package.ps1 -Suite` publishes every shipping app and produces `Photon-<version>-win-x64-Setup.exe` (`installer/Suite.iss`, one component per app) and `Photon-<version>-win-x64-Portable.zip` (one folder per app).

### Installers

`installer/common.iss` holds the shared defines and `[Setup]` directives. Each app script defines its name, exe, AppId GUID, and icon, then includes it.

- Per-user by default (`PrivilegesRequired=lowest`); the privileges dialog offers an all-users install.
- Each app has its own AppId and its own install folder (`{autopf}\<App>`). The suite has its own AppId, installs each app into its own subfolder of `{autopf}\Photon Graphics Suite`, and uses its own ProgIDs, so it never shares folders or registry keys with the standalone installers.
- x64 only (`x64compatible`), modern wizard, LZMA2 max solid compression, uninstaller, Start menu shortcut, optional desktop icon.
- File associations are opt-in tasks: Nodus `.svg`; Imago `.png`, `.jpg`/`.jpeg`, `.psd`.
- Version from `/DAppVersion` (SemVer) and `/DAppFileVersion` (four-part), passed by `package.ps1`.
- `Lumen.iss` refuses to compile unless `/DLumenShipping` is defined; `apps.psd1` marks Lumen as not shipping, so `publish.ps1` and `package.ps1` refuse it too.

Verified locally on 2026-09-26: `Nodus-0.0.0-alpha.0.2-win-x64-Setup.exe` is 63.1 MB (201.7 MB published, 86.1 MB portable ZIP). It installs silently per-user, registers its uninstaller, and uninstalls cleanly.

## CI

| Workflow | Trigger | What it does |
| -------- | ------- | ------------ |
| `.github/workflows/build.yml` | push and PR to `main` | windows-2025: SDK from `global.json`, restore, Release build, test, upload TRX results. |
| `.github/workflows/plan.yml` (`plan-gates`) | changes to `scripts/`, `todo/`, `docs/reviews/`, `.claude/`, `.conclave/`, hooks, `AGENTS.md` | ubuntu-24.04: `todo-graph.py self-test`, `validate`, `plan --sync` followed by a clean `git status`, `campaign_guard.py --self-test`, and commit-hook integrity (mode 100755, LF blob, eol attribute). |
| `.github/workflows/release.yml` | tags `nodus-v*`, `imago-v*`, `lumen-v*`, `photon-v*` | Resolves the app from the tag prefix, installs Inno Setup if missing, runs the tests, runs `package.ps1`, writes `SHA256SUMS`, and creates the GitHub release (notes from the CHANGELOG section whose heading names the tag, or generated notes; prerelease when the version has a hyphen). |
| `.github/dependabot.yml` | weekly | NuGet (grouped) and GitHub Actions (grouped). |

Every action is pinned by full commit SHA with the tag in a trailing comment.

## Package versions

Checked against nuget.org on 2026-09-26. Held-back majors are deliberate:

| Package | Pinned | Latest | Why held |
| ------- | ------ | ------ | -------- |
| SkiaSharp, SkiaSharp.Views.WPF | 3.119.4 | 4.152.1 | 4.x removes the `SKPaint` text APIs Nodus uses (`TextSize`, `Typeface`, `MeasureText`, `DrawText(string, ...)`); a code migration. |
| Svg.Skia | 4.9.1 | 5.2.3 | 5.x requires SkiaSharp 4. 4.9.1 is the newest on SkiaSharp 3.119. |
| SixLabors.ImageSharp / .Drawing | 3.1.12 / 2.1.7 | 4.1.2 / 3.1.2 | 4.x / 3.x fail the build without a paid Six Labors license key. Dependabot ignores these majors. |
| ReactiveUI.WPF | 23.2.28 | 24.3.0 | 24.x no longer brings `System.Reactive`, which `Imago.UI/GlobalUsings.cs` imports. |
| xunit | 2.9.3 | 2.9.3 (v2) | xunit v3 is a separate package family; migrating is a TODO. |

Upgraded on import: AvalonDock 5.0.0, CommunityToolkit.Mvvm 8.4.2, FluentIcons.Wpf 2.1.341, SharpVectors.Wpf 1.8.6, WPF-UI 4.3.0, Microsoft.Extensions.* 10.0.12, Serilog 4.4.0, Serilog.Extensions.* 10.0.0, Microsoft.CodeAnalysis.CSharp(.Scripting) 5.9.0, Microsoft.NET.Test.Sdk 18.10.1, xunit.runner.visualstudio 4.0.0, coverlet.collector 10.0.1, Moq 4.21.0, FluentAssertions 8.11.0, MinVer 8.0.0. `Microsoft.CodeAnalysis.NetAnalyzers` was dropped because the SDK ships the analyzers. `ReactiveUI.Fody` was dropped because nothing referenced it. Both apps were launch-smoked after the upgrades.

Note: FluentAssertions 8 uses the Xceed community license (free for non-commercial and open-source use). Confirm this fits, or pin 7.x.

## Legacy debt (relaxations to retire)

The imported trees build under the root configuration with the relaxations below. Each one is debt and should have a TODO. Nothing else is relaxed.

### Nodus (`src/Nodus/Directory.Build.props`)

- `TreatWarningsAsErrors=false`: warnings stay visible but do not fail the build.
- `EnforceCodeStyleInBuild=false`: `.editorconfig` IDE rules are not enforced in build.

Warning load under the root analyzers (Release, 2026-09-26, 334 distinct warnings):

| Id | Count | Meaning |
| -- | ----- | ------- |
| CA1305 | 151 | Culture-sensitive formatting without `IFormatProvider` |
| CS0618 | 44 | Obsolete SkiaSharp APIs (blocks SkiaSharp 4) |
| CA2263 | 40 | Prefer generic overloads |
| CA1805 | 20 | Explicit default-value initialization |
| NU1701 | 15 | .NET Framework packages (SkiaSharp.Views.WPF 3.x pulls OpenTK 3.3.1 and OpenTK.GLWpfControl 3.3.0) |
| CA1859 | 14 | Use concrete types for performance |
| CA1861 | 10 | Constant arrays as arguments |
| CA1310 | 9 | String comparison without `StringComparison` |
| CA1806 | 8 | Ignored method results |
| CA2008 | 5 | `Task` creation without `TaskScheduler` |
| other | 18 | CA1720, CA1304, CA1868, CA1869, CS9191, CS0219, CA1001, CS8602, CS0675, CA1852, CS8625 |

### Imago (`src/Imago/Directory.Build.props`)

The full root configuration applies (warnings are errors, code style enforced), except these diagnostics, which stay warnings via `WarningsNotAsErrors`:

- `IDE0005`: unnecessary using directives (12 sites, for example `Imago.Core/GlobalUsings.cs`, `Imago.UI/GlobalUsings.cs`).
- `CS0618`: obsolete API use (2 sites).
- `NU1701`: .NET Framework packages (SkiaSharp.Views.WPF 3.x).

### Test quarantine (`tests/Photon.runsettings`)

These legacy tests are excluded through `TestCaseFilter`. Remove each entry in the same change that fixes its test.

| Test | Symptom |
| ---- | ------- |
| `Bezier.Tests.ElementTooltipTests.ElementTooltip_FromElement_UsesUnnamedForNullName` | Fails every run: expected `"Unnamed"`, got `""`. |
| `Bezier.Tests.AssetLibraryServiceTests.ToggleFavorite_AddsFavorite` | Flaky (about half of runs): favorites state leaks between tests, probably persisted user state. |
| `Bezier.Tests.AssetLibraryServiceTests.ToggleFavorite_RemovesFavorite` | Flaky, same cause. |

### Other known debt

- Projects and namespaces still use the `Bezier.*` names, and the Nodus exe is `Bezier.Desktop.exe` (the installers refer to it by that name).
- The legacy layout remains: `src/Nodus/Bezier.*` and `src/Imago/src/*`, `src/Imago/tests/*`.
- Imago still depends on WPF-UI (`FluentWindow`, `TitleBar`, `wpfui:MenuItem`, `SymbolIcon`, the theme dictionaries, and `DialogService`). Removing it is not a trivial change.
- Imago has no icon: `src/Imago/src/Imago.UI/Assets/imago-icon.png` is an empty file, and `installer/Imago.iss` points at a placeholder, `resources/icons/imago/imago.ico`, which does not exist yet.
- Only x64 is published. There is no win-arm64 publish or installer yet.
- Code is not signed (installers and binaries).
- The WPF temporary projects leave `*_wpftmp` folders under `artifacts/bin/`. They are harmless, but noisy.
