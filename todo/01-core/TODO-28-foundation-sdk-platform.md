---
schema_version: 1
id: foundation-sdk-platform
domain: 01-core
status: draft
title: "TODO-28 -- Foundation: isotone::core and isotone::ui on Impossible SDK, the CPU Path Rule, and the Canvas Frame Benchmark"
depends_on: []
track: F15
---

# TODO-28 -- Foundation: isotone::core and isotone::ui on Impossible SDK, the CPU Path Rule, and the Canvas Frame Benchmark

> **Goal:** `isotone::core` and `isotone::ui` call the operating system only through Impossible SDK, so the same source runs on Windows now and on Impossible OS later: the shipped `isotone::core` services and the shipped `Window` move off direct Windows calls onto the SDK's `base` and `window` parts with their tests and pixels unchanged and their timings no worse; every GPU feature keeps a CPU path that a registry and a check enforce; and the canvas target of `docs/parity/gesso-section-design.md` (panning a 100-megapixel document at a 37-degree view rotation, median frame under 16 ms) is judged by a frame benchmark measured through presentation, which the present `native/benchmarks` (pixel premultiplication only) cannot do.

> [!IMPORTANT]
> **Current state (verified 2026-11-27):** The owner decided on 2026-11-27 that Isotone is built on Impossible SDK (`docs/dev/decisions.md`, "2026-11-27: Isotone is built on Impossible SDK, as an Impossible OS app"). `isotone::core` (`native/core/src/atomic_file.cpp`, `app_paths.cpp`, `log.cpp`, `settings.cpp`, `utf.cpp`) and `isotone::ui::Window` (`native/ui/src/window.cpp`) include `<windows.h>` and call Windows directly, `window.h` hands out an `HWND`, and `isotone::core::Error` carries a Win32 error or HRESULT. No Direct2D, DirectWrite, or Direct3D code exists yet, so the renderer, text, and canvas are not moved but planned on the SDK from the start, in the open sections each foundation file revises (`D01 T15 §2`, `D01 T21`, `D01 T24`, `D01 T25`). `native/benchmarks` holds only the pixel premultiplication benchmark.
<!-- claim: exists native/ui/src/window.cpp -->
<!-- claim: exists native/core/src/atomic_file.cpp -->
<!-- claim: exists native/benchmarks/main.cpp -->
<!-- claim: absent native/benchmarks/frame -->

## Inputs

- `docs/specs/2026-11-27-sdk-as-platform-design.md` in the Impossible SDK repository, "What is the shape?", "How is a move judged?", and "In what order?" -- the SDK calls an app may use, the rule that pixels and timings are compared separately on the same machine, and that a CPU screen needs only `window`, `draw`, `text`, and the C++ support while only a GPU surface waits for the `gpu` tier
- [`docs/dev/decisions.md`](../../docs/dev/decisions.md) "2026-11-27: Isotone is built on Impossible SDK, as an Impossible OS app" -- the decision this file builds on
- [`docs/parity/gesso-section-design.md`](../../docs/parity/gesso-section-design.md), the view section's budget -- the canvas target the frame benchmark judges
- [`docs/dev/reference-machine.md`](../../docs/dev/reference-machine.md) -- the machine every measurement here is taken on
- Impossible SDK repository, by topic: the C++ support part with its sample, the opaque window object, the `window` part's presentation timing and test-only accessors, the `base` part's files, atomic replace, known folders, time, and threads, the `gpu` tier with its CPU-path rule and device-loss status, and the boundary checks. A feature Isotone needs that the SDK lacks is built there first by Isotone's session, then `native/sdk.json` moves (`D00 T08 §1`); this file never copies SDK work.
- -> XREF: D00 T08 §2 -- the SDK-toolchain build and boundary checks every program moved here is held by
- The shipped window (`D01 T15 §1`) and test host whose Windows calls §1 moves
- -> XREF: D01 T15 §2 -- the renderer, planned on the SDK's `draw` part and present path
- The shipped app-data paths (`D01 T27 §1`) and logging whose Windows calls §1 moves
- The shipped atomic writes (`D01 T27 §2`) and settings store whose Windows calls §1 moves
- -> XREF: D01 T24 §1 -- the canvas, which registers its GPU and CPU paths under §2 and is measured by §3
- -> XREF: D01 T16 §2 -- the CPU path with its notice, which is the fallback §2's rule requires
- -> XREF: D03 T08 §3 -- the Gesso view section whose 100-megapixel pan budget §3 measures

