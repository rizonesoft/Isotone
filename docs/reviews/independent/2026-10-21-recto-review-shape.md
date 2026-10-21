## Round 1: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:10:05Z
- Effort: medium
- Lines: 30
- Digest: 5ba596b21e58871e

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:520` and `:567`: A numbered P3 finding causes unnumbered findings in the same lens to escape severity checking. Reproduced by passing this text to `check_panel_output`:

   ```text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
   - P1 a.py:2 deletes originals
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ```

   Actual result: `(True, 'four lenses, one verdict each; highest P3')`. Removing the numbered P3 makes the checker correctly refuse it. This allows the round-9 low-severity stop despite an explicit P1 finding. Reject mixed finding formats or include unnumbered findings in the severity floor.

### consistency: needs-attention

2. P3 `docs/reviews/run-records.md:5`: The present-tense wiring description still prescribes slots, Full rounds 1-2, and high-effort signoff/depth rounds. Reading this paragraph reproduces the contradiction with the new single medium-effort route and uniform loop. Update the introductory guidance while preserving historical round records.

### integration: approve

No additional findings.

### record: approve

No additional findings. The claimed local scheduled-task uninstall was not independently verified.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 1

1. Real. `check_panel_output` now counts every detail line under a needs-attention verdict: a numbered item, a column-0 list item, any column-0 line, and an indented line before the verdict's first finding are findings (untagged meaning P1), and only an indented line after a finding continues it, unless it opens with a tag. An understated `HIGHEST:` no longer fails the round (that would void valid verdicts as an outage); the PASS reason names the true floor, so it never ends `; highest P3` and no severity stop can rest on it. The repro now returns `highest P1 (line 7 declares P3, but the needs-attention verdict at line 1 holds a P1 finding)`; at `107539d` it returned `highest P3`. New self-test cases: `highest-unnumbered-list-counts`, `highest-column-0-prose-counts`, `highest-nested-tag-counts`, `highest-indented-lead-counts-p1`, `highest-continuation-keeps-p3`, `highest-understated-names-floor`; `python scripts/review_prompt.py --self-test` prints `476 cases, 0 failed`.
2. Real. The `Panel wiring:` paragraph in `docs/reviews/run-records.md` now describes the one medium-effort route and the 22-round loop, and names the old Full and Light slots as what earlier round lines record.

Record note: the task uninstall ran on this PC. `Get-ScheduledTask -TaskPath '\Isotone\'` listed `isotone-conclave-kits`, `isotone-delegate-probe`, `isotone-local-tools` before `pwsh .conclave/automations/install.ps1`, which printed `Removed isotone-conclave-kits: tasks.json no longer lists it`, and the two others after.

## Round 2: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:16:33Z
- Effort: medium
- Lines: 26
- Digest: f8603b24b026b76e

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:583`: Indented, untagged list items still escape the severity floor. Pass this text to `check_panel_output`:

   ```text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
     - a.py:2 deletes originals
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ```

   Actual result: `(True, 'four lenses, one verdict each; highest P3')`. `_LIST_ITEM_RE` recognizes bullets only at column zero, so the second finding becomes a continuation instead of an untagged P1. This incorrectly permits the round-9 severity stop. Recognize indented list items before deciding that a line continues another finding.

### consistency: approve

### integration: needs-attention

2. P2 `scripts/review_prompt.py:3250`: The bundle transcript validator still accepts only the old panel PASS shape. Four approve verdicts followed by `HIGHEST: none` produce `PASS four lenses, one verdict each; highest none`, but passing those bytes to `_bundle_transcript_ok` returns `False`. Both bundle emission and verification use this check, so even a clean review following the new prompt cannot complete the required portable-bundle handoff. Extend the accepted transcript grammar and cover the new checker outputs in bundle tests.

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 2

1. Real. A bullet at any depth under a needs-attention verdict now counts as a finding (`_LIST_ITEM_RE` takes leading whitespace); only indented prose after a finding continues it. Both prompts (`review-todo-section`'s panel prompt and `docs/review-round-prompt.md`) now say each finding is one numbered line, continued only by indented prose. The repro returns `highest P1 (...)`. New case: `highest-nested-untagged-bullet-counts`; `highest-continuation-keeps-p3` now continues with indented prose and a fenced block.
2. Real. `_BUNDLE_HOLDING_RES` accepts the panel PASS with its `; highest <P1|P2|P3|none>` suffix, or the floored form `; highest <floor> (line N declares <lower>, but the needs-attention verdict at line M holds a <floor> finding)`, and nothing after it. New cases: `bundle-transcript-highest-p3`, `-none`, `-floor`, `-floor-p3` (each the checker's own reason fed to `_bundle_transcript_ok`), and `bundle-transcript-highest-forged-tail-fails`. `python scripts/review_prompt.py --self-test` prints `482 cases, 0 failed`.

## Round 3: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:21:45Z
- Effort: medium
- Lines: 24
- Digest: 66de5ea84535e8f1

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:583`: An indented ordered-list item using `)` escapes the severity floor. Neither finding regex recognizes it, so an explicit P1 becomes continuation prose. Reproduce by passing this text to `check_panel_output`:

   ```text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
     2) P1 a.py:2 deletes originals
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ```

   Actual result: `(True, 'four lenses, one verdict each; highest P3')`. This satisfies the round-9 severity-stop condition despite the P1 finding. Removing the P1 tag also escapes the required untagged-P1 default. Recognize parenthesized ordered-list markers before classifying indented text as continuation, or reject that malformed finding format.

