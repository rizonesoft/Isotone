# Changelog

All notable changes to the Isotone Graphics Suite are recorded here.

The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and each app follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Apps are versioned and released independently, so entries are grouped by app. Release headings name the tag they came from, for example `stilus-v0.1.0`.

Sections: [Stilus](#stilus) · [Gesso](#gesso) · [Albumen](#albumen) · [Isotone.Core](#isotonecore) · [Suite and infrastructure](#suite-and-infrastructure)

## [Unreleased]

### Stilus

#### Added

- Stilus joins the suite: the Bezier vector editor was imported into `src/Stilus/` with its full Git history on 2026-09-26.
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

### Gesso

#### Added

- Gesso joins the suite: imported into `src/Gesso/` with its full Git history on 2026-09-26.
- Domain model: documents, layers with blend modes and bit depths, masks, selections, tiles, and history snapshots.
- Color management types: profiles, conversions, and soft-proofing groundwork.
- Application shell: WPF main window with menus, toolbar, and docking panels.
- MVVM infrastructure with CommunityToolkit.Mvvm: dialog, file, and messenger services.
- Serilog logging, performance logging helpers, and single-instance handling.
- Splash screen.
- Plugin and scripting abstractions (interfaces only; no runtime yet).

#### Changed

- Relicensed from MIT to GPL-3.0 as part of the suite.

### Albumen

- Nothing yet. Albumen is planned; its projects will live in `src/Albumen/`, including the fast default viewer `AlbumenViewer.exe` (`src/Albumen/Isotone.Albumen.Viewer/`) that the parity plan adds.

### Isotone.Core

- Nothing yet. The shared core library is planned; shared code will move into it from Stilus and Gesso.

### Suite and infrastructure

#### Changed

- Renamed before any release (2026-09-27): Photon Graphics Suite is now Isotone Graphics Suite, Nodus is Stilus, Imago is Gesso (briefly Pinxit, renamed again on 2026-09-28 because it was hard to say), and Lumen is Albumen, after a trademark pre-screen found live software marks on the old names.

#### Added

- Monorepo for the Isotone Graphics Suite, with the plan, standards, prompts, and brand resources.
- GPL-3.0 `LICENSE` for the whole repository.
- Repository face: README, contributing guide, security policy, code of conduct, issue forms, pull request template, and documentation indexes.
- Brand assets under `resources/brand/`: Rizonesoft logos for light and dark themes. The neon banner, wordmark, and social preview images were removed on 2026-09-27 (operator decision), since they spelled the retired Photon name. The README now shows `resources/brand/isotone-cover.png`, the Isotone Interface cover from the design page.
- `TRADEMARKS.md`: the trademark policy. "Rizonesoft", "Isotone Graphics Suite", "Stilus", "Gesso", "Albumen", and the app icons are trademarks of Rizonetech (Pty) Ltd; the GPL covers the code, not the names and logos, so a modified version someone distributes needs its own name and icons, while nominative use and unmodified official builds are fine.
- The Windows installers show a notice on Windows 10: the apps target Windows 11, and Windows 10 22H2 may work but is unsupported by .NET 11. Silent installs skip the notice.
- Plan: Stilus parity with Adobe Illustrator 30.8 and CorelDRAW Graphics Suite 2026 (v27.2), by operator decision. The parity catalog under `docs/parity/` merges every row of both feature inventories (4,335 in all) into 2,802 Stilus features, each with one status, and 180 new TODO sections own the planned ones: ten new phases (4 to 13) ending in `stilus-v0.2.0` to `stilus-v1.0.0`, shared pixel-engine, color-management, and AI-core files in `Isotone.Core`, and a planned validator that keeps the catalog and the plan in step. Stilus AI is planned on OpenRouter with the user's own key and three pillars: editable structured output, suite-aware brand kits and hand-offs, and reproducible provenance.
- Plan: Gesso parity with Adobe Photoshop 27.10 (with Camera Raw 18.6), Affinity by Canva 3.3 (Affinity Photo), and GIMP 3.2.6, by operator decision. The Gesso parity catalog under `docs/parity/` merges every row of the three feature inventories (10,829 in all) into 2,367 Gesso features, each with one status, and 175 new TODO sections own the planned ones: twelve new phases (16 to 27) ending in `gesso-v0.2.0` to `gesso-v1.0.0`, `Isotone.Core` pixel engine extensions and a develop engine that Albumen reuses, and a planned validator extension that keeps the Gesso catalog and the plan in step. Gesso AI follows Stilus's three pillars on the shared AI core.
- Design system: the Isotone Interface design system is imported in full into `docs/design/` (tokens, 30 component specs with previews, the shell layout, and the app icon guide) and the repository is now its source of truth, by operator decision ("Yes, full import"); `docs/design/SYNC.md` maps it to the Design System artifact, which is republished from the repository after changes.
- `standards/ui.md`: the binding UI standard (four brightness themes, the Highlight color for state and the app accent for identity only, type, density, focus, icons, window anatomy, accessibility, and the WPF mapping), replacing the design contract in `standards/shared.md`.

#### Changed

- Toolchain: .NET 11 (SDK 11.0.100-rc.1.26425.128 pinned until .NET 11 ships in November 2026), C# `latest` in every project, Windows SDK target 10.0.26100 with Windows 10 1809 as the minimum platform. `Gesso.Plugins.Abstractions` moved from `netstandard2.1` to `net11.0`.
- Packages: SkiaSharp and SkiaSharp.Views.WPF 4.152.1 (Stilus text drawing moved to `SKFont`, paths to `SKPathBuilder`; no .NET Framework OpenTK packages remain), Microsoft.Extensions.* 11.0.0-rc.1.
- Tests: xUnit v3 (4.0.1, on VSTest) and AwesomeAssertions 9.6.0 in place of xUnit 2.9.3 and FluentAssertions 8.
- Installers: Inno Setup 7.1 builds 64-bit Setup programs with a wizard that follows the system light or dark theme. The suite installer (one component per app) is built by `isotone-v*` tags and `scripts/package.ps1 -Suite`.
- Supported OS: Windows 11 (23H2 or later); Windows 10 22H2 is best-effort.
- Ownership: the copyright holder is Rizonetech (Pty) Ltd ("Copyright (C) 2025-2026 Rizonetech (Pty) Ltd"); Rizonesoft is its brand and stays the publisher users see. The assembly metadata (`Company`, `Copyright`), the installers (`AppCopyright`, `VersionInfoCopyright`, `VersionInfoCompany`), the splash cards, the README, and the contributing guide say so; contributors keep the copyright of their contributions under the GPL with the DCO.
- Distribution: installers and portable ZIPs are published only on rizonesoft.com, served from `download.rizonesoft.com` (`<app>/<version>/<file>`, with the update feed at `update/<app>.json`); GitHub releases carry the notes, the source archives, the SHA-256 table, and links to the downloads, never the binaries. The release workflow uploads to S3-compatible storage with rclone and fails a tag release when the storage is not configured.
- CI: the plan gates run on `ubuntu-26.04`; release builds install a hash-pinned Inno Setup 7.
- Plan: the budget's total ceiling rose from 154 to 354 sections on the operator's approval ("New parity phases, up to +200"); the Gesso, Albumen, and distribution phases were renumbered 14 to 20, the old Phase 9 (Stilus after 0.1.0) moved its eight sections into the parity phases, twelve backlog entries were promoted into parity sections, and four were added for obsolete formats, camera RAW import, and 3D in PDF.
- Plan: the budget's total ceiling rose from 354 to 555 sections on the operator's approval ("New Imago parity phases, up to +250"); twelve Gesso parity phases (16 to 27) run after Gesso 0.1.0, Albumen, distribution, and the later phases were renumbered 28 to 32, three Gesso roadmap sections moved into the parity phases, eleven backlog entries were promoted into Gesso parity sections, Gesso scripting merged into a suite-wide scripting and macro entry, and seven entries were added for work deferred to after the first release (scripting and macros, batch processing, video, animation) and for Affinity files, on-device models, and Content Credentials. The Stilus catalog's scripting and batch rows moved from excluded to those deferred entries.
- Plan: Albumen parity with Adobe Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76, by operator decision ("Now Lumen. I want features from Lightroom, but I've alwyas been loving ACDSee photo manager and IrfanView"). The Albumen parity catalog under `docs/parity/` merges every row of the three feature inventories (8,919 in all) into 1,622 Albumen features, each with one status (ACDSee's layered Edit mode routes to named Gesso rows), and 144 new TODO sections own the planned ones: 140 in twelve new Albumen files running in ten new phases (30 to 39) between Albumen 0.1.0 and distribution, ending in Albumen releases 0.2.0 to 1.0.0, on three pillars (a fast default viewer as a second executable, `AlbumenViewer.exe`; browsing without importing; batch tools as core Albumen features), plus a validator extension for the third catalog (`D00 T01 §8`) and three new develop-engine stages (`D01 T07 §7` to `D01 T07 §9`). Originals are safe by default with opt-in writes (operator: "Safe by default, opt-in writes"): one policy (`D04 T11 §1`) owns the four in-place opt-ins, each off by default and taken only after a verified backup, and `standards/albumen.md` and the frozen-behavior rules say so.
- Plan: distribution moved from Phase 30 to 40 and the Gesso and Stilus shared-decoder imports from 31 to 41; the old Phase 32 (Albumen accessibility) left the plan as its row moved into Phase 39, and the opt-in update check moved into Phase 39, where Albumen's Help menu first consumes it. Eight Albumen backlog entries (B-028 to B-032 and B-034 to B-036) were promoted into Albumen parity sections, B-033, B-042, B-043 (now suite-wide video and audio), and B-046 were reworded, and B-048 (tethered capture), B-049 (self-running slideshows), B-050 (formats with no GPL-compatible reader), and B-051 (the Explorer preview handler) were added. Albumen's former B-012 plug-in rows moved onto the suite plug-in host (`D01 T09`), and FlashPix and Corel PHOTO-PAINT CPT onto the shared legacy codecs (`D01 T08`). Gesso builds the guided filter and the PatchMatch completion solver in `Isotone.Core`, since the suite develop engine is their second consumer.
- Plan: operator-directed planning is no longer capped, on the operator's decision ("Why is there a phase limit on planning, should the limit not only be on new sections beign created automatically, but even then that shoiuld not be a small limit"). The phase ceilings and the total ceiling are gone from `todo/budget.json` (schema 2); only sections a campaign files on its own are capped, each marked with an `**Origin:** discovered run=<run id> <date>` line, at most 15 per phase run with the overflow merged into open sections or sent to the backlog. The backlog cap rose from 150 to 500. `validate` refuses a malformed Origin line and more than 15 discovered sections under one run id, and the plan's Progress line reports sections, discovered sections, and backlog use instead of a ceiling.
- Plan: nothing in the plan is capped any more, on the operator's decision ("the cap is worrying me, because I'm worried features will be left behind."): the 15-per-run cap on discovered sections and the 500-entry backlog cap are gone (`todo/budget.json` schema 3, both `null`), and Origin lines stay as provenance. In their place, a backlog entry leaves `todo/backlog.md` only by promotion, by a merge that keeps its key as ``merged: `<key>` ``, or with the operator's words in a removal record (`validate`: `backlog-dropped`), and every release section carries a backlog review item and stamps only when each backlog entry for its app was promoted or carries the operator's recorded deferral (`release-backlog-review-missing`, `release-backlog-unreviewed`).
- Plan: the suite theme section (`D01 T01 §3`) now generates the Darkest, Dark, Medium Gray, and Light theme dictionaries, the Highlight and density dictionaries, and a high-contrast mapping from `docs/design/tokens.json` with a drift check, and switches theme, Highlight color (Blue, Isotone orange, or the Windows accent), and density live; the chrome sections cite the component specs in `docs/design/components/`, and selection and focus use the Highlight tokens instead of the app accents.

#### Removed

- Unused packages: ReactiveUI.WPF, SharpDX.DirectInput, SixLabors.ImageSharp and ImageSharp.Drawing (Gesso); Newtonsoft.Json, AvalonEdit, and Svg.Skia (Stilus), with the unused AvalonEdit highlighting file and the unreferenced `SvgVisualEditor` service.

- Per-app README, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, LICENSE, and issue templates under `src/Stilus/` and `src/Gesso/`; their content is merged into the root files.

[Unreleased]: https://github.com/rizonesoft/Isotone/commits/main
