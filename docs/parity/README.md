# Parity

This folder is the evidence behind three operator decisions, two recorded on 2026-09-26 and one on 2026-09-27. **Stilus** gets every CorelDRAW feature and every Illustrator feature: "For Nodus, we need to add all(and I mean), all CorelDraw features and All Illustrator Features." **Gesso** gets every Photoshop feature and every feature of two other popular programs of the same kind, chosen as Affinity Photo and GIMP 3: "now, imago, all the photoshop and at least 2 other similar popular programs of the same type. All features without leaving anything behind." The budget raises that pay for them are quoted in `todo/budget.json` ("New parity phases, up to +200" and "New Imago parity phases, up to +250"). **Albumen** gets the features of Lightroom Classic, ACDSee Photo Studio Ultimate, and IrfanView: "Now Lumen. I want features from Lightroom, but I've alwyas been loving ACDSee photo manager and IrfanView", with the approved option "New Lumen parity phases, up to +200" placed after Albumen 0.1.0; ACDSee's layered Edit mode routes to Gesso, and the operator's three pillars are a fast default image viewer, browsing without importing, and batch tools as core Albumen features. On 2026-09-27 the operator removed the phase and total ceilings those raises were made against ("Why is there a phase limit on planning, should the limit not only be on new sections beign created automatically, but even then that shoiuld not be a small limit"): parity sections the operator directs are never capped, and only sections a campaign discovers on its own count against a cap of 15 per phase run (`todo/README.md`, "The budget and the backlog"). The design records below keep their budget arithmetic as written.

The same day the operator deferred video and animation, and macros and scripting, to after the first release instead of excluding them, with macros and scripting planned as one suite-wide system for Stilus, Gesso, and Albumen. All three catalogs routed those rows to the backlog entries that held that work (B-041 to B-044, with B-043 made suite-wide for Albumen video and audio); cloud and collaboration stay excluded. Albumen's own batch rename, convert, resize, edit, develop, and export are planned sections of `D04 T11`. On 2026-09-27, because the operator worried "features will be left behind", those entries, the on-device models (B-046), the GPU develop path (B-033), and the formats with no GPL-compatible reader (B-050) became real sections in the post-release Phases 42 to 45 (and `D04 T13 §9` in Phase 30), and the 160 catalog rows that named them were repointed to their `plan` sections (11 Stilus, 86 Gesso, 63 Albumen).

## What is here

