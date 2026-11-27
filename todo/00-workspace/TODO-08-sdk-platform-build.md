---
schema_version: 1
id: sdk-platform-build
domain: 00-workspace
status: draft
title: "TODO-08 -- Impossible SDK as the Build Platform: the Pins, the SDK-Toolchain Release, and the Boundary Checks"
depends_on: []
track: W8
---

# TODO-08 -- Impossible SDK as the Build Platform: the Pins, the SDK-Toolchain Release, and the Boundary Checks

> **Goal:** Isotone is an Impossible OS app by construction: the repository pins the Impossible SDK it builds on in `sdk.json`, names each shipping program in an `app.json`, and builds its release with the SDK toolchain (clang, with libc++ from the SDK's `cxx` part) in CI, where the SDK's boundary checks (the link rule, the source check that allows no Windows, COM, or DirectX header outside the SDK, the exported-header check, and the import check on the finished executable) pass on every shipping program and fail on a planted violation. The MSVC build stays for developer tools and does not ship.

> [!IMPORTANT]
> **Current state (verified 2026-11-27):** The owner decided on 2026-11-27 that Isotone is built on Impossible SDK (`docs/dev/decisions.md`, "2026-11-27: Isotone is built on Impossible SDK, as an Impossible OS app"; the approved design record is `docs/specs/2026-11-27-sdk-as-platform-design.md` in the Impossible SDK repository). Nothing of it is built here: `native/` has `toolchain.json` (the MSVC pin) and no `sdk.json` or `app.json`, every shipping build is MSVC or clang-cl with the static runtime (`/MT`) under `D00 T05`, and `native/system-dlls.txt` lists the Windows system DLLs a shipping executable may import. The SDK's C++ runtime part, its boundary checks, and its arm64 Windows target are Impossible SDK repository work, not this file's.
<!-- claim: exists native/toolchain.json -->
<!-- claim: absent native/sdk.json -->
<!-- claim: exists native/system-dlls.txt -->

## Inputs

- `docs/specs/2026-11-27-sdk-as-platform-design.md` in the Impossible SDK repository, "How is the boundary checked?", "What does the SDK add?", "What does each repository do?", and "In what order?" -- the three boundary checks and the import check, the C++ support part, the rule that a shipping program links only objects built from source, and what Isotone does
- [`docs/dev/decisions.md`](../../docs/dev/decisions.md) "2026-11-27: Isotone is built on Impossible SDK, as an Impossible OS app" -- the decision this file builds
- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), the 2026-11-27 revision note at its head and "The toolchain" -- what the SDK route replaces for shipping builds
- [`native/toolchain.json`](../../native/toolchain.json) and [`scripts/dev-env.ps1`](../../scripts/dev-env.ps1) -- the pin whose shape `sdk.json` follows, and the MSVC environment that stays for tools
- [`.github/workflows/build.yml`](../../.github/workflows/build.yml) -- the workflow §2 adds the SDK job to
- The import and size gates (`D00 T05 §6`): the size gate keeps holding SDK-built programs, and the import gate's system-DLL list stays for the MSVC build
- CI for x64 and ARM64 (`D00 T05 §8`), which the SDK job joins
- -> XREF: D00 T05 §12 -- standard library hardening, which the SDK build repeats for libc++
- -> XREF: D01 T28 §1 -- moves `isotone::core` and the window onto the SDK, the first programs this file's checks hold
- -> XREF: D01 T28 §3 -- the canvas program, the one that links the SDK's `gpu` part and so declares the GPU tier in its `app.json`

## Outcome

- `native/sdk.json` pins the Impossible SDK commit and its toolchain, a check fails when the checkout differs, and every shipping program has an `app.json`.
- `cmake --workflow --preset sdk-release` builds the shipping programs with the SDK toolchain under the SDK's link rule, and the `sdk` job in CI runs the boundary checks and the import check on each.
- A planted Windows header, a planted direct Windows call, a planted prebuilt object, and a planted `void *` without a marker each fail the checks with their own diagnostic, and the tree passes.
- The libc++ runtime Isotone links is registered, hardened, and inside each app's 30 MB budget.

**Adjacency:** all=not-applicable (a pin, a build, and its checks: no records, settings, documents, or surfaces a user sees)

**Adjacency rationale:** Nothing here ships to a user as a feature. It changes how the shipping programs are built and what the build refuses, so every later surface section stands on a boundary that is checked rather than trusted.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The SDK pin, the app manifests, and the runtime register | -- |  [ ]   |
|   2   |   §2    | The SDK-toolchain release build and the boundary checks in CI | §1, D00 T05 §8 |  [ ]   |

