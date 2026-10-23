---
schema_version: 1
id: capio-plan
domain: 08-capio
status: draft
title: "TODO-01 -- Capio: Plan the Screenshots and Screen Recording App"
depends_on: []
track: Capio
---

# TODO-01 -- Capio: Plan the Screenshots and Screen Recording App

> **Goal:** Capio, the suite's screenshot and screen recording app, is planned with the rigor of Stilus, Gesso, and Albumen by the campaign itself, just before it builds the app: its name is pre-screened, its job and fence are written, its competitors (ShareX and PicPick (the operator's models), with the Windows Snipping Tool as the system baseline and Snagit, read from its documentation, as the quality bar) are surveyed into a parity catalog, its layout map and section design are written, its accent, icon, and splash are designed first, and every TODO file of its two phases is authored through `plan-new-feature`, so Phases 43 and 44 end in `capio-v0.1.0` and `capio-v1.0.0`, built on C++23 and our own UI.

> [!IMPORTANT]
> **Current state (verified 2026-10-23):** The operator asked for three more apps on 2026-10-23: "Now, for the sake of completeness, let's als oinclude planning for 3 more additions to the suite. Indesign clone, professional screenshot app, modeled after ShareX and PickPick, but not all the features. and a professional color picker and color studio." and chose, the same day, the names Folium, Capio, and Tinctura, for this app the scope "Capture, annotate, record (Recommended)": every capture mode (region, window, full screen, scrolling, delayed, repeat last), a full annotation editor, OCR, pin to screen, history, and screen recording to MP4 and GIF; output to file, clipboard, and one configurable custom uploader. Out: ShareX's 80-plus upload destinations, automation workflows, and its grab bag of small tools, and their place: after the first suite release (Phase 40) and before the post-release phases, with the campaign writing each app's full plan ahead of its phases (`docs/dev/decisions.md`, "2026-10-23: Three more apps"). Nothing of Capio exists yet but its icon: no parity catalog, no inventories, no other design, no code. **Corrected 2026-10-23:** the operator chose Capio's icon the same day, and `scripts/build-app-icons.py` writes it, its small variants, and its splash under `resources/icons/capio/`, so §4 keeps it. Phases 43 and 44 hold only this file's sections until §5 and §6 author the rest.
<!-- claim: absent docs/parity/capio-parity.md -->
<!-- claim: absent docs/parity/capio-section-design.md -->
<!-- claim: exists docs/plans/2026-10-23-native-replan.md -->
<!-- claim: exists scripts/build-app-icons.py -->
<!-- claim: exists resources/icons/capio/capio.svg -->
<!-- claim: exists scripts/todo-parity.py -->

## Inputs

- [`.claude/skills/plan-new-feature/SKILL.md`](../../.claude/skills/plan-new-feature/SKILL.md) -- the rigor every authored section meets: the job, the competitors, every surface and behavior, the finer details
- [`docs/plans/2026-10-23-native-replan.md`](../../docs/plans/2026-10-23-native-replan.md) -- the ten requirements every authored section delivers ("What every re-plan section must deliver"), the same bar as the re-planned apps
- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md) -- the native architecture, the app layout under the native tree, and the toolchain
- [`docs/completion-review-prompt.md`](../../docs/completion-review-prompt.md) -- the completion checklist each feature section's scope answers
- [`docs/design/`](../../docs/design/) and [`docs/design/app-icons.md`](../../docs/design/app-icons.md) -- the design system, and the icon system §4 extends
- [`docs/parity/README.md`](../../docs/parity/README.md) and `scripts/todo-parity.py` -- the catalog format and the check §2 extends
- -> XREF: D05 T01 §6 -- this app's planning starts after the first suite bundle, `isotone-v1.0.0`
- -> XREF: D05 T01 §7 -- §6 adds Capio to the `isotone-v1.1.0` suite bundle
- -> XREF: D07 T01 §5 -- Tinctura's foundation plan holds the picker this app moves to `Isotone.Core`

