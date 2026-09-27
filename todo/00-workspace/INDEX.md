# 00 Workspace

> **Phase 0**

Toolchain, solution, gates, CI, and the TODO system every later domain leans on. Nothing here ships to a user; everything later depends on it being boring and green.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-dev-automation.md) | Dev-Automation Wiring | draft |
| [TODO-02](./TODO-02-build-and-test-debt.md) | Build and Test Debt from the Import | draft |
| [TODO-03](./TODO-03-repo-layout.md) | Repository Layout, Visual Baselines, and App Icon Export | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- The pinned .NET SDK, `Isotone.slnx`, and one-command build, test, publish, and package scripts
- Warnings as errors, analyzers, and one command that runs every gate (`scripts/check-all.ps1`)
- CI workflows, the commit hook, and the provisioning script
- The checks that keep the plan honest about itself: the TODO graph, claims, the findings ledger, and the campaign guard
- The raster app icons generated from the committed SVG sources under `resources/icons/`, with a check that they match

## Out of scope

- `Isotone.Core` and the apps (01 to 04)
- Release packaging and signing (05), which consumes the build this domain writes
- Developer and user documentation content (06)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
