# Photon -- Implementation Plan to 100%

The order to run every section in, from today to independently distributed releases of Nodus, Imago, and Lumen and the first Photon Graphics Suite bundle.

> **Progress:** **0 of 489 sections complete (0%).** Budget: 489 of 555 sections; backlog 23 of 150. Derived from the Implementation Order tables by `python scripts/todo-graph.py plan --sync` -- never edited by hand.
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

**The plan is bounded.** Every phase has a ceiling on its total sections (open plus shipped) in [`budget.json`](./budget.json), the tree's total is capped at their sum, and `validate` refuses a breach. Work that fails the admission test in [`README.md`](./README.md) ("The budget and the backlog") goes to [`backlog.md`](./backlog.md), which is not in this plan, never runnable, and capped too. Only the operator raises a ceiling. The Progress line above reports the use.

**How phases are authored.** A phase is a `### Phase <N> -- <Title>` heading, one paragraph on why it runs where it does, and one table. Every section in the tree sits in exactly one phase row; a new TODO file places each of its sections here in the commit that authors it. A section's phase is never earlier than the phase of anything it depends on, and within a phase rows run in dependency order. The format is specified in [`README.md`](./README.md) under "The implementation plan: phases and rows".

---

## The acceptance bar

The finished suite is **three standalone creative applications that behave like one product**: each built by one command from a clean checkout, checked by the same gates, installed by its own installer on a machine that has never seen .NET, versioned and released on its own tag, logging every action that changes a document or a setting, undoing every edit, saving atomically, recovering after a crash, opening and saving its formats with proven fidelity, looking and behaving like its siblings through one theme and one set of shared controls, reachable by keyboard and screen reader, and never needing another Photon app at runtime. Lumen additionally never writes an original image. The count of sections is deliberately not repeated here: read it from `query stats`.

| Aim                                                                                                                                               | Owned by                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Every clone refuses a broken plan                                                                                                                 | `D00 T01 §1` (hook) · `D00 T01 §5` (CI read back)                                                                                                                                                                                               |
| Operator-only work never stalls a runner                                                                                                          | `D00 T01 §2` · `D99 T01 §1`-`§5`                                                                                                                                                                                                                |
| The review panel works before the first stamp                                                                                                     | `D00 T01 §4`                                                                                                                                                                                                                                    |
| No quarantined test, no excused warning                                                                                                           | `D00 T02 §1` · `D00 T02 §2` · `D02 T01 §7`                                                                                                                                                                                                      |
| No dependency without a reason and a license                                                                                                      | `D00 T02 §4` · `D00 T02 §5` · `D02 T02 §2` · `D03 T04 §1` · `D04 T01 §3` · `D01 T04 §1` · `D02 T10 §1` · `D02 T13 §14` · `D02 T14 §2` · `D02 T14 §6` · `D02 T14 §10` · `D03 T15 §5` · `D03 T17 §5` · `D03 T17 §6` · `D03 T17 §7` · `D03 T12 §4` |
| Every surface has a baseline to review against                                                                                                    | `D00 T03 §2`                                                                                                                                                                                                                                    |
| The apps carry their own names                                                                                                                    | `D02 T01 §1` · `D03 T01 §1` · `D03 T01 §4`                                                                                                                                                                                                      |
| One composition root per app, logging to disk                                                                                                     | `D01 T02 §1` · `D02 T01 §2` · `D02 T01 §3` · `D03 T01 §5` · `D04 T01 §2`                                                                                                                                                                        |
| Shared once, never copied                                                                                                                         | `D01 T01 §1`-`§4` (Photon.UI) · `D01 T02 §1`-`§5` (Photon.Core) · `D01 T03 §1` · `D01 T04 §1` · `D01 T05 §1` · `D01 T06 §1` · `D01 T07 §1` · `D03 T16 §1` · `D03 T16 §5` · `D03 T17 §2` · `D03 T18 §6`                                          |
| Every edit has a reverse                                                                                                                          | `D02 T03 §1` · `D02 T03 §4` · `D01 T02 §4` · `D03 T03 §2` · `D04 T02 §1`                                                                                                                                                                        |
| Saves never damage the user's file                                                                                                                | `D02 T04 §1` · `D01 T02 §5` · `D03 T04 §2`                                                                                                                                                                                                      |
| A crash loses nothing                                                                                                                             | `D02 T04 §5` · `D03 T04 §6`                                                                                                                                                                                                                     |
| Formats are proven, not assumed                                                                                                                   | `D02 T04 §2` · `D03 T02 §4` · `D03 T04 §2`-`§5` · `D04 T01 §4` · `D04 T02 §2` · `D02 T14 §2` · `D02 T14 §6` · `D02 T14 §12` · `D03 T17 §2` · `D03 T17 §4` · `D03 T17 §5` · `D03 T17 §6`                                                         |
| No menu item silently does nothing                                                                                                                | `D02 T03 §5` · `D03 T06 §2`                                                                                                                                                                                                                     |
| Originals are never written                                                                                                                       | `D04 T01 §6` · `D04 T01 §11` · `D04 T02 §1`                                                                                                                                                                                                     |
| It looks like one suite                                                                                                                           | `standards/shared.md` (design contract) · `D01 T01 §3`                                                                                                                                                                                          |
| It works without a mouse or eyes                                                                                                                  | `D02 T06 §17` · `D03 T07 §16` · `D04 T02 §9`                                                                                                                                                                                                    |
| Each app ships alone, proven on a clean machine                                                                                                   | `D05 T01 §1` · `D02 T05 §4` · `D03 T06 §3` · `D04 T02 §8`                                                                                                                                                                                       |
| The suite ships together without re-versioning                                                                                                    | `D05 T01 §6`                                                                                                                                                                                                                                    |
| Users can learn it                                                                                                                                | `D06 T01 §1`-`§4`                                                                                                                                                                                                                               |
| Nodus covers every CorelDRAW and Illustrator capability in the parity catalog                                                                     | `D00 T01 §6` (the catalog gate) · `D02 T17 §1`-`§10` (each release reconciles its phase)                                                                                                                                                        |
| Nodus opens and saves Illustrator and CorelDRAW files                                                                                             | `D02 T14 §3` · `D02 T14 §4` · `D02 T14 §5` · `D02 T14 §6` · `D02 T14 §7` · `D02 T14 §8`                                                                                                                                                         |
| Print and PDF output are prepress-grade                                                                                                           | `D02 T13 §5` · `D02 T13 §7` · `D02 T13 §14` · `D02 T13 §15`                                                                                                                                                                                     |
| AI results are editable, undoable, and reproducible                                                                                               | `D01 T05 §3` · `D02 T15 §1` · `D02 T15 §2` · `D02 T15 §6` · `D03 T19 §1` · `D03 T19 §2`                                                                                                                                                         |
| Nothing leaves the machine without an explicit user action                                                                                        | `D01 T05 §2` · `D01 T05 §4` · `D03 T19 §1`                                                                                                                                                                                                      |
| Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog                                                           | `D00 T01 §7` (the catalog gate) · `D03 T21 §1`-`§12` (each release reconciles its phase)                                                                                                                                                        |
| Imago round-trips Photoshop documents: PSD and PSB open and save with layers, masks, adjustments, styles, text, and smart objects live            | `D03 T17 §2` · `D03 T17 §13` · `D03 T17 §3`                                                                                                                                                                                                     |
| Imago opens and saves GIMP's XCF                                                                                                                  | `D03 T17 §4` · `D03 T17 §14`                                                                                                                                                                                                                    |
| Editing stays non-destructive: adjustment layers, smart and live filters, masks, and linked content never overwrite pixels until the user applies | `D03 T08 §1` · `D03 T09 §3` · `D03 T09 §9` · `D03 T11 §1` · `D03 T14 §1`                                                                                                                                                                        |
| AI results in Imago are new layers and masks, undoable, and reproducible                                                                          | `D03 T19 §1` · `D03 T19 §2` · `D03 T19 §3` · `D03 T19 §6`                                                                                                                                                                                       |

---

## Where the project stands

Nothing in this plan has been built, but the tree is not empty.

**Nodus** (imported from Bezier with history under `src/Nodus/`, still named `Bezier.*`) is a working WPF vector editor: a SkiaSharp canvas, SVG import and export, select, pen, shape, text, zoom, and pan tools, an undo history, and 968 test methods. Measured on 2026-09-26, it is also mostly unwired: 25 of 31 Core services are referenced only by tests, 26 Object and Path menu commands only set status text, resize and rotate are not undoable, the composition root registers one type, it never writes a log file, and it builds with 334 warnings excused. Its legacy roadmap claims about 420 items done; many of those are code nobody can reach.

