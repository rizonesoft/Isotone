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
