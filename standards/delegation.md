# Delegation

How the writer session routes work to cheaper subagents without lowering the bar. Operator decision 2026-10-01: "Delegate as much research, implementation, testing, documentation, and routine review as can reliably meet that bar to Claude Sonnet subagents running explicitly at high effort", with the lead "accountable for architecture, integration, and final acceptance, retaining stronger-model review for consequential design, security, privacy, data integrity, and critical correctness", and "never weaken requirements or claim equivalent quality merely because tests pass."

Delegation changes who reads and runs, never who writes or what ships. Every gate in `AGENTS.md`, every skill step, the independent GPT review, the panel, and the stamp run exactly as before. Cost is optimized only inside these rules. Operator decision 2026-10-02: "I am not confortable with having a sonnet writer", so no delegate writes code: source, XAML, scripts, tests, and build files are the lead's alone, and the `isotone-implementer` definition was removed. Operator decision the same day: "If you use sonnet as an implementer, make 100% sure that it does not weaken implementations." On 2026-10-17 the shape followed Conclave-SDK commit 4ca1af5: the `isotone-docs` definition, the last delegate that could write, was removed, and documentation prose returned to the lead. With no delegate writing, no delegated diff exists that could weaken an implementation.

## Subagents never write

Subagents read and run; they never write. Every Claude subagent declares an explicit `tools:` list without Edit, Write, MultiEdit, NotebookEdit or `*`. The main loop makes every change and verifies what subagents return.

`python scripts/panel_slots.py validate` refuses any `.claude/agents/*.md` definition that grants one of those tools or does not deny `Edit, Write, NotebookEdit, Agent`, and the `agent-gate` hook refuses every Agent call that would start a subagent able to write: a fork and every built-in agent, whatever model it names (Model and effort are pinned, and checked).

## Who is who

| Role | Runs | Owns |
| ---- | ---- | ---- |
| **Lead** | The writer session, `WRITER` in `scripts/panel_slots.py` (the `claude` route in `.conclave/reviewers.toml`) | Architecture, plan corrections, consequential code, integration, every commit and push, every record (`Started:`, findings, stamps, run files), final acceptance |
| **Delegates** | The `.claude/agents/*.md` definitions, each naming the delegate alias and effort itself (today `sonnet` at effort `high`, served as `claude-sonnet-5-5`, the `DELEGATE` pin in `scripts/panel_slots.py` that `delegate-probe` re-measures) | One bounded brief each; never a tracked change, a commit, a record, or a verdict |
| **Panel** | The reviewer `.conclave/reviewers.toml` routes for the `claude` writer, run by `scripts/review-dispatch.py` | Every recorded review verdict, unchanged; delegates share the writer's family, and the dispatcher refuses a reviewer of that family |

The delegates:

| Agent | Writes | Use it for |
| ----- | ------ | ---------- |
| `isotone-researcher` | nothing | Fact-checking a section's claims (`process-todo-section` step 2), locating callers and consumers, reading a format specification or Microsoft Learn, the competitor research pass (`review-todo-section` step 3, `plan-new-feature`, `groom-plan`) |
| `isotone-verifier` | `build/` only | Running the gates a section owes (`check-all`, the full suite, the TODO validators, design-lint, the checkpoint) into logs the lead reads back |
| `isotone-reviewer` | nothing | The first-pass sweep of `review-todo-section` step 2: candidate findings for the lead to verify |
| `code-explorer` | nothing | Ad hoc "where and how is X implemented" questions outside a section brief: call sites and subsystem maps as `file:line` conclusions |
| `debug-evidence` | nothing | The evidence for a bug before anyone forms a theory: logs around the failure, safe reproduction attempts, what changed recently |
| `git-runner` | nothing | Read-only git surveys: status, diff summaries, log and blame archaeology (the shell gate denies every git write) |
| `test-runner` | `build/` only | Running a named test or check command outside a section's gate run and reporting the counts and the exact failures |
| `mutation-tester` | a scratch folder outside the repository only | Proving a test can fail: each mutation the lead specifies, applied in a scratch copy of the candidate, the named command run, the file restored, and killed or survived reported per mutation |

The last five come from the Conclave-SDK `base` kit (four imported 2026-10-19, `mutation-tester` 2026-10-21), pinned here like the `isotone-*` definitions: the delegate effort, the denied edit tools, and the `delegate-shell-gate` hook. The kit's `mutation-tester` builds its copy with `git worktree add` and `git apply`, which the shell gate denies to every delegate, so Isotone's copy (operator decision 2026-10-21) builds it from `git ls-files` with a plain file copy into a scratch folder outside the repository and runs no git write. Kit subagents are refreshed by porting an SDK change by hand when `scripts/check-conclave-kits.py` reports it, never by `forge.py sync` (AGENTS.md: a sync would overwrite these adaptations), so after a port `python scripts/panel_slots.py validate` must pass before the session uses them.

## What the lead keeps

These never go to a delegate, whatever the cost, because a cheaper miss here is not recoverable by a later gate:

