Isotone Interface is the desktop UI of the Isotone Graphics Suite: Stilus (vector), Pinxit (raster) and Albumen (darkroom and photo manager), built in WPF for Windows 11. It is deliberately familiar to Photoshop users and grows out of Bezier, the Stilus prototype: its 2px corners, hairline dividers, glowing checked tools, rich tooltips, scrubbable number boxes and dense status bar all carry over.

## Principles

1. **Content first.** The image or artwork is the brightest, most colorful thing on screen. Chrome is neutral grey and recedes; color in the chrome means state, identity or status, never decoration.
2. **Photoshop-familiar.** Same window anatomy (menu bar in the title bar, options bar, tool rail on the left, document tabs, docked panels on the right, status bar), same shortcuts, same brightness themes, same blue highlight, same compact density. A Photoshop user should find every tool where their hands expect it.
3. **Suite-consistent.** Stilus, Pinxit and Albumen share every token, control and layout rule. The only visible difference between them is the app accent in the title-bar mark, the splash, and the one primary button of a view.
4. **Dense, not cramped.** 24px controls and 12px text by default, on a 4px grid, with a Comfortable density for larger or touch-adjacent screens.
5. **Every state drawn.** Hover, pressed, checked, disabled and keyboard focus are designed for every control; nothing falls back to stock WPF.

## Theme model

### Four brightness themes

Preferences > Interface > Color theme offers four brightness themes, as Photoshop does. One token set carries all four values; **Dark is the default and the first theme** in `tokens.json`.

| Theme | `frame` | `surface-panel` | `surface-raised` | `surface-field` | `canvas-surround` | `text-primary` |
| --- | --- | --- | --- | --- | --- | --- |
| Dark (default) | #282828 | #323232 | #3A3A3A | #262626 | #1E1E1E | #E3E3E3 |
| Darkest | #151515 | #1E1E1E | #262626 | #121212 | #101010 | #DCDCDC |
| Medium Gray | #454545 | #535353 | #4C4C4C | #3E3E3E | #3B3B3B | #F5F5F5 |
| Light | #C4C4C4 | #D6D6D6 | #EBEBEB | #F7F7F7 | #A3A3A3 | #1A1A1A |

Layering keeps Bezier's crust, mantle and surface order, reorganized around Photoshop's anchors:

- `frame` (Bezier crust): title bar with the menu bar, document tab strip, status bar and the gaps between docked panels.
- `surface-panel` (mantle): panels, tool rail, options bar, the selected document tab.
- `surface-tabstrip`: panel tab strips, collapsed icon strips, the hint bar.
- `surface-raised`: anything that floats: menus, dropdowns, tooltips, dialogs, toasts. Always with `border-popup` and a shadow. In Medium Gray it is slightly darker than the panel, which keeps text and links above 4.5:1.
- `surface-field`: an inset well for text and number fields (near white in Light).
- `surface-control`, `-hover`, `-pressed`: button faces.
- `canvas-surround`: the pasteboard, distinct from both `frame` and `surface-panel` in every theme so the document edge reads.
- `divider` for 1px hairlines between sections; `divider-strong` for toolbar, menu and status separators; `border-control` for the edge that identifies a field or checkbox (3:1 on panels).

### State color (Highlight) versus app accent

Two kinds of color appear in chrome, and they never swap roles.

**State** is the Highlight color, the same in every app: selection, keyboard focus, checked checkboxes and radios, the active tool, the highlighted menu item, slider fills, selected rows, drop targets, links. Tokens: `state` (solid fill that carries `state-on` text), `state-hover`, `state-pressed`, `state-on`, `state-subtle` (selected rows), `state-tint` (translucent checked-tool fill), `state-line` (marks that need 3:1: active tool border, slider fill, underline of the selected tab), `state-text` (links), and `focus-ring` (an alias of `state-line`).

**App accent** is identity only: Stilus cyan `accent-stilus`, Pinxit orange `accent-pinxit`, Albumen green `accent-albumen` (lighter values in the three dark themes, darker in Light). It appears on the title-bar app mark, the splash and its launch progress, and the single primary button of a view, with its label in `accent-<app>-on`. It never marks selection, focus or a checked state.

Examples:

