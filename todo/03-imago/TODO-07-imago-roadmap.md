---
schema_version: 1
id: imago-roadmap
domain: 03-imago
status: draft
title: "TODO-07 -- Imago after 0.1.0: Deferral Owners and Accessibility"
depends_on: []
track: I7
---

# TODO-07 -- Imago after 0.1.0: Deferral Owners and Accessibility

> **Goal:** The Imago work after its first release that the plan is already committed to: the rest of the filter catalog that the 0.1.0 Filter menu names for its disabled items, RAW import through the decoder Lumen shares, and the workspaces, Preferences, accessibility, and localization work the acceptance bar requires. When this file closes, no Imago menu item is disabled as planned, and Imago works without a mouse or eyes. On 2026-09-26 the Imago parity plan relocated three of these sections into its phases without changing their addresses: the filter catalog (§3) runs first in Phase 21, where the filter surfaces and engine extensions extend it, workspaces and Preferences (§17) run first in Phase 27, and the accessibility and localization audit (§16) runs last in Phase 27 so it covers every parity surface; RAW import (§11) stays in Phase 41, after Lumen's decoder ships.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The legacy roadmap (`docs/legacy/imago-roadmap.md`, 853 lines, phases 0 to 11) was mined into 18 sections on 2026-09-26. The same day the plan was bounded (`todo/budget.json`): the 14 sections nothing outside this file depends on, defers to, or names in the acceptance bar moved to `todo/backlog.md` as B-014 to B-027, and their section numbers are retired, never reused. What stays: the filter catalog (§3), which `D03 T05 §3` names in the tooltips of its disabled filters; RAW import (§11), which `D04 T01` cross-references for the shared decoder; accessibility (§16), which the acceptance bar names; and workspaces and Preferences (§17), which §16 builds on and which enables the planned Preferences item. Several features have model types and no behavior, among them `AdjustmentLayer` and a Roslyn `ScriptEngine` in `Imago.Scripting` (62 lines), whose sections now wait in the backlog. Every section below names its legacy source with a `-> SOURCE:` line. **Corrected 2026-09-26:** the Imago parity plan promoted B-014 to B-023 and B-027 into its sections, merged B-025 (scripting) into the suite-wide B-041, and kept B-024 and B-026 in the backlog; `AdjustmentLayer` gains its behavior in `D03 T11 §1`, and the parity sections extend §3, §16, and §17 through their dependency edges. **Corrected 2026-09-27:** on the operator's decision to plan every deferred row ("Group 1: plan them all"), B-026 (performance, `legacy-imago-9`) was promoted into §18 to §20 here, B-024 (filter plug-ins, `legacy-imago-8.1-8.3`) into `D03 T14 §12`, and B-012 (third-party filter plug-in hosts) into `D01 T09` with Imago's surface in `D03 T14 §11`; no section number was reused.
<!-- claim: lines docs/legacy/imago-roadmap.md = 853 -->
<!-- claim: exists src/Imago/src/Imago.Core/Layers/AdjustmentLayer.cs -->
<!-- claim: lines src/Imago/src/Imago.Scripting/ScriptEngine.cs = 62 -->

## Inputs

