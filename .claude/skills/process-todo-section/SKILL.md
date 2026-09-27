---
name: process-todo-section
description: Process exactly one TODO section end to end -- resolve it, validate and fact-check the plan against the repository, correct every drifted claim, build it, run the gates, hand to review, and commit. Use whenever asked to process, implement, ship, continue, or finish a TODO section.
---

# Process TODO Section

One section. One commit. The section is the contract: **and a contract is checked before it is signed.**

Processing a section is two jobs, in order. First establish that the plan is sound: internally consistent, still true of the code, buildable as written, and verifiable when built. Then implement it. A section written weeks ago against a codebase that has since moved is a plan with a bug in it, and building it faithfully ships that bug with full ceremony.

So: **do not improvise around the plan, and do not implement a plan you have found to be wrong.** Correct it in the file, visibly, then build the corrected version.

## Use this skill when

- The user names a section **in any form**: a path and a section, a `DNN TNN §N` reference, or a row pasted straight out of `todo/implementation-plan.md`. Step 0 turns all of them into the same thing.
- An attended runner picks the next `[ ]` row from the plan.
- Do NOT use to audit already-shipped work: that is `review-todo-section` in audit stance.

## Step 0 -- resolve the argument before anything else

**Never hand-translate a reference into a filename.** Ask the graph:

```bash
python scripts/todo-graph.py resolve "$ARGUMENTS"
```

It accepts whatever the caller had in front of them:

| Input | Works |
| --- | :-: |
| `DNN TNN §N` (domain, TODO, and section numbers) | yes |
| <code>&#124; [ ] &#124; \`DNN TNN §N\` &#124; Deliverable … &#124; 5 &#124;</code> (a plan row, pasted whole) | yes |
| `<todo-path> §<n>` (a file path plus its section number, e.g. under `todo/`) | yes |
| Any prose containing one of the above | yes |

It prints the path, the section title, the item count, whether the TODO is frozen, and **which dependencies are unmet**. Its exit code is the instruction:

| Exit | Meaning | Do this |
| :-: | --- | --- |
| `0` | Resolved, open, dependencies met | Proceed to step 1 |
| `1` | No such TODO or no such section | Stop. Report the reference as unresolvable rather than guessing a near match. |
| `2` | No section reference in the input | Stop and ask which section. |
| `3` | The section is already `[x]` | Do **not** process it. This is `review-todo-section` in audit stance; say so and hand over. |
| `4` | Unmet dependencies | Stop at the dependency gate and name the unmet sections. |
| `5` | The section moved out of the tree (`> **Moved:**` under its heading) | Stop. Its open work is worked from the file the `moved` line names, by that file's own rules. |

Use the `skill arg` line it prints as the canonical form for the rest of the run, so the commit message and the review call name the section the same way.

**If `resolve` printed a `needs` line, the section needs a host.** Confirm the host is reachable before writing `Started:` (for `.NET SDK (build/test)`, `dotnet --version` in the repo root prints the version `global.json` pins). If it is not, stop and say which host the section waits on: starting a host-bound section with no host is how a run burns a session producing nothing committable.

**If `resolve` printed a `requires` line with requirements missing here, the section needs that environment.** Confirm it is reachable before writing `Started:`. If it is not, stop and say which capability the section waits on: starting an environment-bound section with no environment burns a session the same way.

**Write `Started:` now, at the first resolve.** If the section body carries no `> **Started:**` line, add one with the current UTC instant (`date -u +%Y-%m-%dT%H:%M:%SZ`). Do **not** overwrite an existing one on resume: review subtracts it from stamp time for `Duration:`, which is the whole working interval. A section resumed after a session death would otherwise report the wrong half of its own cost.

**Stop here if another writer holds the tree.** Check `git status` for unfamiliar uncommitted work you do not understand, and ask before building over it. Two writers on one tree is how a call ships without its interface.

## Execution discipline

