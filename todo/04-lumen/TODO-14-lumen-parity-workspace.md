---
schema_version: 1
id: lumen-parity-workspace
domain: 04-lumen
status: draft
title: "TODO-14 -- Lumen Parity: Workspace, Preferences, and Help"
depends_on: []
frozen: true
track: L14
---

# TODO-14 -- Lumen Parity: Workspace, Preferences, and Help

> **Goal:** Lumen's workspace reaches Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 parity once every parity surface exists: modes and the module picker with the identity plate, panel groups, screen modes, and lights out; customizable toolbars, menus, favorite menus, dockable panes, saved workspaces, and touch input; one default keymap with alternative key sets, the shortcut editor, and the overlay; preference pages for general behavior, interface, file handling, the viewer and browse, performance, caches, color management, and display; the Originals group of the File Handling page where a user may opt in to writing into original files (embedding metadata, rotating in place, saving over the original, converting in place), every opt-in off by default and lockable off by an administrator, rendering the one policy `D04 T11 §1` owns (operator decision 2026-09-27: "Safe by default, opt-in writes"); settings storage with portable mode, administrator deployment, and migration from earlier installations; help, languages, and updates; themes and appearance; and external editors beyond Edit in Imago. The code lives in `src/Lumen/Photon.Lumen.Desktop/Workspace/`, `Preferences/`, and `Help/`, and in `src/Lumen/Photon.Lumen.Core/Settings/`; it consumes the workspace, toolbar, menu, and shortcut-set frames Imago moved to `src/Photon.UI/Workspace/` (`D03 T20 §1` to `D03 T20 §3`), `PreferenceKeyRegistry` in `src/Photon.Core/Settings/` and `WarningRegistry` in `src/Photon.UI/Warnings/` (`D03 T20 §4`), `SystemInfoReport` (`D03 T20 §8`), the settings store (`D01 T02 §2`), the suite theme (`D01 T01 §3`), and the update check (`D05 T01 §4`), never a second copy. The relocated accessibility and localization audit (`D04 T02 §9`) runs after this file, last before Lumen 1.0.0.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no code and no settings of its own: `src/Lumen` does not exist. The shared workspace frames do not exist yet either: `src/Photon.UI` is absent, and Imago's workspace file (`todo/03-imago/TODO-20-imago-parity-workspace.md`) is what moves them from Nodus into it. The Lumen installer `installer/Lumen.iss` is guarded by `LumenShipping` (three mentions) and has no `[Registry]` section, so it registers no file type or setting. The suite update check is planned as `## 4. The Update Check` in `todo/05-release/TODO-01-release-pipeline.md`. `scripts/apps.psd1` still names the legacy Lumen project path `src/Lumen/Lumen.UI/Lumen.UI.csproj`, which `D04 T01 §2` replaces. `standards/lumen.md` states today that Lumen never writes an original image; §10 of this file is the only place that guard gains its operator-approved opt-in exceptions, and the integration commit amends the standard to name them.
<!-- claim: absent src/Lumen -->
<!-- claim: absent src/Photon.UI -->
<!-- claim: exists todo/03-imago/TODO-20-imago-parity-workspace.md -->
<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->
<!-- claim: count "\[Registry\]" installer/Lumen.iss = 0 -->
<!-- claim: count "^## 4\. The Update Check" todo/05-release/TODO-01-release-pipeline.md = 1 -->
<!-- claim: count "src/Lumen/Lumen.UI/Lumen.UI.csproj" scripts/apps.psd1 = 1 -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- window anatomy, theme resources, the settings store, atomic writes, one log line per settings change
- [`standards/ui.md`](../../standards/ui.md) -- the UI standard and the component specs under `docs/design/components/` the chrome sections here build to (**Corrected 2026-09-27:** the design contract moved from `standards/shared.md` to `standards/ui.md` and `docs/design/`)
- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard, safe by default with the opt-in writes of `D04 T11 §1` whose settings §10 renders, and the settings location under `%LOCALAPPDATA%\Rizonesoft\Lumen\`
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- the blueprint for this file; [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows each section owns
- Operator decision 2026-09-27, "Safe by default, opt-in writes": sidecars and new files by default; opt-in settings for writing into originals owned by `D04 T11 §1` (`OriginalWritePolicy` and `InPlaceWriter`, a verified backup by default), which §10 renders and an administrator can lock off
- Lightroom Classic 15.5.1 help: workspace, preferences, catalog settings, keyboard shortcuts, external editing; ACDSee Photo Studio Ultimate 2027 guide: Options dialog, Keyboard Shortcuts, Workspaces, Quick Start; IrfanView 4.76 help: Properties dialog, `i_view64.ini`, Options menu, and the installer switches
- Microsoft Learn: WPF manipulation events, `SpellCheck`, per-monitor v2 DPI awareness, `UISettings.ColorValuesChanged`, satellite assemblies and `.resx` resources
- -> XREF: D03 T20 §1 -- the `Photon.UI/Workspace/` frame, panes, and saved workspaces §1 and §2 consume
- -> XREF: D03 T20 §2 -- the toolbar customization frame §2 consumes
- -> XREF: D03 T20 §3 -- menus, shortcut sets, and command search §3 consumes
- -> XREF: D03 T20 §4 -- `PreferenceKeyRegistry` and `WarningRegistry`, moved to the shared libraries, which §4 consumes
- -> XREF: D03 T20 §6 -- touch and pen input handling §2 reuses
- -> XREF: D03 T20 §8 -- `SystemInfoReport` and the help plumbing §7 consumes
- -> XREF: D03 T20 §9 -- interface appearance and language switching §7 and §8 follow
- -> XREF: D01 T02 §2 -- the settings store §6 extends with portable and deployment modes
- -> XREF: D01 T01 §3 -- the suite theme §8 consumes
- -> XREF: D01 T01 §8 -- the shared dock theme, menus (`D01 T01 §6`), and title bar (`D01 T01 §7`) §2's toolbars, menus, and panes are drawn with
- -> XREF: D01 T01 §4 -- the shared About and shortcuts dialog §3 and §7 consume
- -> XREF: D01 T04 §1 -- display color management §5 configures
- -> XREF: D05 T01 §1 -- the installer and portable ZIP whose switches §6 documents
- -> XREF: D05 T01 §3 -- the win-arm64 builds §7's platform page states
- -> XREF: D05 T01 §4 -- the opt-in update check §7 consumes
- -> XREF: D02 T15 §11 -- `SuiteAppLocator`, which §9 consumes for Imago
- -> XREF: D04 T01 §2 -- the shell, splash, and About §1 and §7 extend
- -> XREF: D04 T01 §7 -- the preview cache §5 sizes and purges
- -> XREF: D04 T02 §7 -- `EditInService`, which §9 extends to other editors
- -> XREF: D04 T02 §9 -- the accessibility and localization audit that runs after this file and checks keyboard reachability against §3's keymap
- -> XREF: D04 T04 §11 -- the viewer's Save, whose in-place variant the `Lumen.Originals.InPlace.Save` key §10 renders enables
- -> XREF: D04 T04 §16 -- lossless JPEG transforms, whose in-place variant the `Lumen.Originals.InPlace.Rotate` key §10 renders enables
- -> XREF: D04 T05 §2 -- the indexer §7's Quick Start feeds with folders to index
- -> XREF: D04 T06 §2 -- the keypad culling keys §3's keymap editor rebinds
- -> XREF: D04 T08 §8 -- `MetadataWriter`, whose write target the `Lumen.Originals.InPlace.EmbedMetadata` key §10 renders switches
- -> XREF: D04 T08 §9 -- the metadata-only rewriters that embed into originals when that key is on, and the per-format capability list §10's confirmation names
- -> XREF: D04 T11 §1 -- `OriginalGuard`, `OriginalWritePolicy`, `InPlaceWriter`, and every `Lumen.Originals.*` key, the one owner of the originals policy that §10 only renders and locks
- -> XREF: D04 T11 §4 -- batch convert, whose Replace originals destination the `Lumen.Originals.InPlace.Convert` key §10 renders enables
- -> XREF: D04 T09 §17 -- develop's Save to Original, enabled by the same `Save` key
- -> XREF: D04 T13 §1 -- the codec registry and `FormatMatrix` §7's Installed Codecs list reads, and the `Lumen.Formats.*` keys §4's File Handling page renders
- -> XREF: D04 T12 §5 -- print overlays that reuse §1's identity plate
- -> XREF: D06 T01 §3 -- the Lumen user guide that §7 links and every section extends
- -> XREF: D06 T02 §3 -- the published guide site §7 opens
- -> XREF: D04 T15 §10 -- Lumen 1.0.0, which follows this file

## Outcome

- Every Lumen mode sits in a customizable module picker with an identity plate, per-module keys and history, panel groups with solo mode, screen modes, and lights out, and every layout survives a restart.
- Toolbars, menus, favorites, docking panes, and saved `.lumenws` workspaces are customizable per mode on the shared frames, and the viewer and loupe answer touch.
- One conflict-free default keymap covers every command, with ACDSee and IrfanView key sets, an editor, the Ctrl+/ overlay, and a generated shortcuts page.
- One Options dialog, generated from `PreferenceKeyRegistry`, shows every registered key exactly once, with search and Reset Page.
- The File Handling page's Originals group renders `D04 T11 §1`'s four opt-ins (embed metadata into originals, rotate in place, save over the original, convert in place) and its backup settings, every opt-in off by default; with every opt-in off no original is ever opened for writing, an administrator can lock them all off, and no second policy, key, or writer exists.
- Lumen runs portably, accepts administrator deployment overlays, resets safely, and imports settings from earlier installations.
- Help, context help, Quick Start, languages, updates, system info, themes, high DPI, and external editors work as the three competitors' do.

**Adjacency:** list=applicable @ D04 T14 §2; document=not-applicable (the workspace, preferences, and help produce no document a user carries; exported settings packages are covered under exchange); settings=applicable @ D04 T14 §4; reporting=applicable @ D04 T14 §7; notifications=applicable @ D04 T14 §7; permissions=applicable @ D04 T14 §6; audit=applicable @ D04 T14 §4; exchange=applicable @ D04 T14 §6; reverse=applicable @ D04 T14 §10

**Adjacency rationale:** The managed lists are workspaces, toolbars, and favorite menus (§2), shortcut sets (§3), external editors (§9), and language packs (§7). This file is the settings surface: every page writes `Lumen.*` keys with defaults and a named consumer that `PreferencePagesTests` prove (§4, §5, §10). Reporting is System Info and the Installed Codecs list (§7). Notifications are update available (§7), settings imported, and reset done (§6). A read-only portable folder, a locked deployment key (§6), a missing editor (§9), and an originals opt-in locked off by the administrator (§10) are refused by name. One Serilog Information line per settings change is the audit trail (§4 and every page after it), and every change to an originals opt-in logs the key and whether it was locked (§10). Exchange is workspace, keymap, and settings export and import and migration from earlier installations (§2, §3, §6). The reverse is Reset Page and reset at launch (§4, §6), restoring the backup a settings import takes (§6), and restoring an original from the backup copy §10 takes before any in-place write.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Modes, the module picker, and panels | D04 T02 §8, D03 T20 §1 |  [ ]   |
|   2   |   §2    | Toolbars, menus, pane layout, saved workspaces, and touch | §1, D03 T20 §2, D03 T20 §6 |  [ ]   |
|   3   |   §3    | The keymap and shortcuts | §2, D03 T20 §3 |  [ ]   |
|   4   |   §4    | Preferences I: general, interface, file handling, and the viewer and browse pages | §1, D03 T20 §4 |  [ ]   |
|   5   |   §5    | Preferences II: performance, caches, color management, and display | §4 |  [ ]   |
|   6   |   §6    | Settings storage, portable mode, and migration | §4 |  [ ]   |
|   7   |   §10   | Originals: the opt-in write settings | §4, §6, D04 T11 §1, D04 T11 §4, D04 T11 §5, D04 T08 §9, D04 T04 §11, D04 T04 §16, D04 T09 §17 |  [ ]   |
|   8   |   §7    | Help, learning, languages, and updates | §1, D03 T20 §8, D05 T01 §4 |  [ ]   |
|   9   |   §8    | Themes and appearance | §1 |  [ ]   |
|  10   |   §9    | External editors | §4 |  [ ]   |

---

## 1. Modes, the Module Picker, and Panels

By Phase 39 Lumen has many modes (Library, Browse, Develop, Map, Book, Slideshow, Print, Web, People, Dashboard, and the viewer), and a photographer moves between tasks by key and hides everything but the photo when judging it. This section puts the modes in a customizable module picker with an identity plate, adds per-module key switching and history, panel groups with solo mode, auto hide, and swap, screen modes, and lights out, and maps ACDSee's modes onto Lumen's. It consumes the `Photon.UI/Workspace/` frame that `D03 T20 §1` moved and must not add a second panel host. Catalog: LP-1059 to LP-1065 (7 features: the module picker, the identity plate, panel groups, screen modes, lights out, module switching, and the ACDSee mode mapping). -> SOURCE: parity-lumen-modes

**Fidelity:** Lumen main window -- docs/captures/lumen/main-window/ (baseline from `D04 T01 §2`); new captures to docs/captures/lumen/workspace/.
**Job:** a photographer can move between tasks by key and hide everything but the photo when judging it. Consumer: the main window shell and every module's layout.
**Treatment:** Lightroom's module picker with an Identity Plate Editor, modules hidden by right-click, F5 to F8 panel toggles, Tab and Shift+Tab, solo mode, end marks, auto hide and show, F full-screen cycling, and L lights out with dim level and color. Cheaper substitute that fails the checkpoint: fixed tabs with no panel control.
**Chrome:** consume the `Photon.UI/Workspace/` frame of `D03 T20 §1` and the `D01 T01 §3` theme. Do not add a second panel host.
**Corrected 2026-09-27:** the specs are `docs/design/shell-layout.md` (Lumen's Library and Develop workspaces as title-bar tabs after the menus, the filmstrip on `frame`) and `docs/design/components/Panel/README.md`; selected thumbnails use a 2 px `state-line` outline and `state-subtle` fill, and `accent-lumen` is only on the Import button.

**Requires:** display-session -- the workspace, screen modes, and captures need an interactive desktop

- [ ] Add `src/Lumen/Photon.Lumen.Desktop/Workspace/ModuleRegistry.cs` registering every mode with its name, icon, default key, and ACDSee name. Done when: a test asserts every mode the parity files add is registered once.
- [ ] Add the module picker (LP-1059): show or hide the picker and individual modules by right-click, button style, condensed buttons, and icons, stored in `Lumen.Workspace.Modules`. Done when: `ModuleNavigatorTests` assert a hidden module is skipped and the state persists across restart.
- [ ] Add `IdentityPlate` in `src/Lumen/Photon.Lumen.Core/Settings/IdentityPlate.cs` (LP-1060): styled text or a graphic, with named presets, consumed by the picker and by the print, slideshow, and web overlays of `D04 T12 §5`, `D04 T12 §7`, and `D04 T12 §9`. Done when: a test round-trips a text plate and a graphic plate.
- [ ] Add the Identity Plate Editor dialog (LP-1060) with fonts and colors for the plate and the picker buttons. Done when: a driven edit updates the picker (capture). Cheaper substitute: a fixed app name.
- [ ] Add panel groups (LP-1061): left, right, top, and bottom groups with show or hide (F5 to F8), Tab and Shift+Tab, solo mode, end marks, auto hide and show, hide individual panels, and swap left and right. Done when: `PanelLayoutStateTests` assert solo mode and swap persist across restart.
- [ ] Add the screen modes (LP-1062): normal, full screen with menu bar, full screen, hide panels, and full-screen preview, cycled by F. Done when: a test asserts the cycle order and each mode's window state.
- [ ] Add lights out (LP-1063): L cycles dim, black out, and normal, with the dim level and color under `Lumen.Workspace.LightsOut.*`. Done when: a driven L cycle is captured at each stage.
- [ ] Add module switching (LP-1064): Ctrl+Alt+1 to 7 per module, back and forward through module history (Ctrl+Alt+Left and Right), and return to the previous module (Ctrl+Alt+Up). Done when: `ModuleNavigatorTests` assert history back and forward across four switches.
- [ ] Add the ACDSee mapping (LP-1065): Manage maps to Browse, View and Media to the viewer and library, Develop, and Dashboard, with a mode switcher listing each mode with its ACDSee name as a tooltip. Done when: a test asserts each ACDSee name resolves to its Lumen mode.
- [ ] Log one Serilog Information line per workspace setting change (module visibility, identity plate, lights-out level). Done when: a Serilog test logger asserts the line.
- [ ] Commit captures of each screen mode and lights-out stage under `docs/captures/lumen/workspace/` and write `docs/user/lumen/workspace.md` for modes and panels. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: modes, the module picker, identity plate, panels, and screen modes"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~ModuleNavigatorTests|FullyQualifiedName~PanelLayoutStateTests"` exits 0; captures of each screen mode and lights out are committed. Cheaper substitute that fails: panels that forget their state, which the persistence test catches.

