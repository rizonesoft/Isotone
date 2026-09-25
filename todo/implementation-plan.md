# Photon -- Implementation Plan to 100%

The order to run every section in, from today to independently distributed releases of Nodus, Imago, and Lumen and the first Rizonesoft Graphics Suite bundle.

> **Progress:** **0 of 169 sections complete (0%).** Derived from the Implementation Order tables by `python scripts/todo-graph.py plan --sync` -- never edited by hand.
>
> **Plan/graph parity.** Every numbered TODO section, open or shipped, appears in exactly one phase table row. `plan --check` enforces missing, unknown, duplicate, and status parity. Read live totals from the generated Progress line above and `python scripts/todo-graph.py query stats`; never repeat a fixed denominator in prose.

Seeded 2026-09-26 from the imported Bezier and Imago code, their legacy roadmaps (kept in [`../docs/legacy/`](../docs/legacy/README.md)), the Photon planning notes, and the operator's decisions recorded in [`../AGENTS.md`](../AGENTS.md).

**How to use this.** The front door is the `process-plan` skill. It audits, then runs `process-phase` on the first phase that has a ready row, then the next ready phase after that closeout or park. One row is `process-todo-section` then `review-todo-section`. Do not invent a side loop.

**Copy a row and paste it.** The skills resolve a reference from whatever shape it arrives in, so this is a complete instruction:

```
process todo section: | [ ] | `D00 T01 §1` | Wire the TODO gate into every clone | 4 |
```

> [!IMPORTANT]
> **The boxes are derived. Never tick one by hand.**
>
> They are a projection of each TODO's Implementation Order table, and those flip in exactly one place: `review-todo-section`, after a `Verified:` stamp exists.
>
> ```bash
> python scripts/todo-graph.py plan --sync     # rewrite the boxes, then re-align every table
> python scripts/todo-graph.py plan --check    # fail if they have gone stale
> ```

**How phases are authored.** A phase is a `### Phase <N> -- <Title>` heading, one paragraph on why it runs where it does, and one table. Every section in the tree sits in exactly one phase row; a new TODO file places each of its sections here in the commit that authors it. A section's phase is never earlier than the phase of anything it depends on, and within a phase rows run in dependency order. The format is specified in [`README.md`](./README.md) under "The implementation plan: phases and rows".

---

## The acceptance bar

The finished suite is **three standalone creative applications that behave like one product**: each built by one command from a clean checkout, checked by the same gates, installed by its own installer on a machine that has never seen .NET, versioned and released on its own tag, logging every action that changes a document or a setting, undoing every edit, saving atomically, recovering after a crash, opening and saving its formats with proven fidelity, looking and behaving like its siblings through one theme and one set of shared controls, reachable by keyboard and screen reader, and never needing another Photon app at runtime. Lumen additionally never writes an original image. The count of sections is deliberately not repeated here: read it from `query stats`.

| Aim                                             | Owned by                                                                      |
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| Every clone refuses a broken plan               | `D00 T01 §1` (hook) · `D00 T01 §5` (CI read back)                             |
| Operator-only work never stalls a runner        | `D00 T01 §2` · `D99 T01 §1`-`§5`                                              |
| The review panel works before the first stamp   | `D00 T01 §4`                                                                  |
| No quarantined test, no excused warning         | `D00 T02 §1` · `D00 T02 §2` · `D02 T01 §7`                                    |
| No dependency without a reason and a license    | `D00 T02 §4` · `D00 T02 §5` · `D02 T02 §2` · `D03 T04 §1` · `D04 T01 §3`      |
| Every surface has a baseline to review against  | `D00 T03 §2`                                                                  |
| The apps carry their own names                  | `D02 T01 §1` · `D03 T01 §1` · `D03 T01 §4`                                    |
| One composition root per app, logging to disk   | `D01 T02 §1` · `D02 T01 §2` · `D02 T01 §3` · `D03 T01 §5` · `D04 T01 §2`      |
| Shared once, never copied                       | `D01 T01 §1`-`§4` (Photon.UI) · `D01 T02 §1`-`§5` (Photon.Core)               |
| Every edit has a reverse                        | `D02 T03 §1` · `D02 T03 §4` · `D01 T02 §4` · `D03 T03 §2` · `D04 T02 §1`      |
| Saves never damage the user's file              | `D02 T04 §1` · `D01 T02 §5` · `D03 T04 §2`                                    |
| A crash loses nothing                           | `D02 T04 §5` · `D03 T04 §6`                                                   |
| Formats are proven, not assumed                 | `D02 T04 §2` · `D03 T02 §4` · `D03 T04 §2`-`§5` · `D04 T01 §4` · `D04 T02 §2` |
| No menu item silently does nothing              | `D02 T03 §5` · `D03 T06 §2`                                                   |
| Originals are never written                     | `D04 T01 §6` · `D04 T01 §11` · `D04 T02 §1`                                   |
| It looks like one suite                         | `standards/shared.md` (design contract) · `D01 T01 §3`                        |
| It works without a mouse or eyes                | `D02 T06 §17` · `D03 T07 §16` · `D04 T03 §10`                                 |
| Each app ships alone, proven on a clean machine | `D05 T01 §1` · `D02 T05 §4` · `D03 T06 §3` · `D04 T02 §8`                     |
| The suite ships together without re-versioning  | `D05 T01 §6`                                                                  |
| Users can learn it                              | `D06 T01 §1`-`§4`                                                             |

