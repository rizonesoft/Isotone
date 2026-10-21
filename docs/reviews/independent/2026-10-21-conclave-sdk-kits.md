## Round 1: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T00:31:53Z
- Effort: high
- Lines: 25
- Digest: f08bbdba102e3620

## adversarial: needs-attention

1. **[P2] Query failures still block the session silently.** `scripts/campaign_guard.py:259` converts a timeout or launch failure into `(None, "")`; `stop_decision` then continues fingerprinting and blocking. The heartbeat receives no error. Reproduced in memory by making the ready-query subprocess raise `TimeoutExpired`: `decision=block`, `recorded_hook_error=False`. Propagate query failures to the hook’s fail-open error handler.

2. **[P2] The metadata limit no longer limits filesystem calls.** `scripts/campaign_guard.py:786` calls `os.stat()` before checking whether the path exceeds the hashing and metadata limits. Large untracked trees therefore still incur a filesystem operation per file, risking repeated hook delays and budget exhaustion. Reproduced with `CAMPAIGN_HASH_FILES=0`, `CAMPAIGN_STAT_FILES=1`, and three paths: three stat calls occurred. The removed PowerShell hook skipped metadata access beyond the limit.

## consistency: advisory

`standards/delegation.md:34` retains guidance about running validation after `forge.py sync`, although `AGENTS.md:41` explicitly prohibits that command because it overwrites Isotone’s adaptations. This contradiction predates the candidate but remains in the paragraph this candidate updates.

## integration: needs-attention

3. **[P2] The mutation-copy recipe cannot reproduce unstaged deletions.** `.claude/agents/mutation-tester.md:26` requires copying every path returned by `git ls-files --cached --others --exclude-standard`. An unstaged deleted tracked file remains in that listing but has no source to copy. Reproduce with a candidate that deletes an unrelated tracked file while modifying the mutation target: setup fails before the baseline runs. The copy procedure must preserve deletions, including unstaged ones.

## source-defect: needs-attention

4. **[P1] The adaptation drops the SDK’s scratch-ownership safeguard.** `.claude/agents/mutation-tester.md:26` copies into a fixed `<scratch>/mt-copy`, and line 38 unconditionally deletes that directory. Neither step requires it to be absent or newly created by this invocation. Reproduce by supplying a scratch directory containing an existing `mt-copy` with unrelated files: setup merges into it and teardown deletes those files. The SDK explicitly restricts removal to the worktree the agent created; the adapted procedure needs equivalent ownership protection.

Findings 1 and 2 also exist in the SDK guard at `kits/todo/templates/scripts/campaign_guard.py:244` and `:590`. They are inherited source defects.

## record: advisory

The claimed 123-case and 781-case self-test results were not independently rerun because those suites create files. Verification here used candidate-source inspection and in-memory probes. No files were modified.

OVERALL: needs-attention

## Response to round 1

Round 1 reviewed `8c2b243`, `ce1debc`, and `af1944e` (prompt: the run guard, query plan, and mutation-tester group). Every finding was checked against the code and holds; all four are fixed in the next commit, each with a regression case where code changed.

1. Fixed. `ready_rows` raises `GuardError` when `query ready` cannot run, exits non-zero, or prints neither shape, so the hook fails open and records the error for the heartbeat, and `end --reason plan-done` refuses. A phase-scoped run on the text summary still reads an unknown count, as designed. Cases `a-failed-ready-query-fails-open-and-is-recorded`, `plan-done-refuses-an-unreadable-ready-query`, and `an-unreadable-ready-summary-fails-open-and-is-recorded` fail with the old `return None, ""`.
2. Fixed. `fingerprint` counts a path past both bounds by its name before any `os.stat`. Case `past-the-stat-bound-a-path-costs-no-stat` fails with the old order.
3. Fixed. `mutation-tester` skips a listed path that no longer exists in the live tree, so an uncommitted deletion is reproduced in the copy.
4. Fixed. `mutation-tester` creates a fresh `<scratch>/mt-<run>` with `os.mkdir`, stops if it exists, and deletes only that folder.

Consistency advisory: fixed. `standards/delegation.md` now says kit subagents are refreshed by porting SDK changes by hand, never by `forge.py sync`.

Record advisory: noted; the self-test figures are re-quoted from this session's runs in the fix commit (campaign_guard 127 cases, 0 failed).

Findings 1 and 2 also stand in the Conclave SDK's `kits/todo/templates/scripts/campaign_guard.py`; that repository is reported to the operator, not changed from here.

## Round 2: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T00:44:41Z
- Effort: high
- Lines: 19
- Digest: 38e12471d4452850