---

## 1. The SDK Pin, the App Manifests, and the Runtime Register

Isotone builds on the Impossible SDK at a pinned commit and moves that pin only after the SDK repository has the feature Isotone needs. The pin, its check, and the per-program manifest come first so every later move names the SDK it was proved on. The schemas belong to the SDK (its app build and packaging section reads `app.json`); this section follows them and invents none.

**Fidelity:** no surface of its own (non-feature infrastructure: a pin, a manifest, and a register entry, with no competitor-facing feature, so no `**Exceed:**` paragraph).
**Needs:** Windows host (build/test)

- [ ] Add `native/sdk.json` pinning the Impossible SDK repository commit and the toolchain record it carries (its `toolchain.json`), in the shape of the SDK's own pin schema read from the pinned checkout. Done when: the file names a commit that exists in the SDK repository, and `python scripts/check-sdk-pin.py` exits 0 on it.
- [ ] Add `scripts/check-sdk-pin.py` (stdlib only) that reads `native/sdk.json`, finds the SDK checkout the build uses, and exits 1 naming the difference when its commit or toolchain record differs from the pin, and wire it into `scripts/check-all.ps1` as the `sdk-pin` stage. Done when: `scripts/tests/test_check_sdk_pin.py` passes with a matching checkout, a checkout one commit away, and a missing checkout (the last two exit 1 and name the pin).
- [ ] Add one `app.json` per shipping program, the first being `native/tests/foundation-host/app.json` and each app adding its own when it first ships: the program's identity, its version, and its declared tier (Desktop for a program of CPU screens, the GPU tier only for one that links the SDK's `gpu` part), in the SDK's `app.json` schema. Done when: the SDK's app build tool accepts the foundation host's file, and a Desktop-tier file for a program that links `gpu` is refused by it (the SDK's effective-tier rule), quoted.
- [ ] Write the pin-move procedure in `native/README.md`: a feature Isotone needs from the SDK is built in the Impossible SDK repository by Isotone's session first (named by repository and topic in the section that needs it, never copied here), then `native/sdk.json` moves in the commit that first uses it, with the section's proof re-run on the new pin. Done when: the README names the steps and `scripts/check-sdk-pin.py` is the gate on the moved pin.
- [ ] Register the SDK's `cxx` runtime (LLVM libc++, libc++abi, and libunwind, Apache-2.0 with LLVM exceptions, <https://llvm.org/LICENSE.txt>) in `docs/dev/native-libraries.md` with its version at the pin, its provenance (built by the SDK's `cxx` part), its advisory identity, the apps that link it, and this section as owner. Done when: `python scripts/native-deps-lint.py` and `python scripts/check-native-advisories.py` pass with it registered.
- [ ] Decide how each third-party library the shipping programs link (LittleCMS, from `D01 T17 §2`, and any later one) is built from source with the SDK toolchain, since the SDK's link step accepts no prebuilt object or archive: a vcpkg triplet that uses the SDK toolchain, or the sources built by `native/` itself. Record the choice with its cost of change in `docs/dev/decisions.md`. Done when: the entry names the route and one library builds through it into a program the SDK's link step accepts.
- [ ] Commit: `"workspace: pin Impossible SDK and name each shipping program"`

**Test checkpoint:** Unit test and static analysis: `scripts/tests/test_check_sdk_pin.py` passes through `python scripts/tests/test_check_sdk_pin.py` with its three cases; `python scripts/check-sdk-pin.py` exits 0 on the tree and exits 1 naming the pin with the checkout moved one commit (both quoted); `python scripts/native-deps-lint.py` and `python scripts/check-native-advisories.py` exit 0 with the runtime registered. Cheaper substitute that fails: a pin recorded in prose only, which nothing compares with the checkout the build uses.

## 2. The SDK-Toolchain Release Build and the Boundary Checks in CI

The shipping build changes from MSVC with the static runtime to the SDK toolchain, and its proof is the SDK's boundary rules running in Isotone's own CI, so a Windows call outside the SDK fails a build here before it can fail an import on Impossible OS. This section proves the pipeline on a small probe program first; `D01 T28 §1` then moves the real programs onto it. The shipping ARM64 build stays on its present toolchain until the SDK's arm64 Windows target is proved (the SDK repository has that section), and then moves by an item added here.

