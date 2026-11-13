---
schema_version: 1
id: foundation-crash-diagnostics
domain: 01-core
status: draft
title: "TODO-26 -- Foundation: Crash Diagnostics by an Out-of-Process Watcher"
depends_on: []
frozen: false
track: F13
---

# TODO-26 -- Foundation: Crash Diagnostics by an Out-of-Process Watcher

> **Goal:** every crash, including the fail-fast kinds no in-process handler sees, leaves an encrypted minidump the user can choose to send, collected by the app's own watcher attached as its debugger, for a standard user in every install mode, with nothing installed or registered beyond the user's own settings, no duplicate report to Windows Error Reporting, and the app unharmed when the watcher ends.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No crash diagnostics exist. Secondary copies of document data, which a dump is, are encrypted by `D01 T19 §3`.
<!-- claim: absent native/core/src/crash -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Crash diagnostics" -- the watcher (`DebugActiveProcess` with `DebugSetProcessKillOnExit(FALSE)`), the debug events acted on, `MiniDumpWriteDump` encrypted through its I/O callbacks, the dump folder and its five-dump limit, the attach breakpoint continued, the developer switch, the Help menu send, the Windows Error Reporting exclusion, symbol archiving, and the proofs
- -> XREF: D01 T19 §3 -- the encryption every dump is written through
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D00 T07 §5 -- the native release pipeline re-plan, which archives the PDBs by build id and re-runs §4 against each app's own installers

## Outcome

- At start each app launches itself in watcher mode, which attaches as the app's debugger and, on a last-chance or fail-fast exception, writes an encrypted minidump of the suspended app, keeping the newest five.
- The user can send a dump from the Help menu, seeing what is sent and decrypting it only for that send; Windows Error Reporting is excluded for the app; every build embeds its version and build id, and each release's PDBs are archived by that id.
- An access violation, a `__fastfail`, a `/GS` overrun, and a stack overflow each write a dump that opens with the symbols at the faulting frame, in each install mode, as a standard user.

**Adjacency:** list=applicable @ D01 T26 §2; document=not-applicable (no printed output); settings=applicable @ D01 T26 §1; reporting=applicable @ D01 T26 §2; notifications=applicable @ D01 T26 §2; permissions=applicable @ D01 T26 §1; audit=applicable @ D01 T26 §1; exchange=applicable @ D01 T26 §2; reverse=applicable @ D01 T26 §2

**Adjacency rationale:** The dumps are listed for the user to send or delete (§2), with what each contains shown before a send; the developer switch that starts without the watcher is a setting (§1); after a crash the next start tells the user a report is available (§2); the watcher runs as the standard user and refuses nothing it needs elevation for (§1); each dump written and each send is logged (§1, §2); a send exports a decrypted copy (§2); and a dump is deleted by the user or rotated out (§2).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The watcher and encrypted minidumps | D00 T07 §3, D01 T19 §3 |  [ ]   |
|   2   |   §2    | Sending a report, the WER exclusion, and symbols | §1, D01 T15 §3 |  [ ]   |
|   3   |   §3    | Packaging the host for the three install modes | §1 |  [ ]   |
|   4   |   §4    | The crash proofs in every install mode | §2, §3 |  [ ]   |

---

## 1. The Watcher and Encrypted Minidumps

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service and a process mode.
**Needs:** Windows host (build/test)

The watcher runs with the user's own permissions and needs no elevation; each dump written is recorded in the audit log.

- [ ] Add `isotone::core::CrashWatcher` in `native/core/src/crash/`: the app relaunches its own executable with `--watcher <pid>`, which calls `DebugActiveProcess` and `DebugSetProcessKillOnExit(FALSE)`, continues the attach breakpoint with `DBG_CONTINUE`, passes every other first-chance exception back with `DBG_EXCEPTION_NOT_HANDLED`, and on a last-chance or fail-fast exception writes a minidump of the suspended app with the event's exception record and thread context. Done when: `CrashWatcher.PassesFirstChanceExceptions` and `CrashWatcher.DumpsOnLastChance` pass with a test child.
- [ ] Write the dump through `MiniDumpWriteDump`'s I/O callbacks into `SecondaryStore`, so no plaintext dump touches the disk, in the app's folder in the user's app data (the portable folder in portable mode), keeping the newest five and logging each. Done when: `CrashWatcher.NoPlaintextDumpOnDisk` and `CrashWatcher.KeepsNewestFive` pass.
- [ ] Add the developer switch `--no-watcher` (also a setting with readback) that starts the app without the watcher, since a process can have only one debugger. Done when: `CrashWatcher.DeveloperSwitchSkipsWatcher` passes.
- [ ] Commit: `"core: the crash watcher writes encrypted minidumps"`

**Test checkpoint:** Unit test: `CrashWatcher.PassesFirstChanceExceptions`, `CrashWatcher.DumpsOnLastChance`, `CrashWatcher.NoPlaintextDumpOnDisk`, `CrashWatcher.KeepsNewestFive`, and `CrashWatcher.DeveloperSwitchSkipsWatcher` pass through CTest on x64 and ARM64, each test child's whole process tree stopped on timeout. Cheaper substitute that fails: an in-process unhandled-exception filter, which never sees a `__fastfail` and can deadlock inside the crashing process.

## 2. Sending a Report, the WER Exclusion, and Symbols

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the report flow, with a placeholder Help menu item and list in the host; the product dialog is each app's.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Crash diagnostics" (the proofs crash a live app in each install mode)

After a crash, the next start shows a notification that a report is available, which the user can send, delete, or dismiss.