| File | Purpose |
| ---- | ------- |
| [`sources/illustrator-30.8.md`](sources/illustrator-30.8.md) | The Adobe Illustrator 30.8 feature inventory (August 2026 release), rows `AI-0001` to `AI-1294`, verbatim as compiled on 2026-09-26 |
| [`sources/coreldraw-2026.md`](sources/coreldraw-2026.md) | The CorelDRAW Graphics Suite 2026 v27.2 feature inventory (September 2026 update), rows `CD-001` to `CD-3041`, verbatim as compiled on 2026-09-26 |
| [`stilus-parity.md`](stilus-parity.md) | The Stilus catalog: every Illustrator and CorelDRAW row merged into Stilus features (`NP-####`), each with exactly one status |
| [`section-design.md`](section-design.md) | The authoring blueprint for the Stilus parity TODO files. Integrated into `todo/` on 2026-09-26 (14 new TODO files, `D00 T01 §6`, Phases 4 to 13 of `todo/implementation-plan.md`); from then on the TODO files are the plan and this file is the design record |
| [`sources/photoshop-27.10.md`](sources/photoshop-27.10.md) | The Adobe Photoshop 27.10 feature inventory (August 2026 release, with Camera Raw 18.6), in two parts: rows `PS-A-0001` to `PS-A-1750` and `PS-B-0001` to `PS-B-1426`, verbatim as compiled on 2026-09-26 |
| [`sources/affinity-3.3.md`](sources/affinity-3.3.md) | The Affinity by Canva 3.3 inventory (the Pixel Studio and photo studios that succeed Affinity Photo 2), rows `AF-0001` to `AF-2762`, verbatim as compiled on 2026-09-26 |
| [`sources/gimp-3.2.6.md`](sources/gimp-3.2.6.md) | The GIMP 3.2.6 inventory, rows `GP-0001` to `GP-4891` (one row per documented option), verbatim as compiled on 2026-09-26 |
| [`gesso-parity.md`](gesso-parity.md) | The Gesso catalog: every Photoshop, Affinity, and GIMP row merged into Gesso features (`IP-####`), each with exactly one status |
| [`sources/lightroom-classic-15.5.1.md`](sources/lightroom-classic-15.5.1.md) | The Adobe Lightroom Classic 15.5.1 inventory (August 2026), rows `LR-0001` to `LR-1857`, verbatim as compiled on 2026-09-27 |
| [`sources/acdsee-ultimate-2027.md`](sources/acdsee-ultimate-2027.md) | The ACDSee Photo Studio Ultimate 2027 inventory (build 20.0, September 2026), rows `AC-0001` to `AC-5182`, verbatim as compiled on 2026-09-27 |
| [`sources/irfanview-4.76.md`](sources/irfanview-4.76.md) | The IrfanView 4.76 x64 inventory with the PlugIns package 4.76 (September 2026), rows `IV-0001` to `IV-1880`, verbatim as compiled on 2026-09-27 |
| [`albumen-parity.md`](albumen-parity.md) | The Albumen catalog: every Lightroom Classic, ACDSee, and IrfanView row merged into Albumen features (`LP-####`), each with exactly one status; ACDSee Edit-mode rows route to named Gesso rows |
| [`albumen-section-design.md`](albumen-section-design.md) | The authoring blueprint for the Albumen parity TODO files: 12 new files, 138 designed sections, Phases 30 to 39 (distribution and the later phases renumbered to 40 and 41), `D00 T01 §8`, the backlog changes, the Gesso additions, and the authoring batches. Integrated into `todo/` on 2026-09-27 (12 new TODO files with 140 sections, six more than designed after four authoring splits and two added sections, `D00 T01 §8`, `D01 T07 §7` to `§9`, Phases 30 to 39 of `todo/implementation-plan.md`, with distribution renumbered 40 and the shared-decoder imports 41); from then on the TODO files are the plan, and where the integration departed from this design (the originals opt-ins, `D01 T07 §7` in Phase 23, the guided filter and PatchMatch in `Isotone.Core`, the plug-in host and legacy codec rows, B-051) the TODO files record it |
| [`gesso-section-design.md`](gesso-section-design.md) | The authoring blueprint for the Gesso parity TODO files: files, sections, phases 16 to 27, dependencies, hints, the budget entry, and authoring batches. Integrated into `todo/` on 2026-09-26 (16 new TODO files, `D00 T01 §7`, Phases 16 to 27 of `todo/implementation-plan.md`, with Albumen, distribution, and the later phases renumbered 28 to 32); from then on the TODO files are the plan and this file is the design record |

The sources are provenance: each row names its version, its menu location, and the help page it came from. They are never edited except to append rows for a newer version (below).

## Sources and versions

- **Illustrator:** Adobe Illustrator 2026, version 30.8 (August 2026), current LTS 29.8.7; read from Adobe's help and release-notes pages through a browser session. The inventory lists its primary sources at its top.
- **CorelDRAW:** CorelDRAW Graphics Suite 2026, version 27.2 (September 2026 Update); read from the CorelDRAW Graphics Suite 2025 (v26) Help (the newest public Help) plus Corel's 2026 what's-new, update, and press pages. The inventory records that caveat at its top.
- **Photoshop:** Adobe Photoshop 2026, version 27.10 (August 2026), current LTS 26.11.7, with Camera Raw 18.6. Adobe's CDN refused the session after about 30 page loads, so option-level rows for long-standing dialogs come from documented product knowledge citing the nearest User Guide page; the file's provenance note says so.
- **Affinity Photo:** Affinity by Canva 3.3 (September 2026 Update). The help site rate-limited the session after about 200 pages, so the rest came from the Affinity Photo 2 help and some rows carry Photo 2 wording; rows marked "(Photo 2 only)" are documented for Photo 2 but absent or replaced in 3.3.
- **GIMP:** GIMP 3.2.6 (September 2026); the GIMP 3.2 manual (all 760 English pages), the GEGL operations reference, and the 3.0 to 3.2.6 release notes were read in full.
- **Lightroom Classic:** Lightroom Classic 15.5.1 (2026-08-31, on the 15.5 feature release of 2026-08-04). Adobe's help answers HTTP 403 to scripted fetches, so about 28 pages were read live through a browser and most option-level rows come from documented product knowledge citing the nearest help page; the file's provenance note says so.
- **ACDSee Photo Studio Ultimate:** Ultimate 2027, build 20.0.0.4660 (2026-09-16); the full 867-page user guide PDF was read in full, with a few image-only pages thin and about 45 special-effect descriptions from product knowledge.
- **IrfanView:** IrfanView 4.76 x64 (2026-09-18) with the PlugIns package 4.76; the bundled help file (140 topics), command-line, plug-in, and change notes were read in full; 61 rows marked (PK) come partly from product knowledge.

