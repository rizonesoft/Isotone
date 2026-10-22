# Gesso plug-in interfaces

Gesso's plug-in contract is a separate assembly, `Gesso.Plugins.Abstractions` (`src/Gesso/src/Gesso.Plugins.Abstractions/`), so a plug-in can reference it without taking a dependency on the editor. Moved from `src/Gesso/docs/plugins/README.md` by `D00 T03 §1`, and corrected against the code on 2026-10-22: the imported page described attributes, a plugins folder, and tool and format plug-in kinds that do not exist.

## What exists today

- [`IPlugin`](../../../src/Gesso/src/Gesso.Plugins.Abstractions/IPlugin.cs): the base contract, with `Id` (a `Guid`), `Name`, `Version`, `Author`, `Description`, `Initialize()`, and `Shutdown()`.
- [`IFilterPlugin`](../../../src/Gesso/src/Gesso.Plugins.Abstractions/IFilterPlugin.cs): a filter, which extends `IPlugin`.

## What does not exist yet

- No loader: Gesso discovers and loads no plug-in, and no plugins folder is read. Managed filter plug-ins are planned in `D03 T14 §12`, and the isolated host for Photoshop-compatible plug-ins in `D01 T09`.
- No metadata attributes: a plug-in describes itself only through the `IPlugin` properties.
- No tool or file format plug-in interfaces: `IFilterPlugin` is the only plug-in kind.

So a plug-in written against these interfaces today compiles but never runs; build against the contract `D03 T14 §12` ships.