### consistency: approve

### integration: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 3

1. Real, and the third list shape in three rounds, so the family is closed rather than the shape: under a needs-attention verdict, a `P1`, `P2` or `P3` token anywhere on a detail line raises the floor to it, a line opening with any list marker at any depth (`-`, `*`, `+`, bullet glyphs, `2)`, `(b)`, `iv.`) starts a finding, a finding whose tag does not follow its marker is P1 even if a severity is named later, and only indented unmarked prose continues a finding. The repro returns `highest P1 (...)`; at `cc260cd` it returned `highest P3`. New cases: `highest-paren-number-counts`, `-paren-number-untagged-`, `-enclosed-letter-`, `-roman-`, `-glyph-`, `-tag-in-continuation-`, `-late-tag-on-finding-`; `python -W error::SyntaxWarning scripts/review_prompt.py --self-test` prints `489 cases, 0 failed`.

## Round 4: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:27:11Z
- Effort: medium
- Lines: 24
- Digest: 238a82afdc185fe5

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:104` and `:592`: Unrecognized indented list markers still bypass the untagged-P1 floor. Reproduced by passing this text to `check_panel_output`:

   ```text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
     **2.** a.py:2 deletes originals
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ```

   Actual result: `(True, 'four lenses, one verdict each; highest P3')`. Replacing `**2.**` with `10000)` produces the same result. Neither marker matches `_LIST_ITEM_RE`, so the untagged finding becomes continuation prose. This incorrectly permits the round-9 severity stop. Reject unsupported finding shapes or conservatively include them in the severity floor.

### consistency: approve

### integration: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 4

1. Real, and the fourth marker shape, so the rule is inverted rather than extended (same-family circuit breaker): continuation is now whitelisted, never inferred. Under a needs-attention verdict, an indented line continues a finding only when it is led by a letter that is not a list marker, or sits in, opens, or closes a fenced block; every other detail line starts a finding whatever its marker, and is P1 unless its tag follows the marker. A verdict that leaves a fence open counts as P1. Both prompts state the format. The repro (`**2.**` and `10000)`) returns `highest P1 (...)`; at `2513da8` it returned `highest P3`. New cases: `highest-bold-number-counts`, `-long-number-`, `-backtick-led-`, `-unclosed-fence-`; `python -W error::SyntaxWarning scripts/review_prompt.py --self-test` prints `493 cases, 0 failed`.

## Round 5: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:31:20Z
- Effort: medium
- Lines: 28
- Digest: 8863309778379dce

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:108` and `:609`: Fence handling toggles a boolean without matching the opener’s character or length. An unclosed fence therefore escapes the required P1 floor and permits the round-9 severity stop. Reproduce by passing this to `check_panel_output`:

   ````text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
      ```text
      - a.py:2 deletes originals
      ~~~
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ````

   Actual result: `(True, 'four lenses, one verdict each; highest P3')`. The tilde fence cannot close the backtick fence. Opening with four backticks and closing with three produces the same incorrect result. Track the opening delimiter and require a valid matching close; otherwise retain the P1 floor.

2. P1 `scripts/review_prompt.py:105` and `:608`: The continuation whitelist still accepts unsupported alphabetic list markers as prose. Replace the fenced portion above with `  aa) a.py:2 deletes originals`. The checker again returns `highest P3`: `aa)` misses `_LIST_ITEM_RE`, but passes `_PROSE_LEAD_RE`. This untagged finding should count as P1. Recognize or reject alphabetic list-marker shapes before granting continuation status.

### consistency: approve

### integration: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 5

1. Real. A fence inside a needs-attention verdict now records its opener (character and length), and only a bare run of the same character at least as long closes it (CommonMark), so `~~~` never closes a backtick fence and three backticks never close four; a fence left open still counts as P1. New cases: `highest-tilde-closes-backticks-counts`, `highest-short-close-counts`.
2. Real. Continuation is now a strict whitelist on the first token: after a finding, an indented line continues it only when its first token is a plain word (`[A-Za-z][A-Za-z'-]*` ending at most in `,` `;` `:`) or it opens a fence. `aa)`, `e.g.`, `iv.`, `**2.**`, digits, glyphs and backticks all start a finding, and the list-marker table is gone. A finding's tag is its first or second token. New cases: `highest-two-letter-marker-counts`, `highest-abbreviation-led-counts`; `python -W error::SyntaxWarning scripts/review_prompt.py --self-test` prints `497 cases, 0 failed`.

Self-review note: the first draft of this fix named its fence pattern `_FENCE_OPEN_RE`, which the prompt fence parser already defines later in the module, so the later definition shadowed it and every fenced block read as P1. The self-test caught it (`highest-continuation-keeps-p3`); the patterns are now `_MD_FENCE_OPEN_RE` and `_MD_FENCE_CLOSE_RE`.

## Round 6: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:37:40Z
- Effort: medium
- Lines: 26
- Digest: 9657ea0e633f633b

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:107` and `:616`: Invalid backtick fence openers bypass the severity floor. `_MD_FENCE_OPEN_RE` accepts backticks in the info string, treating subsequent untagged findings as fenced continuation. Reproduce by passing this to `check_panel_output`:

   ````text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
      ```not`a`fence
      - a.py:2 deletes originals
      ```
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ````

   Observed: `(True, 'four lenses, one verdict each; highest P3')`. The resulting PASS transcript also passes `_bundle_transcript_ok`. The invalid opener must not establish a continuation fence: the untagged bullet requires P1. This currently permits the round-9 severity stop despite that finding. Validate the complete fence opener before entering fence state and add this regression case.

### consistency: approve

### integration: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 6

1. Real. The fence opener now follows CommonMark: a backtick fence's info string holds no backtick (a tilde fence's may), so `` ```not`a`fence `` opens nothing and the bullet after it starts an untagged finding (P1). Valid openers (`` ```python ``, `~~~ info`) still quote their content. New case: `highest-backtick-info-string-counts`; `python -W error::SyntaxWarning scripts/review_prompt.py --self-test` prints `498 cases, 0 failed`.

## Round 7: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:40:39Z
- Effort: medium
- Lines: 26
- Digest: 843f62f09965eedb

### adversarial: needs-attention

1. P1 `scripts/review_prompt.py:110` and `:607`: An excessively indented delimiter closes a fence incorrectly, bypassing the unclosed-fence P1 floor. Pass this text to `check_panel_output` (the closing backticks have twelve leading spaces):

   ````text
   **adversarial: needs-attention**
   1. P3 a.py:1 typo
      ```text
      - a.py:2 deletes originals
               ```
   **consistency: approve**
   **integration: approve**
   **record: approve**
   HIGHEST: P3
   ````

   Observed result: `(True, 'four lenses, one verdict each; highest P3')`. `_bundle_transcript_ok` also accepts its PASS transcript. The repository’s `todo-graph.py::strip_fenced_code` identifies the same input as an unclosed fence starting at line 3. This permits the round-9 severity stop on malformed output that should retain the P1 floor. Constrain closing-fence indentation and add this regression case.

### consistency: approve

### integration: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 7

1. Real, and the third fence defect in three rounds (rounds 5, 6 and 7), so the fence state machine is removed rather than patched (same-family circuit breaker): a fence quotes nothing. Every line inside a fenced block takes the same continuation test as any other line (an indented line whose first token is a plain word continues a finding; a fence delimiter line itself is a continuation), so no opener, closer or indentation can hide a finding. A fenced repro full of list-like or code lines now denies the severity stop, which costs a round at most and never grants a wrong stop. Both prompts tell the reviewer that a line inside a fenced block counts. New cases: `highest-over-indented-close-counts`, `highest-closed-fence-content-counts`; `python -W error::SyntaxWarning scripts/review_prompt.py --self-test` prints `500 cases, 0 failed`.

## Round 8: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:45:41Z
- Effort: medium
- Lines: 12
- Digest: 04157375ee562c8b

### adversarial: approve

### consistency: needs-attention

1. P3 `standards/delegation.md:5` still attributes the delegation rules to “Conclave-SDK commit 4ca1af5”, despite the requested removal of SDK wording from standards and the equivalent cleanup in AGENTS.md. Reproduce with `rg -n 'Conclave-SDK' standards/delegation.md`. Preserve the dated delegation decision while removing the SDK attribution.

### integration: approve

### record: approve

HIGHEST: P3
OVERALL: needs-attention

## Response to round 8

1. Real. `standards/delegation.md` keeps the dated 2026-10-17 decision and drops the SDK commit attribution. A sweep (`git grep -n -i -E 'conclave.sdk|4ca1af5|911c256|forge\.py|kit-drift|check-conclave'`, excluding review and phase-run history and the changelog) leaves only AGENTS.md's statement that the link was cut, the automations README naming the removed task, and the dated correction in `todo/00-workspace/TODO-01-dev-automation.md`, all intended.

## Round 9: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T17:47:52Z
- Effort: medium
- Lines: 10
- Digest: 7ae2066ac3dbbb21

### adversarial: approve

### consistency: approve

### integration: approve

### record: approve

HIGHEST: none
OVERALL: approve