- The selected layer in Pinxit is `state-subtle`; the dialog's OK button in the same window is `accent-pinxit`.
- The active Brush tool shows `state-tint`, a 1px `state-line` border and `glow-state`, in all three apps.
- The highlighted item in a menu is `state` with `state-on` text; the menu bar's app mark beside it is `accent-<app>`.
- Albumen's Import button is `accent-albumen`; the photos it selects in the grid are outlined in `state-line`.

### Highlight color option

Preferences > Interface > Highlight color offers three values. Every `state*` token, and `focus-ring`, `handle-stroke` and `glow-state` with them, follows the choice.

| Option | Values | Why |
| --- | --- | --- |
| **Blue (default)** | the `state*` tokens (#1473E6 family, tuned per theme) | Neutral on photographs and illustrations (few images are dominated by this blue); no clash with warning amber; the safest choice beside error red for color-blind users; clean in the Light theme; matches Photoshop, so it reads as "selected" without learning. |
| **Isotone orange** | the `state-orange*` tokens (Bezier's #FF6B35, darker in Light) | Isotone's Bezier heritage. The dark themes set near-black text on it (`state-orange-on`). |
| **Windows accent color** | derived from `UISettings` Accent and AccentLight1-3 / AccentDark1-3, contrast-adjusted per theme | Matches the rest of the user's Windows. Falls back to Blue when unavailable. |

The Highlight card documents the Windows accent mapping and the WPF swap. Two cautions come with the orange option:

- **Pinxit's identity orange sits close to Isotone orange.** `accent-pinxit` #F5923E and `state-orange` #FF6B35 differ by only 1.1 to 1.2:1 in lightness, so they cannot be told apart by lightness. Roles keep them apart: with the orange option, Pinxit's primary button keeps the identity orange while selected rows use `state-orange-subtle` (a brown tint at least 3:1 away from the button in every theme) and focus uses `state-orange-line`. Blue stays Pinxit's recommended Highlight.
- **Warning amber against Isotone orange.** `status-warning` (amber, #F2C14E in Dark) is 1.6 to 1.9:1 lighter than `state-orange` in the dark themes and differs in hue in Light (1.25:1). Warnings always carry the `alert` icon and a word, so they never depend on that difference.

### Status colors

`status-error`, `status-warning`, `status-success`, `status-info`, each with a `-subtle` fill for info bars and toast wells. They mean status only, never decoration, and always travel with an icon (`error`, `alert`, `success`, `info`) and a word. On a subtle fill the text is `text-primary`. Error and success are not separable by lightness alone (1.0 to 1.3:1), which is why the icon and word are mandatory. `status-info` is independent of the Highlight color.

### Canvas colors

`checker-light`/`checker-dark`, `guide`, `guide-smart`, `ants-light`/`ants-dark`, `handle-fill`, `artboard` are the same in all themes: they sit on artwork, not chrome. `handle-stroke` follows the Highlight color.

## Typography

Segoe UI Variable, falling back to Segoe UI and system-ui: the Windows 11 system face, so nothing ships or loads. Segoe UI Variable Display for the splash only. Mono: Cascadia Mono, then Consolas.

| Style | Size / line | Weight | Use |
| --- | --- | --- | --- |
| `caption` | 11 / 14 | 400 | status bar, number box values, tooltip descriptions, helper lines |
| `body` | 12 / 16 | 400 | menus, labels, rows, buttons, options bar |
| `body-strong` | 12 / 16 | 600 | tooltip titles, the selected document tab, lead words in info bars, primary buttons |
| `section-header` | 11 / 14, +0.04em, capitals | 600 | panel section headers (Bezier's ALL CAPS SemiBold, in `text-secondary`) |
| `title` | 14 / 20 | 400 | flyout and empty-state headings |
| `dialog-title` | 14 / 20 | 600 | dialog titles |
| `display` | 46 / 56, -0.5px | 600 | splash app name only (the Suite card) |
| `mono` | 11 / 14 | 400 | status bar coordinates, pixel readouts |
| `mono-body` | 12 / 16 | 400 | hex values, logs |

Comfortable density swaps `caption`, `body` and `body-strong` for `caption-comfortable` (12/16), `body-comfortable` (13/18) and `body-strong-comfortable`; titles stay. The type scale ships in WPF as `FontSize` resources named `type-caption`, `type-body-compact`, `type-body-comfortable`, `type-title`.

Text rules: sentence case for buttons, labels and messages ("Save a copy"); title case for menu items and dialog titles, following Photoshop ("Image Size", "Convert to Smart Object"); an ellipsis on commands that open a dialog. Use "you" sparingly and never "we". No exclamation marks, no emoji. Numbers use the user's culture and tabular figures in readouts; units follow values with a space in prose ("1.9 GB") and without in fields (the unit sits in its own column).

## Spacing and density

A 4px grid: `space-hair` 2, `space-1` 4, `space-1-5` 6, `space-2` 8, `space-3` 12, `space-4` 16, `space-6` 24. Bezier's paddings stay exact: toolbars 8,4; options and status bars 12,4; hint bar 12,6; panel header 12,10; panel body 12,8; fields 8,6; tooltips 10,6.

Two densities, chosen in Preferences > Interface > UI density. Compact is the default.

| Size token pair | Compact | Comfortable |
| --- | --- | --- |
| `control-h-*` (buttons, fields, combos) | 24 | 30 |
| `control-h-dialog` | 28 | 30 |
| `menu-row-h-*` | 24 | 30 |
| `optionsbar-h-*` | 32 | 40 |
| `doctab-h-*` | 28 | 32 |
| `tool-button-*` / `toolrail-w-*` | 32 / 40 | 40 / 48 |
| `panel-tab-h-*` | 26 | 32 |
| `row-h-*` | 22 | 28 |
| `layer-row-h-*` | 36 | 44 |
| `statusbar-h-*` | 22 | 26 |
| `check-size-*` | 14 | 16 |
| `swatch-*` | 16 | 20 |
| body text | 12 | 13 |
| icons in toolbars | 16 | 20 |

Fixed in both: `titlebar-h` 32, `caption-button-w` 46, `infobar-h` 28, `section-header-h` 28, `ruler-w` 18, `panel-w-default` 280 (260 to 300).

## Radii

Small and nearly square, from Bezier. `radius-sm` 2px for everything docked in the chrome (buttons, fields, checkboxes, tools, tabs, row highlights, tooltips, swatches); `radius-md` 4px for popups (menus, dropdowns, flyouts); `radius-lg` 6px for dialogs and toasts; `radius-round` for radio buttons, toggle switches, slider thumbs and status dots. Nothing else is rounded.

## Borders and elevation

Docked chrome is flat: regions are separated by 1px `divider` hairlines, never by shadows or gaps wider than 1px. Shadows are only for things that float:

- `shadow-tooltip` for tooltips (Bezier: blur 8, depth 2, 30%).
- `shadow-popup` for menus, dropdowns and flyouts.
- `shadow-dialog` for dialogs, toasts and floating panels.
- `glow-state` is not elevation: it is the soft zero-depth glow of a checked tool.

Shadows are darker and tighter in the dark themes and lighter in Light. Every floating surface also has a 1px `border-popup`.

## Motion

Bezier's timings with one curve, `ease-out` (cubic out):

- `duration-fast` 100ms: hover and press colors, checkbox and toggle transitions, scroll bar widening, thumb scale.
- `duration-standard` 200ms: menus and flyouts fading in, section expand and collapse, toasts sliding in 20px, the splash fading out when the main window is ready.
- `duration-slow` 400ms: dialogs popping in from scale 0.95. The splash's travelling border glow keeps Bezier's own timing: one lap per 6 s, fading in over 300ms and out over 500ms.
- `tooltip-delay` 400ms before a tooltip opens.

When Windows "Animation effects" is off (`SystemParameters.ClientAreaAnimation` false, or `UISettings.AnimationsEnabled` false), every duration is 0 and marching ants, spinners and indeterminate bars stop. Nothing in the chrome moves on its own otherwise.

## Iconography

One family: Lucide geometry (ISC), in the shared icon catalog as path data. 24 viewBox, `icon-stroke` 1.5px at `icon-sm` 16px (menus, panels, options bar, rows, buttons) and `icon-md` 20px (tool rail), round caps and joins, strokes only. Icons are `icon` at rest, `text-primary` when hovered or active, `state-on` on a `state` fill, `text-disabled` when disabled. FluentIcons.Wpf, which Bezier mixed in, leaves the suite; the caption buttons draw `minus`, `maximize`, `restore` and `x` from the same catalog at stroke 1. Emoji are never icons.

This UI icon catalog (Lucide-style strokes) is separate from the app icons. The app icons of Stilus, Pinxit and Albumen are Direction C, the suite tile: a shared graphite tile, the spectrum band along its foot and the app's accent glyph. They are drawn from their own SVG files, never from the catalog, and they appear in the taskbar, Start menu, installer, file associations, About dialog and the title-bar app mark (the hand-tuned `-16` file); the splash is the Suite card, which carries the master icon at 136 px (see the Splash component guide). Sizes, construction, colors and rules are in the App icons section, and the files are in the App icons asset group.

## Accessibility

### Contrast

Every text token is checked (WCAG 2.x) against every ground its usage note names, in all four themes: 352 pairs, all passing. Text needs 4.5:1; borders that identify a control, focus rings, icons and state marks need 3:1. A selection of the results:

| Pair | Dark | Darkest | Medium | Light |
| --- | --- | --- | --- | --- |
| `text-primary` on `surface-panel` | 10.0 | 12.2 | 7.1 | 12.0 |
| `text-primary` on `frame` | 11.5 | 13.3 | 8.8 | 10.0 |
| `text-secondary` on `surface-panel` | 5.9 | 6.8 | 5.5 | 7.2 |
| `text-secondary` on `surface-raised` | 5.2 | 6.2 | 6.1 | 8.8 |
| `text-placeholder` on `surface-field` | 4.5 | 4.6 | 5.4 | 5.0 |
| `state-on` on `state` | 4.5 | 4.5 | 5.4 | 4.5 |
| `state-text` on `surface-panel` | 5.3 | 6.0 | 4.9 | 4.8 |
| `state-line` (= `focus-ring`) on `surface-panel` | 5.0 | 5.1 | 4.6 | 4.0 |
| `state-line` on `surface-raised` | 4.5 | 4.6 | 5.2 | 4.8 |
| `border-control` on `surface-panel` | 3.5 | 3.4 | 3.0 | 3.7 |
| `state-orange-on` on `state-orange` | 6.5 | 6.5 | 7.1 | 5.7 |
| `state-orange-line` on `surface-panel` | 5.0 | 5.9 | 4.6 | 3.9 |
| `accent-pinxit-on` on `accent-pinxit` | 7.9 | 7.9 | 7.9 | 5.3 |
| `status-error` on `surface-panel` | 5.1 | 6.1 | 4.7 | 4.7 |

`text-disabled` sits near 2.3 to 2.6:1 on purpose (WCAG exempts inactive controls). The `state` fill itself is a surface, not a mark: in Medium Gray it is only 1.4:1 against the panel, so every checked control also draws a `state-line` border.

### Focus and keyboard

One focus ring (`focus-ring`, 2px, 1px outside; inset on rows), shown for keyboard focus only. F6 cycles the regions (tool rail, options bar, document, dock); Tab moves inside a region; every dialog is fully keyboard operable with Enter and Escape doing what their buttons say; menus have access keys; tool shortcuts never fire while a text field has focus. Every icon-only control has a tooltip naming the command and shortcut and an `AutomationProperties.Name`.

### Windows high contrast

When `SystemParameters.HighContrast` is true, Isotone.UI loads `Themes/HighContrast.xaml`, which maps tokens to system colors instead of the four themes:

| Tokens | SystemColors |
| --- | --- |
| `frame`, `surface-*`, `canvas-surround` | `WindowBrush` |
| `text-primary`, `text-secondary`, `icon`, `border-control`, `divider*` | `WindowTextBrush` |
| `text-disabled` | `GrayTextBrush` |
| `state`, `state-subtle`, `state-tint` | `HighlightBrush` |
| `state-on` | `HighlightTextBrush` |
| `state-line`, `focus-ring` | `HighlightBrush` (drawn 2px) |
| `state-text` | `HotTrackBrush` |
| buttons | `ControlBrush` / `ControlTextBrush` |

Accent and status fills are dropped in high contrast; status keeps its icon and word. The canvas keeps its own colors because it shows the user's content.

### Scaling

Every size token is in device-independent pixels. The UI is checked at 100, 150 and 200 percent: 1px hairlines use `SnapsToDevicePixels` and `UseLayoutRounding` so they stay one device pixel, icons are vector paths, the checkerboard and handles size by display scale, not zoom, and the Comfortable density is the recommended pairing for small high-DPI laptops.

## WPF implementation

`Isotone.UI` carries the system as resources:

```
Isotone.UI/
  Themes/
    (all generated from docs/design/tokens.json by scripts/generate-theme.py; never hand-edited)
    Tokens.xaml            sizes, spacing, radii, durations, font families (single values)
    Dark.xaml              color and shadow tokens, Dark values (default)
    Darkest.xaml
    MediumGray.xaml
    Light.xaml
    HighContrast.xaml      token keys mapped to SystemColors
    Highlight.Blue.xaml    Highlight overlay: Blue (default, maps state keys to the blue set)
    Highlight.Orange.xaml  Highlight overlay: Isotone orange (maps state keys to state-orange)
    Density.Compact.xaml   neutral size keys pointed at the -compact values (default)
    Density.Comfortable.xaml neutral size keys pointed at the -comfortable values
    Controls/*.xaml        one dictionary per control family (Button.xaml, Menu.xaml, NumberBox.xaml...)
  Icons/icons.json         the icon catalog
```

- **Brush keys are token names**: `<SolidColorBrush x:Key="surface-panel" Color="#323232"/>`. Size tokens are `sys:Double` (`control-h-compact`), radii are `CornerRadius` (`radius-sm`), spacing is `Thickness` or `sys:Double`, durations are `Duration` (`duration-fast`), `ease-out` is a `CubicEase` with `EasingMode="EaseOut"`.
- **Always `DynamicResource`** for colors, so a theme or Highlight change restyles open windows without a restart. `StaticResource` is fine for sizes.
- `ThemeService` swaps the brightness dictionary in `Application.Resources.MergedDictionaries` (index 1); `HighlightService` swaps the Highlight overlay after it (`Highlight.Blue.xaml`, `Highlight.Orange.xaml`, or a dictionary built at runtime from the Windows accent); `DensityService` swaps `Density.Compact.xaml` or `Density.Comfortable.xaml`, which point the neutral keys (`control-h`, `row-h`, `menu-row-h`...) at the `-compact` or `-comfortable` values.
- Each app sets `Isotone.App.Accent`, `AccentHover` and `AccentOn` to its `accent-<app>` brushes once at startup.
- Implicit styles cover every stock control a surface uses (Button, ToggleButton, RepeatButton, CheckBox, RadioButton, TextBox, PasswordBox, ComboBox, ListBox, ListView, TreeView, TabControl, Menu, ContextMenu, ToolTip, ScrollBar, ScrollViewer, Slider, ProgressBar, StatusBar, Expander, GridSplitter); `FocusVisualStyle` is `{x:Null}` everywhere and templates draw the Isotone focus ring.
- AvalonDock gets an Isotone theme built from the same keys. No WPF-UI or other control framework.
- A surface never hardcodes a color, size or spacing that a token names; `tokens.json` in this system is the source for the XAML dictionaries.

## What changed from Bezier

| Bezier (Stilus prototype) | Isotone Interface |
| --- | --- |
| One pure-grey dark palette, inline in `MainWindowView.xaml` | Four brightness themes from one token set, in `Isotone.UI` dictionaries |
| Accent broken: grey #808080 with #FF6B35 orange leftovers | Blue Highlight color by default, Isotone orange (#FF6B35, tuned) and Windows accent as options; per-app identity accents kept separate |
| Title bar doubled: OS chrome plus a fake bar with emoji caption buttons | One custom title bar through WindowChrome: app mark, menu bar inside it, 46 x 32 caption buttons with a red close |
| Two icon families (FluentIcons.Wpf and Lucide-style, stroke 2) | One Lucide catalog, stroke 1.5 at 16 and 20px |
| Stock Menu, ContextMenu, ScrollBar, TextBox, ComboBox, Slider, TabControl, ListBox, TreeView | Every control styled, with hover, pressed, disabled and focus states |
| No disabled or keyboard focus visuals | One focus ring spec; disabled states everywhere |
| Sizes and radii drifting (28 to 34px buttons, mixed radii) | Size tokens with Compact and Comfortable pairs; radii 2, 4, 6 |
| Error toast as an orange fill | Neutral toast with a status icon and word; info bars in four severities |
| Kept | 2px radius, 1px hairlines, checked-tool tint + border + glow, rich tooltip with shortcut and 400ms delay, CompactNumberBox scrub label, context toolbar and hint bar, dense status bar with separators and mono coordinates, caps section headers, 100/200/400ms cubic-out motion |