**Imago** (imported under `src/Imago/`) has a sound core model (layers, masks, selections, tiles, color, history) with 41 test methods, a WPF shell still built on WPF-UI, a document service that pretends, and no rendering, tools, or codecs. A local branch carries a December 2025 snapshot with a canvas, ruler, and a WPF-UI-free main window that `D03 T01 §2` ports.

**Lumen** has no code; it is planned in full in `todo/04-lumen/`.

**Nodus parity** is planned, not built: on 2026-09-26 the operator decided Nodus gets every CorelDRAW and every Illustrator feature, the catalog in [`../docs/parity/nodus-parity.md`](../docs/parity/nodus-parity.md) routes each of their 4,335 inventory rows to a section, a backlog entry, an exclusion, or another app, and Phases 4 to 13 run the sections between Nodus 0.1.0 and Imago's foundation.

**Imago parity** is planned, not built: the same day the operator decided Imago gets every Photoshop feature and those of at least two other popular raster editors, chosen as Affinity Photo (Affinity 3.3) and GIMP 3.2.6; the catalog in [`../docs/parity/imago-parity.md`](../docs/parity/imago-parity.md) routes each of their 10,829 inventory rows to a section, a backlog entry, an exclusion, or another app, and Phases 16 to 27 run the sections between Imago 0.1.0 and Lumen's foundation. Scripting, macros, batch processing, video, and animation are deferred to after the first release (backlog B-041 to B-044), with scripting and macros as one suite-wide system.

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
| [ ] | `D00 T01 §6` | The parity catalog validator                        |  19   |
| [ ] | `D00 T01 §7` | The validator reads the Imago parity catalog        |  22   |
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
| [ ] | `D02 T02 §2` | One SVG render path                                |   6   |
| [ ] | `D02 T01 §6` | SkiaSharp 4                                        |   6   |
| [ ] | `D02 T01 §7` | Warnings are errors in Nodus                       |   4   |
| [ ] | `D02 T02 §3` | Selection has one owner                            |   5   |
| [ ] | `D02 T03 §1` | Undo for resize and rotate                         |   6   |
| [ ] | `D02 T03 §2` | Split the main window view model                   |   7   |
| [ ] | `D02 T04 §1` | Atomic save and dirty tracking                     |   8   |
| [ ] | `D02 T04 §2` | SVG round-trip fidelity fixtures                   |   5   |
| [ ] | `D00 T02 §6` | xUnit v3                                           |   5   |

### Phase 3 -- Nodus 0.1.0: shared UI, complete editing, documents, release

With its foundation sound, Nodus becomes a complete first release: `Photon.UI` takes the controls and windows Nodus and Imago duplicate and the suite theme, single instance moves to `Photon.Core`, the triaged services are wired (arrange, align, booleans on `SKPath.Op`, layers, snapping, one keymap), the clipboard and property edits are undoable, exports and recovery work, every menu item works or names its owner, the About, shortcuts, and Help surfaces exist, the user guide is written, the SDK pin moves from the .NET 11 release candidate to GA (`D00 T02 §8`, which waits for the November 2026 GA and parks with that blocker named until then), the clean-machine procedure is proven on Windows 11, and `nodus-v0.1.0` ships.

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
| [ ] | `D00 T02 §8` | Pin the .NET 11 GA SDK                               |   6   |
| [ ] | `D05 T01 §1` | The clean-machine install procedure                  |   3   |
| [ ] | `D02 T05 §4` | Nodus 0.1.0                                          |   8   |

### Phase 4 -- Nodus parity I: document model, pages, layers, selection, and view

Parity starts where every later feature stands. This phase fixes how live objects persist in SVG (the `nodus:` namespace with an expanded fallback), gives the canvas a spatial index so documents with thousands of objects stay interactive, unifies CorelDRAW pages and Illustrator artboards into one model with its panel, and completes layers and the Objects panel, selection, isolation and focus mode, the Properties panel and property bar, rulers, guides, grids, snapping, view modes, history, and the New Document dialog with templates. Tabs and nested layers (`D02 T06 §7`) move here first because pages and layers build on them. It ends with `nodus-v0.2.0`.

|  ✔  | Section       | Deliverable                                                        | Items |
| :-: | ------------- | ------------------------------------------------------------------ | :---: |
| [ ] | `D02 T06 §7`  | Documents in tabs, saved layouts, nested layers                    |   5   |
| [ ] | `D02 T07 §1`  | The live-object contract in the nodus namespace                    |  20   |
| [ ] | `D02 T07 §2`  | Spatial index, culling, and dirty-region rendering                 |  19   |
| [ ] | `D02 T07 §3`  | Pages and artboards: one model, panel, and commands                |  22   |
| [ ] | `D02 T07 §4`  | Multipage views, page background, page numbers, navigation         |  23   |
| [ ] | `D02 T07 §5`  | Layers, master layers, lock and hide, the Objects panel            |  23   |
| [ ] | `D02 T07 §6`  | Selection: Select menu, Select Same, wand, lasso, saved selections |  19   |
| [ ] | `D02 T07 §7`  | Isolation mode and focus mode                                      |  11   |
| [ ] | `D02 T07 §8`  | The Properties panel and the contextual property bar               |  14   |
| [ ] | `D02 T07 §9`  | Rulers, units, drawing scale, and grids                            |  13   |
| [ ] | `D02 T07 §10` | Guides, the Guides panel, the measure tool, the Info panel         |  15   |
| [ ] | `D02 T07 §11` | Snapping modes, smart guides, dynamic and alignment guides         |  19   |
| [ ] | `D02 T07 §12` | View modes, zoom, rotate view, saved views, windows                |  18   |
| [ ] | `D02 T07 §13` | History panel, repeat, paste variants, quick duplicates            |  14   |
| [ ] | `D02 T07 §14` | New Document dialog, presets, templates, document information      |  20   |
| [ ] | `D02 T17 §1`  | Nodus 0.2.0 (Phase 4)                                              |  12   |

### Phase 5 -- Nodus parity II: drawing, paths, shapes, shaping, and transform

With the document model settled, the drawing layer catches up: every pen, curve, freehand, and smart-drawing tool, live shapes with editable parameters and live corners, full node editing, cutting and erasing, liquify and shape-editing brushes, Pathfinder and the shape builder, compound paths and clipping masks, precise transforms and Transform Each, align and distribute extensions, and dimensions and connectors. Path editing (`D02 T06 §2`) moves here first because node editing extends it. It ends with `nodus-v0.3.0`.

|  ✔  | Section       | Deliverable                                                                  | Items |
| :-: | ------------- | ---------------------------------------------------------------------------- | :---: |
| [ ] | `D02 T06 §2`  | Path editing: continue, join, break, reverse, simplify                       |   4   |
| [ ] | `D02 T08 §1`  | Pen, Bezier, and anchor point tools                                          |  14   |
| [ ] | `D02 T08 §2`  | Curvature, B-spline, polyline, 3-point, line and arc tools, parallel drawing |  14   |
| [ ] | `D02 T08 §3`  | Pencil, freehand, smooth, path eraser, join, and smart drawing               |  17   |
| [ ] | `D02 T08 §4`  | Live shapes and live corners                                                 |  20   |
| [ ] | `D02 T08 §5`  | Grid, graph paper, flare, common shapes, and impact tools                    |  16   |
| [ ] | `D02 T08 §6`  | Node editing: types, transforms, align, distribute, reduce                   |  20   |
| [ ] | `D02 T08 §7`  | Join curves, average, offset, anchors, clean up, split into grid             |  14   |
| [ ] | `D02 T08 §8`  | Knife, scissors, eraser, virtual segment delete, crop                        |  15   |
| [ ] | `D02 T08 §9`  | Liquify and shape-editing brushes                                            |  17   |
| [ ] | `D02 T08 §10` | Pathfinder, shaping, and the shape builder                                   |  18   |
| [ ] | `D02 T08 §11` | Compound paths, clipping masks, draw inside and behind, intertwine           |  14   |
| [ ] | `D02 T08 §12` | The Transform panel, dialogs, Transform Again, Transform Each                |  17   |
| [ ] | `D02 T08 §13` | Rotate, reflect, scale, shear, reshape, and free transform tools             |  14   |
| [ ] | `D02 T08 §14` | Align, distribute, arrange, and step and repeat extensions                   |  16   |
| [ ] | `D02 T08 §15` | Dimensions, connectors, and callouts                                         |  17   |
| [ ] | `D02 T17 §2`  | Nodus 0.3.0 (Phase 5)                                                        |  12   |

### Phase 6 -- Nodus parity III: color, fills, strokes, brushes, transparency, styles, and symbols

Appearance comes next because every effect and every format carries it. `Photon.Core` gains its color-management engine first, then Nodus gets the full color model (CMYK, Lab, spot, global), the color panel and pickers, swatches and palettes, color styles and harmonies, Recolor Artwork, every gradient kind including mesh, pattern and texture fills, complete strokes with arrowheads and variable width, the Appearance stack, graphic and object styles, the brush engine with every brush kind, every blend and merge mode with opacity masks, and symbols with overrides and libraries (after `D02 T06 §11`). It ends with `nodus-v0.4.0`.

