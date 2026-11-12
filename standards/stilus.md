# Stilus Standards

Stilus is the suite's vector editor. This file adds to [`shared.md`](shared.md) and never contradicts it. Stilus is being built natively from its plan in `todo/02-stilus/`; the C# prototype it grew from (Bezier) is preserved at the `csharp-final` tag as a behavior reference (`git show csharp-final:<path>`), read to learn what a feature did and never extended.

## Code

| Folder | Holds | May use |
| ------ | ----- | ------- |
| `native/stilus/` core library (`isotone::stilus`) | The document model, commands, tools, the vector engine (geometry, paths, boolean operations), and the SVG reader and writer | `isotone::core`. No window header: it is tested without a window |
| `native/stilus/` executable (`stilus.exe`) | The app shell: its composition root, its surfaces built from `isotone::ui`, and the canvas | The core library, `isotone::core`, `isotone::ui` |
| `native/tests/stilus/` | The GoogleTest suites, fixtures, and fuzz corpora for both | Both |

Settings and logs live under `%LOCALAPPDATA%\Rizonesoft\Stilus\`.

## The document model

- The vector document is the single source of truth. The canvas renders it; it never keeps a second copy of element state.
- Every mutation goes through a command recorded in the document's history, including drags: a drag records one command when the pointer is released that captures the start and end state, so undo restores exactly the pre-drag geometry.
- Coordinates are document units (CSS pixels at 96 DPI) in `double`. Rounding happens only when writing a file, and the writer's precision is a named setting.
- Element identity is a stable id that survives save and reopen when the format can carry it (`id` attributes in SVG).
- Background work reads an immutable snapshot of the document and commits its result as a command on the UI thread only if the document is still at the version it started from ([`cpp.md`](cpp.md), "Ownership and lifetimes").

## SVG is the native format

- One reader and one writer own SVG, and there is one render path: the document model through the vector engine. No second SVG renderer ships in the app.
- The reader treats every byte as hostile ([`cpp.md`](cpp.md), "Untrusted input") and owes its fuzz target and regression corpus beside its round trip.
- Everything the reader does not understand is preserved or reported, never silently dropped. A round trip of a committed fixture is compared element by element ([`testing.md`](testing.md)).
- Inkscape is the reference implementation: fidelity goldens are rendered by Inkscape, with its version recorded beside the fixture.

## Canvas and tools

- The canvas is its own visual with its own swap chain, drawn by the vector engine through Direct2D geometry on the render thread from an immutable snapshot. Rendering allocates nothing per frame: geometry realizations, brushes, and text layouts are cached and invalidated by the document's change events, and every GPU resource is rebuilt after device loss.
- A tool is registered once in the composition root. It owns its cursor, its shortcut (through the command registry), and its on-canvas overlay, and it records its edits as commands.
- Modifier keys match the competitor norm: Shift constrains (angles to 15 degrees, proportions), Alt works from the center, Space pans temporarily. Menus, tools, panels, dialogs, and their terms sit where an Illustrator user expects them, by the layout map Stilus's sections cite (`D01 T13`).

## Icons

- One icon family, drawn through the shared icon catalog of `isotone::ui` (Lucide geometry, `docs/design/components/Icons/README.md`). No second family and no icon control from outside the suite.
- 16 px in menus and panels, 20 px on the tool rail and toolbars (see the design contract).

## Debug tooling

The debug window (F12) is a developer surface: its console reads from the app's structured log, never from a private logger with its own file. It ships in Release builds but is reachable only through its shortcut.
