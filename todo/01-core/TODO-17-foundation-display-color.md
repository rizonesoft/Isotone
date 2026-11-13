---
schema_version: 1
id: foundation-display-color
domain: 01-core
status: draft
title: "TODO-17 -- Foundation: the Display Color Pipeline in SDR, Advanced Color SDR, and HDR"
depends_on: []
frozen: false
track: F4
---

# TODO-17 -- Foundation: the Display Color Pipeline in SDR, Advanced Color SDR, and HDR

> **Goal:** every app shows colors correctly on every kind of display Windows 11 drives: each monitor's mode is read as ordinary SDR, Advanced Color SDR, or HDR; documents are converted to the monitor's profile in SDR and to scRGB on an FP16 swap chain otherwise, with the white level each mode means; HDR highlights are tone-mapped by one defined operator; and a window moved between monitors, or a display configuration change, switches the pipeline without a wrong frame.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No display color code exists, and LittleCMS is not in the dependency register (`docs/dev/native-libraries.md`) or in `native/vcpkg.json`. The renderer's swap chains come from `D01 T15 §2`.
<!-- claim: count "lcms" native/vcpkg.json = 0 -->
<!-- claim: exists docs/dev/native-libraries.md -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Display color" -- the mode query (`DisplayConfigGetDeviceInfo` with `DISPLAYCONFIG_DEVICE_INFO_GET_ADVANCED_COLOR_INFO_2`, the older query elsewhere), the swap chain formats, the luminance policy per mode, the BT.2390 EETF, the re-read triggers, and the proofs
- [`docs/dev/native-libraries.md`](../../docs/dev/native-libraries.md) -- the register LittleCMS 2 joins
- -> XREF: D01 T15 §2 -- the swap chains whose format this pipeline sets
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp

## Outcome

- `isotone::ui::DisplayColor` reports each monitor's mode, SDR white level, and luminance range, and re-reads them on every trigger the spec lists.
- In ordinary SDR the swap chain is 8-bit and documents are converted to the monitor's ICC profile with LittleCMS; in Advanced Color SDR and HDR it is FP16 scRGB, with no reference-white scaling in Advanced Color SDR and the SDR reference white in HDR.
- HDR content is tone-mapped by the BT.2390 EETF to the display's peak in HDR and to SDR white elsewhere.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (the display's mode and white level are Windows settings this pipeline reads, never stores); reporting=applicable @ D01 T17 §1; notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=applicable @ D01 T17 §1; exchange=not-applicable (reads only installed monitor profiles); reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** The pipeline's state per monitor is reported (§1) so a support report can say what the display was; each mode change writes a log line.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Reading each monitor's color mode and following its changes | D00 T07 §3, D01 T15 §2 |  [ ]   |
|   2   |   §2    | The SDR path: 8-bit swap chain and ICC conversion with LittleCMS | §1 |  [ ]   |
|   3   |   §3    | Advanced Color SDR and HDR: FP16 scRGB, white levels, and the EETF | §2 |  [ ]   |

---

## 1. Reading Each Monitor's Color Mode and Following Its Changes

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a display query and its triggers.
**Needs:** Windows host (build/test)

Each mode change on a monitor writes one line to the audit log, so a support report can show the display's history.

- [ ] Add `isotone::ui::DisplayColor::query(HMONITOR)` returning the mode (SDR, Advanced Color SDR, HDR), the SDR white level (`DISPLAYCONFIG_SDR_WHITE_LEVEL`), and the luminance range from `IDXGIOutput6::GetDesc1`, using `DISPLAYCONFIG_DEVICE_INFO_GET_ADVANCED_COLOR_INFO_2` where Windows provides it and the older query otherwise, recording in `native/ui/README.md` what the older query cannot tell apart. Done when: `DisplayColor.ParsesBothQueryShapes` passes over recorded structures for each mode.
- [ ] Re-read on a window's move to another monitor, on `WM_DISPLAYCHANGE`, and when the DXGI factory reports `IsCurrent() == FALSE`, logging each change. Done when: `DisplayColor.RereadsOnEachTrigger` passes with each trigger simulated.
- [ ] Add the host scenario `display-modes` that reports every monitor's mode, white level, and luminance range. Done when: its report on the reference machine is quoted with the Windows settings it matches.
- [ ] Commit: `"ui: read each monitor's color mode and follow its changes"`