## 2. Toolbars, Menus, Pane Layout, Saved Workspaces, and Touch

A user arranges Lumen for their screens and hands and gets it back next time. This section makes toolbars and menus customizable per mode (buttons, labels, tooltips with shortcuts, custom menus, up to 15 favorite commands, and a task pane), lets panes dock, float to a second monitor, stack as tabs, and auto hide, saves and resets workspaces per mode as `.lumenws` packages on the shared frame, remembers dialog and browser window positions, gives text fields spelling check and a special characters flyout, and makes the viewer and loupe answer touch and a tablet mode. It consumes the shared toolbar, menu, and docking frames and Imago's touch handling and must not add a second layout serializer. Catalog: LP-1066 to LP-1079 (14 features: toolbar customization, text field editing, the Workspaces and Panes menus, dockable panes, saved workspaces, touch in the viewer, the task pane, custom menus, the tablet mode dialog, color value copy and paste, dialog position memory, favorite menus, browser window position, and toolbar buttons with the zoom box). -> SOURCE: parity-lumen-workspace-layout

**Fidelity:** Lumen workspace -- docs/captures/lumen/workspace/.
**Job:** a user can arrange Lumen for their screens and hands and get it back next time. Consumer: the shell's toolbars, menus, and dock, and the viewer's input handling.
**Treatment:** a Customize Toolbar dialog, a Favorites menu, Window, Workspaces and Window, Panes menus, a docking compass, and a Tablet Mode dialog. Cheaper substitute that fails the checkpoint: saving only the window size.
**Chrome:** consume the `Photon.UI/Workspace/` toolbar, menu, and docking frames of `D03 T20 §1` and `D03 T20 §2`, and the touch handling of `D03 T20 §6`. Do not add a second layout serializer.
**Corrected 2026-09-27:** the specs are `docs/design/components/Menu/README.md`, `docs/design/components/ToolRail/README.md`, `docs/design/components/StatusBar/README.md`, and `docs/design/components/WindowChrome/README.md`.
**Corrected 2026-09-27:** menus, toolbars, docked and floating panes, and the title bar are drawn by `Photon.UI`'s implicit styles (`D01 T01 §6`), `PhotonWindow` (`D01 T01 §7`), and the Photon AvalonDock theme (`D01 T01 §8`); customization changes their content and layout, not their look.

