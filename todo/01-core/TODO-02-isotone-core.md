---
schema_version: 1
id: isotone-core
domain: 01-core
status: draft
title: "TODO-02 -- Isotone.Core: Shared Services"
depends_on: []
frozen: true
track: C2
---

# TODO-02 -- Isotone.Core: Shared Services

> **Goal:** The non-UI behavior every app needs exists once, in `Isotone.Core`, the day a second app needs it: app-data paths and the Serilog bootstrap, the settings store, single instance with file-open forwarding, the undo history, and the atomic document writer. Each move leaves no copy behind and no shared type with a single consumer.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** There is no `src/Isotone.Core/`. Gesso configures Serilog in `src/Gesso/src/Gesso.UI/App.xaml.cs` through `Host.CreateDefaultBuilder().UseSerilog(...)`, writing to `%LOCALAPPDATA%\Gesso\logs\gesso-.log`; Stilus references `Serilog` and `Serilog.Sinks.File` but no `.cs` file in `src/Stilus/` mentions Serilog, and it logs through its own `DebugLogger` singleton. Gesso's `SettingsService` writes `%LOCALAPPDATA%\Gesso\settings.json`; Stilus has no settings store, and its `FileOperationsService` and `AssetLibraryService` build their own `%LOCALAPPDATA%\Bezier\...` paths. Gesso has `Services/SingleInstanceManager.cs`; Stilus has none. Undo exists twice: Stilus `Bezier.Core/Services/HistoryManager.cs` with `IEditorCommand`, Gesso `Gesso.Core/History/CommandHistory.cs` with its own `ICommand`. Stilus saves with `SvgExporter.ExportToFile` straight onto the target path.
<!-- claim: absent src/Isotone.Core -->
<!-- claim: count "UseSerilog" src/Gesso/src/Gesso.UI/App.xaml.cs = 1 -->
<!-- claim: count "Serilog" src/Stilus/Bezier.Core/Services/DebugLogger.cs = 0 -->
<!-- claim: exists src/Gesso/src/Gesso.UI/Services/SettingsService.cs -->
<!-- claim: exists src/Gesso/src/Gesso.UI/Services/SingleInstanceManager.cs -->
<!-- claim: exists src/Stilus/Bezier.Core/Services/HistoryManager.cs -->
<!-- claim: exists src/Gesso/src/Gesso.Core/History/CommandHistory.cs -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- the logging location, settings, and atomic-save rules this file implements
- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- the list of what moves to `Isotone.Core` and when
- -> XREF: D02 T04 §1 -- the Stilus atomic save §5 moves here when Gesso's save needs it
- -> XREF: D03 T04 §2 -- the Gesso save that is §5's second consumer
- -> XREF: D05 T01 §4 -- the update check that lands in `Isotone.Core` as a release concern
- -> XREF: D02 T01 §2 -- the Stilus composition root that consumes §1's logging bootstrap
- -> XREF: D02 T03 §1 -- the Stilus resize and rotate undo that completes the command set §4 merges
- -> XREF: D03 T03 §2 -- the Gesso edits that are §4's second consumer
- -> XREF: D01 T03 §1 -- the pixel engine, built in `Isotone.Core/Imaging/` on §1's project and §2's settings
- -> XREF: D01 T04 §1 -- the color-management engine, built in `Isotone.Core/Color/` on §1's project with its defaults in §2's store
- -> XREF: D01 T05 §1 -- the AI core, logging through §1, keeping model choices in §2, and recording applies into §4's history
- -> XREF: D02 T07 §13 -- the History panel that reads §4's suite history
- -> XREF: D02 T08 §1 -- the drawing tools whose defaults go through §2's settings store
- -> XREF: D02 T09 §1 -- the color model whose `stilus.*` keys write through §2 and whose commands record into §4
- -> XREF: D02 T10 §1 -- the type sections whose `Stilus.Type.*` keys go through §2 and whose text commands record into §4
- -> XREF: D02 T11 §1 -- the effect framework whose settings go through §2 and whose commands record into §4
- -> XREF: D02 T12 §1 -- Edit Bitmap in Gesso, which relies on §3's single-instance forwarding
- -> XREF: D02 T13 §1 -- the print, proof, and PDF settings kept in §2 and the commands recorded in §4
- -> XREF: D02 T14 §1 -- the format options persisted in §2 and the import and slice edits recorded in §4
- -> XREF: D02 T15 §11 -- the suite hand-off inbox that receives files through §3's single-instance forwarding
- -> XREF: D02 T16 §5 -- the preferences that write through §2 and set §4's undo limit
- -> XREF: D01 T06 §1 -- the pixel engine extensions cites §2: the settings store that holds the `Isotone.Imaging.ProcessingSpace` key
- -> XREF: D01 T07 §1 -- the suite develop engine cites §1: the Isotone.Core project and the app-data paths the presets folder uses; §2: the settings store for profile favorites, raw defaults, and the presets folder
- -> XREF: D03 T08 §6 -- Gesso parity document and view cites §4: the suite history D03 T08 §6 builds its tree over; §5: atomic writes for templates, logs, and exports
- -> XREF: D03 T09 §1 -- Gesso parity layers cites §4: the suite history every command there records into; §5: the atomic writer the frozen `.gesso` save path goes through
- -> XREF: D03 T17 §1 -- Gesso parity formats cites §3: single-instance file-open forwarding D03 T17 §1 routes through; §5: the atomic writer every writer there saves through
- -> XREF: D03 T20 §1 -- Gesso parity workspace cites §2: the settings store every preference writes through
- -> XREF: D04 T04 §1 -- the Albumen Viewer cites §3: single instance and file-open forwarding for D04 T04 §1, D04 T04 §17, and the hand-off to Albumen; §5: the atomic writer D04 T04 §6's Save As and D04 T04 §13's tile export write through
- -> XREF: D04 T05 §1 -- Albumen browse without importing cites §4: the suite history every browse action records its undo step in; §5: the atomic writer for sidecars, vault files, and archives
- -> XREF: D04 T08 §1 -- Albumen parity metadata cites §5: the atomic writer every sidecar write goes through
- -> XREF: D04 T11 §10 -- the Albumen batch tools cites §3: single-instance forwarding the Explorer verb and the viewer's `B` key use in D04 T11 §10; §4: the suite history that records batch develop and orientation as undo steps; §5: the atomic writer every output and every in-place replace uses
- -> XREF: D04 T13 §1 -- Albumen parity formats cites §4: the suite history the extension fix records its undo step in; §5: the atomic writer every writer here saves through
- -> XREF: D04 T14 §6 -- Albumen parity workspace cites §2: the settings store D04 T14 §6 extends with portable and deployment modes
- -> XREF: D01 T10 §1 -- suite automation cites §4: UndoHistory transactions for playback and script runs; §3: single-instance forwarding of command-line switches
- -> XREF: D01 T11 §1 -- the media layer logs, stores Isotone.Media.* settings, and encodes through AtomicFileWriter here
- -> XREF: D01 T12 §1 -- the on-device model runtime stores its backend, device, and models-folder settings here

