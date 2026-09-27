# Building, packaging, and CI

How the Isotone Graphics Suite builds from the repository root: one solution, one build configuration, one package version list.

## Toolchain

| Tool | Version | Notes |
| ---- | ------- | ----- |
| .NET SDK | 11.0.100-rc.1.26425.128 (exact) | Pinned in `global.json` with `allowPrerelease: true` and `rollForward: disable`: the .NET 11 release candidate (go-live), by operator decision on 2026-09-26. `D00 T02 §8` moves the pin to the GA SDK when .NET 11 ships in November 2026. Builds print `NETSDK1057` ("You are using a preview version of .NET") until then; it is a message, not a warning. |
| PowerShell | 7.x | All `scripts/*.ps1` require `pwsh`. |
| Inno Setup | 7.1 or newer | Only for installers. `scripts/_common.ps1` finds `ISCC.exe` under `Inno Setup 7` (or `$env:ISCC`) and refuses Inno Setup 6. CI installs 7.1.0 from the official release, hash-pinned. |
| Python | 3.x | Plan gates (`scripts/todo-graph.py` and friends). |

`tools/provision.ps1` checks all of this and repairs what it can:

```powershell
pwsh tools/provision.ps1 -Verify   # report only; exit 1 on any fault
pwsh tools/provision.ps1           # repair, then verify
```

Repairs: downloads the pinned SDK into `.tools/dotnet-win-x64` (SHA512 verified) when no matching SDK is installed, installs Inno Setup 7 through winget (`JRSoftware.InnoSetup.7`) with the official `innosetup-7.1.0-x64.exe` (SHA256 pinned) as the fallback (Chocolatey has no Inno Setup 7 package), and sets `git config core.hooksPath tools/githooks`. A hooks path that already points somewhere else is left alone.

## One build configuration

