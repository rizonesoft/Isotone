# App icons

Stilus, Gesso and Albumen, and the three planned apps Tinctura, Capio and Folium, share one app icon system: Direction C, the suite tile, chosen on 2026-09-27, with the Solid glyphs chosen on 2026-10-23 (operator decision: concept 2 of five, then refined: the Stilus handles removed and the curve enlarged and weighted, the brush given less material and lighter bristles and enlarged, the lens enlarged, and the stroke dropped from Gesso below 40 px). The splash is the Suite card (operator decision 2026-09-27), a 640 x 360 graphite card that carries the master icon; its spec is the Splash component guide. Direction A, the neon art, is retired and no longer in the repository.

The app icons are separate from the UI icon catalog: catalog icons are Lucide-style strokes that draw commands and tools in the chrome, while app icons are full-color files that identify an app to Windows and to the person using it.

## Family concept

Every icon is built from three layers, and each layer has one job.

- **Graphite tile.** The same dark rounded square for every app, so the three read as one suite in a taskbar or a Start menu folder.
- **Spectrum band.** A wave of the seven suite colors along the foot of the tile: the Isotone signature, identical in every app.
- **Accent glyph.** The app's own object in its accent color, drawn as a two-tone solid lit from the top left, with no cast shadow or glare: for Stilus a Bezier curve between two square anchor points, as a vector editor draws a path (`accent-stilus` cyan); for Gesso a paintbrush laying down a tapered stroke (`accent-gesso` orange); for Albumen a six-blade iris inside its lens rim (`accent-albumen` green). A pen nib was retired for Stilus because it says writing, not vector; the path itself is what vector work is.

The glyph is the only thing that changes between apps; the tile and band never do.

## Construction (master, 256 viewBox)

| Part | Geometry |
| --- | --- |
| Canvas | 256 x 256 viewBox, 8 px transparent margin on every side |
| Tile | `rect` x 8, y 8, 240 x 240 (8 to 248), `rx` 52, vertical gradient #3D3E45 to #18191D |
| Inner highlight | `rect` x 9, y 9, 238 x 238, `rx` 51, white stroke 2 at 12 percent opacity (reads as a 1 px inner edge) |
| Spectrum band | path `M0 230C64 220 120 240 176 230S236 218 256 222V256H0Z`, clipped to the tile, horizontal gradient from x 8 to 248 |
| Band crest | the same curve as a stroke, white 2 px at 35 percent opacity |
| Glyph safe box | about x 36 to 220, y 28 to 204, centred at (128, 116), above the band |

The glyph is centred at (128, 116), not at the tile centre, so it sits optically in the middle of the graphite area above the band.

Optical balancing makes the three glyphs look the same size and weight although their shapes differ: each is grown about (128, 116), Stilus by 1.2, Gesso by 1.12 and Albumen by 1.22, and the Stilus curve is drawn heavier (an 18.5 unit body under an 11.5 unit face) because a line reads lighter than a brush or a disc.