## Outcome

- `docs/parity/capio-parity.md` routes every surveyed competitor feature to a live section of this domain, or to a backlog entry with the operator's words, and `scripts/todo-parity.py` checks it.
- `docs/design/layout-maps/capio.md`, `docs/parity/capio-section-design.md`, the `accent-capio` tokens, and the Capio icon and splash exist before any surface is built.
- Every section of Phases 43 and 44 beyond this file is authored, executable with no conversation context, and meets the ten requirements, through `capio-v1.0.0` and the `isotone-v1.1.0` bundle.

**Adjacency:** all=not-applicable (authoring plan files and design sources: no records, settings, documents, or surfaces a user sees)

**Adjacency rationale:** Every section §5 and §6 author carries its own adjacency line; this file only decides what those sections are.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |  §1    | Capio: the name, the job, and the identity | D05 T01 §6 |  [ ]   |
|   2   |  §2    | Capio: the competitor survey and the parity catalog | §1 |  [ ]   |
|   3   |  §3    | Capio: the section design and the layout map | §2 |  [ ]   |
|   4   |  §4    | Capio: the accent, the icon, and the splash, design first | §3 |  [ ]   |
|   5   |  §5    | Capio: author the foundation and 0.1.0 files | §4, D07 T01 §5 |  [ ]   |
|   6   |  §6    | Capio: author the parity and 1.0.0 files | §5 |  [ ]   |

---

## 1. Capio: The Name, the Job, and the Identity

The operator chose the name Capio (Latin for I capture) on 2026-10-23, and the earlier names were pre-screened for live trademarks before anything shipped (Photon, Nodus, Imago, and Lumen were replaced for that reason). This section repeats that pre-screen for Capio, writes the job and the fence the whole plan answers to, and fixes the app's identity, so no later section invents any of it.