**Requires:** display-session -- docking, a second monitor, and touch need an interactive desktop

- [ ] Register every Lumen toolbar item per module with the shared toolbar frame (LP-1066): show or hide toolbars, text labels, tooltips with shortcuts, and reset. Done when: `ToolbarCustomizationTests` add and remove a button in the Library toolbar and reset restores the default.
- [ ] Add the Customize Toolbar dialog (LP-1066, LP-1079): add or remove buttons, button position, and the zoom box on the viewer toolbar. Done when: a driven customization survives a restart (capture).
- [ ] Add custom menus and button appearance (LP-1073) through the shared menu frame. Done when: a test adds a custom menu with two commands and reads it back from the workspace.
- [ ] Add Favorites (LP-1077): up to 15 commands, added from any menu by right-click, removed, or cleared. Done when: `FavoritesMenuTests` refuse a 16th command with a message and round-trip the list.
- [ ] Add the task pane (LP-1072): context-sensitive common tasks for the current mode and selection. Done when: a test asserts the task list for Browse with one photo selected and for Develop.
- [ ] Add the Window, Panes menu (LP-1068) opening or closing any pane. Done when: a test asserts every registered pane has a menu entry.
- [ ] Add docking (LP-1069): the docking compass, float to a second monitor, stack as tabs, resize, auto hide, and return to the previous location. Done when: a driven float of a pane to a second monitor and back is captured.
- [ ] Add workspaces (LP-1070): save, load, default, and reset per mode, stored as the shared frame's package with the `.lumenws` extension. Done when: `LumenWorkspaceRoundTripTests` restore dock layout, toolbars, favorites, and menus from a saved `.lumenws`.
- [ ] Add window memory (LP-1076, LP-1078): dialogs and the browser window remember size and position per monitor configuration, falling back to centered when a monitor is gone. Done when: a test with two fake monitor layouts asserts each restored rectangle and the fallback.
- [ ] Add text field editing (LP-1067): cut, copy, paste, WPF `SpellCheck` with the Windows spelling languages, and a special characters flyout on caption and keyword fields. Done when: a test asserts `SpellCheck.IsEnabled` on the caption field and the flyout inserts a character.
- [ ] Add color value copy and paste (LP-1075) on every color control through the clipboard as hex. Done when: a test copies a color from one control and pastes it into another.
- [ ] Add touch in the viewer and loupe (LP-1071): swipe, hold and swipe, press and hold, double tap to switch mode, pinch zoom, and pan through `D03 T20 §6`'s manipulation handling. Done when: `TouchGestureMapTests` map manipulation deltas to zoom and pan and a swipe to next image.
- [ ] Add the Tablet Mode dialog (LP-1074) enlarging touch targets and turning on touch-friendly toolbars, stored as `Lumen.Workspace.TabletMode`. Done when: a test asserts the enlarged minimum target size with the key on.
- [ ] Log one Serilog Information line per workspace save, load, and reset. Done when: a Serilog test logger asserts the lines.
- [ ] Commit captures of the dialogs and a floated pane under `docs/captures/lumen/workspace/` and extend `docs/user/lumen/workspace.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: customizable toolbars and menus, docking, saved workspaces, and touch"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~ToolbarCustomizationTests|FullyQualifiedName~FavoritesMenuTests|FullyQualifiedName~LumenWorkspaceRoundTripTests|FullyQualifiedName~TouchGestureMapTests"` exits 0; a driven float of a pane to a second monitor and back is captured. Cheaper substitute that fails: fixed toolbars, which the customization test catches.

## 3. The Keymap and Shortcuts

A user coming from Lightroom, ACDSee, or IrfanView keeps their muscle memory and can change any key. Every parity section registered its commands' default keys; this section turns them into one default Lumen keymap (Lightroom's keys as the base), ships ACDSee and IrfanView alternative key sets, adds the shortcut editor per mode with conflict warnings and right-click reassignment, the Ctrl+/ overlay per module, and the library navigation, application, focus, and editing keys, and generates the user guide's shortcut page so it cannot drift. It consumes the shortcut-set frame `D03 T20 §3` moved to `Photon.UI/Workspace/`. Catalog: LP-1125 to LP-1129, LP-1216 to LP-1217 (7 features: the Ctrl+/ overlay, library navigation keys, the shortcut editor, application keys, focus and context-menu keys, and the next, previous, tag, reject, metadata, keyword, preset, and caption keys around the Edit in Imago hand-off). -> SOURCE: parity-lumen-keymap

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/keymap/.
**Job:** a user coming from Lightroom, ACDSee, or IrfanView can keep their muscle memory and change any key. Consumer: every command binding in both executables.
**Treatment:** Edit, Keyboard Shortcuts with mode categories, commands, current keys, assign with conflict warning, remove, reset all, and a key-set picker (Lumen, ACDSee keys, IrfanView keys); the Ctrl+/ overlay lists the current module's keys. Cheaper substitute that fails the checkpoint: a read-only shortcut list.
**Chrome:** consume the shortcut-set frame of `D03 T20 §3` and the shortcuts dialog of `D01 T01 §4`. Do not add a second key-binding store.