---

## Where the project stands

Nothing in this plan has been built, but the tree is not empty.

**Nodus** (imported from Bezier with history under `src/Nodus/`, still named `Bezier.*`) is a working WPF vector editor: a SkiaSharp canvas, SVG import and export, select, pen, shape, text, zoom, and pan tools, an undo history, and 968 test methods. Measured on 2026-09-26, it is also mostly unwired: 25 of 31 Core services are referenced only by tests, 26 Object and Path menu commands only set status text, resize and rotate are not undoable, the composition root registers one type, it never writes a log file, and it builds with 334 warnings excused. Its legacy roadmap claims about 420 items done; many of those are code nobody can reach.

**Imago** (imported under `src/Imago/`) has a sound core model (layers, masks, selections, tiles, color, history) with 41 test methods, a WPF shell still built on WPF-UI, a document service that pretends, and no rendering, tools, or codecs. A local branch carries a December 2025 snapshot with a canvas, ruler, and a WPF-UI-free main window that `D03 T01 §2` ports.

**Lumen** has no code; it is planned in full in `todo/04-lumen/`.

**The workspace** has a pinned SDK, one solution, one build configuration, scripts, installers, and CI workflows written on 2026-09-26 and not yet committed or run on GitHub.

Every open section is in scope and appears in exactly one phase. A dependency may park a row; it does not remove it. Completion-first: a row flips only whole, and debt always names its collector.

---

## Prerequisites

**These are not sections. They are things that must be true before certain sections can start.**

### 1. A Windows host with the pinned SDK

Everything builds and runs on Windows only. `pwsh tools/provision.ps1` installs the SDK `global.json` pins and Inno Setup, and wires the commit hook.

### 2. An interactive desktop session

Every section that launches an app, drives a surface, or takes a capture carries `**Requires:** display-session`. A runner without one (a service session, CI, WSL) skips those rows and takes the next runnable one.

### 3. A clean Windows machine

The clean-machine procedure (`D05 T01 §1`) and each app release need a Windows machine with no .NET SDK or runtime. Windows Sandbox or a VM snapshot is sufficient. Rows that need it carry `**Needs:** Clean Windows machine (no .NET SDK)`.

### 4. Reference implementations for fidelity goldens

Inkscape (SVG), GIMP or libvips (raster and blend modes), and LibRaw's `dcraw_emu` or darktable (RAW) produce the goldens the fidelity proofs compare against, each with its version recorded beside the fixtures. Install them on the machine that generates goldens.

### 5. A code-signing certificate

There is none. `D05 T01 §2` carries `**Needs:** Signing certificate (release)` and waits; the operator obtains one through `D99 T01 §3`. Releases ship unsigned until then, and the install guide says so.

### 6. The operator's GitHub session

Repository settings and branch protection (`D99 T01 §1`, `§2`) need the owner's logged-in browser. The agent's `gh` credentials push, tag, and create releases; they do not change repository settings.

---

## The phases

### Phase 0 -- Workspace spine: gates, CI, import debt, and baselines

Nothing in this plan can be proven until the gates run on every clone and every push, so this phase wires the commit hook, marks operator-only rows, raises the claims ratchet, proves the review panel, and reads back the first green CI runs. It also retires the import debt that belongs to the workspace (the test quarantine, Imago's excused diagnostics, unused packages, the assertion library's license), records baseline captures so every later UI section has something to be reviewed against, and dry-runs the release pipeline on a prerelease tag. Every row here is ready on day one or depends only on another row here.

