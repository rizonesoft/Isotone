---
name: add-todo
description: Front door for new work -- search the tree for an existing home first, then route to an existing section, a new section, or a whole new file via create-todo. Use whenever work needs capturing.
---

# Add TODO

New work enters through here. The failure this skill exists to prevent is the near-duplicate TODO in a second domain, which is worse than no entry: two owners, neither complete. In Photon the classic shape is the same feature filed once under Nodus and once under Imago when it belongs in `Photon.Core`, or filed in `Photon.Core` when only one app needs it.

## Workflow

### 1. Search before filing

Search the tree for a home the work already has:

```bash
grep -rn "<keywords>" todo/ --include='TODO-*.md' | head -30
python scripts/todo-graph.py query findings | head -20
```

Read the candidates. A home exists when a section's scope already covers the work, even if its checklist does not name it yet. Search every app domain, not only the one the request names: a color picker, an undo stack, or a file dialog asked for in one app is often already owned by another or by the core domain.

### 2. Route to one of four outcomes

| Outcome | When | Do this |
| ------- | ---- | ------- |
| Already covered | A section owns it | Point at the section. File nothing. |
| Fits a section | An open section's scope covers it | Add a checklist item there, or extend the section body. Never touch a `[x]` section's checklist. |
| Needs a section | Real work with no owner, inside an existing file's scope | Append a new `## N.` section in numerical position with its Implementation Order row, place the row in a phase of `todo/implementation-plan.md`, then sync the plan. |
| Needs a file | A new subject no file owns | Delegate to `create-todo`, or to `plan-new-feature` when the subject is a user-facing feature or a new app. |

Shared or app-local: work lands in the core domain only when a second app needs it now. One app's need is filed in that app's domain, with a note naming the day it would move.

### 3. New sections are born complete

A new section carries everything the format requires from birth: context paragraph, micro-step checklist with a `Commit:` item, `Test checkpoint:` citing one of the five proofs in `todo/README.md`, Fidelity/Job/Treatment/Chrome when it builds a surface, `Needs:` when it needs a host, `Requires:` when it needs an environment capability, and its Implementation Order row with a real `Depends On`. A section filed as a one-line stub is a plan defect, not a head start.

Give it a dependency edge, not a wish. If it must wait on another section, say so in `Depends On`; if it truly stands alone, `--`.

### 4. Wire and verify

- Point at related sections with `-> XREF:` and point back from each target. One-sided XREFs are FATAL.
- Name a `(item: "...")` on any deferral that hands this work to an owner, so closure is detectable at item granularity.
- A finding filed from evidence carries a `-> SOURCE: <key>` line naming what it was filed from, so a second run of the same scan cannot open a second row for it.
- Place the new section's row in exactly one phase table of `todo/implementation-plan.md`, no earlier than the phase of anything it depends on.
- Then prove the tree still holds:

```bash
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --sync
python scripts/todo-graph.py plan --check
```

### 5. Commit and report

Commit as `todo: file <what> in <ref>`. Report the section address (`DNN TNN §N`), why that home won over the alternatives searched, and what the plan totals now say.

## Guardrails

- Do not file work into a `[x]` section. New granularity on shipped work is a new section.
- Do not write a bare `TNN` reference without a section on any line containing `XREF`, `Depends`, or `|`.
- Do not leave the plan unsynced. A section with no plan row breaks `plan --check`.
- Do not file the same real-world thing twice. Search first, and stamp automated filings with `SOURCE:`.
- Do not file app-agnostic work into one app's domain when a second app already needs it, and do not file into the core domain what only one app needs.