|  ✔  | Section       | Deliverable                                                                                                  | Items |
| :-: | ------------- | ------------------------------------------------------------------------------------------------------------ | :---: |
| [ ] | `D02 T06 §11` | Symbols and the asset library                                                                                |   3   |
| [ ] | `D01 T04 §1`  | The engine decision, the lcms2 wrapper, profiles, the profile store, and RGB, CMYK, gray, and Lab transforms |  18   |
| [ ] | `D01 T04 §2`  | Rendering intents, black point compensation, proofing transforms, and gamut checks                           |  14   |
| [ ] | `D02 T09 §1`  | The color model: RGB, CMYK, HSB, Lab, grayscale, spot, global, and tints                                     |  13   |
| [ ] | `D02 T09 §2`  | The Color panel, color picker, recent colors, and eyedroppers                                                |  17   |
| [ ] | `D02 T09 §3`  | The Swatches panel, document palette, and color groups                                                       |  14   |
| [ ] | `D02 T09 §4`  | The palette bar, palette editor, color libraries, and palette files                                          |  18   |
| [ ] | `D02 T09 §5`  | Color styles, harmonies, and the color guide                                                                 |  15   |
| [ ] | `D02 T09 §6`  | Recolor Artwork, Edit Colors, and find and replace color                                                     |  14   |
| [ ] | `D02 T09 §7`  | The gradient model: linear, radial, conical, rectangular, stops, repeat, and interpolation                   |  14   |
| [ ] | `D02 T09 §8`  | The gradient tool, interactive fill, stroke gradients, and freeform gradients                                |  15   |
| [ ] | `D02 T09 §9`  | Gradient mesh and mesh fill                                                                                  |  13   |
| [ ] | `D02 T09 §10` | Pattern fills and pattern editing                                                                            |  12   |
| [ ] | `D02 T09 §11` | Texture and procedural fills, and the fill library                                                           |  13   |
| [ ] | `D02 T09 §12` | The Stroke panel: caps, joins, alignment, dashes, arrowheads, and line styles                                |  16   |
| [ ] | `D02 T09 §13` | The width tool and variable outlines                                                                         |  11   |
| [ ] | `D02 T09 §14` | The Appearance panel: stacked fills, strokes, and effects                                                    |  14   |
| [ ] | `D02 T09 §15` | Graphic styles, object styles, style sets, and default properties                                            |  15   |
| [ ] | `D02 T09 §16` | The brush engine, art brushes, and pattern brushes                                                           |  14   |
| [ ] | `D02 T09 §17` | Scatter, sprayer, and calligraphic brushes, the paintbrush, and the blob brush                               |  14   |
| [ ] | `D02 T09 §18` | Bristle and painterly brushes, and brush libraries                                                           |  19   |
| [ ] | `D02 T09 §19` | Opacity and blend modes                                                                                      |  11   |
| [ ] | `D02 T09 §20` | Opacity masks, fountain and pattern transparency, knockout, and feather                                      |  14   |
| [ ] | `D02 T09 §21` | Symbols: dynamic symbols, 9-slice scaling, registration, nesting, and linked libraries                       |  15   |
| [ ] | `D02 T09 §22` | Symbolism tools and the symbol sprayer                                                                       |  11   |
| [ ] | `D02 T17 §3`  | Nodus 0.4.0 (Phase 6)                                                                                        |  12   |

### Phase 7 -- Nodus parity IV: type, tables, and graphs

Type is its own discipline, so it gets its own phase: HarfBuzz shaping with bidirectional and CJK support, the rich text model, fonts and substitution, character, OpenType, and paragraph formatting, frames, threading and wrap, type on a path, text commands, styles, writing tools and text import, then tables and graphs, which are built from text and appearance. Area text and text on a path (`D02 T06 §3`) move here first. It ends with `nodus-v0.5.0`.

|  ✔  | Section       | Deliverable                                                                            | Items |
| :-: | ------------- | -------------------------------------------------------------------------------------- | :---: |
| [ ] | `D02 T06 §3`  | Text: area text, text on path, text to path                                            |   4   |
| [ ] | `D02 T10 §1`  | The text shaping engine: HarfBuzzSharp, bidi, script runs, and font fallback           |  23   |
| [ ] | `D02 T10 §2`  | The rich text model and text objects: point, area, path, and vertical                  |  24   |
| [ ] | `D02 T10 §3`  | Fonts: the font list, filters, samples, and missing-font substitution                  |  28   |
| [ ] | `D02 T10 §4`  | Character formatting                                                                   |  18   |
| [ ] | `D02 T10 §5`  | OpenType features, glyphs, variable fonts, and glyph snapping                          |  26   |
| [ ] | `D02 T10 §6`  | Paragraph formatting, composers, justification, and hyphenation                        |  19   |
| [ ] | `D02 T10 §7`  | Tabs, drop caps, and bullets and numbering                                             |  15   |
| [ ] | `D02 T10 §8`  | Area text frames, columns, threading, and text wrap                                    |  21   |
| [ ] | `D02 T10 §9`  | Type on a path options and effects                                                     |  14   |
| [ ] | `D02 T10 §10` | Vertical, CJK, and right-to-left type                                                  |  17   |
| [ ] | `D02 T10 §11` | Text commands: find and replace, change case, special characters, and placeholder text |  20   |
| [ ] | `D02 T10 §12` | Character, paragraph, and frame styles                                                 |  13   |
| [ ] | `D02 T10 §13` | Writing tools, and text import and export                                              |  25   |
| [ ] | `D02 T10 §14` | Tables                                                                                 |  22   |
| [ ] | `D02 T10 §15` | Graphs                                                                                 |  17   |
| [ ] | `D02 T17 §4`  | Nodus 0.5.0 (Phase 7)                                                                  |  12   |

### Phase 8 -- Nodus parity V: interactive and live effects

Effects sit on the Appearance stack and the live-object contract, both shipped by now. This phase builds the effect framework and then every interactive effect both competitors ship: blend, contour, envelope and warp, distort, shadows and glows and bevels, 3D extrude and 3D and Materials, lenses, PowerClip, symmetry, the perspective grid and perspective objects, puppet warp, Live Paint, repeats and objects on a path, and path effects. It ends with `nodus-v0.6.0`.

|  ✔  | Section       | Deliverable                                                                                  | Items |
| :-: | ------------- | -------------------------------------------------------------------------------------------- | :---: |
| [ ] | `D02 T11 §1`  | The live-effect framework: effect stack, parameters, copy, clone, clear, and expand          |  19   |
| [ ] | `D02 T11 §2`  | Blend: tool, steps, spacing, easing, and color acceleration                                  |  17   |
| [ ] | `D02 T11 §3`  | Blend on a path, node mapping, split, fuse, compound blends, and presets                     |  15   |
| [ ] | `D02 T11 §4`  | Contour                                                                                      |  15   |
| [ ] | `D02 T11 §5`  | Envelope distort and warp                                                                    |  19   |
| [ ] | `D02 T11 §6`  | The distort tool and Distort & Transform effects                                             |  14   |
| [ ] | `D02 T11 §7`  | Drop, inner, perspective, and block shadows                                                  |  17   |
| [ ] | `D02 T11 §8`  | Glows, feather, scribble, round corners, and bevels                                          |  14   |
| [ ] | `D02 T11 §9`  | 3D extrude and revolve: geometry, lighting, bevels, and vanishing points                     |  18   |
| [ ] | `D02 T11 §10` | 3D and Materials: inflate, plane, materials, mapped art, ray-traced rendering, and 3D export |  25   |
| [ ] | `D02 T11 §11` | Lenses                                                                                       |  15   |
| [ ] | `D02 T11 §12` | PowerClip frames                                                                             |  15   |
| [ ] | `D02 T11 §13` | Symmetry drawing mode                                                                        |  14   |
| [ ] | `D02 T11 §14` | The perspective grid and drawing planes                                                      |  15   |
| [ ] | `D02 T11 §15` | Perspective objects and the Add Perspective effect                                           |  17   |
| [ ] | `D02 T11 §16` | Puppet warp                                                                                  |  13   |
| [ ] | `D02 T11 §17` | Live Paint and smart fill                                                                    |  15   |
| [ ] | `D02 T11 §18` | Repeats and objects on a path                                                                |  16   |
| [ ] | `D02 T11 §19` | Path effects: convert to shape, offset, outline, and pathfinder effects                      |  13   |
| [ ] | `D02 T17 §5`  | Nodus 0.6.0 (Phase 8)                                                                        |  12   |

### Phase 9 -- Nodus parity VI: bitmaps, tracing, and the shared pixel engine