## Outcome

- `src/Isotone.Core/Isotone.Core.csproj` (`net11.0`, no WPF) exists, is in `Isotone.slnx`, and is referenced by both editors.
- Both apps log through one bootstrap to `%LOCALAPPDATA%\Rizonesoft\<App>\logs\`, with the rolling and retention the standard names.
- Both apps read and write settings through one atomic JSON store under `%LOCALAPPDATA%\Rizonesoft\<App>\settings.json`.
- A second launch of either app with a file path hands the path to the running instance and exits.
- One undo history type serves both editors.
- Every document save in the suite goes through one atomic writer, and killing a save mid-write leaves the original byte-identical.

**Adjacency:** list=not-applicable (services with no browsable records); document=not-applicable (no printed output); settings=applicable @ D01 T02 §2; reporting=not-applicable (no summaries of its own); notifications=not-applicable (apps own their status strips); permissions=applicable @ D01 T02 §5; audit=applicable @ D01 T02 §1; exchange=not-applicable (no foreign formats); reverse=applicable @ D01 T02 §4

**Adjacency rationale:** The settings store is the settings adjacency for every app; the atomic writer is where a read-only or locked target is refused; the logging bootstrap is the audit trail's foundation; the history is every app's undo.

## Implementation Order

| Order | Section | Deliverable                                                  | Depends On               | Status |
| :---: | :-----: | ------------------------------------------------------------ | ------------------------ | :----: |
|   1   |   §1    | Create Isotone.Core with app-data paths and logging           | D02 T01 §1, D03 T01 §1   |  [ ]   |
|   2   |   §2    | The settings store                                           | §1                       |  [ ]   |
|   3   |   §3    | Single instance and file-open forwarding                     | §1                       |  [ ]   |
|   4   |   §4    | One undo history for the suite                               | D02 T03 §1, D03 T01 §1   |  [ ]   |
|   5   |   §5    | The atomic document writer moves to Isotone.Core              | D02 T04 §1               |  [ ]   |

---

## 1. Create Isotone.Core with App-Data Paths and Logging

Both editors need logging and an app-data folder, and they do it differently today: Gesso through the Generic Host and Serilog, Stilus through a private `DebugLogger` with no file at all. This is the first shared need, so it creates the library. The location changes from `%LOCALAPPDATA%\Gesso` to `%LOCALAPPDATA%\Rizonesoft\Gesso` as `standards/shared.md` decides; nothing has shipped, so there is nothing to migrate.

- [ ] Create `src/Isotone.Core/Isotone.Core.csproj` (`net11.0`; **Corrected 2026-09-26:** said `net10.0`, `Nullable` enable, root namespace `Isotone.Core`) and add it to `Isotone.slnx` under `/Shared/`. Done when: `dotnet build Isotone.slnx -c Release` builds it.
- [ ] Add `src/Isotone.Core/AppData/AppDataPaths.cs`: given an app name, returns `%LOCALAPPDATA%\Rizonesoft\<App>` and its `logs`, `settings.json`, and `recovery` locations, creating folders on first use, with an override root for tests. Done when: `AppDataPathsTests` pass with a temporary root.
- [ ] Add `src/Isotone.Core/Logging/IsotoneLogging.cs` with `UseIsotoneLogging(this IHostBuilder, string appName)`: Serilog to `<logs>\<app>-.log`, daily rolling, 7 files, 10 MB per file, the `Debug` output in Debug builds, minimum level from configuration. Done when: `IsotoneLoggingTests` asserts a written event lands in the file under a temporary root.
- [ ] Gesso's `App.xaml.cs` replaces its inline `UseSerilog` block with `UseIsotoneLogging("Gesso")`, and its `appsettings.json` `Logging.FilePath` entry is removed. Done when: a Gesso run writes `%LOCALAPPDATA%\Rizonesoft\Gesso\logs\gesso-<date>.log`.
- [ ] Stilus references `Isotone.Core` and calls `UseIsotoneLogging("Stilus")` from its startup (the Generic Host itself arrives in `D02 T01 §2`; until then a minimal `Host.CreateDefaultBuilder` in `App.OnStartup` is enough). Done when: a Stilus run writes `%LOCALAPPDATA%\Rizonesoft\Stilus\logs\stilus-<date>.log` with a startup line.
- [ ] Add `tests/Isotone.Core.Tests` for the tests above. Done when: `dotnet test Isotone.slnx` runs them.
- [ ] Commit: `"core: create Isotone.Core with app-data paths and one logging bootstrap"`

**Requires:** display-session -- proving both apps write their log on startup needs launching them

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `AppDataPathsTests` and `IsotoneLoggingTests` reporting; launching each app once produces its dated log file under `%LOCALAPPDATA%\Rizonesoft\<App>\logs\` containing an Information startup line (quote it) and 0 `[ERR]` lines; `grep -rn "UseSerilog(" src/Gesso` prints nothing. Cheaper substitute that fails: copying Gesso's Serilog block into Stilus, which is the second copy the rule forbids.

## 2. The Settings Store

Gesso has a settings service; Stilus has none but needs one now (recent files, autosave interval, export defaults). The store writes JSON atomically so a crash mid-write never leaves an unreadable settings file, and every change is logged.

- [ ] Add `src/Isotone.Core/Settings/JsonSettingsStore.cs` implementing `ISettingsStore` (`Get<T>(key, default)`, `Set<T>(key, value)`, `Save()`, change event), backed by System.Text.Json with a source-generated context, writing through a temp file plus `File.Replace`. Done when: `JsonSettingsStoreTests` cover round trip, missing file (defaults), corrupt file (defaults plus a Warning log and the bad file kept as `settings.json.bad`), and a read-only target (refusal logged, in-memory value kept).
- [ ] Log one Information line per changed key (`Setting {Key} changed from {Old} to {New}`). Done when: a test with a Serilog test logger asserts the line.
- [ ] Gesso's `SettingsService` becomes a thin typed wrapper over `ISettingsStore` (or is replaced by it), and its path moves to `AppDataPaths`. Done when: Gesso reads and writes `%LOCALAPPDATA%\Rizonesoft\Gesso\settings.json`.
- [ ] Stilus registers `ISettingsStore` for `%LOCALAPPDATA%\Rizonesoft\Stilus\settings.json`; its first consumer is the recent-files list (`D02 T04 §5`), so this section adds a `StilusSettings` typed wrapper with the keys that section will use and a unit test proving defaults. Done when: the wrapper test passes.
- [ ] Add the suite scope: `AppDataPaths.Suite` (`%LOCALAPPDATA%\Rizonesoft\Isotone`) and a second store, `ISuiteSettingsStore`, over `Isotone\settings.json`, each key declaring app or suite scope, with changes from another process raising the change event through a debounced `FileSystemWatcher`; suite keys (`ai.*`, `brand.kitsFolder`, `color.default*`, `Isotone.Gpu.*`, `Isotone.AI.Local.*`) read through it, and the key-naming rule (one casing, one prefix scheme) is recorded in `standards/shared.md` in the same commit (**Groomed 2026-09-28:** suite-wide keys were planned against a per-app store). Done when: `SuiteSettingsStoreTests` set a key from a store built for Stilus and read it from one built for Gesso, and two concurrent writers leave valid JSON.
- [ ] Commit: `"core: one atomic settings store for the suite"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `JsonSettingsStoreTests` reporting all four file states; killing a test process between the temp write and the replace (a test hook that throws there) leaves the previous `settings.json` byte-identical. Cheaper substitute that fails: `File.WriteAllText` straight onto `settings.json`, which the interrupted-write test catches.

