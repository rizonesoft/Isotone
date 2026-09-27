# Architecture

How the Isotone Graphics Suite is put together: the applications, the shared libraries, the rules that keep them independent, and where the code is going. The build itself is described in [build.md](build.md) and versioning in [versioning.md](versioning.md). The live plan is [`todo/`](../../todo/TODO-00-INDEX.md).

## The application family

Isotone is a family of standalone creative applications for Windows. They are developed together in one repository and distributed separately.

| App | Kind | Role | Focus | Formats it owns |
| --- | ---- | ---- | ----- | --------------- |
| **Stilus** | Vector editor (Illustrator alternative) | Structure and design | Precision illustration, typography, logos, scalable graphics | `.svg` first; PDF and raster export; `.eps` and `.ai` import are roadmap items |
| **Pinxit** | Raster editor (Photoshop alternative) | Creation and manipulation | Painting, retouching, layer composition, pixel editing | `.png`, `.jpg`, `.tiff`, a native layered format, `.psd` read |
| **Albumen** | Digital darkroom and asset manager (Lightroom alternative) | Development and organization | RAW processing, non-destructive editing, batch work, the photo library | Camera RAW and DNG in; JPEG, TIFF, PNG out |

Albumen is the bridge from the camera to Pinxit: "Edit in Pinxit" hands a rendered image to Pinxit when Pinxit is installed, and refuses by name when it is not.

## Develop together, distribute separately

- **One repository, one solution** (`Isotone.slnx`), one set of gates, one plan.
- **Each app ships alone:** its own installer, its own install folder, its own copy of every shared library, its own version tag (`stilus-v*`, `pinxit-v*`, `albumen-v*`), its own changelog, its own user guide. A suite bundle (`isotone-v*`) packages a set of app versions without changing any of them.
- **No runtime dependency between apps.** An app may *offer* a hand-off to another (Albumen's "Edit in Pinxit"), but it must work, and say so plainly, when the other app is absent. An update to Pinxit can never break an installed Stilus, because nothing is shared on disk.

## Target layout

The imported trees still use their legacy names; the plan renames them in its first app phase (`todo/02-stilus/TODO-01-stilus-structure.md` and `todo/03-pinxit/TODO-01-pinxit-structure.md`). The layout they converge on:

```
src/
  Isotone.Core/                  shared non-UI library (net11.0)
  Isotone.UI/                    shared WPF library (net11.0-windows10.0.26100.0)
  Stilus/
    Isotone.Stilus.Core/          document model, tools, commands, SVG I/O
    Isotone.Stilus.Desktop/       WPF app, AssemblyName Stilus (Stilus.exe)
  Pinxit/
    Isotone.Pinxit.Core/          document, layers, tiles, history, color
    Isotone.Pinxit.Rendering/     render graph, compositing, GPU path
    Isotone.Pinxit.FileFormats/   codecs and the native format
    Isotone.Pinxit.Desktop/       WPF app, AssemblyName Pinxit (Pinxit.exe)
  Albumen/
    Isotone.Albumen.Core/          catalog, import, RAW decode, develop pipeline
    Isotone.Albumen.Desktop/       WPF app, AssemblyName Albumen (Albumen.exe)
    Isotone.Albumen.Viewer/        fast default viewer, AssemblyName AlbumenViewer (AlbumenViewer.exe), shipped only inside the Albumen install
tests/
  Isotone.Core.Tests/  Isotone.UI.Tests/  Isotone.Stilus.Tests/
  Isotone.Pinxit.Core.Tests/  Isotone.Pinxit.Rendering.Tests/  Isotone.Albumen.Tests/
  fixtures/<app>/               committed fixtures for format fidelity proofs
```

Namespaces follow the project names: `Isotone.Stilus.*`, `Isotone.Pinxit.*`, `Isotone.Albumen.*`, `Isotone.Core.*`, `Isotone.UI.*`.

## The shared libraries

### Isotone.Core

A UI-agnostic class library. It holds only behavior that **two apps need now**; one app's need stays in that app with a note naming the day it would move, and an `Isotone.Core` type that only one app consumes is a defect. The plan moves these in as the second consumer arrives:

- App-data paths and the Serilog bootstrap (both apps log today, differently).
- The settings store: atomic JSON settings with defaults and a readback.
- Single instance and file-open forwarding.
- The command and undo history both editors need.
- The atomic document writer every save path uses.
- The update check (all apps).

Candidates that stay in their app until a second app needs them: color science and ICC handling (Pinxit today, Albumen later), the tiled image store (Pinxit), the RAW decoder (Albumen; Pinxit's RAW import is the day it moves), geometry and vector math (Stilus).

### Isotone.UI

A WPF class library for the house style, so the three apps look and behave like one suite without WPF-UI or any other UI framework. It starts with what Stilus and Pinxit already duplicate (`VectorIcon`, `IconService`, `BorderGlowAnimator`, the splash window, the exception window) and the theme resources the design contract in [`standards/shared.md`](../../standards/shared.md) names.

### What neither library does

Neither holds a document model, a tool, or a format specific to one app. The rendering pipelines differ on purpose: Stilus renders a vector scene graph through SkiaSharp; Pinxit composites tiled raster layers through SkiaSharp with a ComputeSharp GPU path; Albumen runs a floating-point develop pipeline.

## Inside an app

Every app has the same skeleton, set by [`standards/shared.md`](../../standards/shared.md):

- **Composition root:** one `Microsoft.Extensions.Hosting` host per app, services registered once, constructor injection everywhere, no static service locator.
- **MVVM:** CommunityToolkit.Mvvm (`ObservableObject`, `[ObservableProperty]`, `[RelayCommand]`). Logic lives in view models and services; code-behind is for view-only concerns.
- **Logging:** Serilog, configured through `Isotone.Core`, writing to `%LOCALAPPDATA%\Rizonesoft\<App>\logs\`, one structured line per action that changes a document or a setting.
- **Documents:** every edit is an undo step; saves are atomic (write a temporary file beside the target, flush, replace); autosave and recovery never overwrite the user's file.
- **Surfaces:** standard WPF controls with the suite theme; every icon-only control has a tooltip and an automation name.

## Development goals

1. **Performance:** lightweight execution and fast startup over feature bloat; each feature names its budget on a large document.
2. **Interoperability:** "Edit in" hand-offs between the apps, over files, never over shared runtime state.
3. **Extensibility:** a plugin surface where it earns its place (Pinxit's filter plugins first), designed per app until a second app needs the same contract.

## Decisions

Recorded decisions with their evidence and cost of change live in [decisions.md](decisions.md) once the first one is written (`todo/00-workspace/TODO-02-build-and-test-debt.md` §5 creates it).
