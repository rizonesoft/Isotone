# 02 Nodus

> **Phases 1, 2, 3, 4 to 13, 41, and 42**

Nodus, the vector editor, imported from Bezier under `src/Nodus/`. Nodus runs first among the apps: it is renamed and restructured, its orphan services triaged, its editing made correct, its documents made safe, and it ships `nodus-v0.1.0` before Imago's foundation starts. After 0.1.0, the parity phases (4 to 13) bring Nodus to parity with every Illustrator 30.8 and CorelDRAW 2026 capability in the parity catalog ([`../../docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md)): TODO-07 to TODO-16 own the features, TODO-17 ships one release per phase from `nodus-v0.2.0` to `nodus-v1.0.0`, and TODO-06's eight sections move into the parity phases where their dependents need them. The legacy roadmap entries the parity sections promoted left the backlog. On 2026-09-27 the operator promoted the Nodus catalog's remaining backlog rows too: TODO-18 plans the legacy vector, document, and raster formats (the old B-037 and B-038, the rasters on the shared codecs of `D01 T08`) in Phase 13 and GIMP XCF and camera RAW import (the old B-039) in Phase 41 after Imago's XCF reader and Lumen's RAW decoder exist, `D02 T13 §17` plans interactive 3D in PDF (the old B-040), and `D02 T12 §10` runs third-party 8BF plug-in filters on the suite host `D01 T09` (the old B-012). Later on 2026-09-27, when the operator worried "features will be left behind", the last Nodus backlog rows (automation, the old B-041 and B-042) became TODO-19 (the Nodus object model, actions, scripts, macros in documents, and batch) on the suite automation of `D01 T10`, released as `nodus-v1.2.0` in Phase 42.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-nodus-structure.md) | Nodus Layout, Names, and Composition Root | draft |
| [TODO-02](./TODO-02-nodus-service-triage.md) | Core Service Triage: Wire, Defer, or Delete | draft |
| [TODO-03](./TODO-03-nodus-editing.md) | Editing Correctness: Undo, Clipboard, and the View Model Split | draft |
| [TODO-04](./TODO-04-nodus-documents.md) | Nodus Documents: Save, Fidelity, Export, and Recovery | draft |
| [TODO-05](./TODO-05-nodus-release.md) | Nodus 0.1.0 | draft |
| [TODO-06](./TODO-06-nodus-roadmap.md) | Nodus after 0.1.0: Deferral Owners and Accessibility | draft |
| [TODO-07](./TODO-07-nodus-parity-document.md) | Nodus Parity: Document Model, Pages, Layers, Selection, and View | draft |
| [TODO-08](./TODO-08-nodus-parity-paths.md) | Nodus Parity: Drawing, Paths, Shapes, Shaping, and Transform | draft |
| [TODO-09](./TODO-09-nodus-parity-color.md) | Nodus Parity: Color, Fills, Strokes, Brushes, Transparency, Styles, and Symbols | draft |
| [TODO-10](./TODO-10-nodus-parity-type.md) | Nodus Parity: Type, Tables, and Graphs | draft |
| [TODO-11](./TODO-11-nodus-parity-effects.md) | Nodus Parity: Interactive and Live Effects | draft |
| [TODO-12](./TODO-12-nodus-parity-bitmaps.md) | Nodus Parity: Bitmaps, Tracing, and Raster Effects | draft |
| [TODO-13](./TODO-13-nodus-parity-print.md) | Nodus Parity: Color Management, Print, Prepress, and PDF | draft |
| [TODO-14](./TODO-14-nodus-parity-formats.md) | Nodus Parity: File Formats, Export, and Web | draft |
| [TODO-15](./TODO-15-nodus-ai.md) | Nodus AI: Editable, Suite-Aware, Reproducible | draft |
| [TODO-16](./TODO-16-nodus-parity-workspace.md) | Nodus Parity: Workspace, Customization, Preferences, and Utilities | draft |
| [TODO-17](./TODO-17-nodus-parity-releases.md) | Nodus Parity Releases: 0.2.0 to 1.0.0 | draft |
| [TODO-18](./TODO-18-nodus-legacy-formats.md) | Nodus Legacy Formats and Camera RAW: FreeHand, Publisher, Visio, PowerPoint, Corel Legacy, Metafiles, Legacy Rasters, XCF, and RAW | draft |
| [TODO-19](./TODO-19-nodus-automation.md) | Nodus Automation: the Object Model, Actions, Scripts, and Batch | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- Everything under `src/Nodus/` and `tests/Photon.Nodus.Tests/`
- The Nodus user-facing surfaces, its SVG reader and writer, its exporters, and its release

## Out of scope

- Code a second app needs (01-core), installers and signing (05-release), the user guide's content (06-docs)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
