# Window chrome

The custom title bar every Isotone document window draws: app mark in the app accent, the menu bar inside the title bar (as Photoshop does), a drag area, and the three Windows 11 caption buttons. There is one title bar per window; the OS frame is removed, never doubled.

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

## Native

- A Win32 window whose frame `isotone::ui` draws itself: the DWM frame is extended into the client area (`DwmExtendFrameIntoClientArea`) and `WM_NCCALCSIZE` removes the system caption, with a 32px caption area and a 6px resize border, keeping the Windows 11 rounded corners and snap shadow.
- Non-client hit testing (`WM_NCHITTEST`) returns `HTCAPTION` for the drag area and `HTCLIENT` for every interactive element in the bar.
- Caption buttons are caption button elements (the close one with its own style); the maximize button returns `HTMAXBUTTON` from `WM_NCHITTEST` so Windows 11 Snap Layouts open on hover.
- UI Automation Names: "Minimize", "Maximize" / "Restore", "Close".
- Colors: `frame`, `caption-close-hover`, and so on: the keys are token names.
- The inactive state follows `WM_ACTIVATE`.
