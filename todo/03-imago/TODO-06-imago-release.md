---
schema_version: 1
id: imago-release-0-1
domain: 03-imago
status: draft
title: "TODO-06 -- Imago 0.1.0"
depends_on: []
track: I6
---

# TODO-06 -- Imago 0.1.0

> **Goal:** Imago ships its first real release, `imago-v0.1.0`: the shared About and shortcuts dialogs with Imago's identity, a menu bar where every item works or names the section that builds it, a user guide, and a tag that produces a verified installer and portable ZIP.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `MainWindowViewModel.About`, `KeyboardShortcuts`, and `Documentation` exist as commands in Imago and only log. No Imago tag exists, `CHANGELOG.md` has no Imago release, and `docs/user/` has no Imago pages. The Nodus release (`D02 T05 §4`) and the shared dialogs (`D01 T01 §4`) are the pattern this file follows.
<!-- claim: count "private void (About|KeyboardShortcuts|Documentation)\(\)" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 3 -->
<!-- claim: absent docs/user/imago -->

## Inputs

- [`standards/release.md`](../../standards/release.md) -- the release checklist §3 runs line by line
- -> XREF: D01 T01 §4 -- the shared About and shortcuts dialogs §1 wires into Imago
- -> XREF: D06 T01 §2 -- the Imago user guide §3 requires
- -> XREF: D05 T01 §1 -- the clean-machine procedure §3 runs
- -> XREF: D04 T02 §7 -- Lumen's Edit in Imago, which relies on the App Paths entry Imago's installer writes
- -> XREF: D03 T08 §1 -- Imago parity document and view cites §3: Imago 0.1.0 ships before every section there
- -> XREF: D03 T20 §8 -- Imago parity workspace cites §1: the Help menu, About, and shortcuts dialog D03 T20 §8 extends
- -> XREF: D03 T21 §1 -- the Imago parity releases cites §3: the 0.1.0 release procedure every section repeats; D03 T21 §1 follows it; §2: the menu audit each release re-runs so no item is disabled without an owner

## Outcome

- Help, About Imago and Help, Keyboard Shortcuts show the shared dialogs with Imago's identity, credits, and keymap; Help, Documentation opens the Imago guide.
- A `MenuAuditTests` for Imago proves every menu item works or names a resolvable section.
- `imago-v0.1.0` is a published GitHub release that passes the checklist in `standards/release.md`.

**Adjacency:** list=applicable @ D03 T06 §1; document=not-applicable (nothing printed here); settings=not-applicable (no new settings); reporting=applicable; notifications=not-applicable (no long operations); permissions=not-applicable (nothing written); audit=not-applicable (no document changes); exchange=not-applicable (no formats); reverse=not-applicable (no edits)

**Adjacency rationale:** The shortcuts dialog is the searchable list and the About dialog is the app's report about itself, both shared with Nodus through `Photon.UI`.

## Implementation Order

| Order | Section | Deliverable                                       | Depends On                                                                  | Status |
| :---: | :-----: | ------------------------------------------------- | --------------------------------------------------------------------------- | :----: |
|   1   |   §1    | About, shortcuts, and help in Imago               | D01 T01 §4, D03 T03 §4                                                      |  [ ]   |
|   2   |   §2    | Every Imago menu command works or names its owner | §1, D03 T03 §8, D03 T04 §6, D03 T05 §3                                      |  [ ]   |
|   3   |   §3    | Imago 0.1.0                                       | §2, D03 T01 §4, D03 T02 §5, D06 T01 §2, D05 T01 §1                          |  [ ]   |

---

## 1. About, Shortcuts, and Help in Imago

`D01 T01 §4` moves Nodus's About and shortcuts dialogs to `Photon.UI` and wires them into Imago's Help menu; this section completes Imago's Help menu around them: Documentation opens the Imago guide, and Check for Updates is disabled with a tooltip naming `D05 T01 §4`.

