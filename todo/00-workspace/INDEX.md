# 00 Workspace

> **Phases 0 to 3**

Toolchain, solution, gates, CI, and the TODO system every later domain leans on. Nothing here ships to a user; everything later depends on it being boring and green.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-dev-automation.md) | Dev-Automation Wiring | draft |
| [TODO-02](./TODO-02-build-and-test-debt.md) | Build and Test Debt from the Import | draft |
| [TODO-03](./TODO-03-repo-layout.md) | Repository Layout, Visual Baselines, and App Icon Export | draft |
| [TODO-04](./TODO-04-native-code-policy.md) | The C++ Standard, the Dependency Register, the Benchmark Harness, and the Advisory Job | draft |
| [TODO-05](./TODO-05-native-spine.md) | The Native Spine: Toolchain, Build, Gates, and CI | draft |
| [TODO-06](./TODO-06-retire-csharp.md) | Retire the C# Code and the .NET Toolchain | draft |
| [TODO-07](./TODO-07-native-replan.md) | The Native Re-plan, Phase by Phase | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- The pinned .NET SDK, `Isotone.slnx`, and one-command build, test, publish, and package scripts
- Warnings as errors, analyzers, and one command that runs every gate (`scripts/check-all.ps1`)
- CI workflows, the commit hook, and the provisioning script
- The native toolchain pin, the CMake presets, the vcpkg baseline, the C++ gates, and native CI (TODO-05)
- The C++ standard (standards/cpp.md), the dependency register and its gate, the advisory job, and the developer-only benchmark harness
- The checks that keep the plan honest about itself: the TODO graph, claims, the findings ledger, and the campaign guard
- The raster app icons generated from the committed SVG sources under `resources/icons/`, with a check that they match

## Out of scope

- `Isotone.Core` and the apps (01 to 04)
- Release packaging and signing (05), which consumes the build this domain writes
- Developer and user documentation content (06)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