## The catalogs

Each catalog row is one user-facing capability. Rows from the competitors that do the same job, and duplicate rows inside one app (a tool and its menu entry, a docker and its command, a destructive filter and its live version, a GIMP option and the feature it parameterizes), are merged into one feature. Columns of `stilus-parity.md`:

| Column | Meaning |
| ------ | ------- |
| `ID` | `NP-0001` onward. Stable: a number is never reused or renumbered |
| `Feature` | The capability in Stilus's words |
| `Illustrator` | The `AI-####` rows it covers, comma-separated, or `--` |
| `CorelDRAW` | The `CD-###` rows it covers, comma-separated, or `--` |
| `Category` | `core`, `format`, `print`, `ai`, `automation`, `cloud`, or `companion`, taken from the inventory rows |
| `Status` | Exactly one of the forms below |
| `Notes` | What Stilus does differently, a license note, or the reason for an exclusion |

Columns of `gesso-parity.md`:

| Column | Meaning |
| ------ | ------- |
| `ID` | `IP-0001` onward. Stable: a number is never reused or renumbered |
| `Feature` | The capability in Gesso's words |
| `Photoshop` | The `PS-A-####` and `PS-B-####` rows it covers, comma-separated, or `--` |
| `Affinity` | The `AF-####` rows it covers, comma-separated, or `--` |
| `GIMP` | The `GP-####` rows it covers, comma-separated, or `--` |
| `Category` | `core`, `format`, `print`, `ai`, `automation`, `video`, `cloud`, or `3d`, taken from the inventory rows |
| `Status` | Exactly one of the forms below |
| `Notes` | What Gesso does differently, the engine section it consumes, "extends" the existing section it builds on, an honest limit, or the reason for an exclusion |

Columns of `albumen-parity.md`:

| Column | Meaning |
| ------ | ------- |
| `ID` | `LP-0001` onward. Stable: a number is never reused or renumbered |
| `Feature` | The capability in Albumen's words |
| `Lightroom` | The `LR-####` rows it covers, comma-separated, or `--` |
| `ACDSee` | The `AC-####` rows it covers, comma-separated, or `--` |
| `IrfanView` | The `IV-####` rows it covers, comma-separated, or `--` |
| `Category` | `core`, `format`, `print`, `ai`, `automation`, `video`, or `cloud`, taken from the inventory rows |
| `Status` | Exactly one of the forms below; an `other-app: Gesso` status names the Gesso catalog row (`IP-####`) that covers the capability |
| `Notes` | What Albumen does differently (for example a sidecar instead of writing the original), the section it extends or consumes, an honest limit, or the reason for an exclusion |

Every source id appears in exactly one row of its catalog. Keyboard-shortcut and menu rows are folded into the feature they trigger or into keymap features. The Gesso catalog's rows `IP-2368` to `IP-2385` were added on 2026-09-27 for ACDSee Edit-mode capabilities the Albumen catalog routes to Gesso; they carry no Photoshop, Affinity, or GIMP id and name the Albumen row in their notes.

## Status grammar

Exactly one status per row, the same grammar in all three catalogs:

