# Developer Guides

Documentation for contributors and maintainers of the Isotone Graphics Suite.

## Guides

| Guide | What it covers |
| ----- | -------------- |
| [Architecture](architecture.md) | Isotone.Core, Isotone.UI, the three apps, and "develop together, distribute separately" |
| [Standards](../../standards/README.md) | Suite-wide and per-app coding, testing, and release standards |
| [Building](build.md) | Toolchain provisioning, building the solution, running the gates, packaging installers, and CI |
| [Versioning and releases](versioning.md) | MinVer, per-app tags (`stilus-v*`, `pinxit-v*`, `albumen-v*`, `isotone-v*`), and the release workflow |
| [Contributing](../../CONTRIBUTING.md) | Workflow, code style, Conventional Commits, DCO sign-off, and pull request checks |
| [The TODO system](../../todo/README.md) | How the plan is organized into domains, tasks, and sections, and how to reference them (`DNN TNN §N`) |
| [Implementation plan](../../todo/implementation-plan.md) | The ordered plan: what runs next and what it depends on |

## Quick reference

```powershell
pwsh tools/provision.ps1              # install the pinned .NET SDK (11.0.100-rc.1) and Inno Setup 7
dotnet build Isotone.slnx              # build everything
pwsh scripts/check-all.ps1            # run every gate
pwsh scripts/package.ps1 -App Stilus   # installer and portable ZIP for one app
```

## Per-app notes

- **Stilus** lives in `src/Stilus/` (projects still named `Bezier.*` from its origin until `D02 T01 §1`). Standards: [`standards/stilus.md`](../../standards/stilus.md).
- **Pinxit** lives in `src/Pinxit/`. Standards: [`standards/pinxit.md`](../../standards/pinxit.md).
- **Albumen** is planned and will live in `src/Albumen/`. Standards: [`standards/albumen.md`](../../standards/albumen.md).
- The original Bezier and Pinxit roadmaps are kept for reference in [`docs/legacy/`](../legacy/README.md).

## Planned

- `debugging.md`: logs, the Stilus debug window, and diagnostics

When a change affects architecture, build, or process, update the matching page here in the same pull request.