## Outcome

- `native/core` and `native/ui` build under the `sdk-release` preset and contain no Windows header, and the `core` and `ui` tests, the host's panel pixels, and the window's timings are the same as before the move or better.
- A registry lists every GPU feature with its CPU path, and a check fails on a GPU feature that has none.
- A frame benchmark reports the median and the worst frame of the 100-megapixel pan at 37 degrees through presentation, on the CPU path and on the GPU path, and its pixels are compared separately.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (no tunable value: the move changes no setting and the budget is fixed); reporting=applicable @ D01 T28 §3; notifications=not-applicable (no long-running work a user starts); permissions=not-applicable (writes no user file); audit=not-applicable (no document edits); exchange=not-applicable (no files read or written for a user); reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** The frame benchmark's report (§3) is this file's one output a person reads. The move (§1) and the rule (§2) change what the code calls and what the gates refuse, and nothing a user sees, saves, or removes.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | isotone::core and the window on the SDK's base and window parts | D00 T08 §2, D01 T15 §1, D01 T27 §2 |  [ ]   |
|   2   |   §2    | The CPU path rule for every GPU feature | §1 |  [ ]   |
|   3   |   §3    | The canvas frame benchmark through presentation | §2, D01 T24 §1 |  [ ]   |

---

## 1. isotone::core and the Window on the SDK's Base and Window Parts

The shipped `isotone::core` services and `isotone::ui::Window` are the first code to move, and they are CPU screens: they need only the SDK's `base`, `window`, `draw`, and `text` parts and its C++ support, never the `gpu` tier. They are shipped sections (`D01 T27`, `D01 T15 §1`), so the move is new work here and edits none of them. It waits for the SDK repository to have what it uses (the C++ support with its sample, the opaque window object, and the boundary checks), and builds any missing `base` or `window` call there first. A move lands only when its pictures match and its timings are no worse, measured on the reference machine before and after, pixels and timings separately.

**Fidelity:** no surface of its own (non-feature infrastructure: the same window and services on a different platform seam, with no competitor-facing feature, so no `**Exceed:**` paragraph; the product sections that use it carry theirs).
**Needs:** Windows host (build/test)