| Status | Meaning |
| ------ | ------- |
| `plan <DNN TNN §N>` | A parity section owns the feature; the section is designed in `section-design.md` or `gesso-section-design.md` and authored under `todo/` |
| `shipped-scope <DNN TNN §N>` | A section that existed before the parity plan already owns the feature (for example `D02 T04 §2` for SVG open and save in Stilus, `D03 T05 §3` for Gaussian blur in Gesso, or a `D01 T03` pixel-engine section whose effect Gesso's Filter menu exposes) |
| `backlog B-NNN` | The feature is kept as a `todo/backlog.md` entry, not a section: a format or integration the operator declined or has not approved (Affinity files B-045, tethered capture B-048, self-running slideshows B-049, the Explorer preview handler B-051, face recognition B-052, SFTP B-053), or a decision not yet taken (Content Credentials B-047) |
| `excluded: <reason>` | Out of scope by operator decision: cloud documents, libraries, sharing, and online services (`cloud`); hardware or an OS Isotone cannot run on (`platform`); features the vendor itself has removed and lists only as removed, such as Photoshop's legacy 3D (`removed`) |
| `other-app: <Stilus|Gesso|Albumen|none> <reason>` | A feature whose job belongs to another Isotone app, or to none |

A `plan` or `shipped-scope` ref names a real section in `DNN TNN §N` form; a `backlog` id names a live backlog entry. Whether a planned feature has shipped is read from its section's Implementation Order row and stamp, never typed into the catalog. `query parity` counts the same way: features and sections are separate units, and a `shipped-scope` row's section counts as stamped only when it carries a `Verified:` stamp (Enforcement, below).

## How to update

- **A new competitor version:** compile the new inventory the same way, and append its new rows to the matching file under `sources/` with the next free ids (`AI-1295`, `CD-3042`, `PS-A-1751` or `PS-B-1427`, `AF-2763`, `GP-4892`, `LR-1858`, `AC-5183`, `IV-1881` onward) and a version note in the row's Feature or Source cell. Never renumber an existing row. Then add each new id to the catalog: merge it into an existing feature when it is the same capability, or add a new row at the end of the right area table with its status.
- **A new catalog row:** take the next free `NP-`, `IP-`, or `LP-` number, even when the row sits in the middle of an area table. A row one catalog adds for another app's routing (as the Gesso rows added for the Albumen catalog) names the routing row in its notes.
- **Rerouting a feature:** change its status in place (for example from `backlog B-041` to `plan D03 T22 §1` when the scripting entry is promoted through `add-todo`), in the same commit that changes the plan.
- **Splitting a feature:** keep the original row for one part and give each other part a new number, moving its source ids with it.

## Enforcement

`python scripts/todo-graph.py validate` reads the Stilus catalog and its two inventories (`D00 T01 §6`, 2026-10-21) and the Gesso catalog and its three (`D00 T01 §7`, 2026-10-22; Photoshop's `PS-A-` and `PS-B-` ids are one family in one file) through `scripts/todo-parity.py`, so the commit hook, the `plan-gates` workflow, and `scripts/check-all.ps1` refuse a catalog that has drifted from its sources or the plan. Every class is FATAL: `parity-id-missing` (a source id no row places), `parity-id-duplicate` (a source id two rows place), `parity-id-unknown` (a cell naming an id its source does not define), `parity-np-duplicate` and `parity-ip-duplicate` (a Stilus or Gesso feature id on two rows), `parity-status-malformed` (a status outside the grammar above), `parity-ref-dead` (a `plan` or `shipped-scope` ref naming no section, or a section that moved out of the tree), `parity-backlog-dead` (a `backlog` id naming no live entry), and `parity-input-damaged` (a catalog or inventory missing while `docs/parity/` exists, a row whose cell count differs from its header, or a source id defined twice in one file), and `parity-totals-drift` (a catalog's Totals table or Areas list that disagrees with its rows, or a part of either missing, repeated, or malformed). Every message opens with its catalog's name (`stilus:`, `gesso:`). A tree with no `docs/parity/` at all has nothing to check; with `docs/parity/` present, every configured catalog and inventory must be there. The check reads tables by a format rule stricter than GitHub Markdown: a table opens with its `| ID |` header and a separator row of the same cell count, and ends only at a blank line, so every line in between is a row that must open with a whole id and match the header's cell count. Keep a blank line between a table and whatever follows it. The rest of a catalog follows a line grammar of the same kind: it is made only of blank lines, table lines, its `# ` title and `## ` sections (at the line start, one space after the hashes, plain text: letters, digits, spaces, and `, ( ) : & ' / -`), the Areas entries under `## Areas`, and plain paragraph lines that open with no block marker (no `#`, `>`, list marker, fence, underline, or indentation); it holds no raw HTML, and no two headings share an anchor, so each Areas entry links its section's plain anchor (`#documents-and-canvas`). `D00 T01 §8` (Albumen, including a check that every `other-app: Gesso` row names a live `IP-` row) extends the same check to the last catalog; until it ships, a change to the Albumen catalog is checked by hand against the rules above in the same commit.

`python scripts/todo-graph.py query parity [--catalog stilus|gesso|all] [--phase N] [--json]` reports, per catalog (`--catalog` narrows the report and its problems to one; `all` is the default), the status totals and, per plan phase, three separate counts: `features` (catalog rows planned to the phase's sections), `sections` (the distinct sections those rows name), and `stamped_sections` (those of them carrying a `Verified:` stamp). A `shipped-scope` row counts as stamped only when its section is, so the report never reads a status as proof of shipping. A row whose section sits in no phase table is reported under `unplaced`. `--phase N` lists that phase's rows; each parity release quotes its phase's line with its app's `--catalog`.

Before the check shipped, at the Gesso integration (2026-09-26), a hand check found every `plan` and `shipped-scope` ref in both catalogs naming a live section, every `backlog` id naming a live entry (B-041 to B-047 are live), and every Gesso parity section's `Catalog:` line matching the rows that name it.

The Albumen catalog was checked on 2026-09-27 with a scratch script against the three Albumen sources, the Albumen design, the live `todo/` tree, `todo/backlog.md`, and the Gesso catalog: every `LR`, `AC`, and `IV` id placed exactly once, every `plan` ref naming a designed section, every `shipped-scope` ref naming a live section, every `other-app: Gesso` row naming an existing `IP-` row, and every `backlog` id naming a live entry except B-048 to B-050, which the integration adds (see [`albumen-section-design.md`](albumen-section-design.md), "Catalog check"). At the integration (2026-09-27) the same hand check ran again over all three catalogs against the integrated tree: every `plan` and `shipped-scope` ref names a live section, every `backlog` id names a live entry (B-041 to B-051 as they now stand), every `other-app: Gesso` row names a live `IP-` row, and every Albumen, Gesso, and Stilus parity section's `Catalog:` line matches the rows that name it.

Later on 2026-09-27 the operator's dependency and reverse-engineering decisions moved twelve Albumen rows (face recognition and the People view) to the new backlog entry B-052, noted the SFTP option of LP-0953 as B-053, recorded the clean-room approval on the Stilus legacy-format rows it covers, and noted on IP-1852 that reverse engineering Affinity files was declined (B-045 stays). The same scratch check then ran over all three catalogs: every `plan` and `shipped-scope` ref names a live section, every `backlog` status names a live entry (B-041 to B-053 as they now stand), every Albumen `other-app: Gesso` row names a live `IP-` row, every section ref and live backlog id in the notes resolves (the only other backlog ids in notes are historical mentions of retired, promoted entries), and the `Catalog:` lines of `D04 T10 §2`, `§3`, and `§12`, `D04 T12 §8` and `§9`, and `D04 T04 §8` match the rows that name them.

Later on 2026-09-27, when the operator planned the post-release work as real sections, 160 rows moved from `backlog` to `plan` (11 Stilus, 86 Gesso, 63 Albumen) and the notes that named the promoted entries were repointed. The same scratch check then ran over all three catalogs: every `plan` and `shipped-scope` ref names a live section, every `backlog` status names a live entry (B-045, B-047 to B-049, and B-051 to B-053), every section ref in the notes resolves, the only retired backlog ids left in notes are historical mentions of earlier promotions, the Totals tables equal a recount of the rows, and the `Catalog:` line of every new section matches the rows that name it.
