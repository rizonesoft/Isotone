# App Icons

The icons of the three Isotone apps: Stilus, Gesso, and Albumen. The design is Direction C, "Suite tile" (operator decision 2026-09-27, "C it is"): one shared graphite rounded tile with a spectrum band at its foot, and a bold glyph in the app's accent color above the band. The splash is the Suite card (operator decision 2026-09-27): a 640 by 360 graphite card carrying the master icon, the app name and the live startup status, with the spectrum band as a wave along its bottom edge. Direction A, the earlier neon line art, is retired and is no longer in the repository.

| App | Glyph | Accent |
| --- | ----- | ------ |
| Stilus | A pen nib with a Bezier handle | Cyan `#29C5E6` |
| Gesso | A paintbrush with pixel squares | Orange `#F5923E` |
| Albumen | A camera aperture inside viewfinder brackets | Green `#4CC47A` |
| Isotone (the suite) | Three Lights: the three app colors as overlapping lights, mixed by the screen formula | All three |

The accents are the ones `standards/shared.md` names for each app.

## Files per app

Each app has one folder, `resources/icons/<app>/`, where `<app>` is `stilus`, `gesso`, or `albumen`.

| File | Used for |
| ---- | -------- |
| `<app>.svg` | The master, drawn on a 256 by 256 grid. It is the source for every size from 48 px up, including 256 and 512. |
| `<app>-16.svg` | Hand-tuned 16 px variant, also the source for 20 px. |
| `<app>-24.svg` | Hand-tuned 24 px variant, also the source for 30 px. |
| `<app>-32.svg` | Hand-tuned 32 px variant, also the source for 36 and 40 px. |
| `<app>-splash.svg` | The Suite card splash, 640 by 360: the reference design for the splash window, which the app builds in XAML to the spec in `docs/design/components/Splash/README.md` so its version, status, and progress are live, and a marketing image. It is not an app icon, is not drawn into the ICO, and the app never loads it. |

The small variants exist because the master's detail turns to mush below 48 px: each one redraws the tile and the glyph for its own pixel grid instead of scaling the master down.

Raster output (PNG sizes and the multi-resolution `<app>.ico`) is generated from these SVGs, never drawn by hand. The export is planned as `D00 T03 §3`: one committed script renders every size, builds each ICO, and renders each `<app>-splash.svg` at 640 by 360, 960 by 540, and 1280 by 720 (`PNG/<app>_splash_{640,960,1280}.png`, for marketing only), and a check re-renders and compares, so a stale raster fails the gates.

## Construction rules

- Master: `viewBox="0 0 256 256"`. The tile is a rounded rectangle at x and y 8 to 248 (240 by 240) with `rx="48"`, filled with a top-to-bottom graphite gradient (`#34353B` to `#1E1F23`), with a faint inner stroke.
- The spectrum band sits at the foot of the tile, clipped by the tile's rounded corners, running red, orange, yellow, green, cyan, blue, violet from left to right. It is identical in all three apps, so the icons read as one family.
- The glyph sits in the box above the band, centered horizontally, drawn in the app accent with a lighter tint of it for highlights and white for handles and details. It is enlarged for the 48 to 256 px sizes, so it fills most of the space above the band.
- Small variants (16, 24, 32) carry the main object alone, enlarged: the Stilus nib without curve or nodes, the Gesso brush without pixel squares, the Albumen aperture without viewfinder corners (operator decision 2026-09-27). The tile keeps the graphite gradient with a smaller corner radius (the full 16 by 16 square with `rx="3"`, then 1 to 23 with `rx="4"`, and 1 to 31 with `rx="6"`), and the band is a straight bar 2, 2.5, and 3.5 px tall. They are generated from the masters by `scripts/generate-small-icons.py` (resvg-py and Pillow); regenerate them after changing a master glyph.
- Every gradient and clip-path id is prefixed with the app and the direction, plus the size on small variants (`stilus-c-spec`, `stilus-c-s16-spec`, `stilus-sp-halo`), so the files can be inlined together in one document without id collisions.
- Colors are literal hex values. The icon SVGs use no text, fonts, filters, or external references.
- The splash SVGs (`viewBox="0 0 640 360"`) embed the app's master icon as a nested `<svg>` at 136 px (x 56, y 92) and set their text in Segoe UI Variable Display and Text, so a faithful render needs those fonts (installed on Windows 11). Their own ids are prefixed `<app>-sp-` (`stilus-sp-bg`, `stilus-sp-halo`, `stilus-sp-spec`); the nested icon keeps the master's ids, identical definitions, so a splash can be inlined beside its master. They use no filters.

## License

Every file in this folder was created for the Isotone project on 2026-09-27 and is licensed under GPL-3.0, with the rest of the repository (see `LICENSE`). No third-party art, stock illustration, or font is used in any of them, so no attribution is owed.

Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. Rizonesoft is a brand of Rizonetech (Pty) Ltd. The GPL covers the files as artwork; the app icons also identify the official apps and are trademarks of Rizonetech (Pty) Ltd, so a modified version you distribute uses its own icons (see [`TRADEMARKS.md`](../../TRADEMARKS.md)).

## Old files and their status

- `stilus/stilus.ico` and `stilus/PNG/stilus_{16,24,32,48,64,72,128,256,512}.png` are the old Stilus design, from before the Direction C decision. They stay until the export in `D00 T03 §3` regenerates them from the new SVGs, because `installer/Stilus.iss` and `installer/Suite.iss` reference `stilus/stilus.ico`. The export overwrites them in place under the same names.
- `stilus/stilus.svg` was the old Stilus master and now holds the Direction C master.
- `gesso/gesso.ico` and `albumen/albumen.ico` do not exist yet; `installer/Gesso.iss` and `installer/Albumen.iss` already point at those paths, and `D00 T03 §3` creates both.
- `stilus_512.png`, `art-and-design.png`, and `lens.png`, the earlier candidate art in this folder, were removed on 2026-09-27: the project-created icons above supersede them.
