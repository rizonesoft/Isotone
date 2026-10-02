# Delegation

How the writer session routes work to cheaper subagents without lowering the bar. Operator decision 2026-10-01: "Delegate as much research, implementation, testing, documentation, and routine review as can reliably meet that bar to Claude Sonnet subagents running explicitly at high effort", with the lead "accountable for architecture, integration, and final acceptance, retaining stronger-model review for consequential design, security, privacy, data integrity, and critical correctness", and "never weaken requirements or claim equivalent quality merely because tests pass."

Delegation changes who types, never what ships. Every gate in `AGENTS.md`, every skill step, the independent GPT review, the panel, and the stamp run exactly as before. Cost is optimized only inside these rules. Operator decision 2026-10-02: "I am not confortable with having a sonnet writer", so no delegate writes code: source, XAML, scripts, tests, and build files are the lead's alone, and the `isotone-implementer` definition was removed. Operator decision the same day: "If you use sonnet as an implementer, make 100% sure that it does not weaken implementations." So no delegated diff is accepted until the lead has proven it does not weaken anything (Accepting delegate output, below).

## Who is who

| Role | Runs | Owns |
| ---- | ---- | ---- |
| **Lead** | The writer session, the `[writer]` model in `.conclave/panel.toml` | Architecture, plan corrections, consequential code, integration, every commit and push, every record (`Started:`, findings, stamps, run files), final acceptance |
| **Delegates** | The `.claude/agents/isotone-*.md` definitions, each pinned to the `[delegate]` alias and effort in `.conclave/panel.toml` (today `sonnet`, served as `claude-sonnet-5-5`, effort `high`) | One bounded brief each; never a commit, a record, or a verdict |
| **Panel** | The GPT slots in `.conclave/panel.toml` | Every recorded review verdict, unchanged; delegates share the writer's family, so `panel_slots.py` keeps them off every slot |

The delegates:

| Agent | Writes | Use it for |
| ----- | ------ | ---------- |
| `isotone-researcher` | nothing | Fact-checking a section's claims (`process-todo-section` step 2), locating callers and consumers, reading a format specification or Microsoft Learn, the competitor research pass (`review-todo-section` step 3, `plan-new-feature`, `groom-plan`) |
| `isotone-verifier` | `build/` only | Running the gates a section owes (`check-all`, the full suite, the TODO validators, design-lint, the checkpoint) into logs the lead reads back |
| `isotone-docs` | its owned Markdown paths | User guide, developer docs, changelog entries; never a code file (no XML doc comments) |
| `isotone-reviewer` | nothing | The first-pass sweep of `review-todo-section` step 2: candidate findings for the lead to verify |

## What the lead keeps

These never go to a delegate, whatever the cost, because a cheaper miss here is not recoverable by a later gate:

- All code: source, XAML, scripts, tests (including test drafts), project and build files, and XML doc comments. No delegate writes code (operator decision 2026-10-02), and `python scripts/panel_slots.py validate` refuses any definition other than `isotone-docs` that can edit or write files.

- Plan validation verdicts and corrections to TODO text (`process-todo-section` steps 2 and 3); a researcher gathers the evidence, the lead judges it.
- Design of anything consequential: public `Isotone.Core` and `Isotone.UI` contracts, the document model, storage and file formats, settings storage, undo history, plugin and extension seams, threading and concurrency models.
- Security, privacy, and data-integrity code: file-format readers and writers, atomic saves, the original-file guard, credentials, update and download paths, anything that parses untrusted input.
- Integration: merging delegate output, resolving conflicts between slices, and the full-suite run at the commit.
- Every record: `Started:`, commits, pushes, the run file, findings files, `Verified:` stamps, attestations, the `[x]` flip, `todo/budget.json`, `todo/backlog.md`, `docs/captures/golden/`, baselines. No brief can make a record an owned path.
- Every review verdict. `isotone-reviewer` output is a list of candidates, never a lens verdict, and never replaces the lead's self-review, the independent `codex review`, the GPT panel, or the architecture gate.
- `AGENTS.md`, `standards/`, skills, `.claude/`, `.conclave/`, hooks, and the TODO tooling, except as an owned path in a brief the lead then reviews line by line.

When the right owner is unclear, the lead keeps it.

## The brief

Every delegation is one bounded brief. A brief that cannot be written this way is a sign the work is not delegable yet.

1. **Task**: one outcome, stated as the section or item it serves (`DNN TNN §N`, item text).
2. **Context**: the paths to read first and the facts already established, so the delegate does not repeat the lead's investigation; never a request to "explore the codebase".
3. **Owned paths**: the exact files or directories the delegate may write. Write ownership never overlaps between delegates running at the same time, and never overlaps the lead's own edits.
4. **Acceptance criteria**: falsifiable, each with the command that proves it.
5. **Output**: the report contract in the agent definition, plus anything extra the lead needs.

## Parallel work