## 3. Single Instance and File-Open Forwarding

The installers register file associations (Stilus `.svg`; Gesso `.png`, `.jpg`, `.psd`). Double-clicking a second file must open it in the running window, not start a second instance. Gesso has `SingleInstanceManager`; Stilus needs the same thing for its association (`D02 T04 §6`), so it moves here.

- [ ] Move `SingleInstanceManager` to `src/Isotone.Core/Instance/SingleInstance.cs` (named mutex plus a named pipe per user and app), with a `FilesReceived` event and a timeout on the client side. Done when: Gesso's copy is deleted and Gesso uses the shared type.
- [ ] Add `SingleInstanceTests`: a second "instance" in the same test process (distinct pipe name) forwards two paths and exits true; a stale mutex with no server does not hang past the timeout. Done when: both pass.
- [ ] Log the forward (`Forwarded {Count} file(s) to the running instance`) on the client and the receipt on the server. Done when: the test logger sees both.
- [ ] Commit: `"core: share single-instance and file-open forwarding"`

**Requires:** display-session -- launching Gesso twice to prove forwarding needs an interactive desktop
**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `SingleInstanceTests` reporting; launching Gesso twice with a path on the second launch leaves one process and a log line naming the forwarded path. Cheaper substitute that fails: a mutex alone, which blocks the second launch but drops the file it was asked to open.

