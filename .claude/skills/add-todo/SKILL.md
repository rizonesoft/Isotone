---
name: add-todo
description: Front door for new work -- search the tree and the backlog for an existing home first, apply the admission test and the budget check, then route to an existing section, a new section, a whole new file via create-todo, or the backlog. Use whenever work needs capturing, and to promote a backlog entry.
---

# Add TODO

New work enters through here. The failure this skill exists to prevent is the near-duplicate TODO in a second domain, which is worse than no entry: two owners, neither complete. In Photon the classic shape is the same feature filed once under Nodus and once under Imago when it belongs in `Photon.Core`, or filed in `Photon.Core` when only one app needs it.

The second failure is growth: the plan must not grow unconditionally (operator decision, 2026-09-26). Every new section passes the admission test and fits its phase's budget, or it does not become a section. The rules are in `todo/README.md` under "The budget and the backlog".

## Workflow

### 1. Search before filing

Search the tree for a home the work already has:

```bash
grep -rn "<keywords>" todo/ --include='TODO-*.md' | head -30
grep -n -i "<keywords>" todo/backlog.md | head -10
python scripts/todo-graph.py query findings | head -20
```

Read the candidates. A home exists when a section's scope already covers the work, even if its checklist does not name it yet. Search every app domain, not only the one the request names: a color picker, an undo stack, or a file dialog asked for in one app is often already owned by another or by the core domain. A matching backlog entry is a home too: extend its text rather than adding a second entry.

### 2. The admission test

New work becomes a section (or a file of sections) only when it is one of these, and the section's context paragraph says which:

1. **A defect in shipped or in-flight work**: something built, or being built, that does not do what its section promised.
2. **Required by an acceptance-bar aim**: name the row of "The acceptance bar" in `todo/implementation-plan.md` it serves.
3. **A prerequisite of an existing planned row**: name the `DNN TNN §N` that cannot ship without it.

Everything else (a competitor feature, a premium win, a nice-to-have from a review, research, or a gap scan) takes the Backlog outcome below. "It would be good" is not an admission clause.

### 3. The budget check

Before creating a section, read the target phase's room:

```bash
python scripts/todo-graph.py query budget
```

At the ceiling there are three moves, and raising the ceiling is not one of them:

- **Merge**: add the work as an item (or a Build-order stage) on an existing open section of that phase whose scope can hold it.
- **Supersede**: when the new work replaces an open section, rewrite that section in place (its address stays) rather than adding a second one.
- **Backlog**: file it as a backlog entry and say why in the report.

Only the operator raises a ceiling, in words, recorded as a new `todo/budget.json` history entry that quotes them (`todo/README.md`, "How the operator raises a ceiling"). Inside a phase run, the run's per-run cap applies too: `python scripts/todo-graph.py query growth --since <run start commit> --check` exits 1 past it, and then the work merges or goes to the backlog (a defect in shipped work with no open owner is the one exception, recorded in the run file).

### 4. Route to one of five outcomes

| Outcome | When | Do this |
| ------- | ---- | ------- |
| Already covered | A section or a backlog entry owns it | Point at it. File nothing. |
| Fits a section | An open section's scope covers it | Add a checklist item there, or extend the section body. Never touch a `[x]` section's checklist. |
| Needs a section | Passes the admission test, has no owner, sits inside an existing file's scope, and its phase has room | Append a new `## N.` section in numerical position with its Implementation Order row, place the row in a phase of `todo/implementation-plan.md`, then sync the plan. |
| Needs a file | Passes the admission test, a new subject no file owns, and every phase it lands in has room | Delegate to `create-todo`, or to `plan-new-feature` when the subject is a user-facing feature or a new app. |
| Backlog | Fails the admission test, or passes it with no room and nothing to merge into | Append one line to `todo/backlog.md` with the next free id: `- [B-NNN] <title> -- app: <app> -- source: <key> -- added: <today> -- summary: <what> -- needs: <refs or ids> -- why deferred: <admission clause failed, or the full phase> -- promote when: <trigger>`. At `backlog_cap`, triage first (merge or drop through `groom-plan`'s backlog triage) or report to the operator; never file a section instead. |

Shared or app-local: work lands in the core domain only when a second app needs it now. One app's need is filed in that app's domain, with a note naming the day it would move.

**Promoting a backlog entry** is this skill run on the entry: it passes the admission test and the budget check like any new work, then the promoting commit writes the section (carrying the entry's `source` as its `-> SOURCE:` line) and deletes the entry, or `validate` fails on the duplicate source.

### 5. New sections are born complete

A new section carries everything the format requires from birth: context paragraph, micro-step checklist with a `Commit:` item, `Test checkpoint:` citing one of the five proofs in `todo/README.md`, Fidelity/Job/Treatment/Chrome when it builds a surface, `Needs:` when it needs a host, `Requires:` when it needs an environment capability, and its Implementation Order row with a real `Depends On`. A section filed as a one-line stub is a plan defect, not a head start.

Give it a dependency edge, not a wish. If it must wait on another section, say so in `Depends On`; if it truly stands alone, `--`.

### 6. Wire and verify

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

### 7. Commit and report

Commit as `todo: file <what> in <ref>`, or `todo: backlog <what> as B-NNN`. Report the address (`DNN TNN §N` or `B-NNN`), the admission clause it passed or failed, why that home won over the alternatives searched, and the budget line the Progress block now shows.

## Guardrails

- Do not file work into a `[x]` section. New granularity on shipped work is a new section.
- Do not write a bare `TNN` reference without a section on any line containing `XREF`, `Depends`, or `|`.
- Do not leave the plan unsynced. A section with no plan row breaks `plan --check`.
- Do not file the same real-world thing twice. Search first (the backlog too), and stamp automated filings with `SOURCE:`.
- Do not create a section that fails the admission test, and do not create one in a phase at its ceiling. Merge, supersede, or backlog.
- Do not raise a ceiling or a cap in `todo/budget.json`. Only the operator does, in words the history entry quotes.
- Do not file app-agnostic work into one app's domain when a second app already needs it, and do not file into the core domain what only one app needs.
