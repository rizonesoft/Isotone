# 04 Albumen

> **Phases 28 to 39 and 42 to 45**

Albumen, the digital darkroom and photo library, planned from nothing with `plan-new-feature` rigor. Its spine, catalog, import, RAW decode, and library views come first; non-destructive develop (on the suite develop engine `D01 T07` that Gesso's parity phases build), export, "Edit in Gesso", and `albumen-v0.1.0` follow; then, by the operator's 2026-09-27 decision ("Now Lumen. I want features from Lightroom, but I've alwyas been loving ACDSee photo manager and IrfanView"), Albumen reaches parity with Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76: the catalog in [`../../docs/parity/albumen-parity.md`](../../docs/parity/albumen-parity.md) routes each of their features to a section, and TODO-04 to TODO-15 run it in ten parity phases (30 to 39) before distribution, each ending in a release from `albumen-v0.2.0` to `albumen-v1.0.0`, on three pillars: a fast default image viewer (TODO-04, `AlbumenViewer.exe`), browsing without importing (TODO-05), and batch tools as core Albumen features (TODO-11). The accessibility and localization audit (TODO-02 §9) runs last in Phase 39, over every parity surface. TODO-03 is a retired address (the old roadmap file, whose sections became parity sections or backlog entries). Originals are safe by default: Albumen never writes an original image unless the user opts in, and then only through the one policy of TODO-11 §1 after a verified backup ("Safe by default, opt-in writes"). Later on 2026-09-27, when the operator worried "features will be left behind", the work deferred to after the first release became sections: TODO-17 (recorded actions, extension points, and the command line, Phase 42), TODO-16 (video and audio, Phase 43), TODO-10 §13 (on-device models, Phase 44), and TODO-13 §9 to §12 (CAD and plotter drawings in Phase 30, then SWF, the optional GDAL formats, and clean-room layered formats in Phase 45), with releases from `albumen-v1.1.0` to `albumen-v1.4.0`. Ideas that are not sections (tethered capture B-048, self-running slideshows B-049, the Explorer preview handler B-051, face recognition B-052, SFTP B-053) wait in [`../backlog.md`](../backlog.md) and are promoted only through `add-todo`.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-albumen-foundation.md) | Albumen: App Spine, Library, and RAW Decode | draft |
| [TODO-02](./TODO-02-albumen-develop.md) | Albumen: Non-Destructive Develop, Export, 0.1.0, and Accessibility | draft |
| [TODO-04](./TODO-04-albumen-viewer.md) | Albumen Parity: the Fast Default Viewer | draft |
| [TODO-05](./TODO-05-albumen-browse.md) | Albumen Parity: Browse Without Importing | draft |
| [TODO-06](./TODO-06-albumen-parity-library.md) | Albumen Parity: Library, Collections, Search, and the Catalog | draft |
| [TODO-07](./TODO-07-albumen-parity-import.md) | Albumen Parity: Import, Devices, and Capture | draft |
| [TODO-08](./TODO-08-albumen-parity-metadata.md) | Albumen Parity: Metadata, Keywords, and Places | draft |
| [TODO-09](./TODO-09-albumen-parity-develop.md) | Albumen Parity: Develop | draft |
| [TODO-10](./TODO-10-albumen-ai.md) | Albumen AI: Faces, Keywords, Similarity, Culling, and Masks | draft |
| [TODO-11](./TODO-11-albumen-batch.md) | Albumen Batch Tools: Rename, Convert, Resize, Edit, and Export | draft |
| [TODO-12](./TODO-12-albumen-parity-output.md) | Albumen Parity: Export, Print, Slideshows, Web Galleries, and Books | draft |
| [TODO-13](./TODO-13-albumen-parity-formats.md) | Albumen Parity: Formats | draft |
| [TODO-14](./TODO-14-albumen-parity-workspace.md) | Albumen Parity: Workspace, Preferences, and Help | draft |
| [TODO-15](./TODO-15-albumen-parity-releases.md) | Albumen Parity Releases: 0.2.0 to 1.0.0 | draft |
| [TODO-16](./TODO-16-albumen-video-audio.md) | Albumen Video and Audio: Cataloging, Playback, Trimming, Media Mode, Image Audio, and Video Slideshows | draft |
| [TODO-17](./TODO-17-albumen-automation.md) | Albumen Automation: Recorded Actions, Extensions, and the Command Line | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- Everything under `src/Albumen/` and `tests/Isotone.Albumen.Tests/`
- The catalog, import, RAW decoding, the develop pipeline, export, and the hand-off to Gesso
- The Albumen Viewer (`src/Albumen/Isotone.Albumen.Viewer/`), browsing without importing and the background indexer, the batch tools and the originals policy, and every Albumen parity surface of the catalog

## Out of scope

- Code a second app needs (01-core), installers and signing (05-release), the user guide's content (06-docs)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