## adversarial: needs-attention

1. **Delegate guard bypass through abbreviated arguments.** [scripts/panel_slots.py:214](R:/GitHub/Isotone/scripts/panel_slots.py:214) blocks only `--writer`, but the dispatcher's argparse accepts `--w` and `--wri`. Reproduce with `python scripts/review-dispatch.py --w claude --prompt p --record docs/reviews/probe.md`: `shell_decision()` permits it, and the dispatcher accepts it. Confirmed with in-memory probes. A delegate can launch reviews and write review records despite the guard.

2. **Cancellation destroys the evidence `--keep` should preserve.** [scripts/review-dispatch.py:295](R:/GitHub/Isotone/scripts/review-dispatch.py:295) copies evidence only after `run()` returns normally, while the `finally` block always removes scratch. Interrupt an active review: partial stdout and stderr are deleted without reaching the keep directory. An in-memory `KeyboardInterrupt` reproduction produced zero `keep_file()` calls and one scratch-removal call. The previous direct redirections preserved those bytes.

## consistency: needs-attention

3. **Raw evidence writes are not atomic.** [scripts/review-dispatch.py:266](R:/GitHub/Isotone/scripts/review-dispatch.py:266) copies directly onto the destination; line 268 also writes directly. This violates the required atomic writes for data files. Reproduce by interrupting or fault-injecting a copy after its destination is opened: the retained evidence is incomplete, any previous destination has been truncated, and the enclosing cleanup deletes the source. Publish each evidence file through a temporary sibling and atomic replacement.

## integration: needs-attention

4. **A failed retry leaves a previous approval at the current review path.** [scripts/review-dispatch.py:308](R:/GitHub/Isotone/scripts/review-dispatch.py:308) skips writing `review.md` on failure but neither invalidates an existing file nor refuses a reused keep directory. Run a successful review, then rerun with the same `--keep` directory and a failing reviewer. Confirmed in memory: the second result reports `reviewer: null`, while `review.md` still contains `OVERALL: approve`. The skill's subsequent file-based checker can consume that stale approval, now beside the failed attempt's stderr. Refuse existing attempt artifacts or otherwise prevent their reuse.

## source-defect: approve

## record: approve

OVERALL: needs-attention

## Response to round 2

Round 2 reviewed `1b11445` and `21a2ed5` (the reviewer kit group). Every finding was checked against the code and holds; all four are fixed in the next commit, each with a regression case that fails when the old code is restored.

1. Fixed at both layers. `scripts/review-dispatch.py` parses with `allow_abbrev=False`, so `--w` is refused; and the delegate shell gate now refuses any dispatcher run except its read-only `--check-pin` and `--list-rounds` reports, whatever the option spelling. Cases: `test_an_abbreviated_option_is_refused`, and the shell-gate denials of `--w claude` and `--prompt p`.
2. Fixed. The kept stdout and stderr are copied in the `finally` that removes the scratch, so an interrupt keeps them. Case: `test_an_interrupted_attempt_still_keeps_what_the_reviewer_wrote`.
3. Fixed. `keep_file` publishes through a temporary sibling and `os.replace`, so a kept file is whole or absent. Case: `test_a_failed_copy_leaves_no_partial_kept_file`.
4. Fixed. `--keep` refuses a folder that already holds `review.md` or kept stdout or stderr, before any reviewer runs. Case: `test_a_reused_keep_folder_is_refused_before_any_reviewer_runs`.

## Round 3: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T00:56:49Z
- Effort: high
- Lines: 33
- Digest: 2038131d554282d6

Locations refer to `e792b1e`. Behavioral reproductions used in-memory fixtures and mocked external calls; no files were modified.

## adversarial: needs-attention

1. **[P2] The vulnerability job receives unnecessary write permissions.** [.github/workflows/pins.yml:33](R:/GitHub/Isotone/.github/workflows/pins.yml:33) grants both matrix entries `contents`, `pull-requests`, `issues`, and `actions` write access. The vulnerability job only needs repository read and issue write access, yet its restore process inherits the broader token. Reproduce by expanding the `vulnerable-packages` matrix entry: all four write permissions remain. This violates [GitHub’s least-privilege guidance](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).

2. **[P2] Version replacement corrupts longer version strings.** [scripts/check-dotnet-pin.py:103](R:/GitHub/Isotone/scripts/check-dotnet-pin.py:103) checks only the trailing boundary, and that boundary excludes `+`. Reproduced an RC2-to-RC3 rewrite changing both `111.0.100-rc.2.26504.105` and `11.0.100-rc.2.26504.105+build42`. Neither is the exact pinned version. The existing test covers only a longer numeric suffix.

