---
schema_version: 1
id: stilus-release-0-1
domain: 02-stilus
status: draft
title: "TODO-05 -- Stilus 0.1.0"
depends_on: []
track: N5
---

# TODO-05 -- Stilus 0.1.0

> **Goal:** Stilus ships its first real release, `stilus-v0.1.0`: an About dialog that says what it is, a keyboard-shortcuts dialog generated from the one keymap, a Help menu whose every item works, a user guide covering every surface, and a tag that produces a verified installer and portable ZIP on `download.rizonesoft.com`, with a GitHub release that links them.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `MainWindowViewModel.About`, `KeyboardShortcuts`, and `Documentation` end in `// TODO` comments and do nothing (lines 1046, 980, 973); `CheckUpdates` sets status text. There is no About or shortcuts dialog anywhere in `src/Stilus/`. No Stilus tag exists; the release workflow has not run (its dry run is `D00 T02 §7`). `CHANGELOG.md` has a Stilus section with no release under it, and `docs/user/README.md` has no Stilus guide pages. **Corrected 2026-09-27:** operator decisions that day: the copyright holder is Rizonetech (Pty) Ltd and Rizonesoft is its brand, so the About dialog states "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd" and "Rizonesoft is a brand of Rizonetech (Pty) Ltd." with the GPL source offer (the About section of `docs/design/components/Dialog/README.md`); and binaries are distributed only from rizonesoft.com (`download.rizonesoft.com`), never attached to a GitHub release, so the release in §4 uploads through `release.yml` to storage the operator provisions in `D99 T01 §8`, and §4 now depends on that step.
<!-- claim: count "// TODO: Show about dialog" src/Stilus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 1 -->
<!-- claim: absent src/Stilus/Bezier.Desktop/Views/AboutDialog.xaml -->
<!-- claim: absent docs/user/stilus -->

## Inputs

- [`standards/release.md`](../../standards/release.md) -- the release checklist §4 runs line by line
- [`CHANGELOG.md`](../../CHANGELOG.md) -- the Stilus section §4 fills
- [`LICENSE`](../../LICENSE) -- GPL-3.0 text the About dialog links
- -> XREF: D01 T01 §4 -- moves §1 and §2's dialogs to `Isotone.UI` the day Pinxit needs them
- -> XREF: D06 T01 §1 -- the Stilus user guide §4 requires
- -> XREF: D05 T01 §1 -- the clean-machine proof §4 requires
- -> XREF: D00 T02 §8 -- the .NET 11 GA SDK pin §4 waits for, so no release ships on a release-candidate SDK
- -> XREF: D02 T07 §1 -- the Stilus parity phases (4 to 13) that follow the 0.1.0 release §4 ships
- -> XREF: D02 T16 §3 -- the shortcut sets that extend §2's shortcuts dialog, and the Help entries `D02 T16 §6` and `§9` add to §3's menu
- -> XREF: D02 T17 §1 -- the parity releases (0.2.0 to 1.0.0) that repeat §4's release procedure
- -> XREF: D99 T01 §8 -- the download storage and secrets §4's tag release uploads to; without them the release workflow fails by design
- -> XREF: D99 T01 §9 -- the product page URL (`ISOTONE_SITE_URL`) §1's About dialog and §4's README link use

## Outcome