|  ✔  | Section      | Deliverable                                         | Items |
| :-: | ------------ | --------------------------------------------------- | :---: |
| [ ] | `D00 T01 §1` | Wire the TODO gate into every clone                 |   4   |
| [ ] | `D00 T01 §2` | The operator requirement for manual rows            |   6   |
| [ ] | `D00 T01 §3` | Raise the claims coverage floor                     |   3   |
| [ ] | `D00 T01 §4` | Prove the review panel end to end                   |   5   |
| [ ] | `D00 T02 §1` | Fix the quarantined tests and empty the quarantine  |   5   |
| [ ] | `D00 T02 §2` | Imago diagnostics to zero                           |   4   |
| [ ] | `D00 T02 §3` | Quiet the WPF temporary project output              |   3   |
| [ ] | `D00 T02 §4` | Prune packages no code uses                         |   7   |
| [ ] | `D00 T02 §5` | The assertion library decision and the decision log |   5   |
| [ ] | `D00 T03 §1` | Fold the per-app docs and samples into the suite    |   7   |
| [ ] | `D00 T03 §2` | Baseline captures of Nodus and Imago                |   7   |
| [ ] | `D00 T01 §5` | First push: CI green and read back                  |   5   |
| [ ] | `D00 T02 §7` | Release pipeline dry run on a prerelease tag        |   7   |

### Phase 1 -- Suite layout and names

Every later section names files, so both imported apps move into the suite layout and take their Photon names before anything else is written against their paths: Bezier becomes `Photon.Nodus` and ships `Nodus.exe`, Imago becomes `Photon.Imago`, and Imago gets its icon. The renames change names only, so they are cheap to review and keep git history intact.

|  ✔  | Section      | Deliverable                                  | Items |
| :-: | ------------ | -------------------------------------------- | :---: |
| [ ] | `D02 T01 §1` | Rename Bezier to Photon.Nodus                |   9   |
| [ ] | `D03 T01 §1` | Restructure and rename Imago to Photon.Imago |   6   |
| [ ] | `D03 T01 §4` | The Imago icon                               |   5   |

### Phase 2 -- Nodus foundation: composition, hygiene, triage, correctness

Nodus goes first among the apps. This phase gives it a real composition root on the Generic Host and the first `Photon.Core` services (logging and settings, which Imago already needs, so the library is born with two consumers), clears the analyzer backlog through the SkiaSharp 4 migration until warnings are errors, triages the orphan services and the three SVG stacks down to one render path, puts selection under one owner, records resize and rotate as undo steps, splits the god view model, makes saving atomic, and proves the SVG round trip against fixtures. xUnit v3 lands here, after both renames moved the test projects.

|  ✔  | Section      | Deliverable                                        | Items |
| :-: | ------------ | -------------------------------------------------- | :---: |
| [ ] | `D01 T02 §1` | Create Photon.Core with app-data paths and logging |   7   |
| [ ] | `D01 T02 §2` | The settings store                                 |   5   |
| [ ] | `D02 T01 §2` | Composition root on the Generic Host               |   5   |
| [ ] | `D02 T01 §3` | The debug console reads the Serilog pipeline       |   5   |
| [ ] | `D02 T01 §4` | Culture-safe formatting and comparisons            |   5   |
| [ ] | `D02 T01 §5` | The rest of the analyzer backlog                   |   4   |
| [ ] | `D02 T02 §1` | The triage record and the delete group             |   4   |
| [ ] | `D02 T02 §2` | One SVG render path                                |   5   |
| [ ] | `D02 T01 §6` | SkiaSharp 4                                        |   6   |
| [ ] | `D02 T01 §7` | Warnings are errors in Nodus                       |   4   |
| [ ] | `D02 T02 §3` | Selection has one owner                            |   5   |
| [ ] | `D02 T03 §1` | Undo for resize and rotate                         |   6   |
| [ ] | `D02 T03 §2` | Split the main window view model                   |   7   |
| [ ] | `D02 T04 §1` | Atomic save and dirty tracking                     |   8   |
| [ ] | `D02 T04 §2` | SVG round-trip fidelity fixtures                   |   5   |
| [ ] | `D00 T02 §6` | xUnit v3                                           |   5   |

### Phase 3 -- Nodus 0.1.0: shared UI, complete editing, documents, release