Bitmaps arrive once vectors are complete. `Photon.Core` gains the pixel engine the operator placed there for the whole suite (buffers, resampling, dithering, adjustments, and every bitmap effect family), and Nodus gets bitmap objects, the non-destructive effect stack, the adjustment lab, tracing (Image Trace and PowerTRACE), photo-based artwork, the Links panel, and SVG filters. Placing images (`D02 T06 §14`) moves here first because bitmap objects need it. It ends with `nodus-v0.7.0`.

|  ✔  | Section       | Deliverable                                                                                | Items |
| :-: | ------------- | ------------------------------------------------------------------------------------------ | :---: |
| [ ] | `D02 T06 §14` | More formats and the export dialog                                                         |   4   |
| [ ] | `D01 T03 §1`  | Pixel buffers, the effect contract, and the golden harness                                 |  20   |
| [ ] | `D01 T03 §2`  | Resampling, rotation, straighten, perspective, and lens correction                         |  14   |
| [ ] | `D01 T03 §3`  | Palette quantization and dithering                                                         |  16   |
| [ ] | `D01 T03 §4`  | Tonal adjustments                                                                          |  16   |
| [ ] | `D01 T03 §5`  | Color adjustments                                                                          |  15   |
| [ ] | `D01 T03 §6`  | Blur, sharpen, and noise                                                                   |  17   |
| [ ] | `D01 T03 §7`  | Distort and 3D-style effects                                                               |  15   |
| [ ] | `D01 T03 §8`  | Artistic and art-stroke effects                                                            |  16   |
| [ ] | `D01 T03 §9`  | Brush-stroke and sketch effects                                                            |  13   |
| [ ] | `D01 T03 §10` | Texture and creative effects                                                               |  15   |
| [ ] | `D01 T03 §11` | Camera, color-transform, edge, custom, pixelate, and video effects                         |  16   |
| [ ] | `D02 T12 §1`  | Bitmap objects: crop, resample, rasterize, convert to bitmap, color mask, and straighten   |  28   |
| [ ] | `D02 T12 §2`  | The effect stack on objects: FX panel, effect gallery, preview, flatten, and effect lenses |  21   |
| [ ] | `D02 T12 §3`  | Adjustments in Nodus: the Image Adjustment Lab and adjustment presets                      |  17   |
| [ ] | `D02 T12 §4`  | The tracing engine: outline tracing, color quantization, and stacking                      |  15   |
| [ ] | `D02 T12 §5`  | Centerline tracing, the Image Trace panel, and PowerTRACE                                  |  19   |
| [ ] | `D02 T12 §6`  | Photo artwork: Pointillizer, PhotoCocktail, Object Mosaic, and mockups                     |  17   |
| [ ] | `D02 T12 §7`  | The Links panel and linked sources                                                         |  20   |
| [ ] | `D02 T12 §8`  | SVG filter effects                                                                         |  13   |
| [ ] | `D02 T17 §6`  | Nodus 0.7.0 (Phase 9)                                                                      |  12   |

### Phase 10 -- Nodus parity VII: color management, print, prepress, and PDF

Output comes after everything it has to print exists. Bitmap color modes finish the color engine, then Nodus gets document color settings, the print dialog, marks and bleed, separations, soft proofing, overprint and trapping, flattening, preflight and packaging, PostScript options, imposition and layout styles, print merge with variable data, and its own PDF writer with PDF/X presets and interactivity. It ends with `nodus-v0.8.0`.

|  ✔  | Section       | Deliverable                                                                      | Items |
| :-: | ------------- | -------------------------------------------------------------------------------- | :---: |
| [ ] | `D01 T04 §3`  | Bitmap color modes, duotone, and multichannel, with the Nodus Duotone dialog     |  18   |
| [ ] | `D02 T13 §1`  | Document color settings: profiles, policies, assign, convert, and embed          |  20   |
| [ ] | `D02 T13 §2`  | The print dialog: printers, range, copies, placement, scaling, and preview       |  20   |
| [ ] | `D02 T13 §3`  | Print tiling, print styles, print to file, and print summaries                   |  11   |
| [ ] | `D02 T13 §4`  | Printer's marks and bleed                                                        |  14   |
| [ ] | `D02 T13 §5`  | Separations, halftone screens, and the ink manager                               |  16   |
| [ ] | `D02 T13 §6`  | Soft proofing, gamut warning, overprint preview, and separations preview         |  14   |
| [ ] | `D02 T13 §7`  | Overprint attributes and trapping                                                |  17   |
| [ ] | `D02 T13 §8`  | Transparency flattening and the flattener preview                                |  12   |
| [ ] | `D02 T13 §9`  | Preflight, Package, and Collect for Output                                       |  11   |
| [ ] | `D02 T13 §10` | PostScript output and driver compatibility options                               |  15   |
| [ ] | `D02 T13 §11` | Imposition, binding, and page placement                                          |  10   |
| [ ] | `D02 T13 §12` | Layout styles, labels, and banners                                               |  11   |
| [ ] | `D02 T13 §13` | Print merge and variable data                                                    |  19   |
| [ ] | `D02 T13 §14` | The PDF writer: spot colors, layers, and exact vector output                     |  17   |
| [ ] | `D02 T13 §15` | PDF presets and standards: PDF/X, PDF/A, compatibility, compression, and marks   |  16   |
| [ ] | `D02 T13 §16` | PDF interactivity and security: bookmarks, hyperlinks, tagged PDF, and passwords |  14   |
| [ ] | `D02 T17 §7`  | Nodus 0.8.0 (Phase 10)                                                           |  12   |

### Phase 11 -- Nodus parity VIII: file formats, export, and web

Formats come after the object model they must carry is complete, so each reader and writer maps onto real Nodus objects and owes a fidelity proof: SVG options, PDF import, Illustrator `.ai` import and export, CorelDRAW `.cdr` import and export, EPS, DXF and DWG, metafiles, raster formats, PSD, office documents, Export for Screens and the export list, Export for Web, slices and hyperlinks, pixel-perfect drawing, and clipboard and OLE exchange. It ends with `nodus-v0.9.0`.

|  ✔  | Section       | Deliverable                                                                 | Items |
| :-: | ------------- | --------------------------------------------------------------------------- | :---: |
| [ ] | `D02 T14 §1`  | SVG options: SVGZ, styling modes, CSS export, and SVG code                  |  17   |
| [ ] | `D02 T14 §2`  | PDF import                                                                  |  19   |
| [ ] | `D02 T14 §3`  | Illustrator import: PDF-compatible .ai files                                |   9   |
| [ ] | `D02 T14 §4`  | Illustrator import: private data and legacy PostScript .ai                  |   9   |
| [ ] | `D02 T14 §5`  | Illustrator .ai export                                                      |  13   |
| [ ] | `D02 T14 §6`  | CorelDRAW import: containers, pages, layers, and objects                    |  14   |
| [ ] | `D02 T14 §7`  | CorelDRAW import: fills, outlines, text, effects, and bitmaps; CMX          |  10   |
| [ ] | `D02 T14 §8`  | CorelDRAW CDR and CMX export                                                |  12   |
| [ ] | `D02 T14 §9`  | EPS and PostScript import and export                                        |  15   |
| [ ] | `D02 T14 §10` | DXF and DWG import and export                                               |  12   |
| [ ] | `D02 T14 §11` | EMF, WMF, CGM, HPGL, and WPG                                                |  12   |
| [ ] | `D02 T14 §12` | Raster formats: import and export through WIC                               |  25   |
| [ ] | `D02 T14 §13` | Photoshop PSD import and export                                             |  12   |
| [ ] | `D02 T14 §14` | Office and text documents, Export For Office, and font export               |  16   |
| [ ] | `D02 T14 §15` | Export for Screens, asset export, and the export list                       |  20   |
| [ ] | `D02 T14 §16` | Export for Web: optimized preview and web formats                           |  15   |
| [ ] | `D02 T14 §17` | Slices, image maps, hyperlinks, rollovers, and SVG interactivity            |  20   |
| [ ] | `D02 T14 §18` | Pixel-perfect drawing, pixel preview, and object hinting                    |  12   |
| [ ] | `D02 T14 §19` | Clipboard formats, OLE objects, placing multiple files, and scanner acquire |  17   |
| [ ] | `D02 T17 §8`  | Nodus 0.9.0 (Phase 11)                                                      |  12   |

### Phase 12 -- Nodus AI: editable, suite-aware, reproducible

The AI features are Nodus's own and come after the object model, formats, and tracing they produce and consume. `Photon.Core` and `Photon.UI` gain the shared AI core (OpenRouter with the user's own key, DPAPI key storage, the explicit-send gate, provenance, and the brand kit), then Nodus maps every competitor AI job to an editable, undoable, reproducible feature: vector generation, patterns and fills, expand and bleed, recolor, the assistant, text rewriting and retyping, image generation and cleanup, concept to vector, and the suite pipeline. It ends with `nodus-v0.10.0`.

