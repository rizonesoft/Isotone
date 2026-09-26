---
schema_version: 1
id: photon-core
domain: 01-core
status: draft
title: "TODO-02 -- Photon.Core: Shared Services"
depends_on: []
frozen: true
track: C2
---

# TODO-02 -- Photon.Core: Shared Services

> **Goal:** The non-UI behavior every app needs exists once, in `Photon.Core`, the day a second app needs it: app-data paths and the Serilog bootstrap, the settings store, single instance with file-open forwarding, the undo history, and the atomic document writer. Each move leaves no copy behind and no shared type with a single consumer.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** There is no `src/Photon.Core/`. Imago configures Serilog in `src/Imago/src/Imago.UI/App.xaml.cs` through `Host.CreateDefaultBuilder().UseSerilog(...)`, writing to `%LOCALAPPDATA%\Imago\logs\imago-.log`; Nodus references `Serilog` and `Serilog.Sinks.File` but no `.cs` file in `src/Nodus/` mentions Serilog, and it logs through its own `DebugLogger` singleton. Imago's `SettingsService` writes `%LOCALAPPDATA%\Imago\settings.json`; Nodus has no settings store, and its `FileOperationsService` and `AssetLibraryService` build their own `%LOCALAPPDATA%\Bezier\...` paths. Imago has `Services/SingleInstanceManager.cs`; Nodus has none. Undo exists twice: Nodus `Bezier.Core/Services/HistoryManager.cs` with `IEditorCommand`, Imago `Imago.Core/History/CommandHistory.cs` with its own `ICommand`. Nodus saves with `SvgExporter.ExportToFile` straight onto the target path.
<!-- claim: absent src/Photon.Core -->
<!-- claim: count "UseSerilog" src/Imago/src/Imago.UI/App.xaml.cs = 1 -->
<!-- claim: count "Serilog" src/Nodus/Bezier.Core/Services/DebugLogger.cs = 0 -->
<!-- claim: exists src/Imago/src/Imago.UI/Services/SettingsService.cs -->
<!-- claim: exists src/Imago/src/Imago.UI/Services/SingleInstanceManager.cs -->
<!-- claim: exists src/Nodus/Bezier.Core/Services/HistoryManager.cs -->
<!-- claim: exists src/Imago/src/Imago.Core/History/CommandHistory.cs -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- the logging location, settings, and atomic-save rules this file implements
- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- the list of what moves to `Photon.Core` and when
- -> XREF: D02 T04 §1 -- the Nodus atomic save §5 moves here when Imago's save needs it
- -> XREF: D03 T04 §2 -- the Imago save that is §5's second consumer
- -> XREF: D05 T01 §4 -- the update check that lands in `Photon.Core` as a release concern
- -> XREF: D02 T01 §2 -- the Nodus composition root that consumes §1's logging bootstrap
- -> XREF: D02 T03 §1 -- the Nodus resize and rotate undo that completes the command set §4 merges
- -> XREF: D03 T03 §2 -- the Imago edits that are §4's second consumer

## Outcome

