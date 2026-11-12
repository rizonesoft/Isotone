---
name: add-todo
description: Front door for new work -- search the tree and the backlog for an existing home first, then route to an existing section, a new section, a whole new file via create-todo, or the backlog. Work a campaign discovers on its own passes the admission test and carries an Origin line for provenance; nothing is capped. Use whenever work needs capturing, and to promote a backlog entry.
---

# Add TODO

New work enters through here (`docs/todo-workflow.md`). Two failures this skill prevents: a duplicate TODO in a second domain (such as filing shared functionality separately under Stilus and Gesso instead of `01-core`, or filing single-app code into `01-core` before a second app needs it), and silently dropped work. Every cap was removed on 2026-09-27 (`todo/budget.json`), so nothing counts against a quota. Discovered work passes the admission test (deciding section versus `todo/backlog.md`, never keep versus drop) and carries an `**Origin:**` line for provenance; backlog entries never leave without a promotion, a merge marker, or an operator removal record.

## Workflow

### 1. Search before filing

Search every domain in `todo/`, `todo/backlog.md`, and the findings list before creating anything:

```powershell
python scripts/todo-graph.py query findings | Select-Object -First 25
git grep -n -i "<keywords>" -- "todo/"
```

Read every candidate file. A home exists when an open section's scope already covers the work even if its checklist omits the micro-step, or when a `todo/backlog.md` entry already names the idea (extend that entry rather than duplicating it). Check shared versus app-local ownership: work enters `01-core` only when at least two apps consume it; single-app work stays in that app's domain with a note naming when it would move.

### 2. Operator-directed or discovered

- **Operator-directed:** the operator asked for this work in an attended session, or you are filing a self-improvement with measured ROI under the operator's autonomous self-improvement mandate (`AGENTS.md`). Operator-directed work skips the admission test and carries no `**Origin:**` line; self-improvements discovered mid-campaign carry the `**Origin:**` line below.
- **Discovered:** found autonomously during a campaign run (`process-phase` gap audit, `review-todo-section` plan/round/completion/research pass, `groom-plan` scan, or adjacent defect discovery). Apply steps 3 and 4.

### 3. The admission test (discovered work)

Discovered work becomes a live section (or item on an open section) only when it satisfies at least one clause, stated in the section's context paragraph:

1. **Defect in shipped or in-flight work:** built or in-progress code/tooling fails its promised behavior, gate, or performance bar.
2. **Required by an acceptance-bar aim:** name the acceptance-bar requirement in `todo/implementation-plan.md` or parity catalog (`docs/parity/`) it serves.
3. **Prerequisite of a planned row:** name the live `D<NN> T<NN> §<N>` section that cannot ship without it.

Everything else (nice-to-haves, speculative polish, extra ideas outside promised parity) routes to `todo/backlog.md` so nothing is lost.

### 4. The Origin line (discovered work)

Every discovered new section places one line immediately under its `## N.` heading, using the campaign guard's `run_id` (or `python scripts/campaign_guard.py mint-generation` when grooming outside a campaign):

```markdown
**Origin:** discovered run=<run id> <YYYY-MM-DD> -- <what found it>
```

Prefer the smallest honest home: merge as a micro-step into an existing open section whose scope covers it, supersede an open section in place when replacing it, or append a new section with its `**Origin:**` line when no open section fits. `python scripts/todo-graph.py validate` enforces the grammar (`origin-malformed`).

### 5. Route to one of five outcomes

| Outcome | When | Action |
| --- | --- | --- |
| Already covered | An open section or backlog entry already owns it | Cite that address; file nothing new. |
| Fits an open section | An open (`[ ]`) section's scope covers it | Add a micro-step item there (never edit a `[x]` section's checklist). |
| Needs a new section | Operator-directed, or discovered passing the admission test, within an existing file's subject | Append `## N.` at the end of the file's numbered sections (max 55 sections per file), add its Implementation Order row, place the row in `todo/implementation-plan.md`, and sync the plan. |
| Needs a new file | Operator-directed, or discovered passing the admission test, for a subject no file owns (or when the file hit 55 sections) | Route to `create-todo` (or `plan-new-feature` for a user-facing feature or app), passing provenance (`discovered` + `run_id` if applicable). |
| Backlog | Discovered failing the admission test, or explicitly deferred by the operator | Append above `## Removed with operator approval` in `todo/backlog.md` with the next free ID: `- [B-NNN] <title> -- app: <app> -- source: <key> -- added: <YYYY-MM-DD> -- summary: <what> -- needs: <refs or ids> -- why deferred: <clause failed or operator quote> -- promote when: <trigger>`. |

**Promoting a backlog entry:** write the live section carrying `-> SOURCE: <entry source key>` (plus `**Origin:**` if campaign-promoted) and delete the backlog line in the same commit so `validate` sees neither a duplicate source key nor `backlog-dropped`. Partial promotions keep the backlog entry and append `-- reviewed: <tag> <YYYY-MM-DD> promoted D<NN> T<NN> §<N>`. Release backlog reviews promote due entries or record the operator's verbatim deferral (`-- reviewed: <tag> <YYYY-MM-DD> deferred by operator: "<words>"`). When any change alters a parity feature's status, update `docs/parity/{stilus,gesso,albumen}-parity.md` in the same commit.

### 6. New sections are born complete

Every new section must be executable with zero conversation context (`todo/README.md`): context paragraph, `**Exceed:**` paragraph for every competitor-facing feature section (`AGENTS.md`), micro-step checklist (max 30 items, each naming a backticked path/symbol, `Done when:`, and `Cheaper substitute:` where applicable, ending with `Commit:`), falsifiable `**Test checkpoint:**` naming one of the canonical proof kinds in `todo/README.md`, `**Fidelity:**`/`**Design:**`/`**Job:**`/`**Treatment:**`/`**Chrome:**` on surface sections (`standards/design-contract.md`, never adding to `todo/.design-baseline`), `**Needs:**` and `**Requires:**` from the closed lists in `todo/README.md` when applicable, and an Implementation Order row with accurate `Depends On` edges (`--` only when standalone).

### 7. Wire, validate, and commit

- Add bidirectional `-> XREF: D<NN> T<NN> §<N>` links on both the new section/file and every referenced target (one-sided XREFs are FATAL).
- Add `-> SOURCE: <key>` when filing from automated/review findings so repeated scans deduplicate cleanly.
- Place the new row in `todo/implementation-plan.md` no earlier than its dependencies, then run:

```powershell
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --sync
python scripts/todo-graph.py plan --check
```

- Commit on `main` (`todo: file <what> in <ref>` or `todo: backlog <what> as B-NNN`) when filing standalone, or include in the active review/groom commit when invoked mid-step.

## Guardrails

- Never edit a `[x]` section's checklist; file follow-up work as a new section.
- Never write bare `TNN` without a section mark on `XREF`, `Depends`, or table lines, and never use em dashes or en dashes (`--` only).
- Never delete a backlog entry without promotion (`-> SOURCE:`), a survivor `merged:` marker, or verbatim operator words under `## Removed with operator approval`.
- Never modify `todo/budget.json` without an explicit operator instruction quoted in its history array.
