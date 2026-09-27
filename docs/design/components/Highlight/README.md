# Highlight color

The state color (selection, focus, checked controls, active tool, highlighted menu item, slider fill, selected rows, links) is a user choice in Preferences > Interface > Highlight color. Blue is the default.

## Options

| Option | Source | Notes |
| --- | --- | --- |
| Blue (default) | the `state*` tokens | Photoshop-like; neutral on photographs, never confused with warning amber or error red |
| Photon orange | the `state-orange*` tokens (Bezier #FF6B35) | the dark themes put near-black text on orange (`state-orange-on`); Light uses a darker orange with white |
| Windows accent color | `UISettings.GetColorValue` Accent, AccentLight1-3, AccentDark1-3 | contrast-adjusted per theme; the preview uses the Windows default #0078D4 as the example |

Each option supplies the whole set: `state`, `state-hover`, `state-pressed`, `state-on`, `state-subtle`, `state-tint`, `state-line`, `state-text`, plus `focus-ring`, `handle-stroke` and `glow-state`, which follow.

## Windows accent mapping

| Token | Dark, Darkest | Medium Gray | Light |
| --- | --- | --- | --- |
| `state` | Accent (AccentDark1 if `state-on` would fall under 4.5:1) | AccentDark1 | AccentDark1 |
| `state-hover` / `state-pressed` | AccentDark1 / AccentDark2 | AccentDark2 / AccentDark3 | AccentDark2 / AccentDark3 |
| `state-line`, `focus-ring` | AccentLight2 (Light1 in Darkest) | AccentLight3 | AccentDark1 |
| `state-text` | AccentLight2 | AccentLight3 | AccentDark2 |
| `state-subtle` | Accent blended 30% over `surface-panel` | 35% | 25% over white |
| `state-tint` | Accent at 20% alpha | 25% | 18% |

After mapping, each value is checked against the same pairs as the blue set (4.5:1 text, 3:1 marks); a value that misses is stepped in OKLCH lightness (lighter in dark themes, darker in Light) until it passes. `state-on` is white or `#141414`, whichever contrasts more with `state`.

## WPF

The four brightness dictionaries hold the blue values. A fifth merged dictionary, the Highlight overlay, is swapped at runtime by `HighlightService`: `Highlight.Blue.xaml` for Blue, `Highlight.Orange.xaml` (each `state` key mapped to its `state-orange` brush) for Photon orange, and for Windows accent a dictionary of brushes computed from `Windows.UI.ViewManagement.UISettings` (WinRT projection, available with the `net11.0-windows10.0.26100.0` target). The service subscribes to `UISettings.ColorValuesChanged` (raised on a worker thread: marshal to the dispatcher) and rebuilds the dictionary live. If the call throws or returns no accent, it falls back to Blue and logs a Warning. `SystemParameters.WindowGlassColor` is not used: it reports the glass color, not the accent. Every consumer uses `DynamicResource`, so swapping the dictionary restyles open windows without a restart.
