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

## Round 2: astra (`gpt-6-astra` via `codex`)

- Writer: agy
- Run: 2026-11-11T07:27:59Z
- Effort: low
- Lines: 18
- Digest: 3ff4905830ba6409

### adversarial: needs-attention

1. P1 `scripts/panel_slots.py:5040`: `git branch -- review-probe` bypasses branch-creation enforcement because parsing stops at `--` without collecting subsequent positionals. Reproduced read-only: `_agy_command_decision('git branch -- review-probe')` returns `None`. A writer command using Git’s standard option separator therefore creates a prohibited local branch.

### consistency: needs-attention

2. P1 `scripts/panel_slots.py:4979`: The checkout allow-list treats `refs/heads/main` as equivalent to `main`, but `git checkout refs/heads/main` detaches HEAD. Reproduced at the gate: `_agy_command_decision('git checkout refs/heads/main')` returns `None`. A writer using the fully qualified ref can consequently commit outside `main`. Git’s [checkout implementation](https://raw.githubusercontent.com/git/git/master/builtin/checkout.c) distinguishes branch names from this commit-selection form.

### integration: needs-attention

3. P2 `scripts/lsp-mcp-server.py:518`: An unversioned empty diagnostic notification can still satisfy a reopened document’s diagnostics request. Clangd sends exactly this notification when processing `didClose`, as shown in its [close handler](https://raw.githubusercontent.com/llvm/llvm-project/main/clang-tools-extra/clangd/ClangdLSPServer.cpp). During a busy campaign, evict file A through the LRU, let the next request time out before clangd processes that close, then immediately request A again. The delayed close notification passes the new sequence threshold and `pub_ver is None`, reporting zero diagnostics before reopened-file analysis finishes. An in-memory reproduction delivering that notification after document synchronization returned `[]`. The round-1 version check does not cover this real lifecycle message.

### source-defect: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention


## Response to round 2

1. **P1 `scripts/panel_slots.py:5040` (`adversarial`):** Real and reproduced. Updated `git branch` parsing in `_segment_creates_branch_or_worktree` (`scripts/panel_slots.py`) to switch to positional collection after `--` instead of breaking early, added `-f`/`--force`/`-t`/`--track`/`--create-reflog` to `forbidden_branch_ops` and `--sort` to option-value skipping, and hardened `worktree`, `symbolic-ref`, `update-ref`, and `fetch`/`pull` refspec parsing across `--` and `-m` option values. Covered in `_self_test` (`git branch -- review-probe`, `git branch -f`, `git symbolic-ref -m`, `git update-ref -m`, and `git fetch origin main:feat`).
2. **P1 `scripts/panel_slots.py:4979` (`consistency`):** Real and reproduced. Removed `refs/heads/main` from both the `git checkout` and `git switch` allow-lists in `_segment_creates_branch_or_worktree` (`scripts/panel_slots.py`) so only the branch name `main` (and `.` / explicit pathspecs on `git checkout`) is allowed, preventing detached-HEAD checkout via `git checkout refs/heads/main`. Covered in `_self_test`.
3. **P2 `scripts/lsp-mcp-server.py:518` (`integration`):** Real and reproduced. Assigned monotonically increasing backend-wide document versions (`self._next_doc_version`) across `didOpen` and `didChange` in `LspBackend` (`scripts/lsp-mcp-server.py`) and required an exact integer version match (`pub_ver == int(open_meta["version"])` and `pub_ver == expected_version`) in `_handle_incoming` and `diagnostics()`, rejecting unversioned `didClose` clear notifications (`pub_ver is None`) and any prior-open version notifications across LRU eviction and reopen cycles. Verified against both live `clangd` and live `pyright` (`test_lsp_mcp_server.py`) and in `_self_test` (`DELAYED_UNVERSIONED_CLOSE`).

## Round 3: astra (`gpt-6-astra` via `codex`)

- Writer: agy
- Run: 2026-11-11T07:38:47Z
- Effort: medium
- Lines: 16
- Digest: f135b52c67010264

### adversarial: needs-attention

1. P1 `scripts/panel_slots.py:4965`: Abbreviated long options bypass detached-HEAD enforcement. Read-only reproduction: `_agy_command_decision('git checkout --det main')` and the equivalent `git switch --det main` both return `None`. Git accepts `--det` as `--detach`, so a writer using this valid command leaves `main` and can commit detached. Unknown long options fall through to the permitted `main` positional. Normalize supported abbreviations or reject unrecognized options. [Git CLI documentation](https://git-scm.com/docs/gitcli#_abbreviating_long_options).

### consistency: approve

### integration: needs-attention

2. P1 `scripts/lsp-mcp-server.py:426`: Synchronization refreshes only the requested file, leaving previously opened dependencies stale indefinitely during continued use. Reproduce by querying module B containing `answer: int = 1`, then consumer A containing `from B import answer; x: int = answer`; change B to `answer: str = "changed"` and request A’s diagnostics again. A still reports zero diagnostics because B’s open buffer retains its previous contents, and A’s cached result remains eligible. Reproduced with live Pyright and in-memory disk-content overlays without modifying files: A returned `[]` after B changed, then reported `reportAssignmentType` only after explicitly synchronizing B. Refresh changed open dependencies and invalidate affected diagnostics before returning results.

### source-defect: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention


## Response to round 3

1. **P1 `scripts/panel_slots.py:4965` (`adversarial`):** Real and reproduced. Hardened `_segment_creates_branch_or_worktree` and `_AGY_RESOLVED_TARGETS` in `scripts/panel_slots.py` to enforce strict canonical option allow-lists for global Git flags and for `worktree`, `checkout`, `switch`, `symbolic-ref`, `update-ref`, `branch`, `stash`, `bisect`, `fetch`, `pull`, and `push` (including `git-<subcmd>` executables and `alias.*` overrides via `-c` / `--config-env`), rejecting unrecognized or abbreviated long options such as `git checkout --det main` and `git switch --det main`. Covered in `_self_test` (1,009 cases passing).
2. **P1 `scripts/lsp-mcp-server.py:426` (`integration`):** Real and reproduced. Added `_refresh_tracked_documents_locked` and per-document `deps_dirty` tracking in `LspBackend` (`scripts/lsp-mcp-server.py`) so every `_sync_document_locked` and `workspace_symbols` call first checks all open and previously evicted documents against disk, emits `textDocument/didChange`, `textDocument/didClose`, and `workspace/didChangeWatchedFiles` for modified or removed dependencies, invalidates stale cached diagnostics across open consumers, and bumps the consumer's version via `textDocument/didChange` so Pyright and clangd re-analyze against fresh dependency buffers. Covered in `_self_test` and in `test_live_pyright_refreshes_changed_open_dependency` (`scripts/tests/test_lsp_mcp_server.py`).