With its foundation sound, Nodus becomes a complete first release: `Photon.UI` takes the controls and windows Nodus and Imago duplicate and the suite theme, single instance moves to `Photon.Core`, the triaged services are wired (arrange, align, booleans on `SKPath.Op`, layers, snapping, one keymap), the clipboard and property edits are undoable, exports and recovery work, every menu item works or names its owner, the About, shortcuts, and Help surfaces exist, the user guide is written, the clean-machine procedure is proven, and `nodus-v0.1.0` ships.

|  ✔  | Section      | Deliverable                                          | Items |
| :-: | ------------ | ---------------------------------------------------- | :---: |
| [ ] | `D01 T01 §1` | Create Photon.UI with the icon catalog               |   7   |
| [ ] | `D01 T01 §2` | Splash, exception window, and glow move to Photon.UI |   7   |
| [ ] | `D01 T01 §3` | The suite theme resources                            |   6   |
| [ ] | `D01 T02 §3` | Single instance and file-open forwarding             |   4   |
| [ ] | `D02 T02 §4` | Arrange, align, distribute, rotate, and flip         |   8   |
| [ ] | `D02 T02 §5` | Boolean path operations on SKPath.Op                 |   5   |
| [ ] | `D02 T02 §6` | The layers panel on LayerManager                     |   7   |
| [ ] | `D02 T02 §7` | Snapping on SnapManager                              |   5   |
| [ ] | `D02 T02 §8` | One keymap on ShortcutManager                        |   4   |
| [ ] | `D02 T03 §3` | Clipboard and the Edit menu                          |   6   |
| [ ] | `D02 T03 §4` | Property edits are undo steps                        |   4   |
| [ ] | `D02 T04 §3` | PNG and JPEG export                                  |   6   |
| [ ] | `D02 T04 §4` | PDF export                                           |   4   |
| [ ] | `D02 T04 §5` | Recent files, autosave, and crash recovery           |   7   |
| [ ] | `D02 T04 §6` | Open from the command line and the .svg association  |   4   |
| [ ] | `D02 T03 §5` | Every menu command works or names its owner          |   5   |
| [ ] | `D02 T05 §1` | The About dialog                                     |   5   |
| [ ] | `D02 T05 §2` | The keyboard shortcuts dialog                        |   4   |
| [ ] | `D02 T05 §3` | The Help menu                                        |   3   |
| [ ] | `D06 T01 §1` | The Nodus user guide                                 |   4   |
| [ ] | `D06 T02 §1` | The architecture page matches the tree               |   4   |
| [ ] | `D05 T01 §1` | The clean-machine install procedure                  |   3   |
| [ ] | `D02 T05 §4` | Nodus 0.1.0                                          |   8   |

### Phase 4 -- Imago foundation: snapshot port, WPF-UI out, tiles, rendering

Imago starts once Nodus has shipped. The December 2025 snapshot's canvas, ruler, and container are ported onto `main` and the branch deleted, WPF-UI leaves the suite for good, Imago starts through the shared logging and settings, its layers become tile-backed, the viewport renders the tiled composite at any zoom, the render graph composites every blend mode against reference goldens, and a ComputeSharp path matches the CPU. The codec decision is made here so file work can start the moment editing exists.

|  ✔  | Section      | Deliverable                                       | Items |
| :-: | ------------ | ------------------------------------------------- | :---: |
| [ ] | `D03 T01 §2` | Port the snapshot canvas, ruler, and container    |   7   |
| [ ] | `D03 T01 §3` | WPF-UI out of Imago                               |   6   |
| [ ] | `D03 T01 §5` | Composition root on Photon.Core                   |   4   |
| [ ] | `D03 T02 §1` | The tiled image store                             |   5   |
| [ ] | `D03 T02 §2` | The viewport on the tiled document                |   6   |
| [ ] | `D03 T02 §3` | The render graph composites layers                |   4   |
| [ ] | `D03 T02 §4` | Blend modes with golden tests                     |   4   |
| [ ] | `D03 T02 §5` | The ComputeSharp compositing path with CPU parity |   5   |
| [ ] | `D03 T04 §1` | The codec decision                                |   4   |

### Phase 5 -- Imago 0.1.0: editing, files, filters, release

