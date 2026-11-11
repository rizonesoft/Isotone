# `isotone-lsp` Antigravity Plugin

Workspace Model Context Protocol (MCP) plugin exposing Isotone's pinned language servers (`clangd` on the pinned Visual Studio 2026 LLVM toolchain and `pyright-langserver`) to Google Antigravity (`agy`).

Antigravity discovers this plugin directly from `.agents/plugins/isotone-lsp/` at workspace priority without machine-specific paths.

## Exposed Tools

- `lsp_diagnostics`: syncs a workspace C/C++ or Python file from disk and returns compiler, type, and `clang-tidy` diagnostics.
- `lsp_hover`: returns hover type signatures and docstrings at a 1-based line and column.
- `lsp_definition`: resolves definitions (`textDocument/definition`) as workspace-relative `path:line:col` ranges.
- `lsp_references`: resolves references (`textDocument/references`) across the workspace.
- `lsp_document_symbols`: returns the hierarchical symbol outline (`textDocument/documentSymbol`) of a file.
- `lsp_workspace_symbols`: searches workspace-wide symbols (`workspace/symbol`) in `clangd` or `pyright`.
- `lsp_status`: inspects backend health, open-document counts, and idle timers, or stops idle backends immediately (`action="stop"`).

## Memory and Lifecycle Bounds

- **Lazy startup:** neither `clangd` nor `pyright-langserver` starts until a tool touches a matching file.
- **Pinned C++ flags and bounded AST cache:** `clangd` launches through `scripts/lsp-launch.py clangd` (`--pch-storage=disk`, `-j=4`, `--clang-tidy`, `--header-insertion=never`, `--background-index-priority=low`, and `--compile-commands-dir` pointing at `artifacts/native/x64-debug` or `x64-release`).
- **LRU open-document cap:** each backend keeps at most 16 `textDocument/didOpen` buffers open simultaneously, evicting older buffers with `textDocument/didClose`.
- **Automatic idle spin-down:** any backend idle for 300 seconds (`ISOTONE_LSP_IDLE_SECONDS`) shuts down cleanly via LSP `shutdown`/`exit` and restarts transparently on the next request.
- **Process-tree containment:** on Windows, `lsp-mcp-server.py` binds itself to its parent and places child language servers inside a `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` job object so no orphaned language server survives session exit.
