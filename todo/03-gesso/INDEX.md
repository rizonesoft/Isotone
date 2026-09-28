# 03 Gesso

> **Phases 1, 14, 15, 16 to 27, 41, and 42 to 44**

Gesso, the raster editor, imported under `src/Gesso/`. Its rename runs early beside Stilus's; its foundation (the snapshot port, WPF-UI removal, tiles, and rendering) starts after Stilus ships 1.0.0, followed by editing, file I/O, filters, and `gesso-v0.1.0`. On 2026-09-26 the operator decided Gesso gets every Photoshop feature and those of two other popular raster editors (Affinity Photo and GIMP 3): the catalog in [`../../docs/parity/gesso-parity.md`](../../docs/parity/gesso-parity.md) routes each one to a section, and TODO-08 to TODO-21 run it in twelve parity phases (16 to 27), each ending in a release from `gesso-v0.2.0` to `gesso-v1.0.0`. TODO-07 keeps four legacy deferral owners at their addresses: its filter catalog runs in Phase 21, its workspaces and its accessibility audit in Phase 27, and its RAW import in Phase 41 once Albumen's decoder is shared. Later on 2026-09-27, when the operator worried "features will be left behind", the work deferred to after the first release became sections: TODO-22 (actions, scripts, procedures, extensions, batch, and data sets, Phase 42), TODO-23 (video layers, the timeline, audio, render video, frame animation, and animated formats, Phase 43), and TODO-19 §16 and §17 (on-device models, Phase 44), each phase ending in a Gesso release from `gesso-v1.1.0` to `gesso-v1.3.0`. Ideas that are not sections wait in [`../backlog.md`](../backlog.md) and are promoted only through `add-todo`. **Corrected 2026-09-28:** TODO-07 also holds the three performance sections §18 to §20 (B-026, promoted 2026-09-27), which run in Phase 27 before the accessibility audit.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-gesso-structure.md) | Gesso Layout, Names, the Snapshot Port, and WPF-UI Removal | draft |
| [TODO-02](./TODO-02-gesso-rendering.md) | Gesso Tiles, Viewport, and the Render Pipeline | draft |
| [TODO-03](./TODO-03-gesso-editing.md) | Gesso Documents, Layers, Tools, and History | draft |
| [TODO-04](./TODO-04-gesso-files.md) | Gesso File I/O | draft |
| [TODO-05](./TODO-05-gesso-adjustments.md) | Gesso Filters and Adjustments for 0.1.0 | draft |
| [TODO-06](./TODO-06-gesso-release.md) | Gesso 0.1.0 | draft |
| [TODO-07](./TODO-07-gesso-roadmap.md) | Gesso after 0.1.0: Deferral Owners and Accessibility | draft |
| [TODO-08](./TODO-08-gesso-parity-document.md) | Gesso Parity: Document, Canvas, View, History, and the Image Menu | draft |
| [TODO-09](./TODO-09-gesso-parity-layers.md) | Gesso Parity: Layers, Masks, Blending, Styles, Smart Objects, and Artboards | draft |
| [TODO-10](./TODO-10-gesso-parity-selection.md) | Gesso Parity: Selection, Refine, Channels, and Quick Mask | draft |
| [TODO-11](./TODO-11-gesso-parity-adjustments.md) | Gesso Parity: Adjustment Layers, Adjustments, Image Modes, and Color | draft |
| [TODO-12](./TODO-12-gesso-parity-painting.md) | Gesso Parity: the Brush Engine, Painting Tools, Fills, Gradients, and Patterns | draft |
| [TODO-13](./TODO-13-gesso-parity-retouch.md) | Gesso Parity: Retouching, Content-Aware Tools, Transform, Warp, and Liquify | draft |
| [TODO-14](./TODO-14-gesso-parity-filters.md) | Gesso Parity: Smart Filters, the Filter Menu, the Filter Gallery, and Interactive Filter Surfaces | draft |
| [TODO-15](./TODO-15-gesso-parity-photo.md) | Gesso Parity: the Camera Raw Filter, Develop Studio, Tone Mapping, and Photo Merges | draft |
| [TODO-16](./TODO-16-gesso-parity-type-vector.md) | Gesso Parity: Type, Paths, Shapes, and Vector Layers | draft |
| [TODO-17](./TODO-17-gesso-parity-formats.md) | Gesso Parity: the File Menu and Every Format | draft |
| [TODO-18](./TODO-18-gesso-parity-output.md) | Gesso Parity: Export, Web Output, Color Management, and Print | draft |
| [TODO-19](./TODO-19-gesso-ai.md) | Gesso AI: Editable, Suite-Aware, Reproducible | draft |
| [TODO-20](./TODO-20-gesso-parity-workspace.md) | Gesso Parity: Workspace, Customization, Preferences, and Help | draft |
| [TODO-21](./TODO-21-gesso-parity-releases.md) | Gesso Parity Releases: 0.2.0 to 1.0.0 | draft |
| [TODO-22](./TODO-22-gesso-automation.md) | Gesso Automation: Actions, Scripts, Procedures, Extensions, Batch, and Data-Driven Graphics | draft |
| [TODO-23](./TODO-23-gesso-video-animation.md) | Gesso Video, Timeline, Audio, and Frame Animation | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- Everything under `src/Gesso/` and `tests/Isotone.Gesso.*`
- Gesso's surfaces, tiles, rendering, codecs, filters, and releases
- Parity with Photoshop 27.10, Affinity Photo (Affinity 3.3), and GIMP 3.2.6 as the catalog in `docs/parity/gesso-parity.md` routes it

## Out of scope

- Code a second app needs (01-core), installers and signing (05-release), the user guide's content (06-docs)
- Cloud and collaboration (excluded); Affinity document import (backlog B-045) and Content Credentials (backlog B-047)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