3. **[P2] Malformed reconciliation blobs silently disable drift detection.** [scripts/check-conclave-kits.py:40](R:/GitHub/Isotone/scripts/check-conclave-kits.py:40) makes the blob optional; line 93 then skips allowed files even when their blob is `None`. Reproduced with `scripts/example.py | sdk not-a-blob | deliberate customization`: parsing succeeds and a changed SDK blob produces no finding. Missing or invalid blobs on file entries must not become permanent exemptions.

4. **[P2] Unrelated SDK commits resend unchanged findings.** [scripts/check-conclave-kits.py:158](R:/GitHub/Isotone/scripts/check-conclave-kits.py:158) hashes the entire SDK HEAD into the notice key. Reproduced two identical drift results with different HEADs: two emails and two notice refs. Any unrelated SDK commit defeats the promised once-per-finding behavior.

## consistency: needs-attention

5. **[P2] Generated pin updates leave contradictory documentation.** [scripts/check-dotnet-pin.py:93](R:/GitHub/Isotone/scripts/check-dotnet-pin.py:93) performs literal version substitutions without handling the README badge’s escaped `--rc.2`. Reproduced an RC3 update that leaves the badge displaying RC2. A GA update also leaves `docs/dev/build.md` claiming `allowPrerelease: true` and describing the SDK as a release candidate, despite removing that setting from `global.json`. `AGENTS.md`, explicitly required by §8’s documentation item, is absent from `DOCS`.

6. **[P2] Configuration writes are not atomic.** [scripts/check-dotnet-pin.py:91](R:/GitHub/Isotone/scripts/check-dotnet-pin.py:91) overwrites `global.json` directly; line 105 similarly overwrites the remaining files. An interruption or write failure after truncation leaves incomplete data. Reproduce by injecting a failure after opening the destination for writing. There is no temporary-file replacement or recovery path, contrary to the repository’s atomic-write requirement.

## integration: needs-attention

7. **[P1] Vulnerabilities can prevent their own issues from being filed.** [scripts/check-vulnerable-packages.py:59](R:/GitHub/Isotone/scripts/check-vulnerable-packages.py:59) restores before collecting the vulnerability report and returns immediately on restore failure. Gesso inherits `TreatWarningsAsErrors=true`, without exemptions for NU1901 through NU1904. NuGet therefore fails restore when an affected dependency is discovered, as [Microsoft documents](https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages). Injecting that restore result reproduced exit 2 with no report command and no GitHub calls. A newly vulnerable Gesso dependency triggers this path.

8. **[P2] Failed CI dispatches are never recovered.** [scripts/lib/pin_proposal.py:98](R:/GitHub/Isotone/scripts/lib/pin_proposal.py:98) returns immediately for any existing PR, although dispatch happens after PR creation at line 121. Reproduced successful creation followed by an HTTP 503 on dispatch: the next run returns success without dispatching either workflow. That PR remains without its promised checks until manually repaired.

9. **[P2] Automatically resolved vulnerabilities remain suppressed if they recur.** [scripts/lib/pin_proposal.py:138](R:/GitHub/Isotone/scripts/lib/pin_proposal.py:138) treats every matching historical issue as dismissal, including issues automatically closed by `resolve_issues`. Reproduce: report vulnerable set A, report clean, then report A again. The final run neither creates nor reopens an issue. Automatic resolution is being confused with an operator’s decision to dismiss the finding.

## source-defect: approve

## record: needs-attention

10. **[P2] The claimed “newer release” condition is only an inequality check.** [scripts/check-dotnet-pin.py:131](R:/GitHub/Isotone/scripts/check-dotnet-pin.py:131) distinguishes equal from different, without checking version ordering. Reproduced a listed pin of `11.0.101` with feed `latest-sdk=11.0.100`: PR mode proposes `pins/dotnet-11.0.100`. A stale or inconsistent feed can therefore propose a downgrade, contrary to the commit’s description.

OVERALL: needs-attention

## Response to round 3

Round 3 reviewed `e792b1e` (the automations commit). Every finding was checked against the code and holds; all ten are fixed in the next commit, each with a case in `scripts/tests/test_pin_automations.py` (`ReviewRound3Tests`, `KitRound3Tests`) that fails when its fix is reverted (a mutation run, twelve mutations, twelve caught).

