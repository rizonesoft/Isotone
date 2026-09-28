# Legacy roadmaps

These are the roadmaps the two imported applications carried before they joined the Photon monorepo. They are kept for reference only: **the live plan is [`todo/`](../../todo/TODO-00-INDEX.md)**, and nothing here is a work item until a TODO section owns it.

| File | Came from | What it was |
| ---- | --------- | ----------- |
| [`stilus-roadmap.md`](stilus-roadmap.md) | `src/Nodus/TODO.md` (Bezier, last edited 2025-12-15) | 26 phases (0 to 25), roughly 2,200 open and 420 checked items |
| [`gesso-roadmap.md`](gesso-roadmap.md) | `src/Imago/TODO.md` (Imago, "Last Updated: December 2024") | 12 phases (0 to 11), 385 open and 102 checked items |

## How they were mined

On 2026-09-26 both files were read end to end and converted into the plan under `todo/`:

- Near-term work (the foundation, correctness, and the first release of each app) became granular sections in `todo/02-nodus/` and `todo/03-imago/`.
- The long tail first became coarser roadmap sections, each carrying a `-> SOURCE: legacy-...` line. When the plan was bounded later on 2026-09-26, the ones nothing else needed moved to [`todo/backlog.md`](../../todo/backlog.md) (B-001 to B-036, keeping their SOURCE keys); the few that own deferrals or acceptance-bar aims stay as sections in the trimmed roadmap files.
- Nodus phases 16 to 25 (collaboration, cross-platform and mobile, 3D, enterprise, industry suites, gamification, audio and video, sustainability, AR and VR) and the Imago "Killer Feature Ideas" list were **not** converted. They are outside the product the suite is building; a future plan that wants one files it through `add-todo`.

## Read the check marks with suspicion

A `[x]` in these files means somebody wrote the code, not that a user can reach it. Measured on 2026-09-26:

- 25 of the 31 services under `src/Nodus/Bezier.Core/Services/` are referenced only by tests, and `PathOperationsService.BooleanOp` returns its first input unchanged ("This will be implemented with SkiaSharp in the Desktop layer"), yet the legacy roadmap checks boolean operations as done.
- The Monaco editor (Nodus 5.6) is checked, but no WebView2 package is referenced anywhere.
- WPF-UI, `FluentWindow`, Mica, and ReactiveUI are checked in the Imago roadmap; the suite forbids WPF-UI and uses CommunityToolkit.Mvvm, so those items are debt, not progress.

The plan under `todo/` records what was verified in each file's `Current state` block, with claims `scripts/todo-claims.py` re-measures.