- Every change: source, XAML, scripts, tests (including test drafts), project and build files, XML doc comments, user guides, developer docs, changelog entries, and READMEs. No subagent writes (Subagents never write); a delegate may report facts or draft wording in its report, and the lead verifies them and writes the file.

- Plan validation verdicts and corrections to TODO text (`process-todo-section` steps 2 and 3); a researcher gathers the evidence, the lead judges it.
- Design of anything consequential: public `Isotone.Core` and `Isotone.UI` contracts, the document model, storage and file formats, settings storage, undo history, plugin and extension seams, threading and concurrency models.
- Security, privacy, and data-integrity code: file-format readers and writers, atomic saves, the original-file guard, credentials, update and download paths, anything that parses untrusted input.
- Integration: merging delegate output, resolving conflicts between slices, and the full-suite run at the commit.
- Every record: `Started:`, commits, pushes, the run file, findings files, `Verified:` stamps, attestations, the `[x]` flip, `todo/budget.json`, `todo/backlog.md`, `docs/captures/golden/`, baselines. No brief can make a record an owned path.
- Every review verdict. `isotone-reviewer` output is a list of candidates, never a lens verdict, and never replaces the lead's self-review, the independent pass, the GPT panel, or the architecture gate.
- `AGENTS.md`, `standards/`, skills, `.claude/`, `.conclave/`, hooks, and the TODO tooling.

When the right owner is unclear, the lead keeps it.

## The brief

Every delegation is one bounded brief. A brief that cannot be written this way is a sign the work is not delegable yet.

1. **Task**: one outcome, stated as the section or item it serves (`DNN TNN §N`, item text).
2. **Context**: the paths to read first and the facts already established, so the delegate does not repeat the lead's investigation; never a request to "explore the codebase".
3. **Scratch**: the `build/delegation/<task>/` directory its logs and notes go to. A brief never names a tracked path for a delegate to write.
4. **Acceptance criteria**: falsifiable, each with the command that proves it.
5. **Output**: the report contract in the agent definition, plus anything extra the lead needs.

## Parallel work

- Delegates run in parallel freely, on distinct questions; two delegates never investigate the same question.
- The lead makes no tracked edit while a delegate runs in the shared tree, so the delegate's scope check reads only what that delegate did.
- `isotone-verifier` runs after the lead's edits it verifies are done, never beside them.

## Accepting delegate output

The lead accepts nothing on the delegate's word. A delegate's output is a report, never a diff, and both steps below run for every delegate:

1. **Scope.** Before dispatching a delegate, `python scripts/weakening-scan.py --snapshot build/delegation/<task>/before.json`; after it returns, `python scripts/weakening-scan.py --scope build/delegation/<task>/before.json --` (no owned paths) lists every path whose content changed and a moved HEAD. It compares per file, so the user's own edits and a dirty file changed again read correctly. The snapshot also records every ref (branches, tags, the stash, remote-tracking refs), a hash of the local git configuration, and the remote's heads, and the check fails on any change to them: a delegate never commits, branches, tags, stashes, configures, or pushes, and this catches it however the command was spelled, a script file or an interpreter included. Beyond the git and GitHub writes the shell gate blocks, a delegate's shell is bound by instruction, so this check is what proves it wrote nothing. Attribution needs one delegate per snapshot, so two delegates running at once each get their own snapshot and the lead reads any finding against both.
2. **Evidence.** Re-run, or read the log of, every acceptance command. Evidence quoted in a commit body or stamp comes from a log file under `build/` the lead read itself, or from the lead's own run; a delegate's summary is never cited as proof. Facts and wording a delegate reports are checked against their cited source before the lead writes them anywhere.

The weakening scan, the line-by-line read, and red-before-green bind the lead's own diff through the section's gates and review; no delegate diff exists to accept.

## Escalation

- **Ambiguity** a delegate reports goes to the lead, which answers it from source, takes and records a justified default, or asks the operator. A delegate never resolves it alone.
- **A failed acceptance check** gets at most one corrected re-brief that names what failed and why. A second failure is not retried: the lead does the work itself, or stops and reports to the operator. Two failed briefs on one slice usually mean the slice was consequential or under-specified.
- **A delegate that wrote** (any finding from the scope check) failed its brief, whatever it wrote: the lead reads the change, discards it, does not use that delegate's report, and either re-briefs once, naming the write, or does the work itself.
- **A finding the lead cannot resolve** goes to the operator, and a red gate stays red until fixed. Weaker output is never accepted to save a round, and passing tests never stand in for review.

## What these controls are, and are not

Delegates are cooperative models that can err, cut corners, or drift from instructions; every control here is built to stop or detect that, and the rule that they never write exists because a passing suite hides exactly the shortcuts a writing delegate takes. They are not a security boundary against a delegate deliberately evading them: a subagent runs as the same operating-system user as the lead, with the same filesystem and network access, so a delegate set on evasion could rewrite a snapshot file, push to an explicit URL, or write where git does not look (an ignored path, `.git/hooks/`, a file outside the checkout). What closes that gap is the lead's own review of every diff and the independent GPT panel on every candidate, plus, if delegates are ever treated as untrusted, operating-system isolation (Claude Code's sandboxing or a separate user or container), which this repository does not configure today.

