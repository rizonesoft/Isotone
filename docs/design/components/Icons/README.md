# Icons

The suite draws every icon from one family: Lucide geometry (ISC license, compatible with GPL-3.0), stored as path data in the shared icon catalog. The survey of the prototypes found a second icon family mixed with Lucide-style paths; it left the suite with them, and no second family is used.

## Rules

- Grid: 24 viewBox, stroke `icon-stroke` 1.5px at both 16 and 20px, round caps and joins, no fills (a filled shape is drawn as a closed stroke).
- Sizes: `icon-sm` 16px in menus, panels, the options bar, list rows and buttons; `icon-md` 20px on the tool rail and in Comfortable toolbars; 12 to 14px only for chevrons and inline glyphs, with stroke 2 so they hold weight.
- Color: `icon` (= `text-secondary`) at rest, `text-primary` on hover or when active, `state-on` on a `state` fill, `text-disabled` when disabled, a status color only next to status text. Icons never take the app accent except inside the app mark.
- Every icon-only control has a tooltip and a UI Automation Name; decorative icons are hidden from UI Automation.
- New icons: take Lucide's if one exists; otherwise draw one on the same grid (2px padding, 1.5 stroke) and add it to the catalog with a name and a note.
- Tool icons match the tool, not the command (Photoshop's names for Photoshop tools).
- The app marks (Bezier curve, paintbrush, iris) are the apps' own icon files, not catalog icons.

## Catalog (preview names)

The preview renders every icon the system currently documents. Names are the catalog keys: `pointer` (Move tool), `marquee`, `lasso`, `wand`, `crop`, `pipette`, `brush`, `pencil`, `eraser`, `stamp`, `bucket`, `pen-tool`, `type`, `square`, `circle`, `hand`, `zoom-in`, `zoom-out`, plus panel, file, edit, status and window glyphs.

## Native

`isotone::ui` holds one icon catalog, loaded once from `icons.json` (name to path data), and an icon element that realizes the path as Direct2D geometry in the 24-unit box, scaled uniformly, with the stroke width scaled so 1.5 at 24 stays 1.5 device-independent pixels at 16 and 20, and round caps and joins. The stroke color is the element's foreground token.
