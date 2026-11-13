---
schema_version: 1
id: foundation-theming
domain: 01-core
status: draft
title: "TODO-14 -- Foundation: Runtime Theming from the Design Tokens"
depends_on: []
frozen: false
track: F1
---

# TODO-14 -- Foundation: Runtime Theming from the Design Tokens

> **Goal:** `isotone::ui` exists as a static library, and every value a native surface draws with comes from token tables generated from `docs/design/tokens.json`, resolved at run time for the current theme, Highlight, density, and high-contrast state, so a style names a token key and never a value, and switching any of them, or Windows changing high contrast, reduced motion, or DPI, redraws exactly what read the changed keys.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** `docs/design/tokens.json` is the design system's single source of values, and `scripts/build-design-site.py` turns it into the design page's CSS; nothing turns it into C++ yet. `native/` holds `isotone::core` (`native/core/`) and the tests, and no `native/ui/` folder exists. `scripts/design-lint.py` skips any file whose header says it is generated from `docs/design/tokens.json` (`GENERATED_MARK_RE`), so the generated tables, which carry that header, are the one place token values may be literal. (**Corrected 2026-11-13** while building `D00 T07 §3`: said the lint already treats `native/ui/tokens/` as generated; it exempts by the header, not by the folder.)
<!-- claim: exists docs/design/tokens.json -->
<!-- claim: exists native/core/CMakeLists.txt -->
<!-- claim: absent native/ui -->
<!-- claim: count "GENERATED_MARK_RE" scripts/design-lint.py = 2 -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Element tree and theming" -- the run-time resolution, the generated tables (one per theme, Highlight, and density, plus the high-contrast mapping), and the Windows signals that invalidate styles
- [`docs/design/tokens.json`](../../docs/design/tokens.json) and [`standards/design-contract.md`](../../standards/design-contract.md) -- the values and the rule that a surface never hardcodes one
- [`docs/design/EDITING.md`](../../docs/design/EDITING.md) -- how a token changes, which this file's generator follows
- -> XREF: D01 T15 §1 -- the window and the foundation test host the switching proof runs in
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T01 §3 -- the UI library's suite theme, re-planned by `D00 T07 §5`, which consumes this file's generated tables and resolution rather than a second copy

## Outcome

- `scripts/generate-ui-tokens.py` writes `native/ui/tokens/` from `docs/design/tokens.json`, and its `--check` fails CI and `check-all.ps1` when the committed tables differ from the source.
- `isotone::ui::Theme` resolves a token key for the current theme, Highlight, density, and high-contrast state, and notifies the styles that read a key when its value changes.
- In the foundation test host, switching theme, Highlight, or density, and each Windows signal, redraws with the new values and nothing else.

