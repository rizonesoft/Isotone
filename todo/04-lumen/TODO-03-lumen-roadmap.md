---
schema_version: 1
id: lumen-roadmap
domain: 04-lumen
status: draft
title: "TODO-03 -- Lumen Roadmap after 0.1.0"
depends_on: []
track: L3
---

# TODO-03 -- Lumen Roadmap after 0.1.0

> **Goal:** The features that take Lumen from a first release to a daily darkroom, each planned at feature grain and expected to be split by `groom-plan` before it runs: local adjustments, detail (sharpening and noise reduction), lens corrections, color grading, HDR and panorama merge, a GPU pipeline, map and GPS, contact sheets and print, catalog maintenance, and accessibility and localization.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Lumen has no code; its first release is planned in `D04 T01` and `D04 T02`. The removed Lumen notes listed only the 0.1.0 features; this roadmap comes from the competitor table in `D04 T01` (Lightroom Classic and darktable feature sets) and the non-goals that file set aside. None of it is a commitment until groomed.
<!-- claim: absent src/Lumen -->

## Inputs

- `docs/dev/lumen/competitor-survey.md` (from `D04 T01 §1`) -- the competitor features each section answers
- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard and the pipeline rules every section keeps

## Outcome

- Each section ships with its surface, its settings, its log lines, its undo through the edit stack, its user-guide page, and its tests, and none writes an original.

**Adjacency:** list=applicable; document=applicable @ D04 T03 §8; settings=applicable; reporting=applicable; notifications=applicable; permissions=not-applicable (file refusals are owned by import and export in D04 T01 and D04 T02); audit=applicable; exchange=applicable; reverse=applicable

**Adjacency rationale:** Catalog maintenance lists and reports on the library; contact sheets and prints are the carried documents; merges run as long jobs that notify and produce new files beside originals; every develop change stays in the edit stack.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On | Status |
| :---: | :-----: | ---------------------------------------------------- | ---------- | :----: |
|   1   |   §1    | Local adjustments: brush, linear, radial masks       | D04 T02 §8 |  [ ]   |
|   2   |   §2    | Detail: sharpening and noise reduction               | D04 T02 §8 |  [ ]   |
|   3   |   §3    | Lens corrections                                     | D04 T02 §8 |  [ ]   |
|   4   |   §4    | Color grading and HSL                                | D04 T02 §8 |  [ ]   |
|   5   |   §5    | HDR and panorama merge                               | D04 T02 §8 |  [ ]   |
|   6   |   §6    | A GPU develop path with CPU parity                   | §2         |  [ ]   |
|   7   |   §7    | Map and GPS                                          | D04 T02 §8 |  [ ]   |
|   8   |   §8    | Contact sheets and print                             | D04 T02 §8 |  [ ]   |
|   9   |   §9    | Catalog maintenance and library statistics           | D04 T02 §8 |  [ ]   |
|  10   |   §10   | Accessibility and localization                       | D04 T02 §8 |  [ ]   |

---

## 1. Local Adjustments: Brush, Linear, and Radial Masks

Global adjustments are half of developing; the other half is local: dodge a face, darken a sky. -> SOURCE: lumen-roadmap-local

**Fidelity:** Masking panel -- new build, no baseline; captured to docs/captures/lumen/masks/.
**Job:** a photographer can apply exposure, contrast, temperature, saturation, and clarity to a painted, linear, or radial region. Consumer: the edit stack and the pipeline.
**Treatment:** masks stored as vector data (brush strokes as paths with feather, gradients as parameters) in `DevelopSettings`, rasterized at render resolution; a masks panel listing each with its adjustments; overlay toggle (O). Cheaper substitute that fails the checkpoint: masks stored as bitmaps at preview resolution.
**Chrome:** consume the develop module and the edit stack.

**Requires:** display-session -- painting masks needs an interactive desktop

- [ ] Mask model and rasterization at any resolution. Done when: preview and full-resolution renders of a masked edit agree within 1/255 at equal scale.
- [ ] Brush, linear, and radial tools with the masks panel. Done when: captures committed.
- [ ] Commit: `"lumen: local adjustments with brush, linear, and radial masks"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with mask rasterization tests reporting the preview and export agreement. Cheaper substitute that fails: bitmap masks.

## 2. Detail: Sharpening and Noise Reduction

Capture sharpening and noise reduction at high ISO, applied in linear light before the tone stages. -> SOURCE: lumen-roadmap-detail

- [ ] Sharpening (amount, radius, detail, masking) and luminance and color noise reduction as pipeline stages with goldens from darktable (version recorded). Done when: fidelity tests pass within stated tolerances.
- [ ] A 1:1 detail preview in the panel. Done when: a capture is committed.
- [ ] Commit: `"lumen: sharpening and noise reduction"`

**Requires:** display-session -- the detail preview needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the detail goldens. Cheaper substitute that fails: sharpening only at export.

## 3. Lens Corrections

Distortion, vignetting, and chromatic aberration corrected from a lens database, matched from EXIF. -> SOURCE: lumen-roadmap-lens

- [ ] Decide the lens data source (the lensfun database, LGPL-3.0 library and CC-BY-SA data, or another) with licenses checked against GPL-3.0 and recorded. Done when: the decision entry exists.
- [ ] Automatic profile matching and the three corrections as pipeline stages with manual overrides. Done when: a fixture with known distortion straightens a grid to within a stated error.
- [ ] Commit: `"lumen: profile-based lens corrections"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the lens tests reporting the grid error. Cheaper substitute that fails: a manual distortion slider only.

