# Codex campaign

Run `scripts/start-campaign.ps1 -Runner codex`, or open "Isotone Codex campaign" on the Windows Desktop. This starts Codex as writer using its configured model at medium reasoning effort and its existing account. Claude credentials are never required or passed to it.

Codex follows `.codex/skills/process-plan/SKILL.md`, using the existing plan, campaign guard and review dispatcher. Its Stop hook is `.codex/hooks.json`; approve this project's hook in Codex after changing it. Its reviewer route is `codex -> carbon`, preserving the project's review schedule. Only one writer may own the tree. A stopped or crashed campaign is not restarted by a background service.

The owner authorised Codex as an additional campaign writer on 2026-11-14. Existing Claude and Carbon launchers remain available. The Codex-specific session and timer rules in its process-plan skill take precedence over the Claude-specific examples in the shared workflow documents.

## Independent reviewer pin (2026-11-14)

Codex routes to the existing `carbon` reviewer: Orchestrator (Carbon), model `gemini-pro-orchestrator`, through the Antigravity CLI (`agy`). Run reviews through `scripts/review-prompt.py` and `scripts/review-dispatch.py --writer codex`; do not invoke the CLI directly. The `agy` and `claude` writer routes still use `astra` (`gpt-6-astra` through `codex`), with no fallback.

The shared three-pass schedule keeps every lens, one round definition, the 33-pass cap and P1/P2 blocking policy. Effort is scoped by reviewer CLI: `effort_by_cli = { codex = "medium" }` applies to plan, first implementation round and completion; `followup_effort_by_cli = { codex = "low" }` applies to subsequent returned implementation rounds, and reconciliation uses low. Failed attempts do not advance the round effort. Orchestrator receives no effort override. The dispatcher and receipt verifier use the same selection rule, including the pin frozen at the section's plan candidate. Older pins retain their original scalar-effort semantics.

Antigravity reviews run in plan mode with the sandbox, `--disable-slash-commands` (review text must not expand into CLI skills), and a temporary session-only `--settings` file. It permits reading the generated prompt and narrowly specified Git show/diff commands with full commit hashes, `--no-pager`, `--no-ext-diff` and `--no-textconv`. The generated prompt explains these commands. File writes, MCP calls, browser execution and downloads are denied. No global permission settings are changed and blanket tool approval is never enabled. This fixes the headless command-permission denial that caused the first empty reply. Permission matching follows [Google's CLI permission documentation](https://antigravity.google/docs/permissions).

A bounded live check uses `--timeout 300` and records the dispatcher verdict. A timeout, empty reply, missing lens or malformed verdict is no review, never approval.
