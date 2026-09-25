# Shared Standards

Cross-cutting standards for every app in the Rizonesoft Graphics Suite (Nodus, Imago, Lumen) and for `Photon.Core` and `Photon.UI`. App files ([`nodus.md`](nodus.md), [`imago.md`](imago.md), [`lumen.md`](lumen.md)) add to this file and never contradict it. [`AGENTS.md`](../AGENTS.md) holds the binding decisions; this file spells them out.

## The stack

| Concern | Choice | Notes |
| ------- | ------ | ----- |
| Runtime | .NET 10, C# `latest` | SDK pinned by `global.json`; every project builds from `Photon.slnx` |
| UI | WPF, standard controls, custom theming | **No WPF-UI** and no other UI framework: a WPF-UI reference is a defect |
| MVVM | CommunityToolkit.Mvvm | `ObservableObject`, `[ObservableProperty]`, `[RelayCommand]`, `IMessenger` where messaging is genuinely needed. **No ReactiveUI.** `Ioc.Default` is not used: composition goes through Microsoft DI |
| Composition | Microsoft.Extensions.DependencyInjection, one Generic Host per app | One composition root per app; constructor injection; no static service locator (`App.Services`, `Foo.Instance`) |
| Logging | Serilog | Configured once per app through `Photon.Core` |
| Rendering | SkiaSharp (all apps), ComputeSharp (Imago GPU path) | |
| Tests | xUnit | See [`testing.md`](testing.md) |
| JSON | System.Text.Json with source-generated contexts | Newtonsoft.Json is not used |

**A dependency is a decision.** A package outside this table is added by a section that records why, and its license is checked against GPL-3.0 before it lands: permissive (MIT, BSD, Apache-2.0) and LGPL are compatible; a license that forbids redistribution, needs a paid key, or restricts field of use is not.

## Where code lives

- App logic lives in the app's `Core` project; its WPF project holds views, view models, and view-only services. A `Core` project never references WPF.
- **Shared code moves to `Photon.Core` (non-UI) or `Photon.UI` (WPF) only when two apps need it now.** One app's need stays in that app with a comment naming the day it would move. A second copy of a behavior in a second app is a defect; so is a shared type only one app consumes.
- An app never references another app's projects, and never assumes another app is installed at runtime.

## C# style

`.editorconfig` is the enforced form of these rules; this is the readable one.

- File-scoped namespaces; `using` directives inside the namespace; `System` usings first.
- Names: PascalCase types, members, and constants; `I` prefix on interfaces; `_camelCase` private fields; `s_camelCase` private static fields; camelCase locals and parameters; `T` prefix on type parameters; `Async` suffix on awaitable methods.
- Member order: constants, fields, constructors, properties, events, methods.
- Prefer `sealed` classes, `record` types for data, `required` members, primary constructors, collection expressions, pattern matching, and switch expressions where they read better than the alternative.
- Nullable reference types on everywhere; `ArgumentNullException.ThrowIfNull` and friends at public boundaries; no `!` suppression without a comment saying why it is safe.
- Async: no `async void` outside event handlers, no `.Result` or `.Wait()`, `ConfigureAwait(false)` in library code, a `CancellationToken` on anything that can take longer than a second.
- Culture: every number or date formatted for a file, a log property, or a comparison passes `CultureInfo.InvariantCulture`; text shown to a user uses the current culture. String comparisons name a `StringComparison`.
- No magic numbers: a threshold, size, or duration is a named constant or a setting.
- XML documentation on every public type and member of `Photon.Core`, `Photon.UI`, and each app's `Core` project.

## MVVM

- View models derive from `ObservableObject` and use `[ObservableProperty]` and `[RelayCommand]`. A command that cannot run is disabled through `CanExecute`, never by silently returning.
- A view model does not construct its services: it receives them through its constructor.
- A view model over 400 lines is a design smell to split by responsibility (document, tools, view state, commands), not a style to keep.
- Code-behind is for view-only concerns: focus, adorners, drag visuals, input capture. Anything a test would want to assert lives in a view model or service.

## Dependency injection

| Lifetime | Use for |
| -------- | ------- |
| Singleton | Settings, logging, theme, the icon catalog, app-wide services |
| Scoped | One scope per open document: its history, its selection, its tool state |
| Transient | Stateless parsers, exporters, codecs, and dialogs' view models |

Every service a view model or tool uses is registered in the app's composition root. A registration commented out is a defect.

## Logging

- Serilog, configured once per app through `Photon.Core`. Files go to `%LOCALAPPDATA%\Rizonesoft\<App>\logs\<app>-<date>.log`, rolled daily, 7 files kept, 10 MB per file. The `Debug` sink is on in Debug builds.
- Never under `artifacts/` or `build/`: those are build output, and an installed app has neither.
- Structured templates, never interpolation: `Log.Information("Saved {Path} in {ElapsedMs} ms", path, ms)`.
- **One Information line per user action that changes a document or a setting**, naming the action and its target. This is the audit trail the adjacency contract calls `audit`.

