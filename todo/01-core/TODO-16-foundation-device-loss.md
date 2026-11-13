---
schema_version: 1
id: foundation-device-loss
domain: 01-core
status: draft
title: "TODO-16 -- Foundation: Device-Loss Recovery and the WARP Fallback"
depends_on: []
frozen: false
track: F3
---

# TODO-16 -- Foundation: Device-Loss Recovery and the WARP Fallback

> **Goal:** a GPU device that is removed or reset, or a Direct2D target that must be recreated, costs the user nothing: the renderer rebuilds every GPU object from CPU-side state and redraws, the documents stay intact, and a machine whose hardware cannot start the renderer runs on the WARP software device with a notice.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** The renderer is built in `D01 T15 §2`; nothing yet handles `DXGI_ERROR_DEVICE_REMOVED`, `DXGI_ERROR_DEVICE_RESET`, or `D2DERR_RECREATE_TARGET`, and no code selects WARP.
<!-- claim: absent native/ui/src/renderer.cpp -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Device loss" -- the signals, the rebuild, the WARP fallback, and the three proofs (forced removal, an injected `D2DERR_RECREATE_TARGET`, and a start on WARP with the hardware adapter hidden)
- -> XREF: D01 T15 §2 -- the renderer whose resources this file rebuilds
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T25 §1 -- the goldens render on the WARP device this file selects

## Outcome

- Every GPU resource is owned by a renderer that can rebuild it from CPU-side state, and a removed or reset device, or a recreate-target signal, rebuilds and redraws without losing a document.
- With the hardware adapter unusable, the app starts on WARP and says so once.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (no tunable value: recovery is automatic); reporting=not-applicable (no data to summarize); notifications=applicable @ D01 T16 §2; permissions=not-applicable (writes no user file); audit=applicable @ D01 T16 §1; exchange=not-applicable (no files); reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** The user is told once when the app runs on WARP (§2), and every device loss and rebuild writes a log line (§1) so a support report shows what the GPU did.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Rebuild on device removal, reset, and recreate-target | D00 T07 §3, D01 T15 §2 |  [ ]   |
|   2   |   §2    | The WARP fallback with a notice | §1 |  [ ]   |

---

## 1. Rebuild on Device Removal, Reset, and Recreate-Target

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the renderer's recovery mechanism.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Device loss" (the proof removes a real device under a live window)

Each device loss writes one line to the audit log with the removal reason and the time the rebuild took.

- [ ] Make every GPU object (device, Direct2D device and context, DirectComposition device and visuals, swap chains, bitmaps, brushes, text layouts' device resources) owned by `isotone::ui::Renderer` and recreatable from CPU-side descriptions, with no document data held only in video memory. Done when: `Renderer.EveryResourceHasACpuSource` enumerates the renderer's resource registry and finds a source for each.
- [ ] Detect `DXGI_ERROR_DEVICE_REMOVED` and `DXGI_ERROR_DEVICE_RESET` from a present or any device call, and `D2DERR_RECREATE_TARGET` from `EndDraw` or `Flush`, then release, recreate, and redraw, logging the reason (`GetDeviceRemovedReason`) and the time the rebuild took. Done when: `Renderer.RebuildsAfterInjectedRemoval` and `Renderer.RecreatesTargetAfterInjectedSignal` pass through a test hook that returns each code once.
- [ ] Add the host scenario `device-loss` that draws known content, forces a removal (the Direct3D debug layer's device removal where available, else `dxcap -forcetdr`, recording which), waits for the rebuild, and compares the redrawn frame with the frame before. Done when: the report gives the forcing method, the rebuild time, and an identical frame.
- [ ] Commit: `"ui: rebuild every GPU resource after device loss"`

**Test checkpoint:** Unit test and driven run with evidence: `Renderer.EveryResourceHasACpuSource`, `Renderer.RebuildsAfterInjectedRemoval`, and `Renderer.RecreatesTargetAfterInjectedSignal` pass through CTest; `foundation-host --scenario device-loss --report build/foundation/device-loss.json` exits 0 with the forcing method, the rebuild time, and the frames before and after equal, and the log line for the loss is quoted. Cheaper substitute that fails: restarting the app on device loss, which loses unsaved work and is what the spec forbids.

## 2. The WARP Fallback with a Notice

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- adapter selection; the notice is a placeholder toast in the host, the product toast is the UI library's.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Device loss" (start on WARP with the hardware adapter hidden)

The WARP notice is this file's one user notification: the host can show it while the software device draws and clears itself when the hardware device returns.

- [ ] When creating the hardware device fails, or a test switch hides the hardware adapter, create the device on `D3D_DRIVER_TYPE_WARP` and continue, logging the failure and the fallback. Done when: `Renderer.FallsBackToWarp` passes with the hardware path forced to fail.
- [ ] Show one notice per session that the app is drawing in software and may be slower, with the reason, and never again in that session. Done when: the host scenario reports the notice shown once.
- [ ] Add the host scenario `warp-start` that starts with the hardware adapter hidden, draws, and runs the `partial-redraw` checks on WARP. Done when: the report names the WARP adapter and `mismatched_frames: 0`.
- [ ] Commit: `"ui: start on WARP when the hardware cannot, with one notice"`

**Test checkpoint:** Unit test and driven run with evidence: `Renderer.FallsBackToWarp` passes through CTest; `foundation-host --scenario warp-start --report build/foundation/warp-start.json` exits 0 naming the WARP adapter, the notice shown once, and `mismatched_frames: 0` (quoted). Cheaper substitute that fails: refusing to start without a GPU, which strands a user on a remote desktop or a virtual machine.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Renderer.*` recovery cases reporting through CTest
- [ ] The `device-loss` and `warp-start` host scenarios pass on the reference machine
- [ ] `python scripts/todo-graph.py validate` clean