- `src/Photon.Core/Photon.Core.csproj` (`net11.0`, no WPF) exists, is in `Photon.slnx`, and is referenced by both editors.
- Both apps log through one bootstrap to `%LOCALAPPDATA%\Rizonesoft\<App>\logs\`, with the rolling and retention the standard names.
- Both apps read and write settings through one atomic JSON store under `%LOCALAPPDATA%\Rizonesoft\<App>\settings.json`.
- A second launch of either app with a file path hands the path to the running instance and exits.
- One undo history type serves both editors.
- Every document save in the suite goes through one atomic writer, and killing a save mid-write leaves the original byte-identical.

**Adjacency:** list=not-applicable (services with no browsable records); document=not-applicable (no printed output); settings=applicable @ D01 T02 §2; reporting=not-applicable (no summaries of its own); notifications=not-applicable (apps own their status strips); permissions=applicable; audit=applicable; exchange=not-applicable (no foreign formats); reverse=applicable @ D01 T02 §4

**Adjacency rationale:** The settings store is the settings adjacency for every app; the atomic writer is where a read-only or locked target is refused; the logging bootstrap is the audit trail's foundation; the history is every app's undo.

## Implementation Order

| Order | Section | Deliverable                                                  | Depends On               | Status |
| :---: | :-----: | ------------------------------------------------------------ | ------------------------ | :----: |
|   1   |   §1    | Create Photon.Core with app-data paths and logging           | D02 T01 §1, D03 T01 §1   |  [ ]   |
|   2   |   §2    | The settings store                                           | §1                       |  [ ]   |
|   3   |   §3    | Single instance and file-open forwarding                     | §1                       |  [ ]   |
|   4   |   §4    | One undo history for the suite                               | D02 T03 §1, D03 T01 §1   |  [ ]   |
|   5   |   §5    | The atomic document writer moves to Photon.Core              | D02 T04 §1               |  [ ]   |

---

## 1. Create Photon.Core with App-Data Paths and Logging

Both editors need logging and an app-data folder, and they do it differently today: Imago through the Generic Host and Serilog, Nodus through a private `DebugLogger` with no file at all. This is the first shared need, so it creates the library. The location changes from `%LOCALAPPDATA%\Imago` to `%LOCALAPPDATA%\Rizonesoft\Imago` as `standards/shared.md` decides; nothing has shipped, so there is nothing to migrate.

- [ ] Create `src/Photon.Core/Photon.Core.csproj` (`net11.0`; **Corrected 2026-09-26:** said `net10.0`, `Nullable` enable, root namespace `Photon.Core`) and add it to `Photon.slnx` under `/Shared/`. Done when: `dotnet build Photon.slnx -c Release` builds it.
- [ ] Add `src/Photon.Core/AppData/AppDataPaths.cs`: given an app name, returns `%LOCALAPPDATA%\Rizonesoft\<App>` and its `logs`, `settings.json`, and `recovery` locations, creating folders on first use, with an override root for tests. Done when: `AppDataPathsTests` pass with a temporary root.
- [ ] Add `src/Photon.Core/Logging/PhotonLogging.cs` with `UsePhotonLogging(this IHostBuilder, string appName)`: Serilog to `<logs>\<app>-.log`, daily rolling, 7 files, 10 MB per file, the `Debug` output in Debug builds, minimum level from configuration. Done when: `PhotonLoggingTests` asserts a written event lands in the file under a temporary root.
- [ ] Imago's `App.xaml.cs` replaces its inline `UseSerilog` block with `UsePhotonLogging("Imago")`, and its `appsettings.json` `Logging.FilePath` entry is removed. Done when: an Imago run writes `%LOCALAPPDATA%\Rizonesoft\Imago\logs\imago-<date>.log`.
- [ ] Nodus references `Photon.Core` and calls `UsePhotonLogging("Nodus")` from its startup (the Generic Host itself arrives in `D02 T01 §2`; until then a minimal `Host.CreateDefaultBuilder` in `App.OnStartup` is enough). Done when: a Nodus run writes `%LOCALAPPDATA%\Rizonesoft\Nodus\logs\nodus-<date>.log` with a startup line.
- [ ] Add `tests/Photon.Core.Tests` for the tests above. Done when: `dotnet test Photon.slnx` runs them.
- [ ] Commit: `"core: create Photon.Core with app-data paths and one logging bootstrap"`

**Requires:** display-session -- proving both apps write their log on startup needs launching them

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `AppDataPathsTests` and `PhotonLoggingTests` reporting; launching each app once produces its dated log file under `%LOCALAPPDATA%\Rizonesoft\<App>\logs\` containing an Information startup line (quote it) and 0 `[ERR]` lines; `grep -rn "UseSerilog(" src/Imago` prints nothing. Cheaper substitute that fails: copying Imago's Serilog block into Nodus, which is the second copy the rule forbids.

## 2. The Settings Store

Imago has a settings service; Nodus has none but needs one now (recent files, autosave interval, export defaults). The store writes JSON atomically so a crash mid-write never leaves an unreadable settings file, and every change is logged.

- [ ] Add `src/Photon.Core/Settings/JsonSettingsStore.cs` implementing `ISettingsStore` (`Get<T>(key, default)`, `Set<T>(key, value)`, `Save()`, change event), backed by System.Text.Json with a source-generated context, writing through a temp file plus `File.Replace`. Done when: `JsonSettingsStoreTests` cover round trip, missing file (defaults), corrupt file (defaults plus a Warning log and the bad file kept as `settings.json.bad`), and a read-only target (refusal logged, in-memory value kept).
- [ ] Log one Information line per changed key (`Setting {Key} changed from {Old} to {New}`). Done when: a test with a Serilog test logger asserts the line.
- [ ] Imago's `SettingsService` becomes a thin typed wrapper over `ISettingsStore` (or is replaced by it), and its path moves to `AppDataPaths`. Done when: Imago reads and writes `%LOCALAPPDATA%\Rizonesoft\Imago\settings.json`.
- [ ] Nodus registers `ISettingsStore` for `%LOCALAPPDATA%\Rizonesoft\Nodus\settings.json`; its first consumer is the recent-files list (`D02 T04 §5`), so this section adds a `NodusSettings` typed wrapper with the keys that section will use and a unit test proving defaults. Done when: the wrapper test passes.
- [ ] Commit: `"core: one atomic settings store for the suite"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `JsonSettingsStoreTests` reporting all four file states; killing a test process between the temp write and the replace (a test hook that throws there) leaves the previous `settings.json` byte-identical. Cheaper substitute that fails: `File.WriteAllText` straight onto `settings.json`, which the interrupted-write test catches.

## 3. Single Instance and File-Open Forwarding

The installers register file associations (Nodus `.svg`; Imago `.png`, `.jpg`, `.psd`). Double-clicking a second file must open it in the running window, not start a second instance. Imago has `SingleInstanceManager`; Nodus needs the same thing for its association (`D02 T04 §6`), so it moves here.

