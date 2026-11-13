---
schema_version: 1
id: foundation-document-safety
domain: 01-core
status: draft
title: "TODO-19 -- Foundation: Document Safety -- the Save Sequence, Secondary Copies, Checkpoints, and Recovery"
depends_on: []
frozen: false
track: F6
---

# TODO-19 -- Foundation: Document Safety -- the Save Sequence, Secondary Copies, Checkpoints, and Recovery

> **Goal:** a document survives anything short of the user deleting it: every save keeps the spec's seven invariants against a crash or power loss at any instruction and against the ordinary programs a file meets, carries the file's identity (owner, DACL, integrity label, encryption, attributes, times, streams) to the new version or refuses, never leaves document data in a weaker copy, and every open document is checkpointed so a crash loses at most the edits since the newest completed checkpoint, which the next start recovers.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** `isotone::core` has no file writing yet: `native/core/` holds only the build information and the premultiply kernels, and the settings store with its atomic write comes from `D01 T27 §2` (**Corrected 2026-11-13** in the round review of `D00 T07 §3`, D00-T07-S3-R1: said `isotone::core` already had an atomic file write for settings). Nothing implements a document save protocol, a journal, a file identity contract, encrypted secondary copies, checkpoints, retirement, or recovery. The spec owns the invariants and the proofs and sends the exact call sequence to this file to design and review.
<!-- claim: exists docs/specs/2026-10-22-native-stack-design.md -->
<!-- claim: absent native/core/include/isotone/core/save.h -->
<!-- claim: absent docs/dev/document-safety.md -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Document safety" -- the failure model, the seven invariants, the save sequence's starting requirements, the file identity contract, secondary copies, checkpoints and their cadence, retirement, recovery, and every listed proof
- [`docs/reviews/independent/2026-10-22-native-stack-spec.md`](../../docs/reviews/independent/2026-10-22-native-stack-spec.md), rounds 3 to 10 -- the requirements the save sequence's review starts from
- [`standards/cpp.md`](../../standards/cpp.md), "Calling Windows" and "Errors" -- every Win32 call checked, every failure a result
- -> XREF: D01 T18 §3 -- checkpoints run as background tasks with version checks
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T26 §1 -- crash dumps are secondary copies, encrypted as §3 sets out
- -> XREF: D01 T15 §1 -- the foundation test host whose `recovery` scenario §5 proves in
- -> XREF: D01 T27 §1 -- the core services foundation: saves log through its logger, and the checkpoint cadence of §4 is a setting in its store; its atomic write serves app data, never a user's document
- -> XREF: D01 T02 §5 -- the shared atomic document writer, re-planned by `D00 T07 §4`, which becomes this file's save sequence rather than a second one

## Outcome

- `docs/dev/document-safety.md` holds the save sequence, designed against the seven invariants and reviewed with its code; `isotone::core::Save` implements it with a durable journal.
- A save carries every item of the file identity contract or is refused naming the item.
- Every secondary copy (checkpoints, dumps, scratch spill, persisted undo, caches) is AES-GCM encrypted before its first byte, in a folder only the user and SYSTEM can read.
- Checkpoints, retirement, and recovery give the cadence and the loss bound the spec states, proved by killing the process at random points and at every step of the protocol.

**Adjacency:** list=applicable @ D01 T19 §5; document=not-applicable (the save writes the user's own document, it prints nothing); settings=applicable @ D01 T19 §4; reporting=applicable @ D01 T19 §5; notifications=applicable @ D01 T19 §4; permissions=applicable @ D01 T19 §2; audit=applicable @ D01 T19 §1; exchange=not-applicable (the format is each app's; this file moves bytes it is given); reverse=applicable @ D01 T19 §5

