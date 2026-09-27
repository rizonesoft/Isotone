---
schema_version: 1
id: repo-layout
domain: 00-workspace
status: draft
title: "TODO-03 -- Repository Layout, Visual Baselines, and App Icon Export"
depends_on: []
track: W3
---

# TODO-03 -- Repository Layout, Visual Baselines, and App Icon Export

> **Goal:** Nothing in the tree is a leftover of the imports: each app's documentation lives under `docs/`, sample files sit with the test fixtures, empty folders are gone, both imported apps have committed captures of their current surfaces as a before record of the legacy look (never a fidelity source: the design in `docs/design/` is, under `standards/design-contract.md`), and every raster app icon (PNG sizes and the multi-resolution ICO of Nodus, Imago, and Lumen) is generated from the committed SVG sources by one script whose check fails the gates when a raster drifts from its source.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The imports brought their own documentation folders: `src/Nodus/docs/` (a `README.md` indexing mostly missing pages, `components/vector-icon.md`, `ui/status-bar.md`) and `src/Imago/docs/` (five `README.md` stubs under `api/`, `architecture/`, `plugins/`, `user-guide/`). Two loose SVG files sit at `src/Nodus/test.svg` and `src/Nodus/bezier-sample.svg`. `src/Imago/.github/` is an empty directory left after the per-app workflows were removed. There is no `docs/captures/` folder, so a `Fidelity:` block that names one cannot be satisfied and `process-todo-section` would refuse every UI section.
<!-- claim: exists src/Nodus/docs/README.md -->
<!-- claim: exists src/Imago/docs/README.md -->
<!-- claim: exists src/Nodus/bezier-sample.svg -->
<!-- claim: exists src/Nodus/test.svg -->
<!-- claim: absent docs/captures -->
>
> **Corrected 2026-09-27:** the operator chose the app icon design that day (Direction C, "Suite tile": "C it is"), and its SVG sources are committed under `resources/icons/<app>/` (`<app>.svg` master for 48 px and up, hand-tuned `<app>-16.svg`, `-24.svg`, `-32.svg`, and `<app>-splash.svg`, which since the operator's second decision that day is the Suite card splash, a 640 by 360 reference design and marketing image that the apps rebuild in XAML), recorded with their construction rules and license in `resources/icons/README.md`. No raster is generated from them yet: `resources/icons/nodus/nodus.ico` and `resources/icons/nodus/PNG/` are still the old Nodus design, which `installer/Nodus.iss` and `installer/Suite.iss` reference, and `resources/icons/imago/imago.ico` and `resources/icons/lumen/lumen.ico`, which `installer/Imago.iss` and `installer/Lumen.iss` point at, do not exist. There is no export script. §3 closes that gap.
<!-- claim: exists resources/icons/README.md -->
<!-- claim: exists resources/icons/nodus/nodus.svg -->
<!-- claim: exists resources/icons/imago/imago-16.svg -->
<!-- claim: exists resources/icons/lumen/lumen-splash.svg -->
<!-- claim: exists resources/icons/nodus/nodus.ico -->
<!-- claim: absent resources/icons/imago/imago.ico -->
<!-- claim: absent resources/icons/lumen/lumen.ico -->
<!-- claim: absent scripts/export-icons.py -->

## Inputs

- [`docs/README.md`](../../docs/README.md), [`docs/dev/README.md`](../../docs/dev/README.md) -- the documentation indexes §1 links the moved pages from
- [`.claude/skills/process-todo-section/gates.md`](../../.claude/skills/process-todo-section/gates.md) -- the launch smoke §2 follows
- [`standards/ui.md`](../../standards/ui.md) and [`docs/design/`](../../docs/design/README.md) -- the design contract the captures illustrate (**Corrected 2026-09-27:** said `standards/shared.md`, which now points here)
- [`resources/icons/README.md`](../../resources/icons/README.md) -- the icon set, which SVG feeds which size, the construction rules, and the license §3 exports from
- [`installer/common.iss`](../../installer/common.iss) -- `SetupIconFile` falls back to the Inno Setup icon with a `WARNING: icon ... not found` message when `AppIcon` is absent, which §3's checkpoint reads
- resvg (https://github.com/linebender/resvg, Apache-2.0 or MIT) through resvg-py 0.5.0 (https://pypi.org/project/resvg-py/, MPL-2.0), and Pillow 12.3.0 (https://pillow.readthedocs.io/, MIT-CMU) with its ICO writer (`IcoImagePlugin`, `sizes` and `append_images`) -- the renderer and the ICO writer §3 pins
- -> XREF: D02 T01 §1 -- the Nodus rename consumes §3's `nodus.ico` and `PNG/nodus_32.png`
- -> XREF: D03 T01 §4 -- the Imago icon consumes §3's `imago.ico` and `PNG/imago_32.png`
- -> XREF: D04 T01 §2 -- the Lumen app consumes §3's `lumen.ico` and PNGs
- -> XREF: D01 T01 §2 -- the shared Suite card splash window consumes §3's app icon PNG and compares its capture against §3's splash reference render
- -> XREF: D02 T02 §2 -- the Nodus Suite card splash consumes §3's `nodus_256.png` instead of SharpVectors and compares its capture against §3's splash reference render
- -> XREF: D99 T01 §4 -- the icon license row, answered by the project-created icons §3 exports

## Outcome

- `src/Nodus/` and `src/Imago/` hold only projects and build overlays; their documentation lives under `docs/dev/nodus/` and `docs/dev/imago/`.
- The two sample SVG files are committed fixtures under `tests/fixtures/nodus/svg/` with a README naming their source.
- `docs/captures/nodus/main-window/` and `docs/captures/imago/main-window/` hold dated before captures of each app's imported main window at 100 and 150 percent scaling, with a `README.md` recording the commit and machine and saying the captures are a before record, not a fidelity source.
- `python scripts/export-icons.py` regenerates `resources/icons/<app>/PNG/` and `resources/icons/<app>/<app>.ico` for Nodus, Imago, and Lumen from the committed SVGs, and `python scripts/export-icons.py --check` fails CI and `scripts/check-all.ps1` when a committed raster differs from what the sources render.

**Adjacency:** all=not-applicable (moving files, recording baselines, and generating icon rasters at build time: no records, settings, or documents a user changes)

**Adjacency rationale:** The captures are evidence for reviewers, not a product surface; the sections that change those surfaces own their adjacency.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On | Status |
| :---: | :-----: | ---------------------------------------------------- | ---------- | :----: |
|   1   |   §1    | Fold the per-app docs and samples into the suite     | --         |  [ ]   |
|   2   |   §2    | Before captures of the imported Nodus and Imago      | --         |  [ ]   |
|   3   |   §3    | Export the app icon rasters from the SVG sources     | D00 T01 §5, D00 T02 §5 |  [ ]   |

---

## 1. Fold the Per-App Docs and Samples into the Suite

The suite has one documentation tree (`docs/dev/`, `docs/user/`) and one fixture tree. Pages left inside `src/` are invisible to anyone reading `docs/`, and sample files beside the projects look like build inputs. Only pages with real content move; index stubs that link to pages that never existed are deleted.

- [ ] Move `src/Nodus/docs/components/vector-icon.md` and `src/Nodus/docs/ui/status-bar.md` to `docs/dev/nodus/`, fixing every relative link inside them. Done when: both files open from `docs/dev/nodus/` with no dead link (checked by following each one).
- [ ] Delete `src/Nodus/docs/README.md` (it indexes `core/`, `elements/`, and tutorial pages that do not exist). Done when: `src/Nodus/docs/` no longer exists.
- [ ] Read the five `src/Imago/docs/**/README.md` files; move any with content beyond a heading and a list of missing links to `docs/dev/imago/`, delete the rest. Done when: `src/Imago/docs/` no longer exists and the commit body lists each file's fate.
- [ ] Move `src/Nodus/test.svg` and `src/Nodus/bezier-sample.svg` to `tests/fixtures/nodus/svg/` and add `tests/fixtures/nodus/svg/README.md` naming their origin (the Bezier repository) and license (GPL-3.0, this repository's). Done when: `git ls-files tests/fixtures/nodus/svg` lists three files.
- [ ] Remove the empty `src/Imago/.github/` directory. Done when: `Test-Path src/Imago/.github` prints `False`.
- [ ] List the moved pages in `docs/dev/README.md` (a "Per-app notes" line per app). Done when: each moved page is linked once from that index.
- [ ] Commit: `"docs: fold per-app docs and samples into the suite layout"`

**Test checkpoint:** `Get-ChildItem src/Nodus, src/Imago -Directory -Recurse | Where-Object Name -in 'docs','.github'` returns nothing; every relative link in `docs/dev/nodus/*.md` and `docs/dev/imago/*.md` resolves to an existing file (a PowerShell loop over the links with `Test-Path`, quoted); `dotnet build Photon.slnx -c Release` still exits 0. Cheaper substitute that fails: copying the pages and leaving the originals, which leaves two copies to drift.

## 2. Before Captures of Nodus and Imago

**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: pixel perfect is "Exact tokens + ±1 DIP geometry + approved goldens", signed off by the review panel) makes `docs/design/` the only fidelity source and the review-approved goldens under `docs/captures/golden/` the regression reference. This section said: every UI section's `Fidelity:` block names a capture under `docs/captures/<app>/`, `process-todo-section` refuses to build a surface whose capture does not exist, and these captures are the starting line the next changes are reviewed against; its Fidelity line named the two main windows as the baseline and its Job line named `review-todo-section` comparing against the capture. The captures are now a before record of the legacy look only: they show a reviewer what a section changed, and no section is built or reviewed to match them.

The imported apps have no captures yet, so this section records their surfaces exactly as they are today, before `Photon.UI` and the design system replace them.

**Fidelity:** no surface of its own -- this section records the imported windows as a before record under `docs/captures/nodus/main-window/` and `docs/captures/imago/main-window/`; it builds or changes no surface, and the design in `docs/design/` (`standards/design-contract.md`) is the fidelity source for the sections that do.
**Job:** a reviewer can see how a legacy surface looked before a section changed it. Consumer: the before-and-after notes of `D01 T01 §1`, `D01 T01 §3`, and `D01 T01 §7`, never a fidelity comparison.
**Treatment:** full-window PNG captures of each app's main window with an empty document, at 100 and 150 percent display scaling, plus one with a sample document open. Cheaper substitute that fails the checkpoint: the marketing screenshots under `resources/screens/`, which are not captures of the built app.
**Chrome:** consume the existing windows unchanged. Do not restyle anything in this section.

**Requires:** display-session -- capturing a rendered WPF window needs an interactive desktop session

- [ ] Build Debug (`dotnet build Photon.slnx -c Debug`) and launch `Bezier.Desktop.exe` from `artifacts/bin/Bezier.Desktop/debug/`; capture the main window with no document to `docs/captures/nodus/main-window/empty-100.png`. Done when: the PNG shows the menu, tool rail, canvas, panels, and status strip.
- [ ] Open `tests/fixtures/nodus/svg/bezier-sample.svg` (or `src/Nodus/bezier-sample.svg` if §1 has not shipped) and capture `docs/captures/nodus/main-window/sample-100.png`. Done when: the drawing is visible on the canvas in the capture.
- [ ] Repeat the empty capture at 150 percent scaling as `empty-150.png`. Done when: the file exists and its pixel width is about 1.5 times the 100 percent capture for the same window size.
- [ ] Launch `Imago.exe` from `artifacts/bin/Imago.UI/debug/` and capture `docs/captures/imago/main-window/empty-100.png` and `empty-150.png`. Done when: both files exist.
- [ ] Write `docs/captures/README.md` (folder per app, then per surface; file names `<state>-<scale>.png`; each surface folder's `README.md` records the commit, date, Windows build, and scaling; the per-app folders are before records of the imported apps and never a fidelity source, while `docs/captures/golden/` holds the review-approved goldens of `standards/design-contract.md`) and one `README.md` per surface folder. Done when: both surface folders carry their record and `docs/captures/README.md` names `standards/design-contract.md` (**Corrected 2026-09-27:** the before-record and golden sentences added).
- [ ] Quote the Serilog error count for the Imago run (`%LOCALAPPDATA%\Imago\logs\`) and the debug-log state for Nodus (it has no file log yet, `D02 T01 §3`). Done when: both are in the commit body.
- [ ] Commit: `"docs: record baseline captures of Nodus and Imago"`

**Test checkpoint:** `Get-ChildItem docs/captures -Recurse -Filter *.png` lists at least five captures, each non-empty and a valid PNG (its first eight bytes are the PNG signature, checked with `Format-Hex`); each surface folder's `README.md` names the commit the captures were taken at. Cheaper substitute that fails: copying `resources/screens/nodus.png`, which the commit record would not match.

## 3. Export the App Icon Rasters from the SVG Sources

The app icons are SVG sources (operator decision 2026-09-27, Direction C, recorded in `resources/icons/README.md`), but Windows and the apps consume rasters: `ApplicationIcon` and Inno Setup's `SetupIconFile` take an `.ico`, and WPF window icons and the splash's app icon take PNGs. Hand-exported rasters drift from their sources without anyone noticing, so this section commits one script that renders every raster, and a check that re-renders and compares. It runs in Phase 1 because the renames there set each app's icon: `D02 T01 §1` (Nodus) and `D03 T01 §4` (Imago), then later `D04 T01 §2` (Lumen) and the splash sections `D01 T01 §2` and `D02 T02 §2`, take their files from here and source no icon art of their own. The old Nodus rasters (`nodus/nodus.ico`, `nodus/PNG/*`) are overwritten in place under the same names, so the installers' `AppIcon` paths stay valid.

**Fidelity:** no surface of its own -- the rasters are files; the surfaces that show them (Explorer, title bars, the splash, the installers) are wired by `D02 T01 §1`, `D03 T01 §4`, `D04 T01 §2`, and `D01 T01 §2`.

**Needs:** Windows host (build/test)

**Corrected 2026-09-27:** the splash renders changed with the operator's Suite card decision that day. The section said: render each `<app>-splash.svg` (then the Direction A neon art, square) to `PNG/<app>_splash_256.png` and `<app>_splash_512.png` for the splash window. The splash is now the Suite card, 640 by 360, built in XAML to `docs/design/components/Splash/README.md` from the app icon PNG plus live text, so the splash renders are 640, 960, and 1280 px wide, marketing only and the capture reference; the per-app PNG count rises from 18 to 19.

Source map, one rule for all three apps (from `resources/icons/README.md`): 16 and 20 px render from `<app>-16.svg`; 24 and 30 px from `<app>-24.svg`; 32, 36, and 40 px from `<app>-32.svg`; 48, 60, 64, 72, 80, 96, 128, 256, and 512 px from the `<app>.svg` master. Every size renders directly from its SVG at its own pixel size, never by resampling another raster.

- [ ] Add `scripts/requirements-icons.txt` pinning `resvg-py==0.5.0` and `Pillow==12.3.0`, with one comment line per package naming its license (resvg-py MPL-2.0 over resvg Apache-2.0 or MIT; Pillow MIT-CMU), and record the decision in `docs/dev/decisions.md` (question: a GPL-compatible SVG renderer for build-time icon export; options: resvg-py, CairoSVG (LGPL-3.0, needs a native Cairo on Windows), the Inkscape CLI (GPL-2.0 or later, a large install), ImageMagick (delegates SVG to librsvg or its own MSVG renderer); evidence: resvg-py rendered the SVGs in `resources/icons/` on 2026-09-27 with no native install; cost of change: one render function). The packages are build-time tools and never ship in an app. Done when: `python -m pip install -r scripts/requirements-icons.txt` in a fresh `python -m venv build/icons-venv` exits 0 (quoted) and the decision entry exists.
- [ ] Add `scripts/export-icons.py` with the source map above as one table (`SIZES = {16: "16", 20: "16", 24: "24", 30: "24", 32: "32", 36: "32", 40: "32", 48: "master", ...}`), rendering each size with `resvg_py.svg_to_bytes(svg_path=..., width=n, height=n)` and writing `resources/icons/<app>/PNG/<app>_<n>.png` through Pillow as 8-bit RGBA with no text or time chunks. Done when: `python scripts/export-icons.py` writes 16 PNGs per app, and a Pillow read of each reports `(n, n)` and mode `RGBA` (quoted for Imago).
- [ ] Render each `<app>-splash.svg` (the Suite card, `viewBox="0 0 640 360"`) at 640 by 360, 960 by 540, and 1280 by 720 (1x, 1.5x, 2x) to `resources/icons/<app>/PNG/<app>_splash_640.png`, `<app>_splash_960.png`, and `<app>_splash_1280.png` in the same run, for marketing images and as the reference the splash captures of `D02 T02 §2` and `D01 T01 §2` are compared against; no app loads them. The SVGs set their text in Segoe UI Variable Display and Text, so the export refuses to write splash PNGs on a host without those fonts, and `--check` skips the nine splash files there with a warning naming the missing font rather than failing (a CI runner may lack them). Done when: nine splash PNGs exist and each reads back at its size (`(640, 360)`, `(960, 540)`, `(1280, 720)`, quoted for Lumen).
- [ ] Write `resources/icons/<app>/<app>.ico` with eight PNG-compressed entries at 16, 20, 24, 32, 40, 48, 64, and 256 px, in that order, each entry the exact frame the script rendered for that size (Pillow `save(format="ICO", sizes=..., append_images=...)`, or the ICONDIR written directly if Pillow resamples an entry). Done when: a header read of each ICO (the ICONDIR count, then each ICONDIRENTRY's width, height, and data starting with the PNG signature) lists the eight sizes, and each entry's decoded pixels equal the committed `PNG/<app>_<n>.png` (quoted for all three apps).
- [ ] Add `--check` to `scripts/export-icons.py`: render everything into memory and compare against the committed files by decoded pixels (exact equality, so a zlib or encoder difference between machines cannot fail it) and by ICO entry list, and fail on a file under `resources/icons/<app>/PNG/` the script does not produce. Exit 1 naming each differing, missing, or stray file. Done when: `--check` exits 0 on a fresh export, and exits 1 naming the file after one pixel of `imago_48.png` is changed (negative probe quoted, then reverted).
- [ ] Run the export for all three apps: it overwrites `resources/icons/nodus/nodus.ico` and every `resources/icons/nodus/PNG/nodus_*.png` in place with the Direction C design, and creates `resources/icons/imago/imago.ico`, `resources/icons/imago/PNG/`, `resources/icons/lumen/lumen.ico`, and `resources/icons/lumen/PNG/`. Done when: `git ls-files resources/icons | Select-String "\.(png|ico)$"` lists 60 files (19 PNGs and one ICO per app) and `--check` exits 0.
- [ ] Remove the `PLACEHOLDER` comment from `installer/Imago.iss` (the ICO it names now exists) and leave every `AppIcon` path as it is. Done when: `Select-String PLACEHOLDER installer/Imago.iss` prints nothing, and `pwsh scripts/package.ps1 -App Nodus` and `-App Imago` print no `icon ... not found` warning from `installer/common.iss` (quoted).
- [ ] Add a step to the `build-windows` job of `.github/workflows/build.yml` that installs `scripts/requirements-icons.txt` and runs `python scripts/export-icons.py --check`. Done when: the first CI run after the commit shows the step green (run URL quoted).
- [ ] Add an `export-icons --check` gate to `scripts/check-all.ps1` beside the plan gates, skipped with a warning naming `scripts/requirements-icons.txt` when `resvg_py` or `PIL` does not import (the pattern the script already uses when python is missing). Done when: `pwsh scripts/check-all.ps1` lists the gate as PASS on a machine with the requirements installed and as SKIP with the warning in a venv without them (both quoted).
- [ ] Update `resources/icons/README.md`: add a "Raster output" table (the PNG sizes and the source of each, the three splash renders and their marketing-only use, the ICO entries, and the two commands) and rewrite "Old files and their status" to say the old Nodus rasters were regenerated and the Imago and Lumen ICOs exist. Done when: the README names `scripts/export-icons.py` and lists no raster as pending.
- [ ] Add an "App icons" paragraph to `docs/dev/build.md` (edit the SVG, run `python scripts/export-icons.py`, commit the SVG and the rasters together; CI runs `--check`) and rewrite its Imago icon bullet to say the ICO exists and only the executable wiring is left to `D03 T01 §4`. Done when: `Select-String "export-icons" docs/dev/build.md` finds the paragraph.
- [ ] Rewrite every `todo/` claim and sentence this export makes false (the `absent` claims for `imago.ico`, `lumen.ico`, and `scripts/export-icons.py` in this file's Current state, and any other `absent` or old-design statement about `resources/icons/`), then run `python scripts/todo-claims.py`. Done when: it exits 0.
- [ ] Commit: `"workspace: export the app icon rasters from the SVG sources"`

**Test checkpoint:** `python scripts/export-icons.py --check` exits 0 (quoted); the negative probe (one changed pixel in `resources/icons/imago/PNG/imago_48.png`) makes it exit 1 naming that file (quoted); the ICO header read lists 16, 20, 24, 32, 40, 48, 64, and 256 as PNG entries for each of `nodus.ico`, `imago.ico`, and `lumen.ico` (quoted); each `PNG/<app>_splash_{640,960,1280}.png` reads back at 640 by 360, 960 by 540, and 1280 by 720 (quoted for one app); `pwsh scripts/package.ps1 -App Imago` prints no icon warning; the CI `build-windows` run shows the check step green. Cheaper substitute that fails: rasters exported by hand from an editor, which `--check` cannot re-derive, or an ICO whose small entries are resampled from the 256 px frame, which the per-entry pixel comparison against the small-variant renders catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0 after the moves
- [ ] `docs/captures/` exists with a record per surface, and its README says the per-app captures are a before record and `golden/` holds the approved goldens
- [ ] `python scripts/export-icons.py --check` exits 0, and every raster under `resources/icons/` is one it produces
- [ ] `python scripts/todo-graph.py validate` clean
