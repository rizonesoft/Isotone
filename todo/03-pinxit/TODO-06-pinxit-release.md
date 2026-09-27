---
schema_version: 1
id: pinxit-release-0-1
domain: 03-pinxit
status: draft
title: "TODO-06 -- Pinxit 0.1.0"
depends_on: []
track: I6
---

# TODO-06 -- Pinxit 0.1.0

> **Goal:** Pinxit ships its first real release, `pinxit-v0.1.0`: the shared About and shortcuts dialogs with Pinxit's identity, a menu bar where every item works or names the section that builds it, a user guide, and a tag that produces a verified installer and portable ZIP.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `MainWindowViewModel.About`, `KeyboardShortcuts`, and `Documentation` exist as commands in Pinxit and only log. No Pinxit tag exists, `CHANGELOG.md` has no Pinxit release, and `docs/user/` has no Pinxit pages. The Stilus release (`D02 T05 §4`) and the shared dialogs (`D01 T01 §4`) are the pattern this file follows.
<!-- claim: count "private void (About|KeyboardShortcuts|Documentation)\(\)" src/Pinxit/src/Pinxit.UI/ViewModels/MainWindowViewModel.cs = 3 -->
<!-- claim: absent docs/user/pinxit -->

## Inputs

- [`standards/release.md`](../../standards/release.md) -- the release checklist §3 runs line by line
- -> XREF: D01 T01 §4 -- the shared About and shortcuts dialogs §1 wires into Pinxit
- -> XREF: D06 T01 §2 -- the Pinxit user guide §3 requires
- -> XREF: D05 T01 §1 -- the clean-machine procedure §3 runs
- -> XREF: D04 T02 §7 -- Albumen's Edit in Pinxit, which relies on the App Paths entry Pinxit's installer writes
- -> XREF: D03 T08 §1 -- Pinxit parity document and view cites §3: Pinxit 0.1.0 ships before every section there
- -> XREF: D03 T20 §8 -- Pinxit parity workspace cites §1: the Help menu, About, and shortcuts dialog D03 T20 §8 extends
- -> XREF: D03 T21 §1 -- the Pinxit parity releases cites §3: the 0.1.0 release procedure every section repeats; D03 T21 §1 follows it; §2: the menu audit each release re-runs so no item is disabled without an owner

## Outcome

- Help, About Pinxit and Help, Keyboard Shortcuts show the shared dialogs with Pinxit's identity, credits, and keymap; Help, Documentation opens the Pinxit guide.
- A `MenuAuditTests` for Pinxit proves every menu item works or names a resolvable section.
- `pinxit-v0.1.0` is a published GitHub release, its files served from `https://download.rizonesoft.com/pinxit/0.1.0/` and linked from its body, that passes the checklist in `standards/release.md`.

**Adjacency:** list=applicable @ D03 T06 §1; document=not-applicable (nothing printed here); settings=not-applicable (no new settings); reporting=applicable @ D03 T06 §1; notifications=not-applicable (no long operations); permissions=not-applicable (nothing written); audit=not-applicable (no document changes); exchange=not-applicable (no formats); reverse=not-applicable (no edits)

**Adjacency rationale:** The shortcuts dialog is the searchable list and the About dialog is the app's report about itself, both shared with Stilus through `Isotone.UI`.

## Implementation Order

| Order | Section | Deliverable                                       | Depends On                                                                  | Status |
| :---: | :-----: | ------------------------------------------------- | --------------------------------------------------------------------------- | :----: |
|   1   |   §1    | About, shortcuts, and help in Pinxit               | D01 T01 §4, D03 T03 §4                                                      |  [ ]   |
|   2   |   §2    | Every Pinxit menu command works or names its owner | §1, D03 T03 §8, D03 T04 §6, D03 T05 §3                                      |  [ ]   |
|   3   |   §3    | Pinxit 0.1.0                                       | §2, D03 T01 §4, D03 T02 §5, D06 T01 §2, D05 T01 §1                          |  [ ]   |

---

## 1. About, Shortcuts, and Help in Pinxit

`D01 T01 §4` moves Stilus's About and shortcuts dialogs to `Isotone.UI` and wires them into Pinxit's Help menu; this section completes Pinxit's Help menu around them: Documentation opens the Pinxit guide, and Check for Updates is disabled with a tooltip naming `D05 T01 §4`.