- **Validate before building.** Step 2 is a gate, not a formality. A section that cannot pass it gets fixed first.
- **Follow the corrected contract.** The checklist items define the scope. Do not widen because something adjacent looks wrong; file it instead with `add-todo`, whose admission test decides between an item on an open section, a new section (carrying its Origin line), and the backlog. Correcting a defect *in* the section is not widening; adding work the section never asked for is.
- **One section = one commit.** If you cannot describe the change in one commit message, the section was mis-sized. Plan corrections may ride in that commit, or land as their own `todo:` commit first when they are substantial. Review fix-loop commits append to the section's candidate range (never amend), and the stamp names the whole range.
- **Commits are free; pushes are not.** Commit locally as often as you like. Push twice per section: the SHIP push, then the STAMP push. While iterating, run the affected checks only (`dotnet build` on the touched project, `dotnet test Photon.slnx --filter '<names>'`), not the whole sweep. A third push is allowed when it is named and the reason recorded.
- **Never mark `[x]` without evidence.** The Implementation Order row flips only after the review stamp exists.
- **User documents first.** A section that writes a user's file, library, preset, or settings is built to: atomic writes (write a temp file beside the target, flush, then replace), read back what was written, skip and report rather than drop or duplicate, and every destructive path confirmed. Its Test checkpoint exercises the failure path, not only the happy path: a read-only target, a locked file, a full disk, a malformed input file.
- **One source of truth for a value.** Any value the user trusts (a pixel, a coordinate, a color, an undo step) is computed in exactly one place, a model or service, and the view binds to it rather than deciding it. A calculation in code-behind that nothing verifies is a bug.
- **The design is the bar on surfaces.** `standards/design-contract.md` is binding: `docs/design/` is the source and the code implements it 1:1 (exact tokens, geometry within 1 DIP at 100, 150, and 200 percent, every state and theme the spec lists, approved goldens). A section that builds a surface proves it against the specs its `**Design:**` line names and against its review-approved goldens, never against the old-app captures under `docs/captures/<app>/` (a before record) and never against memory of what the other apps look like. Standard WPF with custom theming, never WPF-UI. A second color picker, undo stack, or settings writer in a second app is a defect, and so is moving code into `Photon.Core` before a second app needs it.
- **Edits are proven in both directions.** A section that changes a document proves the undo as well as the do, the save as well as the reopen, and what happens when the file cannot be written.

## The session does every step

One session validates, builds, gates, commits, obtains an independent review, and hands to stamping. It dispatches nobody to implement, gate, or keep records, and the one reviewer it invokes is external and advisory. Output discipline is load-bearing: bound every command (`dotnet build -v q` filtered to errors and warnings, `dotnet test --filter` on the touched tests, `tail`/`head` on logs, field extraction on JSON), because an unbounded dump lands in the one context that must carry it for the rest of the run. Full logs go under `build/` (gitignored).

## Workflow

### 1. Read the whole contract

Step 0 gave you the path, the section, and the dependency verdict. Read the entire TODO file, not just the section. The Goal, Current state, and Inputs carry context the section assumes. Read the sections this one depends on: their `Verified:` stamps tell you what actually shipped versus what was planned.

Confirm every dependency in the `Depends On` column is `[x]`. If one is not, stop and say so.

### 2. Validate the plan before building it

The section was written before the code existed. Check it still holds. Seven questions, each answered against the repository rather than from memory:

