# Section Gates

The gate card for `process-todo-section`, `review-todo-section`, and `process-todo-file`. When `standards/testing.md` disagrees with this card, `standards/testing.md` wins and this card is updated in the same commit. Quote the exit code, pass/fail/skip counts, and final summary lines; keep full logs under `build/` (gitignored), never in tracked paths or unbounded chat output.

## Every section: the one-command sweep

```powershell
pwsh scripts/check-all.ps1
```

Runs the full local gate table: Python TODO and review-pin gates (`todo-graph.py self-test`, `todo-graph.py validate`, `todo-graph.py plan --check`, `todo-claims.py`, `todo-findings.py --check`, `todo-runs.py --check`, `campaign_guard.py --self-test`, `review_pin.py --check`, `review-dispatch.py --check-pin`, `panel_slots.py validate`, `lsp-mcp-server.py --self-test`, and all unit test suites under `scripts/tests/`) plus the native C++23 stages (`D00 T05 §7`). Green means exit `0` with every gate `PASS` (a `SKIP` row is never commit-time evidence for an owed gate). Use `-SkipNative` only while iterating on pure Python/docs changes, never for the commit-time sweep of a section touching `native/`, a native script, or `native/toolchain.json`.

## Native C++23 sections: the native stages

`pwsh scripts/check-all.ps1` runs every native stage inside `scripts/dev-env.ps1` with full logs in `build/check-all/<stage>.log`:

| Stage | Proves |
| --- | --- |
| `native presets` | Every non-hidden configure preset in `native/CMakePresets.json` is owned by a build stage |
| `native toolchain` | Local Visual Studio/Clang/CMake/Ninja/Windows SDK match `native/toolchain.json` for x64 and ARM64 (`dev-env.ps1 -Check`) |
| `native x64-debug`, `native x64-release` | Configure, build, and CTest GoogleTest suite on x64 (`cmake --workflow`), plus `native benchmarks smoke` |
| `native x64-asan` | CTest suite under AddressSanitizer |
| `native x64-fuzz-msvc` | libFuzzer targets (`isotone_add_fuzz_target`), static library closures, and `-runs=0` smoke under MSVC `/fsanitize=address /fsanitize=fuzzer` |
| `native arm64-debug`, `native arm64-release`, `native arm64-asan` | ARM64 cross-builds (ARM64 test execution runs on ARM64 CI in `D00 T05 §8`) |
| `native x64-dist`, `native arm64-dist` | Release distribution presets |
| `native deps` | `docs/dev/native-libraries.md` matches installed vcpkg trees and link graphs (`native-deps-lint.py`, `D00 T04 §1`) |
| `native analyze` | MSVC `/analyze` clean on x64 Debug and ARM64 Release |
| `native std`, `native pe` | Single pinned C++23 standard switch across all TUs (`native-std-check.py`), Control Flow Guard + x64 CET on all linked PE images (`native-pe-check.py`) |
| `native format`, `native tidy` | Zero `clang-format` and `clang-tidy` findings |
| `native artifacts`, `native artifacts asan`, `native asan-coverage` | Shipping DLL import allowlist, static CRT/vcpkg linkage, current build outputs, and full ASan archive instrumentation (`native-artifact-gate.py`) |

While iterating on a single C++ target, run a fast targeted Ninja + CTest loop inside `dev-env.ps1` (`pwsh scripts/dev-env.ps1 -Arch x64 -Run 'cmake --build native/../artifacts/native/x64-debug --target <target>; ctest --test-dir artifacts/native/x64-debug -R <Filter> --output-on-failure'`), and verify `lsp_diagnostics` via `isotone-lsp` before running the full commit-time sweep.

## Delegated sections: scope and pin audit

When the section invoked any read-only `research` subagent (`standards/delegation.md`):

```powershell
python scripts/weakening-scan.py --scope build/delegation/<task>/before.json --
python scripts/panel_slots.py delegate-audit --session <Conversation ID>
```

Both must exit `0` (`0 problem(s)` and `0 failing`).

## Surface sections: design-contract gates

```powershell
python scripts/design-lint.py --baseline docs/design/.lint-baseline.json
python scripts/todo-graph.py validate
python scripts/render-design-reference.py --components <Comp>
```

- `design-lint.py` must print `0 new, 0 stale` (shrink the baseline with `--update-baseline` when removing legacy entries; never pass `--allow-add` during implementation).
- `todo-graph.py validate` must report zero `design-*` findings and `todo-graph.py query design` must show the section carrying a live `**Design:**` line outside `todo/.design-baseline`.
- Once the native visual-test runner ships (`todo/README.md` Proof table), run the golden comparison harness and hand renders to `review-todo-section` for golden approval.

## Cadence (operator decisions 2026-11-12 and 2026-11-13, `docs/dev/decisions.md`, "Test cadence")

CI does the heavy lifting. Locally, run only what is fast and what gates a commit: the commit hook, the targeted test of the code changed, and for native code the `x64-debug` preset with a filtered `ctest -R` plus `pwsh scripts/native-format.ps1 -Check`. Push the candidate; the `build` and `plan-gates` workflows run the full table while the review passes run, and the stamp cites their green runs on the final reviewed commit by URL. Start a background read of CI on every push and carry on; when it reports red, stop and repair it before anything else. Run `pwsh scripts/check-all.ps1` locally only with no network, to reproduce a red CI run, or when the change is to the gates themselves.
