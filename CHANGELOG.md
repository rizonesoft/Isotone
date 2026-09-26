# Changelog

All notable changes to the Photon Graphics Suite are recorded here.

The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and each app follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Apps are versioned and released independently, so entries are grouped by app. Release headings name the tag they came from, for example `nodus-v0.1.0`.

Sections: [Nodus](#nodus) · [Imago](#imago) · [Lumen](#lumen) · [Photon.Core](#photoncore) · [Suite and infrastructure](#suite-and-infrastructure)

## [Unreleased]

### Nodus

#### Added

- Nodus joins the suite: the Bezier vector editor was imported into `src/Nodus/` with its full Git history on 2026-09-26.
- SVG documents: open, edit, and save through the SVG parser and exporter.
- Drawing tools: pen (Bezier curves), line, rectangle, ellipse, and text.
- Editing tools: select, node edit, pan, and zoom.
- Layers panel, grouping and ungrouping, alignment, and snapping.
- Command-based undo and redo for add, delete, move, resize, rotate, scale, reorder, group, and property changes.
- Raw SVG view for inspecting and editing markup.
- Artboard name indicator in the status bar.
- Splash, debug, and exception windows.
- Grey theme resources for dark and light modes.

#### Changed

- Replaced the WPF-UI dependency with standard WPF controls.
- Converted all app colors to neutral greys.
- Relicensed from MIT to GPL-3.0 as part of the suite.

### Imago

#### Added

- Imago joins the suite: imported into `src/Imago/` with its full Git history on 2026-09-26.
- Domain model: documents, layers with blend modes and bit depths, masks, selections, tiles, and history snapshots.
- Color management types: profiles, conversions, and soft-proofing groundwork.
- Application shell: WPF main window with menus, toolbar, and docking panels.
- MVVM infrastructure with CommunityToolkit.Mvvm: dialog, file, and messenger services.
- Serilog logging, performance logging helpers, and single-instance handling.
- Splash screen.
- Plugin and scripting abstractions (interfaces only; no runtime yet).

#### Changed

- Relicensed from MIT to GPL-3.0 as part of the suite.

### Lumen

- Nothing yet. Lumen is planned; its projects will live in `src/Lumen/`.

### Photon.Core

- Nothing yet. The shared core library is planned; shared code will move into it from Nodus and Imago.

### Suite and infrastructure

#### Added

- Monorepo for the Photon Graphics Suite, with the plan, standards, prompts, and brand resources.
- GPL-3.0 `LICENSE` for the whole repository.
- Repository face: README, contributing guide, security policy, code of conduct, issue forms, pull request template, and documentation indexes.
- Brand assets under `resources/brand/`: Rizonesoft logos for light and dark themes, the Photon banner, and a social preview image.

#### Removed

- Per-app README, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, LICENSE, and issue templates under `src/Nodus/` and `src/Imago/`; their content is merged into the root files.

[Unreleased]: https://github.com/rizonesoft/Photon/commits/main
