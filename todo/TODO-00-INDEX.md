# Photon -- TODO Index

The live execution plan for the Photon Graphics Suite. Format spec: [README.md](./README.md). Ordered plan: [implementation-plan.md](./implementation-plan.md).

## How to use this tree

- **This file** carries domain order and the active TODOs. Keep it at that altitude: no checklists.
- **Each domain's `INDEX.md`** lists its own TODO files and is the place to look for scope within a domain. Ideas that are not planned work live in [`backlog.md`](./backlog.md), never in a domain.
- Give every topic **one canonical home**. Cross-link with XREFs instead of duplicating scope.
- Numbering is local to a domain (`TODO-01`, `TODO-02`) and never reused.
- When work graduates to documentation, move it to the domain's Completed section rather than leaving a stale checklist here.

## What this plan is

Photon is a .NET 11 WPF monorepo holding three standalone creative applications: **Nodus** (vector, imported from Bezier under `src/Nodus/`), **Imago** (raster, imported under `src/Imago/`), and **Lumen** (darkroom and asset manager, planned). They are developed together and distributed separately. Shared code lives in `Photon.Core` (non-UI) and `Photon.UI` (WPF), and only once a second app needs it. The imported apps' legacy roadmaps were mined into this tree on 2026-09-26 and are kept for reference in [`../docs/legacy/`](../docs/legacy/README.md); the same day the plan was bounded by [`budget.json`](./budget.json), and the feature ideas no planned row needs moved to [`backlog.md`](./backlog.md). Also on 2026-09-26 the operator decided that Nodus gets every CorelDRAW and every Illustrator feature: the parity catalog in [`../docs/parity/`](../docs/parity/README.md) routes each one to a section, and ten parity phases (4 to 13) run between Nodus 0.1.0 and Imago's foundation. The operator then decided that Imago gets every Photoshop feature and those of two other popular raster editors (Affinity Photo and GIMP 3): the Imago parity catalog routes each one the same way, and twelve parity phases (16 to 27) run between Imago 0.1.0 and Lumen's foundation.

## Domain order

Domains are numbered in **allocation order**. `DNN TNN §N` cross-references encode the domain number, so a remap rewrites every reference in the same commit. A new domain appends after the last one.

**Execution order lives in the dependency graph**, not in this column. Ask the graph: `python scripts/todo-graph.py query ready`. The **Phase** column below is the coarse sequencing.

| No. | Domain | Phase | Purpose |
| :-: | ------ | :---: | ------- |
| 00 | [Workspace](./00-workspace/INDEX.md) | 0, 2 | Toolchain, solution, gates, CI, the TODO system, import debt, and visual baselines. |
| 01 | [Core](./01-core/INDEX.md) | 2, 3, 6, 9, 10, 12, 13, 15, 21-23, 36 | `Photon.Core` (non-UI services) and `Photon.UI` (the WPF house style), each filled only when two apps need it, plus the pixel engine, color management, and the AI core the operator placed there for the Nodus parity phases, and the pixel engine extensions and the develop engine the Imago parity phases add. |
| 02 | [Nodus](./02-nodus/INDEX.md) | 1, 2, 3, 4-13, 41 | The vector editor: rename, foundation, 0.1.0, then parity with Illustrator 30.8 and CorelDRAW 2026 through 1.0.0. |
| 03 | [Imago](./03-imago/INDEX.md) | 1, 14, 15, 16-27, 41 | The raster editor: rename, WPF-UI removal, rendering, 0.1.0, then parity with Photoshop 27.10, Affinity 3.3, and GIMP 3.2.6 through 1.0.0, then RAW import once Lumen's decoder is shared. |
| 04 | [Lumen](./04-lumen/INDEX.md) | 28-39 | The darkroom and photo library: planned from nothing, 0.1.0, then parity with Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 through 1.0.0 (a fast default viewer, browsing without importing, batch tools), ending with accessibility. |
| 05 | [Release](./05-release/INDEX.md) | 3, 39, 40 | Clean-machine proof, signing, arm64, the update check, winget, and the suite bundle. |
| 06 | [Docs](./06-docs/INDEX.md) | 3, 15, 29, 40 | User guides, developer docs that stay true to the tree, and the documentation site. |
| 99 | [Manual](./99-manual/INDEX.md) | 99 | Operator-only steps: repository settings, the signing certificate, icon licenses, accent colors. |

`99-manual` is numbered apart from the allocation sequence on purpose, as ScratchPad's is: it is the operator's phase, not a build area, and a new build domain still appends after `06`.

The Phase column is the coarse domain grouping, not an executable schedule. Current dependency-safe sequencing and live counts come only from [`implementation-plan.md`](./implementation-plan.md) plus `python scripts/todo-graph.py query stats`. Do not infer readiness from a domain number or repeat fixed totals here.

## Active TODOs

| TODO | Domain | Title |
| ---- | ------ | ----- |
| [TODO-01](./00-workspace/TODO-01-dev-automation.md) | 00-workspace | Dev-Automation Wiring |
| [TODO-02](./00-workspace/TODO-02-build-and-test-debt.md) | 00-workspace | Build and Test Debt from the Import |
| [TODO-03](./00-workspace/TODO-03-repo-layout.md) | 00-workspace | Repository Layout, Visual Baselines, and App Icon Export |
| [TODO-01](./02-nodus/TODO-01-nodus-structure.md) | 02-nodus | Nodus Layout, Names, and Composition Root |
| [TODO-01](./03-imago/TODO-01-imago-structure.md) | 03-imago | Imago Layout, Names, the Snapshot Port, and WPF-UI Removal |

Every other TODO is listed in its domain's `INDEX.md`; the files above hold the rows that are ready first (Phases 0 and 1).