- [ ] Record the before numbers from the MSVC build at the commit before the move, in `docs/dev/reference-machine.md` beside the machine: the SHA-256 of the client area of the foundation host's `smoke` scenario read back at 100 and 200 percent, and the median of 10 runs of window creation to first present. Done when: the file holds both with the commit and the build id.
- [ ] Move `isotone::core` (`native/core/src/atomic_file.cpp`, `app_paths.cpp`, `log.cpp`, `settings.cpp`, `utf.cpp`) onto the SDK's `base` calls for files, atomic replace, known folders, time, memory, and threads, keeping every public header and signature, and make `isotone::core::Error` carry the SDK's error code and the failing SDK call in place of a Win32 error or HRESULT. Done when: no file under `native/core` includes a Windows header, the existing `AtomicFile.*`, `Settings.*`, `Log.*`, `AppFolders.*`, and `Error.*` cases pass unchanged through CTest on `sdk-release` and on `x64-debug`, and `python scripts/sdk-boundary.py --check` lists `isotone_core`.
- [ ] Move `isotone::ui::Window` (`native/ui/src/window.cpp`) onto the SDK's `window` part: creation, per-monitor DPI and the DPI-change rectangle, input, and present, keeping `dpi.h` and the DIP rounding rule, and removing the native handle from `window.h` (the `HWND` it hands out now). Done when: `Dpi.*` and `Window.*` pass on `sdk-release`, `window.h` names no Windows type, and `native/ui` includes no Windows header.
- [ ] Build the foundation host under `sdk-release` and list it in `native/sdk-programs.txt`: its `smoke` and `lifecycle` scenarios run from the SDK-built program, and a scenario that needs Windows-only instrumentation (the `WM_PRINTCLIENT` readback, the message-path menu invocation) uses the SDK's test-only accessors in the test build path, or stays in a tools-only MSVC build of the host that does not ship. Done when: `ctest -R "^foundation\."` passes against the SDK-built host and `python scripts/sdk-boundary.py --check` lists `foundation-host` and passes.
- [ ] Record the after numbers beside the before numbers and compare them: the client-area hash equal at both scales, and the median creation-to-first-present time no worse than the before median. Done when: the file holds both with the new build id, and a hash difference or a slower median fails `python scripts/sdk-move-compare.py` (a stdlib script that reads the two records), whose test `scripts/tests/test_sdk_move_compare.py` passes with an equal, a different-hash, and a slower record.
- [ ] Commit: `"core: isotone::core and the window call the OS only through the SDK"`

**Test checkpoint:** Unit test and driven run with evidence: the `AtomicFile.*`, `Settings.*`, `Log.*`, `Dpi.*`, and `Window.*` cases pass through `ctest --preset sdk-release` and `ctest --preset x64-debug`; `foundation-host --scenario smoke --data-root build/foundation/data --report build/foundation/smoke.json` exits 0 from the SDK-built host with the client-area hash equal to the before record; `python scripts/sdk-move-compare.py` exits 0 (all quoted, with the machine). Cheaper substitute that fails: a wrapper that forwards each `isotone::core` call to the Windows function it replaced inside the library, which keeps the Windows header the SDK's source check refuses.

## 2. The CPU Path Rule for Every GPU Feature

The SDK's `gpu` tier has one rule: every GPU feature has a CPU path, so a machine with no Direct3D 11 still starts the program. Isotone holds the same rule for its own features with a registry and a check, because a GPU-only feature is a defect on a machine without one, and on Impossible OS until it has Direct3D 11. This section builds the rule; it needs no GPU and runs on the CPU path alone.

**Fidelity:** no surface of its own (non-feature infrastructure: a registry and a check, with no competitor-facing feature, so no `**Exceed:**` paragraph; the product sections that use it carry theirs).
**Needs:** Windows host (build/test)

- [ ] Add `native/gpu-features.txt`, one line per GPU feature: its name, the target that calls the SDK's `gpu` part for it, and the test that draws the same result on the CPU path. The first entry is the canvas (`isotone::ui::Canvas`, registered by `D01 T24 §1`). Done when: the file exists with the canvas entry and a header comment naming the rule.
- [ ] Add `scripts/gpu-feature-check.py` (stdlib only) that finds every first-party source calling an SDK `gpu` function and fails, naming the file, when its target is not in `native/gpu-features.txt` or its CPU-path test is not a registered CTest case; wire it into `scripts/check-all.ps1` as the `gpu-paths` stage. Done when: `scripts/tests/test_gpu_feature_check.py` passes with a registered feature, a source calling `gpu` from an unregistered target (exit 1), and a registered feature whose CPU-path test does not exist (exit 1), and `python scripts/gpu-feature-check.py` exits 0 on the tree.
- [ ] State the rule in `standards/shared.md` and `standards/gesso.md`: a GPU path is an acceleration of a CPU path that gives the same pixels within the app's tolerance, never the only path. Done when: both name `native/gpu-features.txt` and the check.
- [ ] Commit: `"ui: every GPU feature registers the CPU path that gives the same pixels"`