1. Fixed. `pins.yml` is two jobs: `dotnet` keeps `contents`, `pull-requests`, `issues` and `actions` write; `vulnerable-packages` holds only `contents: read` and `issues: write`, with `persist-credentials: false`.
2. Fixed. A version is replaced only where it stands whole: not after a digit or a dot, not before a digit, a dot and a digit, or a `+`.
3. Fixed. A file entry in `.conclave/kit-drift-allow.txt` needs a well-formed `sdk <12 hex>`; a malformed or missing blob is refused (`absorb` alone accepts a missing one, to fill it in).
4. Fixed. The kit notice key is the findings alone, so an unrelated SDK commit sends nothing new.
5. Fixed. The rewrite moves the README badge's escaped `--rc.N` form and covers `AGENTS.md`; a GA pull request lists every docs line that still describes a prerelease pin for `D00 T02 §8`'s documentation item, which owns that prose.
6. Fixed. Every rewritten file goes through a temporary sibling and a rename.
7. Fixed. The restore before the report runs with `-p:NuGetAudit=false`, so a vulnerable package cannot fail the restore under `TreatWarningsAsErrors` before the report names it.
8. Fixed. An open pin pull request whose CI never started gets each missing workflow dispatched on the next run.
9. Fixed. `resolve_issues` labels what it closes `pins:resolved`, and `file_issue` reopens such an issue when its finding returns; a close without the label is still the owner's dismissal.
10. Fixed. SDK versions are ordered (preview, then release candidate, then GA); a feed whose latest SDK is older than the pin exits 2 and proposes nothing.

While these were fixed, `isotone-conclave-kits` reported the SDK's new base-kit skill `adopt-conclave` (SDK 56c3046). It is not imported: it installs and updates kits through `forge.py`, which AGENTS.md forbids here; the allow-list records it with its SDK blob, so a later change to it is still reported.

## Round 4: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T01:15:12Z
- Effort: high
- Lines: 23
- Digest: 7e7be9bff724b4d6

## adversarial: needs-attention

1. **[P2] The shell gate mistakes filenames for read-only options.** `scripts/panel_slots.py:215` exempts any command containing `--check-pin` or `--list-rounds` later in its text. With a valid prompt `p`, `python scripts/review-dispatch.py --writer claude --prompt p --record docs/reviews/--check-pin.md` passes the gate and starts a review. In-memory reproduction returned `shell_decision=None` and reached `review()`. Parse options within the dispatcher invocation; a substring in an argument must not grant the exemption.

## consistency: needs-attention

2. **[P2] Version replacement still modifies longer versions, including cases previously preserved.** `scripts/check-dotnet-pin.py:38` permits alphabetic, hyphenated, and nonnumeric dotted suffixes. Reproduce an RC2-to-GA rewrite with `<PackageVersion Include="Custom" Version="11.0.0-rc.2.26504.105-private" />`: the candidate changes it to `11.0.0-private`, although that package does not match `tracking_packages()` and therefore receives no availability check. An in-memory execution of `rewrite_tree()` confirmed this change; `e792b1e` leaves it untouched. The new regression case covers numeric prefixes and `+build`, but misses these suffixes.

## integration: needs-attention

3. **[P2] Notification deduplication now suppresses subsequent changes to ordinary kit files.** `scripts/check-conclave-kits.py:166` hashes finding text alone, but the missing/different findings at lines 102 and 106 contain no blob identity. Reproduce two different SDK revisions of an unallow-listed `scripts/example.py`: both produce the same finding and notice key, so the second change is suppressed. This also persists after importing the first change and later encountering another. The added test proves unrelated commits stay quiet but does not prove related changes notify.

4. **[P2] Automatically superseded vulnerabilities still become permanent dismissals.** `scripts/lib/pin_proposal.py:160` reopens only issues carrying `pins:resolved`, while automatic supersession at line 169 closes issues without that label. Reproduce vulnerability sets `A`, `A+B`, clean, then `A` again. The first issue was automatically closed without the label; the last run neither creates nor reopens an issue. A stateful in-memory reproduction ended with both issues closed and no notification for the recurring vulnerability. Automatic supersession needs to remain distinguishable from operator dismissal.

5. **[P2] The keep-folder restriction breaks the documented architecture-review retry.** `scripts/review-dispatch.py:566` refuses existing artifacts, but `.claude/skills/review-todo-section/SKILL.md:154` uses the fixed `$RUNDIR/arch` directory and line 157 requires another review after fixing findings. Following that retry reuses the populated directory, returns exit 2, and launches no reviewer. Update the caller to allocate a directory per attempt and read the corresponding result.

## source-defect: approve

## record: advisory

The claimed full-suite and mutation totals were not independently rerun because those suites create files. Verification used source inspection and in-memory probes, including comparisons against `e792b1e`. No files were modified.

