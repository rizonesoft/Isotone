---
schema_version: 1
id: foundation-text
domain: 01-core
status: draft
title: "TODO-21 -- Foundation: the Text Editing Model with the Text Services Framework"
depends_on: []
frozen: false
track: F8
---

# TODO-21 -- Foundation: the Text Editing Model with the Text Services Framework

> **Goal:** one text editing model sits under every text box and every app's type tool: the caret moves and deletes by grapheme cluster, caret and selection follow bidirectional text, typing groups for undo, fonts fall back through DirectWrite's system fallback, and input methods work through a Text Services Framework text store that keeps the lock protocol, composes, commits, cancels, survives a focus change mid-composition, and places the candidate window right at mixed DPI.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No text model, text store, or DirectWrite text layout exists in `isotone::ui`.
<!-- claim: absent native/ui/src/text -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Text" -- grapheme clusters, bidirectional caret and selection, undo grouping, font fallback, the `ITextStoreACP2` text store and its lock protocol and reentrancy rules, composition, candidate window placement, and the proofs (CJK through the real IMEs, Arabic and Hebrew, combining sequences and emoji, text on a transformed canvas)
- -> XREF: D01 T15 §2 -- the renderer the text draws through
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T22 §2 -- the runner that drives the real IMEs

## Outcome

- `isotone::ui::TextModel` edits by grapheme cluster with bidirectional caret and selection, undo grouping, and DirectWrite layout with system font fallback.
- `isotone::ui::TextStore` implements `ITextStoreACP2` with its lock protocol and reentrancy rules, composition start, update, commit, and cancel, focus changes during composition, and candidate window placement at mixed DPI.
- Chinese, Japanese, and Korean composition through the real IMEs, Arabic and Hebrew caret and selection, combining sequences and emoji, and text on a transformed canvas are proved in the host.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (input methods are Windows settings); reporting=not-applicable (no data to summarize); notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=applicable @ D01 T21 §1; exchange=not-applicable (no files); reverse=applicable @ D01 T21 §1

**Adjacency rationale:** Typing is grouped into undo steps that reverse exactly what was typed, and the text model reports its edits as commands so the host's log records them (§1).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The text model: clusters, bidirectional caret and selection, undo grouping, and fallback | D00 T07 §3, D01 T15 §2 |  [ ]   |
|   2   |   §2    | The TSF text store | §1 |  [ ]   |
|   3   |   §3    | The text proofs through real IMEs and scripts | §2, D01 T22 §2 |  [ ]   |

---

## 1. The Text Model: Clusters, Bidirectional Caret and Selection, Undo Grouping, and Fallback

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the editing model under every text box.
**Needs:** Windows host (build/test)

Each typing group is one undo step, and the host's audit log records the command that made it.

- [ ] Add `isotone::ui::TextModel` in `native/ui/src/text/`: caret movement and deletion by grapheme cluster (`IDWriteTextAnalyzer` cluster metrics), word and line movement, and selection by cluster. Done when: `TextModel.DeletesWholeCluster` passes for combining sequences, emoji with modifiers and zero-width joiners, and Hangul syllables.
- [ ] Lay out with DirectWrite and system font fallback, mapping logical to visual positions so the caret and selection follow bidirectional text, with the caret's direction shown. Done when: `TextModel.BidiCaretFollowsVisualOrder` passes for mixed English and Arabic and for Hebrew with numbers.
- [ ] Group typing into undo steps (a run of typing, broken by a caret move, a pause, or a different kind of edit), each a recorded command logged by the host. Done when: `TextModel.TypingGroupsIntoOneUndo` passes.
- [ ] Commit: `"ui: the text editing model"`

**Test checkpoint:** Unit test: `TextModel.DeletesWholeCluster`, `TextModel.BidiCaretFollowsVisualOrder`, and `TextModel.TypingGroupsIntoOneUndo` pass through CTest on every preset. Cheaper substitute that fails: editing by UTF-16 code unit, which splits an emoji or a combining mark in half.

## 2. The TSF Text Store

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the input method bridge.
**Needs:** Windows host (build/test)

- [ ] Implement `isotone::ui::TextStore` as `ITextStoreACP2` over `TextModel`: the read and write lock protocol with `RequestLock` and its reentrancy rules (a synchronous request during a lock refused, an asynchronous one queued), the text and selection queries, and the change sinks. Done when: `TextStore.LockProtocolRefusesReentrantSync` and `TextStore.QueuesAsyncLockDuringLock` pass against a fake TSF manager.
- [ ] Handle composition start, update, commit, and cancel; end a composition cleanly when focus moves; and report the text extent so the candidate window lands under the composition at the window's DPI, correct across monitors of different DPI. Done when: `TextStore.CompositionLifecycle`, `TextStore.FocusChangeEndsComposition`, and `TextStore.CandidateRectAtMixedDpi` pass.
- [ ] Commit: `"ui: the TSF text store"`

**Test checkpoint:** Unit test: `TextStore.LockProtocolRefusesReentrantSync`, `TextStore.QueuesAsyncLockDuringLock`, `TextStore.CompositionLifecycle`, `TextStore.FocusChangeEndsComposition`, and `TextStore.CandidateRectAtMixedDpi` pass through CTest, including the AddressSanitizer lanes. Cheaper substitute that fails: `WM_IME_CHAR` handling through IMM32, which loses composition attributes and the modern IMEs' features.

## 3. The Text Proofs through Real IMEs and Scripts

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- driven proofs in the host's placeholder text box.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Text" (real IMEs compose in a live session)

- [ ] Add the drive tests `TextDrive.ChineseComposition`, `TextDrive.JapaneseComposition`, and `TextDrive.KoreanComposition` that activate each Windows IME through the driven-input runner, type a phrase through `SendInput`, choose a candidate, commit, and read the committed text and its undo through UI Automation. Done when: each passes and the committed text equals the expected phrase.
- [ ] Add `TextDrive.ArabicHebrewCaret` (caret and selection across direction runs by keyboard), `TextDrive.CombiningAndEmoji` (deletion and caret by cluster), and `TextDrive.TransformedCanvasText` (a text box under a rotated and scaled transform, composing with the candidate window at the transformed caret). Done when: each passes.
- [ ] Commit: `"tests: the text proofs through real IMEs and scripts"`

**Test checkpoint:** Driven run with evidence: `ctest --preset x64-debug -L drive -R TextDrive` passes in a display session with the Chinese, Japanese, and Korean IMEs installed, each test's committed text and the IME it used quoted. Cheaper substitute that fails: injecting committed Unicode text, which never exercises composition, candidates, or the lock protocol.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `TextModel.*` and `TextStore.*` cases reporting through CTest
- [ ] The `TextDrive.*` tests pass on the reference machine with the three IMEs installed
- [ ] `python scripts/todo-graph.py validate` clean
