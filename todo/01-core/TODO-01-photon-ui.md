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

> **Goal:** The suite's house style lives in one WPF library, `Photon.UI`, that every app consumes: the icon catalog and `VectorIcon`, the splash and exception windows, the border glow, the theme resources generated from the design system's `docs/design/tokens.json` with live theme, Highlight, and density switching, and the About and shortcuts dialogs once a second app needs them. No control or window exists twice.

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

- [`standards/shared.md`](../../standards/shared.md) -- the rule that shared code moves only when two apps need it
- [`standards/ui.md`](../../standards/ui.md) -- the UI standard every section here builds to (**Corrected 2026-09-27:** the design contract moved from `standards/shared.md` to `standards/ui.md` and the Photon Interface design system in `docs/design/`, operator decision "Yes, full import")
- [`docs/design/tokens.json`](../../docs/design/tokens.json) -- the token source §3 generates the theme dictionaries from; [`docs/design/README.md`](../../docs/design/README.md) (theme model, WPF implementation) and [`docs/design/components/Highlight/README.md`](../../docs/design/components/Highlight/README.md) (Windows accent mapping) are §3's spec
- [`docs/design/components/Icons/README.md`](../../docs/design/components/Icons/README.md) -- the icon catalog spec §1 builds to; [`docs/design/shell-layout.md`](../../docs/design/shell-layout.md) (Splash and Home) is §2's splash spec; [`docs/design/components/Dialog/README.md`](../../docs/design/components/Dialog/README.md) is the dialog spec §2 and §4 build to
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
- -> XREF: D00 T03 §3 -- the app icon raster export (the splash PNGs `AppIdentity.IconUri` names in §2)

## Outcome

- `src/Photon.UI/Photon.UI.csproj` exists, is in `Photon.slnx`, and both Nodus and Imago reference it.
- `VectorIcon`, the icon catalog, `BorderGlowAnimator`, `SplashWindow`, and `ExceptionWindow` exist once, in `Photon.UI`, and neither app keeps a copy.
- The theme dictionaries are generated from `docs/design/tokens.json` with a drift check, both apps merge them, and brightness theme, Highlight color, and density switch live; neither app defines a color a token names.
- The About and keyboard-shortcuts dialogs live in `Photon.UI` from the day Imago needs them, and both apps show them.