**Fidelity:** no surface of its own (non-feature infrastructure: a build preset, a CI job, and planted probes, with no competitor-facing feature, so no `**Exceed:**` paragraph).
**Needs:** Windows host (build/test)

- [ ] Add the `sdk-release` configure and workflow presets to `native/CMakePresets.json` for x64, using the SDK's CMake toolchain and its link rule (no system import library on the link line), and a `native/tests/sdk-probe/` program of Isotone C++23 that throws and catches an exception through a live object, uses `thread_local`, and runs a static constructor and destructor, as the SDK's own C++ sample does. Done when: `cmake --workflow --preset sdk-release` builds `sdk-probe` and the SDK's import check (`tools/check_imports.py`) passes on it at its effective tier.
- [ ] Run the SDK's four boundary checks over every program in `native/sdk-programs.txt` (the shipping programs, starting with `sdk-probe`; `D01 T28` adds each program as it moves): the link rule, that every linked object was built here from source, that no portable part refers to a private name, and the source check that fails on any Windows, COM, or DirectX header in the program or a dependency; then the exported-header check (no Windows handle in an exported header, every untyped pointer marked `IM_MEMORY` or `IM_CONTEXT`). Done when: `python scripts/sdk-boundary.py --check` runs each over each listed program and exits 0 on the tree, naming the check and the file on a failure.
- [ ] Plant one probe per class under `scripts/tests/fixtures/sdk-boundary/`, each asserting its own diagnostic so one rule cannot pass for another: a prebuilt archive linked, a source file calling `CreateFileW`, a source file calling `GetProcAddress`, a source file that includes `<windows.h>` only for a type, an exported header with a Windows handle field, and an unmarked `void *` in an exported header. Done when: `python scripts/tests/test_sdk_boundary.py` passes with each probe failing the check it belongs to and naming it, and the unplanted `sdk-probe` passing.
- [ ] Add the `sdk` job to `.github/workflows/build.yml` (the Windows runner, the SDK checkout at the `native/sdk.json` pin, `scripts/check-sdk-pin.py` first): build `sdk-release`, run `python scripts/sdk-boundary.py --check`, run the SDK's import check on each executable, run `ctest --preset sdk-release`, and run the size gate of `D00 T05 §6` on each program. Done when: the run for the commit is green with each step in its log, read back with `ci-wait`.
- [ ] Make the shipping import gate follow how a program was built: `python scripts/native-artifact-gate.py --policy shipping` accepts a program listed in `native/sdk-programs.txt` only when it was built by the `sdk-release` preset (so a program on the SDK route cannot ship from the MSVC build), and keeps the system-DLL list of `native/system-dlls.txt` for the MSVC build of tools. Done when: `python scripts/native-artifact-gate.py --self-test` reports 0 failed with a fixture of each case, and an MSVC-built copy of `sdk-probe` is refused for shipping.
- [ ] Repeat the standard library hardening of `D00 T05 §12` for the SDK build: set libc++'s hardening mode on every first-party target of `sdk-release`, and add a probe that reads a `std::span<int>` past its end and passes only when it traps. Done when: `ctest --preset sdk-release -L hardening-probe` passes with the trap quoted and fails with the setting removed (quoted, then restored).
- [ ] Keep the MSVC presets for the developer tools that need them (`x64-asan`, the clang-tidy and `/analyze` gates, the fuzz presets) and say in `docs/dev/build.md` that a build from them does not ship. Done when: the document names the `sdk-release` preset as the shipping build and `python scripts/native-deps-lint.py` passes.
- [ ] Commit: `"workspace: build the release with the SDK toolchain behind the SDK boundary checks"`

**Test checkpoint:** Unit test and driven run with evidence: `python scripts/tests/test_sdk_boundary.py` passes with all six planted probes failing with their own diagnostics; `cmake --workflow --preset sdk-release` and `python scripts/sdk-boundary.py --check` exit 0 and the SDK's import check passes on `sdk-probe` (all quoted); the `sdk` job is green for the commit (the run id quoted); `ctest --preset sdk-release -L hardening-probe` passes. Cheaper substitute that fails: reading the finished executable's import table alone, which sees DLL and function names but not which component made a call, and cannot see a COM method at all.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with the `sdk-pin` stage among its gates
- [ ] `cmake --workflow --preset sdk-release` exits 0 and `python scripts/sdk-boundary.py --check` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-artifact-gate.py --policy shipping --require-built'` exits 0
- [ ] The `sdk` job is green on `main` and names each boundary check in its log
- [ ] `python scripts/todo-graph.py validate` clean