- Read-only delegates (`isotone-researcher`, `isotone-reviewer`) run in parallel freely, on distinct questions; two delegates never investigate the same question.
- The shared working tree holds at most one writer at a time: one writing delegate, with the lead not editing meanwhile, so every change in it is attributable. Writing delegates that run in parallel each get `isolation: worktree`, with disjoint owned paths; each is scope-checked in its own worktree, and the lead integrates the results. Read-only delegates may run beside a worktree writer, never beside a shared-tree writer, because their scope check would read the writer's changes as theirs.
- `isotone-verifier` runs after the writers it verifies have returned, never beside them.

## Accepting delegate output

The lead accepts nothing on the delegate's word, and passing tests never prove a delegated change is not weaker than the section asks. Every step below runs for the one writing delegate, `isotone-docs`, before its work joins the candidate, and steps 1 and 5 run for every read-only delegate too:

1. **Scope.** Before dispatching a delegate into the shared tree, `python scripts/weakening-scan.py --snapshot build/delegation/<task>/before.json`; after it returns, `python scripts/weakening-scan.py --scope build/delegation/<task>/before.json -- <owned paths>` lists every path whose content changed outside that delegate's own owned paths, and a moved HEAD. It compares per file, so the user's own edits and a dirty file changed again read correctly. The snapshot also records every ref (branches, tags, the stash, remote-tracking refs), a hash of the local git configuration, and the remote's heads, and the check fails on any change to them: a delegate never commits, branches, tags, stashes, configures, or pushes, and this catches it however the command was spelled, a script file or an interpreter included. A delegate that ran in its own worktree is checked with `--scope build/delegation/<task>/before.json --tree <its worktree> -- <owned paths>`, taken from a snapshot made before it was dispatched. Read-only delegates run the same check with no owned paths: beyond the git and GitHub writes the shell gate blocks, their shell is bound by instruction, so this check is what proves they wrote nothing. Attribution needs one writer per tree, so the check is never run over a union of two delegates' paths (Parallel work).
2. **Weakening scan.** `python scripts/weakening-scan.py --base <rev before the delegate ran> -- <owned paths>` lists every hunk that deletes or relaxes a test, assertion, guard, or error path, adds a skip, a warning suppression, a catch-all, a stub, or a bypass, changes a tolerance, threshold, or timeout, grows a baseline, or edits an existing test or build setting. Each signal is reverted, or justified in one line of the commit body (`Weakening scan: <kind> <path>:<line> -- <why>`); an unjustifiable one fails the brief. The delegate's weakening ledger is cross-checked against the scan: a signal the ledger did not declare fails the brief, whatever the reason.
3. **The whole diff, line by line**, against the section rather than the brief: every requirement met in full (no input refused that the section accepts, no case special-cased, no failure path left unexercised), every existing behavior intact, every check the section names still present. A clean scan narrows where to look; it never replaces this read.
4. **Red before green.** Every test the delegate added or changed must be shown to fail when the behavior it covers is broken, and the failing run is quoted. For a test of new behavior the delegate implemented, the break is the delegate's implementation reverted. For a test of behavior that already existed, or of code the lead wrote (a delegate may draft tests for consequential code), the lead names a fault before running it: the guard removed, the condition inverted, the call dropped, the written byte changed. The lead (or an `isotone-verifier` in a worktree) runs the test against the broken code. A test that no plausible fault in its target makes fail proves nothing and fails the brief.
5. **Evidence.** Re-run, or read the log of, every acceptance command. Evidence quoted in a commit body or stamp comes from a log file under `build/` the lead read itself, or from the lead's own run; a delegate's summary is never cited as proof.

No code is ever accepted from a delegate on the strength of these steps: the lead writes it (What the lead keeps).

## Escalation

- **Ambiguity** a delegate reports goes to the lead, which answers it from source, takes and records a justified default, or asks the operator. A delegate never resolves it alone.
- **A failed acceptance check** gets at most one corrected re-brief that names what failed and why. A second failure is not retried: the lead does the work itself, or stops and reports to the operator. Two failed briefs on one slice usually mean the slice was consequential or under-specified.
- **A weakened diff** (an undeclared weakening signal, a test that passes without the implementation, a requirement met in a narrower form) is a failed brief, never a fix-up: the lead reverts the delegate's change and either re-briefs once, naming the weakening, or does the slice itself.
- **A finding the lead cannot resolve** goes to the operator, and a red gate stays red until fixed. Weaker output is never accepted to save a round, and passing tests never stand in for review.

## What these controls are, and are not

Delegates are cooperative models that can err, cut corners, or drift from instructions; every control here is built to stop or detect that, and the weakening rules exist because a passing suite hides exactly that kind of shortcut. They are not a security boundary against a delegate deliberately evading them: a subagent runs as the same operating-system user as the lead, with the same filesystem and network access, so a delegate set on evasion could rewrite a snapshot file, push to an explicit URL, or write where git does not look (an ignored path, `.git/hooks/`, a file outside the checkout). What closes that gap is the lead's own review of every diff and the independent GPT panel on every candidate, plus, if delegates are ever treated as untrusted, operating-system isolation (Claude Code's sandboxing or a separate user or container), which this repository does not configure today.