**Fidelity:** Pinxit Help menu, About, and Shortcuts dialogs -- docs/design/components/ (Menu, Dialog, ListTree, AppIcon, TextBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/about/, docs/captures/golden/pinxit/shortcuts/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/AppIcon/README.md, docs/design/components/TextBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a Pinxit user can reach help, shortcuts, and version information. Consumer: the user.
**Treatment:** Help, Documentation (F1) opens `https://github.com/rizonesoft/Isotone/blob/main/docs/user/pinxit/README.md`; Keyboard Shortcuts shows the Pinxit keymap (`D03 T03 §4`); About shows Pinxit's identity and generated credits; Check for Updates disabled with `Planned: D05 T01 §4`. Cheaper substitute that fails the checkpoint: log-only Help commands.
**Chrome:** consume `Isotone.UI` `AboutDialog` and `ShortcutsDialog`, `AppIdentity`, and a credits list generated the way Stilus's is. Do not copy the dialogs.

**Requires:** display-session -- driving the Help menu needs an interactive desktop

- [ ] Generate Pinxit's credits list at build time from its package references, as Stilus does. Done when: a test asserts every package in `Pinxit.deps.json` appears with a license.
- [ ] Wire Documentation, and mark Check for Updates planned. Done when: a driven F1 opens the browser (URL logged).
- [ ] Commit: `"pinxit: a complete Help menu on the shared dialogs"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with the credits test reporting; a driven run opens all three Help surfaces (log lines quoted). Cheaper substitute that fails: a hand-written credits list.

## 2. Every Pinxit Menu Command Works or Names Its Owner

The surface-completeness rule applies to Pinxit's menus as it did to Stilus's (`D02 T03 §5`): a shipped menu item either works or is disabled with a tooltip naming a resolvable section.

**Fidelity:** Pinxit menu bar and every menu -- docs/design/components/ (Menu, WindowChrome, Tooltip) and the Pinxit (raster) region of docs/design/shell-layout.md, per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Menu/README.md, docs/design/components/WindowChrome/README.md, docs/design/components/Tooltip/README.md, docs/design/shell-layout.md#pinxit-raster -- states: all in spec -- themes: all four -- density: both
**Job:** a Pinxit user never clicks a menu item that silently does nothing. Consumer: the user.
**Treatment:** a `PlannedCommands` table and a Pinxit `MenuAuditTests` enumerating every `MenuItem`, as in Stilus. Cheaper substitute that fails the checkpoint: hiding unfinished items.
**Chrome:** consume the pattern Stilus built; if the helper is identical, move it to `Isotone.UI` in this section and have both apps consume it.

**Requires:** display-session -- the driven pass over every menu item needs an interactive desktop

- [ ] Classify every remaining log-only command (Preferences, Export, Cut, Copy, Paste, and any the audit finds) as wired here or planned with a section (clipboard is small enough to wire now through the Windows clipboard as PNG plus an internal format). Done when: `grep -nE "\"(Opening |[A-Za-z ]+ requested|[A-Za-z ]+ dialog for)" src/Pinxit/Isotone.Pinxit.Desktop/ViewModels` finds no command whose whole body logs (**Corrected 2026-09-28:** the old grep missed the Cut, Copy, Paste, Export, and Save As stubs).
- [ ] Add `MenuAuditTests` for Pinxit. Done when: it fails on a stub without a planned tooltip.
- [ ] Commit: `"pinxit: every menu command works or names the section that builds it"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with Pinxit's `MenuAuditTests` reporting; every planned ref resolves with `python scripts/todo-graph.py resolve` (loop output quoted); a driven pass of every enabled item logs 0 `[ERR]` lines. Cheaper substitute that fails: removing items.

## 3. Pinxit 0.1.0

Pinxit's first release, following `standards/release.md` exactly as Stilus's did.

**Needs:** Clean Windows machine (no .NET SDK)

**Corrected 2026-09-27:** binaries are distributed only from rizonesoft.com (operator decision 2026-09-27, `standards/release.md` Distribution): the tag's workflow uploads the installer, the portable ZIP, and `SHA256SUMS` to `https://download.rizonesoft.com/pinxit/0.1.0/` and writes the feed `update/pinxit.json`, and the GitHub release carries no attached files, only the notes, the SHA-256 table, the Download links, and the source link. So the download and checkpoint steps below read the files from `download.rizonesoft.com`, and a release cannot publish before the operator's storage step `D99 T01 §8` is done.

**Corrected 2026-09-27:** added the backlog review before the tag (operator decision 2026-09-27, "Release-time backlog gate", with "No drop without operator approval"; `todo/README.md`, The budget and the backlog): every backlog entry for Pinxit or the suite is promoted into a section or deferred by the operator in words recorded on the entry as a `reviewed: pinxit-v0.1.0` field, and `validate` refuses this section's stamp while one is unreviewed (`release-backlog-unreviewed`).

- [ ] `pwsh scripts/check-all.ps1` at the release commit. Done when: every gate is `PASS` (table quoted).
- [ ] Write the `pinxit-v0.1.0` section of `CHANGELOG.md`. Done when: it lists every user-visible change since the import.
- [ ] Confirm the user guide covers every shipped surface. Done when: no surface lacks a page.
- [ ] Package locally and run the clean-machine procedure from `D05 T01 §1` (install per-user and all-users, open each fixture format, save, uninstall; file associations opt-in). Done when: every step passes and is quoted.
- [ ] Run the backlog review for `pinxit-v0.1.0`: list the entries with `python scripts/todo-graph.py query backlog`, and for every entry whose `app:` is `pinxit` or `suite`, either promote it into a section through `add-todo` or ask the operator whether it may wait and append `-- reviewed: pinxit-v0.1.0 <YYYY-MM-DD> deferred by operator: "<their words>"` to the entry (`-- reviewed: pinxit-v0.1.0 <YYYY-MM-DD> promoted DNN TNN §N` when only part of it became a section). Done when: every in-scope entry is promoted or carries a `reviewed: pinxit-v0.1.0` field (list quoted), so the stamp passes `release-backlog-unreviewed`.
- [ ] Push `pinxit-v0.1.0`; verify the workflow, the files and `SHA256SUMS` on `download.rizonesoft.com`, and the update feed; run the portable ZIP from an empty folder. Done when: all pass (URLs and hashes quoted).
- [ ] Update `README.md`'s Pinxit status line. Done when: it names 0.1.0.
- [ ] Commit: `"release: Pinxit 0.1.0"`

**Requires:** display-session -- launching the installed app on the clean machine needs an interactive desktop

**Test checkpoint:** `gh release view pinxit-v0.1.0 --json isPrerelease,assets,body` shows a non-prerelease, no assets, and a body linking the installer, the ZIP, and `SHA256SUMS` under `https://download.rizonesoft.com/pinxit/0.1.0/`; every checklist line has quoted evidence; the downloaded installer's hash matches `SHA256SUMS`. Cheaper substitute that fails: tagging without the clean-machine run.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0 at the tagged commit
- [ ] The `pinxit-v0.1.0` release exists with matching checksums
- [ ] `python scripts/todo-graph.py validate` clean
