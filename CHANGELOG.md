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
- The Windows installers show a notice on Windows 10: the apps target Windows 11, and Windows 10 22H2 may work but is unsupported by .NET 11. Silent installs skip the notice.
- Plan: Nodus parity with Adobe Illustrator 30.8 and CorelDRAW Graphics Suite 2026 (v27.2), by operator decision. The parity catalog under `docs/parity/` merges every row of both feature inventories (4,335 in all) into 2,802 Nodus features, each with one status, and 180 new TODO sections own the planned ones: ten new phases (4 to 13) ending in `nodus-v0.2.0` to `nodus-v1.0.0`, shared pixel-engine, color-management, and AI-core files in `Photon.Core`, and a planned validator that keeps the catalog and the plan in step. Nodus AI is planned on OpenRouter with the user's own key and three pillars: editable structured output, suite-aware brand kits and hand-offs, and reproducible provenance.

#### Changed

- Toolchain: .NET 11 (SDK 11.0.100-rc.1.26425.128 pinned until .NET 11 ships in November 2026), C# `latest` in every project, Windows SDK target 10.0.26100 with Windows 10 1809 as the minimum platform. `Imago.Plugins.Abstractions` moved from `netstandard2.1` to `net11.0`.
- Packages: SkiaSharp and SkiaSharp.Views.WPF 4.152.1 (Nodus text drawing moved to `SKFont`, paths to `SKPathBuilder`; no .NET Framework OpenTK packages remain), Microsoft.Extensions.* 11.0.0-rc.1.
- Tests: xUnit v3 (4.0.1, on VSTest) and AwesomeAssertions 9.6.0 in place of xUnit 2.9.3 and FluentAssertions 8.
- Installers: Inno Setup 7.1 builds 64-bit Setup programs with a wizard that follows the system light or dark theme. The suite installer (one component per app) is built by `photon-v*` tags and `scripts/package.ps1 -Suite`.
- Supported OS: Windows 11 (23H2 or later); Windows 10 22H2 is best-effort.
- CI: the plan gates run on `ubuntu-26.04`; release builds install a hash-pinned Inno Setup 7.
- Plan: the budget's total ceiling rose from 154 to 354 sections on the operator's approval ("New parity phases, up to +200"); the Imago, Lumen, and distribution phases were renumbered 14 to 20, the old Phase 9 (Nodus after 0.1.0) moved its eight sections into the parity phases, twelve backlog entries were promoted into parity sections, and four were added for obsolete formats, camera RAW import, and 3D in PDF.

#### Removed

- Unused packages: ReactiveUI.WPF, SharpDX.DirectInput, SixLabors.ImageSharp and ImageSharp.Drawing (Imago); Newtonsoft.Json, AvalonEdit, and Svg.Skia (Nodus), with the unused AvalonEdit highlighting file and the unreferenced `SvgVisualEditor` service.

- Per-app README, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, LICENSE, and issue templates under `src/Nodus/` and `src/Imago/`; their content is merged into the root files.

[Unreleased]: https://github.com/rizonesoft/Photon/commits/main
