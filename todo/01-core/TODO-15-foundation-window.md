---
schema_version: 1
id: foundation-window
domain: 01-core
status: draft
title: "TODO-15 -- Foundation: a Window with the Isotone Title Bar on the Swap Chain and Partial-Redraw Contract"
depends_on: []
frozen: false
track: F2
---

# TODO-15 -- Foundation: a Window with the Isotone Title Bar on the Swap Chain and Partial-Redraw Contract

> **Goal:** `isotone::ui` opens a per-monitor-DPI-aware Win32 window that draws through one Direct3D 11 device with Direct2D, DirectWrite, and DirectComposition, presents through a flip-sequential swap chain that redraws only what changed and still matches a full redraw in every frame, and carries the Isotone title bar with the menu bar inside it while Windows 11 snap layouts keep working; and the foundation test host every other foundation proves itself in exists.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No window code exists: `native/` holds `isotone::core`, the benchmark harness, and the tests, and `isotone::ui` starts in `D01 T14 §1` with the token tables. No test host exists under `native/tests/`.
<!-- claim: exists native/core/CMakeLists.txt -->
<!-- claim: absent native/tests/foundation-host -->
<!-- claim: exists docs/design/components/WindowChrome/README.md -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Windows and frames", "Rendering", "Swap chains and partial redraw", and "Threading and lifetimes" -- the device, the visuals, `DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL` with `Present1` dirty and scroll rectangles, per-buffer damage, the waitable swap chain with a maximum frame latency of 1
- [`docs/design/components/WindowChrome/README.md`](../../docs/design/components/WindowChrome/README.md) and [`docs/design/shell-layout.md`](../../docs/design/shell-layout.md) -- what the title bar and menu bar hold; this file proves the mechanism with placeholder content, and the product chrome is drawn by the UI library's sections
- -> XREF: D01 T14 §1 -- the library and the token tables the window draws with
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T16 §1 -- device loss rebuilds what this file's renderer owns
- -> XREF: D01 T22 §1 -- the UI Automation provider exposes this window's elements
- -> XREF: D01 T17 §1 -- the display color pipeline sets the format of this file's swap chains
- -> XREF: D01 T18 §2 -- the render thread takes over this file's draws and presents
- -> XREF: D01 T20 §2 -- right-to-left mirroring and mnemonics are proved on this file's menu bar
- -> XREF: D01 T21 §1 -- the text editing model draws through this file's renderer
- -> XREF: D01 T23 §1 -- floating panels use this file's window and frames
- -> XREF: D01 T19 §5 -- the recovery scenario runs in this file's foundation test host
- -> XREF: D01 T27 §2 -- the host logs and keeps its settings through the core services foundation
- -> XREF: D01 T01 §7 -- the shared window chrome of the UI library, re-planned by `D00 T07 §5`, builds the product title bar on this file's title bar mechanism

## Outcome