## Model and effort are pinned, and checked

- Every `.claude/agents/*.md` names the `[delegate]` alias and effort; `python scripts/panel_slots.py validate` fails any definition that does not, and runs in `scripts/check-all.ps1` and the `plan-gates` workflow.
- The `PreToolUse` hook in `.claude/settings.json` (`panel_slots.py agent-gate`) is an allow-list: a pinned `isotone-*` definition (no model override, the delegate pin, or `opus` to escalate), a `fork` (it inherits the writer), or any other agent type with an explicit `model: opus`. It denies everything else: a `haiku` model, the built-in `Explore` agent, a bare `model: sonnet` override (measured: it ran `claude-sonnet-5-5` at effort `medium`, 2026-10-01), and a built-in agent with no model override, because built-ins carry their own default model (`claude-code-guide` defaults to Haiku). It fails closed on an Agent call it cannot judge, and `validate` fails when the hook is missing from the settings.
- Every delegate definition carries a `PreToolUse` hook on its shell tools (`panel_slots.py delegate-shell-gate`) that allows git only as an allow-list of read-only subcommands (`status`, `diff`, `log`, `show`, `grep`, `ls-files`, `rev-parse`, and the like) plus the read forms of `stash`, `config`, `tag`, `branch`, and `remote`, so every write, alias, and unknown subcommand is denied, as is a `-c` override or flag that changes what git executes; it also denies GitHub calls, panel runs, baseline growth, and `--no-verify`, and reads every quoted run of a command line as a command of its own, so quoting hides nothing. It is defense in depth, not a sandbox: a delegate that wrote a script or called git from an interpreter would pass it, which is why the scope check compares refs, configuration, and the remote after every delegate, whatever ran. `validate` requires the verbatim hook block in every shell-capable definition's frontmatter and the verbatim `agent-gate` command in the project settings, refuses `disableAllHooks` in any settings file Claude Code reads, and runs the configured `agent-gate` command to prove it denies a Haiku call.
- Delegation runs only through the Agent tool, whose calls the session transcript records and `delegate-audit` reconciles. Headless runs (`claude -p --agent isotone-<name>`) are not a delegation route: no audit sees them, and they do not apply the definition's `effort` either (measured 2026-10-01: effort `medium`). The only headless runs are the probe and the delegated verification below, which check the wiring and delegate nothing.
- `python scripts/panel_slots.py delegate-audit` reads the session's subagent transcripts, reconciles them against every Agent call the session's own transcript records as started, and fails closed: a started agent with no transcript, an unreadable record in either transcript, a turn on Haiku, a turn below the pinned effort on any model, a model other than the delegate pin and the writer, and an explicit `opus` request served by anything but the writer. Only an Agent call refused before it ran (a hook denial, an unknown agent type, a permission refusal) is exempt; a subagent that started and failed still owes its transcript. A run that delegated records its audit line in the run file; exit 2 means there was nothing to audit, which proves nothing.
- `python scripts/panel_slots.py delegate-probe` asks Claude Code what the alias serves today, fails on drift from the pin, and refuses (exit 2) while `ANTHROPIC_DEFAULT_SONNET_MODEL` pins the alias in the environment or a settings `env` block, because a pinned alias would keep the probe green while newer releases went unseen. It then checks freshness: with `ANTHROPIC_API_KEY` set it compares the pin with the newest Sonnet in Anthropic's published model list and fails on a newer one; without a key the alias can only be as fresh as Claude Code's own mapping, so the probe refuses (exit 2) while Claude Code auto-update is off (`DISABLE_AUTOUPDATER`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, or `autoUpdates: false`). Run it after a Claude Code update and before a campaign. On drift to a newer stable Sonnet, register the model in `.conclave/panel.toml` with the probe date, re-pin `[delegate] model`, retire the previous pin's entry (`validate` refuses a live model of the writer's family that is neither the writer nor the delegate, so an old pin can never pass an audit), and re-run the delegated verification below; anything other than a newer stable Sonnet goes to the operator.
- New agent definitions load when a session starts. A session that creates or edits one verifies it from a fresh session.

### The delegated verification

After any change to the pin or the definitions, prove the wiring with a real delegated task in a fresh session, then audit it:

```bash
claude -p --model sonnet --effort high --permission-mode auto --output-format json --max-turns 6 "Spawn exactly one subagent with the Agent tool, subagent_type isotone-researcher, no model override, with this prompt: 'Report the subject line of git commit <sha> in this repository.' Then reply with only its Findings line." > build/delegation/verify/nested.json
python scripts/panel_slots.py delegate-audit --session <session_id from nested.json>
```

Green means the audit classifies the subagent `pinned` (served the `[delegate]` model at the pinned effort) and exits 0.