- [`docs/legacy/imago-roadmap.md`](../../docs/legacy/imago-roadmap.md) -- the source of every section; read the named legacy phase before grooming
- [`standards/imago.md`](../../standards/imago.md) -- the rules every section builds to
- -> XREF: D04 T01 §4 -- the Lumen RAW decoder §11 moves to `Photon.Core` when Imago imports RAW
- -> XREF: D01 T07 §1 -- the suite develop engine cites §11: Imago's RAW open dialog develops through D01 T07 §1 instead of its own exposure and white balance code
- -> XREF: D03 T08 §1 -- Imago parity document and view cites §17: workspaces the panels there dock into
- -> XREF: D03 T14 §2 -- Imago parity filters cites §3: the legacy filter catalog whose disabled items D03 T14 §2 resolves
- -> XREF: D03 T15 §12 -- Imago parity photo (Camera Raw and merges) cites §11: RAW import: opens RAW into D03 T15 §12's studio and supplies camera RAW sources to RAW layers, merges, and astro frames when it ships in Phase 41
- -> XREF: D03 T20 §9 -- Imago parity workspace cites §17: workspaces and the Preferences dialog it extends; §16: the accessibility and localization audit that consumes D03 T20 §9's settings
- -> XREF: D03 T21 §12 -- the Imago parity releases cites §16: the accessibility and localization audit D03 T21 §12 depends on, so 1.0.0 ships no unaudited surface
- -> XREF: D02 T18 §10 -- Nodus's camera RAW import cites §11: it consumes the RAW decoder §11 moves to `Photon.Core`, never a copy
- [`../backlog.md`](../backlog.md) -- the Imago feature ideas that left this file (B-014 to B-027); on 2026-09-26 the Imago parity plan promoted B-014 to B-023 and B-027 and merged B-025 into B-041, and on 2026-09-27 the operator's decision promoted the last two: B-026 into §18 to §20 and B-024 into `D03 T14 §12`

## Outcome

- Every section below ships with its surface, commands with undo, settings, log lines, user-guide page, and tests, like the 0.1.0 sections before it.
- Every disabled "Planned" menu item from 0.1.0 that names a section of this file is working when this file closes.
- Imago meets a written, measured performance budget on a 100-megapixel, 50-layer document (open, paint, composite, filter, save, memory, cold start), and a gate fails on regression.

**Adjacency:** list=applicable; document=not-applicable (printing arrives with the Imago parity phases in D03 T18 §6); settings=applicable @ D03 T07 §17; reporting=applicable; notifications=applicable; permissions=not-applicable (file refusals are owned by the format sections in D03 T04); audit=applicable; exchange=applicable; reverse=applicable @ D03 T07 §17

**Adjacency rationale:** The workspace and Preferences work is the settings and list surface; filter parity and RAW open results are reporting; long filters and RAW opens notify through the status strip; every edit is logged and undoable.

## Implementation Order

| Order | Section | Deliverable                                            | Depends On              | Status |
| :---: | :-----: | ------------------------------------------------------ | ----------------------- | :----: |
| 1 | §3 | The rest of the filter catalog                         | D03 T06 §3              |  [ ]   |
| 2 | §11 | RAW import through the shared decoder                  | D03 T06 §3, D04 T01 §4, D01 T07 §1, D03 T15 §12 |  [ ]   |
| 3 | §17 | Workspaces, panels, and preferences                    | D03 T06 §3              |  [ ]   |
| 4 | §18 | Performance I: the benchmark harness and the Imago performance budget | D03 T06 §3, D03 T12 §1, D03 T14 §1, D03 T20 §5 |  [ ]   |
| 5 | §19 | Performance II: memory: tile cache, compression, history, and large-document open | §18 |  [ ]   |
| 6 | §20 | Performance III: SIMD hot paths, parallel compositing, and cold start | §18 |  [ ]   |
| 7 | §16 | Accessibility and localization                         | §17, D03 T20 §8, D03 T20 §9 |  [ ]   |

---

## 3. The Rest of the Filter Catalog

The legacy plan lists motion and surface blur, smart sharpen, noise (add, reduce, median, dust and scratches), distort (twirl, pinch, spherize, wave, ripple, displace, polar coordinates), stylize (emboss, find edges, oil paint), and render (clouds, lens flare, lighting). The 0.1.0 menu carries the first five as disabled planned items. -> SOURCE: legacy-imago-5.2-5.7

- [ ] Implement each as an `IImageFilter` through the pipeline, each with a golden from libvips or GIMP (version recorded) and a fidelity test within a stated tolerance. Done when: every filter in the legacy list has a passing test or a recorded decision to drop it in `docs/dev/decisions.md`.
- [ ] Enable every planned filter menu item and remove its `PlannedCommands` entry. Done when: `MenuAuditTests` passes with no filter planned.
- [ ] GPU implementations for the three slowest filters with CPU parity tests. Done when: parity within 1/255 is quoted.
- [ ] Commit: `"imago: the full filter catalog"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` prints a result per filter; the GPU parity results are quoted. Cheaper substitute that fails: filters without goldens.

