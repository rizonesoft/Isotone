# 02 Stilus

> **Phases 1, 2, 3, 4 to 13, 41, and 42**

Stilus, the vector editor, imported from Bezier under `src/Stilus/`. Stilus runs first among the apps: it is renamed and restructured, its orphan services triaged, its editing made correct, its documents made safe, and it ships `stilus-v0.1.0` before Gesso's foundation starts. After 0.1.0, the parity phases (4 to 13) bring Stilus to parity with every Illustrator 30.8 and CorelDRAW 2026 capability in the parity catalog ([`../../docs/parity/stilus-parity.md`](../../docs/parity/stilus-parity.md)): TODO-07 to TODO-16 own the features, TODO-17 ships one release per phase from `stilus-v0.2.0` to `stilus-v1.0.0`, and TODO-06's eight sections move into the parity phases where their dependents need them. The legacy roadmap entries the parity sections promoted left the backlog. On 2026-09-27 the operator promoted the Stilus catalog's remaining backlog rows too: TODO-18 plans the legacy vector, document, and raster formats (the old B-037 and B-038, the rasters on the shared codecs of `D01 T08`) in Phase 13 and GIMP XCF and camera RAW import (the old B-039) in Phase 41 after Gesso's XCF reader and Albumen's RAW decoder exist, `D02 T13 §17` plans interactive 3D in PDF (the old B-040), and `D02 T12 §10` runs third-party 8BF plug-in filters on the suite host `D01 T09` (the old B-012). Later on 2026-09-27, when the operator worried "features will be left behind", the last Stilus backlog rows (automation, the old B-041 and B-042) became TODO-19 (the Stilus object model, actions, scripts, macros in documents, and batch) on the suite automation of `D01 T10`, released as `stilus-v1.2.0` in Phase 42. **Corrected 2026-09-28:** TODO-17 continues past 1.0.0 with `stilus-v1.1.0` (Phase 41) and `stilus-v1.2.0` (Phase 42).

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-stilus-structure.md) | Stilus Layout, Names, and Composition Root | draft |
| [TODO-02](./TODO-02-stilus-service-triage.md) | Core Service Triage: Wire, Defer, or Delete | draft |
| [TODO-03](./TODO-03-stilus-editing.md) | Editing Correctness: Undo, Clipboard, and the View Model Split | draft |
| [TODO-04](./TODO-04-stilus-documents.md) | Stilus Documents: Save, Fidelity, Export, and Recovery | draft |
| [TODO-05](./TODO-05-stilus-release.md) | Stilus 0.1.0 | draft |
| [TODO-06](./TODO-06-stilus-roadmap.md) | Stilus after 0.1.0: Deferral Owners and Accessibility | draft |
| [TODO-07](./TODO-07-stilus-parity-document.md) | Stilus Parity: Document Model, Pages, Layers, Selection, and View | draft |
| [TODO-08](./TODO-08-stilus-parity-paths.md) | Stilus Parity: Drawing, Paths, Shapes, Shaping, and Transform | draft |
| [TODO-09](./TODO-09-stilus-parity-color.md) | Stilus Parity: Color, Fills, Strokes, Brushes, Transparency, Styles, and Symbols | draft |
| [TODO-10](./TODO-10-stilus-parity-type.md) | Stilus Parity: Type, Tables, and Graphs | draft |
| [TODO-11](./TODO-11-stilus-parity-effects.md) | Stilus Parity: Interactive and Live Effects | draft |
| [TODO-12](./TODO-12-stilus-parity-bitmaps.md) | Stilus Parity: Bitmaps, Tracing, and Raster Effects | draft |
| [TODO-13](./TODO-13-stilus-parity-print.md) | Stilus Parity: Color Management, Print, Prepress, and PDF | draft |
| [TODO-14](./TODO-14-stilus-parity-formats.md) | Stilus Parity: File Formats, Export, and Web | draft |
| [TODO-15](./TODO-15-stilus-ai.md) | Stilus AI: Editable, Suite-Aware, Reproducible | draft |
| [TODO-16](./TODO-16-stilus-parity-workspace.md) | Stilus Parity: Workspace, Customization, Preferences, and Utilities | draft |
| [TODO-17](./TODO-17-stilus-parity-releases.md) | Stilus Parity Releases: 0.2.0 to 1.0.0 | draft |
| [TODO-18](./TODO-18-stilus-legacy-formats.md) | Stilus Legacy Formats and Camera RAW: FreeHand, Publisher, Visio, PowerPoint, Corel Legacy, Metafiles, Legacy Rasters, XCF, and RAW | draft |
| [TODO-19](./TODO-19-stilus-automation.md) | Stilus Automation: the Object Model, Actions, Scripts, and Batch | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- Everything under `src/Stilus/` and `tests/Isotone.Stilus.Tests/`
- The Stilus user-facing surfaces, its SVG reader and writer, its exporters, and its release

## Out of scope

- Code a second app needs (01-core), installers and signing (05-release), the user guide's content (06-docs)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