**Requires:** display-session -- the editor and overlay need an interactive desktop

- [ ] Add `src/Lumen/Photon.Lumen.Desktop/Workspace/Keymap/LumenKeymap.cs`: the default set generated from every command's registered default key. Done when: `KeymapConflictTests` assert no two commands in one scope share a key.
- [ ] Add `KeymapCoverageTests`: every command in the command registry has a default key or is listed in `UnboundCommands.txt` as unbound on purpose. Done when: the test fails on a command added without either and passes on the tree.
- [ ] Ship the alternative key sets `ACDSee keys` and `IrfanView keys` as shortcut-set files, unmapped commands falling back to the default set. Done when: `KeymapConflictTests` assert each alternative set is conflict-free after fallback.
- [ ] Add the shortcut editor (LP-1127): per-mode categories, commands, current keys, assign with a conflict warning naming the other command, remove, and reset all. Done when: a driven reassignment with a conflict warning is captured.
- [ ] Add right-click reassignment on any menu item (LP-1127), opening the editor at that command. Done when: a driven right-click on a menu item opens the editor with it selected.
- [ ] Add the Ctrl+/ overlay (LP-1125) listing the current module's keys, dismissed by any key. Done when: a test asserts the overlay lists exactly the current module's bindings.
- [ ] Bind the library navigation keys (LP-1126): next and previous photo, next in selection, beginning and end of grid, scroll thumbnails, and scroll a zoomed photo. Done when: a test asserts each key reaches its command in the grid and loupe.
- [ ] Bind the application keys (LP-1128): close Lumen, close the current image, and close all images. Done when: a test asserts each binding.
- [ ] Bind the focus and context-menu keys (LP-1129): Tab and Shift+Tab through panes, Shift+F10 and the Menu key for context menus in browse and the viewer. Done when: a test asserts focus moves pane to pane in order and Shift+F10 opens the context menu.
- [ ] Bind the filmstrip, tag, reject, metadata, keyword, preset, and caption keys around the Edit in Imago hand-off (LP-1216, LP-1217) so they work while Imago holds a photo. Done when: a test asserts next, previous, first, last, tag, and reject act on the filmstrip during a pending hand-off.
- [ ] Round-trip shortcut sets through export and import. Done when: `ShortcutSetRoundTripTests` pass.
- [ ] Generate `docs/user/lumen/keyboard-shortcuts.md` from the default keymap with a generator test comparing the committed page. Done when: the test fails when a binding changes without regenerating.
- [ ] Log one Serilog Information line per key reassignment and key-set switch. Done when: a Serilog test logger asserts the lines.
- [ ] Commit captures of the editor and overlay under `docs/captures/lumen/keymap/`. Done when: both are captured.
- [ ] Commit: `"lumen: the default keymap, alternative key sets, the editor, and the overlay"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~KeymapConflictTests|FullyQualifiedName~KeymapCoverageTests|FullyQualifiedName~ShortcutSetRoundTripTests"` exits 0 and the generated shortcuts page matches the committed one; a driven reassignment with a conflict warning is captured. Cheaper substitute that fails: a hand-typed shortcut page, which the generator comparison catches.

## 4. Preferences I: General, Interface, File Handling, and the Viewer and Browse Pages

A user finds and changes any behavior in one place and can undo a bad change by resetting a page. Every parity section registered its keys in `PreferenceKeyRegistry`; this section builds Lumen's Options dialog generated from that registry (so no page duplicates a key defined elsewhere) with search and Reset Page, and adds the General, Interface, File Handling, Viewer, and Browse pages: startup and catalog at launch, prompts, completion sounds, interface tweaks, date and time format, the network proxy, the error reporting opt-out, dialog profiles, and browse and file list behavior. The File Handling page hosts §10's Originals group. Catalog: LP-0472, LP-1096 to LP-1109 (15 features: the import completion sound, startup, interface tweaks, completion sounds with system settings, prompts reset, remember last selection per source, the network proxy, the Options dialog, date and time format, browse window options, error reporting opt-out, file list behavior, hiding common folders, dialog profiles, and the viewer start folder). -> SOURCE: parity-lumen-preferences-general

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/preferences/.
**Job:** a user can find and change any behavior in one place and undo a bad change by resetting a page. Consumer: each key's registered consumer (the shell, the viewer, browse, import, export, the AI client, the map tiles, and the update check).
**Treatment:** an Options dialog with a page tree (General, Interface, File Handling, Viewer, Browse, Performance, Color, External Editing), a search box, and Reset Page; each page lists the keys other sections registered. Cheaper substitute that fails the checkpoint: a raw JSON file.
**Chrome:** consume `PreferenceKeyRegistry` and `WarningRegistry` of `D03 T20 §4` and the settings store of `D01 T02 §2`. Pages for keys defined elsewhere are generated from the registry, never duplicated.

**Requires:** display-session -- the Options dialog and captures need an interactive desktop

