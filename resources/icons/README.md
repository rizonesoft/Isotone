# App Icons

The icons of the three Photon apps: Nodus, Imago, and Lumen. The design is Direction C, "Suite tile" (operator decision 2026-09-27, "C it is"): one shared graphite rounded tile with a spectrum band at its foot, and a bold glyph in the app's accent color above the band. Direction A, neon line art on a dark tile, is kept as each app's splash and marketing art.

| App | Glyph | Accent |
| --- | ----- | ------ |
| Nodus | A pen nib with a Bezier handle | Cyan `#29C5E6` |
| Imago | A paintbrush with pixel squares | Orange `#F5923E` |
| Lumen | A camera aperture inside viewfinder brackets | Green `#4CC47A` |

The accents are the ones `standards/shared.md` names for each app.

## Files per app

Each app has one folder, `resources/icons/<app>/`, where `<app>` is `nodus`, `imago`, or `lumen`.

| File | Used for |
| ---- | -------- |
| `<app>.svg` | The master, drawn on a 256 by 256 grid. It is the source for every size from 48 px up, including 256 and 512. |
| `<app>-16.svg` | Hand-tuned 16 px variant, also the source for 20 px. |
| `<app>-24.svg` | Hand-tuned 24 px variant, also the source for 30 px. |
| `<app>-32.svg` | Hand-tuned 32 px variant, also the source for 36 and 40 px. |
| `<app>-splash.svg` | Direction A neon art, for the splash window, the About dialog, and marketing images. It is not an app icon and is not drawn into the ICO. |

The small variants exist because the master's detail turns to mush below 48 px: each one redraws the tile and the glyph for its own pixel grid instead of scaling the master down.

Raster output (PNG sizes and the multi-resolution `<app>.ico`) is generated from these SVGs, never drawn by hand. The export is planned as `D00 T03 §3`: one committed script renders every size, builds each ICO, and a check re-renders and compares, so a stale raster fails the gates.

## Construction rules

- Master: `viewBox="0 0 256 256"`. The tile is a rounded rectangle at x and y 8 to 248 (240 by 240) with `rx="48"`, filled with a top-to-bottom graphite gradient (`#34353B` to `#1E1F23`), with a faint inner stroke.
- The spectrum band sits at the foot of the tile, clipped by the tile's rounded corners, running red, orange, yellow, green, cyan, blue, violet from left to right. It is identical in all three apps, so the icons read as one family.
- The glyph sits in the box above the band, centered horizontally, drawn in the app accent with a lighter tint of it for highlights and white for handles and details. It is enlarged for the 48 to 256 px sizes, so it fills most of the space above the band.
- Small variants (16, 24, 32) use a flat tile (`#2B2C31`) with a smaller corner radius: the full 16 by 16 square with `rx="3"`, then 1 to 23 with `rx="4"`, and 1 to 31 with `rx="6"`. The band is 2, 2.5, and 3.5 px tall, and the glyph is simplified. They are aligned to the pixel grid: tile edges and most glyph edges land on whole pixels, so they render crisp instead of blurred.
- Every gradient and clip-path id is prefixed with the app and the direction, plus the size on small variants (`nodus-c-spec`, `nodus-c-s16-spec`, `nodus-a-glow`), so the files can be inlined together in one document without id collisions.
- Colors are literal hex values. The SVGs use no text, fonts, or external references, and only the splash art uses filters.

## License

Every file in this folder was created for the Photon project on 2026-09-27 and is licensed under GPL-3.0, with the rest of the repository (see `LICENSE`). No third-party art, stock illustration, or font is used in any of them, so no attribution is owed.

## Old files and their status

- `nodus/nodus.ico` and `nodus/PNG/nodus_{16,24,32,48,64,72,128,256,512}.png` are the old Nodus design, from before the Direction C decision. They stay until the export in `D00 T03 §3` regenerates them from the new SVGs, because `installer/Nodus.iss` and `installer/Suite.iss` reference `nodus/nodus.ico`. The export overwrites them in place under the same names.
- `nodus/nodus.svg` was the old Nodus master and now holds the Direction C master.
- `imago/imago.ico` and `lumen/lumen.ico` do not exist yet; `installer/Imago.iss` and `installer/Lumen.iss` already point at those paths, and `D00 T03 §3` creates both.
- `nodus_512.png`, `art-and-design.png`, and `lens.png`, the earlier candidate art in this folder, were removed on 2026-09-27: the project-created icons above supersede them.