| Check | What you are asking | The failure it catches |
| ----- | ------------------- | ---------------------- |
| **Legitimacy** | Does a real source demand this: an observed defect, a format specification, a .NET or WPF contract, a user need? Or was it inferred? | Work invented by the plan, built faithfully, wanted by nobody |
| **Currency** | Do the projects, classes, XAML resources, settings keys, and package versions it names still exist and still behave that way? | A section pinned to a path or count that moved |
| **Consistency** | Do its own items agree with each other, with the file's Current state block, and with the sections it depends on? | Two items specifying different things; the later one silently wins |
| **Correctness** | Are the behaviors, API names, and format details it states actually what the source says? | A stale behavior ported confidently into code |
| **Sufficiency** | Is there enough here to build without inventing? Are the decisions made, or deferred into the implementer's lap? | A section that becomes a design session for an unattended executor |
| **Verifiability** | Can the `Test checkpoint` be executed and can it fail? Does a `Freeze check` name fixtures that exist? | A checkpoint that passes by being unfalsifiable |
| **Accuracy** | Is every concrete claim still literally true: every reference, path, count, ID, and deferral? | A section that reads as authoritative while quietly citing things that moved |

Ground each answer:

```bash
python scripts/todo-graph.py validate          # graph integrity, XREF reciprocity
python scripts/todo-claims.py                  # the TODOs' measured claims still hold
grep -rn "<class/file the section names>" src/ tests/
git log --oneline -5 -- <the paths the section touches>
```

#### Fact-check the section, claim by claim

`validate` proves the graph is well-formed. It cannot tell you whether a sentence is *true*. Walk the section (prose, items, checkpoint) and check every concrete assertion against the thing it describes. A TODO's authority comes from being accurate; one confidently wrong line costs more than ten vague ones, because nobody re-checks a statement that reads as settled.

| Claim in the section | Check it against |
| --- | --- |
| A project, class, method, XAML resource, command, or settings key | It exists, spelled that way, at that path |
| A count, size, version, or measurement | Re-derive it; these age fastest and are quoted most confidently |
| A commit SHA or run ID | It resolves |
| An `-> XREF:` reference | The target section exists, and points back |
| "Nothing exists yet" / "there is still no X" | X really does not exist |
| A quotation from the source or spec | It says that, verbatim, at that location |

#### Deferrals in both directions

```bash
python scripts/todo-graph.py query deferred
```

**Deferrals this section owns**: another section handed you this work, and it is part of your scope whether or not the checklist mentions it. It turns FATAL the moment this row flips, so it is not optional.

**Deferrals this section wrote**: re-read each one against today's repository, not the day it was written. Three things can be wrong with an open deferral, and only the first is caught by tooling:

- **The owner shipped it.** `validate` already makes this FATAL. Close it with `> **Resolved:**`.
- **The description has drifted.** The owner is still legitimately open, but the deferral describes a state that has since changed. Correct the text in place, or close it if the *reason* for deferring is gone even though the owner has not shipped.
- **The work was quietly done by someone else.** The owner never ticked its box, so it is not formally stale, but the thing is fixed. Verify it, then close the deferral **and** tick the owner's item: leaving the owner's box unticked recreates the same rot one level up.

Read the `Verified:` stamps on the sections this one depends on. They record what actually shipped, which is frequently narrower than what was planned: and a section built on the plan rather than on the stamp inherits the gap.

**Anything unclear at this point becomes a question you answer from the source, not a decision you defer.** Where the source is silent, take the industry-standard option, record that it is a default, and carry on with the cost of changing it noted. A section that stalls waiting for an answer is worse than one built on a recorded assumption.

### 3. Correct the section when validation fails

Findings from step 2 are fixed **in the TODO file**, before implementation, so the plan and the build never disagree in the record.