- [ ] Add `src/Lumen/Photon.Lumen.Desktop/Preferences/OptionsDialog.xaml` (LP-1102) generated from `PreferenceKeyRegistry`, with the page tree, a search box filtering controls by label and key, and Reset Page. Done when: `PreferencePagesTests` assert every registered `Lumen.*` key appears on exactly one page. Cheaper substitute: a hand-built page missing registered keys.
- [ ] Generate `docs/dev/lumen/preference-keys.md` from the registry with a test comparing the committed page. Done when: the test fails when a key changes without regenerating.
- [ ] Add the startup settings (LP-1096): splash, default catalog at launch (most recent, prompt, specific), and the catalog chooser when Ctrl is held at launch. Done when: a test asserts the chooser opens with Ctrl held and the configured catalog opens otherwise.
- [ ] Add the prompts settings (LP-1099, LP-1100): Reset All Warning Dialogs through `WarningRegistry`, and remember the last selection per source for the session. Done when: a test suppresses two warnings, resets, and asserts both show again.
- [ ] Add completion sounds (LP-0472, LP-1098) for import, watched-folder import, and export, mapped to Windows sound events registered under `HKCU\AppEvents\Schemes\Apps\Lumen` so the system Sounds settings govern them. Done when: a test asserts each event name is raised by its job.
- [ ] Add the interface tweaks (LP-1097): zoom clicked point to center, font smoothing, and Auto Sync notifications; and the date and time output format, system or custom (LP-1103). Done when: a test asserts a custom format reaches the metadata panel's date rendering.
- [ ] Add the network proxy (LP-1101): system, none, or manual host and port with optional credentials stored with DPAPI, used by the AI client, map tiles, uploads, and the update check through one `HttpClient` handler factory. Done when: `ProxySettingsTests` assert each consumer's handler uses the manual proxy.
- [ ] Add the error reporting opt-out (LP-1105): no crash data leaves the machine unless the user sends a report, stated on the page. Done when: a test asserts no network client is created by the crash handler with the key at its default.
- [ ] Add dialog profiles (LP-1108): named sets of dialog settings saved and loaded; and hide common folders in open and save dialogs (LP-1107). Done when: a test round-trips a dialog profile and asserts the hidden folders in the file dialog options.
- [ ] Add the Viewer page (LP-1109): the viewer start folder (last, fixed, or the file's folder) and the viewer title bar path, reading the viewer's keys from the registry. Done when: a test asserts the viewer opens in the fixed start folder.
- [ ] Add the Browse page (LP-1104, LP-1106): title bar path and catalog name, folder tree density and expanders, clear path history on exit, overlay on excluded folders, Ctrl hot tracking, animations, image-type highlighting, auto scroll while building, and the Esc warning. Done when: the coverage test names each key's browse consumer.
- [ ] Add the File Handling page hosting §10's Originals group and the file-type and sidecar keys other sections registered. Done when: the coverage test lists the File Handling keys and the Originals group placeholder shows "Every original stays unchanged" until §10 ships its controls.
- [ ] Log one Serilog Information line per preference change naming the key and new value. Done when: a Serilog test logger asserts the line.
- [ ] Commit captures of every page under `docs/captures/lumen/preferences/` and write `docs/user/lumen/preferences.md`. Done when: every control is captured and documented with its default.
- [ ] Commit: `"lumen: the Options dialog with general, interface, viewer, and browse pages"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~PreferencePagesTests|FullyQualifiedName~ProxySettingsTests|FullyQualifiedName~ResetPageTests"` exits 0, with every registered key on exactly one page; captures of each page are committed. Cheaper substitute that fails: a hand-built page missing registered keys, which `PreferencePagesTests` catches.

## 5. Preferences II: Performance, Caches, Color Management, and Display

A user trades speed for disk and sees accurate color on their monitor. This section adds the Performance and Color pages to §4's dialog: display color management through `D01 T04 §1` (monitor profile, default input profile for untagged images, managed thumbnails, profile details), GPU preferences and adapter selection (the GPU develop path itself stays backlog B-033 and the page says so), the develop and preview cache location, size, and purge, parallel preview generation and HDR display in the library, and a warning when the display is not true color. Catalog: LP-1110 to LP-1115 (6 features: display color management, the GPU preference, the develop cache, preview generation, GPU selection, and the true color warning). -> SOURCE: parity-lumen-preferences-performance

**Fidelity:** Options dialog -- docs/captures/lumen/preferences/.
**Job:** a user can trade speed for disk and see accurate color on their monitor. Consumer: the display transform, the preview cache of `D04 T01 §7`, the develop cache, and the preview generator.
**Treatment:** Performance and Color pages in §4's dialog with a cache usage bar and a Purge button, and a profile details readout. Cheaper substitute that fails the checkpoint: a GPU on/off switch that changes nothing.
**Chrome:** consume `D01 T04 §1` for display transforms, the preview cache of `D04 T01 §7`, the develop cache, and the HDR display path of `D03 T15 §4`. Do not add a second color engine.

**Requires:** display-session -- the display profile readout and purge need an interactive desktop

- [ ] Add the display color settings (LP-1110): the monitor profile per display read through `D01 T04 §1` (`WcsGetDefaultColorProfile`), the engine name, the default input profile for untagged images, the managed thumbnails toggle, and a profile details readout. Done when: `DisplayProfileSelectionTests` assert the per-display profile and the untagged default reach the display transform.
- [ ] Refresh the display transform when a window moves to another monitor. Done when: a test with two fake monitors asserts the transform changes with the window.
- [ ] Add the GPU preference (LP-1111): auto, custom, or off for display and preview work, and GPU preview generation, with a line stating the develop engine stays on the CPU until B-033 is promoted. Done when: a test asserts the preview generator reads the key and the page text names B-033. Cheaper substitute: a switch that changes nothing, which the consumer test catches.
- [ ] Add adapter selection (LP-1114): automatic or a named adapter from DXGI enumeration. Done when: a test with a fake adapter list asserts the chosen adapter reaches the preview generator.
- [ ] Add the develop cache page (LP-1112): location, maximum size, current usage, and Purge. Done when: `CachePurgeTests` assert purge frees the stated bytes and leaves the catalog intact.
- [ ] Add the preview cache size and purge for `D04 T01 §7`'s cache on the same page. Done when: `CachePurgeTests` cover the preview cache.
- [ ] Refuse a cache location on a read-only or missing drive by name and keep the old location. Done when: a test asserts the message.
- [ ] Add preview settings (LP-1113): parallel preview generation count, HDR display in the library through `D03 T15 §4`'s HDR display path, and hover previews for presets, history, and snapshots. Done when: a test asserts the generator's degree of parallelism follows the key.
- [ ] Add the true color warning (LP-1115) when the display reports under 24 bits per pixel. Done when: a test with a fake 16-bit display asserts the warning once per session.
- [ ] Log one Serilog Information line per cache purge (bytes freed) and per performance setting change. Done when: a Serilog test logger asserts the purge line.
- [ ] Commit captures of the Performance and Color pages under `docs/captures/lumen/preferences/` and extend `docs/user/lumen/preferences.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: performance, cache, color management, and display preferences"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~DisplayProfileSelectionTests|FullyQualifiedName~CachePurgeTests"` exits 0; a driven purge is captured with its log line quoted. Cheaper substitute that fails: an unmanaged preview, which the display profile test catches.

## 6. Settings Storage, Portable Mode, and Migration

A user carries Lumen and its settings between machines, and an administrator deploys it with locked defaults. This section extends the settings store of `D01 T02 §2` with a portable root and a deployment overlay: portable mode from a folder or USB stick with everything under `.\Data\`, a settings package to copy to another PC, a read-only freeze, presets optionally stored with the catalog, reset at launch or on demand with a backup first, migration from an earlier installation, a machine-wide `deployment.json` with locked keys, and the documented installer switches of `D05 T01`. Catalog: LP-0425, LP-1116 to LP-1123 (9 features: presets stored with the catalog, reset to defaults, import settings from a previous installation, import presets from a previous installation, first-run and on-demand import, installer options, portable mode, the settings file, and deployment settings). -> SOURCE: parity-lumen-settings-storage

**Fidelity:** Options dialog -- docs/captures/lumen/preferences/.
**Job:** a user can carry Lumen and its settings between machines, and an administrator can deploy it with locked defaults. Consumer: the settings store, the log and cache paths, and every page that shows a locked key.
**Treatment:** a Settings page showing the settings folder with Copy, Export, Import, Reset, and Freeze, and a first-run Import Settings prompt when an earlier installation is found. Cheaper substitute that fails the checkpoint: settings only in the registry.
**Chrome:** extend the settings store of `D01 T02 §2` with a portable root and a deployment overlay; installer switches live in `D05 T01 §1`. Do not add a second settings writer.

**Requires:** display-session -- the import prompt and the portable run need an interactive desktop

- [ ] Add `src/Lumen/Photon.Lumen.Core/Settings/LumenDataRoot.cs` (LP-1121): a `Lumen.portable` marker beside `Lumen.exe` and `LumenViewer.exe` moves the settings store, logs, caches, and default catalog under `.\Data\`; otherwise `%LOCALAPPDATA%\Rizonesoft\Lumen\`. Done when: `PortableModeTests` assert every write lands under `.\Data\` with the marker present.
- [ ] Refuse a read-only portable medium by name with an offer to use `%LOCALAPPDATA%` for this session. Done when: a test with a read-only folder asserts the message and the fallback.
- [ ] Add the Settings page (LP-1122): the settings folder shown, Copy to another PC as one `.lumensettings` package, Export, Import, and a read-only Freeze that makes the store refuse writes. Done when: a test round-trips a package and asserts a frozen store refuses a write with its message.
- [ ] Take a backup of the settings folder before every import, and offer Restore Previous Settings after an import. Done when: `SettingsImportTests` import, restore, and assert the original values are back.
- [ ] Add presets stored with the catalog (LP-0425): develop, export, and metadata presets optionally in the catalog folder so a catalog moves with them. Done when: a test moves a catalog folder and asserts its presets load.
- [ ] Add reset (LP-1116) at launch by holding Ctrl+Shift, or from the page, taking a backup first. Done when: `SettingsResetTests` assert the defaults and the backup's presence.
- [ ] Add migration (LP-1117, LP-1118, LP-1119): on first run when an earlier installation's folder is found, and on demand, import settings, metadata views and presets, label, category, and keyword sets, search presets and history, new image presets, develop, export, batch, rename, and resize presets, shortcut sets, and external editors. Done when: `SettingsMigrationTests` import each set from a fixture of an earlier installation.
- [ ] Add the administrator deployment overlay (LP-1123): a machine-wide `%ProgramData%\Rizonesoft\Lumen\deployment.json` redirecting the settings folder, setting the default language, locking the toolbar, disabling delete, forcing browsing mode, restricting save formats, suppressing prompts, and locking §10's originals opt-ins off. Done when: `DeploymentOverlayTests` assert locked keys refuse writes and show read-only with a tooltip naming the administrator policy.
- [ ] Store settings as UTF-8 JSON and refuse an unparseable file by name, starting with defaults and keeping the bad file as `settings.json.bad`. Done when: a test with a corrupt file asserts the message and the kept copy.
- [ ] Document the installer switches (LP-1120) of `D05 T01 §1`'s Inno Setup installer (silent install, folder, shortcuts, file associations, settings folder, silent uninstall, desktop link with hotkey) in `docs/user/lumen/deployment.md`. Done when: every switch in `installer/Lumen.iss` appears in the page.
- [ ] Log one Serilog Information line per import, export, reset, freeze, and migration. Done when: a Serilog test logger asserts each line.
- [ ] Commit captures of the Settings page and the first-run import prompt under `docs/captures/lumen/preferences/` and extend `docs/user/lumen/preferences.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: portable mode, deployment settings, reset, and migration"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~PortableModeTests|FullyQualifiedName~DeploymentOverlayTests|FullyQualifiedName~SettingsMigrationTests|FullyQualifiedName~SettingsResetTests|FullyQualifiedName~SettingsImportTests"` exits 0; the portable ZIP run from a USB-like folder writes nothing under `%LOCALAPPDATA%` (a before-and-after listing quoted). Cheaper substitute that fails: a portable flag that still writes logs to `%LOCALAPPDATA%`, which the listing catches.

## 7. Help, Learning, Languages, and Updates

A new user gets going in a minute and a stuck user finds help or reports a problem with the facts attached. This section adds the Help menu (user guide, F1 context help, bundled readme files, community, feedback, and support links), a first-run Quick Start (start folder, folders to index, backup reminder), on-the-fly interface language switching from language packs with a translation kit, the suite's opt-in update check, System Info and the Installed Codecs list, and the platform page. It consumes the help plumbing and `SystemInfoReport` of `D03 T20 §8`, the language switching of `D03 T20 §9`, the update check of `D05 T01 §4`, and the About dialog of `D04 T01 §2`. Catalog: LP-1132 to LP-1140 (9 features: check for updates, system info, help and support links, the interface language, the first-run quick start, context help, the platform statement, the help file and readme files, and the installed codecs list). -> SOURCE: parity-lumen-help

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/help/.
**Job:** a new user can get going in a minute and a stuck user can find help or report a problem with the facts attached. Consumer: the help viewer and browser, the indexer (Quick Start), and the resource lookups (language).
**Treatment:** a Help menu (User Guide, Context Help F1, Keyboard Shortcuts, What's New, Check for Updates, System Info, Installed Codecs, About), a Quick Start dialog on first run, and a Language page. Cheaper substitute that fails the checkpoint: a Help menu that opens the project home page only.
**Chrome:** consume `SystemInfoReport` and the help plumbing of `D03 T20 §8`, the language switching of `D03 T20 §9`, the `UpdateChecker` of `D05 T01 §4`, and the About dialog of `D04 T01 §2`. Do not add a second diagnostics report.

**Requires:** display-session -- the help surfaces and captures need an interactive desktop

- [ ] Add the Help menu (LP-1134, LP-1139): User Guide opening `docs/user/lumen/` pages as published by `D06 T02 §3` (or the bundled copy offline), bundled readme files, and project community (GitHub Discussions), feedback (GitHub Issues), and support links. Done when: a test asserts each menu entry's target and that the bundled guide opens with the network disabled.
- [ ] Add `src/Lumen/Photon.Lumen.Desktop/Help/HelpTopicMap.cs` (LP-1137): F1 maps the focused surface to its user-guide page. Done when: `HelpTopicMapTests` assert every mapped page exists under `docs/user/lumen/` and every registered module and dialog has a topic. Cheaper substitute: F1 opening the guide's front page.
- [ ] Add the Quick Start dialog (LP-1136) on first run: start folder, folders to index (feeding `D04 T05 §2`), catalog backup reminder interval, and show at startup. Done when: a test asserts the chosen folders reach the indexer's locations and the dialog stays hidden when unticked.
- [ ] Add the Language page (LP-1135): on-the-fly switch through `D03 T20 §9`'s mechanism over the `.resx` resources that `D04 T02 §9` extracts, with language packs as satellite assemblies. Done when: `LanguageSwitchTests` switch to the pseudo-locale and assert open windows update without restart.
- [ ] Write the translation kit guide `docs/dev/lumen/translation.md` (the neutral `.resx` files, the satellite build, and a README). Done when: the guide builds a sample satellite assembly from the steps (output quoted).
- [ ] Add Check for Updates (LP-1132) consuming `D05 T01 §4`'s `UpdateChecker`, opt-in, with nothing sent without the user's action; Lumen raises an in-app notification to notify the user when a newer release exists. Done when: a test with a fake feed asserts no request by default and one notification with a newer version.
- [ ] Add System Info (LP-1133) on `SystemInfoReport`: version, OS, GPU, cache sizes, catalog size and path, copyable to the clipboard. Done when: a test with fakes asserts every field in the copied text.
- [ ] Add the Installed Codecs list (LP-1140): every `Photon.Core/Formats/` codec with its native library version, copyable. Done when: `InstalledCodecsReportTests` assert every registered codec appears with a version.
- [ ] Add the platform statement (LP-1138) to About and the user guide: 64-bit x64 and ARM64 (`D05 T01 §3`), the supported Windows range, Unicode paths throughout, and a Store edition recorded as not planned. Done when: a test asserts About shows the process architecture and the guide page states each line.
- [ ] Add What's New from the bundled changelog, shown once after an update. Done when: a test asserts it shows once per version and reopens from Help.
- [ ] Log one Serilog Information line per update check and per language switch. Done when: a Serilog test logger asserts both lines.
- [ ] Commit captures of the Help menu, Quick Start, System Info, and a language switch under `docs/captures/lumen/help/` and write `docs/user/lumen/help.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: help, quick start, languages, updates, and system info"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~HelpTopicMapTests|FullyQualifiedName~InstalledCodecsReportTests|FullyQualifiedName~LanguageSwitchTests"` exits 0; captures of Quick Start, System Info, and a language switch are committed. Cheaper substitute that fails: an F1 key that opens the guide's front page, which `HelpTopicMapTests` catches.

## 8. Themes and Appearance

A user sets Lumen to match their eyes and screen. This section makes both executables follow the suite theme with dark, light, and follow-Windows modes switched live, adds a main window background fill and panel font size as theme overrides, per-monitor v2 high-DPI rendering, and toolbar button sizes and icon sets from the Photon icon catalog standing in for IrfanView skins (no third-party skin art ships and IrfanView skin files are not read). No Lumen view may hardcode a color. Catalog: LP-1080 to LP-1083, LP-1124 (5 features: background fill and panel font size, the display theme and dark mode, high DPI rendering, toolbar skins and button size, and the display theme choice). -> SOURCE: parity-lumen-appearance

**Fidelity:** Lumen main window -- docs/captures/lumen/main-window/.
**Job:** a user can set Lumen to match their eyes and screen. Consumer: the suite theme dictionaries and the icon catalog in both executables.
**Treatment:** an Appearance page with theme (dark, light, follow Windows), background fill, panel font size, toolbar button size, and icon set. Cheaper substitute that fails the checkpoint: hard-coded colors per window.
**Chrome:** consume the suite theme resources of `D01 T01 §3`, `ThemeService` in `Photon.UI/Themes/`, and the icon catalog. No surface hardcodes a color.
**Corrected 2026-09-27:** the suite has four brightness themes (Darkest, Dark, Medium Gray, Light), a Highlight color choice (Blue, Photon orange, Windows accent), and two densities, all from `D01 T01 §3`, not dark and light only; follow Windows picks Dark or Light. Icon sets are sizes and stroke weights of the one Lucide catalog (`docs/design/components/Icons/README.md`), never a second family.

**Requires:** display-session -- theme captures at several DPI settings need an interactive desktop

- [ ] Add the theme choice (LP-1081, LP-1124): Darkest, Dark, Medium Gray, Light, and follow Windows through `UISettings.ColorValuesChanged`, plus the Highlight color and density choices of `D01 T01 §3` (**Corrected 2026-09-27:** said dark, light, and follow Windows), switching live in `Lumen.exe` and `LumenViewer.exe` through the suite theme dictionaries. Done when: `ThemeSwitchTests` assert both executables' resources change without restart.
- [ ] Add background fill and panel font size (LP-1080) as theme overrides stored in `Lumen.Appearance.*`. Done when: a test asserts the override brush and font size reach the main window.
- [ ] Declare per-monitor v2 DPI awareness in both executables' manifests (LP-1082). Done when: a test reads both manifests and finds `PerMonitorV2`.
- [ ] Add toolbar button size and icon sets from the Photon icon catalog (LP-1083); IrfanView skin files are not read and no third-party art ships, which the page states. Done when: a test renders one icon in each set at 200 percent without raster scaling.
- [ ] Add `ThemeResourceAuditTests`: a XAML scan of `src/Lumen/` finds no literal color outside the theme dictionaries. Done when: the test fails on a planted literal and passes on the tree. Cheaper substitute: a dark theme applied to the main window only.
- [ ] Log one Serilog Information line per appearance change. Done when: a Serilog test logger asserts the line.
- [ ] Commit captures at 100, 150, and 200 percent in both themes under `docs/captures/lumen/main-window/` and write `docs/user/lumen/appearance.md`. Done when: the six captures exist and every control is documented.
- [ ] Commit: `"lumen: themes, background, font size, high DPI, and icon sizes"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~ThemeResourceAuditTests|FullyQualifiedName~ThemeSwitchTests"` exits 0; captures at three DPI settings in both themes are committed. Cheaper substitute that fails: a dark theme applied to the main window only, which the XAML audit catches.

## 9. External Editors

A photographer finishes a photo in whatever editor they own and sees the result back in the library. This section extends `D04 T02 §7`'s `EditInService` (render, launch, watch, stack) to up to ten additional editors with per-extension defaults and a default editor on Ctrl+Alt+X, per-editor copy presets, a choice of editing a copy with Lumen adjustments, a copy of the original, or the original non-raw file, HDR hand-off, and the round trip back into the catalog; Edit in Imago gains layers and a linked raw document. "Edit Original" launches the editor on the original's path, where the editor, not Lumen, may write it; Lumen itself never opens the original for writing. It must not write a second hand-off service. Catalog: LP-1084 to LP-1091 (8 features: additional external editors with copy options, the edit choices, Edit in Imago as layers or a linked raw document, HDR hand-off, presets and naming with stacking and round trip, the Editors menu, the default external editor, and the external editor configuration). -> SOURCE: parity-lumen-external-editors

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/external-editors/.
**Job:** a photographer can finish a photo in whatever editor they own and see the result back in the library. Consumer: the external editors (through files) and the catalog.
**Treatment:** an External Editing page (editor list with add, edit, remove, default, per-extension mapping, and presets) and a Photo, Edit In submenu with Imago first and the configured editors after. Cheaper substitute that fails the checkpoint: Open With passing the original path only.
**Chrome:** extend `D04 T02 §7`'s `EditInService` and consume `D02 T15 §11`'s `SuiteAppLocator` for Imago. Do not write a second hand-off service.

**Requires:** display-session -- launching an external editor needs an interactive desktop

**Freeze check:** During every edit flow, including "Edit Original", Lumen opens no handle for write on the original: copies are rendered or copied through `AtomicFileWriter` to new paths, and "Edit Original" only passes the path to the external process after a first-use confirmation; `EditOriginalGuardTests` hook the file-open path and assert no write access was requested on any original. Fixture source: `tests/fixtures/lumen/import/`.

- [ ] Add `src/Lumen/Photon.Lumen.Core/Editing/ExternalEditorRegistry.cs` (LP-1089, LP-1091): up to ten editors with name, executable, arguments, per-extension defaults, short paths, and all selected files in one call. Done when: `ExternalEditorRegistryTests` refuse an 11th editor by name and round-trip the list.
- [ ] Refuse a missing editor executable by name at launch and offer to edit the entry. Done when: a test with a deleted executable asserts the message.
- [ ] Add the copy presets (LP-1084, LP-1088): TIFF, PSD, or PSB, color space, bit depth, resolution, compression, file naming with tokens, and stack with original. Done when: `EditCopyPresetTests` assert each preset's output format, depth, and profile.
- [ ] Add the edit choices (LP-1085): a copy with Lumen adjustments, a copy of the original, or the original non-raw file, with "Edit Original" behind a first-use explanation that the editor, not Lumen, may change the file. Done when: `EditOriginalGuardTests` pass. Cheaper substitute: passing the original path for every edit, which `EditCopyPresetTests` catches.
- [ ] Add the HDR hand-off (LP-1087): Rec. 2020 PQ or linear scene-referred 32-bit TIFF for HDR photos. Done when: a test reads back the 32-bit float TIFF's profile and sample format.
- [ ] Add the default editor on Ctrl+Alt+X (LP-1090) and the Editors menu with shortcuts and toolbar buttons (LP-1089). Done when: a test asserts Ctrl+Alt+X launches the default editor with the fake launcher.
- [ ] Add Edit in Imago as layers (LP-1086): several photos rendered and passed to Imago's open-as-layers command line; until an Imago entry point accepts that, one TIFF per photo is passed and the menu item's tooltip says so. Done when: a test asserts the command line for three photos in each mode.
- [ ] Add Edit in Imago as a linked raw document (LP-1086): the raw file with its develop settings as XMP for Imago's Develop studio. Done when: a test asserts the XMP beside the hand-off copy carries the develop settings.
- [ ] Refresh the stacked copy when the editor saves, through the `D04 T02 §7` watcher. Done when: a driven edit in a second editor (Paint.NET or GIMP, version quoted) refreshes the stacked copy (capture).
- [ ] Add the External Editing page on §4's dialog. Done when: the §4 coverage test lists the external-editor keys.
- [ ] Log one Serilog Information line per external edit (editor, choice, path of the copy). Done when: a Serilog test logger asserts the line.
- [ ] Commit captures under `docs/captures/lumen/external-editors/` and write `docs/user/lumen/external-editors.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: external editors with presets, round trip, and stacking"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~ExternalEditorRegistryTests|FullyQualifiedName~EditCopyPresetTests|FullyQualifiedName~EditOriginalGuardTests"` exits 0; a driven edit in a second editor refreshes the stacked copy (capture, editor version quoted). Cheaper substitute that fails: passing the original path for every edit, which `EditCopyPresetTests` catches.

## 10. Originals: The Opt-In Write Settings

The operator decided on 2026-09-27: "Safe by default, opt-in writes". Lumen writes the catalog, sidecars, and new files by default, but IrfanView, ACDSee, and Lightroom users expect to embed metadata into their JPEGs, rotate JPEGs in place, save over an edited file, and convert in place, and those opt-ins need one place a user finds them and an administrator can lock them. The policy itself is not built here: `D04 T11 §1` owns `OriginalGuard`, `OriginalWritePolicy`, `InPlaceWriter`, and every `Lumen.Originals.*` key (`Lumen.Originals.InPlace.EmbedMetadata`, `.Rotate`, `.Save`, and `.Convert`, all off by default, `Lumen.Originals.BackupBeforeInPlace`, `Lumen.Originals.BackupFolder`, and `Lumen.Originals.BackupRetentionDays`), metadata reaches an original only through `D04 T08 §9`'s metadata-only rewriters (never a re-encode), and the commands each key enables belong to their sections (the viewer's Save in `D04 T04 §11`, lossless rotation in `D04 T04 §16` on `D04 T11 §5`'s `LosslessJpegTransform`, batch convert's Replace originals in `D04 T11 §4`, and develop's Save to Original in `D04 T09 §17`). This section is only the Originals group on §4's File Handling page over those keys, with the confirmations, the status line, and the lock-off through §6's deployment overlay. It must not add a second policy, key, backup copier, or writer. Catalog: none of its own (the in-place variants' catalog rows stay with their owning sections). -> SOURCE: operator-lumen-originals-opt-in