## 11. RAW Import through the Shared Decoder

Lumen decodes RAW (`D04 T01 §4`). The day Imago imports RAW, the decoder adapter moves from `Photon.Lumen.Core` to `Photon.Core` and both apps consume it; nothing is copied. -> SOURCE: legacy-imago-7.2-raw

- [ ] Move the RAW decoder adapter and its tests to `Photon.Core` (and its native dependency with it), with Lumen consuming it unchanged. Done when: Lumen's RAW tests pass against the moved type and `grep` finds one decoder class.
- [ ] Imago opens RAW files into the Develop studio (`D03 T15 §12`), developing through the suite develop engine (`D01 T07 §1`) with the decoder's output as a `RawDevelopSource`, then opens the result as a document in the workflow's bit depth (IP-1471). Done when: a committed small DNG fixture opens with its dimensions and a test asserts the render went through `DevelopPipeline`. **Corrected 2026-09-26:** said "a minimal develop dialog (exposure, white balance, then open as a 16-bit document)"; the Imago parity plan built the Develop studio and the shared engine first, so a second dialog would be a copy.
- [ ] Enable `File, Open RAW into Develop` and RAW layer sources, removing the `Planned: D03 T07 §11` entry `D03 T15 §12` registered in `PlannedCommands`, and register camera RAW with the focus-merge and astro frame loaders that refuse it by name until now (`D03 T15 §9`, `D03 T15 §10`). Done when: `MenuAuditTests` pass with no item planned to this section and a test loads a camera RAW fixture as a focus-merge source.
- [ ] Commit: `"core: share the RAW decoder; Imago opens RAW files"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the moved decoder tests, an Imago RAW open test through the Develop studio, and `MenuAuditTests` reporting; `grep -rn "class .*RawDecoder" src` prints one path under `src/Photon.Core/`. Cheaper substitute that fails: Imago referencing Lumen's assembly.

## 16. Accessibility and Localization

Every Imago surface keyboard- and screen-reader-operable and translatable. -> SOURCE: legacy-imago-6.5

- [ ] Audit every window with Accessibility Insights for Windows (version quoted) and fix every failure. Done when: the committed report shows none.
- [ ] Move strings to `.resx` with a pseudo-locale build. Done when: the pseudo-locale capture shows no untransformed string.
- [ ] High contrast and 200 percent captures of every window. Done when: committed.
- [ ] Commit: `"imago: accessibility fixes and localizable strings"`

**Requires:** display-session -- the audit needs an interactive desktop

**Test checkpoint:** the audit report shows zero failures. Cheaper substitute that fails: automation names on toolbar buttons only.

## 17. Workspaces, Panels, and Preferences

Saved panel layouts, a Preferences dialog over every Imago setting, and shortcut remapping. -> SOURCE: legacy-imago-6.2-6.6

**Fidelity:** Preferences dialog -- new build, no baseline; captured to docs/captures/imago/preferences/.
**Job:** a user can arrange panels, save workspaces, and change every setting and shortcut in one place. Consumer: every setting's consumer.
**Treatment:** Window, Workspace (save, switch, reset); Preferences categories bound to the settings store, applying on OK with Cancel reverting and Reset to Defaults restoring every value; shortcut remapping on the keymap. If Nodus's Preferences dialog frame (`D02 T06 §13`) fits, it moves to `Photon.UI` and both apps use it. Cheaper substitute that fails the checkpoint: settings without a surface.
**Chrome:** consume the settings store, the keymap, and AvalonDock.

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Workspaces and Preferences with a test that every setting key has a control, Cancel reverting an edit, and Reset to Defaults restoring every value. Done when: the tests pass.
- [ ] Enable File, Preferences and remove its planned entry. Done when: `MenuAuditTests` passes.
- [ ] Commit: `"imago: workspaces and a Preferences dialog"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the preferences tests reporting. Cheaper substitute that fails: hand-edited JSON.

