# App icons

Stilus, Gesso and Albumen share one app icon system: Direction C, the suite tile, chosen on 2026-09-27. The splash is the Suite card (operator decision 2026-09-27), a 640 x 360 graphite card that carries the master icon; its spec is the Splash component guide. Direction A, the neon art, is retired and no longer in the repository.

The app icons are separate from the UI icon catalog: catalog icons are Lucide-style strokes that draw commands and tools in the chrome, while app icons are full-color files that identify an app to Windows and to the person using it.

## Family concept

Every icon is built from three layers, and each layer has one job.

- **Graphite tile.** The same dark rounded square for every app, so the three read as one suite in a taskbar or a Start menu folder.
- **Spectrum band.** A wave of the seven suite colors along the foot of the tile: the Isotone signature, identical in every app.
- **Accent glyph.** The app's own mark in its accent color: a pen nib on an anchor path for Stilus (`accent-stilus` cyan), a paintbrush with scattered pixels for Gesso (`accent-gesso` orange), an aperture inside viewfinder corners for Albumen (`accent-albumen` green).

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

Optical balancing makes the three glyphs look the same size although their shapes differ: relative to the original drawings, the Stilus line glyph is scaled up 25 percent (group scale 1.125), Gesso 10 percent (0.990) and Albumen 8 percent (0.972). Stilus gets the most because a thin line drawing reads smallest.

Each master keeps its gradient and clip ids prefixed with the app (`stilus-c-bg`, `gesso-c-spec`...) so several icons can be inlined in one document without collisions.

## Size ladder: which file at which size

| Rendered size | File | Notes |
| --- | --- | --- |
| 16 and 20 px | `<app>-16.svg` | 16 grid, tile fills the canvas, `rx` 3 |
| 24 and 30 px | `<app>-24.svg` | 24 grid, tile x/y 1 to 23, `rx` 4 |
| 32 to 40 px | `<app>-32.svg` | 32 grid, tile x/y 1 to 31, `rx` 6 |
| 48 px and up | `<app>.svg` (the master) | 48, 64, 96, 128, 256 |

Sizes in between are rendered from the next smaller file's grid only when it is an exact multiple (20 from 16 at 125 percent, 30 from 24, 40 from 32); never scale a small variant up past its range.

## The small variants (16, 24, 32)

At taskbar and title-bar sizes an icon is recognized by its silhouette, so the small variants carry the app's main object alone, enlarged to fill the space above the band (operator decision, 2026-09-27: less detail at 32, 24 and 16).

- Stilus: the pen nib alone (no Bezier curve, handle, or anchor nodes). The breather hole stays at 24 and 32; at 16 the nib is solid with only the slit.
- Gesso: the paintbrush alone (no pixel squares). The light ferrule band stays at every size, since it is what makes the shape read as a brush.
- Albumen: the six-blade aperture alone (no viewfinder corners); at 16 the blade separators are heavier so the blades stay distinct.
- The glyph is scaled to fill a box inset from the tile (1.5 px at 16, 2.6 px at 24, 3.2 px at 32) and centered above the band.
- The tile keeps the master's graphite gradient with a smaller corner radius (3, 4, 6), and the spectrum band is a straight bar 2, 2.5, and 3.5 px tall, clipped to the tile corners; the inner highlight and the band crest are dropped.
- The variants are generated from the masters' glyph shapes by `scripts/generate-small-icons.py`, so a change to a master glyph carries through; regenerate them after editing a master.
- Accent colors stay the same hex values as the master, so an icon reads as the same app at every size.

## Colors

| Role | Values |
| --- | --- |
| Tile (master) | vertical gradient #34353B (top) to #1E1F23 (bottom) |
| Tile (16 to 32) | flat #2B2C31 |
| Spectrum band | stops at 0, 0.17, 0.33, 0.5, 0.67, 0.83 and 1: #FF4D6D, #FF9A3C, #FFD84A, #4CC47A, #29C5E6, #5B7CFF, #B45CFF |
| Stilus glyph | `accent-stilus` #29C5E6, light facet #8BE6F7, ferrule #1597BA, anchors white (48 px and up) |
| Gesso glyph | `accent-gesso` #F5923E, highlight #FFC98F, tuft to #FFE08A, pixels #FFD84A and warm neighbours |
| Albumen glyph | `accent-albumen` #4CC47A, light blades #9BE8B6, dark body #1B7A3D and #0B3A1C, viewfinder white |

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
| Splash (the Suite card) | 136 px | master, on the card built in XAML to the Splash component guide |
| Marketing and store art | any | the master, or `<app>-splash.svg` (the Suite card reference design, 640 x 360) |