**Corrected 2026-09-27:** at authoring this section defined a second policy (`Lumen.Originals.EmbedMetadata`, `RotateInPlace`, `SaveInPlace`, `Backup.*`) and its own `OriginalFileWriter`, duplicating `D04 T11 §1`, and routed embedding through `ExportMetadataEmbedder`, which re-encodes. The Lumen integration made `D04 T11 §1` the single owner of the originals policy, moved backup retention there as `Lumen.Originals.BackupRetentionDays`, routed embedding through `D04 T08 §9`, and reduced this section to the preferences group and the administrator lock.

**Fidelity:** Options dialog, File Handling page -- docs/captures/lumen/preferences/; new captures to docs/captures/lumen/originals/.
**Job:** a user who wants their originals updated opts in one kind of write at a time from one page, knowing a verified backup is taken first by default; a user who does nothing never has an original written; an administrator can guarantee nobody opts in. Consumer: `D04 T11 §1`'s `OriginalWritePolicy`, read by the commands of `D04 T04 §11`, `D04 T04 §16`, `D04 T08 §9`, `D04 T09 §17`, and `D04 T11 §4`.
**Treatment:** an Originals group with four checkboxes, all unticked by default: "Embed metadata into original files (JPEG, TIFF, PNG, DNG)", "Rotate JPEG files in place (lossless)", "Allow Save to overwrite the original file", and "Allow batch convert to replace originals"; each ticked box opens a confirmation naming what will be written and that a backup copy is taken first; below them "Keep a verified backup copy before writing an original" (ticked) with the backup folder, a Browse button, and a retention period, where unticking it while an opt-in is on asks for a second confirmation saying such writes cannot be undone; a status line reading "Lumen never changes your original files" while every opt-in is off; and read-only controls with an administrator tooltip when the deployment overlay locks them. Cheaper substitute that fails the checkpoint: one global "allow writing originals" switch, or a page that stores its own keys.
**Chrome:** consume §4's generated page, `PreferenceKeyRegistry`, and `WarningRegistry` (`D03 T20 §4`), §6's deployment overlay, and `D04 T11 §1`'s `OriginalWritePolicy` and restore journal. Do not add a second policy, key, backup copier, or writer for original files.