|  ✔  | Section       | Deliverable                                                                   | Items |
| :-: | ------------- | ----------------------------------------------------------------------------- | :---: |
| [ ] | `D01 T05 §1`  | The OpenRouter client: chat, structured output, images, streaming, and models |  22   |
| [ ] | `D01 T05 §2`  | API keys with DPAPI and the AI settings contract                              |  15   |
| [ ] | `D01 T05 §3`  | The AI provenance record                                                      |  14   |
| [ ] | `D01 T05 §4`  | The explicit-send gate and the shared AI surfaces in Photon.UI                |  17   |
| [ ] | `D01 T05 §5`  | The suite brand kit: shared palettes and styles                               |  13   |
| [ ] | `D02 T15 §1`  | AI in Nodus: the AI menu, settings, usage, and the provenance panel           |  21   |
| [ ] | `D02 T15 §2`  | Generate vector artwork from a prompt                                         |  18   |
| [ ] | `D02 T15 §3`  | Generate patterns and fill shapes                                             |  11   |
| [ ] | `D02 T15 §4`  | Generative expand and print bleed                                             |  10   |
| [ ] | `D02 T15 §5`  | AI recolor and palettes from the brand kit                                    |   9   |
| [ ] | `D02 T15 §6`  | The AI assistant: prompt to edit with undoable commands                       |  15   |
| [ ] | `D02 T15 §7`  | AI text: rewrite, translate, proofread, fit, and retype                       |  12   |
| [ ] | `D02 T15 §8`  | AI images: generate, remix, and reference images                              |  11   |
| [ ] | `D02 T15 §9`  | AI image cleanup: remove background, upscale, repair, and art style           |  10   |
| [ ] | `D02 T15 §10` | Concept to vector: sketches and images to structured vectors                  |  11   |
| [ ] | `D02 T15 §11` | The suite pipeline: Lumen to Imago to Nodus hand-offs and shared brand kits   |  15   |
| [ ] | `D02 T17 §9`  | Nodus 0.10.0 (Phase 12)                                                       |  12   |

### Phase 13 -- Nodus parity IX: workspace, customization, preferences, and Nodus 1.0.0

The last parity phase customizes and audits the whole surface once it exists: the command palette and Preferences (`D02 T06 §12`, `§13`) move here, then workspaces, toolbars, menus and shortcut sets, the preference pages, UI appearance and diagnostics, the welcome screen and navigator, pen and touch input, hints and the project timer, object data and find and replace, QR codes and barcodes, and the accessibility and localization audit (`D02 T06 §17`) over every parity surface. It ends with `nodus-v1.0.0`, which declares the parity catalog complete.

|  ✔  | Section       | Deliverable                                                        | Items |
| :-: | ------------- | ------------------------------------------------------------------ | :---: |
| [ ] | `D02 T06 §12` | The command palette and the on-canvas HUD                          |   4   |
| [ ] | `D02 T06 §13` | Preferences and shortcut remapping                                 |   4   |
| [ ] | `D02 T16 §1`  | Workspaces: presets, save, reset, import, and export               |  16   |
| [ ] | `D02 T16 §2`  | Toolbox, toolbars, property bar, and status bar customization      |  17   |
| [ ] | `D02 T16 §3`  | Menus, context menus, command search, and shortcut sets            |  17   |
| [ ] | `D02 T16 §4`  | Preferences: general, selection and nodes, display, and units      |  16   |
| [ ] | `D02 T16 §5`  | Preferences: files, backup, performance, GPU, and warnings         |  16   |
| [ ] | `D02 T16 §6`  | UI appearance, scaling, and diagnostics                            |  16   |
| [ ] | `D02 T16 §7`  | The welcome screen and the navigator                               |  14   |
| [ ] | `D02 T16 §8`  | Pen, touch, and Surface Dial input                                 |  14   |
| [ ] | `D02 T16 §9`  | Hints, in-app learning, and the project timer                      |  14   |
| [ ] | `D02 T16 §10` | Object data, the Object Data Manager, and find and replace objects |  16   |
| [ ] | `D02 T16 §11` | QR codes and barcodes                                              |  13   |
| [ ] | `D02 T06 §17` | Accessibility and localization                                     |   4   |
| [ ] | `D02 T17 §10` | Nodus 1.0.0 (Phase 13)                                             |  14   |

### Phase 14 -- Imago foundation: snapshot port, WPF-UI out, tiles, rendering

Imago starts once Nodus has shipped `nodus-v1.0.0` at the end of the parity phases. The December 2025 snapshot's canvas, ruler, and container are ported onto `main` and the branch deleted, WPF-UI leaves the suite for good, Imago starts through the shared logging and settings, its layers become tile-backed, the viewport renders the tiled composite at any zoom, the render graph composites every blend mode against reference goldens, and a ComputeSharp path matches the CPU. The codec decision is made here so file work can start the moment editing exists.

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

### Phase 15 -- Imago 0.1.0: editing, files, filters, release

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
| [ ] | `D03 T03 §8` | Fill, gradient, eyedropper, and the color panel   |   4   |
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

### Phase 16 -- Imago parity I: document, canvas, view, history, and layers

Parity starts where every later feature stands. This phase fixes how live content persists in `.imago` (the `imago:` namespace beside a rendered PNG fallback, so GIMP and Krita still open every file), completes the document model (8, 16, and 32-bit float, precision, pixel aspect), new-document presets and templates, every view (zoom, rotate, flip, screen modes, windows, view modes, display filters, the navigator), rulers, guides, grids, snapping, measurement, the info and histogram panels and scopes, snapshots and non-linear history, the Image menu, paste variants, and crop, then the layer model with every layer kind, the Layers panel and Layer menu, masks, clipping and vector masks, blending options with Blend If, and every blend mode the three competitors ship. It ends with `imago-v0.2.0`.

|  ✔  | Section       | Deliverable                                                          | Items |
| :-: | ------------- | -------------------------------------------------------------------- | :---: |
| [ ] | `D03 T08 §1`  | The document model and the native-format contract for live content   |  27   |
| [ ] | `D03 T08 §2`  | New document, presets, and templates                                 |  22   |
| [ ] | `D03 T08 §3`  | Zoom, rotate view, flip view, and screen modes                       |  29   |
| [ ] | `D03 T08 §10` | Windows, arrangement, view modes, display filters, and the navigator |  17   |
| [ ] | `D03 T08 §4`  | Rulers, units, guides, grids, and snapping                           |  28   |
| [ ] | `D03 T08 §5`  | Measure, protractor, count, and notes                                |  19   |
| [ ] | `D03 T08 §11` | Info, histogram, sample points, and scopes                           |  23   |
| [ ] | `D03 T08 §6`  | History extensions: snapshots, non-linear history, and saved history |  21   |
| [ ] | `D03 T08 §7`  | The Image menu: canvas, rotation, trim, reveal, and resampling       |  25   |
| [ ] | `D03 T08 §8`  | Clipboard and paste variants                                         |  19   |
| [ ] | `D03 T08 §9`  | Crop and straighten extensions                                       |  19   |
| [ ] | `D03 T09 §1`  | Every layer kind, locks, labels, tags, and panel filtering           |  20   |
| [ ] | `D03 T09 §2`  | Layers panel selection, linking, visibility, order, and options      |  21   |
| [ ] | `D03 T09 §14` | Merge, stamp, rasterize with revert, matting, and boundaries         |  21   |
| [ ] | `D03 T09 §3`  | Layer masks, mask stacks, and live masks                             |  20   |
| [ ] | `D03 T09 §4`  | Clipping masks, child clipping, and vector masks                     |  15   |
| [ ] | `D03 T09 §5`  | Blending options, Blend If, and blend ranges                         |  18   |
| [ ] | `D03 T09 §6`  | GIMP, Affinity, and Porter-Duff blend modes                          |  18   |
| [ ] | `D03 T21 §1`  | Imago 0.2.0 (Phase 16)                                               |  14   |

### Phase 17 -- Imago parity II: selection, channels, styles, smart objects, and artboards

With layers and masks in place, selection catches up: soft and saved selections, every marquee and lasso, the magic wand and selection by color, Color Range, the local segmentation engine and Focus Area, quick selection, foreground select and intelligent scissors, Select and Mask, modify and transform selection, and the Channels panel with spot channels and quick mask. The same phase finishes the layer stack's richer content: layer styles, embedded and linked smart objects, layer comps, align and distribute, and artboards. It ends with `imago-v0.3.0`.

