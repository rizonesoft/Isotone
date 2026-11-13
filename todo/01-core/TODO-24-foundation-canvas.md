---
schema_version: 1
id: foundation-canvas
domain: 01-core
status: draft
title: "TODO-24 -- Foundation: the GPU Canvas Meeting the Frame Cadence and Pen Latency Goals"
depends_on: []
frozen: false
track: F11
---

# TODO-24 -- Foundation: the GPU Canvas Meeting the Frame Cadence and Pen Latency Goals

> **Goal:** the document canvas is its own composition visual with its own swap chain, fed by the render thread, and on the reference machine it meets the spec's goals while a GPU filter and background work run and floating panels are open: at the display's refresh rate with no more than 1 missed vsync per 1,000 frames and no gap longer than two vsync intervals, and 95 percent of pen samples displayed within one refresh interval plus 4 ms, none over two intervals plus 4 ms.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No canvas exists. `docs/dev/reference-machine.md` is written by the first benchmark section (`D00 T04 §2`) and records the reference machine; the frame and latency measurements are new.
<!-- claim: absent native/ui/src/canvas -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "The goals" (interface frame cadence and pen latency, with their protocols), "Rendering", and "Threading and lifetimes" -- the canvas visual, presentation statistics, `GetPointerInfoHistory` and `POINTER_INFO.PerformanceCount`, and the load the goals are measured under
- [`docs/dev/reference-machine.md`](../../docs/dev/reference-machine.md) -- the machine the goals are measured on
- -> XREF: D01 T18 §2 -- the render thread and the bounded GPU queue the canvas draws through
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T22 §2 -- the runner that injects pen samples with known timestamps

## Outcome

- `isotone::ui::Canvas` is a composition visual with its own waitable swap chain, panned and zoomed from render snapshots, taking pen input through `WM_POINTER` with every coalesced sample.
- A measurement harness reports frame cadence from presentation statistics and per-sample pen latency in one clock domain, and the goals are met on the reference machine under the stated load.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (no tunable value: the goals are fixed); reporting=applicable @ D01 T24 §2; notifications=not-applicable (no long-running work a user starts); permissions=not-applicable (writes no user file); audit=not-applicable (no document edits); exchange=not-applicable (no files); reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** The measurement report (§2) is this file's only output; the canvas content and its edits are the apps'.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The canvas visual, its swap chain, and pen input with every sample | D00 T07 §3, D01 T18 §2 |  [ ]   |
|   2   |   §2    | Measuring the frame cadence and pen latency goals under load | §1, D01 T22 §2 |  [ ]   |

---

## 1. The Canvas Visual, Its Swap Chain, and Pen Input with Every Sample

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the canvas mechanism with placeholder content.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Rendering" (the canvas presents to a live window)

- [ ] Add `isotone::ui::Canvas` in `native/ui/src/canvas/`: a DirectComposition visual with its own flip-sequential waitable swap chain (maximum frame latency 1), drawn by the render thread from snapshots of placeholder tiles, panned and zoomed without redrawing the interface visual. Done when: `Canvas.RedrawsIndependentlyOfInterface` passes and the host scenario `canvas-pan` reports no interface present during a pan.
- [ ] Take pen input through `WM_POINTER`, reading every coalesced sample with `GetPointerInfoHistory` and its `POINTER_INFO.PerformanceCount`, recording which samples each presented frame drew and its present id. Done when: `Canvas.ReadsEveryCoalescedSample` passes with a recorded pointer history.
- [ ] Commit: `"ui: the GPU canvas with every pen sample"`

**Test checkpoint:** Unit test and driven run with evidence: `Canvas.RedrawsIndependentlyOfInterface` and `Canvas.ReadsEveryCoalescedSample` pass through CTest; `foundation-host --scenario canvas-pan --report build/foundation/canvas-pan.json` exits 0 with no interface present during the pan (quoted). Cheaper substitute that fails: one swap chain for the window, where every canvas frame redraws the panels.

## 2. Measuring the Frame Cadence and Pen Latency Goals under Load

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a measurement harness.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "The goals" (presentation statistics of a live display)

- [ ] Add the host scenario `frame-cadence` that pans, zooms, resizes a panel, and resizes the window for 60 s each while a GPU filter (a stand-in that enqueues hundreds of bounded dispatches) and background tasks run and two floating panels are open, taking displayed-frame times from `IDXGISwapChain::GetFrameStatistics` and PresentMon. Done when: its report gives, per activity, the refresh rate, the missed vsyncs per 1,000 frames, and the longest gap.
- [ ] Add `CanvasDrive.PenLatency` that injects pen strokes through the driven-input runner and measures each sample from its `PerformanceCount` to the vsync of the first displayed frame that shows it, counting a merged sample at the later display time and a dropped sample as a failure. Done when: its report gives the share of samples within one refresh interval plus 4 ms and the worst sample.
- [ ] Record both results on the reference machine in `docs/dev/reference-machine.md` beside its description, and send the spec back for revision (a decision entry) if either goal cannot be met. Done when: the file holds the results with the run's date and build id.
- [ ] Commit: `"ui: frame cadence and pen latency measured against the goals"`

**Test checkpoint:** Driven run with evidence: `foundation-host --scenario frame-cadence --report build/foundation/frame-cadence.json` exits 0 with each activity at no more than 1 missed vsync per 1,000 frames and no gap over two vsync intervals; `ctest --preset x64-release -L drive -R CanvasDrive` passes with at least 95 percent of pen samples within one refresh interval plus 4 ms and none over two intervals plus 4 ms (both reports quoted, with the reference machine's refresh rate). Cheaper substitute that fails: renderer timings, which say when a frame was drawn, not when the user saw it.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Canvas.*` cases reporting through CTest
- [ ] Both goals are met on the reference machine and recorded in `docs/dev/reference-machine.md`
- [ ] `python scripts/todo-graph.py validate` clean
