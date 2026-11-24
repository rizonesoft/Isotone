# Codex reviewer only

The Codex campaign launcher was retired by the operator on 2026-11-14. Only Claude Code and Antigravity write in Isotone, one session at a time. Codex runs exclusively as their independent headless reviewer through the repository dispatcher. The Antigravity reviewer route is removed.

Start a campaign with `pwsh -File scripts/start-campaign.ps1 -Runner agy` (Orchestrator Carbon, `gemini-pro-orchestrator`) or `-Runner claude` (latest Opus, medium effort). Run `pwsh -File scripts/start-campaign.ps1 -InstallShortcut` to refresh the Desktop's Isotone Carbon and Isotone Claude campaign shortcuts and remove the retired Codex shortcut. `-Runner codex` is rejected. No campaign starts during shortcut installation.

Both writer routes in `.conclave/reviewers.toml` select only `astra`, model `gpt-6.2-astra`, through `codex`, without fallback. Build review prompts through `scripts/review-prompt.py` and dispatch with `scripts/review-dispatch.py --writer agy` or `--writer claude`.

The shared three-pass schedule retains every lens, the 33-pass cap and P1/P2 blocking policy. Plan, first returned implementation round and completion use medium effort; subsequent returned standalone rounds and reconciliation use low. Section reviews still permit one implementation round. Failed attempts do not advance effort. The dispatcher and receipt verifier share this rule, including the section's frozen pin. Historical receipts retain their recorded pins; no old verdict is rewritten as approval.

A timeout, empty response, missing lens or malformed verdict is no review, never approval. The prior Gemini experiment returned blocking findings and is not approval of this role restoration. No further Gemini review is scheduled.