- Help, About Stilus shows the name, version (from the assembly's informational version, which MinVer sets), "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd", "Rizonesoft is a brand of Rizonetech (Pty) Ltd.", license with a link to the GPL-3.0 text, the source offer "Source code: <GitHub tag URL>", the product page, credits for every bundled third-party package with its license, and links to the repository and issue tracker.
- Help, Keyboard Shortcuts lists every shortcut from the keymap, searchable, grouped by category.
- Help, Documentation opens the Stilus user guide; Check for Updates is disabled with a tooltip naming `D05 T01 §4`.
- `stilus-v0.1.0` is a published GitHub release whose installer and ZIP, served from `https://download.rizonesoft.com/stilus/0.1.0/` and linked from the release body, pass the release checklist in `standards/release.md`.

**Adjacency:** list=applicable @ D02 T05 §2; document=not-applicable (nothing printed here); settings=not-applicable (no new settings); reporting=applicable @ D02 T05 §1; notifications=not-applicable (no long operations); permissions=not-applicable (nothing written); audit=not-applicable (no document or setting changes); exchange=not-applicable (no formats); reverse=not-applicable (no edits)

**Adjacency rationale:** The shortcuts dialog is a searchable list; the About dialog is the app's report about itself (version, license, components).

## Implementation Order

| Order | Section | Deliverable                            | Depends On                                                                              | Status |
| :---: | :-----: | -------------------------------------- | --------------------------------------------------------------------------------------- | :----: |
|   1   |   §1    | The About dialog                       | D02 T03 §2                                                                              |  [ ]   |
|   2   |   §2    | The keyboard shortcuts dialog          | D02 T02 §8                                                                              |  [ ]   |
|   3   |   §3    | The Help menu                          | §1, §2                                                                                  |  [ ]   |
|   4   |   §4    | Stilus 0.1.0                            | §3, D02 T01 §7, D02 T03 §5, D02 T04 §6, D01 T01 §3, D06 T01 §1, D05 T01 §1, D00 T02 §7, D00 T02 §8, D99 T01 §8 |  [ ]   |

---

## 1. The About Dialog

A user reporting a bug needs the exact version; a GPL-3.0 application must make its license and its components' licenses reachable. Only Stilus needs this dialog now, so it is built in Stilus; `D01 T01 §4` moves it to `Isotone.UI` when Pinxit needs one.

**Fidelity:** About dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/about/.
**Design:** docs/design/components/Dialog/README.md#about-dialog, docs/design/components/AppIcon/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: About dialog -- new build, no baseline; captured to docs/captures/stilus/about/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a user can see exactly which Stilus they run and under what license, and copy the version for a bug report. Consumer: the user and bug reports.
**Treatment:** a fixed-size dialog with the Stilus icon, name, version (informational version including the commit), "Copy version info" (version, commit, .NET runtime, Windows build), license line with a link opening the GPL-3.0 text, a credits list (package, version, license, link) generated at build time from the packages the app references, and repository and issue links. Cheaper substitute that fails the checkpoint: a `MessageBox` with a version string.

**Corrected 2026-09-27:** the operator's ownership decision adds three lines, in the order of the About section in `docs/design/components/Dialog/README.md`: "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd", "Rizonesoft is a brand of Rizonetech (Pty) Ltd.", and the GPL source offer "Source code: https://github.com/rizonesoft/Isotone/tree/stilus-v<version>" (the commit URL for an untagged build); and a product page link read from one configured value (default `https://www.rizonesoft.com/`, decided per app in `D99 T01 §9`), never typed into the view. The copyright text is read from the assembly's `AssemblyCopyrightAttribute` (set by `Directory.Build.props`), not restated.
**Chrome:** consume the theme resources and the icon catalog. Do not hardcode colors or a version.

**Requires:** display-session -- capturing and driving the dialog needs an interactive desktop

- [ ] Add `AboutDialog.xaml(.cs)` and `AboutViewModel` in `Isotone.Stilus.Desktop/Views/` and `ViewModels/`, reading `AssemblyInformationalVersionAttribute`. Done when: `AboutViewModelTests` assert the version equals the assembly's and the copied text contains version, runtime, and OS build.
- [ ] Generate the credits list: an MSBuild target in `Isotone.Stilus.Desktop.csproj` writes `credits.json` from the resolved `PackageReference` items with their license expressions (read from each package's nuspec in the restore output) as an embedded resource. Done when: the dialog lists every package in the published folder's `*.deps.json` and a test asserts none has an empty license.
- [ ] Links open with `Process.Start` (UseShellExecute) and log the URL. Done when: a driven click logs the line.
- [ ] Add the ownership and source-offer lines to `AboutViewModel`: `Copyright` from `AssemblyCopyrightAttribute`, the brand line, `SourceUrl` built from the informational version (`https://github.com/rizonesoft/Isotone/tree/stilus-v<version>` for a release build, `.../commit/<sha>` otherwise), and `ProductPageUrl` from the one configured value (default `https://www.rizonesoft.com/`). Done when: `AboutViewModelTests` assert the copyright equals "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd", the brand line is present, a `0.1.0+<sha>` version yields the `stilus-v0.1.0` tree URL, and a `0.1.1-alpha.0.3+<sha>` version yields the commit URL. Cheaper substitute that fails: a hardcoded copyright string or source URL, which the version cases catch.
- [ ] Keyboard: Escape and Enter close; Tab reaches every link and button; each has an automation name. Done when: a driven keyboard-only pass works.
- [ ] Commit: `"stilus: an About dialog with version, license, and credits"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `AboutViewModelTests` reporting; in a published build (`pwsh scripts/publish.ps1 -App Stilus -Version 0.1.0-test`), the dialog shows `0.1.0-test` and the credits list matches `Stilus.deps.json` package for package (quote the counts); capture committed. Cheaper substitute that fails: a hardcoded credits list, which the deps comparison catches.

## 2. The Keyboard Shortcuts Dialog

The keymap (`D02 T02 §8`) is the single source of shortcuts; this dialog presents it, so it can never disagree with the app. Built in Stilus now, moved to `Isotone.UI` by `D01 T01 §4`.

**Fidelity:** Keyboard shortcuts dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/shortcuts/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Keyboard shortcuts dialog -- new build, no baseline; captured to docs/captures/stilus/shortcuts/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a user can find the shortcut for any command by searching its name. Consumer: the user.
**Treatment:** a resizable dialog with a search box (filters as you type, by command or gesture), a grouped list (File, Edit, View, Object, Path, Tools), and "Print" (renders the list to the Windows print dialog); read-only in 0.1.0 (remapping is `D02 T06 §13`). Cheaper substitute that fails the checkpoint: a static image or a hardcoded table.
**Chrome:** consume the theme and the keymap. Do not keep a second list of shortcuts.

**Requires:** display-session -- capturing and driving the dialog needs an interactive desktop

- [ ] Add `ShortcutsDialog.xaml(.cs)` and `ShortcutsViewModel` bound to `ShortcutManager`'s keymap. Done when: `ShortcutsViewModelTests` assert every keymap entry appears and search by "undo" returns Ctrl+Z.
- [ ] Empty search result shows "No shortcut matches '<text>'." Done when: the empty state renders.
- [ ] Print renders the grouped list through `PrintDialog.PrintDocument` with a `FlowDocument`. Done when: printing to "Microsoft Print to PDF" produces a PDF listing every group (file committed under `docs/captures/stilus/shortcuts/`).
- [ ] Commit: `"stilus: a searchable, printable keyboard shortcuts dialog"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `ShortcutsViewModelTests` reporting; adding a keymap entry makes it appear in the dialog with no dialog change; capture and printed PDF committed. Cheaper substitute that fails: a hardcoded list, which the new-entry check catches.

## 3. The Help Menu

Every Help item must work or name its owner (the rule `D02 T03 §5` enforces). Documentation opens the user guide on GitHub (the guide ships in the repository; a hosted site is `D06 T02 §3`).

**Fidelity:** Stilus main window, Help menu -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/main-window/. Items in order: Documentation (F1), Keyboard Shortcuts (Ctrl+/), Check for Updates, separator, About Stilus.
**Design:** docs/design/components/Menu/README.md, docs/design/shell-layout.md#stilus-vector -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Stilus main window, Help menu -- docs/captures/stilus/main-window/. Items in order: Documentation (F1), Keyboard Shortcuts (Ctrl+/), Check for Updates, separator, About Stilus. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a user can reach help, shortcuts, and version information from one menu. Consumer: the user.
**Treatment:** Documentation opens `https://github.com/rizonesoft/Isotone/blob/main/docs/user/stilus/README.md` in the default browser; Keyboard Shortcuts and About open §2 and §1; Check for Updates is disabled with the tooltip `Planned: D05 T01 §4`. Cheaper substitute that fails the checkpoint: a Help menu with items that set status text.
**Chrome:** consume the keymap for gestures and `PlannedCommands` for the disabled item. Do not add a second help system.

**Requires:** display-session -- driving the Help menu needs an interactive desktop

- [ ] Wire `Documentation`, `KeyboardShortcuts`, and `About` to open the browser, §2, and §1, deleting the three `// TODO` comments. Done when: `grep -c "// TODO" src/Stilus/Isotone.Stilus.Desktop/ViewModels` prints 0.
- [ ] Mark `CheckUpdates` planned through `PlannedCommands.cs`. Done when: `MenuAuditTests` passes with it.
- [ ] Commit: `"stilus: a Help menu where every item works or names its owner"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `MenuAuditTests` reporting; a driven run of F1, Ctrl+/, and About opens the browser (log line with the URL quoted), the shortcuts dialog, and the About dialog. Cheaper substitute that fails: leaving Documentation as a TODO.

## 4. Stilus 0.1.0

The first real release proves the whole product path for one app: every gate green, the changelog and guide current, the installer clean on a machine that has never seen .NET, and the tag producing a verified GitHub release. It follows the checklist in `standards/release.md` exactly, quoting each line's evidence. It builds on the .NET 11 GA SDK (`D00 T02 §8`), never on the release candidate the toolchain upgrade of 2026-09-26 pinned. The clean machine is Windows 11 (the supported OS); an extra Windows 10 22H2 smoke is optional and best-effort, its failures recorded rather than blocking.

**Needs:** Clean Windows machine (no .NET SDK)

**Corrected 2026-09-27:** added the backlog review before the tag (operator decision 2026-09-27, "Release-time backlog gate", with "No drop without operator approval"; `todo/README.md`, The budget and the backlog): every backlog entry for Stilus or the suite is promoted into a section or deferred by the operator in words recorded on the entry as a `reviewed: stilus-v0.1.0` field, and `validate` refuses this section's stamp while one is unreviewed (`release-backlog-unreviewed`).

- [ ] Run `pwsh scripts/check-all.ps1` at the release commit. Done when: every gate is `PASS` (table quoted).
- [ ] Write the `stilus-v0.1.0` section of `CHANGELOG.md` listing every user-visible change since the import (group by Added, Changed, Fixed; source: `git log` of the Stilus sections). Done when: the section exists and names the release date.
- [ ] Confirm the user guide covers every surface shipped (`D06 T01 §1`'s surface list against the menu audit). Done when: no surface lacks a page.
- [ ] Build `pwsh scripts/package.ps1 -App Stilus -Version 0.1.0` locally and run the clean-machine procedure from `D05 T01 §1`: install per-user and all-users, launch, open a fixture, save, uninstall; install the alpha from `D00 T02 §7` first and upgrade over it. Done when: every step passes and is quoted.
- [ ] Confirm `D99 T01 §8` is done: the four `ISOTONE_DL_S3_*` secrets exist (`gh secret list` names them) and `https://download.rizonesoft.com/` answers over HTTPS. Done when: both are quoted; a tag pushed without them fails the workflow by design.
- [ ] Show the GPL source offer in the installer: `installer/common.iss` sets `AppComments` (and the Finished page text) to "Source code: https://github.com/rizonesoft/Isotone/tree/<tag>" from a `/DAppTag=<tag>` define that `scripts/package.ps1` passes (`<prefix>-v<version>`, the commit URL for an untagged build). Done when: the built Setup.exe's Add or Remove Programs entry (`Comments` under the uninstall key) shows the tag URL, quoted.
- [ ] Run the backlog review for `stilus-v0.1.0`: list the entries with `python scripts/todo-graph.py query backlog`, and for every entry whose `app:` is `stilus` or `suite`, either promote it into a section through `add-todo` or ask the operator whether it may wait and append `-- reviewed: stilus-v0.1.0 <YYYY-MM-DD> deferred by operator: "<their words>"` to the entry (`-- reviewed: stilus-v0.1.0 <YYYY-MM-DD> promoted DNN TNN §N` when only part of it became a section). Done when: every in-scope entry is promoted or carries a `reviewed: stilus-v0.1.0` field (list quoted), so the stamp passes `release-backlog-unreviewed`.
- [ ] Push the tag `stilus-v0.1.0`. Done when: the `release` workflow run is `success` (URL quoted).
- [ ] Download the release files from `https://download.rizonesoft.com/stilus/0.1.0/` (the links in the release body) and verify `SHA256SUMS` and the body's SHA-256 table; confirm `https://download.rizonesoft.com/update/stilus.json` names 0.1.0; run the portable ZIP from an empty folder (**Corrected 2026-09-27:** said download the release assets, which GitHub releases no longer carry). Done when: hashes match, the feed names 0.1.0, and the portable app starts.
- [ ] Update `README.md`'s Stilus status line and download link, the link pointing at the product page (`ISOTONE_SITE_URL` with `?utm_source=github&utm_medium=readme`) and the version folder on `download.rizonesoft.com`, never at a GitHub asset (coordinate with the repo-face owner; the line is a fact, not marketing). Done when: the README names 0.1.0 as the current Stilus release.
- [ ] Commit: `"release: Stilus 0.1.0"`

**Requires:** display-session -- launching the installed app on the clean machine needs an interactive desktop

**Test checkpoint:** `gh release view stilus-v0.1.0 --json isPrerelease,assets,body` shows `isPrerelease: false`, no assets, and a body linking the installer, the ZIP, and `SHA256SUMS` under `https://download.rizonesoft.com/stilus/0.1.0/` with the source link to the tag; every checklist line in `standards/release.md` has quoted evidence in this section's stamp; `Get-FileHash` of the downloaded installer matches `SHA256SUMS`. Cheaper substitute that fails: tagging from a developer machine without the clean-machine run.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0 at the tagged commit
- [ ] The `stilus-v0.1.0` release exists with installer, ZIP, and checksums that match
- [ ] Every Help item works or names its owner
- [ ] `python scripts/todo-graph.py validate` clean