## 18. Performance I: The Benchmark Harness and the Imago Performance Budget

`standards/shared.md` requires every feature to name the document size it must handle and the time it must meet, and the legacy Imago roadmap's phase 9 asked for benchmarks on a 100-megapixel, 50-layer document, fixes to the top measured costs, and a cold start under two seconds. Nothing measures Imago as a whole yet: individual sections quote their own budgets, but no harness runs the whole document through open, paint, composite, filter, save, and memory, and no gate stops a regression. This section builds that harness on the benchmark project `D03 T04 §1` created and the BenchmarkDotNet package decision `D02 T07` recorded (MIT), writes the budget, commits baselines, and adds a gate; §19 and §20 then fix what it measures. Promoted from backlog B-026 on 2026-09-27 (operator: "Group 1: plan them all"). Owns no catalog rows. -> SOURCE: legacy-imago-9

**Fidelity:** no surface of its own (a benchmark project, a budget document, and a gate script).

**Requires:** display-session -- the paint-latency and first-frame scenarios render to a real window

- [ ] Add `tests/Photon.Imago.Benchmarks/Fixtures/PerfDocumentBuilder.cs`: builds a deterministic 10,000 by 10,000 pixel, 50-layer `.imago` document from a seed (pixel layers with masks, adjustment layers, two smart filters, a text layer, and a group) into `build/perf/`, never committed. Done when: two builds with the same seed produce byte-identical files and the build time is logged.
- [ ] Add scenarios in `tests/Photon.Imago.Benchmarks/Scenarios/`: open the perf document and a 2 GB PSB, a 200-dab brush stroke with dab-to-screen latency, full-view composite and 1:1 pan frame time, Gaussian blur radius 20 on 24 megapixels, re-editing a live filter, save, and undo of the last ten steps. Done when: `dotnet run -c Release --project tests/Photon.Imago.Benchmarks -- --filter *Scenario*` prints every scenario with median and p95.
- [ ] Measure memory per scenario: peak working set, managed heap, tile cache bytes, and history bytes through `System.Diagnostics.Process` and `GC.GetGCMemoryInfo`, reported beside the times. Done when: each scenario row carries the four memory figures.
- [ ] Write `docs/dev/imago/performance.md`: the reference machine class (CPU, cores, RAM, disk, GPU), and the budget per scenario (open under 5 s, stroke latency under 16 ms, pan frame under 16 ms, Gaussian under 300 ms, save under 8 s, peak working set under the Performance page's RAM limit plus 500 MB, cold start under 2 s, warm start under 1 s), citing `standards/shared.md`. Done when: every scenario has a budget line.
- [ ] Commit the baseline `tests/Photon.Imago.Benchmarks/baselines/reference.json` (median of three runs per scenario, with the machine description and commit). Done when: the file lists every scenario and the gate reads it.
- [ ] Add `scripts/perf-gate.ps1`: runs the scenarios three times, fails when a scenario's median exceeds its budget or regresses more than 10 percent over the baseline median, and prints a table. Done when: the gate exits 0 on the baseline commit and exits 1 naming the scenario when a test build injects a 50 ms sleep into the composite loop.
- [ ] Add a `-Perf` switch to `scripts/check-all.ps1` that runs the gate, off by default because of its run time, and document it in `docs/dev/testing.md`. Done when: `pwsh scripts/check-all.ps1 -Perf` includes the gate's table and exit code.
- [ ] Profile every scenario over budget or in the top three by time with `dotnet-trace` and `dotnet-counters` (versions recorded) and record the top ten costs per scenario in `docs/dev/imago/performance.md`, naming which §19 and §20 fix. Done when: the page names at least three measured costs with their share of the scenario time.
- [ ] Commit: `"imago: the benchmark harness, the performance budget, and the perf gate"`

**Test checkpoint:** Driven run with evidence: `pwsh scripts/perf-gate.ps1` exits 0 on this commit with its per-scenario table quoted, and exits 1 naming the composite scenario on a build with an injected 50 ms sleep; `docs/dev/imago/performance.md` carries a budget for every scenario and the recorded top costs. Cheaper substitute that fails: timing one filter with a stopwatch in a unit test, which cannot fail on a paint or memory regression.

## 19. Performance II: Memory: Tile Cache, Compression, History, and Large-Document Open

§18 measures memory on the 100-megapixel, 50-layer document; this section fixes the measured memory costs so that document stays inside the RAM limit the `D03 T20 §5` Performance page sets. The tile cache, its scratch spill (`D03 T02 §1`), and the preference keys already exist; what is missing is compression of idle tiles, history that counts its bytes, lazy tile loading on open, and a proof on the whole document. Owns no catalog rows.

**Fidelity:** no surface of its own (engine and service changes; the refusal texts reuse the status strip and message dialogs).

- [ ] Record the top three memory costs from §18's profile in `docs/dev/imago/performance.md` with their bytes on the perf document. Done when: the page names them and this section's items each cite one.
- [ ] Add idle-tile compression in `src/Imago/Photon.Imago.Core/Tiles/TileCompressor.cs`: tiles untouched for `Imago.Performance.TileCompressAfterSeconds` (default 10) are compressed in memory with the built-in `System.IO.Compression.ZLibStream` at the fastest level and inflated on access. Done when: `TileCompressorTests` round-trip random, flat, and photographic tiles byte-exactly and the perf document's tile cache bytes drop by the measured factor quoted.
- [ ] Count bytes in every history record (`D03 T03 §2`) and enforce the `D03 T20 §5` undo memory limit by dropping the oldest states with one status-strip notice naming how many were dropped. Done when: `HistoryMemoryTests` exceed the limit by ten states and assert the oldest ten are gone, the notice text, and one Information line.
- [ ] Load layer tiles lazily on `.imago` open: map each layer's tile entries in the ZIP and decode a tile on first access, keeping thumbnails and the composite fallback for the first frame. Done when: `LazyOpenTests` open the perf document with fewer than 5 percent of its tiles decoded at first frame and render any tile on demand equal to an eager open.
- [ ] Pool large filter and composite buffers through `ArrayPool<T>.Shared` or the `D01 T03 §1` buffer pool and remove the top large-object-heap allocations the profile named. Done when: the §18 filter scenario's gen-2 collection count drops to the figure quoted and `GC.GetGCMemoryInfo` fragmentation is reported.
- [ ] Decide the GC configuration (workstation concurrent, `GCConserveMemory`, or dynamic adaptation) from measurements on the perf document and record it in `docs/dev/decisions.md` with the numbers. Done when: the row quotes peak working set and pause times for each option measured.
- [ ] Refuse a new or opened image that cannot fit in the RAM limit plus scratch space with a message naming the size and the limit, never an `OutOfMemoryException`. Done when: `LowMemoryTests` request a 300,000 by 300,000 image and assert the message and that the process stays up.
- [ ] Prove the whole-document memory budget: the perf document opened, painted, filtered, and saved keeps peak working set under the §18 budget with the RAM limit at 50 percent. Done when: `pwsh scripts/perf-gate.ps1` passes the memory rows and the figures are quoted.
- [ ] Refresh the §18 baseline and update `docs/dev/imago/performance.md` and `docs/user/imago/preferences.md` (what the memory settings now do). Done when: the baseline commit and both pages name the change.
- [ ] Commit: `"imago: idle-tile compression, history memory accounting, lazy open, and the memory budget"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~TileCompressorTests|FullyQualifiedName~HistoryMemoryTests|FullyQualifiedName~LazyOpenTests|FullyQualifiedName~LowMemoryTests"` exits 0, and `pwsh scripts/perf-gate.ps1` passes every memory row on the perf document with the peak working set quoted against its budget. Cheaper substitute that fails: raising the RAM limit default, which the 50 percent run of the gate rejects.

## 20. Performance III: SIMD Hot Paths, Parallel Compositing, and Cold Start

§18 names the CPU hot paths and the startup cost; this section vectorizes the measured hot paths with `System.Runtime.Intrinsics` and `System.Numerics.Tensors` (both part of .NET), composites tiles in parallel, and brings a cold start under two seconds with ReadyToRun and deferred startup work. WPF does not support IL trimming (Microsoft Learn, "Known trimming incompatibilities"), so startup trimming here means removing work from the startup path, not trimming assemblies. Owns no catalog rows.

**Fidelity:** no surface of its own (engine, build, and startup changes; the first frame is measured, not changed).

**Requires:** display-session -- cold and warm start are measured to the first idle frame of the main window

- [ ] Record the top three CPU hot paths from §18's profile in `docs/dev/imago/performance.md`. Done when: the page names them and the items below each cite one.
- [ ] Vectorize the blend-mode inner loops in `src/Imago/Photon.Imago.Rendering/Blending/` with `Vector128` and `Vector256` paths (AVX2, SSE4.1, and Arm64 AdvSimd through the cross-platform APIs) beside the scalar reference. Done when: `BlendSimdTests` (on the `D01 T03 §1` property suite) assert SIMD equals scalar for every blend mode and the composite scenario's median improves by the figure quoted.
- [ ] Vectorize the remaining named hot paths (premultiply and format conversion, and whichever filter §18 named) the same way, each with a scalar reference test. Done when: each path's SIMD-equals-scalar test passes and its scenario time is quoted before and after.
- [ ] Composite dirty tiles in parallel with a bounded `Parallel.ForEach` honoring `Imago.Performance.WorkerThreads`, keeping render order within a tile. Done when: `ParallelCompositeTests` render the perf document identically with 1 and 8 workers and the pan frame time is quoted.
- [ ] Add startup marks (process start, composition root built, main window shown, first idle) logged at Debug through Serilog, and enable multicore JIT with `ProfileOptimization.SetProfileRoot` and `StartProfile`. Done when: a driven start prints the four marks and the profile file exists after the second start.
- [ ] Defer work off the startup path: panels not visible build on first show, the font catalog warms on a background task, plug-in and module scans (`D03 T14 §11`, `D03 T14 §12`) start after first idle, and recent-file thumbnails load asynchronously. Done when: the startup marks show first idle before each deferred task logs its start.
- [ ] Publish Imago with `PublishReadyToRun` for `win-x64` and `win-arm64` in the publish profile, record the size and start-time trade in `docs/dev/decisions.md`, and state there that WPF IL trimming is not used. Done when: the installer build carries ReadyToRun images and the decision row quotes both measurements.
- [ ] Gate cold and warm start: warm start under 1 s in `scripts/perf-gate.ps1`, and cold start under 2 s measured as the first launch after a reboot of the reference machine, five runs, quoted in `docs/dev/imago/performance.md`. Done when: the gate passes the warm row and the five cold figures are quoted under 2 s.
- [ ] Refresh the §18 baseline with the improved figures and update `docs/dev/imago/performance.md`. Done when: the baseline commit names this section.
- [ ] Commit: `"imago: SIMD hot paths, parallel compositing, ReadyToRun, and a fast cold start"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ParallelCompositeTests|FullyQualifiedName~BlendSimdTests"` exits 0 with every SIMD path equal to its scalar reference, `pwsh scripts/perf-gate.ps1` passes including the warm-start row, and five post-reboot cold starts are quoted under 2 s. Cheaper substitute that fails: enabling ReadyToRun alone, which the recorded hot-path scenario times do not move.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] No "Planned" menu item remains in Imago
- [ ] Every new format has a fidelity fixture
- [ ] `python scripts/todo-graph.py validate` clean