| Finding | Do this |
| ------- | ------- |
| Stale fact: a name, count, version, or path that moved | Correct it in place. Mark it `**Corrected YYYY-MM-DD:**` with what it said before and what the source says now. |
| Two items contradict | Resolve toward the source and the later decision. Say which one lost and why, in the item itself. |
| Item is unbuildable as written | Rewrite it to be concrete: name the file, class, or command. Vagueness is the defect. |
| Item is already true | Tick it and note that it shipped elsewhere, with the XREF. Do not rebuild it. |
| Item is genuinely wrong work | Do **not** silently drop it. Strike it with a stated reason, and if something must replace it, add that item. |
| `Test checkpoint` cannot fail | Rewrite it so it can. An unfalsifiable checkpoint is how a section gets stamped without being verified. |
| The whole section is wrong | Stop. Do not implement. Report what is wrong and what you propose, and let the user decide. |
| A **frozen** behavior looks wrong | Do **not** change it, in code or in the plan. Record the question for the operator with the proposed fix, and continue around it. |
| A reference, path, count, or ID is wrong | Correct it to what the source says, marked `**Corrected YYYY-MM-DD:**`. Never delete a wrong figure silently: the next reader needs to know it moved. |
| A deferral's owner has shipped it | Close it: replace `> **Deferred:**` with `> **Resolved:**` in place, keeping the text and XREF, adding the date and the commit. |
| A deferral's description has drifted | Correct the text in place. If the *reason* for deferring is gone, close it and say so, even though the owner has not shipped. |
| A deferral's work was done without its owner ticking it | Verify it, close the deferral, **and** tick the owner's item. Leaving the owner unticked moves the rot rather than fixing it. |

Two rules keep this honest:

- **Correct the plan, never the goalpost.** Narrowing a section so the code you were about to write happens to satisfy it is not validation, it is fitting the contract to the implementation. If the section demands more than you can deliver, the section wins.
- **Say what you changed.** The plan correction is reported alongside the implementation and appears in the commit body. A silent edit to the contract is indistinguishable from scope drift.

If step 2 finds nothing, say so in one line and move on: that is the expected outcome for a freshly written section, and the check costs little.

### 4. Build the corrected contract

Work the checklist top to bottom. Tick each item as its Done-when becomes true, in the file, as you go: the file is the record of progress, not a form filled in at the end.

- Count discipline: Dones carry per-item test deltas (which tests this item added, which cases it changed), never suite totals: a total typed mid-item goes stale when the next item lands tests. Totals are quoted once, from the commit being created (step 7).
- Build the cheaper substitute's failure into the work: the checkpoint must be able to catch the wrong thing, so build the test that distinguishes them.
- Keep the diff to the section. Adjacent wrongness gets filed with `add-todo`, not fixed in passing.
- UI sections: consume the shared styles, controls, and services named in `**Chrome:**`. A second color picker, progress indicator, or settings writer is a defect, not a shortcut.
- The stack is fixed (`AGENTS.md`): WPF with MVVM through CommunityToolkit.Mvvm, Microsoft.Extensions.DependencyInjection, and Serilog. A section that needs another dependency records the decision and its reason in the section before adding it.

### 4a. Build a surface to the design (UI sections)

Before writing any XAML for a section whose Fidelity line names a surface:

1. **The Design line validates.** The section carries one `**Design:**` line (grammar in `todo/README.md`, Surface fidelity) and `python scripts/todo-graph.py validate` reports no `design-*` finding for it. If the section is still listed in `todo/.design-baseline`, write its Design line now from the specs the surface needs (component READMEs under `docs/design/components/`, `docs/design/shell-layout.md` region anchors, `standards/ui.md` anchors), mark it `**Corrected YYYY-MM-DD:**`, and shrink the baseline in the same commit with `python scripts/todo-graph.py design-baseline`. A surface is never built from a section with no Design line.
2. **Design first.** A ref written `new surface: docs/design/<path>.md` means the spec does not exist: write it (README, `preview.html` card, the page regenerated with `python scripts/build-design-site.py` per `docs/design/EDITING.md`) as the section's first item, then cite it directly on the Design line. A look the spec does not describe goes into `docs/design/` first, never straight into XAML.
3. **Read the whole design input.** Every spec the Design line names, `docs/design/tokens.json` for every value they cite, `standards/design-contract.md`, and the design reference renders (`python scripts/render-design-reference.py --components <Comp>` writes `build/design-reference/<Comp>/<theme>-<density>.png`).
4. **Token keys only.** Every color through `DynamicResource` with a color token key (or `Photon.App.*` for the app accent), every size, spacing, radius, font, and duration through its token key. No literal, no private palette, no `StaticResource` color. `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` reports 0 new violations before the commit, and when the section removes recorded violations it shrinks the baseline with `--update-baseline` in the same range. Never run `--allow-add` from this skill.
5. **Every state, theme, Highlight, density, and scale.** Implement every state the specs list; add the section's scenarios to `tests/Photon.UI.VisualTests` (the harness of `D01 T01 §9`, once it ships) and produce the WPF renders under `build/wpf-renders/` with `pwsh scripts/visual-tests.ps1 -Filter <name>`. Hand them to review with the side-by-side report.
6. **Never approve a golden.** `docs/captures/golden/` is written only by `review-todo-section` after its `design-fidelity` lens passes. A render that differs from the spec is fixed in the code, or recorded as a `**Design deviation:**` line (grammar in `todo/README.md`) with a follow-up section that fixes the design or the code; there is no silent deviation.