**Adjacency rationale:** Recovery lists every leftover file for the user to keep or delete (§5), with the recovery report as its summary; the checkpoint cadence is a default the user can see and change, and a stalled checkpoint tells the user (§4); a refused save names the protection it could not keep (§2); every save, checkpoint, retirement, and recovery writes a log line (§1); and a recovered document can be discarded, which retires its checkpoints (§5).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The save sequence, designed, reviewed, and journaled | D00 T07 §3, D01 T27 §2 |  [ ]   |
|   2   |   §2    | The file identity contract | §1 |  [ ]   |
|   3   |   §3    | Encrypted secondary copies | §1 |  [ ]   |
|   4   |   §4    | Checkpoints and retirement | §3, D01 T18 §3 |  [ ]   |
|   5   |   §5    | Recovery at the next start | §2, §4, D01 T15 §1 |  [ ]   |
|   6   |   §6    | The kill-test proofs | §5 |  [ ]   |

---

## 1. The Save Sequence, Designed, Reviewed, and Journaled

The spec owns the invariants and leaves the exact call sequence to this section, because a sequence is only right with its code beside it. A sequence that cannot meet an invariant sends the spec back for revision, recorded as a decision.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service and its design document.
**Needs:** Windows host (build/test)

Every save writes its journal record and one line to the audit log naming the target, the outcome, and the bytes written.

