# Stilus Standards

Stilus is the suite's vector editor. This file adds to [`shared.md`](shared.md) and never contradicts it. It replaces the imported `src/Stilus/STANDARDS.md` ("Bezier Coding Standards"), whose general C# and logging rules now live in `shared.md`.

## Projects

| Project | Holds | References |
| ------- | ----- | ---------- |
| `Isotone.Stilus.Core` (today `Bezier.Core`) | The document model (`VectorDocument`, `VectorElement` and the `Svg*` element types), commands, tools, services, SVG import and export | No WPF. SkiaSharp is allowed for geometry (`SKPath.Op`, measuring) |
| `Isotone.Stilus.Desktop` (today `Bezier.Desktop`) | The WPF app: views, view models, the Skia canvas, dialogs | `Isotone.Stilus.Core`, `Isotone.Core`, `Isotone.UI` |
| `tests/Isotone.Stilus.Tests` (today `src/Stilus/Bezier.Tests`) | xUnit tests for both | Both projects |

The executable is `Stilus.exe` (`AssemblyName` Stilus); settings and logs live under `%LOCALAPPDATA%\Rizonesoft\Stilus\`.

## The document model

- `VectorDocument` is the single source of truth. The canvas renders it; it never keeps a second copy of element state.
- Every mutation goes through an `IEditorCommand` recorded in the document's history, including drags: a drag records one command on mouse-up that captures the start and end state, so undo restores exactly the pre-drag geometry.
- Coordinates are document units (CSS pixels at 96 DPI) in `double`. Rounding happens only when writing a file, and the writer's precision is a named setting.
- Element identity is a `Guid` that survives save and reopen when the format can carry it (`id` attributes in SVG).

## SVG is the native format

- One reader (`SvgImporter`) and one writer (`SvgExporter`) own SVG. There is one render path: the document model through `SkiaRenderer`. No second SVG renderer (SharpVectors, Svg.Skia) ships in the app.
- Everything the reader does not understand is preserved or reported, never silently dropped. A round trip of a committed fixture is compared element by element (`testing.md`).
- Inkscape is the reference implementation: fidelity goldens are rendered by Inkscape, with its version recorded beside the fixture.

## Canvas and tools

- The canvas is `SkiaCanvas` (SkiaSharp.Views.WPF). Rendering allocates nothing per frame: paints, paths, and fonts are cached and invalidated by the document's change events.
- A tool derives from `ToolBase` and is registered in the tool manager through the composition root. It owns its cursor, its shortcut, and its on-canvas overlay, and it records its edits as commands.
- Modifier keys match the competitor norm: Shift constrains (angles to 15 degrees, proportions), Alt works from the center, Space pans temporarily.

## Icons

- Fluent UI System Icons, drawn through the shared icon catalog (`IconService`, `VectorIcon`, moving to `Isotone.UI`). The `FluentIcons.Wpf` control is used only where the catalog cannot yet draw an icon, and the plan retires it.
- 16 px in menus and panels, 20 px on the tool rail and toolbars (see the design contract).

## Debug tooling

The debug window (F12) is a developer surface: its console reads from the Serilog pipeline, never from a private logger with its own file. It ships in Release builds but is reachable only through its shortcut.