Imago becomes a complete first release: the suite undo history and the atomic document writer move to `Photon.Core` as Imago becomes their second consumer, the About and shortcuts dialogs move to `Photon.UI`, documents open in tabs with every edit in the history, the layers panel and core tools work, PNG, JPEG, TIFF, the native layered format, and PSD import are proven by round trips, autosave and recovery work, the core adjustments and blurs match reference goldens, the user guide is written, and `imago-v0.1.0` ships.

|  ✔  | Section      | Deliverable                                       | Items |
| :-: | ------------ | ------------------------------------------------- | :---: |
| [ ] | `D01 T02 §4` | One undo history for the suite                    |   5   |
| [ ] | `D01 T02 §5` | The atomic document writer moves to Photon.Core   |   4   |
| [ ] | `D01 T01 §4` | About and shortcuts dialogs move to Photon.UI     |   6   |
| [ ] | `D03 T03 §1` | Documents in tabs with dirty tracking             |   5   |
| [ ] | `D03 T03 §2` | Every edit in the suite history                   |   5   |
| [ ] | `D03 T03 §3` | The layers panel                                  |   4   |
| [ ] | `D03 T03 §4` | The tool system: move, hand, and zoom             |   4   |
| [ ] | `D03 T03 §5` | Selection tools                                   |   4   |
| [ ] | `D03 T03 §6` | Brush and eraser                                  |   3   |
| [ ] | `D03 T03 §7` | Transform, crop, image size, and canvas size      |   4   |
| [ ] | `D03 T03 §8` | Fill, gradient, eyedropper, and the color panel   |   3   |
| [ ] | `D03 T04 §2` | PNG and JPEG open and save                        |   7   |
| [ ] | `D03 T04 §3` | TIFF open and save                                |   4   |
| [ ] | `D03 T04 §4` | The native layered format                         |   5   |
| [ ] | `D03 T04 §5` | PSD import                                        |   5   |
| [ ] | `D03 T04 §6` | Autosave and crash recovery                       |   4   |
| [ ] | `D03 T05 §1` | The filter pipeline                               |   4   |
| [ ] | `D03 T05 §2` | Core adjustments                                  |   4   |
| [ ] | `D03 T05 §3` | Blur and sharpen                                  |   5   |
| [ ] | `D03 T06 §1` | About, shortcuts, and help in Imago               |   3   |
| [ ] | `D03 T06 §2` | Every Imago menu command works or names its owner |   3   |
| [ ] | `D06 T01 §2` | The Imago user guide                              |   4   |
| [ ] | `D03 T06 §3` | Imago 0.1.0                                       |   7   |

### Phase 6 -- Lumen foundation: spine, catalog, import, RAW, library

Lumen is planned from nothing with `plan-new-feature` rigor and built on the spine the other two apps proved. The competitor survey is driven first so the plan is corrected by evidence; then the app is created on `Photon.Core` and `Photon.UI`, the RAW decoder is chosen with coverage, speed, and license measured, decoding is proven against a reference, the SQLite catalog and safe import land (the original-file guard joins the frozen set), and the preview cache, grid, and loupe make a 50,000-photo library usable.

|  ✔  | Section      | Deliverable                       | Items |
| :-: | ------------ | --------------------------------- | :---: |
| [ ] | `D04 T01 §1` | The competitor survey, driven     |   4   |
| [ ] | `D04 T01 §2` | Create the Lumen app              |   7   |
| [ ] | `D04 T01 §3` | The RAW decoder decision          |   4   |
| [ ] | `D04 T01 §4` | RAW decode with fidelity fixtures |   5   |
| [ ] | `D04 T01 §5` | The catalog database              |   5   |
| [ ] | `D04 T01 §6` | Import                            |   6   |
| [ ] | `D04 T01 §7` | Thumbnails and the preview cache  |   4   |
| [ ] | `D04 T01 §8` | The library grid                  |   5   |
| [ ] | `D04 T01 §9` | Loupe, compare, and filmstrip     |   3   |

### Phase 7 -- Lumen 0.1.0: develop, export, Edit in Imago, release

Lumen becomes a complete first release: keywords, collections, culling, and XMP sidecars finish the library; the edit stack, the float32 develop pipeline, the develop panel, crop, presets, and export make it a darkroom; Edit in Imago hands photos to Imago over files, never over assemblies; the user guide is written; and `lumen-v0.1.0` ships with the original-file guard proven on the installed build.

