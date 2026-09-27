---
schema_version: 1
id: photon-ui
domain: 01-core
status: draft
title: "TODO-01 -- Photon.UI: the Shared WPF Library"
depends_on: []
track: C1
---

# TODO-01 -- Photon.UI: the Shared WPF Library

> **Goal:** The suite's house style lives in one WPF library, `Photon.UI`, that every app consumes: the icon catalog and `VectorIcon`, the splash and exception windows, the border glow, the theme resources the design contract names, and the About and shortcuts dialogs once a second app needs them. No control or window exists twice.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** There is no `src/Photon.UI/`. Nodus and Imago each carry their own copy of the same UI pieces, grown from one origin: `VectorIcon.cs` (Nodus 145 lines, Imago 119), `IconService.cs` (68 and 69), `BorderGlowAnimator.cs` (209 and 209), `SplashWindow.xaml.cs` (121 and 115), and `ExceptionWindow.xaml.cs` (174 and 171). Each has its own `Resources/icons.json` (Nodus 7 lines, Imago 69), and the two differ. The palettes differ too: Nodus's `MainWindowView.xaml` defines pure greys (`Base` `#1A1A1A`), Imago's `Themes/Colors.xaml` defines Catppuccin Mocha (`Base` `#1E1E2E`) with an orange accent. Both apps load `IconService` through a static `Instance`.
<!-- claim: absent src/Photon.UI -->
<!-- claim: lines src/Nodus/Bezier.Desktop/Controls/VectorIcon.cs = 145 -->
<!-- claim: lines src/Imago/src/Imago.UI/Controls/VectorIcon.cs = 119 -->
<!-- claim: lines src/Nodus/Bezier.Desktop/Helpers/BorderGlowAnimator.cs = 209 -->
<!-- claim: lines src/Imago/src/Imago.UI/Helpers/BorderGlowAnimator.cs = 209 -->
<!-- claim: count "<Color x:Key=\"Base\">#1E1E2E</Color>" src/Imago/src/Imago.UI/Themes/Colors.xaml = 1 -->
<!-- claim: count "<Color x:Key=\"Base\">#1A1A1A</Color>" src/Nodus/Bezier.Desktop/Views/MainWindowView.xaml = 1 -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- the design contract §3 turns into resources, and the rule that shared code moves only when two apps need it
- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- where `Photon.UI` sits in the target layout
- `docs/captures/nodus/main-window/`, `docs/captures/imago/main-window/` -- the baselines (`D00 T03 §2`) the theme change is reviewed against
- -> XREF: D02 T05 §1 -- the Nodus About dialog §4 moves here when Imago needs one
- -> XREF: D03 T06 §1 -- the Imago About and shortcuts surfaces §4 exists for
- -> XREF: D03 T01 §3 -- the WPF-UI removal that must land before Imago consumes this library's dialogs
- -> XREF: D06 T02 §1 -- the architecture page that documents this library once §2 lands
- -> XREF: D01 T05 §4 -- the shared AI surfaces (send preview, AI settings page) built on §3's theme
- -> XREF: D02 T09 §2 -- the Nodus color picker and the swatch-well, checkerboard, and gamut-warning tokens it adds to §3's theme; the picker moves here when Imago's color panel (`D03 T03 §8`) needs it
- -> XREF: D02 T16 §6 -- the UI brightness dictionaries it adds to §3's theme and the error-reporting toggle that governs §2's exception window
- -> XREF: D03 T20 §1 -- Imago parity workspace cites §2: the exception window the debugging and crash-report preferences govern; §3: the suite theme; §4: the shared About and Shortcuts dialogs
- -> XREF: D04 T14 §8 -- Lumen parity workspace cites §3: the suite theme D04 T14 §8 consumes; §4: the shared About and shortcuts dialog D04 T14 §3 and D04 T14 §7 consume

## Outcome

- `src/Photon.UI/Photon.UI.csproj` exists, is in `Photon.slnx`, and both Nodus and Imago reference it.
- `VectorIcon`, the icon catalog, `BorderGlowAnimator`, `SplashWindow`, and `ExceptionWindow` exist once, in `Photon.UI`, and neither app keeps a copy.
- One theme dictionary carries the design contract's tokens, and both apps merge it; neither app defines a color the dictionary names.
- The About and keyboard-shortcuts dialogs live in `Photon.UI` from the day Imago needs them, and both apps show them.

