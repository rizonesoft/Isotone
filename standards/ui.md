# UI Standard

Every user-facing surface of Stilus, Gesso, and Albumen answers to this standard. It is the binding summary of the Isotone Interface design system in [`docs/design/`](../docs/design/README.md), which holds the full specification: the tokens, one README per component, the shell layout, and the app icon guide. The system is browsable as a live page, with every component preview in all four themes, at https://rizonesoft.github.io/Isotone/design/ (generated into `docs/design/index.html` by `scripts/build-design-site.py`; edit the sources, never the page). Where this file and `docs/design/` disagree, `docs/design/` wins and this file is corrected in the same commit. How the code is held to the design (fidelity, goldens, deviations, the gates, and the definition of done for a UI section) is the binding [`design-contract.md`](design-contract.md). The captures of the imported apps under `docs/captures/<app>/` are a before record only; the review reference is the design itself and the approved goldens under `docs/captures/golden/`.

## The source of truth

- `docs/design/tokens.json` is the one source for every color, size, spacing, radius, shadow, duration, and type style. A value that is not a token is not part of the system.
- The token tables of `isotone::ui` (under `native/ui/tokens/`, created with the toolkit by `D01 T01 §3`) are generated from `tokens.json` by a committed generator; never hand-edit a generated table. Change the token, regenerate, and commit both together; the drift check (`D01 T01 §3`) fails when they disagree.
- `docs/design/` is the only home of the design system; its public view is https://rizonesoft.github.io/Isotone/design/, generated from it. Edit the sources and regenerate the page as [`docs/design/EDITING.md`](../docs/design/EDITING.md) describes.
- A surface never hardcodes a color, size, or spacing value that a token names.

## Themes

- Four brightness themes, as Photoshop offers: Darkest, Dark (the default), Medium Gray, and Light. Every color token carries a value for each; the user picks one in Preferences > Interface > Color theme and the switch applies live.
- Chrome is neutral grey and recedes; color in the chrome means state, identity, or status, never decoration. The canvas is the only region with saturated color.
- Surfaces layer as `frame` (title bar, document tab strip, status bar, gaps between panels), `surface-panel` (panels, tool rail, options bar), `surface-tabstrip`, `surface-raised` (anything that floats), `surface-field` (inset wells for text and number fields), `surface-control` (button faces), and `canvas-surround` (the pasteboard).

## State color (Highlight) and app accent

