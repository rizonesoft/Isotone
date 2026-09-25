---
schema_version: 1
id: nodus-structure
domain: 02-nodus
status: draft
title: "TODO-01 -- Nodus Layout, Names, and Composition Root"
depends_on: []
track: N1
---

# TODO-01 -- Nodus Layout, Names, and Composition Root

> **Goal:** The imported Bezier code is Nodus in every name a user or developer meets: `Photon.Nodus.*` projects and namespaces in the target layout, an executable called `Nodus.exe`, one composition root on the Generic Host with every service registered, logging through the suite's Serilog bootstrap, and a build with warnings as errors and code style enforced, like the rest of the suite.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Nodus is three projects under `src/Nodus/`: `Bezier.Core` (`net10.0`), `Bezier.Desktop` (`net10.0-windows`, WPF, no `AssemblyName`, so the executable is `Bezier.Desktop.exe`), and `Bezier.Tests`. 147 `.cs` files declare a `Bezier` namespace, 11 XAML files use `x:Class="Bezier..."` or `clr-namespace:Bezier`, and 17 string literals say "Bezier" (window title `Bezier`, `"Bezier - Untitled"`, `%LOCALAPPDATA%\Bezier` folders). `scripts/apps.psd1`, `installer/Nodus.iss`, and `installer/Suite.iss` name `Bezier.Desktop.exe`. The composition root is `ServiceCollectionExtensions.AddBezierServices`, which registers only `MainWindowViewModel`; the `HistoryManager` and `ToolManager` registrations are commented out, and `MainWindowViewModel` constructs `SvgImporter`, `SvgExporter`, `HistoryManager`, and `ToolManager` itself with `new`. `App.Services` is a static service locator. Logging goes through a custom `DebugLogger` singleton that feeds the debug window and writes no file. `src/Nodus/Directory.Build.props` sets `TreatWarningsAsErrors=false` and `EnforceCodeStyleInBuild=false`; the Release build reports 334 distinct warnings (CA1305 151, CS0618 44, CA2263 40, CA1805 20, NU1701 15, CA1859 14, CA1861 10, CA1310 9, CA1806 8, CA2008 5, others 18, per `docs/dev/build.md`).
<!-- claim: exists src/Nodus/Bezier.Desktop/Bezier.Desktop.csproj -->
<!-- claim: count "^namespace Bezier" src/Nodus/**/*.cs = 147 -->
<!-- claim: count "Exe       = 'Bezier.Desktop.exe'" scripts/apps.psd1 = 1 -->
<!-- claim: count "#define AppExeName \"Bezier.Desktop.exe\"" installer/Nodus.iss = 1 -->
<!-- claim: count "#define NodusExe \"Bezier.Desktop.exe\"" installer/Suite.iss = 1 -->
<!-- claim: count "// services.AddSingleton" src/Nodus/Bezier.Desktop/ServiceCollectionExtensions.cs = 2 -->
<!-- claim: count "private readonly (SvgImporter|SvgExporter|HistoryManager|ToolManager) _\w+ = new\(\);" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 4 -->
<!-- claim: count "<TreatWarningsAsErrors>false</TreatWarningsAsErrors>" src/Nodus/Directory.Build.props = 1 -->

## Inputs

- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- the target layout and names
- [`docs/dev/build.md`](../../docs/dev/build.md) -- the warning table §4 and §5 clear, and the SkiaSharp hold §6 lifts
- [`standards/shared.md`](../../standards/shared.md), [`standards/nodus.md`](../../standards/nodus.md) -- composition, logging, and culture rules
- [`scripts/apps.psd1`](../../scripts/apps.psd1), [`installer/Nodus.iss`](../../installer/Nodus.iss), [`Photon.slnx`](../../Photon.slnx) -- the files that name the executable and the projects
- -> XREF: D00 T02 §6 -- the xUnit v3 migration that waits for §1 to move the test project
- -> XREF: D01 T02 §1 -- the logging bootstrap §2 and §3 consume

## Outcome

