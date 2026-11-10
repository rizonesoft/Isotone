# Claude Code plugins

The plugins this repository ships for its own Claude Code sessions. `.claude/settings.json` declares this folder as the `isotone-tools` marketplace and enables what is listed here.

## isotone-lsp

Language servers, so a session sees compiler and type errors right after an edit and finds definitions and callers by symbol instead of by text search.

| Server | Files | What starts |
| ------ | ----- | ----------- |
| clangd | `.c`, `.h`, `.hpp`, `.cpp`, `.cc`, `.cxx`, `.inl`, `.ixx` | The clangd beside the pinned clang-tidy (Visual Studio's Clang component, `native/toolchain.json`), inside the pinned MSVC environment, reading `artifacts/native/x64-debug/compile_commands.json`, with clang-tidy on |
| pyright | `.py` | `pyright-langserver` from `PATH`, limited by `pyrightconfig.json` to the tracked script folders |

Both start through `python scripts/lsp-launch.py <server>`, which finds the binary, sets its environment, and holds it in a job object so it ends with the session.

## Setting up a clone

```powershell
npm install -g pyright                                   # the Python server; clangd comes with the pinned Visual Studio
claude plugin marketplace add ./tools/claude-plugins     # registers this folder on the machine
claude plugin list                                       # isotone-lsp@isotone-tools reads "enabled"
```

Build the `x64-debug` preset once so clangd has a compile database; without one it still starts and falls back to default flags. Run the marketplace command again after moving the clone, because the machine's registry holds its absolute path.

## Checking a server by hand

A server that does not start shows under `/plugin`, Errors. `python scripts/lsp-launch.py clangd` prints why (a missing Visual Studio component, a toolset `vcvarsall` cannot enter) to stderr and exits 1.
