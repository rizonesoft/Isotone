---
schema_version: 1
id: foundation-localization
domain: 01-core
status: draft
title: "TODO-20 -- Foundation: Localization Services"
depends_on: []
frozen: false
track: F7
---

# TODO-20 -- Foundation: Localization Services

> **Goal:** before any control or command label becomes a fixed interface, the apps can be translated: strings come from translated resources per app with plural and gender rules, numbers, units, and dates are formatted and parsed for the user's locale through the ICU that ships with Windows, the interface mirrors for right-to-left languages, mnemonics and shortcuts survive translation, and a pseudo-localized build the gates run catches every hardcoded or clipped string.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No localization code or resource format exists; nothing in `isotone::core` formats a number or date for a locale. Windows 10 1903 and later ship ICU as the system component `icu.dll`.
<!-- claim: absent native/core/include/isotone/core/locale.h -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Localization" -- translated resources, plural and gender rules, locale-aware formatting and parsing through `icu.dll`, right-to-left layout, mnemonics and shortcuts, and the pseudo-localization build
- [`todo/02-stilus/TODO-01-stilus-structure.md`](../02-stilus/TODO-01-stilus-structure.md) `§4` -- the culture-safe formatting and comparison rules this file carries to the native stack (that file is superseded with the C# code)
- -> XREF: D01 T15 §3 -- the menu bar whose mnemonics and mirroring this file proves
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp

## Outcome

- `isotone::core::Locale` formats and parses numbers, units, and dates for a locale, and selects messages with plural and gender rules, through `icu.dll`.
- Each app's strings live in a resource table keyed by id, with a translation per locale and the English source as fallback.
- The host mirrors its layout in a right-to-left locale, and its mnemonics and shortcuts stay unique and reachable in every translation.
- A pseudo-localized build (longer strings, accents, right-to-left) runs in the gates and fails on a string that was not externalized or that clips.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=applicable @ D01 T20 §1; reporting=applicable @ D01 T20 §3; notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=not-applicable (no document edits); exchange=applicable @ D01 T20 §1; reverse=not-applicable (nothing created that a user removes)

**Adjacency rationale:** The interface language is a setting with readback (§1); the translation files are the one thing other people author for this file, read in §1; and the pseudo-localization run reports every unexternalized or clipped string (§3).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Messages, plurals, and locale formatting through icu.dll | D00 T07 §3, D01 T27 §2 |  [ ]   |
|   2   |   §2    | Right-to-left mirroring, mnemonics, and shortcuts that survive translation | §1, D01 T15 §3 |  [ ]   |
|   3   |   §3    | The pseudo-localization build in the gates | §2 |  [ ]   |

---

## 1. Messages, Plurals, and Locale Formatting through icu.dll

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a core service.
**Needs:** Windows host (build/test)

Translations are the one file this foundation imports from other people: each app's `strings/<locale>.json` is read at start, and a malformed import is refused with its file and line.

- [ ] Add `isotone::core::Locale` over `icu.dll` (loaded as the system component, its absence below Windows 10 1903 refused with a message), formatting and parsing numbers, percentages, units, and dates for a locale, and comparing strings with the locale's collation. Done when: `Locale.FormatsAndParsesRoundTrip` passes for `en-US`, `de-DE`, `fr-FR`, `ar-SA`, and `ja-JP`, and `Locale.ParsesWhatItFormats` round-trips every value it formats.
- [ ] Add the string resource format `native/<app>/resources/strings/<locale>.json` with message ids, ICU MessageFormat patterns for plural and gender selection, and the English source as fallback, and a loader that refuses a malformed file with the file and line. Done when: `Strings.PluralAndGenderSelect` passes for English, Polish, and Arabic plural categories, and `Strings.MalformedFileRefused` passes.
- [ ] Make the interface language a setting with atomic write and readback, defaulting to the Windows display language. Done when: `Strings.LanguageSettingReadsBack` passes.
- [ ] Commit: `"core: localization services through the system ICU"`

**Test checkpoint:** Unit test: `Locale.FormatsAndParsesRoundTrip`, `Locale.ParsesWhatItFormats`, `Strings.PluralAndGenderSelect`, `Strings.MalformedFileRefused`, and `Strings.LanguageSettingReadsBack` pass through CTest on every preset; `python scripts/native-artifact-gate.py --policy shipping --require-built` still reports Windows system DLLs only, with `icu.dll` among them (quoted). Cheaper substitute that fails: `std::locale` and `printf`, which have no plural rules and format differently under the CRT than the rest of Windows.

## 2. Right-to-Left Mirroring, Mnemonics, and Shortcuts That Survive Translation

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the layout and keyboard mechanisms, proved on the host's placeholder menus.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Localization" (the mirrored layout is proved in a live window)

- [ ] Mirror the element tree's layout in a right-to-left locale (leading and trailing instead of left and right, mirrored icons where the design says so), and draw right-to-left text with the right reading order. Done when: `Layout.MirrorsInRtl` passes and the host scenario `rtl` reports the menu bar and panels mirrored.
- [ ] Give each translated label its mnemonic from the translation, and check that every menu's mnemonics are unique in every locale; keep shortcuts defined by key, not by translated letter. Done when: `Mnemonics.UniquePerMenuInEveryLocale` passes over the host's resource tables.
- [ ] Commit: `"ui: right-to-left mirroring and translation-safe mnemonics"`

**Test checkpoint:** Unit test and driven run with evidence: `Layout.MirrorsInRtl` and `Mnemonics.UniquePerMenuInEveryLocale` pass through CTest; `foundation-host --scenario rtl --locale ar-SA --report build/foundation/rtl.json` exits 0 with the mirrored positions and each menu opened by its translated mnemonic (quoted). Cheaper substitute that fails: mirroring with `WS_EX_LAYOUTRTL` only, which mirrors pixels, including text and images that must not flip.

## 3. The Pseudo-Localization Build in the Gates

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a build and a gate.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Localization" (the clipping check measures drawn text)

- [ ] Add `scripts/pseudo-localize.py` writing the pseudo locales `qps-ploc` (each string lengthened by 40 percent with accented characters and brackets) and `qps-plocm` (right-to-left), from each app's English resources. Done when: running it writes both locales and a second run changes no byte.
- [ ] Add the host scenario `pseudo-loc` that runs in each pseudo locale and reports every drawn string not wrapped in the pseudo brackets (a hardcoded string) and every string clipped by its container. Done when: the report lists none on the host, and a deliberately hardcoded label is reported.
- [ ] Run the scenario in `scripts/check-all.ps1` and the `native` CI job. Done when: both list the stage.
- [ ] Commit: `"ui: the pseudo-localization gate"`

**Test checkpoint:** Driven run with evidence: `python scripts/pseudo-localize.py` writes both locales; `foundation-host --scenario pseudo-loc --report build/foundation/pseudo-loc.json` exits 0 with no hardcoded and no clipped string, and exits 1 naming a deliberately hardcoded label (both quoted); the CI stage is green on the candidate's run. Cheaper substitute that fails: reviewing translations by eye, which finds a clipped German label only after it ships.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with the pseudo-localization stage among its gates
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `Locale.*`, `Strings.*`, `Layout.*`, and `Mnemonics.*` cases reporting through CTest
- [ ] `python scripts/todo-graph.py validate` clean
