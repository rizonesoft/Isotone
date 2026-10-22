# Supersession map, 2026-10

> **Goal:** every section that existed when the operator approved the native stack spec (2026-10-23) is listed once, with its treatment in the native re-plan: kept, rewritten in place, superseded (with the successor that takes over its acceptance requirements), or pending until its wave. The rules and the waves are in `docs/plans/2026-10-23-native-replan.md`.

Generated from `python scripts/todo-graph.py query plan` on 2026-10-23 and edited by hand as each wave lands. Stamped sections stay exactly as they shipped. A pending row names the wave that will settle it; its file is parked (`status: blocked`) until then.

| Section | Phase | Title | Treatment | Successor or note |
| ------- | ----- | ----- | --------- | ----------------- |
| D00 T01 §1 | 0 | Wire the TODO gate into every clone | kept | stamped; stays as shipped |
| D00 T01 §2 | 0 | The operator requirement for manual rows | kept | stamped; stays as shipped |
| D00 T01 §11 | 0 | The manual-row invariant | kept | stamped; stays as shipped |
| D00 T01 §3 | 0 | Raise the claims coverage floor | kept | stamped; stays as shipped |
| D00 T01 §4 | 0 | Prove the review panel end to end | kept | stamped; stays as shipped |
| D00 T01 §6 | 0 | The parity catalog validator | kept | stamped; stays as shipped |
| D00 T01 §12 | 0 | Merge dependency PRs at section boundaries | kept | stamped; stays as shipped |
| D00 T01 §15 | 0 | Unattended merges read main's CI back | kept | stamped; stays as shipped |
| D00 T01 §13 | 0 | Run-guard robustness | kept | stamped; stays as shipped |
| D00 T01 §14 | 0 | Retire the unused verify-agent-tiers.mjs | kept | stamped; stays as shipped |
| D00 T01 §16 | 0 | Unattended merger health | kept | stamped; stays as shipped |
| D00 T01 §17 | 0 | Time the guard's deadline cases on the walk | kept | stamped; stays as shipped |
| D00 T01 §7 | 0 | The validator reads the Gesso parity catalog | pending (W1) |  |
| D00 T01 §8 | 0 | The validator reads the Albumen parity catalog | pending (W1) |  |
| D00 T02 §1 | 0 | Fix the quarantined tests and empty the quarantine | pending (W1) |  |
| D00 T02 §9 | 0 | Point every Stilus test at a temporary app data | pending (W1) |  |
| D00 T02 §2 | 0 | Gesso diagnostics to zero | kept | stamped; stays as shipped |
| D00 T02 §3 | 0 | Quiet the WPF temporary project output | pending (W1) |  |
| D00 T02 §4 | 0 | Prune packages no code uses | kept | stamped; stays as shipped |
| D00 T02 §5 | 0 | The assertion library decision and the decision log | pending (W1) |  |
| D00 T04 §1 | 0 | The native-code standard, the register, and the native-lint gate | rewritten in place | now "The C++ standard, the dependency register, and the register gate"; the register columns, advisory requirement, and OS-calling rules carry over (spec); the inventory of the C# apps' shipped native files is superseded because no C# app ships again, its notice and per-architecture requirements carried by the register's Notices shipped and Architectures columns |
| D00 T04 §2 | 0 | The benchmark harness and the first benchmark record | rewritten in place | Google Benchmark replaces BenchmarkDotNet; the reference machine record joins it; new D00 T04 §3 carries the advisory job |
| D00 T03 §1 | 0 | Fold the per-app docs and samples into the suite | pending (W1) |  |
| D00 T03 §2 | 0 | Before captures of the imported Stilus and Gesso | pending (W1) |  |
| D00 T01 §9 | 0 | The design contract gates | pending (W1) |  |
| D00 T01 §10 | 0 | The drift gates | pending (W1) |  |
| D00 T01 §5 | 0 | First push: CI green and read back | pending (W1) |  |
| D00 T02 §7 | 0 | Release pipeline dry run as a draft release | pending (W1) |  |
| D00 T03 §3 | 1 | Export the app icon rasters from the SVG sources | pending (W3) |  |
| D02 T01 §1 | 1 | Rename Bezier to Isotone.Stilus | pending (W3) |  |
| D03 T01 §1 | 1 | Restructure and rename Gesso to Isotone.Gesso | pending (W3) |  |
| D03 T01 §4 | 1 | The Gesso icon | pending (W3) |  |
| D01 T13 §1 | 2 | The layout-map format and the binding rule | pending (W3) |  |
| D01 T13 §2 | 2 | The layout-map checker | pending (W3) |  |
| D01 T13 §7 | 2 | Every layout section cites its map | pending (W3) |  |
| D01 T13 §3 | 2 | The Stilus map from a driven Illustrator run | pending (W3) |  |
| D01 T02 §1 | 2 | Create Isotone.Core with app-data paths and logging | pending (W3) |  |
| D01 T02 §2 | 2 | The settings store | pending (W3) |  |
| D02 T01 §2 | 2 | Composition root on the Generic Host | pending (W3) |  |
| D02 T01 §3 | 2 | The debug console reads the Serilog pipeline | pending (W3) |  |
| D02 T01 §4 | 2 | Culture-safe formatting and comparisons | pending (W3) |  |
| D02 T01 §5 | 2 | The rest of the analyzer backlog | pending (W3) |  |
| D02 T02 §1 | 2 | The triage record and the delete group | pending (W3) |  |
| D02 T02 §2 | 2 | One SVG render path | pending (W3) |  |
| D02 T01 §6 | 2 | SkiaSharp 4 | pending (W3) |  |
| D02 T01 §7 | 2 | Warnings are errors in Stilus | pending (W3) |  |
| D02 T02 §3 | 2 | Selection has one owner | pending (W3) |  |
| D02 T03 §1 | 2 | Undo for resize and rotate | pending (W3) |  |
| D02 T03 §2 | 2 | Split the main window view model | pending (W3) |  |
| D02 T04 §1 | 2 | Atomic save and dirty tracking | pending (W3) |  |
| D02 T04 §2 | 2 | SVG round-trip fidelity fixtures | pending (W3) |  |
| D00 T02 §6 | 2 | xUnit v3 | pending (W3) |  |
| D01 T01 §1 | 3 | Create Isotone.UI with the icon catalog | pending (W3) |  |
| D01 T13 §6 | 3 | The shared layout conformance test helpers | pending (W3) |  |
| D01 T01 §2 | 3 | Splash, exception window, and glow move to Isotone.UI | pending (W3) |  |
| D01 T01 §3 | 3 | The suite theme resources | pending (W3) |  |
| D01 T01 §9 | 3 | The visual regression harness and goldens | pending (W3) |  |
| D01 T01 §5 | 3 | Implicit control styles: buttons and inputs | pending (W3) |  |
| D01 T01 §6 | 3 | Implicit control styles: navigation, data, menus, and feedback | pending (W3) |  |
| D01 T01 §7 | 3 | Shared window chrome: title bar and caption buttons | pending (W3) |  |
| D01 T01 §8 | 3 | Shared window chrome: document tabs, dock theme, and status bar | pending (W3) |  |
| D01 T02 §3 | 3 | Single instance and file-open forwarding | pending (W3) |  |
| D02 T02 §4 | 3 | Arrange, align, distribute, rotate, and flip | pending (W3) |  |
| D02 T02 §5 | 3 | Boolean path operations on SKPath.Op | pending (W3) |  |
| D02 T02 §6 | 3 | The layers panel on LayerManager | pending (W3) |  |
| D02 T02 §7 | 3 | Snapping on SnapManager | pending (W3) |  |
| D02 T02 §8 | 3 | One keymap on ShortcutManager | pending (W3) |  |
| D02 T03 §3 | 3 | Clipboard and the Edit menu | pending (W3) |  |
| D02 T03 §4 | 3 | Property edits are undo steps | pending (W3) |  |
| D02 T04 §3 | 3 | PNG and JPEG export | pending (W3) |  |
| D02 T04 §4 | 3 | PDF export | pending (W3) |  |
| D02 T04 §5 | 3 | Recent files, autosave, and crash recovery | pending (W3) |  |
| D02 T04 §6 | 3 | Open from the command line and the .svg association | pending (W3) |  |
| D02 T03 §5 | 3 | Every menu command works or names its owner | pending (W3) |  |
| D02 T03 §6 | 3 | The main window follows the Illustrator layout map | pending (W3) |  |
| D02 T05 §1 | 3 | The About dialog | pending (W3) |  |
| D02 T05 §2 | 3 | The keyboard shortcuts dialog | pending (W3) |  |
| D02 T05 §3 | 3 | The Help menu | pending (W3) |  |
| D06 T01 §1 | 3 | The Stilus user guide | pending (W8) |  |
| D06 T02 §1 | 3 | The architecture page matches the tree | pending (W8) |  |
| D00 T02 §8 | 3 | Pin the .NET 11 GA SDK | pending (W3) |  |
| D05 T01 §1 | 3 | The clean-machine install procedure | pending (W8) |  |
| D05 T01 §8 | 3 | Third-party notices in every package | pending (W8) |  |
| D02 T05 §4 | 3 | Stilus 0.1.0 | pending (W3) |  |
| D01 T02 §4 | 3 | One undo history for the suite | pending (W3) |  |
| D01 T02 §5 | 3 | The atomic document writer moves to Isotone.Core | pending (W3) |  |
| D02 T06 §7 | 4 | Documents in tabs, saved layouts, nested layers | pending (W4) |  |
| D02 T07 §1 | 4 | The live-object contract in the stilus namespace | pending (W4) |  |
| D02 T07 §2 | 4 | Spatial index, culling, and dirty-region rendering | pending (W4) |  |
| D02 T07 §3 | 4 | Pages and artboards: one model, panel, and commands | pending (W4) |  |
| D02 T07 §4 | 4 | Multipage views, page background, page numbers, navigation | pending (W4) |  |
| D02 T07 §5 | 4 | Layers, master layers, lock and hide, the Objects panel | pending (W4) |  |
| D02 T07 §6 | 4 | Selection: Select menu, Select Same, wand, lasso, saved selections | pending (W4) |  |
| D02 T07 §7 | 4 | Isolation mode and focus mode | pending (W4) |  |
| D02 T07 §8 | 4 | The Properties panel and the contextual property bar | pending (W4) |  |
| D02 T07 §9 | 4 | Rulers, units, drawing scale, and grids | pending (W4) |  |
| D02 T07 §10 | 4 | Guides, the Guides panel, the measure tool, the Info panel | pending (W4) |  |
| D02 T07 §11 | 4 | Snapping modes, smart guides, dynamic and alignment guides | pending (W4) |  |
| D02 T07 §12 | 4 | View modes, zoom, rotate view, saved views, windows | pending (W4) |  |
| D02 T07 §13 | 4 | History panel, repeat, paste variants, quick duplicates | pending (W4) |  |
| D02 T07 §14 | 4 | New Document dialog, presets, templates, document information | pending (W4) |  |
| D02 T17 §1 | 4 | Stilus 0.2.0 (Phase 4) | pending (W4) |  |
| D02 T06 §2 | 5 | Path editing: continue, join, break, reverse, simplify | pending (W4) |  |
| D02 T08 §1 | 5 | Pen, Bezier, and anchor point tools | pending (W4) |  |
| D02 T08 §2 | 5 | Curvature, B-spline, polyline, 3-point, line and arc tools, parallel drawing | pending (W4) |  |
| D02 T08 §3 | 5 | Pencil, freehand, smooth, path eraser, join, and smart drawing | pending (W4) |  |
| D02 T08 §4 | 5 | Live shapes and live corners | pending (W4) |  |
| D02 T08 §5 | 5 | Grid, graph paper, flare, common shapes, and impact tools | pending (W4) |  |
| D02 T08 §6 | 5 | Node editing: types, transforms, align, distribute, reduce | pending (W4) |  |
| D02 T08 §7 | 5 | Join curves, average, offset, anchors, clean up, split into grid | pending (W4) |  |
| D02 T08 §8 | 5 | Knife, scissors, eraser, virtual segment delete, crop | pending (W4) |  |
| D02 T08 §9 | 5 | Liquify and shape-editing brushes | pending (W4) |  |
| D02 T08 §10 | 5 | Pathfinder, shaping, and the shape builder | pending (W4) |  |
| D02 T08 §11 | 5 | Compound paths, clipping masks, draw inside and behind, intertwine | pending (W4) |  |
| D02 T08 §12 | 5 | The Transform panel, dialogs, Transform Again, Transform Each | pending (W4) |  |
| D02 T08 §13 | 5 | Rotate, reflect, scale, shear, reshape, and free transform tools | pending (W4) |  |
| D02 T08 §14 | 5 | Align, distribute, arrange, and step and repeat extensions | pending (W4) |  |
| D02 T08 §15 | 5 | Dimensions, connectors, and callouts | pending (W4) |  |
| D02 T17 §2 | 5 | Stilus 0.3.0 (Phase 5) | pending (W4) |  |
| D02 T06 §11 | 6 | Symbols and the asset library | pending (W4) |  |
| D01 T04 §1 | 6 | The engine decision, the lcms2 wrapper, profiles, the profile store, and RGB, CMYK, gray, and Lab transforms | pending (W4) |  |
| D01 T04 §2 | 6 | Rendering intents, black point compensation, proofing transforms, and gamut checks | pending (W4) |  |
| D02 T09 §1 | 6 | The color model: RGB, CMYK, HSB, Lab, grayscale, spot, global, and tints | pending (W4) |  |
| D02 T09 §2 | 6 | The Color panel, color picker, recent colors, and eyedroppers | pending (W4) |  |
| D02 T09 §3 | 6 | The Swatches panel, document palette, and color groups | pending (W4) |  |
| D02 T09 §4 | 6 | The palette bar, palette editor, color libraries, and palette files | pending (W4) |  |
| D02 T09 §5 | 6 | Color styles, harmonies, and the color guide | pending (W4) |  |
| D02 T09 §6 | 6 | Recolor Artwork, Edit Colors, and find and replace color | pending (W4) |  |
| D02 T09 §7 | 6 | The gradient model: linear, radial, conical, rectangular, stops, repeat, and interpolation | pending (W4) |  |
| D02 T09 §8 | 6 | The gradient tool, interactive fill, stroke gradients, and freeform gradients | pending (W4) |  |
| D02 T09 §9 | 6 | Gradient mesh and mesh fill | pending (W4) |  |
| D02 T09 §10 | 6 | Pattern fills and pattern editing | pending (W4) |  |
| D02 T09 §11 | 6 | Texture and procedural fills, and the fill library | pending (W4) |  |
| D02 T09 §12 | 6 | The Stroke panel: caps, joins, alignment, dashes, arrowheads, and line styles | pending (W4) |  |
| D02 T09 §13 | 6 | The width tool and variable outlines | pending (W4) |  |
| D02 T09 §14 | 6 | The Appearance panel: stacked fills, strokes, and effects | pending (W4) |  |
| D02 T09 §15 | 6 | Graphic styles, object styles, style sets, and default properties | pending (W4) |  |
| D02 T09 §16 | 6 | The brush engine, art brushes, and pattern brushes | pending (W4) |  |
| D02 T09 §17 | 6 | Scatter, sprayer, and calligraphic brushes, the paintbrush, and the blob brush | pending (W4) |  |
| D02 T09 §18 | 6 | Bristle and painterly brushes, and brush libraries | pending (W4) |  |
| D02 T09 §19 | 6 | Opacity and blend modes | pending (W4) |  |
| D02 T09 §20 | 6 | Opacity masks, fountain and pattern transparency, knockout, and feather | pending (W4) |  |
| D02 T09 §21 | 6 | Symbols: dynamic symbols, 9-slice scaling, registration, nesting, and linked libraries | pending (W4) |  |
| D02 T09 §22 | 6 | Symbolism tools and the symbol sprayer | pending (W4) |  |
| D02 T17 §3 | 6 | Stilus 0.4.0 (Phase 6) | pending (W4) |  |
| D02 T06 §3 | 7 | Text: area text, text on path, text to path | pending (W4) |  |
| D02 T10 §1 | 7 | The text shaping engine: HarfBuzzSharp, bidi, script runs, and font fallback | pending (W4) |  |
| D02 T10 §2 | 7 | The rich text model and text objects: point, area, path, and vertical | pending (W4) |  |
| D02 T10 §3 | 7 | Fonts: the font list, filters, live preview, and the Font Sampler | pending (W4) |  |
| D02 T10 §16 | 7 | Missing fonts: substitution, Find Font, and font embedding | pending (W4) |  |
| D02 T10 §4 | 7 | Character formatting | pending (W4) |  |
| D02 T10 §5 | 7 | OpenType features, glyphs, variable fonts, and glyph snapping | pending (W4) |  |
| D02 T10 §6 | 7 | Paragraph formatting, composers, justification, and hyphenation | pending (W4) |  |
| D02 T10 §7 | 7 | Tabs, drop caps, and bullets and numbering | pending (W4) |  |
| D02 T10 §8 | 7 | Area text frames, columns, threading, and text wrap | pending (W4) |  |
| D02 T10 §9 | 7 | Type on a path options and effects | pending (W4) |  |
| D02 T10 §10 | 7 | Vertical, CJK, and right-to-left type | pending (W4) |  |
| D02 T10 §11 | 7 | Text commands: find and replace, change case, special characters, and placeholder text | pending (W4) |  |
| D02 T10 §12 | 7 | Character, paragraph, and frame styles | pending (W4) |  |
| D02 T10 §13 | 7 | Writing tools, and text import and export | pending (W4) |  |
| D02 T10 §14 | 7 | Tables | pending (W4) |  |
| D02 T10 §15 | 7 | Graphs | pending (W4) |  |
| D02 T17 §4 | 7 | Stilus 0.5.0 (Phase 7) | pending (W4) |  |
| D02 T11 §1 | 8 | The live-effect framework: effect stack, parameters, copy, clone, clear, and expand | pending (W4) |  |
| D02 T11 §2 | 8 | Blend: tool, steps, spacing, easing, and color acceleration | pending (W4) |  |
| D02 T11 §3 | 8 | Blend on a path, node mapping, split, fuse, compound blends, and presets | pending (W4) |  |
| D02 T11 §4 | 8 | Contour | pending (W4) |  |
| D02 T11 §5 | 8 | Envelope distort and warp | pending (W4) |  |
| D02 T11 §6 | 8 | The distort tool and Distort & Transform effects | pending (W4) |  |
| D02 T11 §7 | 8 | Drop, inner, perspective, and block shadows | pending (W4) |  |
| D02 T11 §8 | 8 | Glows, feather, scribble, round corners, and bevels | pending (W4) |  |
| D02 T11 §9 | 8 | 3D extrude and revolve: geometry, lighting, bevels, and vanishing points | pending (W4) |  |
| D02 T11 §10 | 8 | 3D and Materials: inflate, plane, materials, mapped art, ray-traced rendering, and 3D export | pending (W4) |  |
| D02 T11 §11 | 8 | Lenses | pending (W4) |  |
| D02 T11 §12 | 8 | PowerClip frames | pending (W4) |  |
| D02 T11 §13 | 8 | Symmetry drawing mode | pending (W4) |  |
| D02 T11 §14 | 8 | The perspective grid and drawing planes | pending (W4) |  |
| D02 T11 §15 | 8 | Perspective objects and the Add Perspective effect | pending (W4) |  |
| D02 T11 §16 | 8 | Puppet warp | pending (W4) |  |
| D02 T11 §17 | 8 | Live Paint and smart fill | pending (W4) |  |
| D02 T11 §18 | 8 | Repeats and objects on a path | pending (W4) |  |
| D02 T11 §19 | 8 | Path effects: convert to shape, offset, outline, and pathfinder effects | pending (W4) |  |
| D02 T17 §5 | 8 | Stilus 0.6.0 (Phase 8) | pending (W4) |  |
| D02 T06 §14 | 9 | More formats and the export dialog | pending (W4) |  |
| D01 T03 §1 | 9 | Pixel buffers, the effect contract, and the golden harness | pending (W4) |  |
| D01 T03 §2 | 9 | Resampling, rotation, straighten, perspective, and lens correction | pending (W4) |  |
| D01 T03 §3 | 9 | Palette quantization and dithering | pending (W4) |  |
| D01 T03 §4 | 9 | Tonal adjustments | pending (W4) |  |
| D01 T03 §5 | 9 | Color adjustments | pending (W4) |  |
| D01 T03 §6 | 9 | Blur, sharpen, and noise | pending (W4) |  |
| D01 T03 §7 | 9 | Distort and 3D-style effects | pending (W4) |  |
| D01 T03 §8 | 9 | Artistic and art-stroke effects | pending (W4) |  |
| D01 T03 §9 | 9 | Brush-stroke and sketch effects | pending (W4) |  |
| D01 T03 §10 | 9 | Texture and creative effects | pending (W4) |  |
| D01 T03 §11 | 9 | Camera, color-transform, edge, custom, pixelate, and video effects | pending (W4) |  |
| D02 T12 §1 | 9 | Bitmap objects: crop, resample, rasterize, convert to bitmap, straighten, and perspective | pending (W4) |  |
| D02 T12 §9 | 9 | Bitmap color modes, monochrome coloring, and the bitmap color mask | pending (W4) |  |
| D02 T12 §2 | 9 | The effect stack on objects: FX panel, effect gallery, preview, flatten, and effect lenses | pending (W4) |  |
| D01 T09 §1 | 9 | The plug-in host decision and the isolated host process | pending (W4) |  |
| D01 T09 §2 | 9 | 8BF filter plug-ins: discovery, the filter record, suites, and Repeat parameters | pending (W4) |  |
| D01 T09 §3 | 9 | Format and acquire plug-ins | pending (W4) |  |
| D01 T09 §4 | 9 | The plug-in manager in Isotone.UI | pending (W4) |  |
| D02 T12 §10 | 9 | Third-party plug-in filters in Stilus | pending (W4) |  |
| D02 T12 §3 | 9 | Adjustments in Stilus: the Image Adjustment Lab and adjustment presets | pending (W4) |  |
| D02 T12 §4 | 9 | The tracing engine: outline tracing, color quantization, and stacking | pending (W4) |  |
| D02 T12 §5 | 9 | Centerline tracing, the Image Trace panel, and PowerTRACE | pending (W4) |  |
| D02 T12 §6 | 9 | Photo artwork: Pointillizer, PhotoCocktail, Object Mosaic, and mockups | pending (W4) |  |
| D02 T12 §7 | 9 | The Links panel and linked sources | pending (W4) |  |
| D02 T12 §8 | 9 | SVG filter effects | pending (W4) |  |
| D02 T17 §6 | 9 | Stilus 0.7.0 (Phase 9) | pending (W4) |  |
| D01 T04 §3 | 10 | Bitmap color modes, duotone, and multichannel, with the Stilus Duotone dialog | pending (W4) |  |
| D02 T13 §1 | 10 | Document color settings: profiles, policies, assign, convert, and embed | pending (W4) |  |
| D02 T13 §2 | 10 | The print dialog: printers, range, copies, placement, scaling, and preview | pending (W4) |  |
| D02 T13 §3 | 10 | Print tiling, print styles, print to file, and print summaries | pending (W4) |  |
| D02 T13 §4 | 10 | Printer's marks and bleed | pending (W4) |  |
| D02 T13 §5 | 10 | Separations, halftone screens, and the ink manager | pending (W4) |  |
| D02 T13 §6 | 10 | Soft proofing, gamut warning, overprint preview, and separations preview | pending (W4) |  |
| D02 T13 §7 | 10 | Overprint attributes and trapping | pending (W4) |  |
| D02 T13 §8 | 10 | Transparency flattening and the flattener preview | pending (W4) |  |
| D02 T13 §9 | 10 | Preflight, Package, and Collect for Output | pending (W4) |  |
| D02 T13 §10 | 10 | PostScript output and driver compatibility options | pending (W4) |  |
| D02 T13 §11 | 10 | Imposition, binding, and page placement | pending (W4) |  |
| D02 T13 §12 | 10 | Layout styles, labels, and banners | pending (W4) |  |
| D02 T13 §13 | 10 | Print merge and variable data | pending (W4) |  |
| D02 T13 §14 | 10 | The PDF writer: spot colors, layers, and exact vector output | pending (W4) |  |
| D02 T13 §15 | 10 | PDF presets and standards: PDF/X, PDF/A, compatibility, compression, and marks | pending (W4) |  |
| D02 T13 §17 | 10 | Interactive 3D models in PDF: U3D annotations | pending (W4) |  |
| D02 T13 §16 | 10 | PDF interactivity and security: bookmarks, hyperlinks, tagged PDF, and passwords | pending (W4) |  |
| D02 T17 §7 | 10 | Stilus 0.8.0 (Phase 10) | pending (W4) |  |
| D02 T14 §1 | 11 | SVG options: SVGZ, styling modes, CSS export, and SVG code | pending (W4) |  |
| D02 T14 §2 | 11 | PDF import | pending (W4) |  |
| D02 T14 §3 | 11 | Illustrator import: PDF-compatible .ai files | pending (W4) |  |
| D02 T14 §4 | 11 | Illustrator import: private data and legacy PostScript .ai | pending (W4) |  |
| D02 T14 §5 | 11 | Illustrator .ai export | pending (W4) |  |
| D02 T14 §6 | 11 | CorelDRAW import: containers, pages, layers, and objects | pending (W4) |  |
| D02 T14 §7 | 11 | CorelDRAW import: fills, outlines, text, effects, and bitmaps; CMX | pending (W4) |  |
| D02 T14 §8 | 11 | CorelDRAW CDR and CMX export | pending (W4) |  |
| D02 T14 §9 | 11 | EPS and PostScript import and export | pending (W4) |  |
| D02 T14 §10 | 11 | DXF and DWG import and export | pending (W4) |  |
| D02 T14 §11 | 11 | EMF, WMF, CGM, HPGL, and WPG | pending (W4) |  |
| D02 T14 §12 | 11 | Raster formats: import and export through WIC | pending (W4) |  |
| D02 T14 §13 | 11 | Photoshop PSD import and export | pending (W4) |  |
| D02 T14 §14 | 11 | Office and text documents, Export For Office, and font export | pending (W4) |  |
| D02 T14 §15 | 11 | Export for Screens, asset export, and the export list | pending (W4) |  |
| D02 T14 §16 | 11 | Export for Web: optimized preview and web formats | pending (W4) |  |
| D02 T14 §17 | 11 | Slices, image maps, hyperlinks, rollovers, and SVG interactivity | pending (W4) |  |
| D02 T14 §18 | 11 | Pixel-perfect drawing, pixel preview, and object hinting | pending (W4) |  |
| D02 T14 §19 | 11 | Clipboard formats, OLE objects, placing multiple files, and scanner acquire | pending (W4) |  |
| D02 T17 §8 | 11 | Stilus 0.9.0 (Phase 11) | pending (W4) |  |
| D01 T05 §1 | 12 | The OpenRouter client: chat, structured output, images, streaming, and models | pending (W4) |  |
| D01 T05 §2 | 12 | API keys with DPAPI and the AI settings contract | pending (W4) |  |
| D01 T05 §3 | 12 | The AI provenance record | pending (W4) |  |
| D01 T05 §4 | 12 | The explicit-send gate and the shared AI surfaces in Isotone.UI | pending (W4) |  |
| D01 T05 §5 | 12 | The suite brand kit: shared palettes and styles | pending (W4) |  |
| D02 T15 §1 | 12 | AI in Stilus: the AI menu, settings, usage, and the provenance panel | pending (W4) |  |
| D02 T15 §2 | 12 | Generate vector artwork from a prompt | pending (W4) |  |
| D02 T15 §3 | 12 | Generate patterns and fill shapes | pending (W4) |  |
| D02 T15 §4 | 12 | Generative expand and print bleed | pending (W4) |  |
| D02 T15 §5 | 12 | AI recolor and palettes from the brand kit | pending (W4) |  |
| D02 T15 §6 | 12 | The AI assistant: prompt to edit with undoable commands | pending (W4) |  |
| D02 T15 §7 | 12 | AI text: rewrite, translate, proofread, fit, and retype | pending (W4) |  |
| D02 T15 §8 | 12 | AI images: generate, remix, and reference images | pending (W4) |  |
| D02 T15 §9 | 12 | AI image cleanup: remove background, upscale, repair, and art style | pending (W4) |  |
| D02 T15 §10 | 12 | Concept to vector: sketches and images to structured vectors | pending (W4) |  |
| D02 T15 §11 | 12 | The suite pipeline: Albumen to Gesso to Stilus hand-offs and shared brand kits | pending (W4) |  |
| D02 T17 §9 | 12 | Stilus 0.10.0 (Phase 12) | pending (W4) |  |
| D02 T06 §12 | 13 | The command palette and the on-canvas HUD | pending (W4) |  |
| D02 T06 §13 | 13 | Preferences and shortcut remapping | pending (W4) |  |
| D02 T16 §1 | 13 | Workspaces: presets, save, reset, import, and export | pending (W4) |  |
| D02 T16 §2 | 13 | Toolbox, toolbars, property bar, and status bar customization | pending (W4) |  |
| D02 T16 §3 | 13 | Menus, context menus, command search, and shortcut sets | pending (W4) |  |
| D02 T16 §4 | 13 | Preferences: general, selection and nodes, display, and units | pending (W4) |  |
| D02 T16 §5 | 13 | Preferences: files, backup, performance, GPU, and warnings | pending (W4) |  |
| D02 T16 §6 | 13 | UI appearance, scaling, and diagnostics | pending (W4) |  |
| D02 T16 §7 | 13 | The welcome screen and the navigator | pending (W4) |  |
| D02 T16 §8 | 13 | Pen, touch, and Surface Dial input | pending (W4) |  |
| D02 T16 §9 | 13 | Hints, in-app learning, and the project timer | pending (W4) |  |
| D02 T16 §10 | 13 | Object data, the Object Data Manager, and find and replace objects | pending (W4) |  |
| D02 T16 §11 | 13 | QR codes and barcodes | pending (W4) |  |
| D01 T08 §1 | 13 | Bitonal and simple legacy codecs: MacPaint, CALS Type 1, GEM IMG, XPM, and Scitex CT | pending (W4) |  |
| D01 T08 §2 | 13 | Kodak Photo CD and FlashPix readers | pending (W4) |  |
| D01 T08 §3 | 13 | Windows icons, cursors, and executable icon resources | pending (W4) |  |
| D01 T08 §4 | 13 | Macintosh PICT: a drawing-operation reader, a writer, and a rasterizer | pending (W4) |  |
| D01 T08 §5 | 13 | Corel and Painter proprietary rasters: CPT, RIF, and WI | pending (W4) |  |
| D02 T18 §1 | 13 | FreeHand import, FXG save, and SWF export | pending (W4) |  |
| D02 T18 §2 | 13 | Microsoft Publisher and Visio import | pending (W4) |  |
| D02 T18 §3 | 13 | PowerPoint PPT import | pending (W4) |  |
| D02 T18 §4 | 13 | Corel and Micrografx legacy: DESIGNER, Micrografx Designer, ArtShow, Presentations, R.A.V.E., and Picture Publisher | pending (W4) |  |
| D02 T18 §5 | 13 | Macintosh PICT and OS/2 MET import and export | pending (W4) |  |
| D02 T18 §6 | 13 | GEM, Frame Vector Metafile, Lotus PIC, and NAPLPS | pending (W4) |  |
| D02 T18 §7 | 13 | WordPerfect, Quattro Pro, Lotus 1-2-3, and WordStar | pending (W4) |  |
| D02 T18 §8 | 13 | Legacy raster import and export in Stilus | pending (W4) |  |
| D02 T06 §17 | 13 | Accessibility and localization | pending (W4) |  |
| D02 T17 §10 | 13 | Stilus 1.0.0 (Phase 13) | pending (W4) |  |
| D01 T13 §4 | 14 | The Gesso map from a driven Photoshop run | pending (W5) |  |
| D03 T01 §2 | 14 | Port the snapshot canvas, ruler, and container | pending (W5) |  |
| D03 T01 §3 | 14 | WPF-UI out of Gesso | pending (W5) |  |
| D03 T01 §5 | 14 | Composition root on Isotone.Core | pending (W5) |  |
| D03 T02 §1 | 14 | The tiled image store | pending (W5) |  |
| D03 T02 §2 | 14 | The viewport on the tiled document | pending (W5) |  |
| D03 T02 §3 | 14 | The render graph composites layers | pending (W5) |  |
| D03 T02 §4 | 14 | Blend modes with golden tests | pending (W5) |  |
| D03 T02 §5 | 14 | The ComputeSharp compositing path with CPU parity | pending (W5) |  |
| D03 T04 §1 | 14 | The codec decision | pending (W5) |  |
| D01 T01 §4 | 15 | About and shortcuts dialogs move to Isotone.UI | pending (W5) |  |
| D03 T03 §1 | 15 | Documents in tabs with dirty tracking | pending (W5) |  |
| D03 T03 §2 | 15 | Every edit in the suite history | pending (W5) |  |
| D03 T03 §3 | 15 | The layers panel | pending (W5) |  |
| D03 T03 §4 | 15 | The tool system: move, hand, and zoom | pending (W5) |  |
| D03 T03 §5 | 15 | Selection tools | pending (W5) |  |
| D03 T03 §6 | 15 | Brush and eraser | pending (W5) |  |
| D03 T03 §7 | 15 | Transform, crop, image size, and canvas size | pending (W5) |  |
| D03 T03 §8 | 15 | Fill, gradient, eyedropper, and the color panel | pending (W5) |  |
| D03 T04 §2 | 15 | PNG and JPEG open and save | pending (W5) |  |
| D03 T04 §3 | 15 | TIFF open and save | pending (W5) |  |
| D03 T04 §4 | 15 | The native layered format | pending (W5) |  |
| D03 T04 §5 | 15 | PSD import | pending (W5) |  |
| D03 T04 §6 | 15 | Autosave and crash recovery | pending (W5) |  |
| D03 T05 §1 | 15 | The filter pipeline | pending (W5) |  |
| D03 T05 §2 | 15 | Core adjustments | pending (W5) |  |
| D03 T05 §3 | 15 | Blur and sharpen | pending (W5) |  |
| D03 T06 §1 | 15 | About, shortcuts, and help in Gesso | pending (W5) |  |
| D03 T06 §2 | 15 | Every Gesso menu command works or names its owner | pending (W5) |  |
| D03 T06 §4 | 15 | Gesso's window follows the Photoshop layout map | pending (W5) |  |
| D06 T01 §2 | 15 | The Gesso user guide | pending (W8) |  |
| D03 T06 §3 | 15 | Gesso 0.1.0 | pending (W5) |  |
| D03 T08 §1 | 16 | The document model and the native-format contract for live content | pending (W5) |  |
| D03 T08 §12 | 16 | Image properties, document setup, pixel aspect, and duplicate | pending (W5) |  |
| D03 T08 §2 | 16 | New document, presets, and templates | pending (W5) |  |
| D03 T08 §3 | 16 | Zoom, rotate view, flip view, and screen modes | pending (W5) |  |
| D03 T08 §13 | 16 | Navigation gestures, print size, window behaviors, and view preferences | pending (W5) |  |
| D03 T08 §10 | 16 | Windows, arrangement, view modes, display filters, and the navigator | pending (W5) |  |
| D03 T08 §4 | 16 | Rulers, units, and guides | pending (W5) |  |
| D03 T08 §14 | 16 | Grids, axis grids, and snapping on the shared core | pending (W5) |  |
| D03 T08 §5 | 16 | Measure, protractor, count, and notes | pending (W5) |  |
| D03 T08 §11 | 16 | Info, histogram, sample points, and scopes | pending (W5) |  |
| D03 T08 §6 | 16 | History extensions: snapshots, non-linear history, and saved history | pending (W5) |  |
| D03 T08 §7 | 16 | The Image menu: canvas, rotation, trim, reveal, and resampling | pending (W5) |  |
| D03 T08 §8 | 16 | Clipboard and paste variants | pending (W5) |  |
| D03 T08 §9 | 16 | Crop and straighten extensions | pending (W5) |  |
| D03 T09 §1 | 16 | Every layer kind, locks, labels, tags, and panel filtering | pending (W5) |  |
| D03 T09 §2 | 16 | Layers panel selection, linking, visibility, order, and options | pending (W5) |  |
| D03 T09 §14 | 16 | Merge, stamp, rasterize with revert, matting, and boundaries | pending (W5) |  |
| D03 T09 §3 | 16 | Layer masks, mask stacks, and live masks | pending (W5) |  |
| D03 T09 §4 | 16 | Clipping masks, child clipping, and vector masks | pending (W5) |  |
| D03 T09 §5 | 16 | Blending options, Blend If, and blend ranges | pending (W5) |  |
| D03 T09 §6 | 16 | GIMP, Affinity, and Porter-Duff blend modes | pending (W5) |  |
| D03 T21 §1 | 16 | Gesso 0.2.0 (Phase 16) | pending (W5) |  |
| D03 T10 §1 | 17 | The selection model: soft selections, saved selections, and the selection editor | pending (W5) |  |
| D03 T10 §2 | 17 | Marquee and lasso extensions | pending (W5) |  |
| D03 T10 §3 | 17 | Magic wand and select by color | pending (W5) |  |
| D03 T10 §4 | 17 | Color Range and tonal selection | pending (W5) |  |
| D03 T10 §6 | 17 | The local segmentation engine and Focus Area | pending (W5) |  |
| D03 T10 §5 | 17 | Quick selection, selection brush, foreground select, and intelligent scissors | pending (W5) |  |
| D03 T10 §7 | 17 | Select and Mask and refine selection | pending (W5) |  |
| D03 T10 §8 | 17 | Modify and transform selection | pending (W5) |  |
| D03 T10 §9 | 17 | Select menu extensions | pending (W5) |  |
| D03 T10 §10 | 17 | The Channels panel, spot channels, and quick mask options | pending (W5) |  |
| D03 T09 §7 | 17 | Layer styles I: framework, shadows, glows, stroke, satin | pending (W5) |  |
| D03 T09 §8 | 17 | Layer styles II: bevel, overlays, contours, Styles panel, ASL | pending (W5) |  |
| D03 T09 §9 | 17 | Embedded smart objects | pending (W5) |  |
| D03 T09 §10 | 17 | Linked smart objects, link layers, and the Resource Manager | pending (W5) |  |
| D03 T09 §11 | 17 | Layer comps and states | pending (W5) |  |
| D03 T09 §12 | 17 | Align, distribute, and move-tool extensions | pending (W5) |  |
| D03 T09 §13 | 17 | Artboards with constraints | pending (W5) |  |
| D03 T21 §2 | 17 | Gesso 0.3.0 (Phase 17) | pending (W5) |  |
| D03 T11 §1 | 18 | Adjustment layers and the Adjustments and Properties panels | pending (W5) |  |
| D03 T11 §2 | 18 | Tonal adjustment extensions: brightness and contrast, light, levels, and curves | pending (W5) |  |
| D03 T11 §11 | 18 | Auto corrections, exposure, shadows and highlights, Light EQ, and GIMP tone operations | pending (W5) |  |
| D03 T11 §3 | 18 | Color adjustments I: hue, balance, vibrance, black and white, photo filter, selective color | pending (W5) |  |
| D03 T11 §4 | 18 | Color adjustments II: channel mixer, LUTs, gradient map, match and replace color, OCIO | pending (W5) |  |
| D03 T11 §5 | 18 | Color adjustments III: threshold, posterize, invert, desaturate, color to alpha, and the photo effect kind | pending (W5) |  |
| D03 T11 §12 | 18 | GIMP color operations: exchange, rotate, color to gray, mono mixer, dither, extract, clip, and maps | pending (W5) |  |
| D03 T11 §6 | 18 | Color analysis | pending (W5) |  |
| D03 T11 §7 | 18 | Image modes and bit depth | pending (W5) |  |
| D03 T11 §8 | 18 | Channel operations: split, merge, decompose, compose, apply image, calculations | pending (W5) |  |
| D03 T11 §9 | 18 | Color panels, pickers, eyedroppers, and color samplers | pending (W5) |  |
| D03 T11 §10 | 18 | Swatches, palettes, and color libraries | pending (W5) |  |
| D03 T21 §3 | 18 | Gesso 0.4.0 (Phase 18) | pending (W5) |  |
| D03 T12 §1 | 19 | The brush engine I: tips, spacing, smoothing, and wet media | pending (W5) |  |
| D03 T12 §2 | 19 | The brush engine II: dynamics | pending (W5) |  |
| D03 T12 §3 | 19 | Brush presets, libraries, and tool presets | pending (W5) |  |
| D03 T12 §4 | 19 | MyPaint brushes | pending (W5) |  |
| D03 T12 §5 | 19 | Painting tools and history brushes | pending (W5) |  |
| D03 T12 §6 | 19 | Mixer brush, smudge, and color replacement | pending (W5) |  |
| D03 T12 §7 | 19 | Erasers | pending (W5) |  |
| D03 T12 §8 | 19 | Fill and stroke | pending (W5) |  |
| D03 T12 §9 | 19 | Gradients and the gradient editor | pending (W5) |  |
| D03 T12 §10 | 19 | Patterns | pending (W5) |  |
| D03 T12 §11 | 19 | Symmetry painting | pending (W5) |  |
| D03 T21 §4 | 19 | Gesso 0.5.0 (Phase 19) | pending (W5) |  |
| D03 T13 §1 | 20 | Clone stamp and the clone source panel | pending (W5) |  |
| D03 T13 §2 | 20 | Healing, patch, blemish, inpainting, and red eye | pending (W5) |  |
| D03 T13 §3 | 20 | The content-aware engine: fill, scale, and move | pending (W5) |  |
| D03 T13 §4 | 20 | Toning and focus tools | pending (W5) |  |
| D03 T13 §5 | 20 | Free Transform and move-tool transform extensions | pending (W5) |  |
| D03 T13 §11 | 20 | The GIMP transform tools | pending (W5) |  |
| D03 T13 §6 | 20 | Warp and mesh warp | pending (W5) |  |
| D03 T13 §7 | 20 | Puppet warp, cage transform, and pins | pending (W5) |  |
| D03 T13 §8 | 20 | Perspective warp | pending (W5) |  |
| D03 T13 §9 | 20 | Liquify | pending (W5) |  |
| D03 T13 §10 | 20 | Frequency separation and retouching workflows | pending (W5) |  |
| D03 T21 §5 | 20 | Gesso 0.6.0 (Phase 20) | pending (W5) |  |
| D03 T07 §3 | 21 | The rest of the filter catalog | pending (W5) |  |
| D01 T06 §1 | 21 | The extensions contract: float processing, abyss policies, GEGL op ids, and on-canvas controls | pending (W5) |  |
| D01 T06 §2 | 21 | Blur extensions | pending (W5) |  |
| D01 T06 §3 | 21 | Lens blur, bokeh, and the blur-gallery kernels | pending (W5) |  |
| D01 T06 §4 | 21 | Sharpen and deconvolution | pending (W5) |  |
| D01 T06 §5 | 21 | Noise and denoise extensions | pending (W5) |  |
| D01 T06 §6 | 21 | Distort and projection extensions | pending (W5) |  |
| D01 T06 §7 | 21 | Map extensions | pending (W5) |  |
| D01 T06 §14 | 21 | Pixelate and halftone extensions | pending (W5) |  |
| D03 T14 §1 | 21 | Smart filters, live filter layers, and non-destructive layer filters | pending (W5) |  |
| D03 T14 §2 | 21 | The Filter menu, generated dialogs, presets, and Fade | pending (W5) |  |
| D03 T14 §11 | 21 | Photoshop-compatible plug-in filters, formats, and acquire in Gesso | pending (W5) |  |
| D03 T14 §3 | 21 | The Filter Gallery | pending (W5) |  |
| D03 T14 §4 | 21 | The Blur Gallery surface | pending (W5) |  |
| D03 T14 §6 | 21 | Lens Correction and Adaptive Wide Angle | pending (W5) |  |
| D03 T14 §7 | 21 | Vanishing Point and live projections | pending (W5) |  |
| D03 T21 §6 | 21 | Gesso 0.7.0 (Phase 21) | pending (W5) |  |
| D01 T06 §8 | 22 | Light and shadow | pending (W5) |  |
| D01 T06 §9 | 22 | Procedural noise and nature | pending (W5) |  |
| D01 T06 §10 | 22 | Patterns and fractals | pending (W5) |  |
| D01 T06 §11 | 22 | Edges and stylize | pending (W5) |  |
| D01 T06 §12 | 22 | Artistic extensions | pending (W5) |  |
| D01 T06 §13 | 22 | Generic, morphology, and channel math | pending (W5) |  |
| D03 T14 §5 | 22 | Lighting and flare surfaces | pending (W5) |  |
| D03 T14 §8 | 22 | The GEGL operation tool and the filter browser | pending (W5) |  |
| D03 T14 §9 | 22 | GIMP decor and combine effects as native commands | pending (W5) |  |
| D03 T14 §10 | 22 | Dedicated filter editors and Affinity filter extras | pending (W5) |  |
| D03 T14 §12 | 22 | Gesso extension modules: managed filter plug-ins | pending (W5) |  |
| D03 T14 §13 | 22 | The G'MIC filter collection | pending (W5) |  |
| D03 T21 §7 | 22 | Gesso 0.8.0 (Phase 22) | pending (W5) |  |
| D01 T07 §1 | 23 | The develop pipeline core: white balance, exposure, tone, and curves | pending (W5) |  |
| D01 T07 §2 | 23 | Presence and color: texture, clarity, dehaze, color mixer, and grading | pending (W5) |  |
| D01 T07 §3 | 23 | Detail and optics: sharpening, noise, grain, vignette, lens, and geometry | pending (W5) |  |
| D01 T07 §4 | 23 | The local masking engine | pending (W5) |  |
| D01 T07 §5 | 23 | Spot removal, red eye, and pet eye | pending (W5) |  |
| D01 T07 §6 | 23 | Presets, snapshots, and XMP settings exchange | pending (W5) |  |
| D01 T07 §7 | 23 | The tone equalizer stage | pending (W5) |  |
| D03 T15 §1 | 23 | The Camera Raw filter dialog | pending (W5) |  |
| D03 T15 §13 | 23 | Camera Raw reports, overlays, view tools, workflow, presets, and Render to DNG | pending (W5) |  |
| D03 T15 §12 | 23 | The Develop studio and RAW layers | pending (W5) |  |
| D03 T15 §2 | 23 | Develop masking and local adjustments surface | pending (W5) |  |
| D03 T15 §4 | 23 | 32-bit HDR editing and HDR display | pending (W5) |  |
| D03 T15 §3 | 23 | Tone mapping and HDR Toning | pending (W5) |  |
| D03 T15 §5 | 23 | The image alignment engine and auto-align layers | pending (W5) |  |
| D03 T15 §6 | 23 | Merge to HDR | pending (W5) |  |
| D03 T15 §7 | 23 | Panorama | pending (W5) |  |
| D03 T15 §8 | 23 | Image stacks and auto-blend layers | pending (W5) |  |
| D03 T15 §9 | 23 | Focus merge | pending (W5) |  |
| D03 T15 §10 | 23 | Astrophotography stacking | pending (W5) |  |
| D03 T15 §14 | 23 | Astro filters: stretches, background extraction, calibration, color mapping, and separation | pending (W5) |  |
| D03 T15 §11 | 23 | Crop and straighten scanned photos | pending (W5) |  |
| D03 T21 §8 | 23 | Gesso 0.9.0 (Phase 23) | pending (W5) |  |
| D03 T16 §1 | 24 | Text layers on the shared text engine | pending (W5) |  |
| D03 T16 §9 | 24 | Type tools and on-canvas text editing | pending (W5) |  |
| D03 T16 §5 | 24 | Paths, the Paths panel, and path geometry in Isotone.Core | pending (W5) |  |
| D03 T16 §10 | 24 | Path exchange and path commands: SVG, Illustrator, clipping paths, booleans, and align | pending (W5) |  |
| D03 T16 §2 | 24 | Character formatting, OpenType, glyphs, and fonts | pending (W5) |  |
| D03 T16 §3 | 24 | Paragraph formatting and text frames | pending (W5) |  |
| D03 T16 §4 | 24 | Type styles and text commands | pending (W5) |  |
| D03 T16 §6 | 24 | Pen and path editing tools | pending (W5) |  |
| D03 T16 §7 | 24 | Shape layers and shape tools | pending (W5) |  |
| D03 T16 §11 | 24 | Custom shapes, vector layers, and the Gfig job | pending (W5) |  |
| D03 T16 §8 | 24 | Frames and vector output | pending (W5) |  |
| D03 T21 §9 | 24 | Gesso 0.10.0 (Phase 24) | pending (W5) |  |
| D03 T17 §1 | 25 | File menu extensions: open, revert, close, and save a copy | pending (W5) |  |
| D03 T17 §15 | 25 | Place, export and overwrite semantics, notes import, Load Files into Stack, and watermarks | pending (W5) |  |
| D03 T17 §12 | 25 | Create from clipboard, screenshots, scanners, URLs, and archives | pending (W5) |  |
| D03 T17 §2 | 25 | PSD and PSB write: structure | pending (W5) |  |
| D03 T17 §13 | 25 | PSD write: live content and editability options | pending (W5) |  |
| D03 T17 §3 | 25 | PSD read fidelity: live adjustments, styles, text, and smart objects | pending (W5) |  |
| D03 T17 §4 | 25 | GIMP XCF read | pending (W5) |  |
| D03 T17 §14 | 25 | GIMP XCF write | pending (W5) |  |
| D03 T17 §5 | 25 | Modern web formats: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, QOI, JPEG XR | pending (W5) |  |
| D03 T17 §6 | 25 | HDR and scientific formats | pending (W5) |  |
| D03 T17 §7 | 25 | Document formats: PDF import, Photoshop PDF, and PDF export | pending (W5) |  |
| D03 T17 §16 | 25 | PostScript, EPS, SVG, and metafiles | pending (W5) |  |
| D03 T17 §8 | 25 | Common and legacy raster formats I | pending (W5) |  |
| D03 T17 §9 | 25 | Legacy raster formats II and text and resource exports | pending (W5) |  |
| D03 T17 §11 | 25 | JPEG, PNG, and TIFF option extensions | pending (W5) |  |
| D03 T17 §10 | 25 | Metadata: EXIF, IPTC, XMP, and File Info | pending (W5) |  |
| D03 T18 §1 | 25 | Export As and Quick Export | pending (W5) |  |
| D03 T18 §8 | 25 | Layers, artboards, and comps to files and PDF, and generated image assets | pending (W5) |  |
| D03 T18 §2 | 25 | Save for Web, Web filters, and the Image Map editor | pending (W5) |  |
| D03 T18 §9 | 25 | The Export studio: slices, per-slice formats, naming tokens, continuous export, and app icons | pending (W5) |  |
| D03 T18 §3 | 25 | Slices | pending (W5) |  |
| D03 T18 §4 | 25 | Color settings, policies, custom CMYK, and assign and convert | pending (W5) |  |
| D03 T18 §10 | 25 | Display color management per view and OpenColorIO | pending (W5) |  |
| D03 T18 §5 | 25 | Soft proofing and gamut warning | pending (W5) |  |
| D03 T18 §6 | 25 | Print | pending (W5) |  |
| D03 T18 §7 | 25 | Print output extras, contact sheets, PDF presentation, and preflight | pending (W5) |  |
| D03 T21 §10 | 25 | Gesso 0.11.0 (Phase 25) | pending (W5) |  |
| D03 T19 §1 | 26 | AI in Gesso: the AI menu, settings, usage, and the provenance panel | pending (W5) |  |
| D03 T19 §2 | 26 | The image-generation adapter | pending (W5) |  |
| D03 T19 §3 | 26 | Generative fill and generative remove | pending (W5) |  |
| D03 T19 §4 | 26 | Generative expand | pending (W5) |  |
| D03 T19 §5 | 26 | Generate image, background, and similar | pending (W5) |  |
| D03 T19 §6 | 26 | AI selection: subject, sky, objects, and people | pending (W5) |  |
| D03 T19 §15 | 26 | AI masks everywhere: detections, mask all objects, and develop masks | pending (W5) |  |
| D03 T19 §7 | 26 | Neural-filter equivalents | pending (W5) |  |
| D03 T19 §14 | 26 | Depth, portrait blur, and relighting | pending (W5) |  |
| D03 T19 §8 | 26 | Upscale and enhance | pending (W5) |  |
| D03 T19 §9 | 26 | Distraction and object removal | pending (W5) |  |
| D03 T19 §10 | 26 | The Gesso assistant: prompt to edit | pending (W5) |  |
| D03 T19 §11 | 26 | AI type and faces | pending (W5) |  |
| D03 T19 §12 | 26 | Sky replacement | pending (W5) |  |
| D03 T19 §13 | 26 | The suite pipeline and the brand kit in Gesso | pending (W5) |  |
| D03 T21 §11 | 26 | Gesso 0.12.0 (Phase 26) | pending (W5) |  |
| D03 T07 §17 | 27 | Workspaces, panels, and preferences | pending (W5) |  |
| D03 T20 §1 | 27 | Workspaces, panels, the Properties panel, and the Contextual Task Bar | pending (W5) |  |
| D03 T20 §2 | 27 | The toolbar and the options bar | pending (W5) |  |
| D03 T20 §3 | 27 | Menus, shortcuts, and command search | pending (W5) |  |
| D03 T20 §4 | 27 | Preferences I: general, tools, cursors, units, guides, and type | pending (W5) |  |
| D03 T20 §9 | 27 | Interface appearance, language, and accessibility display preferences | pending (W5) |  |
| D03 T20 §5 | 27 | Preferences II: files, performance, memory, and resources | pending (W5) |  |
| D03 T20 §6 | 27 | Pen, touch, and input devices | pending (W5) |  |
| D03 T20 §7 | 27 | The presets manager and resource libraries | pending (W5) |  |
| D03 T20 §8 | 27 | Help, learning, and diagnostics | pending (W5) |  |
| D03 T07 §18 | 27 | Performance I: the benchmark harness and the Gesso performance budget | pending (W5) |  |
| D03 T07 §19 | 27 | Performance II: memory: tile cache, compression, history, and large-document open | pending (W5) |  |
| D03 T07 §20 | 27 | Performance III: SIMD hot paths, parallel compositing, and cold start | pending (W5) |  |
| D03 T07 §16 | 27 | Accessibility and localization | pending (W5) |  |
| D03 T21 §12 | 27 | Gesso 1.0.0 (Phase 27): the parity catalog complete | pending (W5) |  |
| D01 T13 §5 | 28 | The Albumen map from Lightroom Classic's documentation | pending (W6) |  |
| D04 T01 §1 | 28 | The competitor survey, driven | pending (W6) |  |
| D04 T01 §2 | 28 | Create the Albumen app | pending (W6) |  |
| D04 T01 §3 | 28 | The RAW decoder decision | pending (W6) |  |
| D04 T01 §4 | 28 | RAW decode with fidelity fixtures | pending (W6) |  |
| D04 T01 §5 | 28 | The catalog database | pending (W6) |  |
| D04 T01 §6 | 28 | Import | pending (W6) |  |
| D04 T01 §7 | 28 | Thumbnails and the preview cache | pending (W6) |  |
| D04 T01 §8 | 28 | The library grid | pending (W6) |  |
| D04 T01 §9 | 28 | Loupe, compare, and filmstrip | pending (W6) |  |
| D04 T01 §10 | 29 | Keywords, collections, and smart collections | pending (W6) |  |
| D04 T01 §11 | 29 | Ratings, flags, labels, and XMP sidecars | pending (W6) |  |
| D04 T01 §12 | 29 | Albumen's window follows the Lightroom Classic map | pending (W6) |  |
| D04 T02 §1 | 29 | The edit stack | pending (W6) |  |
| D04 T02 §2 | 29 | The develop pipeline on the suite develop engine | pending (W6) |  |
| D04 T02 §3 | 29 | The develop panel | pending (W6) |  |
| D04 T02 §4 | 29 | Crop and straighten | pending (W6) |  |
| D04 T02 §5 | 29 | Presets, copy and paste settings, and sync | pending (W6) |  |
| D04 T02 §6 | 29 | Export | pending (W6) |  |
| D06 T01 §3 | 29 | The Albumen user guide | pending (W8) |  |
| D04 T02 §7 | 29 | Edit in Gesso | pending (W6) |  |
| D04 T02 §8 | 29 | Albumen 0.1.0 | pending (W6) |  |
| D04 T13 §1 | 30 | The shared codec registry in Isotone.Core | pending (W6) |  |
| D04 T13 §2 | 30 | Modern and HDR formats in Albumen | pending (W6) |  |
| D04 T13 §3 | 30 | Common legacy and special raster formats | pending (W6) |  |
| D04 T13 §8 | 30 | Rare and historical raster formats | pending (W6) |  |
| D04 T13 §9 | 30 | CAD and plotter drawings: DXF, DWG, HPGL, and CGM | pending (W6) |  |
| D04 T13 §4 | 30 | Documents and multi-page formats | pending (W6) |  |
| D04 T13 §5 | 30 | RAW coverage and RAW+JPEG pairs | pending (W6) |  |
| D04 T04 §1 | 30 | The Albumen Viewer: a second executable with a startup budget and the hand-off to Albumen | pending (W6) |  |
| D04 T04 §17 | 30 | Resident quick-start mode | pending (W6) |  |
| D04 T04 §2 | 30 | The viewer decode path: screen-size decode, prefetch, and display color | pending (W6) |  |
| D04 T04 §3 | 30 | Default viewer registration and shell integration | pending (W6) |  |
| D04 T04 §4 | 30 | Zoom, fit, pan, magnifier, and navigator | pending (W6) |  |
| D04 T04 §5 | 30 | Browsing a folder in the viewer | pending (W6) |  |
| D04 T04 §14 | 30 | Viewer window and display options | pending (W6) |  |
| D04 T04 §6 | 30 | File operations and hand-offs in the viewer | pending (W6) |  |
| D04 T04 §9 | 30 | Image information, histogram, and viewer tools | pending (W6) |  |
| D04 T04 §10 | 30 | Multi-page and animated images in the viewer | pending (W6) |  |
| D04 T04 §7 | 30 | Fullscreen and presentation | pending (W6) |  |
| D04 T04 §8 | 30 | Quick slideshow in the viewer | pending (W6) |  |
| D04 T15 §1 | 30 | Albumen 0.2.0 (Phase 30) | pending (W6) |  |
| D04 T11 §1 | 31 | The batch engine, the original-write policy, and the Activity Manager | pending (W6) |  |
| D04 T11 §2 | 31 | The token engine | pending (W6) |  |
| D04 T11 §3 | 31 | Batch rename | pending (W6) |  |
| D04 T13 §6 | 31 | Write formats and per-format save options | pending (W6) |  |
| D04 T11 §4 | 31 | Batch convert | pending (W6) |  |
| D04 T11 §5 | 31 | Batch resize, rotate, and flip | pending (W6) |  |
| D04 T11 §6 | 31 | Batch color: exposure, profiles, and color depth | pending (W6) |  |
| D04 T11 §8 | 31 | Text overlays and watermarks | pending (W6) |  |
| D04 T11 §7 | 31 | The batch edit pipeline | pending (W6) |  |
| D04 T13 §7 | 31 | The DNG writer | pending (W6) |  |
| D04 T11 §9 | 31 | Batch develop and batch export | pending (W6) |  |
| D04 T11 §10 | 31 | The batch dialog: file lists, profiles, and running from Explorer and the viewer | pending (W6) |  |
| D04 T04 §11 | 31 | Quick edits I: rotate, flip, select, crop, resize, and canvas | pending (W6) |  |
| D04 T04 §16 | 31 | Lossless JPEG transforms to new files, or in place on opt-in | pending (W6) |  |
| D04 T04 §12 | 31 | Quick edits II: color corrections, color depth, and palettes | pending (W6) |  |
| D04 T04 §15 | 31 | Quick edits III: the effects browser and viewer effects | pending (W6) |  |
| D04 T04 §13 | 31 | Quick edits IV: text, watermarks, borders, and combining images | pending (W6) |  |
| D04 T04 §18 | 31 | Captions and info text through the token engine | pending (W6) |  |
| D04 T15 §2 | 31 | Albumen 0.3.0 (Phase 31) | pending (W6) |  |
| D04 T05 §1 | 32 | The browse model: folders without import, browsed and library photos | pending (W6) |  |
| D04 T05 §2 | 32 | The background indexer | pending (W6) |  |
| D04 T05 §3 | 32 | The folder tree, favorites, address bar, tabs, and home page | pending (W6) |  |
| D04 T05 §4 | 32 | File list views, thumbnails, and the preview pane | pending (W6) |  |
| D04 T05 §5 | 32 | Sort, group, filter, and select in browse | pending (W6) |  |
| D04 T05 §6 | 32 | File operations: copy, move, rename, delete, and undo | pending (W6) |  |
| D04 T05 §7 | 32 | Info palette, properties, and compare images | pending (W6) |  |
| D04 T05 §8 | 32 | Image basket and selective browsing | pending (W6) |  |
| D04 T05 §9 | 32 | The private folder | pending (W6) |  |
| D04 T05 §10 | 32 | Calendar and timeline browsing | pending (W6) |  |
| D04 T05 §11 | 32 | Duplicate finder | pending (W6) |  |
| D04 T05 §12 | 32 | Archives and folder sync | pending (W6) |  |
| D04 T15 §3 | 32 | Albumen 0.4.0 (Phase 32) | pending (W6) |  |
| D04 T06 §1 | 33 | Library view extensions: cell styles, overlays, survey, and a second window | pending (W6) |  |
| D04 T06 §2 | 33 | Culling extensions: label sets, flag and rating cycles, tagging, and auto advance | pending (W6) |  |
| D04 T06 §3 | 33 | Stacks, versions, and virtual copies | pending (W6) |  |
| D04 T06 §4 | 33 | The filter bar extended: text, attributes, metadata columns, and presets | pending (W6) |  |
| D04 T06 §5 | 33 | Collections extended: sets, target and quick collections, and the smart-collection rule editor | pending (W6) |  |
| D04 T06 §6 | 33 | Categories and auto categories | pending (W6) |  |
| D04 T06 §7 | 33 | Quick search and advanced search | pending (W6) |  |
| D04 T06 §8 | 33 | Folders and catalog panels: synchronize, relocate, missing photos, and offline volumes | pending (W6) |  |
| D04 T06 §9 | 33 | Catalog backup and maintenance | pending (W6) |  |
| D04 T06 §10 | 33 | Multiple catalogs, catalog settings, and preview management | pending (W6) |  |
| D04 T06 §11 | 33 | Smart previews and offline editing | pending (W6) |  |
| D04 T06 §12 | 33 | The dashboard and library statistics | pending (W6) |  |
| D04 T06 §13 | 33 | Painter and Quick Develop | pending (W6) |  |
| D04 T15 §4 | 33 | Albumen 0.5.0 (Phase 33) | pending (W6) |  |
| D04 T08 §1 | 34 | The metadata model: every EXIF, IPTC, and XMP field read and tracked | pending (W6) |  |
| D04 T08 §8 | 34 | Writing metadata: sidecars, pending writes, and exported copies | pending (W6) |  |
| D04 T08 §9 | 34 | Embedding metadata into originals, opt-in | pending (W6) |  |
| D04 T08 §2 | 34 | The metadata panel and properties pane | pending (W6) |  |
| D04 T08 §3 | 34 | Metadata presets and synchronizing metadata | pending (W6) |  |
| D04 T08 §4 | 34 | Capture time editing | pending (W6) |  |
| D04 T08 §5 | 34 | Keyword extensions | pending (W6) |  |
| D04 T07 §1 | 34 | The import window extended | pending (W6) |  |
| D04 T07 §2 | 34 | File handling on import: previews, backup copies, renaming, and destination folders | pending (W6) |  |
| D04 T07 §3 | 34 | Apply during import and import presets | pending (W6) |  |
| D04 T07 §4 | 34 | Phones and cameras over Windows Portable Devices | pending (W6) |  |
| D04 T07 §5 | 34 | Auto import from watched folders | pending (W6) |  |
| D04 T07 §6 | 34 | Convert to DNG | pending (W6) |  |
| D04 T07 §7 | 34 | Scanning and Copy Shop | pending (W6) |  |
| D04 T07 §8 | 34 | Screen capture | pending (W6) |  |
| D04 T08 §6 | 34 | The map view and places | pending (W6) |  |
| D04 T08 §7 | 34 | Track logs, geotagging, and offline reverse geocoding | pending (W6) |  |
| D04 T15 §5 | 34 | Albumen 0.6.0 (Phase 34) | pending (W6) |  |
| D04 T09 §1 | 35 | The develop workspace extended: tool strip, views, reference, and overlays | pending (W6) |  |
| D04 T09 §2 | 35 | History, snapshots, and the before state | pending (W6) |  |
| D04 T09 §17 | 35 | Saving develop results: leaving develop, new files, sidecars, and opt-in writes to originals | pending (W6) |  |
| D04 T09 §3 | 35 | Profiles, white balance, presence, and HDR editing | pending (W6) |  |
| D04 T09 §4 | 35 | Tone curve, color mixer, point color, color grading, and ACDSee color panels | pending (W6) |  |
| D04 T09 §5 | 35 | Detail: sharpening and noise reduction | pending (W6) |  |
| D04 T09 §6 | 35 | Lens corrections, DNG opcodes, and flat-field | pending (W6) |  |
| D04 T09 §7 | 35 | Transform, Upright, calibration, and process versions | pending (W6) |  |
| D04 T09 §8 | 35 | Effects and crop extensions | pending (W6) |  |
| D04 T09 §10 | 35 | Remove, heal, clone, and red eye | pending (W6) |  |
| D04 T09 §11 | 35 | Presets and defaults extended | pending (W6) |  |
| D04 T09 §12 | 35 | Sync, copy and paste, and auto sync extended | pending (W6) |  |
| D04 T15 §6 | 35 | Albumen 0.7.0 (Phase 35) | pending (W6) |  |
| D04 T09 §9 | 36 | Masking: brushes, gradients, range masks, and pixel targeting | pending (W6) |  |
| D01 T07 §8 | 36 | Soft focus, glow, and skin tune stages | pending (W6) |  |
| D01 T07 §9 | 36 | Develop LUTs, blend modes, and looks | pending (W6) |  |
| D04 T09 §13 | 36 | Light EQ, soft focus, and skin tune | pending (W6) |  |
| D04 T09 §14 | 36 | Color LUTs, develop blend modes, and develop effects | pending (W6) |  |
| D04 T09 §15 | 36 | Soft proofing | pending (W6) |  |
| D04 T09 §16 | 36 | Photo merge: HDR, panorama, and focus stacking | pending (W6) |  |
| D04 T15 §7 | 36 | Albumen 0.8.0 (Phase 36) | pending (W6) |  |
| D04 T10 §1 | 37 | AI in Albumen: the AI menu, the send gate, provenance, and the AI data store | pending (W6) |  |
| D04 T10 §2 | 37 | Face detection through the vision model | pending (W6) |  |
| D04 T10 §3 | 37 | Face naming, person keywords, and person search | pending (W6) |  |
| D04 T10 §12 | 37 | Faces in the viewer and face regions in XMP | pending (W6) |  |
| D04 T10 §4 | 37 | AI keywords, captions, alt text, and OCR | pending (W6) |  |
| D04 T10 §5 | 37 | Similar photos and visual duplicates | pending (W6) |  |
| D04 T10 §6 | 37 | Assisted culling | pending (W6) |  |
| D04 T10 §7 | 37 | AI masks in develop | pending (W6) |  |
| D04 T10 §8 | 37 | Enhance: denoise, raw details, and super resolution | pending (W6) |  |
| D04 T10 §9 | 37 | Generative and distraction removal | pending (W6) |  |
| D04 T10 §10 | 37 | Lens blur and depth | pending (W6) |  |
| D04 T10 §11 | 37 | Adaptive presets, AI auto settings, and natural-language search | pending (W6) |  |
| D04 T15 §8 | 37 | Albumen 0.9.0 (Phase 37) | pending (W6) |  |
| D04 T12 §1 | 38 | Export extended: destinations, naming, formats, sizing, and color | pending (W6) |  |
| D04 T12 §13 | 38 | Export presets, metadata, watermarks, and post-processing | pending (W6) |  |
| D04 T12 §2 | 38 | Export formats and DNG output | pending (W6) |  |
| D04 T12 §3 | 38 | Publish to local folders | pending (W6) |  |
| D04 T12 §4 | 38 | Print I: the print module, page setup, and the print job | pending (W6) |  |
| D04 T12 §5 | 38 | Print II: packages, overlays, templates, and document printing | pending (W6) |  |
| D04 T12 §6 | 38 | Contact sheets | pending (W6) |  |
| D04 T12 §7 | 38 | Slideshow I: templates, layout, overlays, and titles | pending (W6) |  |
| D04 T12 §8 | 38 | Slideshow II: playback, music, transitions, and export | pending (W6) |  |
| D04 T12 §9 | 38 | Web galleries | pending (W6) |  |
| D04 T12 §10 | 38 | Books | pending (W6) |  |
| D04 T12 §11 | 38 | PDF and PowerPoint creation | pending (W6) |  |
| D04 T12 §12 | 38 | Email and local sharing | pending (W6) |  |
| D04 T15 §9 | 38 | Albumen 0.10.0 (Phase 38) | pending (W6) |  |
| D04 T14 §1 | 39 | Modes, the module picker, and panels | pending (W6) |  |
| D04 T14 §2 | 39 | Toolbars, menus, pane layout, saved workspaces, and touch | pending (W6) |  |
| D04 T14 §3 | 39 | The keymap and shortcuts | pending (W6) |  |
| D04 T14 §4 | 39 | Preferences I: general, interface, file handling, and the viewer and browse pages | pending (W6) |  |
| D04 T14 §5 | 39 | Preferences II: performance, caches, color management, and display | pending (W6) |  |
| D04 T14 §6 | 39 | Settings storage, portable mode, and migration | pending (W6) |  |
| D04 T14 §10 | 39 | Originals: the opt-in write settings | pending (W6) |  |
| D05 T01 §4 | 39 | The update check | pending (W8) |  |
| D04 T14 §7 | 39 | Help, learning, languages, and updates | pending (W6) |  |
| D04 T14 §8 | 39 | Themes and appearance | pending (W6) |  |
| D04 T14 §9 | 39 | External editors | pending (W6) |  |
| D04 T02 §9 | 39 | Accessibility and localization | pending (W6) |  |
| D04 T15 §10 | 39 | Albumen 1.0.0 (Phase 39): the parity catalog complete | pending (W6) |  |
| D05 T01 §2 | 40 | Sign binaries and installers | pending (W8) |  |
| D05 T01 §3 | 40 | win-arm64 publish and installers | pending (W8) |  |
| D05 T01 §5 | 40 | winget manifests | pending (W8) |  |
| D06 T01 §4 | 40 | Install and troubleshooting guides | pending (W8) |  |
| D05 T01 §6 | 40 | The suite bundle: isotone-v1.0.0 | pending (W8) |  |
| D06 T02 §2 | 40 | README images from real captures | pending (W8) |  |
| D06 T02 §3 | 40 | The user guides as a published site | pending (W8) |  |
| D03 T07 §11 | 41 | RAW import through the shared decoder | pending (W7) |  |
| D02 T18 §9 | 41 | GIMP XCF import in Stilus on the shared XCF core | pending (W7) |  |
| D02 T18 §10 | 41 | Camera RAW import and the RAW Lab | pending (W7) |  |
| D02 T17 §11 | 41 | Stilus 1.1.0 (Phase 41) | pending (W7) |  |
| D01 T10 §1 | 42 | The action model, the recorder, and playback | pending (W7) |  |
| D01 T10 §2 | 42 | The Actions panel in Isotone.UI | pending (W7) |  |
| D01 T10 §3 | 42 | Action files and the action library | pending (W7) |  |
| D01 T10 §4 | 42 | The scripting host | pending (W7) |  |
| D01 T10 §5 | 42 | The script editor and console | pending (W7) |  |
| D01 T10 §6 | 42 | The automation server and the MCP server | pending (W7) |  |
| D01 T10 §7 | 42 | The extension SDK and the extension manager | pending (W7) |  |
| D01 T10 §8 | 42 | The command line | pending (W7) |  |
| D01 T10 §9 | 42 | The suite batch runner and droplets | pending (W7) |  |
| D02 T19 §1 | 42 | The Stilus object model and recordable commands | pending (W7) |  |
| D02 T19 §2 | 42 | Scripts, extensions, and macros in Stilus documents | pending (W7) |  |
| D02 T19 §3 | 42 | Batch processing and the command line in Stilus | pending (W7) |  |
| D02 T17 §12 | 42 | Stilus 1.2.0 (Phase 42) | pending (W7) |  |
| D03 T22 §1 | 42 | The Gesso object model, recordable commands, and actions in Gesso | pending (W7) |  |
| D03 T22 §2 | 42 | Scripts in Gesso | pending (W7) |  |
| D03 T22 §3 | 42 | Procedures and plug-ins in Gesso | pending (W7) |  |
| D03 T22 §4 | 42 | Extensions, the MCP server, and remote connections in Gesso | pending (W7) |  |
| D03 T22 §5 | 42 | Batch, droplets, the Image Processor, and headless runs | pending (W7) |  |
| D03 T22 §6 | 42 | Variables and data sets | pending (W7) |  |
| D03 T21 §13 | 42 | Gesso 1.1.0 (Phase 42) | pending (W7) |  |
| D04 T17 §1 | 42 | Recorded actions in Albumen | pending (W7) |  |
| D04 T17 §2 | 42 | Albumen extension points | pending (W7) |  |
| D04 T17 §3 | 42 | The Albumen command line | pending (W7) |  |
| D04 T15 §11 | 42 | Albumen 1.1.0 (Phase 42) | pending (W7) |  |
| D01 T11 §1 | 43 | The media stack decision and decoding | pending (W7) |  |
| D01 T11 §2 | 43 | Playback, the audio engine, and the media clock | pending (W7) |  |
| D01 T11 §3 | 43 | Encoding: render video and audio | pending (W7) |  |
| D01 T11 §4 | 43 | The MediaTransport surface in Isotone.UI | pending (W7) |  |
| D03 T23 §1 | 43 | Video layers and opening video | pending (W7) |  |
| D03 T23 §2 | 43 | The Timeline panel | pending (W7) |  |
| D03 T23 §3 | 43 | Audio tracks and render video | pending (W7) |  |
| D03 T23 §4 | 43 | Frame animation, onion skin, and tweening | pending (W7) |  |
| D03 T23 §5 | 43 | Animated formats: GIF, APNG, WebP, MNG, and FLI authoring | pending (W7) |  |
| D03 T23 §6 | 43 | Animation filters and temporal blur | pending (W7) |  |
| D03 T21 §14 | 43 | Gesso 1.2.0 (Phase 43) | pending (W7) |  |
| D04 T16 §1 | 43 | Video and audio in the library and browse | pending (W7) |  |
| D04 T16 §2 | 43 | Video and audio playback in the viewer and the loupe | pending (W7) |  |
| D04 T16 §3 | 43 | Trim, poster frame, frame extraction, and video export | pending (W7) |  |
| D04 T16 §4 | 43 | Media mode | pending (W7) |  |
| D04 T16 §5 | 43 | Image audio | pending (W7) |  |
| D04 T16 §6 | 43 | Video in slideshows and slideshow video export | pending (W7) |  |
| D04 T15 §12 | 43 | Albumen 1.2.0 (Phase 43) | pending (W7) |  |
| D01 T12 §1 | 44 | The local inference runtime | pending (W7) |  |
| D01 T12 §2 | 44 | The model catalog, downloads, and license records | pending (W7) |  |
| D01 T12 §3 | 44 | The Model Manager surface in Isotone.UI | pending (W7) |  |
| D01 T12 §4 | 44 | Task adapters: segmentation, inpainting, upscaling, denoise, and depth | pending (W7) |  |
| D01 T07 §10 | 44 | The GPU compute device in Isotone.Core | pending (W7) |  |
| D01 T07 §11 | 44 | Develop stages on the GPU with CPU parity | pending (W7) |  |
| D01 T07 §12 | 44 | GPU masks, the extended stages, and measured budgets | pending (W7) |  |
| D03 T19 §16 | 44 | On-device models in Gesso: remove, selection, star separation, and normals | pending (W7) |  |
| D03 T19 §17 | 44 | On-device photo models: motion blur reduction, mixed light, and SDR to HDR | pending (W7) |  |
| D03 T21 §15 | 44 | Gesso 1.3.0 (Phase 44) | pending (W7) |  |
| D04 T10 §13 | 44 | On-device models in Albumen: offline denoise, keywords, and similarity | pending (W7) |  |
| D04 T15 §13 | 44 | Albumen 1.3.0 (Phase 44) | pending (W7) |  |
| D04 T13 §10 | 45 | Flash SWF: the first frame through an own parser | pending (W7) |  |
| D04 T13 §11 | 45 | ECW, MrSID, JPM, and MRC through an optional GDAL | pending (W7) |  |
| D04 T13 §12 | 45 | Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC through clean-room analysis | pending (W7) |  |
| D04 T15 §14 | 45 | Albumen 1.4.0 (Phase 45) | pending (W7) |  |
| D05 T01 §7 | 45 | The suite bundle: isotone-v1.1.0 | pending (W8) |  |
| D99 T01 §1 | 99 | About bar, topics, and social preview | kept | operator row; stack-neutral |
| D99 T01 §2 | 99 | Branch protection with the required checks | kept | operator row; stack-neutral |
| D99 T01 §3 | 99 | A code-signing certificate | kept | operator row; stack-neutral |
| D99 T01 §4 | 99 | Confirm the icon art licenses | kept | operator row; stack-neutral |
| D99 T01 §5 | 99 | Choose each app's accent color | kept | operator row; stack-neutral |
| D99 T01 §6 | 99 | Assign the copyright to Rizonetech (Pty) Ltd | kept | operator row; stack-neutral |
| D99 T01 §7 | 99 | Trademark clearance and CIPC filing | kept | operator row; stack-neutral |
| D99 T01 §8 | 99 | Download storage and the release secrets | kept | operator row; stack-neutral |
| D99 T01 §9 | 99 | Decide the product page URLs | kept | operator row; stack-neutral |
| D99 T01 §10 | 99 | Decide on a CLA before outside contributions | kept | operator row; stack-neutral |
