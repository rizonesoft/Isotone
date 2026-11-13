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
> **Current state (verified 2026-11-13):** §1 is built: `isotone::ui::Window` (`native/ui/src/window.cpp`) with the DIP types of `dpi.h`, the shared `native/ui/app.manifest`, and the foundation test host under `native/tests/foundation-host/` with its `smoke` and `lifecycle` scenarios. No renderer and no title bar exist yet (§2, §3).
<!-- claim: exists native/core/CMakeLists.txt -->
<!-- claim: exists native/tests/foundation-host/run_host.cmake -->
<!-- claim: exists native/ui/src/window.cpp -->
<!-- claim: exists native/ui/app.manifest -->
<!-- claim: absent native/ui/src/renderer.cpp -->
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
|   1   |   §1    | The window, DPI layout, and the foundation test host | D00 T07 §3, D01 T14 §1, D01 T27 §2 |  [x]   |
|   2   |   §2    | The renderer: device, visuals, flip-sequential swap chains, and partial redraw | §1 |  [ ]   |
|   3   |   §3    | The Isotone title bar with the menu bar, and snap layouts | §2 |  [ ]   |

---

## 1. The Window, DPI Layout, and the Foundation Test Host

> **Started:** 2026-11-13T17:02:47Z

Every foundation proves itself in one host, so the host and its report format come first, with the window they live in.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a window class and a test host with placeholder content.
**Needs:** Windows host (build/test)

