# Splash

The Suite card: the window each app shows while it starts (operator decision 2026-09-27). A graphite card with the app icon on a soft accent halo, the app name, its role, the suite and version line, a live status line and launch progress, and the spectrum band as a gentle wave along the bottom edge. It is the same card in Stilus, Pinxit and Albumen; only the icon, the accent, the name, the role and the status text differ.

The reference design is `resources/icons/<app>/<app>-splash.svg` (640 x 360), also used as a marketing image. In the app the card is built in XAML to this spec, never shown as a picture, so the version, the status and the progress are live.

## Anatomy

All positions are in DIPs on the 640 x 360 card, origin top left; text positions are baselines, as in the reference SVG.

| Part | Geometry | Values |
| --- | --- | --- |
| Card | 640 x 360, radius 8 | vertical gradient #303136 (top) to #1A1B1E (bottom) |
| Inner highlight | 1px stroke inset 0.5, radius 7.5 | white at 8 percent |
| Halo | circle centred (128, 160), radius 150, clipped to the card | radial `accent-<app>` at 20 percent opacity fading to 0 |
| App icon | 136 x 136 at x 56, y 92 | the Direction C master `<app>.svg` (or its generated `PNG/<app>_256.png`), as is |
| App name | x 228, baseline 148 | Segoe UI Variable Display 46px semibold (600), letter spacing -0.5px, #F4F4F5 |
| Role | x 230, baseline 178 | 16px regular, #B7B8BD: "Vector editor", "Raster and photo editor", "Digital darkroom and photo manager" |
| Suite and version | x 230, baseline 212 | 13px regular, #8C8D93: "Isotone Graphics Suite · Version 0.1.0", the middle dot in #6C6D73 |
| Status line | x 230, baseline 272 | Segoe UI Variable Text 12px regular, #A3A4AA, one line, trimmed with an ellipsis |
| Progress track | 340 x 3 at x 230, y 284, radius 1.5 | #3A3B41 |
| Progress fill | from x 230, same height and radius | `accent-<app>` |
| Copyright | right edge x 610, baseline 312 | 11px regular, #6E6F75: "© 2026 Rizonetech (Pty) Ltd · Free and open source (GPL-3.0)" |
| Spectrum band | path `M0 340C140 330 250 352 380 341S560 326 640 332V360H0Z`, clipped to the card | horizontal gradient x 0 to 640, the seven suite stops of the app icons |
| Band crest | the same curve as a stroke, 1.5px | white at 35 percent |
| Border glow | a highlight travelling around the card edge, 1.5px | `accent-<app>` |

Layout grid: a left column for the icon (x 56 to 192, centred on y 160) and a text column from x 230 to the right margin at x 610; the name, role and version block sits above the status and progress block, and the copyright closes the text column above the band.

## Colors

- The accent is `accent-<app>` (Stilus #29C5E6, Pinxit #F5923E, Albumen #4CC47A), the dark-theme value in every theme: the card is always graphite.
- The card greys (#303136, #1A1B1E, #F4F4F5, #B7B8BD, #8C8D93, #6C6D73, #A3A4AA, #3A3B41, #6E6F75) have no token: they are the splash's own palette, matched to the app icon tile. The card looks the same in every brightness theme, like the app icon.
- Spectrum stops at 0, 0.167, 0.333, 0.5, 0.667, 0.833 and 1: #FF4D6D, #FF9A3C, #FFD84A, #4CC47A, #29C5E6, #5B7CFF, #B45CFF.
- High contrast: the card fill is the system Window color, every text and the 1px border the system WindowText color, the progress fill the system Highlight color; the halo, the band crest and the glow are dropped; the icon and the band stay, as images.

## Behaviour

- Show the splash as the first thing the process draws, on its own UI thread, centred on the monitor that holds the cursor.
- Status and progress are live: each startup step sets the status line ("Loading tools…", "Loading brushes…", "Opening the catalog…") and advances the fill by its share of the steps. The bar is always determinate.
- The fill width change animates over `duration-fast` 100ms with `ease-out`; it jumps when animations are off.
- The border glow is Bezier's `BorderGlowAnimator` in `accent-<app>`: one lap around the card every 6 seconds while loading, fading in over 300ms and out over 500ms when loading ends. When Windows animation effects are off there is no glow at all.
- Timing: the splash stays until the main window is ready (loaded and rendered once), then fades out over `duration-standard` 200ms while the main window shows. There is no minimum display time and no artificial delay; with animations off it closes at once.
- A startup failure closes the splash before the exception window opens.

## Rules

- Never ship the reference SVG, or a PNG of it, as the splash: the text would be frozen.
- The version is the app's own informational version without the build metadata ("Version 0.1.0", "Version 0.2.0-beta.1").
- The status line is sentence case, ends with an ellipsis while working, and names what is loading, never a file path or a percentage.
- No buttons, no links, no close box, no tips carousel.
- The accent appears only on the halo, the progress fill and the glow; the icon keeps its own colors.

## Keyboard

Not focusable and takes no input. Screen readers get the window name ("Stilus is starting"), the status line as a polite live region, and the progress through UIA `RangeValue`.

## WPF

`Isotone.UI` `SplashWindow` (`WindowStyle="None"`, `AllowsTransparency="True"`, `ShowInTaskbar="False"`, `Topmost="True"`, `ResizeMode="NoResize"`), a 640 x 360 `Grid` clipped to a radius 8 `RectangleGeometry`, drawn from an `AppIdentity` (name, role, version, icon, accent). The card greys are named brushes in the window's own resources, not in the theme dictionaries. The icon is an `Image` of the app's generated `PNG/<app>_256.png` (or a `DrawingImage` of the master) at 136 x 136 with `RenderOptions.BitmapScalingMode="HighQuality"`; the band is a `Path` with the geometry above and a `LinearGradientBrush` in absolute units. The progress is a `ProgressBar` restyled to the 3px track. The glow is `BorderGlowAnimator` on a 1.5px `Rectangle` stroke with `RadiusX`/`RadiusY` 8. The check is a capture of the running window at 100 percent, compared against the render of `<app>-splash.svg` at 640 x 360: same positions and colors, apart from the live status text and progress.