**Requires:** display-session -- the Originals group, its confirmations, and the captures need an interactive desktop

**Freeze check:** With every `Lumen.Originals.InPlace.*` opt-in at its default (off), the unchanged-originals test of `D04 T02 §1` passes over a session that opens this page, saves metadata, rotates, saves from the viewer, and batch converts; this page writes only settings through the settings store and never constructs `InPlaceWriter`; a key locked off by §6's overlay reads `false` in `OriginalWritePolicy` whatever the stored value, so no command can write an original. Fixture source: `tests/fixtures/lumen/batch/` (from `D04 T11 §1`).

- [ ] Add the Originals group to §4's File Handling page in `src/Lumen/Photon.Lumen.Desktop/Preferences/OriginalsGroupView.xaml`, generated from the `PreferenceKeyRegistry` entries `D04 T11 §1` registered, replacing §4's placeholder: the four opt-in checkboxes bound to `Lumen.Originals.InPlace.EmbedMetadata`, `.Rotate`, `.Save`, and `.Convert`. Done when: `PreferencePagesTests` list the four keys under File Handling, Originals, and a capture shows every box unticked by default. Cheaper substitute: a hand-built page with its own key strings.
- [ ] Add the backup controls bound to `Lumen.Originals.BackupBeforeInPlace`, `Lumen.Originals.BackupFolder` (with Browse and a writable-folder check), and `Lumen.Originals.BackupRetentionDays`. Done when: `OriginalsGroupViewModelTests` assert each binding and that an unwritable folder is refused by name without changing the stored value.
- [ ] Show a confirmation through `WarningRegistry` when a box is ticked, naming the kind of write, the file types (for embedding, the formats `D04 T08 §9`'s `EmbedCapability` lists as writable), the backup folder, and the commands the key enables; Cancel leaves the key off, and the confirmation is never suppressible. Done when: `OriginalsGroupViewModelTests.Confirmations` assert each key's text and that Cancel stores nothing.
- [ ] Ask a second confirmation when backup is unticked while any opt-in is on ("In-place writes will not be undoable"), and restore the tick on Cancel. Done when: a test asserts the prompt and that Cancel keeps `BackupBeforeInPlace` true.
- [ ] Add the status line: "Lumen never changes your original files" while every opt-in is off, otherwise the enabled kinds and the backup folder. Done when: a test asserts both texts.
- [ ] Add Open Backup Folder and Restore Originals from Backup, which lists `D04 T11 §1`'s journaled in-place writes and restores the selected ones through that journal. Done when: a test with two journaled writes lists both and restoring one rereads its pre-write bytes.
- [ ] Render §6's deployment-overlay lock of the originals opt-ins (all four at once or per key): a locked key shows read-only with the tooltip naming the administrator policy, and `OriginalWritePolicy` reads the key through the overlay so a locked key is `false` even when the stored value is `true`. Done when: `DeploymentOverlayTests.OriginalsLocked` store `true`, lock the key, and assert the policy refuses the kind and `D04 T11 §1`'s first-use confirmation never appears.
- [ ] Add `OriginalsSettingsOwnerTests`: every `Lumen.Originals.*` key in `PreferenceKeyRegistry` is registered by `D04 T11 §1`'s `OriginalWritePolicy` and names its consumer commands, none by this page, and `grep -rn "class OriginalWritePolicy\|class InPlaceWriter" src` prints one path each. Done when: the test fails on a planted second key and passes on the tree.
- [ ] Log one Serilog Information line per opt-in change (`Originals opt-in {Key} {Old} -> {New} locked={Locked}`). Done when: a Serilog test logger asserts the line for a tick and for a refused locked change.
- [ ] Drive the round trip: tick Rotate on this page, rotate a temp copy of a fixture JPEG from the grid, and confirm the write went through `InPlaceWriter` with a verified backup; then lock the key through the overlay and confirm the command is disabled. Done when: the log lines are quoted and the captures of the group, each confirmation, the status line, and the locked state are committed under `docs/captures/lumen/originals/`.
- [ ] Extend `docs/user/lumen/originals.md` (written by `D04 T11 §1`) with the Originals group, each opt-in, the backup settings, restore, and the administrator lock, and `docs/dev/lumen/deployment.md` with the overlay keys. Done when: every control on the group is documented with its default.
- [ ] Commit: `"lumen: the Originals preferences group over the one originals policy, lockable off"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~OriginalsGroupViewModelTests|FullyQualifiedName~OriginalsSettingsOwnerTests|FullyQualifiedName~DeploymentOverlayTests|FullyQualifiedName~PreferencePagesTests"` exits 0: every `Lumen.Originals.*` key has one owner, every opt-in defaults off, a locked key refuses; the driven round trip quotes the in-place rotate's log line with its backup path and the locked-state capture. Cheaper substitute that fails: a page with its own keys or writer, which `OriginalsSettingsOwnerTests` catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every test class named in §1 to §10 reporting
- [ ] The freeze checks of §9 and §10 pass: with every `Lumen.Originals.*` opt-in at its default, the unchanged-originals test of `D04 T02 §1` passes over a full session, and `OriginalsSettingsOwnerTests` find every `Lumen.Originals.*` key registered by `D04 T11 §1`'s `OriginalWritePolicy` and no writer onto an original outside its `InPlaceWriter`
- [ ] `PreferencePagesTests` pass over every key the parity files registered, and `docs/dev/lumen/preference-keys.md` and `docs/user/lumen/keyboard-shortcuts.md` match their generators
- [ ] `grep -rn "class WorkspaceService\|class PreferenceKeyRegistry\|class SystemInfoReport" src` prints one path per type, none under `src/Lumen/`
- [ ] Every capture named in a Fidelity line exists under `docs/captures/lumen/`, and every user guide page named in a section exists under `docs/user/lumen/`
- [ ] `python scripts/todo-claims.py` holds for this file
- [ ] `python scripts/todo-graph.py validate` clean