**Corrected 2026-11-13** (pre-build validation, each fact measured that day): (1) **Headers.** The items name only `window.cpp`; the public headers are `native/ui/include/isotone/ui/window.h` and `dpi.h`. (2) **The manifest** is the executable's, not the library's: one shared `native/ui/app.manifest` (per-monitor DPI awareness v2, the Windows 10 and 11 `supportedOS` ids, `asInvoker`, long paths) that every app and the host embed; the smoke report records the awareness context the window actually runs under, so the manifest is proved by the run, not by its text. (3) **The rounding rule** is stated: a DIP edge becomes the physical pixel `floor(dip * dpi / 96 + 0.5)`, and a rectangle converts by its edges, never by its width, so two rectangles that share an edge in DIPs share it in pixels at every scale; the test proves both. (4) **`WM_DPICHANGED` without a second monitor**: `Window.DpiChangeTakesTheSuggestedRectangle` sends the message to a hidden window with a suggested rectangle and a new DPI and reads both back. (5) **The host** is a development-only console program (its failures print where CTest reads them); its placeholder menu bar is a Win32 menu and its two placeholder panels are filled with GDI from `Theme` colors until §2's renderer and §3's title bar replace them, and each menu command writes one log line; it keeps its log and settings under `--data-root <folder>` (required: a test never writes the user's real app-data folder) through `isotone::core`. (6) **No window flashes on the desktop**: the smoke scenario creates its window hidden, which gives the same DPI and client size; a later scenario that must be visible says so. (7) **Exit codes**: 0 pass, 1 fail, 2 a usage error (an unknown scenario, a report that cannot be written), and 77 when no window can be created at all, which CTest reads as skipped (`SKIP_RETURN_CODE`): that is the item's "marked to need a display session". (8) **The report** is one JSON object written through `isotone::core::AtomicFile`: `schema_version`, `scenario`, `result` (`pass`, `fail`, or `no-display`), `failures` (one sentence each), `measurements`, and `build_id`. (9) `USER32.dll` and `GDI32.dll` join `native/system-dlls.txt` with their reasons.

**Added 2026-11-13** (plan review, D01-T15-S1-PR1 to PR5): (1) a window that cannot be created is a skip only when the display session is positively absent (the process's window station is not the visible one); on a working display it is a failure, exit 1, naming the call that failed. Both classifications are tested: the rule as a function, and a forced creation failure through the host's `--fail-window` test switch. (2) The smoke scenario proves the placeholders, not only the measurements: it finds the four menus and their eight commands, invokes each command through the window's own message path and finds its log event, renders the client area to a memory surface (`WM_PRINTCLIENT`) and finds each panel filled with its token's color, and requires the window's DPI awareness to be per-monitor v2. (3) The window's life is proved: the `lifecycle` scenario shows the window without activating it, placed off every monitor so nothing appears on the desktop, pumps its message loop, resizes it and finds the panels laid out again and repainted, closes it, and finds it destroyed and the loop ended; run with no `--scenario`, the host is that same window on screen until the user closes it. (4) Every invocation names `--data-root`, in the items, the checkpoint, and CTest, and its absence is refused, exit 2, before any log or setting is opened. (5) The report and the refusals are tested by behavior: each CTest entry runs the host through `native/tests/foundation-host/run_host.cmake`, which checks the exit code, parses the report, and checks its fields against the exit code; an unknown scenario, a report that cannot be written, and a missing `--data-root` each exit 2 with a sentence on the console that names the problem.

**Corrected 2026-11-13** (while building): the `lifecycle` window is kept off the desktop by being fully transparent, not activated, and without a taskbar button (`Window::Options::quiet`: `WS_EX_LAYERED` at alpha 0 with `WS_EX_NOACTIVATE` and `WS_EX_TOOLWINDOW`), not by being placed off every monitor as the plan-review note (3) said: the scenario must find the window painted, and a window with no part on a monitor is never painted (measured that day with a probe window: 0 paint messages off every monitor across a show and a resize, against one on show and one more on resize for the transparent window). The promise is unchanged: nothing appears on the desktop, and the window is shown, painted, resized, repainted, closed, and destroyed.

- [x] Add `isotone::ui::Window` in `native/ui/src/window.cpp`: a Win32 window class, per-monitor DPI awareness v2 set in the manifest, `WM_DPICHANGED` handled with the suggested rectangle, and a `Dip` type whose conversion to physical pixels rounds by one rule at every scale. Done when: `Dpi.RoundTripAtEveryScale` covers 100, 125, 150, 175, 200, 250, and 300 percent and no layout edge moves by more than the contract's 1 DIP; `Dpi.SharedEdgesStayShared` and `Window.DpiChangeTakesTheSuggestedRectangle` pass. Done 2026-11-13: `native/ui/include/isotone/ui/dpi.h` (`Dip`, `DipSize`, `DipRect`, `PixelRect`, `to_pixels`, `to_dips`, `scale_percent`), `window.h` and `src/window.cpp` (`Window`, `Message`, `DpiAwareness`, `resize_client` so a menu bar added after creation does not eat into the client size), and `native/ui/app.manifest`. Tests added: `Dpi.RoundTripAtEveryScale`, `Dpi.HalvesRoundUpOnBothSidesOfZero`, `Dpi.OneRuleAtEveryScale`, `Dpi.SharedEdgesStayShared`, `Window.ClientAreaIsTheSizeAskedFor`, `Window.DpiIsKnownWhileTheWindowIsBeingCreated` (the window tests embed the manifest, so it reads the monitor's DPI; it fails with 96 against 144 when the DPI is read only after creation), `Window.ResizeClientGivesTheSizeAskedForUnderAMenu`, `Window.DpiChangeTakesTheSuggestedRectangle`, `Window.HandlerAnswersAndItsExceptionsStayInside`, `Window.CloseDestroysTheWindowAndEndsTheLoop`, `Window.DestructionDestroysTheHandle`. A converted edge moves at most half a physical pixel, which is at most 0.5 DIP at 100 percent and above. Review round 1 added `Window.AHandlerThatAnswersTheLastMessagesCannotKeepTheWindowAlive` and `Window.AHandlerThatAnswersTheDpiChangeStillLeavesTheNewDpi`: the window takes its new DPI, the end of its loop, and the loss of its handle from a message whether or not the handler answered it.
- [x] Add `native/tests/foundation-host/` building `foundation-host.exe` from `isotone::ui`, with a placeholder menu bar (File, Edit, View, Help, each with two commands) and two placeholder panels, and a `--scenario <name>` switch with `--report <path>` that writes one JSON object (scenario, result, measurements, and the build id) and exits 0 on success and 1 on failure. Done when: `foundation-host --scenario smoke --data-root <folder> --report <path>` writes the report with the window's DPI and client size, the four menus and eight commands found and each command's log event, both panels' colors as painted, and per-monitor v2 awareness; and `--scenario lifecycle` reports the resize, the repaint, the close, and the destroyed window. Done 2026-11-13: `host.h`, `host.cpp`, `main.cpp`, `CMakeLists.txt`; `foundation-host --scenario smoke --data-root build/foundation/data --report build/foundation/smoke.json` exited 0 on the development machine with `result: pass`, `dpi: 144`, `scale_percent: 150`, `dpi_awareness: per-monitor-v2`, client 1440 x 900 px (960 x 600 DIP), 4 menus and 8 commands each logged when invoked, and panels painted `#323232` (left, `surface-panel`) and `#2b2b2b` (right, `surface-tabstrip`) as their tokens give; `lifecycle` reported `paints: 2`, `loop_exit_code: 0`, `destroyed: true` after the resize (to a 1080 x 720 px client area at 150 percent on the final code).
- [x] Register the host with CTest through `run_host.cmake` as `foundation.smoke` and `foundation.lifecycle`, run headless where the session allows and marked to need a display session otherwise, with the refusal entries `foundation.unknown-scenario`, `foundation.unwritable-report`, `foundation.missing-data-root`, and `foundation.window-failure`. Done when: `ctest --test-dir artifacts/native/x64-debug -R "^foundation\."` passes in a display session, each entry checking the exit code and the parsed report, and `HostDisplay.OnlyAnAbsentSessionIsASkip` passes. Done 2026-11-13: six `foundation.*` entries with `SKIP_RETURN_CODE 77`, all passing in the display session (`ctest --test-dir artifacts/native/x64-debug`: 100% tests passed, 0 failed out of 102); `foundation_host_tests` adds `HostDisplay.OnlyAnAbsentSessionIsASkip`, `HostArguments.EverySwitchIsRead`, `HostArguments.UnusableArgumentsAreNamed`, `HostScenarios.AreListedInOrder`; the host's own failure path uses the tested rule (`exit_code_without_window`). Review round 1 added a seventh entry, `foundation.unusable-data-root`: a data root the log and settings cannot be kept under is a failing report, exit 1 (`x64-debug` 106/106 and `x64-asan` 107/107 on that tree). Two CI repairs followed, both in the host's tests and neither in the window: the `lifecycle` scenario resizes the client area smaller (720 x 480 DIP) and names its numbers on failure, because a runner's desktop held the grown window to its own size; and each entry's scratch folder is `run-<case>` directly in the binary folder, as `scripts/run-arm64-tests.ps1` requires. On the final code `6d16e6c813b9`: `x64-debug` 106/106, `x64-asan` 107/107, plan-gates success https://github.com/rizonesoft/Isotone/actions/runs/43487282095, build success (x64 and ARM64 presets and the ARM64 test job) https://github.com/rizonesoft/Isotone/actions/runs/43487282353.
- [x] Document the host and its report schema in `native/tests/foundation-host/README.md`. Done when: the README names every field and how a foundation adds a scenario. Done 2026-11-13: the README gives the switches, the exit codes, both scenarios, every report field and each scenario's measurements, the six CTest entries, and the four steps to add a scenario; `native/README.md`, `docs/dev/architecture.md`, `README.md`, and `AGENTS.md` now name the window and the host.
- [x] Commit: `"ui: a per-monitor-DPI window and the foundation test host"`

**Test checkpoint:** Unit test and driven run with evidence: `Dpi.RoundTripAtEveryScale`, `Dpi.SharedEdgesStayShared`, and `Window.DpiChangeTakesTheSuggestedRectangle` pass through CTest on every preset; `foundation-host --scenario smoke --data-root build/foundation/data --report build/foundation/smoke.json` exits 0 and its report gives the DPI, the client size, the menus and commands, the panel colors, and the awareness (quoted); `ctest -R "^foundation\."` passes its six entries; `HostDisplay.OnlyAnAbsentSessionIsASkip` passes. Cheaper substitute that fails: a per-foundation sample app, which multiplies window code and makes every proof run in a different window.

> **Verified:** 2026-11-13 | §1 | 04fd25cdb6da150b07c6dcd48179e838d71d1fc1
> **Review:** `docs/reviews/d01-t15-s1.json`

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