The title bar is the only place in the chrome where the app icon appears; everywhere else the chrome stays neutral and the app is identified by its accent on the one primary button.

## The suite icon and wordmark

The Isotone Graphics Suite has its own icon and wordmark (operator decision 2026-09-28: icon direction A, "Three Lights", and wordmark 2, with the dot of the i as the three primaries). Both are generated by `scripts/build-suite-mark.py`; edit the script, never the SVGs.

- **Icon** (`resources/icons/isotone/isotone.svg`, with `isotone-16.svg`, `-24.svg`, `-32.svg` from `scripts/generate-small-icons.py`): the same graphite tile and spectrum band as the app icons, with the three app accents as overlapping lights of radius 45 whose centres sit 25 from (128, 114): Stilus cyan above, Gesso orange lower left, Albumen green lower right. Each overlap is filled with the screen mix of its colors, precomputed, so no renderer needs a blend mode; the centre, where all three meet, is near white. It identifies the suite (the suite installer, the README, the design page), never an app.
- **Wordmark** (`resources/brand/isotone-wordmark-on-dark.svg`, `-on-light.svg`): "isotone" in lowercase Sora SemiBold with the dotless i, its dot replaced by a small Three Lights cluster, over "GRAPHICS SUITE" in Sora Medium tracked 4.5. The letters are outlines, so the files never depend on an installed font; Sora is licensed under the SIL Open Font License 1.1 (`resources/brand/fonts/Sora-OFL.txt`).
- **Lockups** (`resources/brand/isotone-lockup-on-dark.svg`, `-on-light.svg`): the icon at 96 with the wordmark left-aligned 22 to its right, vertically centred. Use the on-dark file on dark grounds and the on-light file on light grounds, never recolored.
- **Do not** put the suite icon on an app's window, taskbar entry, or file association, and do not recolor the three lights: their order and colors are the three apps.

## The Suite card splash

The splash shows the master icon at 136 px on a graphite card (640 x 360, radius 8, the same family of greys as the tile), over a soft halo of the app accent, beside the app name, its role, the suite and version line, a live status line and the launch progress in the accent, with the spectrum band as a gentle wave along the card's bottom edge (the same seven stops as the icons). The card is identical in the three apps apart from the icon, the accent and the words. `<app>-splash.svg` is its reference design and a marketing image; the app draws the card in XAML so the version, status and progress are live. The full spec (layout grid, colors, text styles, progress, band, glow and timing) is the Splash component guide, summarized in the Shell layout's Splash and Home.

## Do and do not

- Do use the file the ladder names for the rendered size.
- Do keep clear space around the icon of at least one eighth of its size (the 8 px margin of the master) on every side.
- Do place the icon as is on any theme's `frame` or `surface-panel`: the graphite tile carries its own contrast.
- Do not recolor a glyph, tint it with the Highlight color, or swap one app's accent for another's.
- Do not draw the master below 48 px: its band crest and highlight turn to mush; use the small variants.
- Do not add text, a version number or a badge to the tile.
- Do not drop or reorder the spectrum band, or change its colors per app.
- Do not use a catalog icon (`pen-tool`, `brush`, `aperture`) as a stand-in for an app icon.
- Do not use the Suite card splash as an app icon, or ship its SVG or a PNG of it as the in-app splash: the app builds the card in XAML so its text is live.

## Export

PNG sizes and each app's multi-resolution `.ico` (16, 20, 24, 30, 32, 40, 48, 64, 128 and 256) are generated from these SVGs by the icon export script, each size taken from the file the ladder names.

Never hand-edit an exported PNG or `.ico`: change the SVG and export again.

The export also renders each `<app>-splash.svg` at 640 x 360, 960 x 540 and 1280 x 720 (1x, 1.5x and 2x) for marketing only; the apps never load them.

Source files: `resources/icons/<app>/<app>.svg` (master), `<app>-16.svg`, `<app>-24.svg`, `<app>-32.svg` and `<app>-splash.svg` (the Suite card reference design), the same fifteen files as the App icons asset group.