**Adjacency:** list=not-applicable (a control library holds no records to browse); document=not-applicable (no printed output); settings=not-applicable (the library reads no settings; apps pass values in); reporting=not-applicable (no data of its own); notifications=not-applicable (the splash status line is owned by each app's startup); permissions=not-applicable (nothing here writes a file); audit=not-applicable (no user action changes state here); exchange=not-applicable (no import or export); reverse=not-applicable (no edits to reverse)

**Adjacency rationale:** `Photon.UI` is presentation plumbing. Every user-facing behavior it enables is owned, and adjacency-declared, by the app section that uses it.

## Implementation Order

| Order | Section | Deliverable                                            | Depends On                           | Status |
| :---: | :-----: | ------------------------------------------------------ | ------------------------------------ | :----: |
|   1   |   §1    | Create Photon.UI with the icon catalog                 | D02 T01 §1, D03 T01 §1               |  [ ]   |
|   2   |   §2    | Splash, exception window, and glow move to Photon.UI   | §1, D00 T03 §3                       |  [ ]   |
|   3   |   §3    | The suite theme resources                              | §1, D00 T03 §2                       |  [ ]   |
|   4   |   §4    | About and shortcuts dialogs move to Photon.UI          | §3, D02 T05 §1, D02 T05 §2, D03 T01 §3 |  [ ]   |

---

## 1. Create Photon.UI with the Icon Catalog

`VectorIcon` and `IconService` draw Fluent UI System Icons from path data in `icons.json`, and both apps carry their own copy with diverged catalogs. This section creates the library with the union of both, so an icon added for one app is available to the other and drawn identically.

**Corrected 2026-09-27:** the spec is `docs/design/components/Icons/README.md`: one Lucide catalog (24 viewBox, stroke 1.5, round caps and joins, strokes only) and FluentIcons.Wpf leaves the suite. The merge below still moves the catalogs without a visual change; the added item then redraws every entry on the Lucide grid, so the after captures show the Lucide icons, not the baseline's.

**Fidelity:** no surface of its own -- the icons render inside existing windows whose captures (`docs/captures/nodus/main-window/`, `docs/captures/imago/main-window/`) must look the same after the move.

- [ ] Create `src/Photon.UI/Photon.UI.csproj` (`net11.0-windows10.0.26100.0` with `TargetPlatformMinVersion` 10.0.17763.0, as the apps; **Corrected 2026-09-26:** said `net10.0-windows`, `UseWPF`, `Nullable` enable, namespace root `Photon.UI`) and add it to `Photon.slnx` under a `/Shared/` folder. Done when: `dotnet build Photon.slnx -c Release` builds it.
- [ ] Merge the two `icons.json` catalogs into `src/Photon.UI/Resources/icons.json` (union by icon name; where both define a name with different path data, keep Nodus's and list the conflict in the commit body). Done when: every icon name used in either app's XAML (`grep -rho 'Icon="[A-Za-z0-9]*"'`) exists in the merged file.
- [ ] Move `VectorIcon` to `src/Photon.UI/Controls/VectorIcon.cs` from the larger Nodus copy, folding in any Imago-only behavior. Done when: both apps' copies are deleted and their XAML uses `xmlns:pui="clr-namespace:Photon.UI.Controls;assembly=Photon.UI"`.
- [ ] Move `IconService` to `src/Photon.UI/Icons/IconCatalog.cs` as a class registered as a singleton in each app's composition root; keep a static accessor only where `VectorIcon` needs one at XAML parse time, and document why beside it. Done when: neither app calls `IconService.Instance`.
- [ ] Load the catalog as an embedded resource of `Photon.UI` instead of a loose `Content` file. Done when: neither app's `.csproj` carries an `icons.json` item and the icons still render.
- [ ] Add `tests/Photon.UI.Tests` with `IconCatalogTests` (every catalog entry parses as WPF path geometry; a missing name returns the documented fallback, not an exception). Done when: the tests pass under `dotnet test Photon.slnx`.
- [ ] Replace every merged entry with its Lucide geometry (the names in `docs/design/components/bundle.js` first; a name Lucide lacks is drawn on the same grid with a note), render strokes in `VectorIcon` (`icon-stroke` 1.5 at 16 and 20 px, round caps and joins, no fill), and remove any FluentIcons.Wpf package reference (**Corrected 2026-09-27**). Done when: `IconCatalogTests` assert every entry is stroke-only on a 24 viewBox and `grep -rn FluentIcons src` prints nothing.
- [ ] Commit: `"ui: create Photon.UI with one icon catalog for the suite"`

**Requires:** display-session -- the launch smoke confirming both apps' icons still render needs an interactive desktop

**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0; `dotnet test Photon.slnx` exits 0 with `IconCatalogTests` reporting; `grep -rln "class VectorIcon\|class IconService" src/Nodus src/Imago` prints nothing; both apps launch and their main windows match the baseline captures icon for icon (new captures committed beside the baseline as `after-photon-ui-100.png`). Cheaper substitute that fails: referencing Nodus's `VectorIcon` from Imago, which makes one app depend on the other.

## 2. Splash, Exception Window, and Glow Move to Photon.UI

The splash window, the exception window, and `BorderGlowAnimator` are the same code in both apps with small drifts. Each app passes what differs (name, version, icon, log folder) as parameters.

**Corrected 2026-09-27:** each app now has splash art: the operator kept the neon Direction A drawings as splash and marketing art (`resources/icons/<app>/<app>-splash.svg`, `resources/icons/README.md`), and `D00 T03 §3` generates them as `resources/icons/<app>/PNG/<app>_splash_256.png` and `_512.png`. `AppIdentity.IconUri` points at the app's generated splash PNG (a pack URI to a linked `Resource`), so the shared window draws each app's own art without SharpVectors and without a copy of the art in `Photon.UI`. Where that art replaces what the before capture shows, the commit body names the difference.

**Fidelity:** splash and exception windows as imported -- no capture exists for either, so this section captures both apps' splash and exception windows before the move under `docs/captures/nodus/splash/`, `docs/captures/nodus/exception/`, and the Imago equivalents, then shows the moved windows match.
**Job:** a user sees which app is starting and, when something breaks, can copy a report and choose to continue or exit. Consumer: the user; the report text is also written to the app's log.
**Treatment:** one `SplashWindow` and one `ExceptionWindow` in `Photon.UI`, parameterized by an `AppIdentity` record (display name, version, icon URI). Cheaper substitute that fails the checkpoint: keeping two copies and sharing only a base class.
**Chrome:** consume the theme resources each app already merges. Do not invent a second window style.
**Corrected 2026-09-27:** the splash spec is `docs/design/shell-layout.md` (Splash and Home): 480 x 280, `surface-raised` with `radius-lg` and `shadow-dialog`, the neon art at 64 px, the app name in `display`, the version in `caption`, a launch progress bar and the border glow in `accent-<app>` (the glow fades over 300 ms and is off when animations are off); the exception window follows `docs/design/components/Dialog/README.md`. The only accent in either window is the app's identity accent; no hardcoded orange.

**Requires:** display-session -- the before and after captures of the splash and exception windows need an interactive desktop

- [ ] Capture both apps' splash and exception windows before the move (trigger the exception window with a Debug-only menu item or the debug window, then remove any temporary trigger). Done when: four capture folders exist with `before-100.png`.
- [ ] Add `src/Photon.UI/AppIdentity.cs` (a `record` with `DisplayName`, `Version`, `IconUri`, `LogFolder`). Done when: both apps construct one in their startup from assembly metadata, with `IconUri` naming the app's `resources/icons/<app>/PNG/<app>_splash_256.png` from `D00 T03 §3` (**Corrected 2026-09-27**).
- [ ] Move `SplashWindow` to `src/Photon.UI/Windows/SplashWindow.xaml(.cs)`, keeping the separate-thread show and the status-text API. Done when: both apps' copies are deleted and startup shows the shared window with the app's own name.
- [ ] Move `ExceptionWindow` to `src/Photon.UI/Windows/ExceptionWindow.xaml(.cs)`; "Copy report" copies the exception, the app identity, and the log folder path. Done when: both apps' copies are deleted and the copied text names the app.
- [ ] Move `BorderGlowAnimator` to `src/Photon.UI/Animation/BorderGlowAnimator.cs`, honoring `SystemParameters.ClientAreaAnimation` (no animation when Windows animation effects are off). Done when: both apps' copies are deleted.
- [ ] Add `AppIdentityTests` and an `ExceptionReportTests` for the report text (it contains the app name, version, exception type, and message). Done when: both pass under `dotnet test Photon.slnx`.
- [ ] Commit: `"ui: share the splash and exception windows and the border glow"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the two new test classes reporting; both apps start with the shared splash showing their own name; the exception window's copied report names the app; after captures under the four folders match the before captures apart from the app name; `grep -rln "class SplashWindow\|class ExceptionWindow\|class BorderGlowAnimator" src/Nodus src/Imago` prints nothing. Cheaper substitute that fails: moving only the code-behind and leaving two XAML files.

## 3. The Suite Theme Resources

**Corrected 2026-09-27:** rewritten for the operator's decision "Yes, full import": the design contract is now `standards/ui.md` and `docs/design/`, and the WPF themes are generated from `docs/design/tokens.json` with a drift check instead of hand-written from a table in `standards/shared.md`. The section said: create one hand-written `Photon.Dark.xaml` from the old grey ramp (`Crust` through `Text`) with a per-app `Accent` used for focus and selection, and test it against a table parsed from `standards/shared.md`. The old ramp, the single dark theme, and accent-as-selection are retired: selection and focus use the `state*` (Highlight) tokens, and the app accent is identity only.

`docs/design/tokens.json` defines four brightness themes (Darkest, Dark default, Medium Gray, Light), the Highlight color (Blue default, Photon orange, Windows accent), the app accents, status colors, type, spacing, two densities, radii, shadows, and motion. Today Nodus carries pure greys inline in `MainWindowView.xaml` and Imago carries Catppuccin Mocha in `Themes/Colors.xaml`. This section generates every theme dictionary from the tokens with a committed generator and a drift check, merges the result into both apps so neither defines a color a token names, and adds live switching of brightness theme, Highlight color (including the Windows accent), and density.

**Fidelity:** Nodus and Imago main windows -- docs/captures/nodus/main-window/ and docs/captures/imago/main-window/. Both apps move from their baselines to the design system's Dark theme: the new captures are compared against `docs/design/README.md` and the Cover and component previews of the Design System artifact, which win over both baselines.
**Job:** a user who opens two suite apps side by side sees one product, and can pick the brightness, Highlight color, and density they work best with, live. Consumer: every WPF surface in every app, through `DynamicResource` lookups, and the Preferences pages that expose the three choices (`D02 T16 §6`, `D03 T20 §9`, `D04 T14 §8`).
**Treatment:** `scripts/generate-theme.py` (stdlib Python, like the other scripts) reads `docs/design/tokens.json` and writes `src/Photon.UI/Themes/{Tokens,Darkest,Dark,MediumGray,Light,HighContrast}.xaml`, `Highlight.{Blue,Orange}.xaml`, and `Density.{Compact,Comfortable}.xaml` with token names as resource keys; `ThemeService`, `HighlightService`, and `DensityService` swap the merged dictionaries at runtime. Cheaper substitute that fails the checkpoint: hand-writing the dictionaries, which leaves XAML and tokens free to drift.
**Chrome:** consume the generated dictionaries through `DynamicResource`. Do not define a second palette in any app, and never hand-edit a generated file.

**Requires:** display-session -- the before and after captures of both main windows and the live-switch captures need an interactive desktop

- [ ] Add `scripts/generate-theme.py` reading `docs/design/tokens.json`: one `Color` plus `SolidColorBrush` pair per color token keyed by the token name (`surface-panel`, `state-line`, `accent-imago`...), per brightness theme, into `src/Photon.UI/Themes/Darkest.xaml`, `Dark.xaml`, `MediumGray.xaml`, and `Light.xaml` (theme ids `darkest`, `dark`, `medium`, `light`), with aliases such as `focus-ring` resolved to their target's value. Done when: the four files exist, each with one brush per color token in `tokens.json`.
- [ ] Generate `src/Photon.UI/Themes/Tokens.xaml` with the single-value tokens: sizes and spacing as `sys:Double` (and `Thickness` where the README names one), radii as `CornerRadius`, durations as `Duration`, `ease-out` as a `CubicEase` with `EasingMode="EaseOut"`, font families, and the type sizes (`type-caption`, `type-body-compact`, `type-body-comfortable`, `type-title`). Done when: every spacing, size, radius, and duration token has one resource.
- [ ] Generate the shadows (`shadow-tooltip`, `shadow-popup`, `shadow-dialog`, `glow-state`, `glow-state-orange`) per theme as `DropShadowEffect` resources in the brightness dictionaries. Done when: each theme file carries all five with its own values.
- [ ] Generate `Highlight.Blue.xaml` (empty: the brightness dictionaries carry the blue `state*` values) and `Highlight.Orange.xaml`, which re-points every `state*` key plus `focus-ring`, `handle-stroke`, and `glow-state` at the active theme's `state-orange*` values, so Orange follows a brightness switch. Done when: a test merges Orange over each theme and reads each theme's `state-orange` value from `state`.
- [ ] Generate `Density.Compact.xaml` and `Density.Comfortable.xaml`, pointing the neutral keys (`control-h`, `menu-row-h`, `optionsbar-h`, `doctab-h`, `tool-button`, `toolrail-w`, `panel-tab-h`, `row-h`, `layer-row-h`, `statusbar-h`, `check-size`, `swatch`, and the body type size) at the `-compact` or `-comfortable` token. Done when: every `-compact` and `-comfortable` pair in `tokens.json` has one neutral key in both files.
- [ ] Generate `HighContrast.xaml` mapping token keys to `SystemColors` brushes per the high-contrast table in `docs/design/README.md` (surfaces to `WindowBrush`; text, icons, and borders to `WindowTextBrush`; the `state` family to `HighlightBrush`; `state-on` to `HighlightTextBrush`; `state-text` to `HotTrackBrush`; disabled text to `GrayTextBrush`), with accent and status fills dropped. Done when: every color token has a high-contrast entry.
- [ ] Write a header comment into every generated file naming `docs/design/tokens.json` and `scripts/generate-theme.py` and saying the file is generated and must not be hand-edited; make the output byte-stable (token order from the JSON, LF line ends, no timestamp). Done when: running the generator twice produces identical bytes.
- [ ] Add the drift check: `python scripts/generate-theme.py --check` regenerates into memory and exits 1 naming each file that differs from the committed XAML; wire it into `scripts/check-all.ps1` and the CI workflow. Done when: editing one hex in a generated file, or one value in `tokens.json` without regenerating, makes `check-all` fail, and the clean tree passes.
- [ ] Add `ThemeTokensTests` in `tests/Photon.UI.Tests`: load each generated dictionary and assert every color token in `docs/design/tokens.json` resolves with that theme's value, parsing the JSON itself so a token change without regeneration fails. Done when: the tests pass for all four themes, both Highlight files, both density files, and `HighContrast.xaml`.
- [ ] Merge `Tokens.xaml`, `Dark.xaml`, `Highlight.Blue.xaml`, and `Density.Compact.xaml` in that order at the top of Nodus's `App.xaml`, delete the inline `Color` definitions from `MainWindowView.xaml`, and map every old key (`Crust`, `Base`, `Mantle`, `Surface0`...) to its token (`frame`, `canvas-surround`, `surface-panel`, `surface-control`...), listing the mapping in the commit body. Done when: `grep -c '<Color x:Key'` on that file prints 0 and Nodus launches with 0 `Cannot find resource` lines.
- [ ] Merge the same dictionaries in Imago's `App.xaml`, delete `Themes/Colors.xaml` and the palette part of `Themes/Brushes.xaml`, and map every Catppuccin key Imago uses (`Surface0`, `Overlay1`, `Mauve`...) to its token, listing the mapping in the commit body; the orange Imago used for selection or focus maps to the `state*` tokens, never to `accent-imago`. Done when: Imago builds, the debug output has no `Cannot find resource` line, and `grep -rni "#FF6B35\|#F5923E" src/Imago --include=*.xaml` prints nothing.
- [ ] Set the app accent once per app at startup (`Photon.App.Accent`, `AccentHover`, `AccentOn` pointed at `accent-<app>`, `-hover`, `-on`), used only by the title-bar app mark, the splash, and the primary button; replace every selection, focus, checked, or active-tool use of an accent or orange brush in both apps with the matching `state*` token. Done when: a XAML scan test finds `Photon.App.Accent` referenced only from the primary button, splash, and app-mark styles.
- [ ] Replace hardcoded `#RRGGBB` literals in both main windows with token lookups where a token names the value; list any literal that stays (artwork preview checkerboards, for example) with a reason. Done when: `grep -c '#[0-9A-Fa-f]\{6\}'` on each main-window XAML is at most the listed count.
- [ ] Add `ThemeService.Apply(ThemeId)` in `src/Photon.UI/Themes/` that swaps the brightness dictionary in `Application.Resources.MergedDictionaries` live, persisted as `photon.ui.theme` (default `dark`), and loads `HighContrast.xaml` instead while `SystemParameters.HighContrast` is true (following `SystemParameters.StaticPropertyChanged`). Done when: `ThemeServiceTests` apply each of the four themes and every token resolves from that theme without a restart, and a faked high-contrast flag loads the high-contrast dictionary.
- [ ] Add `HighlightService.Apply(HighlightId)` (`blue` default, `orange`, `windows`) swapping the Highlight dictionary merged after the brightness dictionary, persisted as `photon.ui.highlight`, reapplied on every theme switch. Done when: `HighlightServiceTests` assert `state` resolves to the blue, then the orange value of the active theme, without a restart.
- [ ] Build the Windows accent option in `HighlightService`: read `UISettings.GetColorValue` (Accent, AccentLight1-3, AccentDark1-3), map per theme by the table in `docs/design/components/Highlight/README.md`, check each value against the blue set's pairs (4.5:1 text, 3:1 marks), step it in OKLCH lightness until it passes, pick `state-on` as white or `#141414` by contrast, and rebuild on `UISettings.ColorValuesChanged` marshalled to the dispatcher; on an exception or no accent, fall back to Blue and log a Warning. Done when: `WindowsAccentHighlightTests` with a fake `UISettings` source assert the mapping, the contrast adjustment of a too-light accent, the live rebuild on a change event, and the Blue fallback.
- [ ] Add `DensityService.Apply(DensityId)` (`compact` default, `comfortable`) swapping the density dictionary live, persisted as `photon.ui.density`. Done when: `DensityServiceTests` assert `control-h` resolves to 24 then 30 without a restart.
- [ ] Capture one live switch in each app to Light, to Photon orange, and to Comfortable under `docs/captures/nodus/main-window/` and `docs/captures/imago/main-window/`. Done when: the captures are committed and each switch happened without a restart.
- [ ] Commit: `"ui: generate the suite themes from the design tokens with live theme, highlight, and density"`

**Test checkpoint:** `python scripts/generate-theme.py --check` exits 0 on the clean tree and 1 after a one-value edit to `docs/design/tokens.json` without regenerating; `dotnet test Photon.slnx` exits 0 with `ThemeTokensTests`, `ThemeServiceTests`, `HighlightServiceTests`, `WindowsAccentHighlightTests`, and `DensityServiceTests` reporting; both apps launch with 0 `Cannot find resource` lines in the debug output; new captures `docs/captures/nodus/main-window/theme-100.png` and `docs/captures/imago/main-window/theme-100.png` (the Dark theme) and the live-switch captures are committed. Cheaper substitute that fails: hand-written dictionaries or a Dark-only theme, which the drift check and `ThemeTokensTests` reject.

## 4. About and Shortcuts Dialogs Move to Photon.UI

Nodus builds its About and keyboard-shortcuts dialogs first (`D02 T05 §1`, `§2`), inside Nodus, because only Nodus needs them then. The day Imago needs the same dialogs (its 0.1.0, `D03 T06 §1`), they move here instead of being copied. This section is that move.

**Fidelity:** Nodus About and shortcuts dialogs -- docs/captures/nodus/about/ and docs/captures/nodus/shortcuts/ (written by `D02 T05 §1` and `§2`); the Imago versions must match them apart from identity and content.
**Job:** a user of either app can see what they are running (name, version, license, credits, links) and every keyboard shortcut. Consumer: the user.
**Treatment:** `AboutDialog` parameterized by `AppIdentity` plus a credits list; `ShortcutsDialog` bound to a keymap the app passes in (the app owns its commands, the dialog owns the presentation, search, and print). Cheaper substitute that fails the checkpoint: a copy of Nodus's dialogs in Imago.
**Chrome:** consume the generated theme dictionaries of §3 and `AppIdentity`. Do not build a second dialog shell.
**Corrected 2026-09-27:** said consume `Photon.Dark.xaml`, which §3 no longer creates. The dialog spec is `docs/design/components/Dialog/README.md`; the About dialog shows the app icon master at 128 px (`docs/design/components/AppIcon/README.md`), and its one primary button is the only place it shows the app accent.

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
