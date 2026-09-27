# Section gates

The gate card for `process-todo-section`, `review-todo-section`, and `process-todo-file`. When `standards/testing.md` exists and disagrees with this card, the file wins, and this card is corrected in the same commit.

Quote the exit code, the passed, failed, and skipped counts, and the last lines of output. Leave the full log under `build/` (gitignored), never in the context.

## Every section: the one-command sweep

```powershell
pwsh scripts/check-all.ps1
```

It builds `Isotone.slnx` in Debug and Release with warnings as errors, runs `dotnet test`, and runs the TODO gates (`todo-graph.py validate`, `todo-graph.py plan --check`, `todo-claims.py`, `campaign_guard.py --self-test`). Every gate runs even after an earlier one fails, and it prints a table of gate results; green means exit 0 with every gate `PASS`. A `SKIP` row (no Python, a script absent) is not green: quote it and fix the cause. `-SkipBuild` reuses the last build for a re-run of the tests and gates only, while iterating, never for the commit-time run; `-Config Debug` runs the tests against the Debug build instead of the default Release.

## Every code section: the whole suite

```powershell
dotnet test Isotone.slnx
```

Green means zero failed. Skipped tests are quoted by name with their skip reason; a skip with no reason is a failure of the test, not a pass. While iterating, narrow to the touched tests:

```powershell
dotnet test Isotone.slnx --filter "FullyQualifiedName~<Namespace.Class>"
```

The filtered run is iteration only. The commit-time quote comes from the unfiltered run at the commit being created.

## Surface sections: design-lint

```powershell
python scripts/design-lint.py --baseline docs/design/.lint-baseline.json
```

Green means `0 new, 0 stale`. It runs in `scripts/check-all.ps1`, the commit hook (on the staged tree), and the `build` workflow; the rules and the baseline are in the script's docstring and `standards/design-contract.md`. A new violation is fixed with a token key, never recorded. A stale entry means the section fixed a recorded violation: shrink the baseline with `--update-baseline` in the same range and quote the removed count. `--allow-add` is never run by a section; review alone may, with a reason it quotes in the stamp.

## Surface sections: the Design line

`python scripts/todo-graph.py validate` reports no `design-*` finding, and `python scripts/todo-graph.py query design` shows the section with a Design line and out of `todo/.design-baseline`.

## Surface sections: visual regression (once `D01 T01 §9` ships)

```powershell
pwsh scripts/visual-tests.ps1 -Filter <scenario>
python scripts/render-design-reference.py --components <Comp>
```

The first renders the section's scenarios into `build/wpf-renders/` and compares them with the approved goldens under `docs/captures/golden/` within the contract's tolerance; the second renders the design's own previews into `build/design-reference/` with the side-by-side report. Quote the pass count and, on a failure, the differing pixel count and largest difference it prints. A scenario with no golden yet fails naming the approve command: review approves it, the section does not. Until `D01 T01 §9` ships, a surface section says so in its checkpoint and relies on the launch smoke below plus the design reference renders.

## Surface sections: launch smoke (placeholder)

Isotone has no UI test suite yet. Until the workspace domain ships one, a section that builds or changes a surface owes a driven launch smoke by hand, which needs a display session (`**Requires:** display-session`):

1. Build Debug, then launch the touched app's executable from its output folder under `artifacts/`.
2. Drive the surface the section changed: open the fixture named in the checkpoint, exercise every control the section accounts for, and close the app through its own menu.
3. Record the evidence: the app stayed up, the Serilog log for the run carries no `Error` or `Fatal` line (quote the count), and a capture of the changed surface is committed under `docs/captures/<app>/` as a record of the run (the design and the goldens, not the capture, are what it is judged against).

A launch smoke is evidence of one run. It never substitutes for a unit test on the logic behind the surface, and when the UI suite lands this section of the card is replaced, not kept beside it.

## Document sections: fidelity round trip

A section that reads or writes a file format re-runs its round-trip tests unfiltered (`dotnet test Isotone.slnx --filter "Category=Fidelity"` once the category exists, else the named test classes) and quotes the per-fixture result, including the tolerance used for any pixel comparison.

The file-level full suite and every fidelity fixture belong to `process-todo-file`.