**Adjacency:** list=not-applicable (a control library holds no records to browse); document=not-applicable (no printed output); settings=not-applicable (the library reads no settings; apps pass values in); reporting=not-applicable (no data of its own); notifications=not-applicable (the splash status line is owned by each app's startup); permissions=not-applicable (nothing here writes a file); audit=not-applicable (no user action changes state here); exchange=not-applicable (no import or export); reverse=not-applicable (no edits to reverse)

**Adjacency rationale:** `Photon.UI` is presentation plumbing. Every user-facing behavior it enables is owned, and adjacency-declared, by the app section that uses it.

## Implementation Order

| Order | Section | Deliverable                                            | Depends On                           | Status |
| :---: | :-----: | ------------------------------------------------------ | ------------------------------------ | :----: |
|   1   |   §1    | Create Photon.UI with the icon catalog                 | D02 T01 §1, D03 T01 §1               |  [ ]   |
|   2   |   §2    | Splash, exception window, and glow move to Photon.UI   | §1                                   |  [ ]   |
|   3   |   §3    | The suite theme resources                              | §1, D00 T03 §2                       |  [ ]   |
|   4   |   §4    | About and shortcuts dialogs move to Photon.UI          | §3, D02 T05 §1, D02 T05 §2, D03 T01 §3 |  [ ]   |

---

## 1. Create Photon.UI with the Icon Catalog

`VectorIcon` and `IconService` draw Fluent UI System Icons from path data in `icons.json`, and both apps carry their own copy with diverged catalogs. This section creates the library with the union of both, so an icon added for one app is available to the other and drawn identically.

**Fidelity:** no surface of its own -- the icons render inside existing windows whose captures (`docs/captures/nodus/main-window/`, `docs/captures/imago/main-window/`) must look the same after the move.

- [ ] Create `src/Photon.UI/Photon.UI.csproj` (`net11.0-windows10.0.26100.0` with `TargetPlatformMinVersion` 10.0.17763.0, as the apps; **Corrected 2026-09-26:** said `net10.0-windows`, `UseWPF`, `Nullable` enable, namespace root `Photon.UI`) and add it to `Photon.slnx` under a `/Shared/` folder. Done when: `dotnet build Photon.slnx -c Release` builds it.
- [ ] Merge the two `icons.json` catalogs into `src/Photon.UI/Resources/icons.json` (union by icon name; where both define a name with different path data, keep Nodus's and list the conflict in the commit body). Done when: every icon name used in either app's XAML (`grep -rho 'Icon="[A-Za-z0-9]*"'`) exists in the merged file.
- [ ] Move `VectorIcon` to `src/Photon.UI/Controls/VectorIcon.cs` from the larger Nodus copy, folding in any Imago-only behavior. Done when: both apps' copies are deleted and their XAML uses `xmlns:pui="clr-namespace:Photon.UI.Controls;assembly=Photon.UI"`.
- [ ] Move `IconService` to `src/Photon.UI/Icons/IconCatalog.cs` as a class registered as a singleton in each app's composition root; keep a static accessor only where `VectorIcon` needs one at XAML parse time, and document why beside it. Done when: neither app calls `IconService.Instance`.
- [ ] Load the catalog as an embedded resource of `Photon.UI` instead of a loose `Content` file. Done when: neither app's `.csproj` carries an `icons.json` item and the icons still render.
- [ ] Add `tests/Photon.UI.Tests` with `IconCatalogTests` (every catalog entry parses as WPF path geometry; a missing name returns the documented fallback, not an exception). Done when: the tests pass under `dotnet test Photon.slnx`.
- [ ] Commit: `"ui: create Photon.UI with one icon catalog for the suite"`

**Requires:** display-session -- the launch smoke confirming both apps' icons still render needs an interactive desktop

**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0; `dotnet test Photon.slnx` exits 0 with `IconCatalogTests` reporting; `grep -rln "class VectorIcon\|class IconService" src/Nodus src/Imago` prints nothing; both apps launch and their main windows match the baseline captures icon for icon (new captures committed beside the baseline as `after-photon-ui-100.png`). Cheaper substitute that fails: referencing Nodus's `VectorIcon` from Imago, which makes one app depend on the other.

## 2. Splash, Exception Window, and Glow Move to Photon.UI

The splash window, the exception window, and `BorderGlowAnimator` are the same code in both apps with small drifts. Each app passes what differs (name, version, icon, log folder) as parameters.

**Fidelity:** splash and exception windows as imported -- no capture exists for either, so this section captures both apps' splash and exception windows before the move under `docs/captures/nodus/splash/`, `docs/captures/nodus/exception/`, and the Imago equivalents, then shows the moved windows match.
**Job:** a user sees which app is starting and, when something breaks, can copy a report and choose to continue or exit. Consumer: the user; the report text is also written to the app's log.
**Treatment:** one `SplashWindow` and one `ExceptionWindow` in `Photon.UI`, parameterized by an `AppIdentity` record (display name, version, icon URI). Cheaper substitute that fails the checkpoint: keeping two copies and sharing only a base class.
**Chrome:** consume the theme resources each app already merges. Do not invent a second window style.

**Requires:** display-session -- the before and after captures of the splash and exception windows need an interactive desktop

- [ ] Capture both apps' splash and exception windows before the move (trigger the exception window with a Debug-only menu item or the debug window, then remove any temporary trigger). Done when: four capture folders exist with `before-100.png`.
- [ ] Add `src/Photon.UI/AppIdentity.cs` (a `record` with `DisplayName`, `Version`, `IconUri`, `LogFolder`). Done when: both apps construct one in their startup from assembly metadata.
- [ ] Move `SplashWindow` to `src/Photon.UI/Windows/SplashWindow.xaml(.cs)`, keeping the separate-thread show and the status-text API. Done when: both apps' copies are deleted and startup shows the shared window with the app's own name.
- [ ] Move `ExceptionWindow` to `src/Photon.UI/Windows/ExceptionWindow.xaml(.cs)`; "Copy report" copies the exception, the app identity, and the log folder path. Done when: both apps' copies are deleted and the copied text names the app.
- [ ] Move `BorderGlowAnimator` to `src/Photon.UI/Animation/BorderGlowAnimator.cs`, honoring `SystemParameters.ClientAreaAnimation` (no animation when Windows animation effects are off). Done when: both apps' copies are deleted.
- [ ] Add `AppIdentityTests` and an `ExceptionReportTests` for the report text (it contains the app name, version, exception type, and message). Done when: both pass under `dotnet test Photon.slnx`.
- [ ] Commit: `"ui: share the splash and exception windows and the border glow"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the two new test classes reporting; both apps start with the shared splash showing their own name; the exception window's copied report names the app; after captures under the four folders match the before captures apart from the app name; `grep -rln "class SplashWindow\|class ExceptionWindow\|class BorderGlowAnimator" src/Nodus src/Imago` prints nothing. Cheaper substitute that fails: moving only the code-behind and leaving two XAML files.

## 3. The Suite Theme Resources

The design contract in `standards/shared.md` names one grey ramp, one type scale, and one spacing grid for the whole suite. Today Nodus carries the greys inline in `MainWindowView.xaml` and Imago carries Catppuccin Mocha in `Themes/Colors.xaml`. This section makes the contract a resource dictionary both apps merge, so Imago takes the suite palette and neither app defines a color the dictionary names.

**Fidelity:** Nodus and Imago main windows -- docs/captures/nodus/main-window/ and docs/captures/imago/main-window/. Nodus must look the same after the change (its values are the contract's); Imago moves from Catppuccin to the contract's greys, and its new capture is compared against the contract in `standards/shared.md`, which wins over the Imago baseline.
**Job:** a user who opens two suite apps side by side sees one product. Consumer: every WPF surface in both apps, through `DynamicResource` lookups.
**Treatment:** `src/Photon.UI/Themes/Photon.Dark.xaml` with the contract's tokens as `Color` and `SolidColorBrush` pairs, plus typography (`FontFamily`, sizes) and spacing (`Thickness`) resources, merged first in each `App.xaml`. Cheaper substitute that fails the checkpoint: copying Nodus's inline colors into Imago's `Colors.xaml`, which leaves two dictionaries to drift.
**Chrome:** consume `Photon.Dark.xaml`. Do not define a second palette in either app.

**Requires:** display-session -- the before and after captures of both main windows need an interactive desktop

- [ ] Create `src/Photon.UI/Themes/Photon.Dark.xaml` with every token in the contract's Color table (`Crust` through `Text`), a `Brush` for each, the status colors, `Accent` set per app from the design contract's accent table (Nodus `#29C5E6`, Imago `#F5923E`, Lumen `#4CC47A` in the dark theme; **Corrected 2026-09-27:** said `Accent` defaults to `Subtext0` until the operator picks per-app accents; the operator chose them that day), the type sizes, and the spacing steps. Done when: every token in `standards/shared.md` has a resource of the same name and each app resolves `Accent` to its row of the accent table.
- [ ] Merge it first in `src/Nodus/.../App.xaml` and delete the inline `Color` definitions from Nodus's `MainWindowView.xaml`. Done when: `grep -c '<Color x:Key' ` on that file prints 0 and the window looks unchanged.
- [ ] Merge it first in Imago's `App.xaml`, delete `Themes/Colors.xaml` and the palette part of `Themes/Brushes.xaml`, and map every Catppuccin key Imago uses (`Surface0`, `Overlay1`, `Mauve`, and so on) to the contract's nearest token, listing the mapping in the commit body. Done when: Imago builds, no `StaticResource` or `DynamicResource` lookup fails at runtime (the debug output has no `Cannot find resource` line), and Imago's capture shows the grey ramp.
- [ ] Replace hardcoded `#RRGGBB` literals in both main windows with token lookups where a token names the value; list any literal that stays (artwork preview checkerboards, for example) with a reason. Done when: `grep -c '#[0-9A-Fa-f]\{6\}'` on each main-window XAML is at most the listed count.
- [ ] Add a `ThemeTokensTests` in `tests/Photon.UI.Tests` that loads `Photon.Dark.xaml` and asserts every token named in `standards/shared.md`'s Color table exists with the stated value and each app's `Accent` equals its dark-theme value in the accent table. Done when: the test parses the table from the standard itself, so changing one without the other fails.
- [ ] Commit: `"ui: one suite theme from the design contract"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `ThemeTokensTests` reporting; editing one value in `standards/shared.md` without the dictionary makes it fail; both apps launch with 0 `Cannot find resource` lines in the debug output; new captures `docs/captures/nodus/main-window/theme-100.png` (visually identical to `empty-100.png`) and `docs/captures/imago/main-window/theme-100.png` (grey ramp) are committed. Cheaper substitute that fails: leaving Imago on Catppuccin, which `ThemeTokensTests` cannot see but the Imago capture comparison against the contract can.

## 4. About and Shortcuts Dialogs Move to Photon.UI

Nodus builds its About and keyboard-shortcuts dialogs first (`D02 T05 §1`, `§2`), inside Nodus, because only Nodus needs them then. The day Imago needs the same dialogs (its 0.1.0, `D03 T06 §1`), they move here instead of being copied. This section is that move.

**Fidelity:** Nodus About and shortcuts dialogs -- docs/captures/nodus/about/ and docs/captures/nodus/shortcuts/ (written by `D02 T05 §1` and `§2`); the Imago versions must match them apart from identity and content.
**Job:** a user of either app can see what they are running (name, version, license, credits, links) and every keyboard shortcut. Consumer: the user.
**Treatment:** `AboutDialog` parameterized by `AppIdentity` plus a credits list; `ShortcutsDialog` bound to a keymap the app passes in (the app owns its commands, the dialog owns the presentation, search, and print). Cheaper substitute that fails the checkpoint: a copy of Nodus's dialogs in Imago.
**Chrome:** consume `Photon.Dark.xaml` and `AppIdentity`. Do not build a second dialog shell.

**Requires:** display-session -- captures of both apps' dialogs need an interactive desktop

- [ ] Move `AboutDialog` from Nodus to `src/Photon.UI/Dialogs/AboutDialog.xaml(.cs)` with an `AboutViewModel` taking `AppIdentity` and a credits list. Done when: Nodus's copy is deleted and Nodus's Help, About still shows its own identity.
- [ ] Move `ShortcutsDialog` to `src/Photon.UI/Dialogs/ShortcutsDialog.xaml(.cs)`, taking an `IReadOnlyList<ShortcutEntry>` (`record ShortcutEntry(string Category, string Command, string Gesture)`). Done when: Nodus passes its keymap and the dialog shows it unchanged.
- [ ] Wire both dialogs into Imago's Help menu with Imago's identity, credits, and keymap. Done when: Imago's Help, About and Help, Keyboard Shortcuts open them.
- [ ] Move the view-model tests with the code to `tests/Photon.UI.Tests`. Done when: they pass there and no copy remains in the Nodus tests.
- [ ] Capture Imago's two dialogs under `docs/captures/imago/about/` and `docs/captures/imago/shortcuts/`. Done when: the four capture folders exist.
- [ ] Commit: `"ui: share the About and shortcuts dialogs across Nodus and Imago"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the moved tests reporting from `Photon.UI.Tests`; `grep -rln "class AboutDialog\|class ShortcutsDialog" src/Nodus src/Imago` prints nothing; both apps show both dialogs with their own identity and keymap, and the captures show it. Cheaper substitute that fails: Imago referencing Nodus's assembly for the dialogs.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every `Photon.UI.Tests` class reporting
- [ ] No duplicate of a `Photon.UI` type remains in any app (`grep` per type, quoted)
- [ ] Captures for every surface this file moved are committed
- [ ] `python scripts/todo-graph.py validate` clean
