# Developer Guides

Documentation for contributors and maintainers of the Isotone Graphics Suite.

## Guides

| Guide | What it covers |
| ----- | -------------- |
| [Architecture](architecture.md) | `isotone::core`, `isotone::ui`, the engines, the apps, and "develop together, distribute separately" |
| [Standards](../../standards/README.md) | Suite-wide and per-app coding, design, testing, and release standards |
| [Building](build.md) | The pinned toolchain, the CMake presets, running the gates, packaging, and CI |
| [The native tree](../../native/README.md) | The layout of `native/`, the presets, the sanitizer lane, format and analysis, imports and size, packages |
| [Versioning and releases](versioning.md) | SemVer from per-app tags (`stilus-v*`, `gesso-v*`, `albumen-v*`, `isotone-v*`), channels, changelogs, and the release workflow |
| [The dependency register](native-libraries.md) | Every third-party library, its license, its advisory identity, and the apps that link it |
| [Decisions](decisions.md) | Recorded decisions with their evidence and cost of change |
| [The reference machine](reference-machine.md) | The machine benchmark records are measured on |
| [Contributing](../../CONTRIBUTING.md) | Workflow, code style, Conventional Commits, DCO sign-off, and pull request checks |
| [The TODO system](../../todo/README.md) | How the plan is organized into domains, tasks, and sections, and how to reference them (`DNN TNN §N`) |
| [Implementation plan](../../todo/implementation-plan.md) | The ordered plan: what runs next and what it depends on |

## Quick reference

```powershell
pwsh tools/provision.ps1 -Verify                # the machine has what the pins need (it never changes Visual Studio)
pwsh scripts/dev-env.ps1 -Check -Arch x64       # the pinned native toolchain is what this shell would run
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; cmake --workflow --preset x64-debug'   # configure, build, test
pwsh scripts/check-all.ps1                      # every gate: the plan gates and every native preset, test, sanitizer, and analysis stage
```

## Product facts

The suite's facts (its name, each app's name, slug, tag prefix, and role, the repository description, topics, and homepage, the README's opening line, where each version is pinned, and the retired names) are stated once, in [`docs/facts.json`](../facts.json): a fact changes there first, and `python scripts/drift-check.py` then holds the README, every tracked text file, and the repository's settings on GitHub to it.

## Per-app notes

- **Stilus** is planned under `native/stilus/` (`todo/02-stilus/`). Standards: [`standards/stilus.md`](../../standards/stilus.md). Notes on the C# prototype, kept as a behavior reference: [the vector icon control](stilus/vector-icon.md) and [the status bar](stilus/status-bar.md).
- **Gesso** is planned under `native/gesso/` (`todo/03-gesso/`). Standards: [`standards/gesso.md`](../../standards/gesso.md). Notes on the C# prototype: [the plug-in interfaces](gesso/plugins.md).
- **Albumen** is planned under `native/albumen/` (`todo/04-albumen/`). Standards: [`standards/albumen.md`](../../standards/albumen.md).
- **Tinctura**, **Capio**, and **Folium** are planned by the campaign from `todo/07-tinctura/`, `todo/08-capio/`, and `todo/09-folium/`.
- The C# prototypes of Stilus and Gesso were removed from `main` by `D00 T06 §3` and are readable at the `csharp-final` tag ([build.md](build.md), "Reading the C# reference"). The original Bezier and Imago roadmaps (the apps now named Stilus and Gesso) are kept for reference in [`docs/legacy/`](../legacy/README.md).

## Planned

- `debugging.md`: logs, crash dumps, the Stilus debug window, and diagnostics

When a change affects architecture, build, or process, update the matching page here in the same pull request.
