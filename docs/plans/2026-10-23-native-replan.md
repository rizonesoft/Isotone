# The native re-plan

> **Goal:** every section in `todo/` can be executed on the native stack from `docs/specs/2026-10-22-native-stack-design.md`, by a runner with no conversation context, from the first phase to the suite bundle, so an unattended `process-plan` campaign can run the plan end to end and produce Stilus, Gesso, and Albumen as complete, production-ready C++23 products with our own UI, laid out the way Illustrator, Photoshop, and Lightroom Classic users expect.

**Source:** the operator approved the native stack spec on 2026-10-23 ("Approve, start re-plan"), and the same day chose how the rest runs (`docs/dev/decisions.md`, "2026-10-23: The unattended campaign"): the campaign re-plans each phase ahead of building it, C# is removed by the first section that can do it safely, blockers are worked around and queued, and versioning is SemVer from tags, automated. The spec's section "The re-plan, and what it must preserve" is this plan's contract. Started 2026-10-23.

## Why a plan

The tree held 772 sections in 79 files (14 stamped, 758 open), nearly all written against C#, WPF, and .NET. They are re-planned in waves; the first waves were done in attended sessions, and every later wave is a re-plan section in `todo/00-workspace/TODO-07-native-replan.md` that the campaign runs as the first row of the phase it rewrites.

## How sections are treated

- **Rewritten in place** (the default for open work): a section whose feature scope carries over keeps its address, its cross-references, its parity catalog rows, and its acceptance requirements; its checklist, `Done when:` clauses, and Test checkpoints are re-expressed for the native stack (C++23, `native/`, GoogleTest through CTest, UI Automation and `SendInput` driven runs, the C++ gates). AGENTS.md requires section addresses and bidirectional cross-references to be preserved, and the parity validator requires every catalog row to name a live section, so in-place rewriting is the rule and supersession the exception.
- **Kept:** a stamped section stays exactly as it shipped. A section that is stack-neutral (the TODO tooling, operator rows, research) is kept as written or touched only where it names the .NET stack.
- **Superseded:** a whole file whose purpose exists only because of the C# code (a WPF framework removal, a C# project restructure, a .NET-only debt list) gets `status: superseded` and `superseded_by` naming its native successor file; any catalog row or cross-reference into it is re-pointed in the same commit.
- **New:** the native spine, the foundations, and anything the spec requires that no section owns are authored as new files through `create-todo`.

Every row of the map below names one of these, and every superseded or rewritten row names where its acceptance requirements went.

## Parking

Until a file is re-planned, its frontmatter is `status: blocked` and a line under its Goal reads `> **Re-plan:** parked until the native re-plan reaches it (docs/plans/2026-10-23-native-replan.md).`. A blocked file's sections are deferred (`query ready`, `query plan`, and every campaign skip them), so no runner can execute C#-era work. A re-plan section unparks each file it finishes (`status: draft`, the Re-plan line removed). `todo/99-manual/` stays live: its rows are operator steps that do not depend on the stack.

## Waves

| Wave | Scope | Done by |
| ---- | ----- | ------- |
| W0 | This plan, the supersession map, parking | attended, 2026-10-23 |
| W1 | The native spine (`D00 T05`) and the C++ standard, register, benchmarks, and advisory job (`D00 T04`, rewritten) | attended, 2026-10-23 |
| W1b | Retiring the C# code (`D00 T06`) and the re-plan sections (`D00 T07`) | attended, 2026-10-23 |
| W2 to W9 | The foundations, the UI toolkit, the layout maps, every app and its parity, distribution and the post-release phases, the release and documentation domains, the standards | the campaign, through `D00 T07`'s re-plan sections, each the first row of its phase |

## What every re-plan section must deliver

A re-plan section is done only when all of these hold for the files it owns, and its review loop runs to a clean round like any section:

1. **Every section rewritten, kept, or superseded** by the rules above, the map row updated, the file unparked; no open section names WPF, XAML, .NET, `dotnet`, NuGet, MinVer, or a C# project as its implementation (`git grep` over the files is empty).
2. **Executable without context, and complete:** each feature section's scope names every entry point and companion the completion checklist in `docs/completion-review-prompt.md` lists for it (menu items and shortcuts, tool rail, options bar, panel, and context menu buttons, dialogs and their controls, states, undo, persistence, round trips, accessibility, the user guide entry, the log line), or names the section that owns each one; each item has a backticked path or symbol and a `Done when:`; each Test checkpoint cites a proof from `todo/README.md` "What counts as proof" that runs on a gate that exists by then; dependencies name the foundation or toolkit section that provides what the section uses.
3. **Design, exactly:** every surface section carries its `**Design:**` line to `docs/design/` (tokens, component specs, shell layout) and its `**Fidelity:**` golden folder; the native toolkit implements the design contract (`standards/design-contract.md`) with the mechanism names the re-plan renamed from WPF.
4. **Layout, exactly as Adobe users expect:** every section that builds a menu, shortcut, tool, options bar, panel, panel button, or dialog cites its layout map (`docs/design/layout-maps/`, `D01 T13`) and its conformance test; the maps cover dialogs (layout, control order, labels, defaults) and terminology as well as menus, tools, and panels; Adobe's own terms are used exactly except Adobe trademarks, which take the glossary's recorded near-equivalents; Isotone's own features sit beside their nearest Adobe analog by the map's recorded placement rule.
5. **Parity complete:** every parity catalog row the files own still resolves to a live section, and none is dropped (`python scripts/todo-graph.py validate` reports no `parity-*` finding).
6. **Releases never block development:** each app release is split into a release-candidate section the campaign completes (built, tested, packaged, signed-ready, notes and changelog written) and a publish section that depends on the `todo/99-manual/` rows (signing certificate, download storage and secrets); no later phase depends on a publish section.
7. **Versioning as decided:** release and packaging sections use SemVer 2.0 per app from its own tag, computed by CMake from git; the Windows four-part file version with a build number; `alpha`, `beta`, and `rc` channels in the update feeds; Conventional Commits with app scopes generating each app's changelog and next version; version and commit embedded in every binary.
8. **Performance fixtures:** each app's first performance section commits that app's small, typical, and large fixture documents under `native/tests/fixtures/<app>/benchmark/`, the large one at the plan's documented limits, and measures the spec's goals on them (`D00 T04 §2`, spec "Goals and how each is measured").
9. **Gates green:** `python scripts/todo-graph.py validate` (no FATAL, no new WARN), `plan --sync` then `plan --check`, and `python scripts/todo-claims.py` pass, with every rewritten Current state re-measured as claims.

## Acceptance

- Every section is in the map below with a final treatment, and no open section names WPF, XAML, .NET, `dotnet`, or a C# project as its implementation.
- Every Test checkpoint cites a gate that exists or that an earlier section in the dependency graph creates.
- `validate` reports no FATAL and no new WARN, `plan --check` and `todo-claims.py` pass, every parity catalog row resolves, no file is parked for the re-plan and no map row reads `pending`, and every row `query ready` lists is written for the native stack.
- The last re-plan section runs `groom-plan` over the whole tree and a plan review whose final round returns no P1 or P2.

## The supersession map

`todo/supersession-2026-10.md`, generated from `python scripts/todo-graph.py query plan` and kept current by every wave and re-plan section.
