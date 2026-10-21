# Review-run records

schema: 1

Panel wiring: every round runs through `python scripts/review-dispatch.py --writer claude` on the one route `.conclave/reviewers.toml` pins, GPT-6 Astra through codex at medium effort (2026-10-21; earlier rounds ran the Full and Light slots, `bulk` medium for Full rounds 1-2 and `signoff` and `depth` high after, as their lines record), and the writer's family never reviews. A loop runs at most 22 rounds and, from round 9, stops on a round whose findings are all P3 (`review-todo-section`, The loop). Round headings in the per-section review files read `GPT panel`, and a round's `model:` must be a registered model of its heading's family. There is no fallback: a failed round waits for the operator.

Terminology, pinned. A run is one section's independent review, however many rounds it took; an engagement is the same thing counted for the report. A round is one reviewer invocation against one candidate. Voided rounds keep their numbers. Two outcomes skip the panel mapping without voiding their findings: stamp, a stamp-review pass over the staged stamp, and independent, a non-panel independent pass inside a panel block; their refs count in yield and coverage, but they meet no panel section. Empty is outcome-based: an engagement is empty when every round came back empty.

One block per stamped section whose review reached an independent round, appended by `review-todo-section` after the stamp. Checked by `scripts/todo-runs.py --check`, which cross-reads the per-section review files: every listed ref must resolve to an independent-marked finding heading, every `(independent)` mark must be listed by exactly one run, every review file must have a run block, `empty` must equal the rounds with outcome `empty`, and `refuted` must equal the listed refs whose disposition is refuted. Panel runs additionally re-read their round verdicts from the review file's panel sections, and every candidate must be a commit that exists.

Each round line carries the model, provider, exact version (`unresolved` when the invocation never pinned one), cost in total tokens (`unresolved` when unrecorded), latency in wall-clock seconds from the reviewer invocation to its returned output (`unresolved` when untimed), opportunity scope, review purpose, provenance, and the refs that round raised. Findings described only in review prose, without a ref, are noted in `#` comments and counted nowhere.

Panel probe, 2026-10-21 (D00 T01 §4): one dispatcher round per review kind against a planted typo (`Documentaion` in `docs/README.md` line 3, probe commit `237664cb95f227576707988213ac3b83bd3099a5`, built in a scratch clone and fetched by sha, on no branch), kept under `build/panel-probe/<kind>/`; each fenced kind (panel, architecture, plan review, stamp review) keeps its own `manifest.md` beside its `review.md`, so its review replays against its checker or receipt, while the independent pass is unfenced (it reads the commit with `git show` from `docs/review-round-prompt.md`) and carries no manifest (the first runs shared one manifest across kinds and were re-run after the independent review named it; they are kept under `build/panel-probe/superseded-1/`). Every round's summary names reviewer astra, model gpt-6-astra, CLI codex, effort medium, no failover; codex-cli 0.162.1, writer harness Claude Code 2.1.306. Panel: exit 0, `PASS four lenses, one verdict each; highest P3`, the typo named (18s, 17694 tokens). Architecture: exit 0, `**architecture: needs-attention**` naming the typo, its receipt matching its manifest (16s, 17292 tokens). Plan review: exit 0, `PASS 2 findings, one per line`, the typo named (15s, 17307 tokens). Stamp review: exit 0, `PASS 1 naming(s) to answer`, the misquoted line named (27s, 12294 tokens). Independent pass: exit 0, `source-defect` needs-attention naming the typo (22s, 29286 tokens). No kind failed. Stamp path check: a probe stamp citing the missing `docs/reviews/00-workspace/D00-T01-s4-gates.log` was named on the first attempt in three runs in a row (`PASS 1 naming(s) to answer`, then `PASS 2 naming(s) to answer` twice; 27s, 23s, 33s; 18956, 18680, 21393 tokens), each replaying against its own manifest.

run: D00-T01-S1
date: 2026-10-19
runner: panel
rounds: 3
round: 1 model: gpt-6-astra effort: medium outcome: empty candidate: ad0742d provider: openai version: gpt-6-astra cost: 18807tokens latency: 15s opportunity: full-scope purpose: section-review provenance: recorded findings:
round: 2 model: gpt-6-astra effort: high outcome: empty candidate: ad0742d provider: openai version: gpt-6-astra cost: 18822tokens latency: 18s opportunity: full-scope purpose: section-review provenance: recorded findings:
round: 3 model: gpt-6-astra effort: high outcome: independent candidate: ad0742d provider: openai version: gpt-6-astra cost: unresolved latency: 40s opportunity: full-scope purpose: section-review provenance: recorded findings:
empty: 2
refuted: 0

run: D00-T01-S2
date: 2026-10-19
runner: panel
rounds: 4
round: 1 model: gpt-6-astra effort: medium outcome: findings candidate: 7ef0113 provider: openai version: gpt-6-astra cost: 32061tokens latency: 21s opportunity: full-scope purpose: section-review provenance: recorded findings: D00-T01-S2-F1
round: 2 model: gpt-6-astra effort: medium outcome: empty candidate: ce9a258 provider: openai version: gpt-6-astra cost: 31422tokens latency: 17s opportunity: delta-plus-regressions purpose: fix-loop provenance: recorded findings:
round: 3 model: gpt-6-astra effort: high outcome: empty candidate: ce9a258 provider: openai version: gpt-6-astra cost: 27882tokens latency: 16s opportunity: delta-plus-regressions purpose: fix-loop provenance: recorded findings:
round: 4 model: gpt-6-astra effort: high outcome: independent candidate: 7ef0113 provider: openai version: gpt-6-astra cost: unresolved latency: 94s opportunity: full-scope purpose: section-review provenance: recorded findings:
empty: 2
refuted: 0

run: D00-T01-S11
date: 2026-10-19
runner: panel
rounds: 4
round: 1 model: gpt-6-astra effort: medium outcome: empty candidate: f6fb40a provider: openai version: gpt-6-astra cost: 25245tokens latency: 20s opportunity: full-scope purpose: section-review provenance: recorded findings:
round: 2 model: gpt-6-astra effort: medium outcome: empty candidate: f6fb40a provider: openai version: gpt-6-astra cost: 21643tokens latency: 16s opportunity: full-scope purpose: section-review provenance: recorded findings:
round: 3 model: gpt-6-astra effort: high outcome: empty candidate: f6fb40a provider: openai version: gpt-6-astra cost: 21829tokens latency: 19s opportunity: full-scope purpose: section-review provenance: recorded findings:
round: 4 model: gpt-6-astra effort: high outcome: independent candidate: f6fb40a provider: openai version: gpt-6-astra cost: unresolved latency: 56s opportunity: full-scope purpose: section-review provenance: recorded findings:
empty: 3
refuted: 0

run: D00-T01-S3
date: 2026-10-21
runner: panel
rounds: 2
round: 1 model: gpt-6-astra effort: medium outcome: empty candidate: 353cfbf provider: openai version: gpt-6-astra cost: 14013tokens latency: 17s opportunity: full-scope purpose: section-review provenance: recorded findings:
round: 2 model: gpt-6-astra effort: medium outcome: independent candidate: 353cfbf provider: openai version: gpt-6-astra cost: 43370tokens latency: 62s opportunity: full-scope purpose: section-review provenance: recorded findings:
empty: 1
refuted: 0
