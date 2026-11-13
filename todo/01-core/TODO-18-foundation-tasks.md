---
schema_version: 1
id: foundation-tasks
domain: 01-core
status: draft
title: "TODO-18 -- Foundation: the Task System and Threading"
depends_on: []
frozen: false
track: F5
---

# TODO-18 -- Foundation: the Task System and Threading

> **Goal:** the threading model the spec fixes is built and proved: the UI thread is the one place a document changes, a render thread owns the Direct3D immediate context and is fed immutable snapshots with a bounded GPU queue, background work runs on a thread pool in three cancellable priority classes, and a task's result never overwrites newer work or reaches a closed document.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** `isotone::core` (`native/core/`) has no task system; the renderer of `D01 T15 §2` draws on the UI thread until this file moves it.
<!-- claim: exists native/core/CMakeLists.txt -->
<!-- claim: absent native/core/include/isotone/core/tasks.h -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Threading and lifetimes" -- the UI thread as the OLE single-threaded apartment, the render thread and its snapshots, the bounded GPU queue with `D3D11_QUERY_EVENT` and at most one unfinished dispatch, the 2 ms dispatch budget, the three priority classes, and version-checked results with weak document references
- [`standards/cpp.md`](../../standards/cpp.md), "Threading" -- the code rules these types follow
- -> XREF: D01 T15 §2 -- the renderer moved onto the render thread here
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T19 §4 -- checkpoints run as background tasks with version checks
- -> XREF: D01 T24 §1 -- the canvas consumes the render thread's snapshots

## Outcome

- `isotone::core::Tasks` runs work in the interactive, background, and idle classes, every task cancellable, and a document's tasks cancelled before it closes.
- The render thread does every draw and present from immutable snapshots, keeps only the newest per visual, and submits a GPU engine dispatch only while fewer than one is unfinished.
- A task's result commits only if its document is still open and still at the edit version the task started from.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (the budgets are spec defaults, measured, not user settings); reporting=not-applicable (no data to summarize); notifications=applicable @ D01 T18 §3; permissions=not-applicable (writes no user file); audit=applicable @ D01 T18 §3; exchange=not-applicable (no files); reverse=applicable @ D01 T18 §3

**Adjacency rationale:** A result discarded because the document moved on is reported to the user when they started the work (an applied filter), logged either way, and never commits an edit undo would have to unwind.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The thread pool in three cancellable priority classes | D00 T07 §3 |  [ ]   |
|   2   |   §2    | The render thread, immutable snapshots, and the bounded GPU queue | §1, D01 T15 §2 |  [ ]   |
|   3   |   §3    | Version-checked results and weak document references | §1 |  [ ]   |

---

## 1. The Thread Pool in Three Cancellable Priority Classes

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service.
**Needs:** Windows host (build/test)

- [ ] Add `isotone::core::Tasks` in `native/core/include/isotone/core/tasks.h` over the Windows thread pool (`CreateThreadpool` with one pool per class), with `submit(Priority, CancellationToken, work)`, interactive work bounded so it never starves the UI thread's frames. Done when: `Tasks.InteractiveRunsBeforeBackground` and `Tasks.IdleRunsOnlyWhenIdle` pass.
- [ ] Make every task cancellable through a token checked at the task's own yield points, and cancel a document's tasks (by its identity) before it closes, waiting for running ones to reach a yield point. Done when: `Tasks.CancelledTaskNeverCompletes` and `Tasks.CloseCancelsDocumentTasks` pass, under `x64-asan` too.
- [ ] Marshal results to the UI thread through a posted message, never by calling into windows from a pool thread. Done when: `Tasks.ResultsArriveOnUiThread` asserts the thread id.
- [ ] Commit: `"core: the task system with three cancellable priority classes"`

**Test checkpoint:** Unit test: `Tasks.InteractiveRunsBeforeBackground`, `Tasks.IdleRunsOnlyWhenIdle`, `Tasks.CancelledTaskNeverCompletes`, `Tasks.CloseCancelsDocumentTasks`, and `Tasks.ResultsArriveOnUiThread` pass through CTest on every preset, including `x64-asan` and `arm64-asan`. Cheaper substitute that fails: `std::async`, which has no priorities, no cancellation, and no way to keep a background task off an interactive one's core.

## 2. The Render Thread, Immutable Snapshots, and the Bounded GPU Queue

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the render thread and its queue.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Threading and lifetimes" (the queue's proof measures presented frames)

- [ ] Move every draw and present onto one render thread that owns the Direct3D 11 immediate context; the UI thread hands it immutable snapshots (the draw list and the visible tiles at a version), and only the newest pending snapshot per visual is kept. Done when: `RenderThread.KeepsOnlyNewestSnapshot` passes and no Direct3D call is made from another thread (a debug assertion in the context wrapper).
- [ ] Cut GPU engine work into bounded dispatches and submit the next only while fewer than one is unfinished, tracked with `D3D11_QUERY_EVENT`, interface frames before engine work. Done when: `RenderThread.AtMostOneDispatchInFlight` passes with a mock dispatcher.
- [ ] Add the host scenario `gpu-backlog` that queues several hundred engine dispatches while interface frames are presented, and reports the frame gaps from presentation statistics. Done when: the report shows no gap longer than two vsync intervals while the backlog drains.
- [ ] Commit: `"ui: the render thread with snapshots and a bounded GPU queue"`

**Test checkpoint:** Unit test and driven run with evidence: `RenderThread.KeepsOnlyNewestSnapshot` and `RenderThread.AtMostOneDispatchInFlight` pass through CTest; `foundation-host --scenario gpu-backlog --report build/foundation/gpu-backlog.json` exits 0 with the dispatch count and no frame gap over two vsync intervals (quoted). Cheaper substitute that fails: drawing on the UI thread, where a long engine dispatch blocks input and the frame both.

## 3. Version-Checked Results and Weak Document References

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the commit rule for background results.
**Needs:** Windows host (build/test)

A discarded result writes one line to the audit log; when the user started the work (an applied filter), a notification says it was discarded because the document changed, and since nothing is committed there is nothing to undo or cancel afterwards.

- [ ] Give each task its document's identity and the edit version it started from, holding the document weakly; commit its result as a command on the UI thread only if the document is open and still at that version, otherwise discard it and re-run it (a preview) or report it (an applied filter the user started), logging the outcome. Done when: `TaskResults.DiscardedAfterNewerEdit`, `TaskResults.DiscardedAfterUndo`, `TaskResults.NothingAfterCancel`, and `TaskResults.NothingAfterClose` pass.
- [ ] Commit: `"core: background results commit only at the version they started from"`

**Test checkpoint:** Unit test: `TaskResults.DiscardedAfterNewerEdit`, `TaskResults.DiscardedAfterUndo`, `TaskResults.NothingAfterCancel`, and `TaskResults.NothingAfterClose` pass through CTest on every preset, including the AddressSanitizer lanes (no use after the document closed). Cheaper substitute that fails: committing every finished result, which overwrites an edit the user made while the filter ran.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Tasks.*`, `RenderThread.*`, and `TaskResults.*` cases reporting through CTest
- [ ] The `gpu-backlog` scenario passes on the reference machine
- [ ] `python scripts/todo-graph.py validate` clean