**Adjacency:** list=not-applicable (no records to browse); document=not-applicable (no printed output); settings=applicable @ D01 T14 §2; reporting=not-applicable (no data of its own to summarize); notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=applicable @ D01 T14 §2; exchange=not-applicable (reads only the repository's own token file at build time); reverse=applicable @ D01 T14 §2

**Adjacency rationale:** The theme, Highlight, and density a user picks are settings, read back and applied live in §2, and each change writes its log line and can be switched back; the product's Preferences page that offers them belongs to each app's preferences section, which reads this file's service.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The isotone::ui library and the generated token tables | D00 T07 §3 |  [ ]   |
|   2   |   §2    | Run-time resolution and live switching, proved in the host | §1, D01 T15 §2, D01 T27 §2 |  [ ]   |

---

## 1. The isotone::ui Library and the Generated Token Tables

The library starts here because tokens are the first thing any surface draws with. The tables are generated, never hand-edited, so the design page and the native code can never disagree about a value.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a library target and generated tables; the surfaces that draw with them are later sections'.
**Needs:** Windows host (build/test)

- [ ] Add the static library target `isotone_ui` (alias `isotone::ui`) in `native/ui/CMakeLists.txt`, wired from `native/CMakeLists.txt`, building under every preset with the spine's flags and linking only `isotone::core` and Windows system libraries. Done when: `cmake --workflow --preset x64-debug` builds it and `python scripts/native-artifact-gate.py --policy shipping --require-built` stays clean.
- [ ] Add `scripts/generate-ui-tokens.py` (stdlib) that reads `docs/design/tokens.json` and writes `native/ui/tokens/tokens.generated.h` and `tokens.generated.cpp`: an enum of every token key, and one table per theme (Darkest, Dark, Medium Gray, Light), per Highlight (Blue, Isotone orange, Windows accent), per density (Compact, Comfortable), and the high-contrast mapping to Windows system colors, each value typed (color as linear and sRGB, size in DIPs, type style with family, size, weight, and line height), and each file opening with the header `generated from docs/design/tokens.json by scripts/generate-ui-tokens.py; do not edit` that `scripts/design-lint.py` skips. Done when: the generated files compile, a second run changes no byte, and `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` passes over them.
- [ ] Add `--check` to the generator (regenerate in memory, compare with the committed files, exit 1 naming each difference), run it in `scripts/check-all.ps1` and the `native` job of `.github/workflows/build.yml`. Done when: changing one value in `tokens.json` without regenerating fails `--check` naming the token (probe quoted, then reverted).
- [ ] Add `isotone::ui::Theme` in `native/ui/include/isotone/ui/theme.h` with `resolve(TokenKey)` returning the typed value for the current state, and unit tests in `native/tests/ui/theme_tests.cpp` registered through `isotone_add_test`. Done when: `Theme.EveryKeyResolvesInEveryState` resolves every key in every theme, Highlight, density, and high-contrast state, and `Theme.ValuesMatchTokensJson` compares a sample of each type with the values the generator read.
- [ ] Update `docs/design/EDITING.md` (after changing `tokens.json`, run `python scripts/generate-ui-tokens.py`) and `docs/dev/build.md`. Done when: both name the generator.
- [ ] Commit: `"ui: start isotone::ui with token tables generated from the design"`

**Test checkpoint:** Unit test and static analysis: `Theme.EveryKeyResolvesInEveryState` and `Theme.ValuesMatchTokensJson` pass through CTest on `x64-debug`, `x64-release`, `x64-asan`, and the ARM64 presets; `python scripts/generate-ui-tokens.py --check` exits 0, and exits 1 naming the token after one value in `tokens.json` is changed (quoted, then reverted); `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` reports `0 new`. Cheaper substitute that fails: a hand-written header of colors, which drifts from the design the first time a token changes and which `--check` would not catch.

## 2. Run-Time Resolution and Live Switching, Proved in the Host

A style reads keys, so a change of theme, Highlight, density, or a Windows signal is a change of resolved values, and only the styles that read a changed key are invalidated. The proof runs in the foundation test host, whose placeholder panels draw with tokens.

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the switching mechanism, proved on the test host's placeholder panels; product surfaces bind their own Design lines.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Element tree and theming" (the switch is proved in a live window)

Each theme, Highlight, density, or contrast change writes one line to the host's audit log, and setting the previous value again reverses it exactly, so the change needs no undo entry of its own.

- [ ] Add key-level change tracking to `isotone::ui::Theme`: a style registers the keys it read, and a state change computes the changed keys and invalidates only those styles. Done when: `Theme.SwitchInvalidatesOnlyReaders` passes, with a style that reads no changed key not invalidated.
- [ ] Persist the user's theme, Highlight, and density through the settings store of `D01 T27 §2` (atomic write and readback), logging one line per change through its logger. Done when: `Theme.ChoicePersistsAndReadsBack` passes and the change's log line is asserted.
- [ ] Handle `WM_SETTINGCHANGE` for high contrast, `SPI_GETCLIENTAREAANIMATION` for reduced motion, and `WM_DPICHANGED` in the window, each re-resolving and invalidating. Done when: `Theme.HighContrastMapsToSystemColors` passes and the host reports each signal handled.
- [ ] Add the host scenario `theme-switch` to `native/tests/foundation-host/` that cycles every theme, Highlight, and density and back, recording for each state the resolved values of the keys its placeholder panels read and the count of styles invalidated, to its `--report` JSON. Done when: the report lists every state, and switching back returns the first state's values exactly.
- [ ] Commit: `"ui: live theme, Highlight, and density switching with key-level invalidation"`

**Test checkpoint:** Unit test and driven run with evidence: `Theme.SwitchInvalidatesOnlyReaders`, `Theme.ChoicePersistsAndReadsBack`, and `Theme.HighContrastMapsToSystemColors` pass through CTest; the host run `foundation-host --scenario theme-switch --report build/foundation/theme-switch.json` exits 0 and its report lists every theme, Highlight, and density with the invalidation counts and the round trip back to the first state equal (quoted); the setting's log line and its readback after a restart of the host are quoted. Cheaper substitute that fails: redrawing everything on any change, which hides a style that reads a stale value and costs a full frame for a one-token change.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with `generate-ui-tokens --check` among its gates
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Theme.*` cases reporting through CTest
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-artifact-gate.py --policy shipping --require-built'` exits 0
- [ ] `python scripts/todo-graph.py validate` clean
