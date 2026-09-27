# Lumen Standards

Lumen is the suite's digital darkroom and photo library. This file adds to [`shared.md`](shared.md) and never contradicts it. Lumen has no code yet; its plan is `todo/04-lumen/`, and this file is the contract that plan builds to.

## Projects

| Project | Holds |
| ------- | ----- |
| `Photon.Lumen.Core` | The catalog, import, metadata, the RAW decoder adapter, the develop pipeline, export |
| `Photon.Lumen.Desktop` | The WPF app; `AssemblyName` Lumen (`Lumen.exe`) |
| `Photon.Lumen.Viewer` | The fast default image viewer; `AssemblyName` LumenViewer (`LumenViewer.exe`), a second executable with its own minimal startup path and a recorded startup budget (`D04 T04 §1`), shipped only inside the Lumen installer and portable ZIP and versioned with Lumen |
| `tests/Photon.Lumen.Tests` | xUnit tests, including develop-pipeline goldens |

Settings, logs, the catalog, and the preview cache live under `%LOCALAPPDATA%\Rizonesoft\Lumen\` by default; the catalog location is a setting.

## The original-file guard

**Lumen never writes an original image unless the user opts in**; a verified backup is taken by default before every in-place write (an optional backup copy: the user may turn it off only through a second confirmation). Originals are safe by default with opt-in writes (operator decision 2026-09-27, "Safe by default, opt-in writes"). This is a frozen behavior from the day the import path ships:

- Import reads originals; it copies them only when the user chose "copy", and a copy is verified by hash before the import records it.
- Edits are data: a develop setting stack stored in the catalog (and in an XMP sidecar when the user enables sidecars). Rendering applies the stack to a decoded original in memory.
- Metadata changes (rating, flag, label, keywords) go to the catalog and, when enabled, to a sidecar `<name>.xmp` beside the original, written atomically. They reach the original's own bytes only when the user turns on embedding (`Lumen.Originals.InPlace.EmbedMetadata`), and then only through the metadata-only rewriters of `D04 T08 §9`, which never re-encode pixels and verify the image data before replacing the file.
- Converted, resized, rotated, edited, and developed results are new files by default. The four opt-ins, each off by default, are the in-place kinds of one policy, `OriginalWritePolicy` in `D04 T11 §1`: embed metadata, rotate in place (lossless), save over the original (the viewer's Save and develop's Save to Original), and convert in place (batch). They are set on the Originals group of the File Handling preferences (`D04 T14 §10`), and an administrator can lock them off through the deployment overlay. No other key, policy, or writer may write an original.
- Every in-place write goes through `InPlaceWriter` (`D04 T11 §1`): the original is copied to the backup folder and the copy verified by SHA-256 (on by default; turning the backup off while an opt-in is on needs a second confirmation that the write cannot be undone), the new bytes are written through the suite atomic writer, the result is reread, and a journaled Restore Original from Backup is recorded. RAW files are never written.
- File operations the user asks for (rename, move, copy, delete to the Recycle Bin) are file operations, not image writes: they move the sidecar and any RAW+JPEG partner with the photo and are journaled for undo where the file system allows.
- Every code path that opens an original opens it read-only, except `InPlaceWriter` under the policy, and a test proves a full workflow (import, develop, export, metadata edit, batch, viewer) with every `Lumen.Originals.*` opt-in at its default leaves every fixture byte-identical.

## The catalog

- SQLite through `Microsoft.Data.Sqlite`, one file, versioned schema with forward-only migrations, each migration tested on a copy of the previous version's catalog.
- The catalog is a user document: writes are transactional, a crash never leaves it unopenable, and a backup is taken before a migration.
- Paths are stored relative to a root folder where possible so a moved library can be reconnected.
- A photo belongs to the catalog in one of two ways: `library` for imported photos and `browsed` for files Lumen has seen while browsing a folder without importing it (`D04 T05 §1`); browsed records are a cache keyed by path, size, and last-write time, and Add to Library turns them into library records in place.

## The develop pipeline

- Float32 linear-light working space from demosaic to output transform; the output transform converts to the export profile (sRGB, Display P3, Adobe RGB, or ProPhoto) once, at the end.
- Every operation is a pure function of its input and its settings, so a preview and an export of the same settings produce the same pixels within a stated tolerance.
- Previews render at screen resolution and are cancelled when the settings change; an export renders at full resolution.

## RAW decoding

The decoder library is a recorded decision (`docs/dev/decisions.md`) with its license checked against GPL-3.0, its camera coverage measured on a pinned sample set, and its output compared against a reference decoder (LibRaw's `dcraw_emu` or darktable) as a fidelity proof.

## Hand-offs

"Edit in Imago" writes a rendered 16-bit TIFF beside the catalog's working folder, starts Imago when it is installed, and imports the edited result as a new version stacked with the original. When Imago is not installed, the command is disabled with a tooltip saying so. Lumen never loads Imago's assemblies.
