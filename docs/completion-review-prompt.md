# Completion review prompt

Copy this into a scratch file, fill in the placeholders, and pass it to `scripts/review-dispatch.py --prompt`. It is the one-pass completion review every TODO section gets after its review loop signs off (`review-todo-section`, step 5a; operator decision 2026-10-23).

---

You are an independent reviewer. Do not modify any file. The candidate below has already passed a correctness review. Your question is different: is what it built a complete feature a user can reach and use, or only its core?

## Candidate

- Commit range: `<BASE_SHA>..<TIP_SHA>` (inspect it with `git diff` and `git show`).
- TODO section: `<DNN TNN §N>` (its contract: `python scripts/todo-graph.py resolve "<DNN TNN §N>"`).
- Where the feature appears: `<layout map file and entries>`, `<design specs on the section's Design line>`, `<parity catalog rows>`, `<user guide page>`.

## What to check

For each capability the section adds or changes, check every entry point and companion a user of Illustrator, Photoshop, or Lightroom Classic would expect, as the layout map places them, and say for each whether the candidate implements it:

1. Menu items, in the menu and position the layout map gives, with the map's shortcut.
2. Keyboard shortcuts and the command search entry.
3. Tool rail, toolbar, options bar, panel, panel menu, and context menu buttons and items.
4. Dialogs: every control the map and the design spec list, their defaults, validation, and OK, Cancel, and Reset behavior.
5. States: enabled and disabled conditions, empty, loading, error, and cancelled states, with the messages the user sees.
6. Undo and redo, settings and workspace persistence, and recent-files or history entries where they apply.
7. File formats: the open, save, import, or export path round trips, where the feature touches a document.
8. Accessibility (UI Automation names and patterns, a keyboard path) and localizable strings.
9. The user guide entry and the log line for each action that changes a document or a setting.
10. Anything the feature needs from another part of the suite that does not exist yet.
11. Better, not a clone: whether the section's `**Exceed:**` improvement is real, built, and proved (its target measured against the competitor, its removed step gone, its added capability working), or whether the feature merely matches the competitor where the section promised to beat it.

## Reply format

One numbered line per gap, tagged right after its number `in-scope` (the section's contract or its parity rows cover it) or `out-of-scope` (another section must own it), naming the missing entry point or behavior and the file and line where it should be, or the map entry it fails. Then `HIGHEST: P1`, `P2`, `P3`, or `none` (a missing entry point a user needs to reach the feature is P1), and a final line `OVERALL: complete` or `OVERALL: incomplete`. If you could not read the candidate, say why in one line and end with `OVERALL: blocked`.