**Fidelity:** Imago Help menu and the shared dialogs -- docs/captures/imago/about/ and docs/captures/imago/shortcuts/ (from `D01 T01 §4`).
**Job:** an Imago user can reach help, shortcuts, and version information. Consumer: the user.
**Treatment:** Help, Documentation (F1) opens `https://github.com/rizonesoft/Photon/blob/main/docs/user/imago/README.md`; Keyboard Shortcuts shows the Imago keymap (`D03 T03 §4`); About shows Imago's identity and generated credits; Check for Updates disabled with `Planned: D05 T01 §4`. Cheaper substitute that fails the checkpoint: log-only Help commands.
**Chrome:** consume `Photon.UI` `AboutDialog` and `ShortcutsDialog`, `AppIdentity`, and a credits list generated the way Nodus's is. Do not copy the dialogs.

**Requires:** display-session -- driving the Help menu needs an interactive desktop

- [ ] Generate Imago's credits list at build time from its package references, as Nodus does. Done when: a test asserts every package in `Imago.deps.json` appears with a license.
- [ ] Wire Documentation, and mark Check for Updates planned. Done when: a driven F1 opens the browser (URL logged).
- [ ] Commit: `"imago: a complete Help menu on the shared dialogs"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the credits test reporting; a driven run opens all three Help surfaces (log lines quoted). Cheaper substitute that fails: a hand-written credits list.

## 2. Every Imago Menu Command Works or Names Its Owner

The surface-completeness rule applies to Imago's menus as it did to Nodus's (`D02 T03 §5`): a shipped menu item either works or is disabled with a tooltip naming a resolvable section.

**Fidelity:** Imago main window, every menu -- docs/captures/imago/main-window/.
**Job:** an Imago user never clicks a menu item that silently does nothing. Consumer: the user.
**Treatment:** a `PlannedCommands` table and an Imago `MenuAuditTests` enumerating every `MenuItem`, as in Nodus. Cheaper substitute that fails the checkpoint: hiding unfinished items.
**Chrome:** consume the pattern Nodus built; if the helper is identical, move it to `Photon.UI` in this section and have both apps consume it.

**Requires:** display-session -- the driven pass over every menu item needs an interactive desktop

- [ ] Classify every remaining log-only command (Preferences, Export, Cut, Copy, Paste, and any the audit finds) as wired here or planned with a section (clipboard is small enough to wire now through the Windows clipboard as PNG plus an internal format). Done when: `grep -n "_logger.Information(\"Opening" src/Imago/Photon.Imago.Desktop/ViewModels` finds no command whose whole body logs.
- [ ] Add `MenuAuditTests` for Imago. Done when: it fails on a stub without a planned tooltip.
- [ ] Commit: `"imago: every menu command works or names the section that builds it"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with Imago's `MenuAuditTests` reporting; every planned ref resolves with `python scripts/todo-graph.py resolve` (loop output quoted); a driven pass of every enabled item logs 0 `[ERR]` lines. Cheaper substitute that fails: removing items.

## 3. Imago 0.1.0

Imago's first release, following `standards/release.md` exactly as Nodus's did.

**Needs:** Clean Windows machine (no .NET SDK)

- [ ] `pwsh scripts/check-all.ps1` at the release commit. Done when: every gate is `PASS` (table quoted).
- [ ] Write the `imago-v0.1.0` section of `CHANGELOG.md`. Done when: it lists every user-visible change since the import.
- [ ] Confirm the user guide covers every shipped surface. Done when: no surface lacks a page.
- [ ] Package locally and run the clean-machine procedure from `D05 T01 §1` (install per-user and all-users, open each fixture format, save, uninstall; file associations opt-in). Done when: every step passes and is quoted.
- [ ] Push `imago-v0.1.0`; verify the workflow, the assets, and `SHA256SUMS`; run the portable ZIP from an empty folder. Done when: all pass (URLs and hashes quoted).
- [ ] Update `README.md`'s Imago status line. Done when: it names 0.1.0.
- [ ] Commit: `"release: Imago 0.1.0"`

**Requires:** display-session -- launching the installed app on the clean machine needs an interactive desktop

**Test checkpoint:** `gh release view imago-v0.1.0 --json isPrerelease,assets` shows a non-prerelease with three assets; every checklist line has quoted evidence; the downloaded installer's hash matches `SHA256SUMS`. Cheaper substitute that fails: tagging without the clean-machine run.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0 at the tagged commit
- [ ] The `imago-v0.1.0` release exists with matching checksums
- [ ] `python scripts/todo-graph.py validate` clean