|  ✔  | Section       | Deliverable                                                                      | Items |
| :-: | ------------- | -------------------------------------------------------------------------------- | :---: |
| [ ] | `D03 T10 §1`  | The selection model: soft selections, saved selections, and the selection editor |  20   |
| [ ] | `D03 T10 §2`  | Marquee and lasso extensions                                                     |  16   |
| [ ] | `D03 T10 §3`  | Magic wand and select by color                                                   |  16   |
| [ ] | `D03 T10 §4`  | Color Range and tonal selection                                                  |  17   |
| [ ] | `D03 T10 §6`  | The local segmentation engine and Focus Area                                     |  16   |
| [ ] | `D03 T10 §5`  | Quick selection, selection brush, foreground select, and intelligent scissors    |  13   |
| [ ] | `D03 T10 §7`  | Select and Mask and refine selection                                             |  21   |
| [ ] | `D03 T10 §8`  | Modify and transform selection                                                   |  15   |
| [ ] | `D03 T10 §9`  | Select menu extensions                                                           |  10   |
| [ ] | `D03 T10 §10` | The Channels panel, spot channels, and quick mask options                        |  21   |
| [ ] | `D03 T09 §7`  | Layer styles I: framework, shadows, glows, stroke, satin                         |  26   |
| [ ] | `D03 T09 §8`  | Layer styles II: bevel, overlays, contours, Styles panel, ASL                    |  22   |
| [ ] | `D03 T09 §9`  | Embedded smart objects                                                           |  16   |
| [ ] | `D03 T09 §10` | Linked smart objects, link layers, and the Resource Manager                      |  14   |
| [ ] | `D03 T09 §11` | Layer comps and states                                                           |  13   |
| [ ] | `D03 T09 §12` | Align, distribute, and move-tool extensions                                      |  16   |
| [ ] | `D03 T09 §13` | Artboards with constraints                                                       |  16   |
| [ ] | `D03 T21 §2`  | Imago 0.3.0 (Phase 17)                                                           |  14   |

### Phase 18 -- Imago parity III: adjustment layers, adjustments, modes, and color

Adjustments become non-destructive layers over the suite pixel engine: every tonal and color adjustment of Photoshop, Affinity, and the GIMP Colors menu, auto corrections, analysis, every image mode and bit depth through the suite color engine, channel operations with Apply Image and Calculations, the color panels, pickers, samplers, and swatches with palette files and color libraries from user files. It ends with `imago-v0.4.0`.

|  ✔  | Section       | Deliverable                                                                                                | Items |
| :-: | ------------- | ---------------------------------------------------------------------------------------------------------- | :---: |
| [ ] | `D03 T11 §1`  | Adjustment layers and the Adjustments and Properties panels                                                |  26   |
| [ ] | `D03 T11 §2`  | Tonal adjustment extensions                                                                                |  26   |
| [ ] | `D03 T11 §3`  | Color adjustments I: hue, balance, vibrance, black and white, photo filter, selective color                |  16   |
| [ ] | `D03 T11 §4`  | Color adjustments II: channel mixer, LUTs, gradient map, match and replace color, OCIO                     |  23   |
| [ ] | `D03 T11 §5`  | Color adjustments III: threshold, posterize, invert, desaturate, color to alpha, and GIMP color operations |  26   |
| [ ] | `D03 T11 §6`  | Color analysis                                                                                             |   8   |
| [ ] | `D03 T11 §7`  | Image modes and bit depth                                                                                  |  23   |
| [ ] | `D03 T11 §8`  | Channel operations: split, merge, decompose, compose, apply image, calculations                            |  13   |
| [ ] | `D03 T11 §9`  | Color panels, pickers, eyedroppers, and color samplers                                                     |  21   |
| [ ] | `D03 T11 §10` | Swatches, palettes, and color libraries                                                                    |  20   |
| [ ] | `D03 T21 §3`  | Imago 0.4.0 (Phase 18)                                                                                     |  14   |

### Phase 19 -- Imago parity IV: the brush engine, painting, fills, gradients, and patterns

Painting is judged on its brush engine, so it gets its own phase: tips, smoothing, wet media, full dynamics, presets with ABR, Affinity, and GIMP brush import, MyPaint brushes, every painting tool, mixer and smudge, erasers, fill and stroke including GIMP's line-art fill, gradients with an on-canvas editor, patterns, and symmetry painting. It ends with `imago-v0.5.0`.

|  ✔  | Section       | Deliverable                                                 | Items |
| :-: | ------------- | ----------------------------------------------------------- | :---: |
| [ ] | `D03 T12 §1`  | The brush engine I: tips, spacing, smoothing, and wet media |  20   |
| [ ] | `D03 T12 §2`  | The brush engine II: dynamics                               |  17   |
| [ ] | `D03 T12 §3`  | Brush presets, libraries, and tool presets                  |  24   |
| [ ] | `D03 T12 §4`  | MyPaint brushes                                             |  13   |
| [ ] | `D03 T12 §5`  | Painting tools and history brushes                          |  19   |
| [ ] | `D03 T12 §6`  | Mixer brush, smudge, and color replacement                  |  12   |
| [ ] | `D03 T12 §7`  | Erasers                                                     |  11   |
| [ ] | `D03 T12 §8`  | Fill and stroke                                             |  18   |
| [ ] | `D03 T12 §9`  | Gradients and the gradient editor                           |  24   |
| [ ] | `D03 T12 §10` | Patterns                                                    |  17   |
| [ ] | `D03 T12 §11` | Symmetry painting                                           |  11   |
| [ ] | `D03 T21 §4`  | Imago 0.5.0 (Phase 19)                                      |  14   |

### Phase 20 -- Imago parity V: retouching, content-aware tools, transform, warp, and liquify

Retouching builds on painting: clone and the clone source panel, healing, patch, blemish and inpainting, the content-aware engine for fill, scale, and move, toning tools, every transform tool of the three apps, warp, puppet warp and cage, perspective warp, Liquify, and frequency separation. It ends with `imago-v0.6.0`.

|  ✔  | Section       | Deliverable                                       | Items |
| :-: | ------------- | ------------------------------------------------- | :---: |
| [ ] | `D03 T13 §1`  | Clone stamp and the clone source panel            |  16   |
| [ ] | `D03 T13 §2`  | Healing, patch, blemish, inpainting, and red eye  |  18   |
| [ ] | `D03 T13 §3`  | The content-aware engine: fill, scale, and move   |  17   |
| [ ] | `D03 T13 §4`  | Toning and focus tools                            |  15   |
| [ ] | `D03 T13 §5`  | Free Transform and move-tool transform extensions |  18   |
| [ ] | `D03 T13 §11` | The GIMP transform tools                          |  16   |
| [ ] | `D03 T13 §6`  | Warp and mesh warp                                |  13   |
| [ ] | `D03 T13 §7`  | Puppet warp, cage transform, and pins             |  14   |
| [ ] | `D03 T13 §8`  | Perspective warp                                  |  11   |
| [ ] | `D03 T13 §9`  | Liquify                                           |  18   |
| [ ] | `D03 T13 §10` | Frequency separation and retouching workflows     |  11   |
| [ ] | `D03 T21 §5`  | Imago 0.6.0 (Phase 20)                            |  14   |

### Phase 21 -- Imago parity VI: filters I, the filter surfaces and the engine extensions for blur, sharpen, noise, distort, and pixelate

Filters come once the layer stack can host them non-destructively. The relocated filter-catalog section (`D03 T07 §3`) runs first, then `Photon.Core` gains the engine extensions contract and the blur, lens-blur, sharpen, denoise, distort, map, and pixelate families, and Imago gets smart filters and live filter layers, the Filter menu with generated dialogs for every engine effect, the Filter Gallery, the Blur Gallery surface, Lens Correction and Adaptive Wide Angle, and Vanishing Point. It ends with `imago-v0.7.0`.

|  ✔  | Section       | Deliverable                                                                                    | Items |
| :-: | ------------- | ---------------------------------------------------------------------------------------------- | :---: |
| [ ] | `D03 T07 §3`  | The rest of the filter catalog                                                                 |   4   |
| [ ] | `D01 T06 §1`  | The extensions contract: float processing, abyss policies, GEGL op ids, and on-canvas controls |  17   |
| [ ] | `D01 T06 §2`  | Blur extensions                                                                                |  18   |
| [ ] | `D01 T06 §3`  | Lens blur, bokeh, and the blur-gallery kernels                                                 |  18   |
| [ ] | `D01 T06 §4`  | Sharpen and deconvolution                                                                      |  17   |
| [ ] | `D01 T06 §5`  | Noise and denoise extensions                                                                   |  16   |
| [ ] | `D01 T06 §6`  | Distort and projection extensions                                                              |  22   |
| [ ] | `D01 T06 §7`  | Map extensions                                                                                 |  16   |
| [ ] | `D01 T06 §14` | Pixelate and halftone extensions                                                               |  12   |
| [ ] | `D03 T14 §1`  | Smart filters, live filter layers, and non-destructive layer filters                           |  24   |
| [ ] | `D03 T14 §2`  | The Filter menu, generated dialogs, presets, and Fade                                          |  22   |
| [ ] | `D03 T14 §3`  | The Filter Gallery                                                                             |   9   |
| [ ] | `D03 T14 §4`  | The Blur Gallery surface                                                                       |  14   |
| [ ] | `D03 T14 §6`  | Lens Correction and Adaptive Wide Angle                                                        |  22   |
| [ ] | `D03 T14 §7`  | Vanishing Point and live projections                                                           |  14   |
| [ ] | `D03 T21 §6`  | Imago 0.7.0 (Phase 21)                                                                         |  14   |