- [ ] Pre-screen the name Capio as the 2026-09-27 pre-screen did: the USPTO trademark search, EUIPO eSearch, the WIPO Global Brand Database, the Microsoft Store, `winget-pkgs`, GitHub, and a web search for "Capio" with "software" and "app", in classes 9 and 42. Done when: a `docs/dev/decisions.md` entry lists each source with its result and the date; a live software mark that conflicts is filed through `add-todo` as an operator question in `todo/99-manual/` (the work continues under the working name, which lives in this domain and the names below), and no conflict is recorded as such.
- [ ] Write Capio's job at the head of `docs/parity/capio-parity.md`: whose problem, in what situation, what done looks like to them, the audience, and the one-line purpose the About page, the tool rail tooltip, and the user guide quote. Done when: the paragraph and the purpose line are in the file.
- [ ] Write the fence under the job: the operator's scope ("Capture, annotate, record (Recommended)": every capture mode (region, window, full screen, scrolling, delayed, repeat last), a full annotation editor, OCR, pin to screen, history, and screen recording to MP4 and GIF; output to file, clipboard, and one configurable custom uploader. Out: ShareX's 80-plus upload destinations, automation workflows, and its grab bag of small tools) quoted, and the non-goals named (ShareX's catalog of upload destinations, after-capture automation workflows, and its small utilities (hash checker, URL shortener, and the like); full image editing belongs to Gesso). Done when: every non-goal is named, so no later section plans across the fence without an operator decision.
- [ ] Fix the identity in `docs/parity/capio-parity.md`'s header: the executable `Capio.exe`, the tag prefix `capio-v`, the app's home under the native tree the spec names, the document types it opens and owns (its own format, if it has one, and the file associations it registers), and single-instance behavior. Done when: each is decided with its reason, and nothing it names collides with Stilus, Gesso, or Albumen.
- [ ] Update Capio's row in the app table of `AGENTS.md` and `README.md` if the pre-screen changed the name. Done when: both name the app as decided.
- [ ] Run `python scripts/todo-graph.py validate` and `python scripts/todo-claims.py`. Done when: no FATAL, no new WARN, every claim holds.
- [ ] Commit: `"todo: capio: the name, the job, and the identity"`

**Test checkpoint:** Static evidence: the decision record's pre-screen lines and the job, fence, and identity in `docs/parity/capio-parity.md` (quoted); `validate` and `todo-claims.py` pass (quoted). Cheaper substitute that fails: a job paragraph without a fence, which lets the plan grow past what the operator chose.

## 2. Capio: The Competitor Survey and the Parity Catalog

The plan is only as good as its picture of the competition: ShareX and PicPick (the operator's models), with the Windows Snipping Tool as the system baseline and Snagit, read from its documentation, as the quality bar. Each is driven here at its current release and inventoried feature by feature, as `docs/parity/sources/` holds for the other apps, and the catalog routes every feature to Capio.

- [ ] Drive each competitor at its current release on this machine and record its version from its About page; where one cannot run here (a web app behind an account, a paid app without a licence), read its official documentation and say so in each row it sources. Done when: each competitor has a version and a source line.
- [ ] Write one inventory per competitor under `docs/parity/sources/<competitor>-<version>.md` in the shape of the existing inventories, ids `CP-` for the catalog, and `SX-` (ShareX), `PP-` (PicPick), `ST-` (Snipping Tool), and `SG-` (Snagit) for the inventories: every feature, with its surfaces, its behaviors, and its finer details (shortcuts and modifiers, empty and failure states, presets, export, undo granularity) and what it does badly. Done when: no menu, panel, tool, dialog, or preference of the competitor is missing.
- [ ] Write the catalog rows of `docs/parity/capio-parity.md`: one row per Capio feature, each naming the competitor ids it covers and a status `docs/parity/README.md` allows; a feature outside the fence of §1 is a row whose status cites the operator's decision, never a silent omission. Done when: every inventory id appears in exactly one catalog row.
- [ ] Add Capio's catalog to `CATALOGS` in `scripts/todo-parity.py` the way Albumen's was added (its path, its id shape, its duplicate class, and one column per inventory), register the new duplicate class with the other parity classes and in the diagnostic registry, and add a self-test fixture for it. Done when: the parity check reads the catalog, and its self-test fails on a duplicated `CP-` id.
- [ ] Run the parity check, `python scripts/todo-graph.py validate`, and `python scripts/todo-claims.py`. Done when: all pass.
- [ ] Commit: `"todo: capio: the competitor survey and the parity catalog"`

**Test checkpoint:** The parity check's summary line naming Capio's catalog and its totals, and its self-test (quoted); the inventories' version lines (quoted). Cheaper substitute that fails: a catalog written from memory, which the version and source lines expose.

## 3. Capio: The Section Design and the Layout Map

The catalog says what Capio must do; this section decides where each thing lives and how it is laid out, before any file is authored. Capio has no Adobe counterpart, so its capture overlay and editor take the layout ShareX and PicPick users expect, and every annotation tool that Gesso also has keeps Gesso's Adobe name, icon, and shortcut (Brush, Text, Crop, Eyedropper), so the suite reads as one.

- [ ] Write `docs/design/layout-maps/capio.md` in the shape of the other layout maps: the window and its regions, every tool in its rail order with its icon, shortcut, and modifiers, the menu map item by item, every panel and its grouping, every dialog, the context and options bars, and the terminology list, each with the competitor id it matches, and Capio's own features placed where users of that competitor would look for them. Done when: every catalog row with a surface has a place on the map.
- [ ] Write `docs/parity/capio-section-design.md`: the TODO files of Phase 43 (the spine, the core model, and 0.1.0) and Phase 44 (parity through 1.0.0), each with its sections, every catalog row routed to one section, and each feature section's `**Exceed:**` improvement over its competitor, named and measurable (requirement 9). Done when: no catalog row is unrouted and no feature section lacks its improvement.
- [ ] Decide the shared code in the section design: The system-wide picker is Tinctura's: this app's foundation plan moves it to `Isotone.Core` the first time Capio needs it (`AGENTS.md`, one suite, shared deliberately), never a second copy. Annotation rendering runs on the suite pixel engine. Screen recording's encoder stays in Capio, with a note naming the post-release media system (Phase 49) as the point it moves when a second app needs encoding. Done when: each shared system names what Capio consumes from `Isotone.Core`, what moves there and when, and what stays in Capio with the point at which it would move.
- [ ] Run `python scripts/todo-graph.py validate` and the parity check. Done when: both pass.
- [ ] Commit: `"todo: capio: the section design and the layout map"`

**Test checkpoint:** Static evidence: the layout map's coverage (every surfaced catalog row placed) and the section design's routing (every row routed) counted and quoted; `validate` and the parity check pass (quoted). Cheaper substitute that fails: a section design that lists files without routing every catalog row, which leaves features no section owns.

## 4. Capio: The Accent, the Icon, and the Splash, Design First

Every surface answers to `docs/design/` (`standards/design-contract.md`), so Capio's identity is designed before any section draws it: its accent tokens, its icon in the suite's Solid style on the Direction C tile and band, and its Suite card splash.

- [ ] Add `accent-capio` to `docs/design/tokens.json`: the default dark value #FF4D6D (red, the spectrum band's own stop, which no other app uses) and a light value that meets 4.5:1 against white by the method `standards/shared.md` records, both recorded in its Color section, and add Capio to the accents `D99 T01 §5` asks the operator to confirm. Done when: both values and their ratios are recorded, and the operator can replace the default there.
- [ ] Keep Capio's icon as the operator chose it on 2026-10-23 and as `scripts/build-app-icons.py` already draws it (`resources/icons/capio/`, its masters, its variants below 40 px, and `capio-splash.svg`); if the accent changes, change it there and regenerate. Done when: `python scripts/build-app-icons.py --check` passes and a rendered contact sheet shows the six icons balanced at 256, 48, 32, 24, and 16 px.
- [ ] Add Capio to `docs/design/app-icons.md` (glyph, geometry, colors, and the small variant), `resources/icons/README.md`, and the AppIcon component page, then regenerate the design page as `docs/design/EDITING.md` describes. Done when: `python scripts/build-design-site.py --check` passes and the page shows Capio's icon.
- [ ] Run `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` and `python scripts/todo-graph.py validate`. Done when: no new design-contract violation and no FATAL.
- [ ] Commit: `"design: capio: the accent, the icon, and the splash"`

**Test checkpoint:** `python scripts/build-app-icons.py --check` and `python scripts/build-design-site.py --check` pass (quoted), the contact sheet renders (driven run, the render command and its output path quoted), and the accent's contrast ratios are recorded. Cheaper substitute that fails: an icon drawn by hand into `resources/icons/capio/`, which `--check` refuses because the generator would overwrite it.

## 5. Capio: Author the Foundation and 0.1.0 Files

With the job, the catalog, the layout, and the identity decided, the campaign authors Phase 43's files through `plan-new-feature` and `create-todo`: the capture engine and every mode, the overlay, the annotation editor, OCR, pin to screen, history, recording to MP4 and GIF, the outputs and the custom uploader, and the release, as far as `capio-v0.1.0`, each section born complete.

- [ ] Author the Phase 43 TODO files in `todo/08-capio/` from `docs/parity/capio-section-design.md`, through `plan-new-feature` (every surface, behavior, state, and string) and `create-todo` (every section complete): the app spine (the native app project, composition, settings, logging, single instance, file associations, About, first run), the core model, the 0.1.0 features, and the performance section that commits Capio's small, typical, and large fixtures (requirement 8). Done when: each file validates and every section is executable with no conversation context.
- [ ] Apply every requirement of "What every re-plan section must deliver" in `docs/plans/2026-10-23-native-replan.md` to each authored section: the design and layout map lines, the completion checklist, the release split into a release-candidate section and a release section (requirement 6), SemVer from the `capio-v` tag (requirement 7), and an `**Exceed:**` paragraph on every feature section. Done when: each requirement is checked for each section and any deviation is recorded in the file with its reason.
- [ ] Author Capio's user guide sections in `todo/06-docs/` and its packaging and release sections, each XREFed both ways with the sections whose behavior they document or ship. Done when: `validate` reports no one-way XREF.
- [ ] Place every authored section in Phase 43 of `todo/implementation-plan.md` after this row, and add `D08 T01 §5` to the Depends On of each authored file's open entry points, so none runs before this section is stamped. Done when: `python scripts/todo-graph.py resolve` on each entry point exits 4 naming this section.
- [ ] List the authored files in `todo/08-capio/INDEX.md` and under Active TODOs in `todo/TODO-00-INDEX.md`, and set the status of every catalog row the files now own in `docs/parity/capio-parity.md` in the same commit. Done when: the parity check passes with the new statuses.
- [ ] Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `python scripts/todo-claims.py`, and the parity check. Done when: no FATAL, no new WARN, the plan current, every claim and catalog row holding.
- [ ] Commit: `"todo: capio: author the foundation and 0.1.0 files"`

**Test checkpoint:** Static evidence: `validate`, `plan --check`, `todo-claims.py`, and the parity check pass (quoted); before this section's stamp, `resolve` on each authored entry point exits 4 naming this section (quoted). The review loop reviews the authored files against the ten requirements and the completion checklist. Cheaper substitute that fails: section titles with no checklists, which a campaign cannot build without inventing the plan as it goes.

## 6. Capio: Author the Parity and 1.0.0 Files

Phase 44 opens with this section, so the parity files are written against what 0.1.0 actually shipped: every remaining catalog row becomes a section, and Capio reaches `capio-v1.0.0` and joins the next suite bundle.

- [ ] Author the Phase 44 TODO files in `todo/08-capio/` from `docs/parity/capio-section-design.md`, re-read against the shipped 0.1.0, through `plan-new-feature` and `create-todo`: every remaining catalog row, the workspace, preferences, and help, the accessibility and localization audit last over every surface, and the releases from `capio-v0.2.0` to `capio-v1.0.0`. Done when: every catalog row is owned by a live section or by a backlog entry that quotes the operator's deferral.
- [ ] Apply the ten requirements to each authored section as §5 does. Done when: each is checked and any deviation recorded with its reason.
- [ ] Add Capio to the `isotone-v1.1.0` suite bundle: extend the scope of `D05 T01 §7` to carry `capio-v1.0.0` at its own version, with its installer and its notices. Done when: the section names Capio and its checkpoint covers it.
- [ ] Place every authored section in Phase 44 after this row, gate the authored entry points on `D08 T01 §6`, list the files in the indexes, and set the catalog statuses in the same commit. Done when: `resolve` on each entry point exits 4 naming this section and the parity check passes.
- [ ] Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `python scripts/todo-claims.py`, and the parity check. Done when: all pass.
- [ ] Commit: `"todo: capio: author the parity and 1.0.0 files"`

**Test checkpoint:** Static evidence: the parity check reports no catalog row without a live owner or a quoted deferral (quoted); `validate`, `plan --check`, and `todo-claims.py` pass (quoted); `resolve` on each authored entry point exits 4 naming this section before the stamp (quoted). Cheaper substitute that fails: parity rows parked in the backlog without the operator's words, which `validate` refuses as a dropped feature.

## Verification

- [ ] `python scripts/todo-graph.py validate` -- no FATAL and no new WARN
- [ ] `python scripts/todo-graph.py plan --check` -- the plan current
- [ ] `python scripts/todo-claims.py` -- every claim holds
- [ ] The parity check -- Capio's catalog fully routed
- [ ] `python scripts/build-app-icons.py --check` and `python scripts/build-design-site.py --check` -- the identity current