|  ✔  | Section       | Deliverable                                  | Items |
| :-: | ------------- | -------------------------------------------- | :---: |
| [ ] | `D04 T01 §10` | Keywords, collections, and smart collections |   4   |
| [ ] | `D04 T01 §11` | Ratings, flags, labels, and XMP sidecars     |   4   |
| [ ] | `D04 T02 §1`  | The edit stack                               |   4   |
| [ ] | `D04 T02 §2`  | The develop pipeline                         |   6   |
| [ ] | `D04 T02 §3`  | The develop panel                            |   4   |
| [ ] | `D04 T02 §4`  | Crop and straighten                          |   3   |
| [ ] | `D04 T02 §5`  | Presets, copy and paste settings, and sync   |   3   |
| [ ] | `D04 T02 §6`  | Export                                       |   4   |
| [ ] | `D06 T01 §3`  | The Lumen user guide                         |   4   |
| [ ] | `D04 T02 §7`  | Edit in Imago                                |   4   |
| [ ] | `D04 T02 §8`  | Lumen 0.1.0                                  |   7   |

### Phase 8 -- Distribution and the suite bundle

With all three apps released, distribution catches up: signing (waiting on the operator's certificate through its `Needs:` line), win-arm64 builds, an opt-in update check shared by every app, winget manifests, the install and troubleshooting guides, and the first suite bundle, `photon-v1.0.0`, which carries each app at its own version. The README shows the real apps and the guides are published as a site.

|  ✔  | Section      | Deliverable                         | Items |
| :-: | ------------ | ----------------------------------- | :---: |
| [ ] | `D05 T01 §2` | Sign binaries and installers        |   5   |
| [ ] | `D05 T01 §3` | win-arm64 publish and installers    |   5   |
| [ ] | `D05 T01 §4` | The update check                    |   4   |
| [ ] | `D05 T01 §5` | winget manifests                    |   5   |
| [ ] | `D06 T01 §4` | Install and troubleshooting guides  |   4   |
| [ ] | `D05 T01 §6` | The suite bundle: photon-v1.0.0     |   5   |
| [ ] | `D06 T02 §2` | README images from real captures    |   3   |
| [ ] | `D06 T02 §3` | The user guides as a published site |   4   |

### Phase 9 -- Nodus roadmap

The long tail of the legacy Bezier roadmap at feature grain, after the suite release. Each section is born complete and is expected to be split by `groom-plan` before it runs; the deferred services from the triage are wired here.

|  ✔  | Section       | Deliverable                                            | Items |
| :-: | ------------- | ------------------------------------------------------ | :---: |
| [ ] | `D02 T06 §1`  | Shape tools: polygon, star, spiral, arc                |   5   |
| [ ] | `D02 T06 §2`  | Path editing: continue, join, break, reverse, simplify |   4   |
| [ ] | `D02 T06 §3`  | Text: area text, text on path, text to path            |   4   |
| [ ] | `D02 T06 §4`  | Clipping, masks, and compound paths                    |   4   |
| [ ] | `D02 T06 §5`  | Appearance: swatches, multiple fills, conic gradients  |   4   |
| [ ] | `D02 T06 §6`  | Artboards: presets, duplicate, arrange, fit            |   3   |
| [ ] | `D02 T06 §7`  | Documents in tabs, saved layouts, nested layers        |   5   |
| [ ] | `D02 T06 §8`  | The contextual property bar                            |   2   |
| [ ] | `D02 T06 §9`  | Transform precision and smart selection                |   3   |
| [ ] | `D02 T06 §10` | Guides and measurement                                 |   3   |
| [ ] | `D02 T06 §11` | Symbols and the asset library                          |   3   |
| [ ] | `D02 T06 §12` | The command palette and the on-canvas HUD              |   4   |
| [ ] | `D02 T06 §13` | Preferences and shortcut remapping                     |   4   |
| [ ] | `D02 T06 §14` | More formats and the export dialog                     |   4   |
| [ ] | `D02 T06 §15` | Freehand tools: pencil, brush, eraser                  |   3   |
| [ ] | `D02 T06 §16` | Large documents: spatial index, culling, dirty regions |   5   |
| [ ] | `D02 T06 §17` | Accessibility and localization                         |   4   |
| [ ] | `D02 T06 §18` | Brushes, patterns, and color tools                     |   3   |
| [ ] | `D02 T06 §19` | Print and prepress                                     |   3   |
| [ ] | `D02 T06 §20` | Scripting and plugins                                  |   4   |
| [ ] | `D02 T06 §21` | Onboarding and the navigator                           |   3   |

### Phase 10 -- Imago roadmap

The long tail of the legacy Imago roadmap at feature grain: non-destructive adjustments, masks, the rest of the filter catalog, styles, retouching, text and shapes, brushes, formats, the shared RAW decoder, color management, plugins, scripting, performance, accessibility, and workspaces. Rows run in dependency order (color management before print, workspaces before accessibility).

|  ✔  | Section       | Deliverable                                            | Items |
| :-: | ------------- | ------------------------------------------------------ | :---: |
| [ ] | `D03 T07 §1`  | Adjustment layers                                      |   4   |
| [ ] | `D03 T07 §2`  | Layer masks, clipping masks, and vector masks          |   3   |
| [ ] | `D03 T07 §3`  | The rest of the filter catalog                         |   4   |
| [ ] | `D03 T07 §4`  | Layer styles                                           |   3   |
| [ ] | `D03 T07 §5`  | Retouching tools                                       |   3   |
| [ ] | `D03 T07 §6`  | Text layers                                            |   3   |
| [ ] | `D03 T07 §7`  | Shape layers and vector tools                          |   3   |
| [ ] | `D03 T07 §8`  | The brush engine: tips, dynamics, presets              |   3   |
| [ ] | `D03 T07 §10` | More formats: WebP, HEIC, EXR, GIF, PSD write          |   5   |
| [ ] | `D03 T07 §11` | RAW import through the shared decoder                  |   3   |
| [ ] | `D03 T07 §12` | Color management and soft proofing                     |   4   |
| [ ] | `D03 T07 §9`  | Print                                                  |   2   |
| [ ] | `D03 T07 §13` | Filter plugins                                         |   4   |
| [ ] | `D03 T07 §14` | Scripting                                              |   4   |
| [ ] | `D03 T07 §15` | Performance: memory, SIMD, startup                     |   4   |
| [ ] | `D03 T07 §17` | Workspaces, panels, and preferences                    |   3   |
| [ ] | `D03 T07 §16` | Accessibility and localization                         |   4   |
| [ ] | `D03 T07 §18` | Smart selection: magic wand, quick select, color range |   3   |

### Phase 11 -- Lumen roadmap

The darkroom features beyond the first release, drawn from the competitor survey: local adjustments, detail, lens corrections, color grading, merges, a GPU path, map, print, catalog maintenance, and accessibility.

|  ✔  | Section       | Deliverable                                    | Items |
| :-: | ------------- | ---------------------------------------------- | :---: |
| [ ] | `D04 T03 §1`  | Local adjustments: brush, linear, radial masks |   3   |
| [ ] | `D04 T03 §2`  | Detail: sharpening and noise reduction         |   3   |
| [ ] | `D04 T03 §3`  | Lens corrections                               |   3   |
| [ ] | `D04 T03 §4`  | Color grading and HSL                          |   2   |
| [ ] | `D04 T03 §5`  | HDR and panorama merge                         |   3   |
| [ ] | `D04 T03 §6`  | A GPU develop path with CPU parity             |   2   |
| [ ] | `D04 T03 §7`  | Map and GPS                                    |   2   |
| [ ] | `D04 T03 §8`  | Contact sheets and print                       |   2   |
| [ ] | `D04 T03 §9`  | Catalog maintenance and library statistics     |   4   |
| [ ] | `D04 T03 §10` | Accessibility and localization                 |   3   |

### Phase 99 -- Manual: operator-only steps

No agent runner takes rows from this phase. Each row is a click path, a purchase, or a taste call the operator performs from the steps in `todo/99-manual/`; an agent verifies the public proof afterward and review stamps the evidence like any other row. Until `D00 T01 §2` ships, the rows are held back by their dependency on it; after it ships, each carries `**Requires:** operator`, so `query ready` lists them as runnable elsewhere and runners skip them.

|  ✔  | Section      | Deliverable                                | Items |
| :-: | ------------ | ------------------------------------------ | :---: |
| [ ] | `D99 T01 §1` | About bar, topics, and social preview      |   5   |
| [ ] | `D99 T01 §2` | Branch protection with the required checks |   3   |
| [ ] | `D99 T01 §3` | A code-signing certificate                 |   4   |
| [ ] | `D99 T01 §4` | Confirm the icon art licenses              |   3   |
| [ ] | `D99 T01 §5` | Choose each app's accent color             |   2   |