## Model and effort are pinned, and checked

- Every `.claude/agents/*.md` names the delegate alias and effort (`DELEGATE_ALIASES`, `DELEGATE_EFFORTS` in `scripts/panel_slots.py`); `python scripts/panel_slots.py validate` fails any definition that does not, and runs in `scripts/check-all.ps1` and the `plan-gates` workflow.
- The `PreToolUse` hook in `.claude/settings.json` (`panel_slots.py agent-gate`) is an allow-list: a pinned read-only `.claude/agents/` definition (no model override, the delegate pin, or `opus` to escalate). It denies everything else: a `fork` (it inherits the writer's tools, edit tools included), every built-in agent even at `model: opus` (each carries its own tools), a `haiku` model, the built-in `Explore` agent, a bare `model: sonnet` override (measured: it ran `claude-sonnet-5-5` at effort `medium`, 2026-10-01), and a built-in agent with no model override, because built-ins carry their own default model (`claude-code-guide` defaults to Haiku). It fails closed on an Agent call it cannot judge, and `validate` fails when the hook is missing from the settings.
- Every delegate definition carries a `PreToolUse` hook on its shell tools (`panel_slots.py delegate-shell-gate`) that allows git only as an allow-list of read-only subcommands (`status`, `diff`, `log`, `show`, `grep`, `ls-files`, `rev-parse`, and the like) plus the read forms of `stash`, `config`, `tag`, `branch`, and `remote`, so every write, alias, and unknown subcommand is denied, as is a `-c` override or flag that changes what git executes; it also denies GitHub calls, panel runs, baseline growth, and `--no-verify`, and reads every quoted run of a command line as a command of its own, so quoting hides nothing. It is defense in depth, not a sandbox: a delegate that wrote a script or called git from an interpreter would pass it, which is why the scope check compares refs, configuration, and the remote after every delegate, whatever ran. `validate` requires the verbatim hook block in every shell-capable definition's frontmatter and the verbatim `agent-gate` command in the project settings, refuses `disableAllHooks` in any settings file Claude Code reads, and runs the configured `agent-gate` command to prove it denies a Haiku call.
- Delegation runs only through the Agent tool, whose calls the session transcript records and `delegate-audit` reconciles. Headless runs (`claude -p --agent isotone-<name>`) are not a delegation route: no audit sees them, and they do not apply the definition's `effort` either (measured 2026-10-01: effort `medium`). The only headless runs are the probe and the delegated verification below, which check the wiring and delegate nothing.
- `python scripts/panel_slots.py delegate-audit` reads the session's subagent transcripts, reconciles them against every Agent call the session's own transcript records as started, and fails closed: a started agent with no transcript, an unreadable record in either transcript, a turn on Haiku, a turn below the pinned effort on any model, a model other than the delegate pin and the writer, and an explicit `opus` request served by anything but the writer. Only an Agent call refused before it ran (a hook denial, an unknown agent type, a permission refusal) is exempt; a subagent that started and failed still owes its transcript. A run that delegated records its audit line in the run file; exit 2 means there was nothing to audit, which proves nothing.
- `python scripts/panel_slots.py delegate-probe` asks Claude Code what the alias serves today, fails on drift from the pin, and refuses (exit 2) while `ANTHROPIC_DEFAULT_SONNET_MODEL` pins the alias in the environment or a settings `env` block, because a pinned alias would keep the probe green while newer releases went unseen. It then checks freshness: with `ANTHROPIC_API_KEY` set it compares the pin with the newest Sonnet in Anthropic's published model list and fails on a newer one; without a key the alias can only be as fresh as Claude Code's own mapping, so the probe refuses (exit 2) while Claude Code auto-update is off (`DISABLE_AUTOUPDATER`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, or `autoUpdates: false`). Run it after a Claude Code update and before a campaign. On drift to a newer stable Sonnet, re-pin `DELEGATE` in `scripts/panel_slots.py` to the served model with the probe date in its comment (the audit then refuses the old model as off-pin), add it to `RECORD_MODELS` in `scripts/todo-runs.py` if a record will name it, and re-run the delegated verification below; anything other than a newer stable Sonnet goes to the operator.
- New agent definitions load when a session starts. A session that creates or edits one verifies it from a fresh session.

### The delegated verification

After any change to the pin or the definitions, prove the wiring with a real delegated task in a fresh session, then audit it:

```bash
claude -p --model sonnet --effort high --permission-mode auto --output-format json --max-turns 6 "Spawn exactly one subagent with the Agent tool, subagent_type isotone-researcher, no model override, with this prompt: 'Report the subject line of git commit <sha> in this repository.' Then reply with only its Findings line." > build/delegation/verify/nested.json
python scripts/panel_slots.py delegate-audit --session <session_id from nested.json>
```

Green means the audit classifies the subagent `pinned` (served the `DELEGATE` model at the pinned effort) and exits 0.
