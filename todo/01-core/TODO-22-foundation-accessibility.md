---
schema_version: 1
id: foundation-accessibility
domain: 01-core
status: draft
title: "TODO-22 -- Foundation: UI Automation, the Driven-Input Runner, and the Screen Reader Scenarios"
depends_on: []
frozen: false
track: F9
---

# TODO-22 -- Foundation: UI Automation, the Driven-Input Runner, and the Screen Reader Scenarios

> **Goal:** every element of `isotone::ui` is exposed to UI Automation with the patterns, properties, and events its control needs, under a stated lifetime and threading rule; a driven-input runner drives the keyboard and mouse through `SendInput`, the pen and touch through synthetic pointer injection, and a real IME's composition, so every later section can prove input paths UI Automation bypasses; and Narrator and NVDA scenarios run as driven checks with their transcripts recorded.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No UI Automation provider, input driver, or screen reader check exists. `todo/README.md`'s proof table marks the driven-run proof's UI Automation, `SendInput`, and synthetic pointer injection runner `unusable for a stamp until D01 T22 §2 lands`, the marker `D00 T07 §3` set, so the stamp of §2 activates it.
<!-- claim: absent native/tests/drive -->
<!-- claim: count "until `D01 T22 §2` lands" todo/README.md = 1 -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Accessibility" -- the provider, the patterns (Invoke, Toggle, Value, RangeValue, Selection and SelectionItem, ExpandCollapse, Scroll, Text, Grid), the events, fragment navigation, virtualized items, the lifetime and threading rule, the input paths UI Automation bypasses, and the named screen reader scenarios
- [`todo/README.md`](../README.md), "Proof: what a Test checkpoint may cite" -- the marker §2 activates
- -> XREF: D01 T15 §3 -- the window and title bar whose elements the provider exposes
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T21 §3 -- drives real IME composition through §2's runner
- -> XREF: D01 T23 §2 -- drags a panel out and back through §2's runner
- -> XREF: D01 T24 §2 -- injects pen samples through §2's runner to measure latency

## Outcome

