# Codex campaign

Run `scripts/start-campaign.ps1 -Runner codex`, or open "Isotone Codex campaign" on the Windows Desktop. This starts Codex as writer using its configured model at medium reasoning effort and its existing account. Claude credentials are never required or passed to it.

Codex follows `.codex/skills/process-plan/SKILL.md`, using the existing plan, campaign guard and review dispatcher. Its Stop hook is `.codex/hooks.json`; approve this project's hook in Codex after changing it. Its reviewer route is `codex -> carbon`, preserving the project's review schedule. Only one writer may own the tree. A stopped or crashed campaign is not restarted by a background service.

The owner authorised Codex as an additional campaign writer on 2026-11-14. Existing Claude and Carbon launchers remain available. The Codex-specific session and timer rules in its process-plan skill take precedence over the Claude-specific examples in the shared workflow documents.

## Independent reviewer pin (2026-11-14)

Codex routes to the existing `carbon` reviewer: Orchestrator (Carbon), model `gemini-pro-orchestrator`, through the Antigravity CLI (`agy`). Run reviews through `scripts/review-prompt.py` and `scripts/review-dispatch.py --writer codex`; do not invoke the CLI directly. The `agy` and `claude` writer routes still use `astra` (`gpt-6-astra` through `codex`), with no fallback.

The shared three-pass schedule keeps every lens, one round, the 33-pass cap and P1/P2 blocking policy. Its plan, round, completion and reconciliation steps have no effort overrides because Orchestrator rejects them. This also removes explicit effort from scheduled Astra invocations: the dispatcher uses the step alone and does not fall back to `[reviewers.astra].effort = "medium"`. Astra scheduled reviews therefore use the Codex CLI configuration; the retained reviewer effort applies only without a schedule. Restoring explicit scheduled Astra effort would require separately scoped schedules, not restoring a global override.

A bounded live check uses `--timeout 300` and records the dispatcher verdict. A timeout, empty reply, missing lens or malformed verdict is no review, never approval.
