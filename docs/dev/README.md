# Developer Guides

Documentation for contributors and maintainers of the Photon Graphics Suite.

## Guides

| Guide | What it covers |
| ----- | -------------- |
| [Architecture](architecture.md) | Photon.Core, Photon.UI, the three apps, and "develop together, distribute separately" |
| [Standards](../../standards/README.md) | Suite-wide and per-app coding, testing, and release standards |
| [Building](build.md) | Toolchain provisioning, building the solution, running the gates, packaging installers, and CI |
| [Versioning and releases](versioning.md) | MinVer, per-app tags (`nodus-v*`, `imago-v*`, `lumen-v*`, `photon-v*`), and the release workflow |
| [Contributing](../../CONTRIBUTING.md) | Workflow, code style, Conventional Commits, DCO sign-off, and pull request checks |
| [The TODO system](../../todo/README.md) | How the plan is organized into domains, tasks, and sections, and how to reference them (`DNN TNN §N`) |
| [Implementation plan](../../todo/implementation-plan.md) | The ordered plan: what runs next and what it depends on |

## Quick reference

```powershell
pwsh tools/provision.ps1              # install the pinned .NET SDK (11.0.100-rc.1) and Inno Setup 7
dotnet build Photon.slnx              # build everything
pwsh scripts/check-all.ps1            # run every gate
pwsh scripts/package.ps1 -App Nodus   # installer and portable ZIP for one app
```

## Per-app notes

- **Nodus** lives in `src/Nodus/` (projects still named `Bezier.*` from its origin until `D02 T01 §1`). Standards: [`standards/nodus.md`](../../standards/nodus.md).
- **Imago** lives in `src/Imago/`. Standards: [`standards/imago.md`](../../standards/imago.md).
- **Lumen** is planned and will live in `src/Lumen/`. Standards: [`standards/lumen.md`](../../standards/lumen.md).
- The original Bezier and Imago roadmaps are kept for reference in [`docs/legacy/`](../legacy/README.md).

## Planned

- `debugging.md`: logs, the Nodus debug window, and diagnostics

When a change affects architecture, build, or process, update the matching page here in the same pull request.
