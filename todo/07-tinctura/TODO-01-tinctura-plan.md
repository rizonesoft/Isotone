---
schema_version: 1
id: tinctura-plan
domain: 07-tinctura
status: draft
title: "TODO-01 -- Tinctura: Plan the Color Picker and Color Studio App"
depends_on: []
track: Tinctura
---

# TODO-01 -- Tinctura: Plan the Color Picker and Color Studio App

> **Goal:** Tinctura, the suite's color picker and color studio, is planned with the rigor of Stilus, Gesso, and Albumen by the campaign itself, just before it builds the app: its name is pre-screened, its job and fence are written, its competitors (Microsoft PowerToys Color Picker, Just Color Picker, Adobe Color, and Coolors, with the color surfaces of Photoshop and Illustrator (the Color Picker dialog, the Color and Swatches panels, Color Themes) as the Adobe reference) are surveyed into a parity catalog, its layout map and section design are written, its accent, icon, and splash are designed first, and every TODO file of its two phases is authored through `plan-new-feature`, so Phases 41 and 42 end in `tinctura-v0.1.0` and `tinctura-v1.0.0`, built on C++23 and our own UI.

> [!IMPORTANT]
> **Current state (verified 2026-10-23):** The operator asked for three more apps on 2026-10-23: "Now, for the sake of completeness, let's als oinclude planning for 3 more additions to the suite. Indesign clone, professional screenshot app, modeled after ShareX and PickPick, but not all the features. and a professional color picker and color studio." and chose, the same day, the names Folium, Capio, and Tinctura, for this app the scope "Picker plus full studio (Recommended)": a system-wide eyedropper with magnifier, every color space (HEX, RGB, HSL, HSV, Lab, LCH, OKLCH, ICC-managed CMYK), palettes and harmonies, gradients, palette extraction from images, WCAG and APCA contrast, color-blindness simulation, and exchange in ASE, ACO, GPL, CSS, and design tokens; licensed libraries such as Pantone are out, and their place: after the first suite release (Phase 40) and before the post-release phases, with the campaign writing each app's full plan ahead of its phases (`docs/dev/decisions.md`, "2026-10-23: Three more apps"). Nothing of Tinctura exists yet but its icon: no parity catalog, no inventories, no other design, no code. **Corrected 2026-10-23:** the operator chose Tinctura's icon the same day, and `scripts/build-app-icons.py` writes it, its small variants, and its splash under `resources/icons/tinctura/`, so §4 keeps it. Phases 41 and 42 hold only this file's sections until §5 and §6 author the rest.
<!-- claim: absent docs/parity/tinctura-parity.md -->
<!-- claim: absent docs/parity/tinctura-section-design.md -->
<!-- claim: exists docs/plans/2026-10-23-native-replan.md -->
<!-- claim: exists scripts/build-app-icons.py -->
<!-- claim: exists resources/icons/tinctura/tinctura.svg -->
<!-- claim: exists scripts/todo-parity.py -->

## Inputs

- [`.claude/skills/plan-new-feature/SKILL.md`](../../.claude/skills/plan-new-feature/SKILL.md) -- the rigor every authored section meets: the job, the competitors, every surface and behavior, the finer details
- [`docs/plans/2026-10-23-native-replan.md`](../../docs/plans/2026-10-23-native-replan.md) -- the ten requirements every authored section delivers ("What every re-plan section must deliver"), the same bar as the re-planned apps
- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md) -- the native architecture, the app layout under the native tree, and the toolchain
- [`docs/completion-review-prompt.md`](../../docs/completion-review-prompt.md) -- the completion checklist each feature section's scope answers
- [`docs/design/`](../../docs/design/) and [`docs/design/app-icons.md`](../../docs/design/app-icons.md) -- the design system, and the icon system §4 extends
- [`docs/parity/README.md`](../../docs/parity/README.md) and `scripts/todo-parity.py` -- the catalog format and the check §2 extends
- -> XREF: D05 T01 §6 -- this app's planning starts after the first suite bundle, `isotone-v1.0.0`
- -> XREF: D05 T01 §7 -- §6 adds Tinctura to the `isotone-v1.1.0` suite bundle
- -> XREF: D08 T01 §5 -- Capio's foundation plan moves this app's picker to `Isotone.Core` when Capio needs it; this file's §5 plans the picker so it can move

## Outcome