**Test checkpoint:** Unit test and static analysis: `python scripts/tests/test_gpu_feature_check.py` passes with its three cases, `python scripts/gpu-feature-check.py` exits 0 on the tree and exits 1 naming the file on the unregistered case (all quoted), and `pwsh scripts/check-all.ps1` lists the `gpu-paths` stage. Cheaper substitute that fails: a comment in the canvas source saying a CPU path exists, which no gate reads.

## 3. The Canvas Frame Benchmark through Presentation

The canvas target is a frame time a user sees, so it is measured at presentation, not in the renderer, and pixels and timings are judged separately. The present `native/benchmarks` time only pixel premultiplication and cannot judge a canvas move; this benchmark is the missing one. The SDK's window part has to expose how long a presented frame took to appear (its presentation timing); if it lacks that, the SDK repository gets it first, and PresentMon over the same run is the cross-check the stack design's protocol already uses.

**Waits for:** the SDK's `gpu` tier for the GPU path only; the CPU path is measured first and needs only the `window`, `draw`, and `text` parts.

**Fidelity:** no surface of its own (non-feature infrastructure: a benchmark, with no competitor-facing feature, so no `**Exceed:**` paragraph; `D03 T08 §3` carries the Gesso budget this measures).
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "The goals" (displayed-frame times come from presentation of a live display, not from renderer timings)

- [ ] Add `native/benchmarks/frame/` (a program under the `sdk-release` preset, listed in `native/sdk-programs.txt`) that builds a synthetic tiled 100-megapixel document with a fixed seed, pans it for 60 s along a fixed path at a 37-degree view rotation in an SDK window, and records each frame's presentation time and the median, the 95th percentile, and the worst frame, to a `--report` JSON with the build id and the machine. Done when: `frame-bench --path cpu --report build/benchmarks/frame-cpu.json` exits 0 with the three figures and 3,600 or more frames.
- [ ] Add `--path gpu`, which pans the same document on the `gpu` tier through `isotone::ui::Canvas`, and `--pixels`, which reads back the presented frame at 10 fixed points of the path on each path and compares them within the canvas tolerance of `D01 T24 §1`. Done when: the pixel comparison and the timings are separate fields of the report, and the report names the CPU and GPU paths and whether the GPU path was available.
- [ ] Record the CPU and GPU results beside the machine in `docs/dev/reference-machine.md` with the date and build id, and state in `native/README.md` that `native/benchmarks` (premultiplication) cannot judge a canvas move and `native/benchmarks/frame` can. Done when: both files say so and the results file holds both paths.
- [ ] Judge the target: the median frame under 16 ms on the path the app ships as its default for the machine, each result quoted with the machine, and the work the CPU cannot do within the target moved to the GPU path under §2's rule. Done when: the report's verdict field reads pass for the default path, or a decision entry in `docs/dev/decisions.md` names the miss and what moves to the GPU path.
- [ ] Commit: `"benchmarks: the canvas frame benchmark through presentation"`

**Test checkpoint:** Driven run with evidence: `frame-bench --path cpu --report build/benchmarks/frame-cpu.json` and `frame-bench --path gpu --report build/benchmarks/frame-gpu.json` exit 0 on the reference machine with the median, the 95th percentile, and the worst frame, the pixel comparison, and the verdict (quoted, with the machine and the display's refresh rate). Cheaper substitute that fails: renderer timings, which say when a frame was drawn and not when the user saw it, and the premultiplication benchmark, which times neither a frame nor a pan.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with the `gpu-paths` stage among its gates
- [ ] `cmake --workflow --preset sdk-release` exits 0 and `python scripts/sdk-boundary.py --check` lists `isotone_core`, `isotone_ui`, `foundation-host`, and `frame-bench`
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-artifact-gate.py --policy shipping --require-built'` exits 0
- [ ] `python scripts/sdk-move-compare.py` exits 0 and the frame benchmark's CPU and GPU reports are recorded in `docs/dev/reference-machine.md`
- [ ] `python scripts/todo-graph.py validate` clean