- [ ] Move `SingleInstanceManager` to `src/Photon.Core/Instance/SingleInstance.cs` (named mutex plus a named pipe per user and app), with a `FilesReceived` event and a timeout on the client side. Done when: Imago's copy is deleted and Imago uses the shared type.
- [ ] Add `SingleInstanceTests`: a second "instance" in the same test process (distinct pipe name) forwards two paths and exits true; a stale mutex with no server does not hang past the timeout. Done when: both pass.
- [ ] Log the forward (`Forwarded {Count} file(s) to the running instance`) on the client and the receipt on the server. Done when: the test logger sees both.
- [ ] Commit: `"core: share single-instance and file-open forwarding"`

**Requires:** display-session -- launching Imago twice to prove forwarding needs an interactive desktop
**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `SingleInstanceTests` reporting; launching Imago twice with a path on the second launch leaves one process and a log line naming the forwarded path. Cheaper substitute that fails: a mutex alone, which blocks the second launch but drops the file it was asked to open.

## 4. One Undo History for the Suite

Both editors need undo, and each grew its own: Nodus's `HistoryManager` over `IEditorCommand` (with move, resize, rotate, scale, group, reorder, add, delete, and property commands) and Imago's `CommandHistory` over its own `ICommand` with persistence and snapshots. A second copy of a behavior in a second app is a defect, so the day Imago wires its history into a document (`D03 T03 §2`), both move onto one type here. Nodus's resize and rotate undo (`D02 T03 §1`) lands first so the merged type is proven against a complete command set.

- [ ] Compare the two APIs (execute, undo, redo, merge of consecutive edits, transaction or macro grouping, limits, change events, descriptions) and write the comparison as the first paragraph of `src/Photon.Core/History/README.md`. Done when: the table names which app's behavior each member keeps and why.
- [ ] Add `src/Photon.Core/History/IUndoableCommand.cs`, `UndoHistory.cs` (bounded stack, `BeginTransaction`/`Commit`/`Rollback`, merge window for drags and slider edits, `Changed` event, description for menu text), with tests for every member. Done when: `UndoHistoryTests` pass, including transaction rollback restoring state and the limit dropping the oldest entry.
- [ ] Port Nodus's commands to `IUndoableCommand` and delete `HistoryManager` and `IEditorCommand`. Done when: every existing Nodus history test passes against `UndoHistory`.
- [ ] Port Imago's `CommandBase` to `IUndoableCommand`, keep Imago's persistence and snapshot features in Imago (`Photon.Imago.Core/History/`) as extensions over the shared history (only Imago needs them), and delete `CommandHistory`. Done when: Imago's history tests pass against `UndoHistory`.
- [ ] Commit: `"core: one undo history for Nodus and Imago"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `UndoHistoryTests` and both apps' history tests reporting; `grep -rn "class HistoryManager\|class CommandHistory" src` prints nothing; in Nodus, drawing a rectangle, resizing it, and pressing Ctrl+Z twice removes it (log lines for each step quoted). Cheaper substitute that fails: an adapter that wraps one app's history for the other, which leaves two implementations.

## 5. The Atomic Document Writer Moves to Photon.Core

Nodus's save path writes through an atomic writer built in Nodus (`D02 T04 §1`), because only Nodus saved documents then. Imago's first save (`D03 T04 §2`) is the second consumer, so the writer moves here in the commit before that section, and both saves go through it.

**Freeze check:** Save-over writes to a temp file in the target directory, flushes to disk, and replaces the target with `File.Replace` (or a rename when the target does not exist); killing the process after the temp write and before the replace leaves the original byte-identical, and a read-only or locked target is refused with the document still open and dirty. Fixture source: `tests/fixtures/save-over/` (a small SVG and PNG, created by this section). The move must not change what Nodus writes: a Nodus save of `tests/fixtures/nodus/svg/bezier-sample.svg` before and after this commit produces identical bytes.

- [ ] Move `AtomicFileWriter` from Nodus to `src/Photon.Core/IO/AtomicFileWriter.cs` unchanged apart from its namespace, with its tests to `tests/Photon.Core.Tests`. Done when: Nodus's copy is deleted and Nodus's save calls the shared type.
- [ ] Add the `tests/fixtures/save-over/` fixtures and a `SaveOverTests` class: interrupted write (a test hook throws between write and replace) leaves the original identical; read-only target refuses; locked target (opened with `FileShare.None`) refuses; target on a missing folder refuses. Done when: all four pass.
- [ ] Prove the Nodus bytes are unchanged: save the sample through Nodus's exporter before and after the move and compare hashes in a test. Done when: the test asserts equal SHA-256.
- [ ] Commit: `"core: move the atomic document writer to Photon.Core for Imago's save"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `SaveOverTests` reporting all four cases and the byte-identity test passing; `grep -rn "class AtomicFileWriter" src` prints exactly one path, under `src/Photon.Core/`. Cheaper substitute that fails: Imago copying the Nodus writer, which the grep catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every `Photon.Core.Tests` class reporting
- [ ] Every `Photon.Core` type has at least two app consumers (`grep` per public type across `src/Nodus`, `src/Imago`, `src/Lumen`, quoted)
- [ ] The save-over fixtures pass their freeze check
- [ ] `python scripts/todo-graph.py validate` clean