| Level | Use for |
| ----- | ------- |
| Verbose | Inner loops, per-frame detail (off by default) |
| Debug | Developer diagnostics |
| Information | User actions and lifecycle: opened, saved, exported, setting changed |
| Warning | Recovered problems: a skipped file, a fallback taken |
| Error | A failed action the app survived |
| Fatal | The app is going down |

## Errors

- Throw specific exceptions (`ArgumentException`, `InvalidOperationException`, `IOException`, a domain exception) with context; never swallow one silently. `catch (Exception)` only at the top of an action or in the global handler, and it logs.
- Expected failures (a file that will not parse, a refused write) return a result, not an exception, and the user sees a message naming the action, the file, and what it needed.
- Every app installs global handlers for the dispatcher, the app domain, and unobserved tasks. They log at Fatal or Error and show the shared exception window with a copyable report.

## Documents and user data

- **Every edit is an undo step.** An edit nobody can roll back is the most expensive defect class a creative tool has.
- **Saves are atomic:** write a temporary file in the target folder, flush, then replace. Killing the process mid-save leaves the original byte-identical.
- Autosave writes to the app's data folder, never over the user's file. Recovery offers what it found and deletes nothing without asking.
- A read-only file, a locked folder, or a full disk is refused with a message naming the file and the reason; the document stays open and dirty.
- Lumen never writes an original image. See [`lumen.md`](lumen.md).
- Settings live in `%LOCALAPPDATA%\Rizonesoft\<App>\settings.json`, written atomically through the `Photon.Core` settings store. Every setting has a default, a consumer, and a log line when it changes.

## Performance

- Name the budget: a feature states the document size it must handle (a 10,000-node path set, a 100-megapixel image, a 50,000-photo library) and the time it must meet.
- Anything slower than a second shows progress and can be cancelled.
- No allocation per frame on a render or input path; pool buffers (`ArrayPool<T>`), use `Span<T>`, and avoid LINQ and boxing in hot loops.
- Dispose native and GPU resources deterministically (`using`, `IDisposable` owners).

## Commits

Conventional Commits: `<type>(<scope>): <description>`, imperative, types `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`. TODO sections name their own commit message in their `Commit:` item; use it. One section is one logical change.

## The design contract

Every user-facing surface answers to this contract; the captures under `docs/captures/<app>/` are its visual reference, and where a capture and this contract disagree, the contract wins. `Photon.UI` carries these values as resources once it exists (`todo/01-core/`); until then each app's theme dictionary carries them under the same keys.

### Color

The suite is a neutral dark UI so the artwork carries the color. One grey ramp, shared by every app:

| Token | Value | Use |
| ----- | ----- | --- |
| `Crust` | `#151515` | Window frame, title bar |
| `Base` | `#1A1A1A` | Canvas surround, main background |
| `Mantle` | `#202020` | Panels and docks |
| `Surface0` | `#2A2A2A` | Controls at rest, list rows |
| `Surface1` | `#353535` | Controls hovered |
| `Surface2` | `#404040` | Controls pressed, selected rows |
| `Overlay0` | `#505050` | Borders, separators |
| `Subtext0` | `#B0B0B0` | Secondary text, captions |
| `Text` | `#E0E0E0` | Primary text |

These are Nodus's values as imported (`MainWindowView.xaml`, "Convert all app colors to pure greys"). Imago still carries Catppuccin Mocha with an orange accent; the shared theme section in `todo/01-core/` replaces it. Each app may name one accent color for focus and selection; until the operator chooses them, the accent is `Subtext0`. Status colors (error, warning, success) are named once in the theme and used only for status, never for decoration.

### Type and spacing

- Font: Segoe UI Variable (Segoe UI fallback), 12 px body, 11 px captions, 14 px dialog titles. Monospace: Cascadia Mono, then Consolas.
- Spacing on a 4 px grid: 4, 8, 12, 16, 24. Controls are 24 px tall in toolbars and panels, 28 px in dialogs.
- Icons are 16 px in menus and panels, 20 px on the tool rail, drawn from the shared icon catalog, and never a mix of icon families on one surface.

### Behavior

- Every icon-only control has a tooltip naming the command and its shortcut, and an `AutomationProperties.Name`.
- Every dialog is fully keyboard operable in a logical tab order, with Enter and Escape doing what their buttons say.
- Surfaces render correctly at 100, 150, and 200 percent scaling and in Windows high contrast.
- Animated feedback respects the Windows "animation effects" setting.
- Confirmations name what, how many, and how large; refusals name the action and what it needed.
- A surface never hardcodes a color, size, or spacing its theme resources name.

### Window anatomy

A document window is a menu bar, a tool rail on the left, the canvas, docked panels on the right, and a status strip at the bottom. Panels dock and float through AvalonDock with the shared theme. A feature adds to this anatomy; it does not invent a second one.