### 5. Surface completeness (UI sections)

Before the checkpoint, account for **every control, menu item, dialog, command, and state** the section's design specs (its `**Design:**` line) list, each resolved to working (proven on the rendered surface) or deferred to a named, resolving section. A control disabled with a reason that names no section is missing, not deferred. `review-todo-section` refuses the stamp for an unaccounted control; decide here, not there.

### 6. Run the Test checkpoint, for real

Execute the checkpoint command and read the output. Quote the result in the commit body. If the checkpoint cannot run (no Windows host, no pinned .NET SDK, missing fixture), the section is not done: record what ran, what did not, and why, and stop without a stamp. A checkpoint half-run is not evidence.

Then run **every gate the section owes**, not only the checkpoint. The gate card is `.claude/skills/process-todo-section/gates.md`:

```powershell
pwsh scripts/check-all.ps1          # Debug and Release build, tests, TODO gates, guard self-test
dotnet test Photon.slnx             # the whole suite, not only the new tests
python scripts/todo-graph.py validate
python scripts/todo-claims.py       # the TODOs' measured claims still hold
```

**If a claim went stale, the section changed something a TODO had measured.** That is not a nuisance to silence: fix the claim *and* re-read the sentence it supports, in this commit, because the prose around a changed figure is usually wrong too.

While iterating, narrow with `dotnet test --filter`. Before committing, run the full sweep once: a section that passes its own filter and breaks another suite has not passed.

### 7. Commit and push the ship

Commit as one section commit with the evidence in the body:

```
<area>: <what now works> (<ref>)

<checkpoint output, quoted>
<plan corrections, if any>
```

Quote every suite count in the body from the commit being created: re-run the suites at this commit and quote those figures, never figures measured mid-item. Live-green quotes ride the same commit-time discipline: two non-simultaneous measurements never jointly satisfy one checkpoint.

Push the SHIP push. The commit must exist on the remote before the next step, because the independent reviewer reads the commit. Capture the remote head first (`BEFORE=$(git ls-remote origin refs/heads/main | cut -f1)`) and read CI back after it with `python scripts/review_prompt.py ci-wait <SHIP_SHA> --since $BEFORE`, and record its line in the run file: a red read-back is repaired before the review, never carried into it, by the bounded repair loop the review skill's push block states, escalating only a cause the tree cannot fix. After a repair, `<SHIP_SHA>` is the repaired head: re-run the checkpoint there and give step 8 that sha, because the pre-repair commit is not the candidate any more.

`ci-wait` reads the `plan-gates` workflow (`.github/workflows/plan.yml`) by default; a section whose paths the build workflow covers reads that one back too with `--workflow <name> --workflow-path .github/workflows/<file>.yml`, and records both lines.

### 8. Independent review, before the stamp

