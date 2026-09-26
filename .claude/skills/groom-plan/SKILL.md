---
name: groom-plan
description: Harden the todo tree for a weaker executor -- sequence check, drift sweep, gap scan, complete-feature pass, backlog triage -- within the per-run cap on discovered sections, without moving rows between phases, ticking boxes, or starting a campaign. Use before a long run, or when the plan feels stale.
---

# Groom Plan

## Evidence before reordering

```bash
python scripts/todo-graph.py query sequence
```

It prints the longest dependency chain, which is where delay costs most, and every coupling the review findings recorded: a section that filed a finding to another section ran into work that section owns, which the dependency graph does not carry.

Read what it says about direction before acting on it. **A filing is not proof the order is wrong.** Most filings are work discovered early rather than work needed first, and nothing in the data separates those. Acting on the signal alone can invert a correct order, which is exactly what happened in the plan this system was ported from.

The command proposes and cannot act: it opens no file for writing. Reordering happens here, by hand, with the addresses and cross-references kept consistent as below.

Hardening the tree so a weaker executor can run it. Grooming adds prerequisites and fills gaps within the per-run cap; it never moves a row out of its phase, never ticks a box, never raises a cap, and never starts a campaign.

Record the groom's start commit (`git rev-parse HEAD`) and a run id first (`python scripts/campaign_guard.py mint-generation`, or the campaign's `run_id` when a campaign runs the groom): a groom is a run for the per-run cap, so it files at most `per_run_discovered_sections` (15, `todo/budget.json`) sections of its own finding, each carrying `**Origin:** discovered run=<run id> <YYYY-MM-DD> -- groom-plan <step>` directly under its heading, checked with `python scripts/todo-graph.py query growth --since <start> --check` before each new section. Sections the operator asks for during a groom are operator-directed: no Origin line, no cap.

## Workflow

### 1. Sequence check

For every dependency edge (section-level `Depends On` and file-level `depends_on`), confirm the prerequisite sits no later than its consumer in phase/row order. Where an edge points later:

- Prefer adding or splitting the prerequisite under the consumer's phase (a small new section with a dated note), so the consumer's row can run in order.
- Never move the consumer's row: phase membership is stable, and moving rows rewrites the plan's history.
- Record each fix with `**Corrected YYYY-MM-DD:**` or `**Groomed YYYY-MM-DD:**`.

Run `python scripts/todo-graph.py validate` after every structural edit. Cycles are FATAL: break them at authoring time.

### 2. Drift sweep

Walk every open section's concrete claims against today's repository: projects, classes, XAML files, paths, package versions, settings keys, counts. Correct drift in place with dated notes, exactly as `process-todo-section` steps 2-3 do, but tree-wide and without building anything.

```bash
python scripts/todo-claims.py              # re-measure what the TODOs claim
python scripts/todo-claims.py --coverage   # Current state blocks nothing re-measures
```

Pay special attention to:

- "Nothing exists yet" claims that are no longer true.
- Counts and versions quoted confidently (these age fastest): SDK, package, and target framework versions especially.
- Paths under `src/Nodus/` and `src/Imago/` that the imports and renames moved.
- Deferrals whose descriptions drifted while their owners stayed open.
- XREFs whose targets moved or shipped (reciprocity still holds, or the line is corrected).

### 3. Gap scan

Read the plan as the user will use each finished app, domain by domain, and ask what has no owner: surfaces, commands, handoffs between apps (Lumen to Imago, Imago to Nodus), error paths, settings without consumers, writes without readback. File each gap with `add-todo` (evidence, owner, dependency), which applies the admission test and stamps the Origin line: a gap becomes a section only when it is a defect in shipped or in-flight work, something an acceptance-bar aim requires, or a prerequisite of a planned row, and the groom's cap has room. Nice-to-haves go to the backlog by default. Past the per-run cap, admission-test passes merge into existing sections as items or go to the backlog, and the groom record lists each overflow. Place any new rows in their phases and sync the plan.

Check the Adjacency declarations while here: `python scripts/todo-graph.py query adjacency` advisories that name real gaps become sections; ones that are already covered get their anchors sharpened.

### 4. Complete-feature pass

For every UI surface in the plan, confirm the feature is whole: list, find, create, edit, delete (or the honest not-applicable), settings with consumers, refusal paths exercised (read-only file, locked file, unsupported format), undo for every edit, and the reverse of every create. For every write to a user's document or library, confirm the atomic save, the readback, the recovery path, and the log line. For every type in `Photon.Core`, confirm at least two apps consume it, and for every pattern duplicated across two apps, confirm a section moves it into `Photon.Core`. File what is missing through `add-todo` (these usually pass the admission test, because the acceptance bar names undo, atomic saves, and shared code), preferring an item on the owning section to a new section; do not redesign what exists.

### 5. Backlog triage

```bash
python scripts/todo-graph.py query backlog
python scripts/todo-graph.py query budget
```

When the backlog is at or near `backlog_cap` (within 10 percent), or on any groom that finds it stale, triage it:

- **Merge duplicates**: two entries for one real-world thing become one (keep the lower id; fold the other's text and `source` into the survivor's summary, since a second `source` field is refused).
- **Drop stale entries**: an idea overtaken by shipped work, a decision, or a removed feature leaves the file, with one line of reason per dropped id in the commit message.
- **Promote what has come due**: an entry whose `promote when` has come true and that passes the admission test is promoted through `add-todo` (the promoting commit writes the section, with its Origin line, and deletes the entry); it counts against the groom's cap. Never raise a cap to promote.

### 6. Report and commit

Write the groom record: what was sequenced, what drifted and was corrected, what gaps were filed and where they landed (sections versus backlog, and any overflow past the per-run cap), what the backlog triage merged, dropped, and promoted, the run id and its discovered count against the cap, and the size line the Progress block now shows. Commit as `todo: groom <scope> (<date>)` after a final `validate` plus `plan --sync` plus `plan --check`.

## Guardrails

- Do not move a row out of its phase. Add or split prerequisites instead.
- Do not tick a box. Grooming never ships.
- Do not start a campaign. Grooming prepares one.
- Do not redesign sections. Harden them.
- Do not raise a cap, and do not file discovered sections past the per-run cap or without their Origin line. Merge, supersede, or backlog.
- Do not leave the tree unvalidated. `validate` plus `plan --check` pass before the commit.
