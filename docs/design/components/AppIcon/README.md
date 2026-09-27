# App icon

The app icons of Stilus, Pinxit and Albumen: Direction C, the suite tile, a shared graphite tile with the spectrum band along its foot and the app's accent glyph, in a 256 master and hand-tuned 16, 24 and 32 variants.

The full guide (construction, colors, pixel-grid rules, export) is the App icons section of the brand book; the files are the App icons asset group.

## Which file

| Rendered size | File |
| --- | --- |
| 16 and 20 px | `<app>-16.svg` |
| 24 and 30 px | `<app>-24.svg` |
| 32 to 40 px | `<app>-32.svg` |
| 48 px and up | `<app>.svg` |
| Splash (the Suite card) | the master at 136 px, on the card built in XAML (see Splash); `<app>-splash.svg` is the card's reference design and a marketing image, not an icon |

## Rules

- The title-bar app mark is `<app>-16.svg` at 16 px (20 px at 125 percent and up), drawn as is in the 40 px app mark zone.
- The About dialog shows the master at 128 px; taskbar, Start menu, installer and file associations take sizes from the generated `.ico`.
- Never recolor the glyph, never draw the master below 48 px, never add text, never drop the band, keep clear space of one eighth of the icon size.
- The icon keeps its own colors in every brightness theme and in high contrast; it is an image, not chrome.
- A catalog icon (`pen-tool`, `brush`, `aperture`) never stands in for an app icon.

## WPF

- `Window.Icon` and the title-bar mark take the app's `.ico` generated from these SVGs; the mark picks the frame the ladder names for the current DPI (16 at 100 percent, 20 at 125 percent, 24 at 150 percent), never a scaled master.
- `AutomationProperties.Name` on the title-bar mark is the app name ("Pinxit").