- `src/Nodus/Photon.Nodus.Core/`, `src/Nodus/Photon.Nodus.Desktop/`, and `tests/Photon.Nodus.Tests/` build, with `Photon.Nodus.*` namespaces throughout and no `Bezier` identifier left in code, XAML, scripts, or installers.
- The published app is `Nodus.exe` with the Nodus icon, and the installer and portable ZIP carry it.
- `App.xaml.cs` builds a Generic Host; every service a view model or tool uses is registered and constructor-injected; no `new` of a service inside a view model and no static locator.
- The debug window's console reads the Serilog pipeline, and every Nodus log line reaches `%LOCALAPPDATA%\Rizonesoft\Nodus\logs\`.
- The Release build of Nodus has zero warnings, with `TreatWarningsAsErrors` and `EnforceCodeStyleInBuild` on, on SkiaSharp 4.

**Adjacency:** list=not-applicable (no user records here); document=not-applicable (no printed output); settings=not-applicable (settings arrive with the Photon.Core store in D01 T02 §2); reporting=not-applicable (no summaries); notifications=not-applicable (no long operations); permissions=not-applicable (nothing new is written); audit=applicable; exchange=not-applicable (formats are TODO-04's); reverse=not-applicable (no user edits introduced)

**Adjacency rationale:** This file is structure and hygiene. Its one user-relevant outcome is that Nodus actions reach a real log file (§3), which is the audit trail's foundation.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On         | Status |
| :---: | :-----: | ---------------------------------------------------- | ------------------ | :----: |
|   1   |   §1    | Rename Bezier to Photon.Nodus                        | D00 T02 §1         |  [ ]   |
|   2   |   §2    | Composition root on the Generic Host                 | §1, D01 T02 §1     |  [ ]   |
|   3   |   §3    | The debug console reads the Serilog pipeline         | §2                 |  [ ]   |
|   4   |   §4    | Culture-safe formatting and comparisons              | §1                 |  [ ]   |
|   5   |   §5    | The rest of the analyzer backlog                     | §4                 |  [ ]   |
|   6   |   §6    | SkiaSharp 4                                          | §5, D02 T02 §2     |  [ ]   |
|   7   |   §7    | Warnings are errors in Nodus                         | §6                 |  [ ]   |

---

## 1. Rename Bezier to Photon.Nodus

Every later Nodus section names files; doing the rename first means each of them is written once against the final paths. It is a mechanical change with a wide blast radius, so it changes names only: no behavior, no formatting, no refactor rides along. Git sees renames when content stays mostly the same, which keeps `git log --follow` working through the history imported from Bezier.

- [ ] `git mv src/Nodus/Bezier.Core src/Nodus/Photon.Nodus.Core` and rename the project file to `Photon.Nodus.Core.csproj`. Done when: the folder and file exist under the new names.
- [ ] `git mv src/Nodus/Bezier.Desktop src/Nodus/Photon.Nodus.Desktop`, rename the project file, and set `<AssemblyName>Nodus</AssemblyName>` and `<RootNamespace>Photon.Nodus.Desktop</RootNamespace>`. Done when: the Debug build produces `artifacts/bin/Photon.Nodus.Desktop/debug/Nodus.exe`.
- [ ] `git mv src/Nodus/Bezier.Tests tests/Photon.Nodus.Tests`, rename its project file, and fix its `ProjectReference` paths. Done when: `dotnet test Photon.slnx` discovers the same number of tests as before the rename.
- [ ] Rewrite `namespace Bezier` to `namespace Photon.Nodus` and every `using Bezier` to `using Photon.Nodus` in all `.cs` files, and `x:Class`/`clr-namespace` values in all XAML. Done when: `grep -rn "Bezier" src/Nodus tests/Photon.Nodus.Tests --include=*.cs --include=*.xaml` prints only string literals handled by the next item.
- [ ] Replace user-visible and path strings: the window title and `"Bezier - ..."` titles become `Nodus`, `AddBezierServices` becomes `AddNodusServices`, and `%LOCALAPPDATA%\Bezier` paths in `FileOperationsService` and `AssetLibraryService` become `%LOCALAPPDATA%\Rizonesoft\Nodus` (the `Photon.Core` paths arrive in `D01 T02 §1`). Done when: `grep -rni "bezier" src/Nodus tests/Photon.Nodus.Tests --include=*.cs --include=*.xaml` prints nothing except the curve type (`BezierSegment`, cubic Bezier math), each remaining hit quoted in the commit body.
- [ ] Replace `Resources/Icons/Bezier.ico`, `Bezier.svg`, and `Bezier_32.png` with the Nodus icon from `resources/icons/nodus/` (`nodus.ico`, `nodus.svg`, `PNG/nodus_32.png`) and point `ApplicationIcon` and the `Resource` items at them. Done when: `Nodus.exe` shows the Nodus icon in Explorer.
- [ ] Update `Photon.slnx`, `scripts/apps.psd1` (`Project` and `Exe = 'Nodus.exe'`), `installer/Nodus.iss` (`AppExeName`), `installer/Suite.iss` (`NodusExe`), and the Nodus lines of `docs/dev/build.md`, `standards/nodus.md` (drop the "today `Bezier.*`" notes), and `AGENTS.md`. Done when: `grep -rn "Bezier.Desktop\|Bezier.Core\|Bezier.Tests" --include=*.slnx --include=*.psd1 --include=*.iss --include=*.md . | grep -v "^./docs/legacy/"` prints nothing.
- [ ] Rewrite every `src/Nodus/Bezier.*` and `Bezier.Tests` path in `todo/` claims and prose to the new paths, and re-run `python scripts/todo-claims.py`. Done when: it exits 0.
- [ ] Commit: `"nodus: rename Bezier to Photon.Nodus and ship Nodus.exe"`

**Requires:** display-session -- confirming the Nodus icon in Explorer and the installed app starting needs an interactive desktop
**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0; `dotnet test Photon.slnx` exits 0 with the same test count as before the rename; `pwsh scripts/package.ps1 -App Nodus` produces a Setup exe whose silent install creates `Nodus.exe` (quote `Get-ChildItem "$env:LOCALAPPDATA\Programs\Nodus\Nodus.exe"`); `git log --follow --oneline src/Nodus/Photon.Nodus.Core/Models/VectorDocument.cs | wc -l` is greater than 1, proving history survived. Cheaper substitute that fails: setting `AssemblyName` only, which leaves every namespace and path saying Bezier.

## 2. Composition Root on the Generic Host

`standards/shared.md` requires one composition root per app with constructor injection and no static locator. Today the root registers one type, and the main view model builds its own services, so nothing can be replaced in a test and the per-document lifetime the standard asks for cannot exist. This section wires what exists; it does not add features.

- [ ] Replace `App.OnStartup`'s `ServiceCollection` with `Host.CreateApplicationBuilder` (or `Host.CreateDefaultBuilder`) in `src/Nodus/Photon.Nodus.Desktop/App.xaml.cs`, calling `UsePhotonLogging("Nodus")` from `Photon.Core`, starting the host before the main window and stopping it on exit. Done when: startup and shutdown each log one Information line.
- [ ] `AddNodusServices` registers `SvgImporter`, `SvgExporter` (transient), `ToolManager` and every tool (singleton), `HistoryManager` (singleton until per-document scopes land with tabs), `DebugInfoService`, `PerformanceMetricsService`, and `IconCatalog`/`IconService`. Done when: the commented-out lines are gone and a `ServiceRegistrationTests` test resolves every registered type from a built provider.
- [ ] `MainWindowViewModel` receives its services through its constructor instead of `new`. Done when: the file has no `= new SvgImporter()`, `new SvgExporter()`, `new HistoryManager()`, or `new ToolManager()`.
- [ ] Remove the static `App.Services` property and every use of it; the main window is resolved from the host. Done when: `grep -rn "App.Services" src/Nodus` prints nothing.
- [ ] Commit: `"nodus: one composition root on the Generic Host"`

**Requires:** display-session -- the launch smoke proving the host starts the main window needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `ServiceRegistrationTests` reporting; launching `Nodus.exe` shows the main window and writes `Host started` and, on File, Exit, `Host stopped` to `%LOCALAPPDATA%\Rizonesoft\Nodus\logs\`; the captures in `docs/captures/nodus/main-window/` still match. Cheaper substitute that fails: uncommenting the two registrations and leaving the `new` calls, which the grep catches.

## 3. The Debug Console Reads the Serilog Pipeline

`DebugLogger` is a second logging system: it keeps an in-memory list for the debug window and writes nothing to disk, so a user's crash leaves no trace. The debug window is worth keeping; its private logger is not. It becomes a Serilog sink.

- [ ] Add `src/Nodus/Photon.Nodus.Desktop/Diagnostics/InMemoryLogSink.cs` (a bounded ring buffer of `LogEvent`s implementing `ILogEventSink`, raising an event on the dispatcher) and register it in the logger configuration. Done when: `InMemoryLogSinkTests` prove the bound and the ordering.
- [ ] `DebugWindow` reads from `InMemoryLogSink` instead of `DebugLogger`; its export writes the buffered events as text. Done when: the debug window shows the same entries the log file receives for a session.
- [ ] Replace every `DebugLogger.Instance.Log/Error/Warn` call with an injected `ILogger<T>` (or `Serilog.ILogger` where a type has no DI) using structured templates. Done when: `grep -rn "DebugLogger" src/Nodus` prints nothing and `DebugLogger.cs` is deleted.
- [ ] Every user action that changes the document or a setting already routed through a command logs one Information line naming the action (`Executed {Command} on {Count} element(s)` in `HistoryManager`). Done when: a test with a Serilog test logger asserts the line for `AddElementCommand`.
- [ ] Commit: `"nodus: route the debug console through Serilog and retire DebugLogger"`

**Requires:** display-session -- showing the debug window's live console needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `InMemoryLogSinkTests` reporting; a driven run (draw a rectangle, undo, open the debug window with F12) shows the add and undo lines in both the debug console and the day's log file (quote both); `grep -rn "class DebugLogger" src` prints nothing. Cheaper substitute that fails: making `DebugLogger` also write a file, which keeps two logging systems.

## 4. Culture-Safe Formatting and Comparisons

CA1305 (151 sites), CA1304, and CA1310 (9) are the largest warning group and a real defect class for a document editor: an SVG written on a machine whose culture uses a decimal comma is invalid. Each site is decided, not blanket-fixed: text written to a file, a log property, or compared as an identifier uses the invariant culture; text shown to the user uses the current culture.

- [ ] Fix every CA1305 site in `Photon.Nodus.Core` with `CultureInfo.InvariantCulture` (the SVG reader and writer, path data, numbers in ids). Done when: the Core project reports 0 CA1305.
- [ ] Fix every CA1305 site in `Photon.Nodus.Desktop`, using `CultureInfo.CurrentCulture` for status-bar and panel text and invariant for anything persisted. Done when: the Desktop project reports 0 CA1305.
- [ ] Fix every CA1304 and CA1310 site with an explicit culture or `StringComparison.Ordinal`/`OrdinalIgnoreCase`. Done when: 0 of each.
- [ ] Add `SvgExporterCultureTests`: with `CultureInfo.CurrentCulture` set to `de-DE`, export a document with fractional coordinates and assert the SVG uses `.` decimals and reparses to equal coordinates. Done when: the test passes and fails if one `ToString()` loses its culture argument.
- [ ] Commit: `"nodus: format and compare with an explicit culture everywhere"`

**Test checkpoint:** `dotnet build Photon.slnx -c Release -v q 2>&1 | grep -cE "CA1305|CA1304|CA1310"` prints 0; `dotnet test Photon.slnx` exits 0 with `SvgExporterCultureTests` reporting. Cheaper substitute that fails: setting `CultureInfo.DefaultThreadCurrentCulture` to invariant at startup, which silences the analyzer's intent and shows users invariant numbers.

## 5. The Rest of the Analyzer Backlog

With culture done, about 120 warnings remain outside the SkiaSharp obsolescence group (CS0618, which §6 clears by migrating) and NU1701 (which leaves with SkiaSharp.Views.WPF 3.x). Each rule is fixed as its analyzer documentation says, not suppressed.

- [ ] Fix CA2263 (40, prefer generic overloads) and CA1805 (20, explicit default initialization). Done when: 0 of each.
- [ ] Fix CA1859 (14), CA1861 (10), CA1806 (8, a result that is ignored is either used or discarded with `_ =` and a comment saying why it is safe), and CA2008 (5, pass `TaskScheduler.Default`). Done when: 0 of each.
- [ ] Fix the remaining 18 (CA1720, CA1868, CA1869, CS9191, CS0219, CA1001, CS8602, CS0675, CA1852, CS8625), treating each nullable warning (CS8602, CS8625) as a possible bug and adding a test where it was one. Done when: the Release build reports only CS0618 and NU1701 for Nodus.
- [ ] Commit: `"nodus: clear the analyzer backlog apart from the SkiaSharp migration"`

**Test checkpoint:** `dotnet build Photon.slnx -c Release -v q 2>&1 | grep -E "warning (CA|CS|IDE)" | grep -v "CS0618" | grep -c "src/Nodus"` prints 0; `dotnet test Photon.slnx` exits 0 with the same count as before the section. Cheaper substitute that fails: `<NoWarn>` entries in the Nodus props, which the grep does not see but review does.

## 6. SkiaSharp 4

SkiaSharp 4 removes the `SKPaint` text APIs Nodus uses (`TextSize`, `Typeface`, `MeasureText`, `DrawText(string, ...)`), which is why 44 CS0618 warnings exist and why the package is held at 3.119.4. Migrating clears them, drops the .NET Framework OpenTK packages SkiaSharp.Views.WPF 3.x pulls in (NU1701), and unblocks current fixes. It runs after the SVG decision (`D02 T02 §2`), which removes Svg.Skia, the other package pinned to SkiaSharp 3.

- [ ] Move `SkiaSharp` and `SkiaSharp.Views.WPF` to the current 4.x in `Directory.Packages.props`. Done when: `dotnet restore Photon.slnx` exits 0 and no NU1701 is reported for Nodus.
- [ ] Rewrite text drawing and measuring in `SkiaRenderer.cs`, `SkiaToolRenderContext.cs`, and the text tool on `SKFont` (`SKFont.Size`, `SKFont.Typeface`, `SKFont.MeasureText`, `SKCanvas.DrawText(string, x, y, SKTextAlign, SKFont, SKPaint)`). Done when: 0 CS0618 in Nodus. Source: the SkiaSharp 4 migration notes in the SkiaSharp repository's release notes.
- [ ] Imago's `Imago.Rendering` builds on the same version (it references SkiaSharp through global usings); fix anything the upgrade breaks there. Done when: the whole solution builds.
- [ ] Add `SkiaRendererTextTests`: render a text element at a fixed size to an `SKBitmap` and compare its ink bounds with the 3.x rendering captured before the upgrade (committed as `tests/fixtures/nodus/render/text-3x.png`) within 1 pixel. Done when: the test passes.
- [ ] Remove the SkiaSharp rows from the held-back table in `docs/dev/build.md`, and remove `NU1701` from `src/Imago/Directory.Build.props` if Imago no longer reports it. Done when: both files are current.
- [ ] Commit: `"nodus: migrate to SkiaSharp 4 and the SKFont text API"`

**Requires:** display-session -- the canvas launch smoke after a renderer upgrade needs an interactive desktop

**Test checkpoint:** `dotnet build Photon.slnx -c Release -v q 2>&1 | grep -cE "CS0618|NU1701"` prints 0; `dotnet test Photon.slnx` exits 0 with `SkiaRendererTextTests` reporting; opening `tests/fixtures/nodus/svg/bezier-sample.svg` in Nodus renders the same as `docs/captures/nodus/main-window/sample-100.png` (new capture `sample-skia4-100.png` committed beside it). Cheaper substitute that fails: `#pragma warning disable CS0618` around the old calls, which leaves the package held.

## 7. Warnings Are Errors in Nodus

The Nodus overlay is the last place in the suite where a warning does not fail the build. With the backlog at zero, the two relaxations are removed and the overlay holds only the app's identity, like Imago's.

- [ ] Remove `TreatWarningsAsErrors=false` and `EnforceCodeStyleInBuild=false` from `src/Nodus/Directory.Build.props`, and the "LEGACY DEBT" comment with them. Done when: the file sets only `MinVerTagPrefix`, `Product`, and `PhotonApp`.
- [ ] Fix every IDE diagnostic the now-enforced code style reports (run `dotnet format Photon.slnx --verify-no-changes` first to see them, then `dotnet format` on the Nodus projects and review the diff). Done when: the Release build is clean.
- [ ] Remove the Nodus block from "Legacy debt" in `docs/dev/build.md`. Done when: the section names no Nodus relaxation.
- [ ] Commit: `"build(nodus): warnings are errors and code style is enforced"`

**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0 with 0 warnings; `dotnet format Photon.slnx --verify-no-changes` exits 0; adding an unused `using System.Text;` to any Nodus file makes the Release build fail. Cheaper substitute that fails: moving the relaxations to `WarningsNotAsErrors`, which the props-file check catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every Nodus test class reporting
- [ ] `grep -rni "bezier" src/Nodus tests/Photon.Nodus.Tests scripts installer` shows only curve-math identifiers
- [ ] A packaged Nodus installs as `Nodus.exe` and logs to `%LOCALAPPDATA%\Rizonesoft\Nodus\logs\`
- [ ] `python scripts/todo-graph.py validate` clean