- `docs/parity/tinctura-parity.md` routes every surveyed competitor feature to a live section of this domain, or to a backlog entry with the operator's words, and `scripts/todo-parity.py` checks it.
- `docs/design/layout-maps/tinctura.md`, `docs/parity/tinctura-section-design.md`, the `accent-tinctura` tokens, and the Tinctura icon and splash exist before any surface is built.
- Every section of Phases 41 and 42 beyond this file is authored, executable with no conversation context, and meets the ten requirements, through `tinctura-v1.0.0` and the `isotone-v1.1.0` bundle.

**Adjacency:** all=not-applicable (authoring plan files and design sources: no records, settings, documents, or surfaces a user sees)

**Adjacency rationale:** Every section §5 and §6 author carries its own adjacency line; this file only decides what those sections are.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |  §1    | Tinctura: the name, the job, and the identity | D05 T01 §6 |  [ ]   |
|   2   |  §2    | Tinctura: the competitor survey and the parity catalog | §1 |  [ ]   |
|   3   |  §3    | Tinctura: the section design and the layout map | §2 |  [ ]   |
|   4   |  §4    | Tinctura: the accent, the icon, and the splash, design first | §3 |  [ ]   |
|   5   |  §5    | Tinctura: author the foundation and 0.1.0 files | §4 |  [ ]   |
|   6   |  §6    | Tinctura: author the parity and 1.0.0 files | §5 |  [ ]   |

---

## 1. Tinctura: The Name, the Job, and the Identity

The operator chose the name Tinctura (Latin for a tint or dye) on 2026-10-23, and the earlier names were pre-screened for live trademarks before anything shipped (Photon, Nodus, Imago, and Lumen were replaced for that reason). This section repeats that pre-screen for Tinctura, writes the job and the fence the whole plan answers to, and fixes the app's identity, so no later section invents any of it.

- [ ] Pre-screen the name Tinctura as the 2026-09-27 pre-screen did: the USPTO trademark search, EUIPO eSearch, the WIPO Global Brand Database, the Microsoft Store, `winget-pkgs`, GitHub, and a web search for "Tinctura" with "software" and "app", in classes 9 and 42. Done when: a `docs/dev/decisions.md` entry lists each source with its result and the date; a live software mark that conflicts is filed through `add-todo` as an operator question in `todo/99-manual/` (the work continues under the working name, which lives in this domain and the names below), and no conflict is recorded as such.
- [ ] Write Tinctura's job at the head of `docs/parity/tinctura-parity.md`: whose problem, in what situation, what done looks like to them, the audience, and the one-line purpose the About page, the tool rail tooltip, and the user guide quote. Done when: the paragraph and the purpose line are in the file.
- [ ] Write the fence under the job: the operator's scope ("Picker plus full studio (Recommended)": a system-wide eyedropper with magnifier, every color space (HEX, RGB, HSL, HSV, Lab, LCH, OKLCH, ICC-managed CMYK), palettes and harmonies, gradients, palette extraction from images, WCAG and APCA contrast, color-blindness simulation, and exchange in ASE, ACO, GPL, CSS, and design tokens; licensed libraries such as Pantone are out) quoted, and the non-goals named (licensed spot-color libraries (Pantone and the like, which need commercial licences), image editing, and vector drawing). Done when: every non-goal is named, so no later section plans across the fence without an operator decision.
- [ ] Fix the identity in `docs/parity/tinctura-parity.md`'s header: the executable `Tinctura.exe`, the tag prefix `tinctura-v`, the app's home under the native tree the spec names, the document types it opens and owns (its own format, if it has one, and the file associations it registers), and single-instance behavior. Done when: each is decided with its reason, and nothing it names collides with Stilus, Gesso, or Albumen.
- [ ] Update Tinctura's row in the app table of `AGENTS.md` and `README.md` if the pre-screen changed the name. Done when: both name the app as decided.
- [ ] Run `python scripts/todo-graph.py validate` and `python scripts/todo-claims.py`. Done when: no FATAL, no new WARN, every claim holds.
- [ ] Commit: `"todo: tinctura: the name, the job, and the identity"`

**Test checkpoint:** Static evidence: the decision record's pre-screen lines and the job, fence, and identity in `docs/parity/tinctura-parity.md` (quoted); `validate` and `todo-claims.py` pass (quoted). Cheaper substitute that fails: a job paragraph without a fence, which lets the plan grow past what the operator chose.

## 2. Tinctura: The Competitor Survey and the Parity Catalog

The plan is only as good as its picture of the competition: Microsoft PowerToys Color Picker, Just Color Picker, Adobe Color, and Coolors, with the color surfaces of Photoshop and Illustrator (the Color Picker dialog, the Color and Swatches panels, Color Themes) as the Adobe reference. Each is driven here at its current release and inventoried feature by feature, as `docs/parity/sources/` holds for the other apps, and the catalog routes every feature to Tinctura.

