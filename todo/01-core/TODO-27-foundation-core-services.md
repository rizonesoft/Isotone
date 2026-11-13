---
schema_version: 1
id: foundation-core-services
domain: 01-core
status: draft
title: "TODO-27 -- Foundation: App-Data Paths, Structured Logging, Atomic Writes, and the Settings Store"
depends_on: []
frozen: false
track: F14
---

# TODO-27 -- Foundation: App-Data Paths, Structured Logging, Atomic Writes, and the Settings Store

> **Goal:** the core services every other foundation writes through exist before them: each app resolves its app-data folder (and the portable folder in portable mode), writes structured log events with one configuration per app and one line per action that changes a document or a setting, writes every persistent data file atomically with readback, and keeps its settings as versioned JSON in one store, so the foundations log, persist, and read back through one implementation instead of each growing its own.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** `native/core/` holds the build information, the premultiply kernels, and, from §1, the error type, the app-data folders, and the structured log; it has no atomic file writing and no settings store, which §2 adds. (**Corrected 2026-11-13** at §1's build: said `native/core/` had no app-data paths and no logging.) The C#-era plan for these services is `todo/01-core/TODO-02-isotone-core.md` `§1` and `§2` (parked, re-planned by `D00 T07 §4` in Phase 2); the round review of `D00 T07 §3` found the Phase 1 foundations depending on them before that re-plan, so this file brings the mechanisms forward and `D00 T07 §4` re-plans `D01 T02` onto it without a second copy.
<!-- claim: exists native/core/include/isotone/core/build_info.h -->
<!-- claim: exists native/core/include/isotone/core/log.h -->
<!-- claim: absent native/core/include/isotone/core/atomic_file.h -->
<!-- claim: absent native/core/include/isotone/core/settings.h -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "`isotone::core`" -- app-data paths, settings stored as JSON with atomic writes and readback, structured logging with one line per action that changes a document or a setting, and atomic file I/O
- [`standards/cpp.md`](../../standards/cpp.md), "Calling Windows" and "Errors" -- every Win32 call checked, every failure a result
- [`standards/shared.md`](../../standards/shared.md), "Logging" and "Commands and state" -- the log's location, roll, retention, size limit, debugger output, message templates, and levels, and process-wide services passed down from the composition root
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T02 §1 -- the C#-era paths and logging section, re-planned by `D00 T07 §4` onto this file rather than a second copy
- -> XREF: D01 T15 §1 -- the foundation test host logs and keeps its settings through this file
- -> XREF: D01 T19 §1 -- document saves keep their own seven-invariant sequence; this file's atomic write serves settings and other app data, never a user's document

## Outcome

- `isotone::core::AppFolders` resolves each app's data root and its `logs`, `settings`, and `recovery` folders under `%LOCALAPPDATA%\Rizonesoft\<App>\` (beside the executable in portable mode), creating them on first use.
- `isotone::core::Log` writes structured events (a message template with named values) as JSON lines to daily files of at most 10 MB, keeping the newest 7, with one configuration per app, a bounded in-memory buffer later sections can read, and the debugger output in a Debug build.
- `isotone::core::AtomicFile` writes a data file by temporary file, flush, verified readback, and replace with the previous version kept until the new one reads back; `isotone::core::Settings` keeps versioned JSON settings through it, logging one line per change.

**Adjacency:** list=not-applicable (no records a user browses); document=not-applicable (no printed output); settings=applicable @ D01 T27 §2; reporting=not-applicable (no data to summarize); notifications=not-applicable (no long-running work); permissions=not-applicable (writes only the app's own data folders); audit=applicable @ D01 T27 §1; exchange=not-applicable (no user files); reverse=not-applicable (a setting is reversed by setting it again)

**Adjacency rationale:** The settings store is this file's settings surface for every later section (§2); the structured log is the audit history every later section writes its one line per action into (§1).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | App-data paths and structured logging | D00 T07 §3 |  [ ]   |
|   2   |   §2    | Atomic file writes and the settings store | §1 |  [ ]   |

---

## 1. App-Data Paths and Structured Logging

> **Started:** 2026-11-13T05:44:35Z

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service.
**Needs:** Windows host (build/test)

Every later section writes its audit log line through this one logger, so the log format is fixed here once.

**Corrected 2026-11-13** (pre-build validation, each fact measured that day): (1) `SHGetKnownFolderPath` is exported by `shell32.dll` and its string is freed with `CoTaskMemFree` from `ole32.dll`, and `native/system-dlls.txt` allows only `KERNEL32.dll`, `SHLWAPI.dll`, and the API sets, so this section adds `SHELL32.dll` and `OLE32.dll` there with their reason, in its commit. (2) `native/core/` has no error type yet; `standards/cpp.md` (Errors) asks for one per module deriving from `std::exception` and naming the failing call and its code, so this section adds `isotone::core::Error` in `native/core/include/isotone/core/error.h`. (3) A logger that throws would turn a full disk or a removed folder into a crash in whatever action logged, so `Log::write` never throws: a failure to open or write the file is counted (`Log::failures()`) and the event still reaches the memory buffer, and a test proves that failure path. (4) The JSON line must be exact and the daily file must roll at UTC midnight, both untestable against the wall clock, so `LogConfig` takes a clock for tests. (5) **Default:** the portable marker is a file named `portable` beside the executable, and portable mode keeps `Logs`, `Settings`, and `Recovery` folders beside it; changing the name later means changing the portable ZIP the release pipeline builds.

**Added 2026-11-13** (plan review, D01-T27-S1-PR1 to PR4, and `standards/shared.md`, "Logging", which the section had not read): the log follows the shared standard: files at `%LOCALAPPDATA%\Rizonesoft\<App>\logs\<app>-<date>.log`, rolled daily, 7 files kept, 10 MB per file, a Debug build also writing to the debugger output; an event is a message template with named values; the levels are Verbose (off by default), Debug, Information, Warning, Error, and Fatal. The folders are lowercase (`logs`, `settings`, `recovery`) to match it. Process-wide services are created once in the composition root and passed down, with no mutable singleton (`standards/shared.md`, "Commands and state"), so the test override is an explicit root a test passes, not a process-wide switch. Writes go straight to the file with `WriteFile`, with no buffer of our own, so a failed write is seen on the call that made it.

- [x] Add `isotone::core::Error` in `native/core/include/isotone/core/error.h` (the failing call and its Win32 code), and `isotone::core::AppFolders` in `native/core/include/isotone/core/app_paths.h`: the data root, `logs`, `settings`, and `recovery` folders for an app name, resolved from an `AppFolderSources` (the local app data folder and the executable's folder), whose `from_windows()` reads `SHGetKnownFolderPath(FOLDERID_LocalAppData)` and `GetModuleFileNameW`; the root is `<local app data>\Rizonesoft\<App>\`, or the executable's folder when a `portable` marker file sits there; the folders are created on first use; a test passes its own sources, so no test writes the user's real folders; `SHELL32.dll` and `OLE32.dll` join `native/system-dlls.txt`. Only an absent marker means per-user mode: a marker that cannot be inspected is reported, never read as absent; copying an `Error` never throws. Done when: `AppPaths.ResolvesPerUserAndPortable`, `AppPaths.TestRootIsolates`, `AppPaths.FailureNamesTheCall`, and `AppPaths.UnreadableMarkerIsReported` pass, `Error` is checked nothrow-copyable at compile time, and `python scripts/native-artifact-gate.py --policy shipping --require-built` passes with the two DLLs registered. Done 2026-11-13: `native/core/include/isotone/core/error.h` with `src/error.cpp`, `app_paths.h` with `src/app_paths.cpp`, the private `src/utf.h` conversions, `SHELL32.dll` and `OLE32.dll` in `native/system-dlls.txt`, and `native/tests/core/app_paths_test.cpp` (4 cases, `UnreadableMarkerIsReported` added in round 1) pass in `x64-debug` and `x64-asan`; the artifact gate is read from the candidate's CI run, which builds every preset.
- [x] Add `isotone::core::Log` in `native/core/include/isotone/core/log.h`: an event is a level, a message template (`Saved {path} in {elapsed_ms} ms`), and named typed values; it is written as one JSON line (`time` in UTC with milliseconds, `level`, `template`, the rendered `message`, and the `fields` object) to `<logs>\<app>-<YYYY-MM-DD>.log`, appending when the file exists, starting a new part (`<app>-<YYYY-MM-DD>.1.log`, `.2.log`) before a line would take the file past 10 MB and a new file at UTC midnight, and deleting the oldest files beyond the newest 7; one `LogConfig` per app names the minimum level (Information by default, Debug in a Debug build) and the outputs (the file and the bounded ordered memory buffer by default, the debugger output added in a Debug build through `OutputDebugStringW`), and a test may pass its own clock and its own file writer; `write` is safe from any thread and never throws: a failed or partial file write is counted in `failures()`, the event still reaches the memory buffer and the debugger, the handle is reopened on the next write, and that write starts on a fresh line, so an incomplete record never runs into the next; an event whose line alone is larger than the limit is written as a stand-in record naming its size and how its template began, while the memory buffer keeps it whole. Done when: `Log.WritesOneJsonLinePerEvent`, `Log.MemoryBufferIsBoundedAndOrdered`, `Log.SafeFromManyThreads`, `Log.BelowLevelIsDropped`, `Log.ReopenAppends`, `Log.DateChangeStartsNewFile`, `Log.SizeLimitStartsNewPart`, `Log.KeepsNewestSevenFiles`, `Log.OnlyEnabledOutputsReceive`, `Log.UnwritableFolderKeepsMemoryAndCounts`, `Log.PartialWriteLeavesLaterRecordsReadable`, and `Log.OversizedEventIsReplaced` pass, the thread test under `x64-asan` too. Done 2026-11-13: `native/core/include/isotone/core/log.h` with `src/log.cpp` and `native/tests/core/log_test.cpp` (12 cases, `OversizedEventIsReplaced` added in round 1) pass in `x64-debug` and `x64-asan`; `pwsh scripts/native-tidy.ps1`: 16 translation units, 0 with diagnostics; `docs/dev/architecture.md` and `native/README.md` describe what `isotone::core` now holds.
- [ ] Commit: `"core: app-data paths and structured logging"`

**Test checkpoint:** Unit test: `AppPaths.ResolvesPerUserAndPortable`, `AppPaths.TestRootIsolates`, `AppPaths.FailureNamesTheCall`, `AppPaths.UnreadableMarkerIsReported`, `Log.WritesOneJsonLinePerEvent`, `Log.MemoryBufferIsBoundedAndOrdered`, `Log.SafeFromManyThreads`, `Log.BelowLevelIsDropped`, `Log.ReopenAppends`, `Log.DateChangeStartsNewFile`, `Log.SizeLimitStartsNewPart`, `Log.KeepsNewestSevenFiles`, `Log.OnlyEnabledOutputsReceive`, `Log.UnwritableFolderKeepsMemoryAndCounts`, `Log.PartialWriteLeavesLaterRecordsReadable`, and `Log.OversizedEventIsReplaced` pass through CTest on every preset, including `x64-asan` and `arm64-asan`; builds clean: `python scripts/native-artifact-gate.py --policy shipping --require-built` passes with `SHELL32.dll` and `OLE32.dll` registered. Cheaper substitute that fails: `OutputDebugString` or `printf` logging, which leaves no file a support report can read and no structure a test can assert.

## 2. Atomic File Writes and the Settings Store

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service.
**Needs:** Windows host (build/test)

Every later section's settings persist through this store, and a change writes one line to the audit log of §1.

- [ ] Add `isotone::core::AtomicFile` in `native/core/include/isotone/core/atomic_file.h`: write a data file to a fresh temporary file in the same folder, `FlushFileBuffers`, read the temporary file back and compare; then `ReplaceFileW` the target with it, keeping the previous version as a backup file beside it, read the target back and compare, and only then delete the backup; on any failure after the replace, restore the backup to the target's name and report the failure; a backup left by a crash is restored or removed at the next read, whichever holds the newer verified contents. Done when: `AtomicFile.ReplacesAndReadsBack`, `AtomicFile.FailureBeforeReplaceLeavesPrevious`, `AtomicFile.ReadbackFailureAfterReplaceRestoresPrevious`, and `AtomicFile.LeftoverBackupSettledAtNextRead` pass, each failure injected through a test seam.
- [ ] Add `isotone::core::Settings` in `native/core/include/isotone/core/settings.h`: one versioned JSON file per app in the settings folder, typed get and set by key with defaults, every set written through `AtomicFile` with readback and logged as one event naming the key and the new value, an unreadable or newer-version file kept aside and reported rather than overwritten. Done when: `Settings.SetPersistsAndReadsBack`, `Settings.ChangeWritesOneLogLine`, and `Settings.CorruptFileKeptAndReported` pass.
- [ ] Commit: `"core: atomic writes and the settings store"`

**Test checkpoint:** Unit test: `AtomicFile.ReplacesAndReadsBack`, `AtomicFile.FailureBeforeReplaceLeavesPrevious`, `AtomicFile.ReadbackFailureAfterReplaceRestoresPrevious`, `AtomicFile.LeftoverBackupSettledAtNextRead`, `Settings.SetPersistsAndReadsBack`, `Settings.ChangeWritesOneLogLine`, and `Settings.CorruptFileKeptAndReported` pass through CTest on every preset, including the AddressSanitizer lanes. Cheaper substitute that fails: writing the settings file in place, which a crash mid-write leaves truncated and unreadable.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `AppPaths.*`, `Log.*`, `AtomicFile.*`, and `Settings.*` cases reporting through CTest
- [ ] `python scripts/todo-graph.py validate` clean
