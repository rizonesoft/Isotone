# Window chrome

The custom title bar every Photon document window draws: app mark in the app accent, the menu bar inside the title bar (as Photoshop does), a drag area, and the three Windows 11 caption buttons. There is one title bar per window; the OS frame is removed, never doubled.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Bar | full width x `titlebar-h` (32px) | fill `frame`, 1px `divider` under it only when the options bar is hidden |
| App mark | 40px zone, the app icon at 16px (20px at 125 percent scale and up) | the hand-tuned `<app>-16.svg` from the App icons group, drawn as is: never recolored, never a catalog glyph |
| Menu bar | titles 24px tall, 8px side padding | see Menu |
| Drag area | the remaining width | `frame` |
| Caption buttons | `caption-button-w` x `titlebar-h` (46 x 32) | glyphs 10px drawn from the icon catalog at stroke 1 in `text-primary` |

The document name is not repeated in the title bar: the document tabs carry it. With no document open, the drag area shows the app name in `text-secondary`.

## States

- Caption button: rest (transparent), hover `surface-control-hover`, pressed `surface-control-pressed`, keyboard focus (focus ring inset).
- Close: hover `caption-close-hover` with the glyph in `caption-close-on`, pressed `caption-close-pressed`. Never tinted by the Highlight color or the app accent.
- Maximized: the maximize glyph becomes restore; the bar keeps 32px and gains a 7px top inset handled by WindowChrome (no content under the screen edge).
- Inactive window: menu titles, title text and caption glyphs go to `text-disabled`; the app icon stays in full color, as Windows draws app icons in inactive windows.

## Keyboard

- Alt or F10 moves focus to the first menu title and shows access-key underlines; Alt+letter opens that menu.
- Alt+Space opens the system menu (Restore, Move, Size, Minimize, Maximize, Close).
- Caption buttons are not tab stops; they stay reachable through the system menu.

## WPF

- `Window` with `WindowChrome` (`CaptionHeight` = 32, `ResizeBorderThickness` = 6, `GlassFrameThickness` = 0 on Windows 10, -1 to keep the Windows 11 rounded corners and snap shadow, `UseAeroCaptionButtons` = False).
- Every interactive element in the bar sets `WindowChrome.IsHitTestVisibleInChrome="True"`.
- Caption buttons are `Button`s styled `Photon.CaptionButton` / `Photon.CaptionCloseButton`; the maximize button returns `HTMAXBUTTON` from a `WM_NCHITTEST` hook so Windows 11 Snap Layouts open on hover.
- `AutomationProperties.Name`: "Minimize", "Maximize" / "Restore", "Close".
- Brushes: `{DynamicResource frame}`, `{DynamicResource caption-close-hover}` and so on: brush keys are token names.
- Watch `IsActive` with a `DataTrigger` for the inactive state.
