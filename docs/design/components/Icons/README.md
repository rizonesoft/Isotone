# Icons

The suite draws every icon from one family: Lucide geometry (ISC license, compatible with GPL-3.0), stored as path data in the shared icon catalog. The survey found FluentIcons.Wpf mixed with Lucide-style paths; FluentIcons.Wpf leaves the suite.

## Rules

- Grid: 24 viewBox, stroke `icon-stroke` 1.5px at both 16 and 20px, round caps and joins, no fills (a filled shape is drawn as a closed stroke).
- Sizes: `icon-sm` 16px in menus, panels, the options bar, list rows and buttons; `icon-md` 20px on the tool rail and in Comfortable toolbars; 12 to 14px only for chevrons and inline glyphs, with stroke 2 so they hold weight.
- Color: `icon` (= `text-secondary`) at rest, `text-primary` on hover or when active, `state-on` on a `state` fill, `text-disabled` when disabled, a status color only next to status text. Icons never take the app accent except inside the app mark.
- Every icon-only control has a tooltip and an `AutomationProperties.Name`; decorative icons are hidden from UIA.
- New icons: take Lucide's if one exists; otherwise draw one on the same grid (2px padding, 1.5 stroke) and add it to the catalog with a name and a note.
- Tool icons match the tool, not the command (Photoshop's names for Photoshop tools).
- The app marks (pen nib, paintbrush, aperture) are the apps' own icon files, not catalog icons.

## Catalog (preview names)

The preview renders every icon the system currently documents. Names are the catalog keys: `pointer` (Move tool), `marquee`, `lasso`, `wand`, `crop`, `pipette`, `brush`, `pencil`, `eraser`, `stamp`, `bucket`, `pen-tool`, `type`, `square`, `circle`, `hand`, `zoom-in`, `zoom-out`, plus panel, file, edit, status and window glyphs.

## WPF

`Isotone.UI.Icons`: an `IconCatalog` singleton loaded from `icons.json` (name to path data, source-generated JSON context), an `Isotone.Icon` control (`Path` with `Stretch="Uniform"` inside a 24-unit `Viewbox`, `StrokeThickness` scaled so 1.5 at 24 stays 1.5 device-independent pixels at 16 and 20, `StrokeStartLineCap`/`EndLineCap`/`LineJoin` round), and a markup extension `{ph:Icon brush}`. `Foreground` drives the stroke through `TemplateBinding`.