- [ ] Write `docs/dev/document-safety.md`: the save sequence step by step (the temporary file with a fresh random name created `CREATE_NEW` beside the target, its protection derived from the target's before any data, the data written with its SHA-256 computed through CNG as it passes, flushed, the previous version moved aside through a handle held since before, the commit by rename that never replaces, the contract items applied and made durable, the previous version released through its held handle), each step mapped to the invariants it keeps and to the journal state it records, with the starting requirements of review rounds 3 to 10. Done when: every invariant 1 to 7 names the steps that keep it, and the independent review of the design document (`independent-review`) is recorded with its findings resolved.
- [ ] Implement `isotone::core::Save` in `native/core/src/save.cpp` to that sequence, holding no lock on an open document's file between saves, and writing a journal record (atomic, flushed) at each durable state. Done when: `Save.JournalRecordsEachDurableState` and `Save.NoLockBetweenSaves` (another process opens the target for write between saves) pass.
- [ ] Serialize saves per target in edit order: a save requested while one runs waits, and only the newest waiting request runs. Done when: `Save.NewestWaitingSaveRuns` passes.
- [ ] Hash the previous version while it is held and keep it as a conflict when it is not the version the app last read or wrote. Done when: `Save.ForeignPreviousVersionKeptAsConflict` passes.
- [ ] Log one line per save naming the target, the outcome, and the bytes written. Done when: the tests assert the line.
- [ ] Commit: `"core: the document save sequence, designed, reviewed, and journaled"`

**Test checkpoint:** Unit test: `Save.JournalRecordsEachDurableState`, `Save.NoLockBetweenSaves`, `Save.NewestWaitingSaveRuns`, and `Save.ForeignPreviousVersionKeptAsConflict` pass through CTest on every preset, including the AddressSanitizer lanes; the design document's independent review record is quoted with its findings resolved. Cheaper substitute that fails: `ReplaceFileW` alone, which keeps neither the temporary file's protection before data nor a journal recovery can resume.

## 2. The File Identity Contract

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the contract items a save carries.
**Needs:** Windows host (build/test)

- [ ] Carry each item of the contract from the version displaced to its replacement, checked before any document data is written and applied, made durable, and read back before the previous version is released: the owner where the user may set it, the DACL, the mandatory integrity label with its policy (`LABEL_SECURITY_INFORMATION`), the security resource attributes, the creation time, the file attributes (a read-only target refused), compression, EFS encryption with every user able to decrypt the target (`QueryUsersOnEncryptedFile`, `AddUsersToEncryptedFileEx`), and the named streams the spec lists. Done when: `FileIdentity.CarriesEachItem` passes for each item on NTFS, and `FileIdentity.RefusesWhatItCannotReproduce` names the item in the refusal.
- [ ] Apply a protection another program adds to the target while the save runs to the new file before the save is reported, telling the user it arrived mid-save; roll the save back when a post-commit step cannot complete safely (invariant 7). Done when: `FileIdentity.MidSaveProtectionReachesNewFile` and `Save.PostCommitFailureRollsBack` pass.
- [ ] Record what a volume without access control lists (FAT, exFAT) cannot carry, and refuse nothing there that the volume never had. Done when: `FileIdentity.FatVolumeCarriesWhatItCan` passes on a FAT test volume (a VHD the test mounts and removes).
- [ ] Commit: `"core: saves carry the file's identity or refuse"`

**Test checkpoint:** Unit test: `FileIdentity.CarriesEachItem`, `FileIdentity.RefusesWhatItCannotReproduce`, `FileIdentity.MidSaveProtectionReachesNewFile`, `Save.PostCommitFailureRollsBack`, and `FileIdentity.FatVolumeCarriesWhatItCan` pass through CTest (the EFS and integrity-label cases on the reference machine, which the run records). Cheaper substitute that fails: copying the DACL only, which loses EFS key holders and the integrity label and so weakens a protected file on its first save.

## 3. Encrypted Secondary Copies

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the storage rule for every copy of document data.
**Needs:** Windows host (build/test)

- [ ] Add `isotone::core::SecondaryStore`: every secondary copy (checkpoints, crash dumps, the tile store's scratch spill, persisted undo data, preview and thumbnail caches) is encrypted with AES-GCM through CNG before its first byte is written, under a key protected for the current user with DPAPI, into a folder created with a DACL granting only the user and SYSTEM, logging where a volume cannot carry the DACL. Done when: `SecondaryStore.NoPlaintextReachesDisk` (a scan of every byte written finds no plaintext marker) and `SecondaryStore.FolderGrantsOnlyUserAndSystem` pass.
- [ ] Refuse a secondary-copy kind that is not registered with the store, so a later section's new kind joins the list in that section. Done when: `SecondaryStore.UnregisteredKindRefused` passes.
- [ ] Commit: `"core: secondary copies of document data are encrypted before their first byte"`

**Test checkpoint:** Unit test: `SecondaryStore.NoPlaintextReachesDisk`, `SecondaryStore.FolderGrantsOnlyUserAndSystem`, and `SecondaryStore.UnregisteredKindRefused` pass through CTest on every preset. Cheaper substitute that fails: relying on the folder DACL alone, which a FAT or exFAT drive cannot carry.

## 4. Checkpoints and Retirement

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the checkpoint cadence and its retirement records; the stall notice is a placeholder in the host.
**Needs:** Windows host (build/test)

When no checkpoint has completed for 120 s while edits are unsaved, the host can show a notification to the user, and it clears at the next completed checkpoint.

- [ ] Checkpoint each open document, untitled ones included, into two alternating slots in the recovery folder with the save's write, flush, and verify steps, each checkpoint carrying a checksum, the document's persistent identity, the session's identity, and the edit counter. Done when: `Checkpoint.AlternatesSlots` and `Checkpoint.CorruptSlotLeavesPreviousGood` pass.
- [ ] Use the spec's default cadence (within 10 s of the first unsaved edit, then every 60 s with unsaved edits or after 5 s idle), as a setting the user can change with readback, and tell the user when no checkpoint has completed for 120 s while edits are unsaved. Done when: `Checkpoint.CadenceFollowsSetting` and `Checkpoint.StallIsReported` pass on a fake clock.
- [ ] Retire checkpoints by an atomic retirement record naming the identity, the session, and the edit counter covered: a durable save retires only those at or below its counter, a clean close or a discard retires all after pending writes finish or are cancelled. Done when: `Checkpoint.SaveRetiresOnlyCovered` and `Checkpoint.DiscardCannotBeResurrected` pass.
- [ ] Commit: `"core: checkpoints with a bounded loss and exact retirement"`

**Test checkpoint:** Unit test: `Checkpoint.AlternatesSlots`, `Checkpoint.CorruptSlotLeavesPreviousGood`, `Checkpoint.CadenceFollowsSetting`, `Checkpoint.StallIsReported`, `Checkpoint.SaveRetiresOnlyCovered`, and `Checkpoint.DiscardCannotBeResurrected` pass through CTest on every preset. Cheaper substitute that fails: one checkpoint file overwritten in place, which a crash mid-write leaves with nothing good.

## 5. Recovery at the Next Start

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- recovery and its report; the recovery list is a placeholder in the host, the product dialog is each app's.
**Needs:** Windows host (build/test)

- [ ] At start, settle every journal record left behind, resuming each save from its last durable state as far as it can without deleting or overwriting anything (invariant 3): complete a committed save's contract from the previous version, give a free target name its previous version back by a rename that never replaces, and keep and list every leftover file. Done when: `Recovery.ResumesFromEachJournalState` passes for each state the journal records.
- [ ] Keep a record whose step cannot complete yet (another program holds the committed file) and retry it at each start, telling the user which file is pending. Done when: `Recovery.PendingStateKeptAndReported` passes.
- [ ] Recover each document from its newest completed checkpoint, retiring its earlier checkpoints only once the recovered contents are durable again or the user discards them, and list every leftover in a recovery report the user keeps or deletes from. Done when: `Recovery.NewestCheckpointWins` and `Recovery.ReportListsEveryLeftover` pass, and the host scenario `recovery` shows the list.
- [ ] Commit: `"core: recovery settles every save and restores every document"`

**Test checkpoint:** Unit test and driven run with evidence: `Recovery.ResumesFromEachJournalState`, `Recovery.PendingStateKeptAndReported`, `Recovery.NewestCheckpointWins`, and `Recovery.ReportListsEveryLeftover` pass through CTest; `foundation-host --scenario recovery --report build/foundation/recovery.json` exits 0 listing the recovered document and every leftover file (quoted). Cheaper substitute that fails: deleting leftovers at start, which can delete the only good copy of a document.

## 6. The Kill-Test Proofs

The spec's proofs kill the process at random points and at every step of the protocol; this section runs them as a harness and records the results.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a test harness.
**Needs:** Windows host (build/test)

- [ ] Add `native/tests/document-safety/kill_harness.cpp`: a driver that runs a child doing edits, saves, and checkpoints, kills it with `TerminateProcess` at random points (seeded, the seed recorded) and at each step of the save protocol in turn, restarts, recovers, and checks that the target's name holds a complete old or new file and the recovered contents equal the newest completed checkpoint. Done when: `DocumentSafety.KillAtEveryProtocolStep` and `DocumentSafety.KillAtRandomPoints` (at least 1,000 kills) pass, with the child's whole process tree stopped on timeout.
- [ ] Add the spec's ordering proofs: a save of revision N completing after N+1 was checkpointed, then a kill, recovers N+1; a slow save of N with N+1 queued, killed at each point, never leaves N after N+1 committed; a cleanup failure injected after the commit is reported as a successful save and finished at the next start. Done when: `DocumentSafety.LateSaveDoesNotLoseNewerCheckpoint`, `DocumentSafety.QueuedSavesCommitInOrder`, and `DocumentSafety.CleanupFinishedAtNextStart` pass.
- [ ] Add the concurrent-program proofs: an external editor saving the file between saves, a reader holding it open, and a sync-client-style stream attached during a save. Done when: `DocumentSafety.ExternalSaveOfferedReload`, `DocumentSafety.ReaderHoldingFileDoesNotBlockSave`, and `DocumentSafety.AttachedStreamLosesNoData` pass.
- [ ] Commit: `"core: the document safety kill tests"`

**Test checkpoint:** Unit test and driven run with evidence: `DocumentSafety.KillAtEveryProtocolStep`, `DocumentSafety.KillAtRandomPoints` (the seed and kill count quoted), `DocumentSafety.LateSaveDoesNotLoseNewerCheckpoint`, `DocumentSafety.QueuedSavesCommitInOrder`, `DocumentSafety.CleanupFinishedAtNextStart`, `DocumentSafety.ExternalSaveOfferedReload`, `DocumentSafety.ReaderHoldingFileDoesNotBlockSave`, and `DocumentSafety.AttachedStreamLosesNoData` pass through CTest on the reference machine (x64) and on an ARM64 machine. Cheaper substitute that fails: a crash handler that saves on the way down, which the failure model rules out because no code runs after the failure.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Save.*`, `FileIdentity.*`, `SecondaryStore.*`, `Checkpoint.*`, `Recovery.*`, and `DocumentSafety.*` cases reporting through CTest
- [ ] The kill harness runs clean under `x64-asan`
- [ ] `docs/dev/document-safety.md` matches the code it describes, step for step
- [ ] `python scripts/todo-graph.py validate` clean
