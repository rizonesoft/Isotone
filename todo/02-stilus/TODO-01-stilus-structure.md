---
schema_version: 1
id: stilus-structure
domain: 02-stilus
status: draft
title: "TODO-01 -- Stilus Layout, Names, and Composition Root"
depends_on: []
track: N1
---

# TODO-01 -- Stilus Layout, Names, and Composition Root

> **Goal:** The imported Bezier code is Stilus in every name a user or developer meets: `Isotone.Stilus.*` projects and namespaces in the target layout, an executable called `Stilus.exe`, one composition root on the Generic Host with every service registered, logging through the suite's Serilog bootstrap, and a build with warnings as errors and code style enforced, like the rest of the suite.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Stilus is three projects under `src/Stilus/`: `Bezier.Core` (`net11.0`), `Bezier.Desktop` (`net11.0-windows10.0.26100.0`, WPF, no `AssemblyName`, so the executable is `Bezier.Desktop.exe`), and `Bezier.Tests`. 147 `.cs` files declare a `Bezier` namespace, 11 XAML files use `x:Class="Bezier..."` or `clr-namespace:Bezier`, and 17 string literals say "Bezier" (window title `Bezier`, `"Bezier - Untitled"`, `%LOCALAPPDATA%\Bezier` folders). `scripts/apps.psd1`, `installer/Stilus.iss`, and `installer/Suite.iss` name `Bezier.Desktop.exe`. The composition root is `ServiceCollectionExtensions.AddBezierServices`, which registers only `MainWindowViewModel`; the `HistoryManager` and `ToolManager` registrations are commented out, and `MainWindowViewModel` constructs `SvgImporter`, `SvgExporter`, `HistoryManager`, and `ToolManager` itself with `new`. `App.Services` is a static service locator. Logging goes through a custom `DebugLogger` singleton that feeds the debug window and writes no file. `src/Stilus/Directory.Build.props` sets `TreatWarningsAsErrors=false` and `EnforceCodeStyleInBuild=false`; the Release build reports 334 distinct warnings (CA1305 151, CS0618 44, CA2263 40, CA1805 20, NU1701 15, CA1859 14, CA1861 10, CA1310 9, CA1806 8, CA2008 5, others 18, per `docs/dev/build.md`).
>
> **Corrected 2026-09-26:** the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune) moved Stilus to .NET 11 (said `net10.0` and `net10.0-windows`; `Bezier.Desktop` and `Bezier.Tests` now target `net11.0-windows10.0.26100.0` with `TargetPlatformMinVersion` 10.0.17763.0, which also selects SkiaSharp.Views.WPF 4's OpenTK 4 dependency group) and to SkiaSharp 4.152.1, and deleted the unreferenced `Services/SvgVisualEditor.cs`, so 146 files declare a `Bezier` namespace (said 147). The Release build now reports no CS0618 and no NU1701 for Stilus; the remaining counts are in `docs/dev/build.md`.
<!-- claim: exists src/Stilus/Bezier.Desktop/Bezier.Desktop.csproj -->
<!-- claim: count "^namespace Bezier" src/Stilus/**/*.cs = 146 -->
<!-- claim: count "<TargetFramework>net11.0-windows10.0.26100.0</TargetFramework>" src/Stilus/Bezier.Desktop/Bezier.Desktop.csproj = 1 -->
<!-- claim: count "Exe       = 'Bezier.Desktop.exe'" scripts/apps.psd1 = 1 -->
<!-- claim: count "#define AppExeName \"Bezier.Desktop.exe\"" installer/Stilus.iss = 1 -->
<!-- claim: count "#define StilusExe \"Bezier.Desktop.exe\"" installer/Suite.iss = 1 -->
<!-- claim: count "// services.AddSingleton" src/Stilus/Bezier.Desktop/ServiceCollectionExtensions.cs = 2 -->
<!-- claim: count "private readonly (SvgImporter|SvgExporter|HistoryManager|ToolManager) _\w+ = new\(\);" src/Stilus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 4 -->
<!-- claim: count "<TreatWarningsAsErrors>false</TreatWarningsAsErrors>" src/Stilus/Directory.Build.props = 1 -->

## Inputs

- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- the target layout and names
- [`docs/dev/build.md`](../../docs/dev/build.md) -- the warning table §4 and §5 clear, and the SkiaSharp hold §6 lifts
- [`standards/shared.md`](../../standards/shared.md), [`standards/stilus.md`](../../standards/stilus.md) -- composition, logging, and culture rules
- [`scripts/apps.psd1`](../../scripts/apps.psd1), [`installer/Stilus.iss`](../../installer/Stilus.iss), [`Isotone.slnx`](../../Isotone.slnx) -- the files that name the executable and the projects
- -> XREF: D00 T02 §6 -- the xUnit v3 migration that waits for §1 to move the test project
- -> XREF: D00 T03 §3 -- the app icon raster export (`resources/icons/stilus/stilus.ico` and `PNG/stilus_*.png`, regenerated from the Direction C SVGs, that §1 wires in)
- -> XREF: D01 T02 §1 -- the logging bootstrap §2 and §3 consume
- -> XREF: D02 T07 §1 -- the live-object contract, first of the Stilus parity sections whose checklists name the `Isotone.Stilus.*` paths §1's rename creates
- -> XREF: D02 T11 §1 -- the effect framework whose paths assume §1's rename

## Outcome

- `src/Stilus/Isotone.Stilus.Core/`, `src/Stilus/Isotone.Stilus.Desktop/`, and `tests/Isotone.Stilus.Tests/` build, with `Isotone.Stilus.*` namespaces throughout and no `Bezier` identifier left in code, XAML, scripts, or installers.
- The published app is `Stilus.exe` with the Stilus icon, and the installer and portable ZIP carry it.
- `App.xaml.cs` builds a Generic Host; every service a view model or tool uses is registered and constructor-injected; no `new` of a service inside a view model and no static locator.
- The debug window's console reads the Serilog pipeline, and every Stilus log line reaches `%LOCALAPPDATA%\Rizonesoft\Stilus\logs\`.
- The Release build of Stilus has zero warnings, with `TreatWarningsAsErrors` and `EnforceCodeStyleInBuild` on, on SkiaSharp 4.

**Adjacency:** list=not-applicable (no user records here); document=not-applicable (no printed output); settings=not-applicable (settings arrive with the Isotone.Core store in D01 T02 §2); reporting=not-applicable (no summaries); notifications=not-applicable (no long operations); permissions=not-applicable (nothing new is written); audit=applicable; exchange=not-applicable (formats are TODO-04's); reverse=not-applicable (no user edits introduced)

**Adjacency rationale:** This file is structure and hygiene. Its one user-relevant outcome is that Stilus actions reach a real log file (§3), which is the audit trail's foundation.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On         | Status |
| :---: | :-----: | ---------------------------------------------------- | ------------------ | :----: |
|   1   |   §1    | Rename Bezier to Isotone.Stilus                        | D00 T02 §1, D00 T03 §3 |  [ ]   |
|   2   |   §2    | Composition root on the Generic Host                 | §1, D01 T02 §1     |  [ ]   |
|   3   |   §3    | The debug console reads the Serilog pipeline         | §2                 |  [ ]   |
|   4   |   §4    | Culture-safe formatting and comparisons              | §1                 |  [ ]   |
|   5   |   §5    | The rest of the analyzer backlog                     | §4                 |  [ ]   |
|   6   |   §6    | SkiaSharp 4                                          | §5, D02 T02 §2     |  [ ]   |
|   7   |   §7    | Warnings are errors in Stilus                         | §6                 |  [ ]   |

---

## 1. Rename Bezier to Isotone.Stilus

Every later Stilus section names files; doing the rename first means each of them is written once against the final paths. It is a mechanical change with a wide blast radius, so it changes names only: no behavior, no formatting, no refactor rides along. Git sees renames when content stays mostly the same, which keeps `git log --follow` working through the history imported from Bezier.

- [ ] `git mv src/Stilus/Bezier.Core src/Stilus/Isotone.Stilus.Core` and rename the project file to `Isotone.Stilus.Core.csproj`. Done when: the folder and file exist under the new names.
- [ ] `git mv src/Stilus/Bezier.Desktop src/Stilus/Isotone.Stilus.Desktop`, rename the project file, and set `<AssemblyName>Stilus</AssemblyName>` and `<RootNamespace>Isotone.Stilus.Desktop</RootNamespace>`. Done when: the Debug build produces `artifacts/bin/Isotone.Stilus.Desktop/debug/Stilus.exe`.
- [ ] `git mv src/Stilus/Bezier.Tests tests/Isotone.Stilus.Tests`, rename its project file, and fix its `ProjectReference` paths. Done when: `dotnet test Isotone.slnx` discovers the same number of tests as before the rename.
- [ ] Rewrite `namespace Bezier` to `namespace Isotone.Stilus` and every `using Bezier` to `using Isotone.Stilus` in all `.cs` files, and `x:Class`/`clr-namespace` values in all XAML. Done when: `grep -rn "Bezier" src/Stilus tests/Isotone.Stilus.Tests --include=*.cs --include=*.xaml` prints only string literals handled by the next item.
- [ ] Replace user-visible and path strings: the window title and `"Bezier - ..."` titles become `Stilus`, `AddBezierServices` becomes `AddStilusServices`, and `%LOCALAPPDATA%\Bezier` paths in `FileOperationsService` and `AssetLibraryService` become `%LOCALAPPDATA%\Rizonesoft\Stilus` (the `Isotone.Core` paths arrive in `D01 T02 §1`). Done when: `grep -rni "bezier" src/Stilus tests/Isotone.Stilus.Tests --include=*.cs --include=*.xaml` prints nothing except the curve type (`BezierSegment`, cubic Bezier math), each remaining hit quoted in the commit body.
- [ ] Replace `Resources/Icons/Bezier.ico`, `Bezier.svg`, and `Bezier_32.png` with the Stilus icon from `resources/icons/stilus/` (`stilus.ico`, `stilus.svg`, `PNG/stilus_32.png`) and point `ApplicationIcon` and the `Resource` items at them (**Corrected 2026-09-27:** the operator chose a new icon design that day (Direction C, `resources/icons/README.md`); `stilus.ico` and `PNG/stilus_32.png` are generated by `D00 T03 §3` from `stilus.svg` and the hand-tuned small SVGs, which overwrites the old-design rasters under the same names, so link the generated files and never edit or re-export them here; `stilus.svg` is a 256 px master that WPF cannot draw without SharpVectors, so the window icon and any in-app use take a PNG). Done when: `Stilus.exe` shows the Stilus icon in Explorer.
- [ ] Update `Isotone.slnx`, `scripts/apps.psd1` (`Project` and `Exe = 'Stilus.exe'`), `installer/Stilus.iss` (`AppExeName`), `installer/Suite.iss` (`StilusExe`), and the Stilus lines of `docs/dev/build.md`, `standards/stilus.md` (drop the "today `Bezier.*`" notes), and `AGENTS.md`. Done when: `grep -rn "Bezier.Desktop\|Bezier.Core\|Bezier.Tests" --include=*.slnx --include=*.psd1 --include=*.iss --include=*.md . | grep -v "^./docs/legacy/"` prints nothing.
- [ ] Rewrite every `src/Stilus/Bezier.*` and `Bezier.Tests` path in `todo/` claims and prose to the new paths, and re-run `python scripts/todo-claims.py`. Done when: it exits 0.
- [ ] Delete the unreferenced `src/Stilus/Resources/` (the old Bezier icon set and `icons_filled.md`/`icons_regular.md`), after `grep -rn "Stilus/Resources\|icons_filled\|icons_regular" src scripts installer` prints nothing (**Groomed 2026-09-28:** no section owned it, and it fails this file's Verification grep). Done when: the folder is gone and the Release build is green.
- [ ] Commit: `"stilus: rename Bezier to Isotone.Stilus and ship Stilus.exe"`

**Requires:** display-session -- confirming the Stilus icon in Explorer and the installed app starting needs an interactive desktop
**Test checkpoint:** `dotnet build Isotone.slnx -c Release` exits 0; `dotnet test Isotone.slnx` exits 0 with the same test count as before the rename; `pwsh scripts/package.ps1 -App Stilus` produces a Setup exe whose silent install creates `Stilus.exe` (quote `Get-ChildItem "$env:LOCALAPPDATA\Programs\Stilus\Stilus.exe"`); `git log --follow --oneline src/Stilus/Isotone.Stilus.Core/Models/VectorDocument.cs | wc -l` is greater than 1, proving history survived. Cheaper substitute that fails: setting `AssemblyName` only, which leaves every namespace and path saying Bezier.

## 2. Composition Root on the Generic Host

`standards/shared.md` requires one composition root per app with constructor injection and no static locator. Today the root registers one type, and the main view model builds its own services, so nothing can be replaced in a test and the per-document lifetime the standard asks for cannot exist. This section wires what exists; it does not add features.

- [ ] Replace `App.OnStartup`'s `ServiceCollection` with `Host.CreateApplicationBuilder` (or `Host.CreateDefaultBuilder`) in `src/Stilus/Isotone.Stilus.Desktop/App.xaml.cs`, calling `UseIsotoneLogging("Stilus")` from `Isotone.Core`, starting the host before the main window and stopping it on exit. Done when: startup and shutdown each log one Information line.
- [ ] `AddStilusServices` registers `SvgImporter`, `SvgExporter` (transient), `ToolManager` and every tool (singleton), `HistoryManager` (singleton until per-document scopes land with tabs), `DebugInfoService`, `PerformanceMetricsService`, and `IconCatalog`/`IconService`. Done when: the commented-out lines are gone and a `ServiceRegistrationTests` test resolves every registered type from a built provider.
- [ ] `MainWindowViewModel` receives its services through its constructor instead of `new`. Done when: the file has no `= new SvgImporter()`, `new SvgExporter()`, `new HistoryManager()`, or `new ToolManager()`.
- [ ] Remove the static `App.Services` property and every use of it; the main window is resolved from the host. Done when: `grep -rn "App.Services" src/Stilus` prints nothing.
- [ ] Commit: `"stilus: one composition root on the Generic Host"`

**Requires:** display-session -- the launch smoke proving the host starts the main window needs an interactive desktop

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `ServiceRegistrationTests` reporting; launching `Stilus.exe` shows the main window and writes `Host started` and, on File, Exit, `Host stopped` to `%LOCALAPPDATA%\Rizonesoft\Stilus\logs\`; the captures in `docs/captures/stilus/main-window/` still match. Cheaper substitute that fails: uncommenting the two registrations and leaving the `new` calls, which the grep catches.

## 3. The Debug Console Reads the Serilog Pipeline

`DebugLogger` is a second logging system: it keeps an in-memory list for the debug window and writes nothing to disk, so a user's crash leaves no trace. The debug window is worth keeping; its private logger is not. It becomes a Serilog sink.

- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Diagnostics/InMemoryLogSink.cs` (a bounded ring buffer of `LogEvent`s implementing `ILogEventSink`, raising an event on the dispatcher) and register it in the logger configuration. Done when: `InMemoryLogSinkTests` prove the bound and the ordering.
- [ ] `DebugWindow` reads from `InMemoryLogSink` instead of `DebugLogger`; its export writes the buffered events as text. Done when: the debug window shows the same entries the log file receives for a session.
- [ ] Replace every `DebugLogger.Instance.Log/Error/Warn` call with an injected `ILogger<T>` (or `Serilog.ILogger` where a type has no DI) using structured templates. Done when: `grep -rn "DebugLogger" src/Stilus` prints nothing and `DebugLogger.cs` is deleted.
- [ ] Every user action that changes the document or a setting already routed through a command logs one Information line naming the action (`Executed {Command} on {Count} element(s)` in `HistoryManager`). Done when: a test with a Serilog test logger asserts the line for `AddElementCommand`.
- [ ] Commit: `"stilus: route the debug console through Serilog and retire DebugLogger"`

**Requires:** display-session -- showing the debug window's live console needs an interactive desktop

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `InMemoryLogSinkTests` reporting; a driven run (draw a rectangle, undo, open the debug window with F12) shows the add and undo lines in both the debug console and the day's log file (quote both); `grep -rn "class DebugLogger" src` prints nothing. Cheaper substitute that fails: making `DebugLogger` also write a file, which keeps two logging systems.

## 4. Culture-Safe Formatting and Comparisons

CA1305 (151 sites), CA1304, and CA1310 (9) are the largest warning group and a real defect class for a document editor: an SVG written on a machine whose culture uses a decimal comma is invalid. Each site is decided, not blanket-fixed: text written to a file, a log property, or compared as an identifier uses the invariant culture; text shown to the user uses the current culture.

- [ ] Fix every CA1305 site in `Isotone.Stilus.Core` with `CultureInfo.InvariantCulture` (the SVG reader and writer, path data, numbers in ids). Done when: the Core project reports 0 CA1305.
- [ ] Fix every CA1305 site in `Isotone.Stilus.Desktop`, using `CultureInfo.CurrentCulture` for status-bar and panel text and invariant for anything persisted. Done when: the Desktop project reports 0 CA1305.
- [ ] Fix every CA1304 and CA1310 site with an explicit culture or `StringComparison.Ordinal`/`OrdinalIgnoreCase`. Done when: 0 of each.
- [ ] Add `SvgExporterCultureTests`: with `CultureInfo.CurrentCulture` set to `de-DE`, export a document with fractional coordinates and assert the SVG uses `.` decimals and reparses to equal coordinates. Done when: the test passes and fails if one `ToString()` loses its culture argument.
- [ ] Commit: `"stilus: format and compare with an explicit culture everywhere"`

**Test checkpoint:** `dotnet build Isotone.slnx -c Release -v q 2>&1 | grep -cE "CA1305|CA1304|CA1310"` prints 0; `dotnet test Isotone.slnx` exits 0 with `SvgExporterCultureTests` reporting. Cheaper substitute that fails: setting `CultureInfo.DefaultThreadCurrentCulture` to invariant at startup, which silences the analyzer's intent and shows users invariant numbers.

## 5. The Rest of the Analyzer Backlog

With culture done, about 120 warnings remain outside the SkiaSharp obsolescence group (CS0618, which §6 clears by migrating) and NU1701 (which leaves with SkiaSharp.Views.WPF 3.x). **Corrected 2026-09-26:** CS0618 and NU1701 already left with the toolchain upgrade, so nothing is carved out any more. Each rule is fixed as its analyzer documentation says, not suppressed.

- [ ] Fix CA2263 (40, prefer generic overloads) and CA1805 (20, explicit default initialization). Done when: 0 of each.
- [ ] Fix CA1859 (14), CA1861 (10), CA1806 (8, a result that is ignored is either used or discarded with `_ =` and a comment saying why it is safe), and CA2008 (5, pass `TaskScheduler.Default`). Done when: 0 of each.
- [ ] Fix the remaining 18 (CA1720, CA1868, CA1869, CS9191, CS0219, CA1001, CS8602, CS0675, CA1852, CS8625), treating each nullable warning (CS8602, CS8625) as a possible bug and adding a test where it was one. Done when: the Release build reports no warning for Stilus. **Corrected 2026-09-26:** said "only CS0618 and NU1701"; both left with the toolchain upgrade.
- [ ] Commit: `"stilus: clear the analyzer backlog apart from the SkiaSharp migration"`

**Test checkpoint:** `dotnet build Isotone.slnx -c Release -v q 2>&1 | grep -E "warning (CA|CS|IDE)" | grep -v "CS0618" | grep -c "src/Stilus"` prints 0; `dotnet test Isotone.slnx` exits 0 with the same count as before the section. Cheaper substitute that fails: `<NoWarn>` entries in the Stilus props, which the grep does not see but review does.

## 6. SkiaSharp 4

SkiaSharp 4 removes the `SKPaint` text APIs Stilus uses (`TextSize`, `Typeface`, `MeasureText`, `DrawText(string, ...)`), which is why 44 CS0618 warnings exist and why the package is held at 3.119.4.

**Corrected 2026-09-26:** the migration was done out of band by the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune), ahead of `D02 T02 §2` (Svg.Skia turned out to be referenced by nothing and was removed in the same change). SkiaSharp and SkiaSharp.Views.WPF are 4.152.1; `SkiaRenderer.cs` draws and measures text through `SKFont` and `SKCanvas.DrawText(string, x, y, SKTextAlign, SKFont, SKPaint)`, builds its polygon, polyline, and ruler-indicator paths with `SKPathBuilder`, and `SkiaToolRenderContext.DrawText` uses the non-obsolete overload; Pinxit needed no source change. NU1701 did not leave with the package bump alone: SkiaSharp.Views.WPF 4 ships a `net10.0-windows10.0.19041` group with OpenTK 4.3.0 and GLWpfControl 4.2.3, and plain `net11.0-windows` fell back to the .NET Framework group, so the Stilus WPF projects moved to `net11.0-windows10.0.26100.0`. Rendering parity was measured in a throwaway harness (SkiaSharp 3.119.4 old API against 4.152.1 new API, four strings, Segoe UI and Arial, 10 to 48 px, bold italic included): `MeasureText` widths and bounds identical, 0 to 5 differing anti-aliased edge pixels out of 63 to 5,038 ink pixels. The harness was not committed, so the items below keep the committed regression test and the captures; the package and code items are rewritten to verify rather than perform. Migrating clears them, drops the .NET Framework OpenTK packages SkiaSharp.Views.WPF 3.x pulls in (NU1701), and unblocks current fixes. It runs after the SVG decision (`D02 T02 §2`), which removes Svg.Skia, the other package pinned to SkiaSharp 3.

- [ ] Verify `SkiaSharp` and `SkiaSharp.Views.WPF` are on the current 4.x in `Directory.Packages.props` (moved out of band). Done when: `dotnet restore Isotone.slnx` exits 0 and no NU1701 is reported for Stilus.
- [ ] Verify text drawing and measuring in `SkiaRenderer.cs`, `SkiaToolRenderContext.cs`, and the text tool are on `SKFont` (rewritten out of band) (`SKFont.Size`, `SKFont.Typeface`, `SKFont.MeasureText`, `SKCanvas.DrawText(string, x, y, SKTextAlign, SKFont, SKPaint)`). Done when: 0 CS0618 in Stilus. Source: the SkiaSharp 4 migration notes in the SkiaSharp repository's release notes.
- [ ] Verify Pinxit's `Pinxit.Rendering` builds on the same version (it references SkiaSharp through global usings; nothing broke out of band). Done when: the whole solution builds.
- [ ] Add `SkiaRendererTextTests`: render a text element at a fixed size to an `SKBitmap` and compare its ink bounds with a 3.x rendering within 1 pixel. **Corrected 2026-09-26:** the tree is already on 4.x, so the 3.x reference is produced by a one-off program pinned to SkiaSharp 3.119.4 with the old `SKPaint` text API (the harness recipe above), committed as `tests/fixtures/stilus/render/text-3x.png` with its generator's package version recorded beside it. Done when: the test passes.
- [ ] Verify the SkiaSharp rows are gone from the held-back table in `docs/dev/build.md` and `NU1701` from `src/Pinxit/Directory.Build.props` (both done out of band). Done when: both files are current.
- [ ] Commit: `"stilus: migrate to SkiaSharp 4 and the SKFont text API"`

**Requires:** display-session -- the canvas launch smoke after a renderer upgrade needs an interactive desktop

**Test checkpoint:** `dotnet build Isotone.slnx -c Release -v q 2>&1 | grep -cE "CS0618|NU1701"` prints 0; `dotnet test Isotone.slnx` exits 0 with `SkiaRendererTextTests` reporting; opening `tests/fixtures/stilus/svg/bezier-sample.svg` in Stilus renders the same as `docs/captures/stilus/main-window/sample-100.png` (new capture `sample-skia4-100.png` committed beside it). Cheaper substitute that fails: `#pragma warning disable CS0618` around the old calls, which leaves the package held.

## 7. Warnings Are Errors in Stilus

The Stilus overlay is the last place in the suite where a warning does not fail the build. With the backlog at zero, the two relaxations are removed and the overlay holds only the app's identity, like Pinxit's.

- [ ] Remove `TreatWarningsAsErrors=false` and `EnforceCodeStyleInBuild=false` from `src/Stilus/Directory.Build.props`, and the "LEGACY DEBT" comment with them. Done when: the file sets only `MinVerTagPrefix`, `Product`, and `IsotoneApp`.
- [ ] Fix every IDE diagnostic the now-enforced code style reports (run `dotnet format Isotone.slnx --verify-no-changes` first to see them, then `dotnet format` on the Stilus projects and review the diff). Done when: the Release build is clean.
- [ ] Remove the Stilus block from "Legacy debt" in `docs/dev/build.md`. Done when: the section names no Stilus relaxation.
- [ ] Commit: `"build(stilus): warnings are errors and code style is enforced"`

**Test checkpoint:** `dotnet build Isotone.slnx -c Release` exits 0 with 0 warnings; `dotnet format Isotone.slnx --verify-no-changes` exits 0; adding an unused `using System.Text;` to any Stilus file makes the Release build fail. Cheaper substitute that fails: moving the relaxations to `WarningsNotAsErrors`, which the props-file check catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 with every Stilus test class reporting
- [ ] `grep -rni "bezier" src/Stilus tests/Isotone.Stilus.Tests scripts installer` shows only curve-math identifiers
- [ ] A packaged Stilus installs as `Stilus.exe` and logs to `%LOCALAPPDATA%\Rizonesoft\Stilus\logs\`
- [ ] `python scripts/todo-graph.py validate` clean