- `isotone::ui::Window` lays out in device-independent pixels rounded to physical pixels at every scale, and follows a move between monitors of different DPI.
- The renderer presents with dirty rectangles and per-buffer damage, and a scenario that alternates disjoint invalidations, scrolling, resizing, and occlusion matches a full redraw in every presented frame.
- The Isotone title bar extends the DWM frame, holds the menu bar, and answers hit testing so the maximize button shows Windows 11 snap layouts.
- `native/tests/foundation-host/` builds `foundation-host.exe` with placeholder menus and panels and a `--scenario <name> --report <file>` mode that every foundation uses.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (window placement is saved by the apps' workspace sections); reporting=applicable @ D01 T15 §1; notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=not-applicable (no document edits); exchange=not-applicable (no files read or written); reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** This is a mechanism with a test host. Its only report is the host's scenario report, which every foundation's proof reads; what a user sees and saves about windows (placement, the workspace) belongs to the apps and to the docking work that saves workspaces.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The window, DPI layout, and the foundation test host | D00 T07 §3, D01 T14 §1, D01 T27 §2 |  [ ]   |
|   2   |   §2    | The renderer: device, visuals, flip-sequential swap chains, and partial redraw | §1 |  [ ]   |
|   3   |   §3    | The Isotone title bar with the menu bar, and snap layouts | §2 |  [ ]   |

---

## 1. The Window, DPI Layout, and the Foundation Test Host

> **Started:** 2026-11-13T17:02:47Z

Every foundation proves itself in one host, so the host and its report format come first, with the window they live in.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a window class and a test host with placeholder content.
**Needs:** Windows host (build/test)

**Corrected 2026-11-13** (pre-build validation, each fact measured that day): (1) **Headers.** The items name only `window.cpp`; the public headers are `native/ui/include/isotone/ui/window.h` and `dpi.h`. (2) **The manifest** is the executable's, not the library's: one shared `native/ui/app.manifest` (per-monitor DPI awareness v2, the Windows 10 and 11 `supportedOS` ids, `asInvoker`, long paths) that every app and the host embed; the smoke report records the awareness context the window actually runs under, so the manifest is proved by the run, not by its text. (3) **The rounding rule** is stated: a DIP edge becomes the physical pixel `floor(dip * dpi / 96 + 0.5)`, and a rectangle converts by its edges, never by its width, so two rectangles that share an edge in DIPs share it in pixels at every scale; the test proves both. (4) **`WM_DPICHANGED` without a second monitor**: `Window.DpiChangeTakesTheSuggestedRectangle` sends the message to a hidden window with a suggested rectangle and a new DPI and reads both back. (5) **The host** is a development-only console program (its failures print where CTest reads them); its placeholder menu bar is a Win32 menu and its two placeholder panels are filled with GDI from `Theme` colors until §2's renderer and §3's title bar replace them, and each menu command writes one log line; it keeps its log and settings under `--data-root <folder>` (required: a test never writes the user's real app-data folder) through `isotone::core`. (6) **No window flashes on the desktop**: the smoke scenario creates its window hidden, which gives the same DPI and client size; a later scenario that must be visible says so. (7) **Exit codes**: 0 pass, 1 fail, 2 a usage error (an unknown scenario, a report that cannot be written), and 77 when no window can be created at all, which CTest reads as skipped (`SKIP_RETURN_CODE`): that is the item's "marked to need a display session". (8) **The report** is one JSON object written through `isotone::core::AtomicFile`: `schema_version`, `scenario`, `result` (`pass`, `fail`, or `no-display`), `failures` (one sentence each), `measurements`, and `build_id`. (9) `USER32.dll` and `GDI32.dll` join `native/system-dlls.txt` with their reasons.

- [ ] Add `isotone::ui::Window` in `native/ui/src/window.cpp`: a Win32 window class, per-monitor DPI awareness v2 set in the manifest, `WM_DPICHANGED` handled with the suggested rectangle, and a `Dip` type whose conversion to physical pixels rounds by one rule at every scale. Done when: `Dpi.RoundTripAtEveryScale` covers 100, 125, 150, 175, 200, 250, and 300 percent and no layout edge moves by more than the contract's 1 DIP; `Dpi.SharedEdgesStayShared` and `Window.DpiChangeTakesTheSuggestedRectangle` pass.
- [ ] Add `native/tests/foundation-host/` building `foundation-host.exe` from `isotone::ui`, with a placeholder menu bar (File, Edit, View, Help, each with two commands) and two placeholder panels, and a `--scenario <name>` switch with `--report <path>` that writes one JSON object (scenario, result, measurements, and the build id) and exits 0 on success and 1 on failure. Done when: `foundation-host --scenario smoke --report <path>` writes the report with the window's DPI and client size.
- [ ] Register the host with CTest as `foundation.smoke`, run headless where the session allows and marked to need a display session otherwise. Done when: `ctest --preset x64-debug -R foundation.smoke` passes in a display session.
- [ ] Document the host and its report schema in `native/tests/foundation-host/README.md`. Done when: the README names every field and how a foundation adds a scenario.
- [ ] Commit: `"ui: a per-monitor-DPI window and the foundation test host"`

**Test checkpoint:** Unit test and driven run with evidence: `Dpi.RoundTripAtEveryScale`, `Dpi.SharedEdgesStayShared`, and `Window.DpiChangeTakesTheSuggestedRectangle` pass through CTest on every preset; `foundation-host --scenario smoke --report build/foundation/smoke.json` exits 0 and its report gives the DPI and client size (quoted); `ctest -R foundation.smoke` passes. Cheaper substitute that fails: a per-foundation sample app, which multiplies window code and makes every proof run in a different window.

## 2. The Renderer: Device, Visuals, Flip-Sequential Swap Chains, and Partial Redraw

One Direct3D 11 device per process with Direct2D and DirectWrite over it; each window's interface is one DirectComposition visual with its own swap chain. Partial presentation is where flip-model renderers usually go wrong, because back buffers rotate, so the proof compares every frame with a full redraw.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the rendering mechanism, proved on the host's placeholder content.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Swap chains and partial redraw" (the proof presents to a real window)

- [ ] Add `isotone::ui::Renderer` in `native/ui/src/renderer.cpp`: one `ID3D11Device` with BGRA support per process, the Direct2D device and context over it (multithread-protected), the DirectWrite factory, and a DirectComposition device with one visual per window. Done when: `Renderer.OneDevicePerProcess` passes and the host reports the adapter it chose.
- [ ] Create each window's swap chain with `DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL` for composition, waitable, with `SetMaximumFrameLatency(1)`, and present with `Present1` dirty and scroll rectangles. Done when: the host's report records the swap chain description and the waitable object.
- [ ] Track damage per back buffer in `isotone::ui::DamageTracker`: each buffer's accumulated damage since it was last presented, and redraw the union. Done when: `DamageTracker.RotatingBuffersRedrawTheUnion` passes for two- and three-buffer chains with disjoint, overlapping, and scrolled damage.
- [ ] Add the host scenario `partial-redraw` that alternates disjoint invalidations, scrolling, resizing, and occlusion for at least 600 frames, reads back each presented frame, renders the same state with a full redraw offscreen, and counts the frames whose pixels differ. Done when: the report gives the frame count and `mismatched_frames: 0`, and a deliberate fault (a test switch that skips the union) makes it report mismatches.
- [ ] Commit: `"ui: the renderer with flip-sequential swap chains and per-buffer damage"`

**Test checkpoint:** Unit test and driven run with evidence: `Renderer.OneDevicePerProcess` and `DamageTracker.RotatingBuffersRedrawTheUnion` pass through CTest; `foundation-host --scenario partial-redraw --report build/foundation/partial-redraw.json` exits 0 with at least 600 frames and `mismatched_frames: 0`, and with the fault switch reports a nonzero count (both quoted). Cheaper substitute that fails: presenting the whole window every frame, which passes every picture test and misses the frame cadence the canvas foundation measures.

## 3. The Isotone Title Bar with the Menu Bar, and Snap Layouts

The title bar is drawn by us with the menu bar inside it, by extending the DWM frame into the client area; Windows 11 shows snap layouts only when hit testing reports the maximize button, so the proof is the hit-test map.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the frame and hit-testing mechanism with placeholder menus; the product chrome and its goldens are the UI library's window chrome sections.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Windows and frames" (snap layouts and the caption are a live window's)

- [ ] Extend the frame with `DwmExtendFrameIntoClientArea` and handle `WM_NCCALCSIZE` so the client area covers the title bar, keeping the system's resize borders. Done when: the host's report gives the frame margins and the resize border width at 100 and 200 percent.
- [ ] Answer `WM_NCHITTEST` with `HTCAPTION` over the title bar's free space, `HTMINBUTTON`, `HTMAXBUTTON`, and `HTCLOSE` over the caption buttons, `HTCLIENT` over the menu bar, and the border codes at the edges. Done when: `TitleBar.HitTestMap` passes over a grid of points at 100, 150, and 200 percent.
- [ ] Put the menu bar inside the title bar, opening on click and on `Alt` and its mnemonic letter, with keyboard navigation between menus. Done when: the host scenario `title-bar` reports each menu opened by its mnemonic through the window's own message path.
- [ ] Add the host scenario `title-bar` that records the hit-test map, the maximize button's `HTMAXBUTTON` region, and a maximize and restore round trip. Done when: the report lists every region and the round trip restores the window's rectangle.
- [ ] Commit: `"ui: the Isotone title bar with the menu bar and snap-layout hit testing"`

**Test checkpoint:** Unit test and driven run with evidence: `TitleBar.HitTestMap` passes through CTest; `foundation-host --scenario title-bar --report build/foundation/title-bar.json` exits 0 with the hit-test map, the `HTMAXBUTTON` region, the menus opened by mnemonic, and the maximize and restore round trip (quoted); a screenshot of the snap layouts flyout over the maximize button on Windows 11 is recorded in the run file. Cheaper substitute that fails: a borderless window with a fake caption, which loses snap layouts, the system menu, and Aero Snap.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Dpi.*`, `Renderer.*`, `DamageTracker.*`, and `TitleBar.*` cases reporting through CTest
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-artifact-gate.py --policy shipping --require-built'` exits 0
- [ ] The three host scenarios (`smoke`, `partial-redraw`, `title-bar`) pass on the reference machine and on an ARM64 machine
- [ ] `python scripts/todo-graph.py validate` clean