- [ ] Drive each competitor at its current release on this machine and record its version from its About page; where one cannot run here (a web app behind an account, a paid app without a licence), read its official documentation and say so in each row it sources. Done when: each competitor has a version and a source line.
- [ ] Write one inventory per competitor under `docs/parity/sources/<competitor>-<version>.md` in the shape of the existing inventories, ids `TC-` for the catalog, and `PT-` (PowerToys), `JC-` (Just Color Picker), `AC-` (Adobe Color), and `CO-` (Coolors) for the inventories: every feature, with its surfaces, its behaviors, and its finer details (shortcuts and modifiers, empty and failure states, presets, export, undo granularity) and what it does badly. Done when: no menu, panel, tool, dialog, or preference of the competitor is missing.
- [ ] Write the catalog rows of `docs/parity/tinctura-parity.md`: one row per Tinctura feature, each naming the competitor ids it covers and one status of the grammar in `docs/parity/README.md`: `to-author D07 T01 §6` for every feature Tinctura will build (§3 moves the Phase 41 ones to `to-author D07 T01 §5`), `excluded: scope <reason>` quoting the operator's fence for a feature outside §1's fence, or `other-app: <app> <reason>` for a job another Isotone app owns, never a silent omission and never a `plan` ref before its section exists. Done when: every inventory id appears in exactly one catalog row.
- [ ] Add Tinctura's catalog to `CATALOGS` in `scripts/todo-parity.py` the way Albumen's was added (its path, its id shape, its duplicate class, and one column per inventory), register the new duplicate class with the other parity classes and in the diagnostic registry, and add a self-test fixture for it. Done when: the parity check reads the catalog, and its self-test fails on a duplicated `TC-` id.
- [ ] Run the parity check, `python scripts/todo-graph.py validate`, and `python scripts/todo-claims.py`. Done when: all pass.
- [ ] Commit: `"todo: tinctura: the competitor survey and the parity catalog"`

**Test checkpoint:** The parity check's summary line naming Tinctura's catalog and its totals, and its self-test (quoted); the inventories' version lines (quoted). Cheaper substitute that fails: a catalog written from memory, which the version and source lines expose.

## 3. Tinctura: The Section Design and the Layout Map

The catalog says what Tinctura must do; this section decides where each thing lives and how it is laid out, before any file is authored. Tinctura's color surfaces match Adobe's where Adobe has them (the Color Picker dialog's fields and order, the Swatches and Color panels, Adobe Color's harmony rules and their names: Analogous, Monochromatic, Triad, Complementary, Split Complementary, Square, Compound, Shades), and its own studio tools (contrast, simulation, extraction, exchange) sit where those surfaces would put them.

- [ ] Write `docs/design/layout-maps/tinctura.md` in the shape of the other layout maps: the window and its regions, every tool in its rail order with its icon, shortcut, and modifiers, the menu map item by item, every panel and its grouping, every dialog, the context and options bars, and the terminology list, each with the competitor id it matches, and Tinctura's own features placed where users of that competitor would look for them. Done when: every catalog row with a surface has a place on the map.
- [ ] Write `docs/parity/tinctura-section-design.md`: the TODO files of Phase 41 (the spine, the core model, and 0.1.0) and Phase 42 (parity through 1.0.0), each with its sections, every catalog row routed to one section, and each feature section's `**Exceed:**` improvement over its competitor, named and measurable (requirement 9). Done when: no catalog row is unrouted and no feature section lacks its improvement.
- [ ] Set the status of every catalog row the section design routes to Phase 41 to `to-author D07 T01 §5`, leaving the Phase 42 rows at `to-author D07 T01 §6`. Done when: the parity check passes, the number of rows reading `to-author D07 T01 §5` and the number reading `to-author D07 T01 §6` in `docs/parity/tinctura-parity.md` (each counted with `Select-String`, quoted) equal the section design's Phase 41 and Phase 42 feature totals, and the Totals table's one `to-author` row equals their sum.
- [ ] Decide the shared code in the section design: Color conversion and ICC transforms are consumed from the suite's color management in `Isotone.Core`, never re-implemented. The system-wide picker overlay stays in Tinctura until a second app needs it: Capio is that app, and its foundation plan (`D08 T01 §5`) moves the picker to `Isotone.Core` rather than copying it. Done when: each shared system names what Tinctura consumes from `Isotone.Core`, what moves there and when, and what stays in Tinctura with the point at which it would move.
- [ ] Run `python scripts/todo-graph.py validate` and the parity check. Done when: both pass.
- [ ] Commit: `"todo: tinctura: the section design and the layout map"`

