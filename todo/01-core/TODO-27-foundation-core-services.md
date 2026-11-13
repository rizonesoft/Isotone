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
> **Current state (verified 2026-11-13):** `native/core/` holds only the build information and the premultiply kernels; it has no app-data paths, no logging, no file writing, and no settings store. The C#-era plan for these services is `todo/01-core/TODO-02-isotone-core.md` `§1` and `§2` (parked, re-planned by `D00 T07 §4` in Phase 2); the round review of `D00 T07 §3` found the Phase 1 foundations depending on them before that re-plan, so this file brings the mechanisms forward and `D00 T07 §4` re-plans `D01 T02` onto it without a second copy.
<!-- claim: exists native/core/include/isotone/core/build_info.h -->
<!-- claim: absent native/core/include/isotone/core/log.h -->
<!-- claim: absent native/core/include/isotone/core/settings.h -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "`isotone::core`" -- app-data paths, settings stored as JSON with atomic writes and readback, structured logging with one line per action that changes a document or a setting, and atomic file I/O
- [`standards/cpp.md`](../../standards/cpp.md), "Calling Windows" and "Errors" -- every Win32 call checked, every failure a result
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T02 §1 -- the C#-era paths and logging section, re-planned by `D00 T07 §4` onto this file rather than a second copy
- -> XREF: D01 T15 §1 -- the foundation test host logs and keeps its settings through this file
- -> XREF: D01 T19 §1 -- document saves keep their own seven-invariant sequence; this file's atomic write serves settings and other app data, never a user's document

## Outcome

- `isotone::core::AppPaths` resolves each app's data, log, settings, and recovery folders under `%LOCALAPPDATA%\Rizonesoft\<App>\` (beside the executable in portable mode), creating them on first use.
- `isotone::core::Log` writes structured events (time, level, event name, fields) as JSON lines to a daily file, with one configuration per app and a bounded in-memory buffer later sections can read.
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

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service.
**Needs:** Windows host (build/test)

Every later section writes its audit log line through this one logger, so the log format is fixed here once.

- [ ] Add `isotone::core::AppPaths` in `native/core/include/isotone/core/app_paths.h`: the data, log, settings, and recovery folders for an app name, under `SHGetKnownFolderPath(FOLDERID_LocalAppData)` plus `Rizonesoft\<App>\`, or beside the executable when a `portable` marker file sits there, created on first use, with an override for tests so no test writes the user's real folders. Done when: `AppPaths.ResolvesPerUserAndPortable` and `AppPaths.TestOverrideIsolates` pass.
- [ ] Add `isotone::core::Log` in `native/core/include/isotone/core/log.h`: structured events (UTC time, level, event name, typed fields) written as one JSON line each to `<log folder>\<app>-<YYYY-MM-DD>.log`, one configuration per app (level and outputs), safe from any thread, plus a bounded ordered in-memory buffer that keeps the newest events for a console to read. Done when: `Log.WritesOneJsonLinePerEvent`, `Log.MemoryBufferIsBoundedAndOrdered`, and `Log.SafeFromManyThreads` pass, the last under `x64-asan` too.
- [ ] Commit: `"core: app-data paths and structured logging"`

**Test checkpoint:** Unit test: `AppPaths.ResolvesPerUserAndPortable`, `AppPaths.TestOverrideIsolates`, `Log.WritesOneJsonLinePerEvent`, `Log.MemoryBufferIsBoundedAndOrdered`, and `Log.SafeFromManyThreads` pass through CTest on every preset, including `x64-asan` and `arm64-asan`. Cheaper substitute that fails: `OutputDebugString` or `printf` logging, which leaves no file a support report can read and no structure a test can assert.

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