- The state color, called the Highlight color, marks selection, keyboard focus, checked checkboxes and radios, the active tool, the highlighted menu item, slider fills, selected rows, drop targets, and links. Its tokens are `state`, `state-hover`, `state-pressed`, `state-on`, `state-subtle`, `state-tint`, `state-line`, `state-text`, and `focus-ring` (an alias of `state-line`); `handle-stroke` and `glow-state` follow it.
- The Highlight color is a user choice in Preferences > Interface > Highlight color: Blue (default, `#1473E6` family, tuned per theme), Isotone orange (the `state-orange*` tokens, Bezier's `#FF6B35`), or the Windows accent color.
- The choice switches at runtime without a restart. The Windows accent option reads `UISettings` (Accent, AccentLight1-3, AccentDark1-3), follows `UISettings.ColorValuesChanged`, contrast-adjusts each derived value per theme until it meets the targets below, and falls back to Blue with a Warning log line when no accent is available. The mapping is in [`docs/design/components/Highlight/README.md`](../docs/design/components/Highlight/README.md).
- The app accent is identity only: it appears on the title-bar app mark, the splash and its launch progress, and the single primary button of a view, with its label in `accent-<app>-on`. It never marks selection, focus, or a checked state, and a Highlight color never stands in for it.

| App | Accent | Dark, Darkest, Medium Gray | Light |
| --- | --- | --- | --- |
| Stilus | Cyan, `accent-stilus` | `#29C5E6` | `#00758C` |
| Gesso | Orange, `accent-gesso` | `#F5923E` | `#B04F00` |
| Albumen | Green, `accent-albumen` | `#4CC47A` | `#1B7A3D` |

- The values above are copied from `tokens.json` for reading; `tokens.json` is authoritative, with the `-hover` and `-on` companions of each accent.

## Status colors

- `status-error`, `status-warning`, `status-success`, and `status-info`, each with a `-subtle` fill for info bars and toast wells, mean status only and are never decoration.
- A status color always travels with its icon (`error`, `alert`, `success`, `info`) and a word; color alone never carries the meaning, because error and success are not separable by lightness.
- Destructive commands are default buttons with a verb that names what goes, never red fills.

## Type

- Segoe UI Variable (then Segoe UI, then system-ui) for the interface; Segoe UI Variable Display for the splash name only; Cascadia Mono (then Consolas) for coordinates, readouts, hex values, and logs. Nothing ships a font.
- The scale: `caption` 11/14, `body` 12/16, `body-strong` 12/16 semibold, `section-header` 11/14 semibold in capitals, `title` 14/20, `dialog-title` 14/20 semibold, `display` 46/56 semibold (the splash app name), `mono` 11/14, `mono-body` 12/16. Comfortable density raises caption, body, and body-strong to 12/16, 13/18, and 13/18.
- Sentence case for buttons, labels, and messages; title case for menu items and dialog titles; an ellipsis on commands that open a dialog. No exclamation marks, no emoji, never "we".

## Spacing and density

- A 4 px grid: `space-hair` 2, `space-1` 4, `space-1-5` 6, `space-2` 8, `space-3` 12, `space-4` 16, `space-6` 24.
- Two densities in Preferences > Interface > UI density, switched live: Compact (the default: 24 px controls, 12 px text, 16 px toolbar icons) and Comfortable (30 px controls, 13 px text, 20 px toolbar icons). Every density-dependent size is a `-compact` and `-comfortable` token pair.
- Fixed in both densities: title bar 32, caption buttons 46 wide, info bar 28, section header 28, ruler 18, right dock 280 (260 to 300).

## Shape, elevation, and motion

- Radii: `radius-sm` 2 px for everything docked in the chrome, `radius-md` 4 px for menus, dropdowns, and flyouts, `radius-lg` 6 px for dialogs and toasts, `radius-round` only for radio buttons, toggle switches, slider thumbs, and status dots.
- Docked chrome is flat and separated by 1 px `divider` hairlines. Elevation exists only on things that float: `shadow-tooltip` on tooltips, `shadow-popup` on menus, dropdowns, and flyouts, `shadow-dialog` on dialogs, toasts, and floating panels, each with a 1 px `border-popup`.
- Motion uses one curve, `ease-out` (cubic out), at `duration-fast` 100 ms (hover, press, toggles), `duration-standard` 200 ms (menus, flyouts, expanders, toasts, the splash fade-out), and `duration-slow` 400 ms (dialogs); tooltips open after `tooltip-delay` 400 ms.
- When Windows animation effects are off (`SPI_GETCLIENTAREAANIMATION` false, re-read on `WM_SETTINGCHANGE`), every duration is 0 and marching ants, spinners, and indeterminate bars stop. Nothing in the chrome moves on its own otherwise.

## Focus

- One focus ring: 2 px `focus-ring`, drawn 1 px outside buttons and boxes, inset on rows, tabs, and menu titles, and as a colored border plus 1 px inner line on fields, so a field does not grow.
- The ring shows for keyboard focus only, never for mouse focus, and is never removed. No system focus rectangle is ever shown; each element draws the ring itself. The spec is [`docs/design/components/FocusRing/README.md`](../docs/design/components/FocusRing/README.md).

## Icons

- One UI icon catalog: Lucide geometry (ISC), 24 viewBox, stroke 1.5, round caps and joins, strokes only, at `icon-sm` 16 px (menus, panels, options bar, rows, buttons) and `icon-md` 20 px (tool rail). No second icon family is used, and emoji are never icons. The spec is [`docs/design/components/Icons/README.md`](../docs/design/components/Icons/README.md).
- Icon color is `icon` at rest, `text-primary` on hover or when active, `state-on` on a `state` fill, and `text-disabled` when disabled; a catalog icon never takes the app accent.
- App icons are separate from the catalog: the Direction C suite tile files in `resources/icons/<app>/`, used by the ladder and rules in [`docs/design/app-icons.md`](../docs/design/app-icons.md). A catalog icon never stands in for an app icon, and an app icon is never recolored.

## Window anatomy

- Every document window has one anatomy, specified in [`docs/design/shell-layout.md`](../docs/design/shell-layout.md): a custom title bar with the app mark, the menu bar inside it, a drag area, and the three caption buttons; the options bar; an optional hint bar; the tool rail on the left; document tabs; the canvas with rulers; docked panels on the right; and the status bar. A feature adds to this anatomy; it never invents a second one.
- The title bar is drawn by `isotone::ui` itself (the DWM frame extended into the client area, with non-client hit testing that keeps Windows 11 snap layouts on the maximize button): the OS frame is removed, never doubled, and the caption buttons are 46 x 32 catalog glyphs with a red close hover, never tinted by the Highlight color or the accent. Panels dock and float through the suite's own docking system, drawn from the same tokens.
- Each component in the anatomy has its spec under [`docs/design/components/`](../docs/design/components/): `WindowChrome`, `Menu`, `ContextMenu`, `OptionsBar`, `ToolRail`, `DocumentTabs`, `Panel`, `StatusBar`, `Dialog`, `Tooltip`, `Toast`, `NumberBox`, and the rest. A section that builds one of these cites its README as the spec.

## Ownership and legal text

- The copyright holder is Rizonetech (Pty) Ltd; Rizonesoft is its brand and stays the publisher users see (operator decision 2026-09-27). Every surface that states ownership says "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd" (the splash card shortens it to "© 2026 Rizonetech (Pty) Ltd · Free and open source (GPL-3.0)"), and none names Rizonesoft as the copyright holder.
- The About dialog carries exactly the lines of the About section in [`docs/design/components/Dialog/README.md`](../docs/design/components/Dialog/README.md): version, copyright, "Rizonesoft is a brand of Rizonetech (Pty) Ltd.", the GPL-3.0 license link, the source offer "Source code: <the GitHub tag URL of the build>", the product page, and the credits.
- A product page or download link is read from one configured value (default `https://www.rizonesoft.com/`), never typed into a surface; binaries are offered only from rizonesoft.com, never from GitHub. The names and icons are covered by [`TRADEMARKS.md`](../TRADEMARKS.md).

## Accessibility

- Contrast (WCAG 2.x) in all four themes: text at least 4.5:1 against every ground its usage names; control borders, focus rings, icons, and state marks at least 3:1. `text-disabled` is exempt. The checked pairs are in [`docs/design/README.md`](../docs/design/README.md); a new token or ground adds its pairs to that check.
- Windows high contrast (`SPI_GETHIGHCONTRAST`, re-read on `WM_SETTINGCHANGE`) selects the token table that maps tokens to the system colors (`GetSysColor`) instead of the four themes; accent and status fills are dropped while status keeps its icon and word, and the canvas keeps its own colors.
- Keyboard: F6 cycles the regions (tool rail, options bar, document, dock); Tab moves inside a region; every dialog works with the keyboard alone, with Enter and Escape doing what their buttons say; menus have access keys; tool shortcuts never fire while a text field has focus.
- Every icon-only control has a tooltip naming the command and its shortcut, and a UI Automation Name.
- Surfaces render correctly at 100, 150, and 200 percent scaling: sizes are device-independent, layout is rounded to physical pixels at every scale so hairlines stay one device pixel, and icons are vector paths.

## Native toolkit mapping

How `isotone::ui` carries the design (the spec's "Isotone UI", Element tree and theming). The values and tolerances are the design's and are unchanged; only the mechanism is named here.

- `isotone::ui` holds one generated token table per brightness theme (Darkest, Dark, Medium Gray, Light), a high-contrast table, the Highlight tables (Blue, Isotone orange, and one computed at run time from the Windows accent), and the Compact and Comfortable density tables, all generated from `tokens.json`. The theme, Highlight, and density names are the operator's (2026-09-27); `docs/design/README.md` and the Highlight card carry them too.
- A style names a token key and never a value: colors, sizes, radii, spacing, durations, the `ease-out` curve, and type styles are all looked up by the names `tokens.json` gives them (`surface-panel`, `control-h`, `radius-sm`, `duration-fast`).
- Tokens are resolved at run time, so a theme, Highlight, or density switch, or Windows changing high contrast, reduced motion, or DPI, invalidates the styles that read the changed keys and redraws open windows without a restart.
- The theme service selects the brightness table; the Highlight service layers the Highlight table over it; the density service points the neutral keys at the `-compact` or `-comfortable` values. Each app sets its accent keys once at startup.
- Every control a surface uses is one of the suite's own, drawn to its spec under `docs/design/components/` with rest, hover, pressed, disabled, and keyboard-focus states. No third-party control framework.