- [ ] List the dumps in a Help menu item, show what a dump contains before sending, decrypt it only into the send, let the user delete one, and tell the user at the next start that a report is available. Done when: the host scenario `crash-report` lists, describes, exports, and deletes a dump.
- [ ] Exclude the app from Windows Error Reporting for the current user (`WerAddExcludedApplication`) at first run, and embed the version and build id in every executable (`isotone::core::BuildInfo`) with its PDB kept beside it under `artifacts/native/`, matched by the CodeView record; archiving each release's PDBs by build id, never shipping them, belongs to the native publish step `D00 T07 §5` re-plans. Done when: `CrashWatcher.ExcludedFromWer` and `CrashWatcher.DumpNamesBuildId` pass.
- [ ] Commit: `"core: crash reports the user controls"`

**Test checkpoint:** Unit test and driven run with evidence: `CrashWatcher.ExcludedFromWer` and `CrashWatcher.DumpNamesBuildId` pass through CTest; `foundation-host --scenario crash-report --report build/foundation/crash-report.json` exits 0 listing, describing, exporting, and deleting a dump (quoted). Cheaper substitute that fails: relying on Windows Error Reporting, whose dumps leave the machine without the user's choice and whose local dumps need registry settings outside the user's own.

## 3. Packaging the Host for the Three Install Modes

The crash proofs must run in each install mode the spec names: the per-user installer default, a per-machine install, and the portable ZIP. The native apps' installers come with the release pipeline `D00 T07 §5` re-plans, so this section packages the foundation host itself, with the suite's own installer definitions (`installer/common.iss`, already per-user by default with `PrivilegesRequired=lowest`) on the pinned Inno Setup 7, so the proofs of §4 run against real installs. The host's installer and ZIP are test artifacts under `artifacts/`, never published.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a test installer and its script.
**Needs:** Windows host (build/test)

- [ ] Add `installer/FoundationHost.iss`, which defines the host's identity and includes `installer/common.iss`, and `scripts/package-foundation-host.ps1 -Preset <preset>` that stages the host's build output and builds `artifacts/foundation-host/FoundationHost-Setup.exe` with Inno Setup 7 (found by `Find-Iscc` in `scripts/_common.ps1`) and `artifacts/foundation-host/FoundationHost-portable.zip` holding the build and the `portable` marker. Done when: both artifacts are built from a fresh `x64-release` build, and a second run reproduces the ZIP's file list.
- [ ] Add `-Install PerUser|PerMachine|Portable` and `-Uninstall <mode>` to the script: `PerUser` runs the installer silently in its default per-user mode (`/VERYSILENT /CURRENTUSER`), `PerMachine` with `/VERYSILENT /ALLUSERS` from an elevated session, `Portable` extracts the ZIP to a scratch folder, and `-Uninstall` removes each through the installer's uninstaller (the ZIP's folder by deletion), checking that nothing is left in the install folder, the Start menu, or the uninstall registry. Done when: `python scripts/tests/test_package_foundation_host.py` installs and uninstalls the per-user and portable modes on the reference machine and checks the per-machine mode refuses without elevation, naming it.
- [ ] Install Inno Setup 7 in the `native` job of `.github/workflows/build.yml` the way `scripts/dev-env.ps1` repairs it (the official installer with its SHA-256 recorded in `docs/dev/build.md`), build both artifacts, and install and uninstall all three modes, the uninstall in an `always()` step; the runner's session is elevated, so the per-machine install needs no prompt. Done when: the job lists the steps and the candidate's run passes them.
- [ ] Commit: `"tests: package the foundation host for the three install modes"`

**Test checkpoint:** Unit test and driven run with evidence: `python scripts/tests/test_package_foundation_host.py` passes on the reference machine (the per-user installer and the portable ZIP installed and removed with nothing left, the per-machine install refused without elevation); the candidate's `build` run installs and uninstalls all three modes green (run URL quoted). Cheaper substitute that fails: copying the build into the install folders, which never runs the installer that decides the folder, the registry entries, and the access a standard user has.

## 4. The Crash Proofs in Every Install Mode

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- driven crash proofs of the host.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Crash diagnostics" (the proofs crash a live app in each install mode)

- [ ] Add `CrashProof.EachKindWritesAnOpenableDump`: with the host installed by §3 (the per-user installer, the per-machine installer, and the portable ZIP extracted), and run under an un-elevated token (`runas /trustlevel:0x20000`, so as a standard user even from an administrator's session), crash it by an access violation, a `__fastfail`, a `/GS` stack-buffer overrun, and a stack overflow; check that each writes one dump in the user's data folder (the portable folder in portable mode), that the app's export decrypts it, that it opens with the build's symbols at the faulting frame (`cdb -z <dump> -c "k; q"`), that no report is queued in Windows Error Reporting, that a healthy session writes no dump, and that killing the watcher leaves the app running. Done when: it passes in each mode, recorded per mode: per-user and portable on the reference machine, and all three in the `native` CI job.
- [ ] Commit: `"core: the crash proofs in every install mode"`

**Test checkpoint:** Driven run with evidence: `CrashProof.EachKindWritesAnOpenableDump` passes under an un-elevated token in the per-user install and the portable ZIP on the reference machine and in all three installs in the candidate's `build` run (run URL quoted), each crash kind's faulting frame from `cdb` quoted, no Windows Error Reporting queue entry, no dump from a healthy session, and the app still running after the watcher is killed. Cheaper substitute that fails: crashing the host from an elevated test runner, which hides a dump folder the standard user cannot write.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `CrashWatcher.*` cases reporting through CTest
- [ ] `python scripts/tests/test_package_foundation_host.py` passes
- [ ] `CrashProof.EachKindWritesAnOpenableDump` passes in all three install modes on x64 and ARM64
- [ ] `python scripts/todo-graph.py validate` clean