**Test checkpoint:** Static evidence: the layout map's coverage (every surfaced catalog row placed) and the section design's routing (every row routed) counted and quoted; `validate` and the parity check pass (quoted). Cheaper substitute that fails: a section design that lists files without routing every catalog row, which leaves features no section owns.

## 4. Tinctura: The Accent, the Icon, and the Splash, Design First

Every surface answers to `docs/design/` (`standards/design-contract.md`), so Tinctura's identity is designed before any section draws it: its accent tokens, its icon in the suite's Solid style on the Direction C tile and band, and its Suite card splash.

- [ ] Add `accent-tinctura` to `docs/design/tokens.json`: the default dark value #B45CFF (violet, the spectrum band's own stop, which no other app uses) and a light value that meets 4.5:1 against white by the method `standards/shared.md` records, both recorded in its Color section, and add Tinctura to the accents `D99 T01 §5` asks the operator to confirm. Done when: both values and their ratios are recorded, and the operator can replace the default there.
- [ ] Keep Tinctura's icon as the operator chose it on 2026-10-23 and as `scripts/build-app-icons.py` already draws it (`resources/icons/tinctura/`, its masters, its variants below 40 px, and `tinctura-splash.svg`); if the accent changes, change it there and regenerate. Done when: `python scripts/build-app-icons.py --check` passes and a rendered contact sheet shows the six icons balanced at 256, 48, 32, 24, and 16 px.
- [ ] Add Tinctura to `docs/design/app-icons.md` (glyph, geometry, colors, and the small variant), `resources/icons/README.md`, and the AppIcon component page, then regenerate the design page as `docs/design/EDITING.md` describes. Done when: `python scripts/build-design-site.py --check` passes and the page shows Tinctura's icon.
- [ ] Run `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` and `python scripts/todo-graph.py validate`. Done when: no new design-contract violation and no FATAL.
- [ ] Commit: `"design: tinctura: the accent, the icon, and the splash"`

**Test checkpoint:** `python scripts/build-app-icons.py --check` and `python scripts/build-design-site.py --check` pass (quoted), the contact sheet renders (driven run, the render command and its output path quoted), and the accent's contrast ratios are recorded. Cheaper substitute that fails: an icon drawn by hand into `resources/icons/tinctura/`, which `--check` refuses because the generator would overwrite it.

## 5. Tinctura: Author the Foundation and 0.1.0 Files

With the job, the catalog, the layout, and the identity decided, the campaign authors Phase 41's files through `plan-new-feature` and `create-todo`: the picker overlay and magnifier, the color model and every conversion, the studio window, palettes and harmonies, exchange formats with format fidelity proofs, the accessibility tools, and the release, as far as `tinctura-v0.1.0`, each section born complete.

- [ ] Author the Phase 41 TODO files in `todo/07-tinctura/` from `docs/parity/tinctura-section-design.md`, through `plan-new-feature` (every surface, behavior, state, and string) and `create-todo` (every section complete): the app spine (the native app project, composition, settings, logging, single instance, file associations, About, first run), the core model, the 0.1.0 features, and the performance section that commits Tinctura's small, typical, and large fixtures (requirement 8). Done when: each file validates and every section is executable with no conversation context.
- [ ] Apply every requirement of "What every re-plan section must deliver" in `docs/plans/2026-10-23-native-replan.md` to each authored section: the design and layout map lines, the completion checklist, the release split into a release-candidate section and a release section (requirement 6), SemVer from the `tinctura-v` tag (requirement 7), and an `**Exceed:**` paragraph on every feature section. Done when: each requirement is checked for each section and any deviation is recorded in the file with its reason.
- [ ] Extend every app list in the tooling to Tinctura, so no gate or script treats it as unknown: `scripts/release-manifest.ps1` (its `-Slug` set), `scripts/build-design-site.py` (`APPS`), and any other list `git grep -n -i -E "stilus.{0,40}gesso.{0,40}albumen" -- scripts tools .github .conclave` prints; the release and design gates of `scripts/todo-graph.py` already name it. Done when: that grep's every hit names Tinctura or states why the list is for the three first apps only.
- [ ] Author Tinctura's user guide sections in `todo/06-docs/` and its packaging and release sections, each XREFed both ways with the sections whose behavior they document or ship. Done when: `validate` reports no one-way XREF.
- [ ] Place every authored section in Phase 41 of `todo/implementation-plan.md` after this row, and add `D07 T01 §5` to the Depends On of each authored file's open entry points, so none runs before this section is stamped. Done when: `python scripts/todo-graph.py resolve` on each entry point exits 4 naming this section.
- [ ] List the authored files in `todo/07-tinctura/INDEX.md` and under Active TODOs in `todo/TODO-00-INDEX.md`, and reroute every `to-author D07 T01 §5` row of `docs/parity/tinctura-parity.md` to `plan <the section that owns it>` in the same commit. Done when: the parity check passes and no row still reads `to-author D07 T01 §5` (a row left behind fails as `parity-to-author-stale` once this section is stamped).
- [ ] Add the authored `tinctura-v0.1.0` release-candidate section (requirement 6 of `docs/plans/2026-10-23-native-replan.md`: built, tested, packaged, and signing-ready, the part the campaign completes) to §6's Depends On in this file's Implementation Order, never the publication section, which may wait on the operator's credentials and must not hold later phases. Done when: `python scripts/todo-graph.py resolve 'D07 T01 §6'` exits 4 naming that release-candidate section.
- [ ] Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `python scripts/todo-claims.py`, and the parity check. Done when: no FATAL, no new WARN, the plan current, every claim and catalog row holding.
- [ ] Commit: `"todo: tinctura: author the foundation and 0.1.0 files"`

