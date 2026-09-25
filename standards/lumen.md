# Lumen Standards

Lumen is the suite's digital darkroom and photo library. This file adds to [`shared.md`](shared.md) and never contradicts it. Lumen has no code yet; its plan is `todo/04-lumen/`, and this file is the contract that plan builds to.

## Projects

| Project | Holds |
| ------- | ----- |
| `Photon.Lumen.Core` | The catalog, import, metadata, the RAW decoder adapter, the develop pipeline, export |
| `Photon.Lumen.Desktop` | The WPF app; `AssemblyName` Lumen (`Lumen.exe`) |
| `tests/Photon.Lumen.Tests` | xUnit tests, including develop-pipeline goldens |

Settings, logs, the catalog, and the preview cache live under `%LOCALAPPDATA%\Rizonesoft\Lumen\` by default; the catalog location is a setting.

## The original-file guard

**Lumen never writes an original image.** This is a frozen behavior from the day the import path ships:

- Import reads originals; it copies them only when the user chose "copy", and a copy is verified by hash before the import records it.
- Edits are data: a develop setting stack stored in the catalog (and in an XMP sidecar when the user enables sidecars). Rendering applies the stack to a decoded original in memory.
- Metadata changes (rating, flag, label, keywords) go to the catalog and, when enabled, to a sidecar `<name>.xmp` beside the original, written atomically. Never into the original's own bytes.
- Every code path that opens an original opens it read-only, and a test proves a full workflow (import, develop, export, metadata edit) leaves every fixture byte-identical.

## The catalog

- SQLite through `Microsoft.Data.Sqlite`, one file, versioned schema with forward-only migrations, each migration tested on a copy of the previous version's catalog.
- The catalog is a user document: writes are transactional, a crash never leaves it unopenable, and a backup is taken before a migration.
- Paths are stored relative to a root folder where possible so a moved library can be reconnected.

## The develop pipeline

- Float32 linear-light working space from demosaic to output transform; the output transform converts to the export profile (sRGB, Display P3, Adobe RGB, or ProPhoto) once, at the end.
- Every operation is a pure function of its input and its settings, so a preview and an export of the same settings produce the same pixels within a stated tolerance.
- Previews render at screen resolution and are cancelled when the settings change; an export renders at full resolution.

## RAW decoding

The decoder library is a recorded decision (`docs/dev/decisions.md`) with its license checked against GPL-3.0, its camera coverage measured on a pinned sample set, and its output compared against a reference decoder (LibRaw's `dcraw_emu` or darktable) as a fidelity proof.

## Hand-offs

"Edit in Imago" writes a rendered 16-bit TIFF beside the catalog's working folder, starts Imago when it is installed, and imports the edited result as a new version stacked with the original. When Imago is not installed, the command is disabled with a tooltip saying so. Lumen never loads Imago's assemblies.
