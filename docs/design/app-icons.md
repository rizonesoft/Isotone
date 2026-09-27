# App icons

Nodus, Imago and Lumen share one app icon system: Direction C, the suite tile, chosen on 2026-09-27. Direction A, the neon art, is kept for the splash and for marketing only.

The app icons are separate from the UI icon catalog: catalog icons are Lucide-style strokes that draw commands and tools in the chrome, while app icons are full-color files that identify an app to Windows and to the person using it.

## Family concept

Every icon is built from three layers, and each layer has one job.

- **Graphite tile.** The same dark rounded square for every app, so the three read as one suite in a taskbar or a Start menu folder.
- **Spectrum band.** A wave of the seven suite colors along the foot of the tile: the Photon signature, identical in every app.
- **Accent glyph.** The app's own mark in its accent color: a pen nib on an anchor path for Nodus (`accent-nodus` cyan), a paintbrush with scattered pixels for Imago (`accent-imago` orange), an aperture inside viewfinder corners for Lumen (`accent-lumen` green).

The glyph is the only thing that changes between apps; the tile and band never do.

## Construction (master, 256 viewBox)

| Part | Geometry |
| --- | --- |
| Canvas | 256 x 256 viewBox, 8 px transparent margin on every side |
| Tile | `rect` x 8, y 8, 240 x 240 (8 to 248), `rx` 48, vertical gradient #34353B to #1E1F23 |
| Inner highlight | `rect` x 9, y 9, 238 x 238, `rx` 47, white stroke 2 at 9 percent opacity (reads as a 1 px inner edge) |
| Spectrum band | path `M0 226C64 214 120 238 176 226S236 212 256 216V256H0Z`, clipped to the tile, horizontal gradient from x 8 to 248 |
| Band crest | the same curve as a stroke, white 2 px at 35 percent opacity |
| Glyph safe box | about x 36 to 220, y 28 to 204, centred at (128, 116), above the band |

The glyph is centred at (128, 116), not at the tile centre, so it sits optically in the middle of the graphite area above the band.

Optical balancing makes the three glyphs look the same size although their shapes differ: relative to the original drawings, the Nodus line glyph is scaled up 25 percent (group scale 1.125), Imago 10 percent (0.990) and Lumen 8 percent (0.972). Nodus gets the most because a thin line drawing reads smallest.

Each master keeps its gradient and clip ids prefixed with the app (`nodus-c-bg`, `imago-c-spec`...) so several icons can be inlined in one document without collisions.

## Size ladder: which file at which size

| Rendered size | File | Notes |
| --- | --- | --- |
| 16 and 20 px | `<app>-16.svg` | 16 grid, tile fills the canvas, `rx` 3 |
| 24 and 30 px | `<app>-24.svg` | 24 grid, tile x/y 1 to 23, `rx` 4 |
| 32 to 40 px | `<app>-32.svg` | 32 grid, tile x/y 1 to 31, `rx` 6 |
| 48 px and up | `<app>.svg` (the master) | 48, 64, 96, 128, 256 |

Sizes in between are rendered from the next smaller file's grid only when it is an exact multiple (20 from 16 at 125 percent, 30 from 24, 40 from 32); never scale a small variant up past its range.

## Pixel-grid rules for the small variants

The 16, 24 and 32 variants are hand-tuned, not reductions of the master, and follow these rules.

- The tile is a flat #2B2C31 (the gradient's midpoint): a 20-step gradient over 16 pixels only adds blur.
- The spectrum band becomes a straight bar on whole pixels: 2 px at 16, 2.5 px at 24, 3.5 px at 32, clipped to the tile corners.
- The inner highlight and the band crest are dropped; they cannot resolve below 48 px.
- Glyphs are simplified to their silhouette: Nodus keeps the nib, the ferrule and two anchor squares; Imago keeps the brush and one to four pixel squares; Lumen keeps the aperture blades, and the viewfinder corners from 24 up.
- Straight edges and small squares sit on whole or half pixels so they render crisp at 100 percent; anchor squares are at least 2 px.
- Accent colors stay the same hex values as the master, so an icon reads as the same app at every size.

## Colors

| Role | Values |
| --- | --- |
| Tile (master) | vertical gradient #34353B (top) to #1E1F23 (bottom) |
| Tile (16 to 32) | flat #2B2C31 |
| Spectrum band | stops at 0, 0.17, 0.33, 0.5, 0.67, 0.83 and 1: #FF4D6D, #FF9A3C, #FFD84A, #4CC47A, #29C5E6, #5B7CFF, #B45CFF |
| Nodus glyph | `accent-nodus` #29C5E6, light facet #8BE6F7, ferrule #1597BA, anchors white |
| Imago glyph | `accent-imago` #F5923E, highlight #FFC98F, tuft to #FFE08A, pixels #FFD84A and warm neighbours |
| Lumen glyph | `accent-lumen` #4CC47A, light blades #9BE8B6, dark body #1B7A3D and #0B3A1C, viewfinder white |

The accents are the dark-theme values of the `accent-<app>` tokens; the icon keeps them in every theme, because it is an image on its own tile, not chrome.

## Where each is used

| Surface | Size | File |
| --- | --- | --- |
| Title-bar app mark | 16 px (20 px at 125 percent and up) | `<app>-16.svg` |
| Taskbar | 24 px at 100 percent, 30 to 48 px when scaled | `-24`, `-32`, master by the ladder |
| Start menu, pinned and all apps | 24 to 48 px by scale | by the ladder |
| Installer (Inno Setup wizard and uninstall entry) | from the `.ico` | all sizes |
| File associations (Explorer) | 16 to 256 px from the `.ico` | all sizes |
| About dialog | 128 px | master |
| Splash | 64 px | `<app>-splash.svg` (Direction A neon art), never the tile |
| Marketing and store art | any | the neon art or the master |

The title bar is the only place in the chrome where the app icon appears; everywhere else the chrome stays neutral and the app is identified by its accent on the one primary button.

## Do and do not

- Do use the file the ladder names for the rendered size.
- Do keep clear space around the icon of at least one eighth of its size (the 8 px margin of the master) on every side.
- Do place the icon as is on any theme's `frame` or `surface-panel`: the graphite tile carries its own contrast.
- Do not recolor a glyph, tint it with the Highlight color, or swap one app's accent for another's.
- Do not draw the master below 48 px: its band crest and highlight turn to mush; use the small variants.
- Do not add text, a version number or a badge to the tile.
- Do not drop or reorder the spectrum band, or change its colors per app.
- Do not use a catalog icon (`pen-tool`, `brush`, `aperture`) as a stand-in for an app icon.
- Do not use the neon art as the app icon; it is for the splash and marketing.

## Export

PNG sizes and each app's multi-resolution `.ico` (16, 20, 24, 30, 32, 40, 48, 64, 128 and 256) are generated from these SVGs by the icon export script, each size taken from the file the ladder names.

Never hand-edit an exported PNG or `.ico`: change the SVG and export again.

Source files: `resources/icons/<app>/<app>.svg` (master), `<app>-16.svg`, `<app>-24.svg`, `<app>-32.svg` and `<app>-splash.svg`, the same fifteen files as the App icons asset group.
