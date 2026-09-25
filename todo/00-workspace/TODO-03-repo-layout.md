---
schema_version: 1
id: repo-layout
domain: 00-workspace
status: draft
title: "TODO-03 -- Repository Layout and Visual Baselines"
depends_on: []
track: W3
---

# TODO-03 -- Repository Layout and Visual Baselines

> **Goal:** Nothing in the tree is a leftover of the imports: each app's documentation lives under `docs/`, sample files sit with the test fixtures, empty folders are gone, and both imported apps have committed captures of their current surfaces, so every later UI section has a visual baseline to be reviewed against.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The imports brought their own documentation folders: `src/Nodus/docs/` (a `README.md` indexing mostly missing pages, `components/vector-icon.md`, `ui/status-bar.md`) and `src/Imago/docs/` (five `README.md` stubs under `api/`, `architecture/`, `plugins/`, `user-guide/`). Two loose SVG files sit at `src/Nodus/test.svg` and `src/Nodus/bezier-sample.svg`. `src/Imago/.github/` is an empty directory left after the per-app workflows were removed. There is no `docs/captures/` folder, so a `Fidelity:` block that names one cannot be satisfied and `process-todo-section` would refuse every UI section.
<!-- claim: exists src/Nodus/docs/README.md -->
<!-- claim: exists src/Imago/docs/README.md -->
<!-- claim: exists src/Nodus/bezier-sample.svg -->
<!-- claim: exists src/Nodus/test.svg -->
<!-- claim: absent docs/captures -->

## Inputs

- [`docs/README.md`](../../docs/README.md), [`docs/dev/README.md`](../../docs/dev/README.md) -- the documentation indexes §1 links the moved pages from
- [`.claude/skills/process-todo-section/gates.md`](../../.claude/skills/process-todo-section/gates.md) -- the launch smoke §2 follows
- [`standards/shared.md`](../../standards/shared.md) -- the design contract the captures illustrate

## Outcome

- `src/Nodus/` and `src/Imago/` hold only projects and build overlays; their documentation lives under `docs/dev/nodus/` and `docs/dev/imago/`.
- The two sample SVG files are committed fixtures under `tests/fixtures/nodus/svg/` with a README naming their source.
- `docs/captures/nodus/main-window/` and `docs/captures/imago/main-window/` hold dated captures of each app's current main window at 100 and 150 percent scaling, with a `README.md` recording the commit and machine.

**Adjacency:** all=not-applicable (moving files and recording baselines: no records, settings, or documents a user changes)

**Adjacency rationale:** The captures are evidence for reviewers, not a product surface; the sections that change those surfaces own their adjacency.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On | Status |
| :---: | :-----: | ---------------------------------------------------- | ---------- | :----: |
|   1   |   §1    | Fold the per-app docs and samples into the suite     | --         |  [ ]   |
|   2   |   §2    | Baseline captures of Nodus and Imago                 | --         |  [ ]   |

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

## 2. Baseline Captures of Nodus and Imago

Every UI section carries a `Fidelity:` block naming a capture under `docs/captures/<app>/`, and `process-todo-section` refuses to build a surface whose capture does not exist. The apps have no captures yet, so this section records the imported surfaces exactly as they are today: not the target look, the starting line the next changes are reviewed against.

**Fidelity:** Nodus main window and Imago main window as imported -- docs/captures/nodus/main-window/ and docs/captures/imago/main-window/ are created by this section; the captures record the current state, and the design contract in `standards/shared.md` is what later sections move them toward.
**Job:** a reviewer can compare a changed surface against how it looked before the change. Consumer: `review-todo-section`, which compares the rendered surface against the named capture before stamping.
**Treatment:** full-window PNG captures of each app's main window with an empty document, at 100 and 150 percent display scaling, plus one with a sample document open. Cheaper substitute that fails the checkpoint: the marketing screenshots under `resources/screens/`, which are not captures of the built app.
**Chrome:** consume the existing windows unchanged. Do not restyle anything in this section.

**Requires:** display-session -- capturing a rendered WPF window needs an interactive desktop session

- [ ] Build Debug (`dotnet build Photon.slnx -c Debug`) and launch `Bezier.Desktop.exe` from `artifacts/bin/Bezier.Desktop/debug/`; capture the main window with no document to `docs/captures/nodus/main-window/empty-100.png`. Done when: the PNG shows the menu, tool rail, canvas, panels, and status strip.
- [ ] Open `tests/fixtures/nodus/svg/bezier-sample.svg` (or `src/Nodus/bezier-sample.svg` if §1 has not shipped) and capture `docs/captures/nodus/main-window/sample-100.png`. Done when: the drawing is visible on the canvas in the capture.
- [ ] Repeat the empty capture at 150 percent scaling as `empty-150.png`. Done when: the file exists and its pixel width is about 1.5 times the 100 percent capture for the same window size.
- [ ] Launch `Imago.exe` from `artifacts/bin/Imago.UI/debug/` and capture `docs/captures/imago/main-window/empty-100.png` and `empty-150.png`. Done when: both files exist.
- [ ] Write `docs/captures/README.md` (folder per app, then per surface; file names `<state>-<scale>.png`; each surface folder's `README.md` records the commit, date, Windows build, and scaling) and one `README.md` per surface folder. Done when: both surface folders carry their record.
- [ ] Quote the Serilog error count for the Imago run (`%LOCALAPPDATA%\Imago\logs\`) and the debug-log state for Nodus (it has no file log yet, `D02 T01 §3`). Done when: both are in the commit body.
- [ ] Commit: `"docs: record baseline captures of Nodus and Imago"`

**Test checkpoint:** `Get-ChildItem docs/captures -Recurse -Filter *.png` lists at least five captures, each non-empty and a valid PNG (its first eight bytes are the PNG signature, checked with `Format-Hex`); each surface folder's `README.md` names the commit the captures were taken at. Cheaper substitute that fails: copying `resources/screens/nodus.png`, which the commit record would not match.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0 after the moves
- [ ] `docs/captures/` exists with a record per surface
- [ ] `python scripts/todo-graph.py validate` clean
