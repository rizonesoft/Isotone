# Isotone -- TODO Index

The live execution plan for the Isotone Graphics Suite. Format spec: [README.md](./README.md). Ordered plan: [implementation-plan.md](./implementation-plan.md).

## How to use this tree

- **This file** carries domain order and the active TODOs. Keep it at that altitude: no checklists.
- **Each domain's `INDEX.md`** lists its own TODO files and is the place to look for scope within a domain. Ideas that are not planned work live in [`backlog.md`](./backlog.md), never in a domain.
- Give every topic **one canonical home**. Cross-link with XREFs instead of duplicating scope.
- Numbering is local to a domain (`TODO-01`, `TODO-02`) and never reused.
- When work graduates to documentation, move it to the domain's Completed section rather than leaving a stale checklist here.

## What this plan is

Isotone is a .NET 11 WPF monorepo holding three standalone creative applications: **Stilus** (vector, imported from Bezier under `src/Stilus/`), **Gesso** (raster, imported under `src/Gesso/`), and **Albumen** (darkroom and asset manager, planned). They are developed together and distributed separately. Shared code lives in `Isotone.Core` (non-UI) and `Isotone.UI` (WPF), and only once a second app needs it. The imported apps' legacy roadmaps were mined into this tree on 2026-09-26 and are kept for reference in [`../docs/legacy/`](../docs/legacy/README.md); the same day the plan was bounded by [`budget.json`](./budget.json), and the feature ideas no planned row needs moved to [`backlog.md`](./backlog.md). Also on 2026-09-26 the operator decided that Stilus gets every CorelDRAW and every Illustrator feature: the parity catalog in [`../docs/parity/`](../docs/parity/README.md) routes each one to a section, and ten parity phases (4 to 13) run between Stilus 0.1.0 and Gesso's foundation. The operator then decided that Gesso gets every Photoshop feature and those of two other popular raster editors (Affinity Photo and GIMP 3): the Gesso parity catalog routes each one the same way, and twelve parity phases (16 to 27) run between Gesso 0.1.0 and Albumen's foundation. On 2026-09-27, when the operator worried "features will be left behind", the operator decided to plan the work deferred to after the first release as real sections: Phases 42 to 45 run suite automation, video and audio with animation, on-device models with the GPU develop path, and Albumen's remaining formats after the suite's first release, ending with the `isotone-v1.1.0` bundle.

## Domain order

Domains are numbered in **allocation order**. `DNN TNN §N` cross-references encode the domain number, so a remap rewrites every reference in the same commit. A new domain appends after the last one.

**Execution order lives in the dependency graph**, not in this column. Ask the graph: `python scripts/todo-graph.py query ready`. The **Phase** column below is the coarse sequencing.

| No. | Domain | Phase | Purpose |
| :-: | ------ | :---: | ------- |
| 00 | [Workspace](./00-workspace/INDEX.md) | 0-3 | Toolchain, solution, gates, CI, the TODO system, import debt, and visual baselines. |
| 01 | [Core](./01-core/INDEX.md) | 2, 3, 6, 9, 10, 12, 13, 15, 21-23, 36, 42-44 | `Isotone.Core` (non-UI services) and `Isotone.UI` (the WPF house style), each filled only when two apps need it, plus the pixel engine, color management, and the AI core the operator placed there for the Stilus parity phases, and the pixel engine extensions and the develop engine the Gesso parity phases add, and the suite automation, media, on-device model, and GPU develop systems of the post-release phases. |
| 02 | [Stilus](./02-stilus/INDEX.md) | 1, 2, 3, 4-13, 41, 42 | The vector editor: rename, foundation, 0.1.0, then parity with Illustrator 30.8 and CorelDRAW 2026 through 1.0.0, then imports on shared decoders and automation after the first release. |
| 03 | [Gesso](./03-gesso/INDEX.md) | 1, 14, 15, 16-27, 41, 42-44 | The raster editor: rename, WPF-UI removal, rendering, 0.1.0, then parity with Photoshop 27.10, Affinity 3.3, and GIMP 3.2.6 through 1.0.0, then RAW import once Albumen's decoder is shared, then automation, video and animation, and on-device models after the first release. |
| 04 | [Albumen](./04-albumen/INDEX.md) | 28-39, 42-45 | The darkroom and photo library: planned from nothing, 0.1.0, then parity with Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 through 1.0.0 (a fast default viewer, browsing without importing, batch tools), ending with accessibility, then automation, video and audio, on-device models, and the remaining formats after the first release. |
| 05 | [Release](./05-release/INDEX.md) | 3, 39, 40, 45 | Clean-machine proof, signing, arm64, the update check, winget, and the suite bundle. |
| 06 | [Docs](./06-docs/INDEX.md) | 3, 15, 29, 40 | User guides, developer docs that stay true to the tree, and the documentation site. |
| 99 | [Manual](./99-manual/INDEX.md) | 99 | Operator-only steps: repository settings, the signing certificate, the icon license and accent confirmations, the copyright assignment, trademarks, the CLA decision, download storage, and the product pages. |

`99-manual` is numbered apart from the allocation sequence on purpose, as ScratchPad's is: it is the operator's phase, not a build area, and a new build domain still appends after `06`.

The Phase column is the coarse domain grouping, not an executable schedule. Current dependency-safe sequencing and live counts come only from [`implementation-plan.md`](./implementation-plan.md) plus `python scripts/todo-graph.py query stats`. Do not infer readiness from a domain number or repeat fixed totals here.

## Active TODOs

| TODO | Domain | Title |
| ---- | ------ | ----- |
| [TODO-01](./00-workspace/TODO-01-dev-automation.md) | 00-workspace | Dev-Automation Wiring |
| [TODO-02](./00-workspace/TODO-02-build-and-test-debt.md) | 00-workspace | Build and Test Debt from the Import |
| [TODO-03](./00-workspace/TODO-03-repo-layout.md) | 00-workspace | Repository Layout, Visual Baselines, and App Icon Export |
| [TODO-04](./00-workspace/TODO-04-native-code-policy.md) | 00-workspace | The Native-Code Policy, Its Gate, and the Benchmark Harness |
| [TODO-01](./02-stilus/TODO-01-stilus-structure.md) | 02-stilus | Stilus Layout, Names, and Composition Root |
| [TODO-01](./03-gesso/TODO-01-gesso-structure.md) | 03-gesso | Gesso Layout, Names, the Snapshot Port, and WPF-UI Removal |

Every other TODO is listed in its domain's `INDEX.md`; the files above hold the rows that are ready first (Phases 0 and 1).
