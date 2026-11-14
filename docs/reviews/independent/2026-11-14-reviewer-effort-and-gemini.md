## Round 1: carbon (`gemini-pro-orchestrator` via `agy`)

- Writer: codex
- Run: 2026-11-14T20:49:27Z
- Candidate: 03c639fd7914bf87df2c0bc4edaed8712845115c
- Lenses: adversarial, consistency, integration, quality, optimization, source-defect, docs-drift
- Lines: 54
- Digest: 56e5573e7105b585

### `adversarial`

Verdict: `advisory`

1. `P3` `scripts/review-dispatch.py:551` ([review-dispatch.py](file:///D:/Isotone/scripts/review-dispatch.py#L548-L556)) and `scripts/review-dispatch.py:202` ([review-dispatch.py](file:///D:/Isotone/scripts/review-dispatch.py#L196-L205)): When `appended` is `True`, `review()` overwrites the resolved `prompt_file` with `tmp / "prompt.md"` on an unresolved `tempfile.mkdtemp()` path, so `command()` (`scripts/review-dispatch.py:224`, [review-dispatch.py](file:///D:/Isotone/scripts/review-dispatch.py#L223-L227)) embeds the unresolved path in `-p=Follow the review instructions in the file ...` (used for `.cmd`/`.bat` shims and prompts over `ARGV_PROMPT_LIMIT`) while `agy_review_settings()` writes `read_file({Path(prompt_path).resolve().as_posix()})` into `agy-settings.json`; additionally, an unscheduled `--prompt` path containing parentheses produces an unescaped `read_file(...)` token. Reproduce on Windows where `%TEMP%` uses an 8.3 short segment (for example `C:\Users\FIRSTL~1\AppData\Local\Temp`) or a directory junction and invoke `review-dispatch.py` with an `agy.cmd` shim or a prompt over 24,000 characters: `-p` instructs `agy` to read the unresolved backslash path while `permissions.allow` lists only the canonicalized path.

### `consistency`

Verdict: `advisory`

1. `P3` `scripts/review_pin.py:398` ([review_pin.py](file:///D:/Isotone/scripts/review_pin.py#L397-L422)): `check_step_keys()` still formats step key refusals using `need = {"required": "lenses, and may set effort", "optional": "only effort and lenses", "none": "only effort"}` without naming `effort_by_cli` or `followup_effort_by_cli`, and `check_step_effort()` aborts on the first invalid key in `("effort_by_cli", "followup_effort_by_cli")` instead of collecting independent field faults per step under `review_pin.py --check --all` (`scripts/review_pin.py:302`, [review_pin.py](file:///D:/Isotone/scripts/review_pin.py#L302-L307)). Reproduce by running `python scripts/review_pin.py --check --all` on a pin whose `[[schedule.rounds]]` entry sets both `effort_by_cli = {}` and `followup_effort_by_cli = {}` (only `effort_by_cli` is reported), or `completion = 1` (refusal says `[schedule] completion needs only effort`).

### `integration`

Verdict: `needs-attention`

1. `P2` `scripts/review-dispatch.py:524` ([review-dispatch.py](file:///D:/Isotone/scripts/review-dispatch.py#L523-L556)): `review()` writes `agy-settings.json` (`scripts/review-dispatch.py:553-555`) and `command()` passes `--settings .../agy-settings.json` (`scripts/review-dispatch.py:225-226`, [review-dispatch.py](file:///D:/Isotone/scripts/review-dispatch.py#L225-L227)) unconditionally whenever `reviewer["cli"] == "agy"`, restricting session Git commands to exact `git --no-pager show --no-ext-diff --no-textconv ...` and `git --no-pager diff --no-ext-diff --no-textconv ...` invocations (`scripts/review-dispatch.py:198-203`, [review-dispatch.py](file:///D:/Isotone/scripts/review-dispatch.py#L198-L203)), yet the prompt addendum instructing headless `agy` to use those exact command shapes (`scripts/review-dispatch.py:526-532`) is gated inside `if appended:`. Whenever `appended` is `False` -- which happens on every dispatch under a valid `schema_version = 1` pin without `[schedule]` and on every `--kind completion` pass under a rotation `[schedule]` (where `[schedule.completion]` forbids `lenses` and `three_pass` is `False`) -- headless `agy` receives only the base prompt (`docs/review-round-prompt.md:11`, [review-round-prompt.md](file:///D:/Isotone/docs/review-round-prompt.md#L11), or `docs/completion-review-prompt.md:11`, [completion-review-prompt.md](file:///D:/Isotone/docs/completion-review-prompt.md#L11), which tell it to run `git show` or `git diff`), hits headless permission denial on Git inspection, and fails or returns `blocked`. Reproduce by running `review-dispatch.py --writer codex --prompt <prompt>` against a valid pin routing `codex = ["carbon"]` (`cli = "agy"`) either with no `[schedule]` or with a rotation `[schedule]` and `--kind completion --candidate <40-char-sha>`: `--settings` enforces the `--no-pager --no-ext-diff --no-textconv` regexes while the prompt sent to `agy` omits the `Read-only headless review` instructions.
2. `P3` `scripts/lib/todo_graph.py:588` ([todo_graph.py](file:///D:/Isotone/scripts/lib/todo_graph.py#L586-L596)): In `schedule_ok()`, `reviewer_cli(entry, candidate=base)` defaults `candidate` to `base` (`data["plan"]["candidate"]`) when resolving the routed CLI of failed completion, reconciliation, or round attempts (`entry.get("cli")` is `None`). Under `three-pass` (`three_pass == True`) the pin is frozen at `base`, but for a rotation receipt `section_pin_sha()` and `receipt_data_ok()` (`scripts/lib/todo_graph.py:577` and `scripts/lib/todo_graph.py:990`, [todo_graph.py](file:///D:/Isotone/scripts/lib/todo_graph.py#L990-L1005)) bind `data["schedule"]` to `stamp_sha` (`data["implementation_sha"]`) unless the pin later switched to `three-pass`. Reproduce by replaying `schedule_ok()` on a rotation receipt whose route changed between `plan.candidate` and `implementation_sha` with a failed `## Round 1: none` entry: `reviewer_cli()` reads the route from `plan.candidate` instead of `data.get("schedule_sha", data["implementation_sha"])`.

### `quality`

Verdict: `advisory`

1. `P3` `scripts/tests/test_three_pass.py:616` ([test_three_pass.py](file:///D:/Isotone/scripts/tests/test_three_pass.py#L616-L640)) and `scripts/tests/test_review_dispatch.py:1333` ([test_review_dispatch.py](file:///D:/Isotone/scripts/tests/test_review_dispatch.py#L1333-L1356)): `test_scoped_efforts_dispatch_and_replay_failed_attempts_and_followups` validates follow-up round replay in `todo_graph.schedule_ok()` only by writing to a non-section path (`docs/reviews/independent/scoped.md`) and mocking `todo_graph.three_pass_ok` to a no-op (since `three_pass_ok` forbids two returned rounds on a section), while `test_review_dispatch.py` tests `agy` session permissions only when `appended` is `True`, leaving the unscheduled and rotation-completion `agy` paths (`appended == False`) untested. Reproduce by inspecting `test_review_dispatch.py:1333-1356`, which never asserts the `Read-only headless review:` prompt block on an unscheduled or rotation-completion `agy` run.

### `optimization`

Verdict: `approve`

No findings.

### `source-defect`

Verdict: `approve`

No findings.

### `docs-drift`

Verdict: `needs-attention`

1. `P2` `scripts/review_pin.py:33` ([review_pin.py](file:///D:/Isotone/scripts/review_pin.py#L33-L36)): The module docstring still states the pre-change rule: ``An Antigravity reviewer's model name must end with every effort the schedule sets. `effort` is optional everywhere: with a schedule, the step alone decides, and a step without one passes no effort to the reviewer's CLI, whose own configuration then decides``. This range added `effort_by_cli` and `followup_effort_by_cli` (`scripts/review_pin.py:68` and `scripts/review_pin.py:411-421`, [review_pin.py](file:///D:/Isotone/scripts/review_pin.py#L411-L421)) so the schedule sets `medium` and `low` for `codex` in `.conclave/reviewers.toml` (`reviewers.toml:45-59`, [reviewers.toml](file:///D:/Isotone/.conclave/reviewers.toml#L45-L59)) while the Antigravity reviewer `gemini-pro-orchestrator` (`reviewers.toml:26`, [reviewers.toml](file:///D:/Isotone/.conclave/reviewers.toml#L24-L26)) carries no `-medium` or `-low` suffix (`check_agy_effort()` at `scripts/review_pin.py:439-443`, [review_pin.py](file:///D:/Isotone/scripts/review_pin.py#L439-L443), applies only to un-scoped `step["effort"]`), and the schema overview in `scripts/review_pin.py:14-36` never documents `effort_by_cli` or `followup_effort_by_cli`. Reproduce by comparing `scripts/review_pin.py:33-35` with `.conclave/reviewers.toml:24-59` and `python scripts/review_pin.py --check`, which passes on `gemini-pro-orchestrator` despite scheduled `medium` and `low` efforts.
2. `P2` `scripts/review_pin.py:726` ([review_pin.py](file:///D:/Isotone/scripts/review_pin.py#L721-L742)): Immediately below the lines updated in `scheduled()` (`scripts/review_pin.py:722-724`), the docstring still states: ``Three-pass: the pass's lenses with its conditional ones (`lenses_for`); the one round's position is 1.`` In `scripts/review_pin.py:739-741`, `three-pass` computes `position = len(returned) + 1` and passes `position > 1` to `step_effort(schedule["rounds"][0], reviewer_cli, position > 1)` specifically so follow-up standalone rounds under the `three-pass` pin advance past position 1 (`2`, `3`, ...) and take `followup_effort_by_cli`. Reproduce by calling `review_pin.scheduled(schedule, "round", [returned_round], False, reviewer_cli="codex")` on `.conclave/reviewers.toml` (as `scripts/tests/test_three_pass.py:630`, [test_three_pass.py](file:///D:/Isotone/scripts/tests/test_three_pass.py#L630-L631), does on round 2), which returns `position == 2` and `effort == "low"`.

LENS adversarial: findings
LENS consistency: findings
LENS integration: findings
LENS quality: findings
LENS optimization: clean
LENS source-defect: clean
LENS docs-drift: findings

HIGHEST: P2
OVERALL: needs-attention

## Response to round 1

The returned Gemini review is valid and blocking. The headless route delivered all seven lens verdicts, `HIGHEST: P2` and `OVERALL: needs-attention` through the dispatcher on `gemini-pro-orchestrator`, with no effort override or fallback. A timeout remains a failed attempt; the earlier 300-second probe is not approval.

- Integration P2: confirmed and fixed. The headless command instructions now accompany every Antigravity invocation, including unscheduled reviews and rotation completion. Regression tests for both previously failed, then passed.
- Docs-drift P2 findings: confirmed and fixed. The schema overview now distinguishes scalar from CLI-scoped effort, and the scheduler documents standalone follow-up positions separately from the one-round section contract.
- Adversarial P3: canonicalized the temporary directory and the file pointer, matching the permission target. A path containing spaces, parentheses and a parent segment is covered by a regression. No undocumented permission escaping was added; the operator subsequently retired the Gemini reviewer, so no follow-up live attempt was run.
- Consistency P3: confirmed and fixed. Step diagnostics list the new keys, and all-fault validation checks scoped effort fields independently. A regression with two invalid maps failed before the fix and passes afterward.
- Integration P3: confirmed and fixed. Failed rotation attempts resolve the route at the receipt's schedule or implementation commit, with a regression that changes the route after plan review.
- Quality P3: added coverage for unscheduled and rotation-completion instructions and a real section dispatch sequence with medium plan/round/completion and low reconciliation. Standalone follow-up replay remains a separate scheduler test; the section contract still refuses two returned implementation rounds.

Validation before the follow-up: 40 reviewer-pin tests and 91 dispatcher tests passed (two platform-specific skips). The section and graph suites are rerun for the receipt change. No LSP diagnostics tool is exposed in this session. No native code changed.

## Operator supersession

The operator restored Claude and Antigravity as the only writers and Codex as the only reviewer. The Gemini route and Codex campaign integration are retired. This record preserves the returned blocking review and does not claim approval of subsequent changes.