OVERALL: needs-attention

## Response to round 4

Round 4 reviewed the fix range `e792b1e..46dcff2`. Every finding was checked against the code and holds; all five are fixed in the next commit, each with a regression case that fails when its fix is reverted (a mutation run, five of five caught).

1. Fixed. The shell gate no longer reads a substring: `dispatch_round` finds the token that is the dispatcher itself and exempts it only when its own arguments hold `--check-pin` or `--list-rounds` as whole tokens and no `-c` comes before it, so `--record docs/reviews/--check-pin.md` and a `python -c` run are refused.
2. Fixed. A version followed by a letter, a digit, a hyphen, a `+`, or a dot and a letter or digit is part of a longer one and is left alone (`...-private`); only the badge's escaped form may be followed by a `-`, its field separator.
3. Fixed. Every kit finding names the SDK blob, so a further SDK change to a reported file is a new finding and a new notice.
4. Fixed. `file_issue` labels the issues it supersedes `pins:resolved`, like `resolve_issues`, so a superseded finding that returns reopens its issue; only the owner's own close dismisses.
5. Fixed. The architecture gate and the plan review keep one `--keep` folder per attempt (`$RUNDIR/arch-<N>`, `$RUNDIR/plan-<N>`), like the panel and stamp rounds, and the `review_prompt.py` skill pins name them.

Record advisory: noted.

## Round 5: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T01:27:13Z
- Effort: high
- Lines: 19
- Digest: 1fb59beb3def3667

## adversarial: needs-attention

1. **[P2] Non-argument tokens still grant the dispatcher exemption.** [scripts/panel_slots.py:892](R:/GitHub/Isotone/scripts/panel_slots.py:892) treats comments and redirection targets as dispatcher arguments. Reproduce with `python scripts/review-dispatch.py --writer claude --prompt p # --check-pin`, or replace the comment with `> --check-pin`. Both return `shell_decision=None`, although the shell removes that token from the dispatcher’s arguments. An in-memory probe confirmed the resulting arguments reach `review()`. Round 4 finding 1 remains incompletely fixed.

## consistency: needs-attention

2. **[P2] GA updates now leave the README badge stale.** [scripts/check-dotnet-pin.py:126](R:/GitHub/Isotone/scripts/check-dotnet-pin.py:126) generates badge replacements only when the old version contains a hyphen, while the tightened ordinary boundary rejects the badge’s hyphen separator. Reproduce `rewrite_tree()` updating SDK `11.0.100` to `11.0.101` with badge `.NET-11.0.100-512BD4`: `global.json` changes, but the badge remains `11.0.100`. The parent updates it correctly. The regression covers prerelease badges only.

## integration: needs-attention

3. **[P2] Reopening a superseded finding leaves the newer, obsolete issue open.** [scripts/lib/pin_proposal.py:166](R:/GitHub/Isotone/scripts/lib/pin_proposal.py:166) returns before superseding other issues whenever the requested title already exists. Reproduce vulnerability sets `A`, `A+B`, then `A`, without an intervening clean run: the candidate reopens A but leaves A+B open, still reporting the removed vulnerability B. A stateful in-memory reproduction confirmed both remain open. The new regression at [scripts/tests/test_pin_automations.py:450](R:/GitHub/Isotone/scripts/tests/test_pin_automations.py:450) uses separate canned responses and omits the still-open A+B issue, missing this lifecycle defect.

## source-defect: approve

## record: advisory

The full-suite and five-mutation totals were not independently rerun because those runs create files. Verification used candidate and parent source plus in-memory probes. No files were modified.

OVERALL: needs-attention

## Response to round 5

Round 5 reviewed `c5a662e`. Every finding was checked and holds; all three are fixed in the next commit, each with a regression case that fails when its fix is reverted (three mutations, three caught).

1. Rethought, not patched. The shell gate needed a fix in rounds 2, 4 and 5 for the same unit (telling a read-only dispatcher report from a review round by reading a shell line), so per the independent-review rule the approach changed: the gate now refuses any command that names the review dispatcher, whatever its options, comments or redirections. A delegate needs neither report (it can read `.conclave/reviewers.toml`); the delegate definitions and `standards/delegation.md` say so.
2. Fixed. Badge URLs are rewritten on their own: inside a shields.io URL every short version moves where a single `-`, a query or the URL's end follows it, so a GA-to-GA move updates the badge, and a longer version in a badge is left alone.
3. Fixed. `file_issue` closes every other open issue of the check as superseded before it reopens or keeps the matching one, so a returning finding never leaves a newer, obsolete issue open.

Record advisory: noted.