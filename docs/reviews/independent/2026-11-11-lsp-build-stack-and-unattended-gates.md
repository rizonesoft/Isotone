## Round 1: astra (`gpt-6-astra` via `codex`)

- Writer: agy
- Run: 2026-11-11T07:15:37Z
- Effort: medium
- Lines: 20
- Digest: d2e913820568ea21

### adversarial: needs-attention

1. P1 `scripts/lsp-mcp-server.py:498`: Diagnostics timeout returns cached diagnostics or `[]`, which the caller reports as successful `0 diagnostics`. A cold or busy clangd exceeding `timeout_seconds` therefore appears clean without completing analysis. Reproduced with an alive backend that publishes nothing: `diagnostics(..., timeout=0.01)` returns `[]`. Return an explicit timeout error instead.

### consistency: needs-attention

2. P1 `scripts/panel_slots.py:4968`: The trunk guard allows implicit branch creation. `_agy_command_decision('git switch dependabot/github_actions/actions-39799580c0')` returns `None`; that remote branch exists in this checkout, and Git’s default guessing creates and switches to its local tracking branch. The writer can therefore leave `main` through an ordinary dependency-inspection command. The analogous `git checkout` path is also allowed.

### integration: needs-attention

3. P1 `scripts/lsp-mcp-server.py:285`: Published diagnostics discard `params.version` and use arrival order to establish freshness. If version 1 analysis finishes after version 2 is submitted, its clean result satisfies the version 2 request, potentially hiding newly introduced errors. Reproduced in memory by delivering version 1 diagnostics while the open document is version 2: `diagnostics()` accepts the stale empty result. Match diagnostics to the requested document version.

### source-defect: approve

### record: advisory

4. P3 `scripts/tests/test_lsp_mcp_server.py:86`: `test_live_clangd_symbols_and_diagnostics` never requests diagnostics. It only requests document symbols and stops the backend, so passing this test supplies no live clangd diagnostics evidence. Inspect its calls at lines 98 and 108; add an actual diagnostics assertion that requires a known error to be reported.

HIGHEST: P1
OVERALL: needs-attention


## Response to round 1

1. **P1 `scripts/lsp-mcp-server.py:498` (`adversarial`):** Real and reproduced. Updated `LspBackend.diagnostics` in `scripts/lsp-mcp-server.py` to enforce a single wall-clock deadline across pull (`textDocument/diagnostic`) and push (`textDocument/publishDiagnostics`) paths and raise `LspToolError("<backend> timed out after ... waiting for diagnostics on ...")` (`isError=True`) instead of returning cached or empty diagnostics on timeout. Covered in `_self_test` (`silent.py` with `timeout_seconds=0.1`).
2. **P1 `scripts/panel_slots.py:4968` (`consistency`):** Real and reproduced. Tightened `_segment_creates_branch_or_worktree` in `scripts/panel_slots.py` to an allow-list for `git switch`, `git checkout`, `git worktree`, `git symbolic-ref`, and `git update-ref`: `git switch` allows only `main` or `refs/heads/main` without creation/tracking/detach flags (blocking implicit DWIM remote-tracking branches such as `git switch dependabot/...`, `git switch -`, and `--detach`), `git checkout` allows only path restores (`git checkout [<tree-ish>] -- <paths...>` or `--pathspec-from-file`) or `main` / `refs/heads/main` / `.` without creation/tracking/detach/guess flags, `git worktree` allows only `list`/`prune`/`remove`/`unlock`/`repair`, and `git symbolic-ref` / `git update-ref` deny repointing `HEAD` or writing non-`main` local branch refs. Covered in `_self_test`.
3. **P1 `scripts/lsp-mcp-server.py:285` (`integration`):** Real and reproduced. Updated `_handle_incoming`, `_sync_document_locked`, and `diagnostics` in `scripts/lsp-mcp-server.py` to synchronize `_open_docs` and `_diagnostics` under `self._cond`, drop incoming `textDocument/publishDiagnostics` notifications whose `params.version` is older than the open document's current `version`, and require `pub_ver >= expected_version` (whenever `version` is provided) alongside `seq >= expected_seq` before satisfying `diagnostics()`. Covered in `_self_test` (`STALE_PREV_VERSION` publishing clean `version - 1` diagnostics before `version` error diagnostics).
4. **P3 `scripts/tests/test_lsp_mcp_server.py:86` (`record`):** Real. Extended `test_live_clangd_symbols_and_diagnostics` in `scripts/tests/test_lsp_mcp_server.py` to run live `lsp_diagnostics` through `clangd` on a probe C++ file containing a type error (`int value = "not_an_int";`) and assert that `clangd` reports an `Error` diagnostic before cleaning up the probe directory and stopping the backend.