**Test checkpoint:** Unit test and driven run with evidence: `DisplayColor.ParsesBothQueryShapes` and `DisplayColor.RereadsOnEachTrigger` pass through CTest; `foundation-host --scenario display-modes --report build/foundation/display-modes.json` exits 0 and its mode and white level match what Windows Settings shows for each monitor (both quoted). Cheaper substitute that fails: telling the modes apart from `GetDesc1` alone, which the spec rules out because it cannot distinguish Advanced Color SDR from SDR.

## 2. The SDR Path: 8-bit Swap Chain and ICC Conversion with LittleCMS

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the conversion path, proved with measured patches.
**Needs:** Windows host (build/test)

- [ ] Add LittleCMS 2 through vcpkg in `native/vcpkg.json` and register it in `docs/dev/native-libraries.md` (version, provenance, MIT license and its URL, its advisory identity, the apps that link it, this section as owner). Done when: `python scripts/native-deps-lint.py` and `python scripts/check-native-advisories.py` pass with it registered.
- [ ] Convert a document's colors from its profile to the monitor's ICC profile (`GetICMProfileW` or the WCS default for the monitor) with LittleCMS on an 8-bit swap chain, caching transforms per profile pair. Done when: `DisplayColor.SdrPatchesThroughKnownProfile` converts a committed patch set through a committed test profile and every patch is within 1 code value of the reference values computed by LittleCMS's own transform tool, recorded in `native/tests/ui/fixtures/display-color/`.
- [ ] Commit: `"ui: the SDR display path with LittleCMS"`

**Test checkpoint:** Unit test: `DisplayColor.SdrPatchesThroughKnownProfile` passes through CTest on every preset, including `x64-asan`; `python scripts/native-deps-lint.py` passes with LittleCMS registered (quoted). Cheaper substitute that fails: drawing document colors unconverted, which is right only on an sRGB monitor.

## 3. Advanced Color SDR and HDR: FP16 scRGB, White Levels, and the EETF

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the wide-gamut and HDR paths, proved with measured patches and a monitor move.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Display color" (the HDR and Advanced Color proofs need those display modes on the machine; the run records the displays used)

- [ ] In Advanced Color SDR and HDR, use an FP16 swap chain (`DXGI_FORMAT_R16G16B16A16_FLOAT`) with `DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709` and convert documents to scRGB; in HDR scale the interface and SDR documents by the SDR white level over 80 nits, and in Advanced Color SDR apply no scaling. Done when: `DisplayColor.ScrgbWhiteMeansEachMode` passes for both modes.
- [ ] Tone-map HDR documents with the ITU-R BT.2390 EETF to the display's peak on HDR and tone- and gamut-map to SDR white elsewhere. Done when: `DisplayColor.Bt2390MatchesReferenceCurve` matches the reference curve's values at committed sample points within 1e-4.
- [ ] Switch the swap chain format when a window moves between monitors in different modes, with no frame presented in the wrong format. Done when: the host scenario `display-move` reports every presented frame's format matching its monitor's mode.
- [ ] Add the host scenario `display-patches` that draws the committed patch set in each mode available on the machine and reads back the presented values. Done when: the report lists each mode with its patches within the stated tolerance, and names any mode the machine lacks.
- [ ] Commit: `"ui: Advanced Color SDR and HDR with the BT.2390 EETF"`

**Test checkpoint:** Unit test and driven run with evidence: `DisplayColor.ScrgbWhiteMeansEachMode` and `DisplayColor.Bt2390MatchesReferenceCurve` pass through CTest; `foundation-host --scenario display-patches` and `--scenario display-move` exit 0 on the reference machine, the patches within tolerance in each available mode and no frame in the wrong format across a move between monitors in different modes (reports quoted, with the displays and modes the run had). Cheaper substitute that fails: an FP16 swap chain everywhere with one white level, which washes out the interface on HDR and oversaturates it on Advanced Color SDR.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `DisplayColor.*` cases reporting through CTest
- [ ] `python scripts/native-deps-lint.py` and `python scripts/check-native-advisories.py` pass with LittleCMS registered
- [ ] The `display-modes`, `display-patches`, and `display-move` scenarios pass on the reference machine, in each mode its displays offer
- [ ] `python scripts/todo-graph.py validate` clean