### Phase 22 -- Imago parity VII: filters II, render, light, stylize, artistic, generic, and GEGL

The second filter phase completes the long tail GIMP and GEGL bring: light and shadow, procedural noise, patterns and fractals, edges and stylize, the artistic set, generic and morphology filters, the lighting and flare surfaces, the GEGL operation tool and filter browser, GIMP's decor and combine effects as native commands, and Affinity's filter extras. It ends with `imago-v0.8.0`.

|  ✔  | Section       | Deliverable                                         | Items |
| :-: | ------------- | --------------------------------------------------- | :---: |
| [ ] | `D01 T06 §8`  | Light and shadow                                    |  23   |
| [ ] | `D01 T06 §9`  | Procedural noise and nature                         |  20   |
| [ ] | `D01 T06 §10` | Patterns and fractals                               |  18   |
| [ ] | `D01 T06 §11` | Edges and stylize                                   |  16   |
| [ ] | `D01 T06 §12` | Artistic extensions                                 |  18   |
| [ ] | `D01 T06 §13` | Generic, morphology, and channel math               |  23   |
| [ ] | `D03 T14 §5`  | Lighting and flare surfaces                         |  10   |
| [ ] | `D03 T14 §8`  | The GEGL operation tool and the filter browser      |   8   |
| [ ] | `D03 T14 §9`  | GIMP decor and combine effects as native commands   |  15   |
| [ ] | `D03 T14 §10` | Dedicated filter editors and Affinity filter extras |  17   |
| [ ] | `D03 T21 §7`  | Imago 0.8.0 (Phase 22)                              |  14   |

### Phase 23 -- Imago parity VIII: the develop engine, Camera Raw, HDR, panorama, stacks, and astrophotography

Photography gets its own phase. `Photon.Core` gains the scene-referred develop engine that Lumen will reuse, and Imago gets the Camera Raw filter and Affinity's Develop studio with local masks, 32-bit editing and HDR display, tone mapping, the alignment engine, Merge to HDR, panoramas, image stacks and auto-blend, focus merge, astrophotography stacking, and splitting scanned photos. RAW files themselves open once Lumen's decoder is shared (`D03 T07 §11`, Phase 31). It ends with `imago-v0.9.0`.

|  ✔  | Section       | Deliverable                                                               | Items |
| :-: | ------------- | ------------------------------------------------------------------------- | :---: |
| [ ] | `D01 T07 §1`  | The develop pipeline core: white balance, exposure, tone, and curves      |  29   |
| [ ] | `D01 T07 §2`  | Presence and color: texture, clarity, dehaze, color mixer, and grading    |  18   |
| [ ] | `D01 T07 §3`  | Detail and optics: sharpening, noise, grain, vignette, lens, and geometry |  25   |
| [ ] | `D01 T07 §4`  | The local masking engine                                                  |  19   |
| [ ] | `D01 T07 §5`  | Spot removal, red eye, and pet eye                                        |  13   |
| [ ] | `D01 T07 §6`  | Presets, snapshots, and XMP settings exchange                             |  16   |
| [ ] | `D03 T15 §1`  | The Camera Raw filter dialog                                              |  27   |
| [ ] | `D03 T15 §12` | The Develop studio and RAW layers                                         |  20   |
| [ ] | `D03 T15 §2`  | Develop masking and local adjustments surface                             |  14   |
| [ ] | `D03 T15 §4`  | 32-bit HDR editing and HDR display                                        |  19   |
| [ ] | `D03 T15 §3`  | Tone mapping and HDR Toning                                               |  20   |
| [ ] | `D03 T15 §5`  | The image alignment engine and auto-align layers                          |  16   |
| [ ] | `D03 T15 §6`  | Merge to HDR                                                              |  16   |
| [ ] | `D03 T15 §7`  | Panorama                                                                  |  18   |
| [ ] | `D03 T15 §8`  | Image stacks and auto-blend layers                                        |  19   |
| [ ] | `D03 T15 §9`  | Focus merge                                                               |  13   |
| [ ] | `D03 T15 §10` | Astrophotography stacking                                                 |  27   |
| [ ] | `D03 T15 §11` | Crop and straighten scanned photos                                        |  10   |
| [ ] | `D03 T21 §8`  | Imago 0.9.0 (Phase 23)                                                    |  14   |

### Phase 24 -- Imago parity IX: type, paths, shapes, and vectors

Type and vectors come after the layer stack and styles they live in. The suite text engine moves from Nodus to `Photon.Core` as Imago becomes its second consumer, and Imago gets text layers, character and paragraph formatting, OpenType and glyphs, styles and text commands, paths with geometry shared with Nodus, every pen and shape tool, vector layers, frames, and SVG output. It ends with `imago-v0.10.0`.

|  ✔  | Section      | Deliverable                                              | Items |
| :-: | ------------ | -------------------------------------------------------- | :---: |
| [ ] | `D03 T16 §1` | Text layers on the shared text engine                    |  27   |
| [ ] | `D03 T16 §5` | Paths, the Paths panel, and path geometry in Photon.Core |  28   |
| [ ] | `D03 T16 §2` | Character formatting, OpenType, glyphs, and fonts        |  26   |
| [ ] | `D03 T16 §3` | Paragraph formatting and text frames                     |  14   |
| [ ] | `D03 T16 §4` | Type styles and text commands                            |  20   |
| [ ] | `D03 T16 §6` | Pen and path editing tools                               |  22   |
| [ ] | `D03 T16 §7` | Shape layers, shape tools, and vector layers             |  30   |
| [ ] | `D03 T16 §8` | Frames and vector output                                 |  15   |
| [ ] | `D03 T21 §9` | Imago 0.10.0 (Phase 24)                                  |  14   |

### Phase 25 -- Imago parity X: formats, export, color management, and print

Formats come after the document model they must carry is complete, so each reader and writer maps onto real Imago content and owes a fidelity proof: the File menu, screenshots and scanners, PSD and PSB write with live content and full-fidelity read, XCF read and write, modern web formats, HDR and scientific formats, PDF, EPS, SVG, and metafiles, every common and legacy raster format, format options, and metadata; then export, Save for Web and slices, color settings and soft proofing, and print with its extras. It ends with `imago-v0.11.0`.

|  ✔  | Section       | Deliverable                                                              | Items |
| :-: | ------------- | ------------------------------------------------------------------------ | :---: |
| [ ] | `D03 T17 §1`  | File menu extensions: open, place, revert, close, and save a copy        |  27   |
| [ ] | `D03 T17 §12` | Create from clipboard, screenshots, scanners, URLs, and archives         |  16   |
| [ ] | `D03 T17 §2`  | PSD and PSB write: structure                                             |  18   |
| [ ] | `D03 T17 §13` | PSD write: live content and editability options                          |  18   |
| [ ] | `D03 T17 §3`  | PSD read fidelity: live adjustments, styles, text, and smart objects     |  13   |
| [ ] | `D03 T17 §4`  | GIMP XCF read                                                            |  16   |
| [ ] | `D03 T17 §14` | GIMP XCF write                                                           |  11   |
| [ ] | `D03 T17 §5`  | Modern web formats: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, QOI, JPEG XR   |  21   |
| [ ] | `D03 T17 §6`  | HDR and scientific formats                                               |  24   |
| [ ] | `D03 T17 §7`  | Document and vector formats: PDF, Photoshop PDF, EPS, SVG, and metafiles |  29   |
| [ ] | `D03 T17 §8`  | Common and legacy raster formats I                                       |  24   |
| [ ] | `D03 T17 §9`  | Legacy raster formats II and text and resource exports                   |  24   |
| [ ] | `D03 T17 §11` | JPEG, PNG, and TIFF option extensions                                    |  18   |
| [ ] | `D03 T17 §10` | Metadata: EXIF, IPTC, XMP, and File Info                                 |  25   |
| [ ] | `D03 T18 §1`  | Export As, Quick Export, and asset export                                |  27   |
| [ ] | `D03 T18 §2`  | Save for Web and the Export studio                                       |  28   |
| [ ] | `D03 T18 §3`  | Slices                                                                   |  14   |
| [ ] | `D03 T18 §4`  | Color settings, profiles, and display color management                   |  27   |
| [ ] | `D03 T18 §5`  | Soft proofing and gamut warning                                          |  15   |
| [ ] | `D03 T18 §6`  | Print                                                                    |  20   |
| [ ] | `D03 T18 §7`  | Print output extras, contact sheets, PDF presentation, and preflight     |  14   |
| [ ] | `D03 T21 §10` | Imago 0.11.0 (Phase 25)                                                  |  14   |