## 4. Color Grading and HSL

Per-hue hue, saturation, and luminance, and three-way color grading for shadows, midtones, and highlights. -> SOURCE: lumen-roadmap-color

**Fidelity:** HSL and Color Grading panels -- new build, no baseline; captured to docs/captures/lumen/color/.
**Job:** a photographer can shift specific colors and tint tonal ranges. Consumer: the pipeline.
**Treatment:** eight hue bands with smooth falloff in a perceptual space (Oklab), and color wheels per tonal range with blending and balance. Cheaper substitute that fails the checkpoint: RGB channel curves only.
**Chrome:** consume the develop module.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] HSL and grading stages with unit tests on known colors. Done when: moving the orange band's hue leaves a blue patch unchanged within 1/255.
- [ ] Commit: `"lumen: HSL and color grading"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the color tests reporting. Cheaper substitute that fails: channel curves.

## 5. HDR and Panorama Merge

Merging brackets into an HDR DNG-like linear file and stitching panoramas, written as new files beside the originals. -> SOURCE: lumen-roadmap-merge

- [ ] HDR merge of aligned brackets into a linear float TIFF with deghosting, as a background job with progress. Done when: a bracket fixture merges with no clipped highlights that any single frame kept.
- [ ] Panorama stitching through a recorded library decision (license checked). Done when: a two-frame fixture stitches.
- [ ] Commit: `"lumen: HDR merge and panorama stitching"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the merge tests reporting; the unchanged-originals assertion holds. Cheaper substitute that fails: merging into an original.

## 6. A GPU Develop Path with CPU Parity

The develop pipeline on the GPU through ComputeSharp for interactive previews at full resolution, matching the CPU path. If Imago's compositing shaders and Lumen's share infrastructure, the shared part moves to `Photon.Core` through `add-todo`. -> SOURCE: lumen-roadmap-gpu

- [ ] GPU implementations of every pipeline stage with parity tests within 1/255, skipping with a reason where no DirectX 12 device exists. Done when: parity is quoted on the development machine.
- [ ] Commit: `"lumen: a GPU develop path with CPU parity"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the parity tests reporting per stage. Cheaper substitute that fails: a GPU path without parity tests.

## 7. Map and GPS

Photos placed on a map from their GPS data, and GPS assigned from a track log, stored in the catalog and sidecars. -> SOURCE: lumen-roadmap-map

**Fidelity:** Map module -- new build, no baseline; captured to docs/captures/lumen/map/.
**Job:** a photographer can find photos by place and geotag photos from a GPX track. Consumer: the catalog and sidecars.
**Treatment:** a map view on a tile source whose terms allow the use (decision recorded), clusters per location, GPX matching by capture time with an offset. Cheaper substitute that fails the checkpoint: a latitude and longitude text field.
**Chrome:** consume the catalog and the sidecar writer.

**Requires:** display-session -- the map view needs an interactive desktop

- [ ] Map view and GPX tagging with tests on time matching. Done when: a fixture track tags three photos correctly.
- [ ] Commit: `"lumen: the map module and GPX geotagging"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the matching tests reporting. Cheaper substitute that fails: manual coordinates only.

## 8. Contact Sheets and Print

Printing photos and contact sheets with layouts, sharpening for paper, and color management. -> SOURCE: lumen-roadmap-print

**Fidelity:** Print module -- new build, no baseline; captured to docs/captures/lumen/print/.
**Job:** a photographer can print single photos and contact sheets. Consumer: the printer.
**Treatment:** layouts (single, grid, contact sheet with captions from metadata), print sharpening, and printer profiles; PDF output through the Windows print path. Cheaper substitute that fails the checkpoint: printing a screenshot.
**Chrome:** consume the export renderer.

**Requires:** display-session -- the print module needs an interactive desktop

- [ ] Layouts and printing to "Microsoft Print to PDF" with captions. Done when: the PDF shows the expected grid and captions.
- [ ] Commit: `"lumen: printing and contact sheets"`

**Test checkpoint:** the printed PDF's layout is quoted (page count, cells per page). Cheaper substitute that fails: screenshots.

## 9. Catalog Maintenance and Library Statistics

A long-lived catalog needs backups, integrity checks, missing-file reconnection, and optimization. -> SOURCE: lumen-roadmap-catalog

- [ ] Scheduled catalog backups (on exit weekly by default, a setting) with retention, and restore. Done when: a restore test reopens a backup.
- [ ] Integrity check and optimize (SQLite `integrity_check`, `VACUUM`). Done when: a corrupted fixture is detected and reported.
- [ ] Find missing photos and reconnect a moved root folder. Done when: a test moves a fixture folder and reconnects it.
- [ ] Commit: `"lumen: catalog backup, integrity, and reconnection"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the maintenance tests reporting. Cheaper substitute that fails: no backups.

## 10. Accessibility and Localization

Every Lumen surface keyboard- and screen-reader-operable and translatable. -> SOURCE: lumen-roadmap-a11y

- [ ] Accessibility Insights audit (version quoted) with every failure fixed. Done when: the committed report shows none.
- [ ] Strings in `.resx` with a pseudo-locale build. Done when: the capture shows no untransformed string.
- [ ] Commit: `"lumen: accessibility fixes and localizable strings"`

**Requires:** display-session -- the audit needs an interactive desktop

**Test checkpoint:** the audit report shows zero failures. Cheaper substitute that fails: automation names on buttons only.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0
- [ ] The unchanged-originals tests pass after every section
- [ ] `python scripts/todo-graph.py validate` clean
