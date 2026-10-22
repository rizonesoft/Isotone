# The native re-plan

> **Goal:** every section in `todo/` can be executed on the native stack from `docs/specs/2026-10-22-native-stack-design.md`, by a runner with no conversation context, from the first phase to the suite bundle, so a campaign can run the plan end to end and produce Stilus, Gesso, and Albumen as complete, production-ready products.

**Source:** the operator approved the native stack spec on 2026-10-23 ("Approve, start re-plan"); the spec's section "The re-plan, and what it must preserve" is this plan's contract. Started 2026-10-23.

## Why a plan

The tree holds 772 sections in 79 files (14 stamped, 758 open), nearly all written against C#, WPF, and .NET. Re-planning them is multi-session work, so it runs in waves, each leaving the tree valid and committed.

## How sections are treated

- **Rewritten in place** (the default for open work): a section whose feature scope carries over keeps its address, its cross-references, its parity catalog rows, and its acceptance requirements; its checklist, `Done when:` clauses, and Test checkpoints are re-expressed for the native stack (C++23, `native/`, GoogleTest through CTest, UI Automation and `SendInput` driven runs, the C++ gates). AGENTS.md requires section addresses and bidirectional cross-references to be preserved, and the parity validator requires every catalog row to name a live section, so in-place rewriting is the rule and supersession the exception.
- **Kept:** a stamped section stays exactly as it shipped. A section that is stack-neutral (the TODO tooling, operator rows, research) is kept as written or touched only where it names the .NET stack.
- **Superseded:** a whole file whose purpose exists only because of the C# code (a WPF framework removal, a C# project restructure, a .NET-only debt list) gets `status: superseded` and `superseded_by` naming its native successor file; any catalog row or cross-reference into it is re-pointed in the same commit.
- **New:** the native spine and the foundations the spec's order of work lists are authored as new files through `create-todo`.

Every row of the map below names one of these, and every superseded or rewritten row names where its acceptance requirements went.

## Parking

Until a file is re-planned, its frontmatter is `status: blocked` and a line under its Goal reads `> **Re-plan:** parked until the native re-plan reaches it (docs/plans/2026-10-23-native-replan.md).`. A blocked file's sections are deferred (`query ready`, the plan, and every campaign skip them), so no runner can execute C#-era work while the re-plan is in progress. `todo/99-manual/` stays live: its rows are operator steps that do not depend on the stack.

## Waves

| Wave | Scope | Phases |
| ---- | ----- | ------ |
| W0 | This plan, the supersession map, parking | none |
| W1 | The native spine: `scripts/dev-env.ps1` and the pinned toolchain, presets, vcpkg baseline and triplets, the C++ gates (build, analysis, format, size, imports, sanitizer), CI for x64 and ARM64, the test harness, the dependency register (`D00 T04 §1` rewritten), and the proof standard in `todo/README.md` re-expressed for C++ | 0 |
| W2 | The foundations, each ending in its driven proof: document safety, tasks and threading, localization, the window and title bar on the swap chain, device loss and WARP, display color, text and TSF, UI Automation and screen readers, docking, the GPU canvas, runtime theming, the goldens environment, crash diagnostics | new phases after 0 |
| W3 | Isotone UI's controls and docking, the layout maps (`D01 T13`, with its 2026-10-22 review findings answered), Stilus native to its 0.1.0 scope, the design contract's mechanisms renamed for the native toolkit and design-lint retargeted to the C++ sources | 1 to 3 |
| W4 | Stilus parity | 4 to 13 |
| W5 | Gesso native and its parity | 14 to 27 |
| W6 | Albumen and its parity | 28 to 39 |
| W7 | Distribution, the shared-decoder imports, automation on Lua, media, local models, Albumen's remaining formats, the suite bundle | 40 to 45 |
| W8 | The release and documentation domains, the standards (`standards/*.md` for C++), and AGENTS.md's stack bullets once the spine has landed | across |
| W9 | `groom-plan` over the whole tree, then a plan review of the result | all |

Each wave unparks only the files it finishes. A wave's files are authored through the `create-todo` and `add-todo` skills, validated (`python scripts/todo-graph.py validate`, `plan --sync`, `python scripts/todo-claims.py`), reviewed through `python scripts/review-dispatch.py --writer claude` on the pinned route, and committed; nothing in a wave is marked done without that record.

## Acceptance

- Every section is in the map below with a final treatment, and no open section names WPF, XAML, .NET, `dotnet`, or a C# project as its implementation.
- Every Test checkpoint cites a gate that exists or that an earlier section in the dependency graph creates.
- `validate` reports no FATAL and no new WARN, `plan --check` and `todo-claims.py` pass, every parity catalog row resolves, and `query ready` starts with the native spine.
- The final plan review returns no P1 or P2.

## The supersession map

`todo/supersession-2026-10.md`, generated from `python scripts/todo-graph.py query plan` and kept current as each wave lands.