### Phase 26 -- Imago AI: editable, suite-aware, reproducible

The AI features are Imago's own and come after the layers, masks, selections, retouching, and formats they produce and consume. On the shared AI core, Imago maps every competitor AI job to a non-destructive, undoable, reproducible feature: the AI menu and provenance panel, the image-generation adapter, generative fill, remove, and expand, image generation, AI selection and masks, neural-filter equivalents, depth and relighting with honest limits, upscaling, distraction removal, the prompt-to-edit assistant, font matching and face landmarks, sky replacement, and the suite pipeline with the brand kit. It ends with `imago-v0.12.0`.

|  ✔  | Section       | Deliverable                                                          | Items |
| :-: | ------------- | -------------------------------------------------------------------- | :---: |
| [ ] | `D03 T19 §1`  | AI in Imago: the AI menu, settings, usage, and the provenance panel  |  22   |
| [ ] | `D03 T19 §2`  | The image-generation adapter                                         |  17   |
| [ ] | `D03 T19 §3`  | Generative fill and generative remove                                |  17   |
| [ ] | `D03 T19 §4`  | Generative expand                                                    |  12   |
| [ ] | `D03 T19 §5`  | Generate image, background, and similar                              |  15   |
| [ ] | `D03 T19 §6`  | AI selection: subject, sky, objects, and people                      |  20   |
| [ ] | `D03 T19 §15` | AI masks everywhere: detections, mask all objects, and develop masks |  13   |
| [ ] | `D03 T19 §7`  | Neural-filter equivalents                                            |  17   |
| [ ] | `D03 T19 §14` | Depth, portrait blur, and relighting                                 |  15   |
| [ ] | `D03 T19 §8`  | Upscale and enhance                                                  |  18   |
| [ ] | `D03 T19 §9`  | Distraction and object removal                                       |  15   |
| [ ] | `D03 T19 §10` | The Imago assistant: prompt to edit                                  |  15   |
| [ ] | `D03 T19 §11` | AI type and faces                                                    |  12   |
| [ ] | `D03 T19 §12` | Sky replacement                                                      |  12   |
| [ ] | `D03 T19 §13` | The suite pipeline and the brand kit in Imago                        |  15   |
| [ ] | `D03 T21 §11` | Imago 0.12.0 (Phase 26)                                              |  14   |

### Phase 27 -- Imago parity XI: workspace, customization, preferences, and Imago 1.0.0

The last parity phase customizes and audits the whole surface once it exists: workspaces and Preferences (`D03 T07 §17`) move here first, then workspace presets, the toolbar and options bar, menus, shortcuts, and command search, every preference page, interface appearance and language, pen and touch input, the presets manager and resource libraries, help and diagnostics, and the accessibility and localization audit (`D03 T07 §16`) over every parity surface. It ends with `imago-v1.0.0`, which declares the parity catalog complete.

|  ✔  | Section       | Deliverable                                                           | Items |
| :-: | ------------- | --------------------------------------------------------------------- | :---: |
| [ ] | `D03 T07 §17` | Workspaces, panels, and preferences                                   |   3   |
| [ ] | `D03 T20 §1`  | Workspaces, panels, the Properties panel, and the Contextual Task Bar |  26   |
| [ ] | `D03 T20 §2`  | The toolbar and the options bar                                       |  16   |
| [ ] | `D03 T20 §3`  | Menus, shortcuts, and command search                                  |  15   |
| [ ] | `D03 T20 §4`  | Preferences I: general, tools, cursors, units, guides, and type       |  23   |
| [ ] | `D03 T20 §9`  | Interface appearance, language, and accessibility display preferences |  18   |
| [ ] | `D03 T20 §5`  | Preferences II: files, performance, memory, and resources             |  17   |
| [ ] | `D03 T20 §6`  | Pen, touch, and input devices                                         |  16   |
| [ ] | `D03 T20 §7`  | The presets manager and resource libraries                            |  15   |
| [ ] | `D03 T20 §8`  | Help, learning, and diagnostics                                       |  20   |
| [ ] | `D03 T07 §16` | Accessibility and localization                                        |   4   |
| [ ] | `D03 T21 §12` | Imago 1.0.0 (Phase 27): the parity catalog complete                   |  17   |

### Phase 28 -- Lumen foundation: spine, catalog, import, RAW, library

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

### Phase 29 -- Lumen 0.1.0: develop, export, Edit in Imago, release

Lumen becomes a complete first release: keywords, collections, culling, and XMP sidecars finish the library; the edit stack, the develop pipeline on the suite develop engine that Phase 23 builds (`D01 T07`), the develop panel, crop, presets, and export make it a darkroom; Edit in Imago hands photos to Imago over files, never over assemblies; the user guide is written; and `lumen-v0.1.0` ships with the original-file guard proven on the installed build.

|  ✔  | Section       | Deliverable                                      | Items |
| :-: | ------------- | ------------------------------------------------ | :---: |
| [ ] | `D04 T01 §10` | Keywords, collections, and smart collections     |   4   |
| [ ] | `D04 T01 §11` | Ratings, flags, labels, and XMP sidecars         |   4   |
| [ ] | `D04 T02 §1`  | The edit stack                                   |   4   |
| [ ] | `D04 T02 §2`  | The develop pipeline on the suite develop engine |   6   |
| [ ] | `D04 T02 §3`  | The develop panel                                |   4   |
| [ ] | `D04 T02 §4`  | Crop and straighten                              |   3   |
| [ ] | `D04 T02 §5`  | Presets, copy and paste settings, and sync       |   3   |
| [ ] | `D04 T02 §6`  | Export                                           |   4   |
| [ ] | `D06 T01 §3`  | The Lumen user guide                             |   4   |
| [ ] | `D04 T02 §7`  | Edit in Imago                                    |   4   |
| [ ] | `D04 T02 §8`  | Lumen 0.1.0                                      |   7   |

### Phase 30 -- Distribution and the suite bundle

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

### Phase 31 -- Imago after 0.1.0: RAW import through the shared decoder

After the suite release, Imago opens camera RAW files through the decoder Lumen shares once it moves to `Photon.Core` (`D04 T01 §4`), developing them through the suite develop engine (`D01 T07 §1`) into Imago's Develop studio; until then the Camera Raw filter of Phase 23 works on open layers. Three of this phase's former rows moved into the Imago parity phases on 2026-09-26 without changing address: the filter catalog (`D03 T07 §3`) to Phase 21, and workspaces (`D03 T07 §17`) and the accessibility and localization audit (`D03 T07 §16`) to Phase 27. The legacy Imago roadmap's other entries were promoted into the parity phases or wait in [`backlog.md`](./backlog.md).

|  ✔  | Section       | Deliverable                           | Items |
| :-: | ------------- | ------------------------------------- | :---: |
| [ ] | `D03 T07 §11` | RAW import through the shared decoder |   4   |

### Phase 32 -- Lumen after 0.1.0: accessibility

After the suite release, Lumen gets the accessibility and localization the acceptance bar requires. The darkroom features beyond the first release (local adjustments, detail, lens corrections, color grading, merges, a GPU path, map, print, catalog maintenance) wait in [`backlog.md`](./backlog.md) (B-028 to B-036).

|  ✔  | Section      | Deliverable                    | Items |
| :-: | ------------ | ------------------------------ | :---: |
| [ ] | `D04 T02 §9` | Accessibility and localization |   3   |

### Phase 99 -- Manual: operator-only steps

No agent runner takes rows from this phase. Each row is a click path, a purchase, or a taste call the operator performs from the steps in `todo/99-manual/`; an agent verifies the public proof afterward and review stamps the evidence like any other row. Until `D00 T01 §2` ships, the rows are held back by their dependency on it; after it ships, each carries `**Requires:** operator`, so `query ready` lists them as runnable elsewhere and runners skip them.

|  ✔  | Section      | Deliverable                                | Items |
| :-: | ------------ | ------------------------------------------ | :---: |
| [ ] | `D99 T01 §1` | About bar, topics, and social preview      |   5   |
| [ ] | `D99 T01 §2` | Branch protection with the required checks |   3   |
| [ ] | `D99 T01 §3` | A code-signing certificate                 |   4   |
| [ ] | `D99 T01 §4` | Confirm the icon art licenses              |   3   |
| [ ] | `D99 T01 §5` | Choose each app's accent color             |   2   |