| Glyph | Geometry (256 space, before the growth) |
| --- | --- |
| Stilus | the curve `M68 168C82 92 174 140 188 64` as a #127EA0 body, a #29C5E6 face offset (-1, -2) and a #C7F4FC highlight offset (-3, -5); two 22 unit square anchors at its ends, white #F2F3F5 with a 4 unit #29C5E6 edge, corner radius 3 |
| Gesso | a brush at `translate(124 112) rotate(45)`: handle two-tone #F5923E and #D9741F, ferrule two-tone #E3E6EA and #AEB4BD with one #7D838D crimp, bristles from #B8763E through #E88A3A to a #FFC861 tip; a tapered stroke from the tip, #E0701C through #F5923E to #FFD15A, with one white gloss line at 40 percent |
| Albumen | a lens rim of radius 66 (#6A707A to #25272C), a black well of radius 56, six blades alternating #5FD58C and #38AE64 that extend the sides of a radius 22 hexagon opening (#0B2414) to the well, so they tile it exactly; a glint arc and a rim edge in white |
| Tinctura (planned) | a ring of twelve hue segments between radii 48 and 76, one every 30 degrees from red at the top (HSL lightness 0.6, saturation 0.85), 1.2 degrees of tile between neighbours; nothing in the centre (grown by 1.05) |
| Capio (planned) | four crop corners, 44 unit arms and a 16 unit stroke in two-tone red (#FF4D6D and #C9264A), framing x 52 to 204 and y 42 to 190; a white #F2F3F5 crosshair at the centre: a radius 24 ring and four ticks, 7 units |
| Folium (planned) | a page (x 64 to 194, y 36 to 196) in two-tone white with a folded corner; a blue header bar, a crossed placeholder graphic frame (#A3B5FF, edged #3550D6), and two columns of #8A93A6 text lines |

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

At taskbar and title-bar sizes an icon is recognized by its silhouette, so below 40 px each app shows its simplified glyph, enlarged to fill the space above the band (operator decisions 2026-09-27, less detail at 32, 24 and 16, and 2026-10-23, no stroke on Gesso below 40 px).

- Stilus: the curve and its two anchors, heavier (a 25 unit body, 32 unit anchors with a 6 unit edge), without the highlight.
- Gesso: the paintbrush alone, without the stroke or the crimp line; the light ferrule stays, since it is what makes the shape read as a brush.
- Albumen: the rim, the blades and the opening, without the glints.
- Tinctura: the hue ring with 3 degrees between segments, so the colors stay apart.
- Capio: the corners at a 22 unit stroke and the crosshair at 10.
- Folium: the page, the header, the frame, and three heavy lines in place of the text columns.
- The glyph is scaled to fill a box inset from the tile (1.5 px at 16, 2.6 px at 24, 3.2 px at 32) and centered above the band.
- The tile keeps the master's graphite gradient with a smaller corner radius (3, 4, 6), and the spectrum band is a straight bar 2, 2.5, and 3.5 px tall, clipped to the tile corners; the inner highlight and the band crest are dropped.
- The masters, the variants and the icon inside each `<app>-splash.svg` are written by `scripts/build-app-icons.py` from one geometry, so a change to a glyph carries through every size; edit the script, never the SVGs, and `python scripts/build-app-icons.py --check` fails when a committed file differs from what it writes. The suite icon's variants come from `scripts/generate-small-icons.py`.
- Accent colors stay the same hex values as the master, so an icon reads as the same app at every size.

## Colors

| Role | Values |
| --- | --- |
| Tile (every size) | vertical gradient #3D3E45 (top) to #18191D (bottom) |
| Spectrum band | stops at 0, 0.17, 0.33, 0.5, 0.67, 0.83 and 1: #FF4D6D, #FF9A3C, #FFD84A, #4CC47A, #29C5E6, #5B7CFF, #B45CFF |
| Stilus glyph | `accent-stilus` #29C5E6 face, #127EA0 body, #C7F4FC highlight, anchors #F2F3F5 edged in #29C5E6 |
| Gesso glyph | `accent-gesso` #F5923E and #D9741F handle, #E3E6EA and #AEB4BD ferrule, bristles #B8763E to #FFC861, stroke #E0701C to #FFD15A |
| Albumen glyph | `accent-albumen` family: blades #5FD58C and #38AE64, opening #0B2414, rim #6A707A to #25272C |

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
- **Wordmark** (`resources/brand/isotone-wordmark-on-dark.svg`, `-on-light.svg`): "isotone" in lowercase Sora SemiBold with the dotless i, its dot a single circle filled with the three app colors blended in color-wheel order (orange, green, cyan, lower left to upper right, so no step of the blend turns grey), placed where the operator approved it (radius 6.56, 10 right of the stem centre, 41 above the baseline, at a 58 font size), over "GRAPHICS SUITE" in Sora Medium tracked 4.5. The letters are outlines, so the files never depend on an installed font; the font itself is in `resources/brand/fonts/` (SIL Open Font License 1.1).
- **The wordmark stands alone:** it is never locked up with the suite icon (operator decision 2026-09-28). The icon has its own places (the suite installer, the design page, social images), and each is used on its own.
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