## 4. One Undo History for the Suite

Both editors need undo, and each grew its own: Stilus's `HistoryManager` over `IEditorCommand` (with move, resize, rotate, scale, group, reorder, add, delete, and property commands) and Gesso's `CommandHistory` over its own `ICommand` with persistence and snapshots. A second copy of a behavior in a second app is a defect, so the day Gesso wires its history into a document (`D03 T03 §2`), both move onto one type here. Stilus's resize and rotate undo (`D02 T03 §1`) lands first so the merged type is proven against a complete command set.

- [ ] Compare the two APIs (execute, undo, redo, merge of consecutive edits, transaction or macro grouping, limits, change events, descriptions) and write the comparison as the first paragraph of `src/Isotone.Core/History/README.md`. Done when: the table names which app's behavior each member keeps and why.
- [ ] Add `src/Isotone.Core/History/IUndoableCommand.cs`, `UndoHistory.cs` (bounded stack, `BeginTransaction`/`Commit`/`Rollback`, merge window for drags and slider edits, `Changed` event, description for menu text), with tests for every member. Done when: `UndoHistoryTests` pass, including transaction rollback restoring state and the limit dropping the oldest entry.
- [ ] Port Stilus's commands to `IUndoableCommand` and delete `HistoryManager` and `IEditorCommand`. Done when: every existing Stilus history test passes against `UndoHistory`.
- [ ] Port Gesso's `CommandBase` to `IUndoableCommand`, keep Gesso's persistence and snapshot features in Gesso (`Isotone.Gesso.Core/History/`) as extensions over the shared history (only Gesso needs them), and delete `CommandHistory`. Done when: Gesso's history tests pass against `UndoHistory`.
- [ ] Commit: `"core: one undo history for Stilus and Gesso"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `UndoHistoryTests` and both apps' history tests reporting; `grep -rn "class HistoryManager\|class CommandHistory" src` prints nothing; in Stilus, drawing a rectangle, resizing it, and pressing Ctrl+Z twice removes it (log lines for each step quoted). Cheaper substitute that fails: an adapter that wraps one app's history for the other, which leaves two implementations.

## 5. The Atomic Document Writer Moves to Isotone.Core

Stilus's save path writes through an atomic writer built in Stilus (`D02 T04 §1`), because only Stilus saved documents then. Gesso's first save (`D03 T04 §2`) is the second consumer, so the writer moves here in the commit before that section, and both saves go through it.

**Freeze check:** Save-over writes to a temp file in the target directory, flushes to disk, and replaces the target with `File.Replace` (or a rename when the target does not exist); killing the process after the temp write and before the replace leaves the original byte-identical, and a read-only or locked target is refused with the document still open and dirty. Fixture source: `tests/fixtures/save-over/` (a small SVG and PNG, created by this section). The move must not change what Stilus writes: a Stilus save of `tests/fixtures/stilus/svg/bezier-sample.svg` before and after this commit produces identical bytes.

- [ ] Move `AtomicFileWriter` from Stilus to `src/Isotone.Core/IO/AtomicFileWriter.cs` unchanged apart from its namespace, with its tests to `tests/Isotone.Core.Tests`. Done when: Stilus's copy is deleted and Stilus's save calls the shared type.
- [ ] Add the `tests/fixtures/save-over/` fixtures and a `SaveOverTests` class: interrupted write (a test hook throws between write and replace) leaves the original identical; read-only target refuses; locked target (opened with `FileShare.None`) refuses; target on a missing folder refuses. Done when: all four pass.
- [ ] Prove the Stilus bytes are unchanged: save the sample through Stilus's exporter before and after the move and compare hashes in a test. Done when: the test asserts equal SHA-256.
- [ ] Commit: `"core: move the atomic document writer to Isotone.Core for Gesso's save"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `SaveOverTests` reporting all four cases and the byte-identity test passing; `grep -rn "class AtomicFileWriter" src` prints exactly one path, under `src/Isotone.Core/`. Cheaper substitute that fails: Gesso copying the Stilus writer, which the grep catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 with every `Isotone.Core.Tests` class reporting
- [ ] Every `Isotone.Core` type has at least two app consumers (`grep` per public type across `src/Stilus`, `src/Gesso`, `src/Albumen`, quoted)
- [ ] The save-over fixtures pass their freeze check
- [ ] `python scripts/todo-graph.py validate` clean