**An outside reviewer reads the commit before this session stamps its own work.** The session that built a section is the worst judge of whether it is right, and this step exists to break that.

```bash
python scripts/panel_slots.py exec independent --commit <SHIP_SHA>
```

It reviews read-only and changes nothing.

**The model is pinned in the `independent` slot of `.conclave/panel.toml`, not left to the machine's config.** `exec` runs `codex review --commit <SHIP_SHA>` with the slot's model and effort as `-c` overrides, enforces the slot timeout, and prints the resolved pin as its first stderr line; quote that line in the `Independent:` line. `~/.codex/config.toml` has a `model` key, and relying on it makes every stamp's `Review:` line unverifiable: a stamp records which reviewer read a commit, and a model taken from a config file anybody can edit is only as good as the config on the day somebody reads it back. Pinning it means the slot table at the stamped commit and the stamp together say exactly what reviewed what. Re-pinning is an edit to `.conclave/panel.toml` plus a fresh probe date, never an edit here, and stamps written under an earlier pin are left alone: they record what actually read those commits.

**`--commit` takes no review instructions.** The usage line prints `codex review --commit <SHA> [PROMPT]`, but supplying either a prompt string or `-` for stdin fails with `the argument '--commit <SHA>' cannot be used with '[PROMPT]'`. `--base <BRANCH>` and `--uncommitted` refuse a prompt the same way. Do not add one **on this command**.

**A bare prompt works.** `codex review "<instructions>"` with **no scope flag** is legal, reviews the latest commit when the working tree is clean, and obeys the instructions. Its price is that the scope is implicit: a bare prompt cannot pin a SHA, so it is only trustworthy with a clean tree immediately after the SHIP push, when the latest commit is the one under review. Check the summary names the right work before believing it. The pinned `--commit` pass above stays the pass of record, because a stamp needs a scope that cannot be misread.

Codex reads `AGENTS.md` from the repository root on its own, so the contract it needs is already in front of it: the paths table, the stack rules, and the proof types. **When a section needs review guidance the reviewer would not otherwise have, put it in the section's own `Test checkpoint` rather than in the command**, because the reviewer reads the section.

Then act on what it returns:

- **A finding that is right** gets fixed in a follow-up commit on the same section, and the fix is quoted in the stamp. Do not argue with a correct finding to avoid a second commit.
- **A finding that is wrong** gets one line in the stamp saying so and why. Record it; do not silently discard it.
- **A finding that is right but out of scope** gets filed with its own owner and dependency, per the guardrail below. Do not widen the section to absorb it.

If `codex` is unavailable on this machine, say so plainly in the report and in the stamp. A missing reviewer is a recorded gap, never a silent pass.

### 9. Stamp, then push the stamp

Invoke `review-todo-section` on the same ref. Review writes the stamp and flips the row; this skill never flips a row itself. The stamp records the independent review's outcome alongside the checkpoint evidence.

After the stamp lands, push the STAMP push (through the review skill's push block) and sync the plan:

```bash
python scripts/todo-graph.py plan --sync
```

### 10. Report

Tell the user plainly: what was built, what the checkpoint proved (quoted), what the independent review found and what was done about each finding, what plan corrections were made, what was filed rather than fixed, and where the stamp stands.

## Guardrails

- Do not implement a section you judged wrong. Correct it or stop.
- Do not widen the section. File adjacent work.
- Do not flip the Implementation Order row. Review owns that.
- Do not claim a checkpoint passed without running it: quote the output.
- Do not build a UI surface whose `**Design:**` line is missing or does not validate, or whose `new surface:` spec is not written into `docs/design/` first.
- Do not commit a new design-lint violation, run `design-lint.py --allow-add`, or write under `docs/captures/golden/`. Goldens are review's to approve.
- Do not end with the plan unsynced.
- Do not stamp before the independent review has run, or without recording that it could not.
- Do not discard a review finding silently. Fix it, refute it in the stamp, or file it.
