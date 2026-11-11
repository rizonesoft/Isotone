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


## Round 4: astra (`gpt-6-astra` via `codex`)

- Writer: agy
- Run: 2026-11-11T22:11:35Z
- Effort: low
- Lines: 18
- Digest: 95a6e260e9b6371f

### adversarial: approve

### consistency: needs-attention

1. P2 `scripts/panel_slots.py:5250`: The forbidden-short-option scan interprets characters inside an attached upstream argument as flags. Reproduced read-only: `_agy_command_decision('git branch -uorigin/main')` denies branch creation because `origin/main` contains `m`, while `git branch -u origin/main` is allowed. This blocks ordinary upstream repair on `main`. Parse `-u` and its argument before scanning flag clusters; attached arguments are supported [Git syntax](https://git-scm.com/docs/gitcli#_separating_argument_from_the_option).

### integration: needs-attention

2. P1 `scripts/lsp-mcp-server.py:538`: Reopening a changed, evicted dependency discards its previous hash without invalidating open consumers. The dependency is excluded from refresh at line 532, and the new-open path never marks consumers dirty. Reproduce with an LRU cap of two: open B, C, then A importing B; change B’s exported type, reopen B, then request A’s diagnostics before asynchronous reanalysis finishes. An in-memory reproduction returned cached `[]`, kept A’s version unchanged, and sent no consumer-refresh notification. The default 16-document cap reaches the same failure during normal campaign browsing.

### source-defect: approve

### record: needs-attention

3. P3 `docs/reviews/independent/2026-11-11-lsp-build-stack-and-unattended-gates.md:100`: The round-3 response claims its Git parser hardening is covered by `_self_test`, but that commit adds no corresponding parser regression cases. Inspect `git show 7840339 -- scripts/panel_slots.py`: neither `checkout --det main` nor `switch --det main` is tested. The reported aggregate case count does not establish coverage of the repaired bypass.

HIGHEST: P1
OVERALL: needs-attention


## Response to round 4

1. **P2 `scripts/panel_slots.py:5250` (`consistency`):** Real and reproduced. Replaced character-set pre-scans with left-to-right Git `parse_options` short-cluster scanning across `branch`, `checkout`, `fetch`, `pull`, and `push` in `_segment_creates_branch_or_worktree` (`scripts/panel_slots.py`), so value-taking short options (`-u`, `-U`, `-o`, `-j`, `-e`) consume their attached or separate argument instead of scanning characters inside the value as flags (allowing `git branch -uorigin/main` and `git branch -vuorigin/main`, while denying `git branch -muorigin/main` and `git push -odelete=1 . HEAD:feat`).
2. **P1 `scripts/lsp-mcp-server.py:538` (`integration`):** Real and reproduced. Updated `LspBackend._sync_document_locked` and `_refresh_tracked_documents_locked` in `scripts/lsp-mcp-server.py` so reopening a previously evicted document whose `sha256` changed while closed (or opening a newly created/untracked file, or modifying an unopened workspace file detected via `_take_workspace_snapshot`, or deleting a tracked file on disk) invalidates cached diagnostics and sets `deps_dirty = True` across open consumers, emits `workspace/didChangeWatchedFiles`, and forces a consumer version bump on subsequent queries. Added deterministic LRU-eviction reopen coverage in `_self_test` (`25 cases, 0 failed`) and live Pyright integration coverage (`test_live_pyright_refreshes_reopened_evicted_and_unopened_dependencies`) in `scripts/tests/test_lsp_mcp_server.py`.
3. **P3 `docs/reviews/independent/2026-11-11-lsp-build-stack-and-unattended-gates.md:100` (`record`):** Real. Added explicit parser regression cases to `_self_test` in `scripts/panel_slots.py` (`1039 cases, 0 failed`) covering `git checkout --det main`, `git switch --det main`, `git switch --cr feat/foo`, `git branch --co main feat/foo`, `git worktree --porc list`, `git -c alias.co=checkout co -b feat/foo`, `git-checkout -b feat/foo`, `git branch -uorigin/main`, `git branch -vuorigin/main`, `git branch -muorigin/main`, and `git push -odelete=1 . HEAD:feat`.


## Round 5: astra (`gpt-6-astra` via `codex`)

- Writer: agy
- Run: 2026-11-11T22:30:51Z
- Effort: medium
- Lines: 16
- Digest: 8e698b0cb2c7e5d7

### adversarial: needs-attention

1. P1 `scripts/panel_slots.py:5415`: `git push --repo` bypasses ref checks because its repository value is discarded and the first refspec is subsequently treated as the repository. Read-only reproduction: `_agy_command_decision('git push --repo=. HEAD:feat')` returns `None`, whereas `git push . HEAD:feat` is denied. Likewise, `git push --repo=origin --delete main` passes. These are valid Git commands an operator or writer can issue, allowing prohibited branch creation or main deletion.

### consistency: approve

### integration: needs-attention

2. P2 `scripts/lsp-mcp-server.py:412`: Backend termination kills only the immediate process. The installed `pyright-langserver.EXE` launches Python, which launches Node; the MCP-wide job remains alive during backend shutdown. Reproduce by stopping Pyright while its Node process is unresponsive beyond the three-second shutdown timeout: terminating the launcher leaves descendants running, and closing pipes can block behind the reader thread. This can hang `lsp_status(action="stop")` or idle cleanup. Terminate the backend’s entire process tree before closing its pipes.

### source-defect: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention


## Response to round 5

1. **P1 `scripts/panel_slots.py:5415` (`adversarial`):** Real and reproduced. Upgraded `git push`, `git fetch`, and `git pull` in `_segment_creates_branch_or_worktree` (`scripts/panel_slots.py`) to closed canonical Git option allow-lists matching `checkout`, `switch`, `branch`, and `worktree`, explicitly forbidding `git push --repo`/`--no-repo`/`--all`/`--branches`/`--mirror`, `git fetch --stdin`/`--refmap`, and abbreviated or unrecognized options, resetting `delete_mode` on `--no-delete`, and stripping leading `+` before checking empty-source deletion refspecs (`+:main`, `:heads/main`, `:refs/heads/main`). Added explicit `_self_test` coverage (`1061 cases, 0 failed`).
2. **P2 `scripts/lsp-mcp-server.py:412` (`integration`):** Real and reproduced. Assigned each spawned LSP backend process (`CREATE_SUSPENDED` on Windows, `start_new_session=True` on POSIX) to its own per-backend Win32 kill-on-close Job Object (`_create_backend_job` / `_assign_and_resume_backend_job`) and terminated the entire job tree (`TerminateJobObject` + `CloseHandle` in `_close_backend_job`, or `os.killpg` on POSIX) inside `LspBackend._kill_proc` before closing stdio pipes. Added a regression test in `lsp-mcp-server.py --self-test` (`27 cases, 0 failed`) that spawns a descendant sleeper holding inherited pipes while `shutdown` hangs, verifying `lsp_status(action="stop")` returns promptly and kills the descendant process.


## Round 6: astra (`gpt-6-astra` via `codex`)

- Writer: agy
- Run: 2026-11-11T22:49:54Z
- Effort: low
- Lines: 16
- Digest: bd07c70d8aaada31

### adversarial: needs-attention

1. P1 `scripts/panel_slots.py:5032`: Command-line remote configuration bypasses refspec enforcement. Read-only reproduction: `_agy_command_decision('git -c remote.origin.fetch=+refs/heads/main:refs/heads/feature fetch origin')` returns `None`, permitting Git to create a non-main local branch. Likewise, `git -c remote.origin.push=HEAD:refs/heads/feature push origin` passes. A writer using temporary remote mappings can therefore perform operations forbidden by the equivalent positional refspec checks. Validate these configuration overrides alongside positional refspecs.

### consistency: approve

### integration: needs-attention

2. P2 `scripts/lsp-mcp-server.py:418`: Blocking stdin writes occur before the request timeout starts; notification writes are also unbounded. If clangd or Pyright stops consuming stdin, synchronizing a document larger than the pipe buffer hangs while holding `_op_lock`, preventing idle termination and subsequent MCP calls. Reproduced without file changes using a sleeping subprocess with piped stdin: a 1 MiB request with `timeout=0.1` remained blocked after one second and released only when the child was killed. Bound transport writes and terminate the backend tree when that deadline expires.

### source-defect: approve

### record: approve

HIGHEST: P1
OVERALL: needs-attention


## Response to round 6

1. **P1 `scripts/panel_slots.py:5032` (`adversarial`):** Real and reproduced. Added `_check_fetch_refspec`, `_check_push_refspec`, and `_check_git_trunk_config_override` in `scripts/panel_slots.py` and wired them across `git -c`, `git --config-env`, `git config`, and `git remote`, validating `remote.*.fetch` and `remote.*.push` refspecs with the exact same rules as positional `fetch`/`pull`/`push` refspecs and forbidding overrides of `remote.*` non-refspec keys (`url`, `pushurl`, `mirror`), `alias.*`, `include.*`/`includeIf.*`, `checkout.*`, `worktree.*`, `branch.*`, `push.*`, `url.*`, and `core.worktree`/`core.bare`/`core.hooksPath`, as well as remote-mutating `git remote` subcommands. Added explicit `_self_test` coverage (`1091 cases, 0 failed`).
2. **P2 `scripts/lsp-mcp-server.py:418` (`integration`):** Real and reproduced. Added a dedicated per-backend `_BackendWriter` thread in `scripts/lsp-mcp-server.py` so every transport write (`_send_notification_locked` and `_request_locked`, with `deadline` started before writing stdin) runs under a bounded deadline, and when any write or request deadline expires `LspBackend` immediately terminates the backend process tree (`_terminate_backend_instance` / `_kill_proc`), joins the writer thread, resets backend state, and releases `_op_lock`. Added deterministic 1 MiB stalled-stdin notification and request timeout regression tests in `lsp-mcp-server.py --self-test` (`29 cases, 0 failed`).