- `isotone::ui` elements answer UI Automation through fragment providers, with the patterns and events their controls need, answering from the UI thread's state whatever thread the call arrives on.
- `native/tests/drive/` provides the runner: reading and invoking through UI Automation, the keyboard and mouse through `SendInput`, pen and touch through `CreateSyntheticPointerDevice` and `InjectSyntheticPointerInput`, and IME composition through a real IME, with a CTest label and a `check-all.ps1` stage; its stamp turns the proof table's marker into the runner command.
- Narrator and NVDA scenarios on the host run as driven checks whose transcripts are recorded.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (screen reader and input settings are Windows'); reporting=applicable @ D01 T22 §3; notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=not-applicable (no document edits); exchange=not-applicable (no files); reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** The screen reader transcripts are this file's report (§3); everything else is a mechanism other sections prove through.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The UI Automation provider for every element | D00 T07 §3, D01 T15 §3 |  [ ]   |
|   2   |   §2    | The driven-input runner: UI Automation, SendInput, synthetic pointer injection, and IME composition | §1 |  [ ]   |
|   3   |   §3    | The Narrator and NVDA scenarios with recorded transcripts | §2 |  [ ]   |

---

## 1. The UI Automation Provider for Every Element

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the accessibility provider, proved on the host's placeholder controls.
**Needs:** Windows host (build/test)

- [ ] Add `isotone::ui::Accessible`: a fragment root per window (`IRawElementProviderFragmentRoot` answering `WM_GETOBJECT`) and a fragment per element with navigation, bounding rectangles in physical pixels, names, automation ids, control types, and the patterns its control declares, with the provider lifetime and threading rule written in `native/ui/README.md` (calls arrive on any thread and are answered from a snapshot the UI thread publishes). Done when: `Accessible.TreeMatchesElementTree` and `Accessible.CallsFromAnyThreadAnswerFromUiState` pass.
- [ ] Raise the focus, structure, property, selection, and text events, and support virtualized items for long lists (`ItemContainer` and `VirtualizedItem`). Done when: `Accessible.RaisesFocusAndStructureEvents` and `Accessible.VirtualizedListRealizesOnDemand` pass.
- [ ] Commit: `"ui: a UI Automation provider for every element"`

**Test checkpoint:** Unit test: `Accessible.TreeMatchesElementTree`, `Accessible.CallsFromAnyThreadAnswerFromUiState`, `Accessible.RaisesFocusAndStructureEvents`, and `Accessible.VirtualizedListRealizesOnDemand` pass through CTest, including the AddressSanitizer lanes (no provider outlives its element). Cheaper substitute that fails: one provider for the whole window, which a screen reader reads as a single unnamed pane.

## 2. The Driven-Input Runner: UI Automation, SendInput, Synthetic Pointer Injection, and IME Composition

UI Automation's invoke bypasses hit testing and input, so input paths are proved by driving input itself. This section is the runner every later driven-run checkpoint cites, and its stamp activates the proof.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a test runner.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Accessibility" (input is injected into a live interactive session)

- [ ] Add `native/tests/drive/` (library `isotone_drive`): a UI Automation client that finds, reads, and invokes elements by automation id; keyboard and mouse through `SendInput`; pen pressure, tilt, and barrel button and multi-touch through `CreateSyntheticPointerDevice` and `InjectSyntheticPointerInput`; and IME composition by activating the Windows Japanese, Chinese, and Korean IMEs and typing through `SendInput`, observing composition events, never injecting committed text. Done when: `Drive.InvokesByAutomationId`, `Drive.TypesThroughSendInput`, `Drive.InjectsPenWithPressureAndTilt`, and `Drive.ComposesThroughJapaneseIme` pass against the host.
- [ ] Register the drive tests with the CTest label `drive`, add a `drive` stage to `scripts/check-all.ps1` that runs them in a display session and skips with a warning naming the missing session otherwise, and document the runner in `native/tests/drive/README.md`. Done when: `ctest --preset x64-debug -L drive` passes in a display session and the stage is listed.
- [ ] Activate the proof at this section's stamp: in `todo/README.md`'s proof table the driven-run row's marker for UI Automation, `SendInput`, and synthetic pointer injection names this section, and the stamp tool rewrites it to the runner command `ctest --preset <preset> -L drive` (`D00 T07 §3`). Done when: the marker names `D01 T22 §2` before the stamp and the runner command after it.
- [ ] Commit: `"tests: the driven-input runner for UI Automation, SendInput, pointer injection, and IMEs"`

**Test checkpoint:** Driven run with evidence: `ctest --preset x64-debug -L drive` passes in a display session, with `Drive.InvokesByAutomationId`, `Drive.TypesThroughSendInput`, `Drive.InjectsPenWithPressureAndTilt`, and `Drive.ComposesThroughJapaneseIme` reporting (output quoted); the `check-all.ps1` `drive` stage passes there and skips with its warning in a session without a desktop (both quoted). Cheaper substitute that fails: invoking every control through UI Automation, which never exercises hit testing, focus, or the IME.

## 3. The Narrator and NVDA Scenarios with Recorded Transcripts

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- driven screen reader checks on the host.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Accessibility" (screen readers run against a live desktop)

The transcripts are this file's report: each run writes one report per screen reader comparing its speech with the expected text, step by step.

- [ ] Write the named scenarios in `native/tests/drive/screen-readers.md`: open the host, move through the menu bar and open a menu, tab through the placeholder panels' controls, change a value, and hear each element's name, role, and state. Done when: each scenario lists its steps and the expected speech.
- [ ] Drive each scenario with the runner under Narrator (its speech captured through the Narrator developer mode's text output) and under NVDA (its speech log), and record the transcripts under `docs/captures/screen-readers/`. Done when: both transcripts match the expected speech step by step.
- [ ] Commit: `"tests: the Narrator and NVDA scenarios with transcripts"`

**Test checkpoint:** Driven run with evidence: each scenario run under Narrator and under NVDA with the runner, the two transcripts committed under `docs/captures/screen-readers/` and each step's speech matching the expected text (quoted). Cheaper substitute that fails: Accessibility Insights' automated checks alone, which find missing names but cannot hear a confusing order.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with the `drive` stage passing in a display session
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Accessible.*` cases reporting through CTest
- [ ] The proof table's driven-run marker reads the runner command once §2 is stamped
- [ ] `python scripts/todo-graph.py validate` clean
