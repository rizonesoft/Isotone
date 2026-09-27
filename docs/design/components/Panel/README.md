# Panel

Docked panels in the right dock: a tab strip of grouped panels, a panel menu, collapsible sections, and a collapsed icon-strip form.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Dock | `panel-w-default` 280px (min `panel-w-min` 260, default max `panel-w-max` 300; user resizable) | panels `surface-panel` separated by 1px `divider` over `frame` |
| Tab strip | `panel-tab-h-compact` 26px (Comfortable 32px) | `surface-tabstrip`, 1px `divider` below |
| Panel tab | 12px side padding, `body` | inactive `text-secondary`; selected `surface-panel` + `text-primary` joined to the body |
| Strip tools | 20px subtle icon buttons: collapse (`chevrons-right`), panel menu (`menu`) | `icon` |
| Section header | `section-header-h` 28px, 12px chevron, caps `section-header` | `text-secondary`, hover `text-primary`; optional count right aligned |
| Section body | 12px sides, 4px top, 12px bottom, 8px row gap | property rows: 60px label column in `text-secondary` |
| Icon strip (collapsed) | `panel-iconstrip-w` 36px, 28px buttons | as tool buttons; the open panel's button is checked |

## Behavior

- Section expanded state persists per panel in settings.
- Collapsing the dock turns each panel group into its icons; clicking one flies the panel out over the canvas (with `shadow-popup`), clicking elsewhere closes it.
- Panels float by dragging the tab out; floating panels use `surface-raised` with `shadow-dialog` and a 20px caption strip.
- Nothing inside a panel is louder than the canvas: no fills beyond `surface-panel`, no accent color.

## Keyboard

F6 reaches the dock; Ctrl+Tab inside a panel group moves between tabs; section headers are buttons (Enter or Space toggles, `aria-expanded`); the panel menu opens with Shift+F10 on the tab.

## WPF

AvalonDock (`LayoutAnchorablePane`) with a Isotone theme dictionary replacing `AnchorablePaneTitle` and `AnchorablePaneTabPanel` templates; outside AvalonDock, `Isotone.PanelHost` (`TabControl` + `ItemsControl`). Section: `Expander` styled `Isotone.SectionExpander` (Bezier CollapsibleHeader), header template with a rotating 12px chevron (`duration-standard`, `ease-out`). Property rows: `Grid` with `ColumnDefinition Width="60"` shared by `Grid.IsSharedSizeScope`.