**Test checkpoint:** Static evidence: `validate`, `plan --check`, `todo-claims.py`, and the parity check pass (quoted); before this section's stamp, `resolve` on each authored entry point exits 4 naming this section (quoted). The review loop reviews the authored files against the ten requirements and the completion checklist. Cheaper substitute that fails: section titles with no checklists, which a campaign cannot build without inventing the plan as it goes.

## 6. Tinctura: Author the Parity and 1.0.0 Files

Phase 42 opens with this section, so the parity files are written against the completed 0.1.0 release candidate: every remaining catalog row becomes a section, and Tinctura reaches `tinctura-v1.0.0` and joins the next suite bundle.

- [ ] Author the Phase 42 TODO files in `todo/07-tinctura/` from `docs/parity/tinctura-section-design.md`, re-read against the completed 0.1.0 release candidate, through `plan-new-feature` and `create-todo`: every remaining catalog row, the workspace, preferences, and help, the accessibility and localization audit last over every surface, and the releases from `tinctura-v0.2.0` to `tinctura-v1.0.0`. Done when: every catalog row is owned by a live section; a row goes to `todo/backlog.md` only with the operator's own words quoting the deferral (asked in an attended session; an unattended run plans the row instead, since no feature is left behind).
- [ ] Apply the ten requirements to each authored section as §5 does. Done when: each is checked and any deviation recorded with its reason.
- [ ] Add Tinctura to the `isotone-v1.1.0` suite bundle: extend the scope of `D05 T01 §7` to carry `tinctura-v1.0.0` at its own version, with its installer and its notices. Done when: the section names Tinctura and its checkpoint covers it.
- [ ] Place every authored section in Phase 42 after this row, gate the authored entry points on `D07 T01 §6`, list the files in the indexes, and reroute every `to-author D07 T01 §6` row to `plan <its owner>` or to a backlog entry quoting the operator's deferral in the same commit. Done when: `resolve` on each entry point exits 4 naming this section, the parity check passes, and no `to-author` row remains.
- [ ] Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `python scripts/todo-claims.py`, and the parity check. Done when: all pass.
- [ ] Commit: `"todo: tinctura: author the parity and 1.0.0 files"`

**Test checkpoint:** Static evidence: the parity check reports no catalog row without a live owner or a quoted deferral (quoted); `validate`, `plan --check`, and `todo-claims.py` pass (quoted); `resolve` on each authored entry point exits 4 naming this section before the stamp (quoted). Cheaper substitute that fails: parity rows parked in the backlog without the operator's words. Nothing in `validate` reads a deferral's wording when it is filed; the guards are the completion review, which refuses a deferral that quotes no operator, and the release's backlog review, which refuses the `tinctura-v1.0.0` stamp until every Tinctura backlog entry is promoted or carries the operator's quoted deferral (`release-backlog-unreviewed`, whose release gate knows the `tinctura-v` tags).

## Verification

- [ ] `python scripts/todo-graph.py validate` -- no FATAL and no new WARN
- [ ] `python scripts/todo-graph.py plan --check` -- the plan current
- [ ] `python scripts/todo-claims.py` -- every claim holds
- [ ] The parity check -- Tinctura's catalog fully routed
- [ ] `python scripts/build-app-icons.py --check` and `python scripts/build-design-site.py --check` -- the identity current