| File | Role |
| ---- | ---- |
| `global.json` | SDK pin. |
| `Isotone.slnx` | Every project: Stilus, Pinxit, and their tests. |
| `Directory.Build.props` | Shared settings: nullable, implicit usings, `LangVersion` latest (no project overrides it), deterministic, SourceLink, strict analyzers, `UseArtifactsOutput`, company and copyright, repository URL, MinVer. |
| `Directory.Build.targets` | Four-part `FileVersion` (see [versioning](versioning.md)). |
| `Directory.Packages.props` | Central package management: every package version, once. |
| `nuget.config` | nuget.org only, with package source mapping. |
| `.editorconfig` | Formatting, naming, and analyzer severities for the whole tree. |
| `tests/Isotone.runsettings` | Test results location and the test quarantine list. |
| `src/Stilus/Directory.Build.props`, `src/Pinxit/Directory.Build.props` | Thin overlays: import the root file, set the app's MinVer tag prefix and product name, and hold the legacy relaxations listed below. |

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
dotnet build Isotone.slnx                     # Debug build of everything
dotnet test Isotone.slnx                      # all tests
pwsh scripts/build.ps1 -Config Release       # same, scripted (-App Stilus|Pinxit, -Test)
pwsh scripts/check-all.ps1                   # every gate (below)
pwsh scripts/publish.ps1 -App Stilus          # self-contained publish
pwsh scripts/package.ps1 -App Stilus          # installer and portable ZIP
pwsh scripts/package.ps1 -Suite              # suite installer and ZIP
pwsh scripts/release-manifest.ps1 -Slug stilus -Name Stilus -Version 0.1.0 -Tag stilus-v0.1.0   # release body and update feed from artifacts/dist (release.yml runs it)
```

`scripts/apps.psd1` is the app manifest the scripts read: project path, exe name, tag prefix, installer script, and whether the app ships.

### check-all.ps1

Runs, in order, and reports a table at the end (exit 1 if any gate failed):

1. `dotnet build Isotone.slnx -c Debug` and `-c Release` (skip with `-SkipBuild`)
2. `dotnet test Isotone.slnx -c <Config>` (default Release)
3. `python scripts/todo-graph.py self-test`
4. `python scripts/todo-graph.py validate`
5. `python scripts/todo-graph.py plan --check`
6. `python scripts/todo-claims.py`
7. `python scripts/todo-findings.py --check`
8. `python scripts/todo-runs.py --check`
9. `python scripts/campaign_guard.py --self-test`
10. `python scripts/build-design-site.py --check`
11. `python scripts/design-lint.py --self-test`
12. `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json`

A Python gate whose script is missing is skipped with a warning rather than failed.

## Publishing and packaging

`scripts/publish.ps1 -App <App> [-Runtime win-x64] [-Version x.y.z]` publishes self-contained, single-folder, ReadyToRun output. No .NET runtime is needed on the target machine. Publishing passes the app's `MinVerTagPrefix` as a global property, so every project in the app's closure gets the app's version.

`scripts/package.ps1 -App <App> [-Version x.y.z]` publishes, then produces in `artifacts/dist/`:

- `<App>-<version>-win-x64-Setup.exe` (Inno Setup, `installer/<App>.iss`)
- `<App>-<version>-win-x64-Portable.zip`

`scripts/package.ps1 -Suite` publishes every shipping app and produces `Isotone-<version>-win-x64-Setup.exe` (`installer/Suite.iss`, the Isotone Graphics Suite installer, one component per shipping app) and `Isotone-<version>-win-x64-Portable.zip` (one folder per app). The suite version comes from `isotone-v*` tags, and every app inside it carries that version.

**Per-app and suite releases are independent.** A `stilus-v*` or `pinxit-v*` tag runs `package.ps1 -App <App>` and ships only that app's installer and ZIP; it never builds or needs the suite installer. An `isotone-v*` tag runs `package.ps1 -Suite` and ships only the suite installer and ZIP. Either way the files are uploaded to `download.rizonesoft.com` (`<slug>/<version>/`), never attached to the GitHub release; [versioning.md](versioning.md) has the layout, the update feed, and the repository settings.

### Installers

`installer/common.iss` holds the shared defines and `[Setup]` directives. Each app script defines its name, exe, AppId GUID, and icon, then includes it.

- Per-user by default (`PrivilegesRequired=lowest`); the privileges dialog offers an all-users install.
- Each app has its own AppId and its own install folder (`{autopf}\<App>`). The suite has its own AppId, installs each app into its own subfolder of `{autopf}\Isotone Graphics Suite`, and uses its own ProgIDs, so it never shares folders or registry keys with the standalone installers.
- Built with Inno Setup 7: a 64-bit Setup program (`SetupArchitecture=x64`) that installs in 64-bit mode (`ArchitecturesAllowed` and `ArchitecturesInstallIn64BitMode` `x64compatible`), modern wizard following the system light or dark theme (`WizardStyle=modern dynamic`), LZMA2 max solid compression, uninstaller, Start menu shortcut, optional desktop icon. Inno 7's changed defaults are accepted: `AppVerName` is set explicitly to `<App> <version>` (now also the default), `TimeStampsInUTC=yes`, `WizardSizePercent=120,120`, Segoe UI 9 pt. None of the removed directives (`WizardResizable`, `WindowVisible`, `EnableFsRedirection`) is used.
- Supported OS: Windows 11. `MinVersion=10.0.17763` still lets Windows 10 (1809 or later) install; on build < 22000 the wizard shows one non-blocking page saying Windows 10 is not officially supported by .NET 11 and the app may work but is untested. Silent installs (`/SILENT`, `/VERYSILENT`) show no wizard pages, so they skip it. The page lives in `common.iss` `[Code]` with `InitializeWizard` and `ShouldSkipPage` event attributes.
- File associations are opt-in tasks: Stilus `.svg`; Pinxit `.png`, `.jpg`/`.jpeg`, `.psd`.
- Version from `/DAppVersion` (SemVer) and `/DAppFileVersion` (four-part), passed by `package.ps1`.
- `Albumen.iss` refuses to compile unless `/DAlbumenShipping` is defined; `apps.psd1` marks Albumen as not shipping, so `publish.ps1` and `package.ps1` refuse it too.

Verified locally on 2026-09-26 with Inno Setup 7.1.0 and the .NET 11 RC SDK (version `0.0.0-alpha.0.9`):

| Output | Setup.exe | Portable ZIP | Published |
| ------ | --------- | ------------ | --------- |
| Stilus | 66.0 MB | 93.1 MB | 233.0 MB |
| Pinxit | 73.5 MB | 103.4 MB | 259.1 MB |
| Suite (`Isotone-...`) | 136.4 MB | 196.5 MB | both apps |

Every Setup.exe is a PE32+ AMD64 image. The Stilus installer installs silently per-user (`/VERYSILENT /CURRENTUSER`; its log reports `Inno Setup version 7.1.0 (64-bit)` and `64-bit install mode: Yes`), registers its uninstaller under HKCU, launches, and uninstalls cleanly. Before the upgrade (Inno 6, .NET 10) Stilus was 63.1 MB, 86.1 MB, and 201.7 MB.

## CI

| Workflow | Trigger | What it does |
| -------- | ------- | ------------ |
| `.github/workflows/build.yml` | push and PR to `main` | windows-2025: SDK from `global.json` (`actions/setup-dotnet` installs the exact prerelease version it names), job `build-windows`: restore, Release build, test, upload TRX results, the design-lint self-test and baseline gates, and the optional design reference renders. |
| `.github/workflows/plan.yml` (`plan-gates`) | changes to `scripts/`, `todo/`, `docs/reviews/`, `.claude/`, `.conclave/`, hooks, `AGENTS.md` | ubuntu-26.04: `todo-graph.py self-test`, `validate`, `plan --sync` followed by a clean `git status`, `campaign_guard.py --self-test`, and commit-hook integrity (mode 100755, LF blob, eol attribute), plus the design-lint self-test and the design page check (job `plan-gates`); job `campaign-guard` runs the guard self-test on windows-2025. The path list also covers `docs/design/**` and `resources/icons/**`. |
| `.github/workflows/pages.yml` (`design-pages`) | changes to `docs/design/`, `resources/icons/`, `scripts/build-design-site.py` | ubuntu-26.04: checks the committed design page against its sources and deploys it to https://rizonesoft.github.io/Isotone/design/. |
| `.github/workflows/release.yml` | tags `stilus-v*`, `pinxit-v*`, `albumen-v*`, `isotone-v*`; manual dispatch with `tag` and `draft` inputs (the draft dry run) | Resolves the app from the tag prefix (`isotone-v*` is the suite), fails a tag release whose distribution storage secrets are missing (a draft skips the upload with a notice instead), installs Inno Setup 7.1.0 from the official release with a pinned SHA256 unless `Program Files\Inno Setup 7` exists (the image's Inno Setup 6 is never used), runs the tests, runs `package.ps1` (with `ISOTONE_SITE_URL` as the installer's publisher URL), writes `SHA256SUMS`, writes the release body and update feed (`scripts/release-manifest.ps1`), uploads the files to `download.rizonesoft.com` with a hash-pinned rclone and checks each public URL, creates the GitHub release with no attached files (the body: the CHANGELOG section whose heading names the tag, Download links, the SHA-256 table, and the source link; prerelease when the version has a hyphen), and writes the update feed last. |
| `.github/dependabot.yml` | weekly | NuGet (grouped) and GitHub Actions (grouped). |

Every action is pinned by full commit SHA with the tag in a trailing comment.

## Package versions

Checked against nuget.org on 2026-09-26 (`dotnet list Isotone.slnx package --outdated --include-prerelease`). Every package is on its latest stable release, except where the table says why:

| Package | Pinned | Why |
| ------- | ------ | --- |
| Microsoft.Extensions.DependencyInjection, .Hosting | 11.0.0-rc.1.26425.128 | Match the .NET 11 RC runtime of the pinned SDK. They move to 11.0.x stable with the GA SDK pin (`D00 T02 §8`). |
| SkiaSharp, SkiaSharp.Views.WPF | 4.152.1 | Latest stable; 4.153 and 4.154 are previews. |
| xunit.v3.mtp-off | 4.0.1 | xUnit v3 without Microsoft.Testing.Platform. The plain `xunit.v3` 4.x package brings `xunit.v3.mtp-v2`, and the .NET 10+ SDK then refuses VSTest `dotnet test` ("Testing with VSTest target is no longer supported by Microsoft.Testing.Platform"). The mtp-off flavor keeps `dotnet test` on VSTest through `xunit.runner.visualstudio` 4.0.0, so `tests/Isotone.runsettings` (results folder, quarantine filter) still applies. Test projects set `OutputType` `Exe`. |
| AwesomeAssertions | 9.6.0 | Replaces FluentAssertions 8 (Xceed commercial license); Apache-2.0 fork of FluentAssertions 7 with the same API. The decision record is owed by `D00 T02 §5`. |
| Serilog.Extensions.Logging, .Hosting | 10.0.0 | Latest stable; they depend on Microsoft.Extensions.* abstractions, which central transitive pinning lifts to 11.0.0-rc.1. |
| Dirkster.AvalonDock (+ Themes.VS2013) | 5.0.0 | Latest stable; 5.0.1 is a preview. |
| SharpVectors.Wpf | 1.8.6 | Latest. Used only by the Stilus splash logo (`SplashWindow.xaml`, `svgc:SvgViewbox`); `D02 T02 §2` replaces it and drops the package. |
| WPF-UI | 4.3.0 | Latest. Pinxit only; removal is planned. |

The rest are latest stable: MinVer 8.0.0, FluentIcons.Wpf 2.1.341, CommunityToolkit.Mvvm 8.4.2, ComputeSharp 3.2.0, Microsoft.CodeAnalysis.CSharp(.Scripting) 5.9.0, Serilog 4.4.0, Serilog.Sinks.File 7.0.0, Serilog.Sinks.Debug 3.0.0, Microsoft.NET.Test.Sdk 18.10.1, xunit.runner.visualstudio 4.0.0, coverlet.collector 10.0.1, Moq 4.21.0.

Removed on 2026-09-26 because no code used them (evidence: no type or namespace from the package in any `.cs` or `.xaml` file): ReactiveUI.WPF, SharpDX.DirectInput, SixLabors.ImageSharp, SixLabors.ImageSharp.Drawing (Pinxit); Newtonsoft.Json, AvalonEdit (with its unused `VsCodeDarkXml.xshd`), Svg.Skia (Stilus). `ComputeSharp` and `SkiaSharp.Views.WPF` in `Pinxit.Rendering` are also unused today but stay for the planned rendering work (`D03 T02 §2`, `D03 T02 §5`).

### The SkiaSharp 4 migration

SkiaSharp 4 removed the `SKPaint` text members (`TextSize`, `Typeface`, `MeasureText`) and the `DrawText(string, x, y, SKPaint)` overload. `SkiaRenderer.cs` now measures and draws text through `SKFont` and `SKCanvas.DrawText(string, x, y, SKTextAlign, SKFont, SKPaint)`, and builds paths through `SKPathBuilder` (the mutating `SKPath.MoveTo`/`LineTo`/`Close` are obsolete). A throwaway comparison of 3.119.4 (old API) against 4.152.1 (new API) measured identical text widths and bounds and 0 to 5 differing anti-aliased edge pixels per string.

SkiaSharp.Views.WPF 4 has a `net10.0-windows10.0.19041` dependency group (OpenTK 4.3.0, GLWpfControl 4.2.3) and a .NET Framework group (OpenTK 3.3.1). A plain `net11.0-windows` project resolves the .NET Framework group and reports NU1701, so every WPF project targets `net11.0-windows10.0.26100.0` with `TargetPlatformMinVersion` 10.0.17763.0 (Windows 10 1809). The cost is the Windows SDK projection in each publish (`Microsoft.Windows.SDK.NET.dll`, 56.9 MB with ReadyToRun, about 3 MB compressed in the installer).

## Legacy debt (relaxations to retire)

The imported trees build under the root configuration with the relaxations below. Each one is debt and should have a TODO. Nothing else is relaxed.

### Stilus (`src/Stilus/Directory.Build.props`)

- `TreatWarningsAsErrors=false`: warnings stay visible but do not fail the build.
- `EnforceCodeStyleInBuild=false`: `.editorconfig` IDE rules are not enforced in build.

Warning load under the root analyzers (clean Release build on the .NET 11 RC SDK, 2026-09-26, 219 distinct sites counted by file, line, and column; the earlier figure of 334 counted the WPF temporary project's duplicates and the CS0618 and NU1701 groups the SkiaSharp 4 migration removed):

| Id | Count | Meaning |
| -- | ----- | ------- |
| CA1305 | 121 | Culture-sensitive formatting without `IFormatProvider` |
| CA2263 | 40 | Prefer generic overloads |
| CA1805 | 17 | Explicit default-value initialization |
| CA1310 | 9 | String comparison without `StringComparison` |
| CA1859 | 8 | Use concrete types for performance |
| CA1806 | 4 | Ignored method results |
| other | 20 | CA1720, CA1304, CA1868, CA2008, CA1869, CA1861 (2 each); CS8602, CS0675, CA1830, CA1852, CS0219, CS9191, CA1001, CS8625 (1 each) |

### Pinxit (`src/Pinxit/Directory.Build.props`)

The full root configuration applies (warnings are errors, code style enforced), except these diagnostics, which stay warnings via `WarningsNotAsErrors`:

- `IDE0005`: unnecessary using directives (6 sites, for example `Pinxit.Core/GlobalUsings.cs`, `Pinxit.UI/GlobalUsings.cs`).
- `CS0618`: obsolete API use (1 site: WPF-UI `IContentDialogService.SetDialogHost` in `Views/MainWindow.xaml.cs`).

`NU1701` left the list on 2026-09-26: SkiaSharp.Views.WPF 4 on the Windows SDK TFM restores OpenTK 4 for .NET. The .NET 11 SDK also enforces `IDE1006` naming in the WPF markup-compile pass and adds `IDE0054` and `IDE0330`; the handful of Pinxit sites they found were fixed, and `.editorconfig` gained a private-constants naming rule because the new Roslyn matches `const` fields against `required_modifiers = static`.

### Test quarantine (`tests/Isotone.runsettings`)

These legacy tests are excluded through `TestCaseFilter`. Remove each entry in the same change that fixes its test.

| Test | Symptom |
| ---- | ------- |
| `Bezier.Tests.ElementTooltipTests.ElementTooltip_FromElement_UsesUnnamedForNullName` | Fails every run: expected `"Unnamed"`, got `""`. |
| `Bezier.Tests.AssetLibraryServiceTests.ToggleFavorite_AddsFavorite` | Flaky (about half of runs): favorites state leaks between tests, probably persisted user state. |
| `Bezier.Tests.AssetLibraryServiceTests.ToggleFavorite_RemovesFavorite` | Flaky, same cause. |

### Other known debt

- Projects and namespaces still use the `Bezier.*` names, and the Stilus exe is `Bezier.Desktop.exe` (the installers refer to it by that name).
- The legacy layout remains: `src/Stilus/Bezier.*` and `src/Pinxit/src/*`, `src/Pinxit/tests/*`.
- Pinxit still depends on WPF-UI (`FluentWindow`, `TitleBar`, `wpfui:MenuItem`, `SymbolIcon`, the theme dictionaries, and `DialogService`). Removing it is not a trivial change.
- Pinxit has no icon yet: `src/Pinxit/src/Pinxit.UI/Assets/pinxit-icon.png` is an empty file, and `installer/Pinxit.iss` points at `resources/icons/pinxit/pinxit.ico`, which does not exist yet. The icon design is chosen and its SVG sources are committed (`resources/icons/README.md`); `D00 T03 §3` generates `pinxit.ico` and the PNGs for all three apps from those SVGs, and `D03 T01 §4` wires Pinxit's into the executable.
- Only x64 is published. There is no win-arm64 publish or installer yet.
- Code is not signed (installers and binaries).
- The SDK is the .NET 11 release candidate (`11.0.100-rc.1.26425.128`) and Microsoft.Extensions.* are `11.0.0-rc.1`; `D00 T02 §8` pins GA when it ships (November 2026), and the first product release waits for it.
- SharpVectors.Wpf ships only for the Stilus splash logo; `D02 T02 §2` replaces the `SvgViewbox` and drops it.
- The WPF temporary projects leave `*_wpftmp` folders under `artifacts/bin/`. They are harmless, but noisy.
