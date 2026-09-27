# 05 Release

> **Phases 3, 39, 40, and 45**

Distribution for every app and the suite: the clean-machine install procedure each release runs, code signing (waiting on a certificate), win-arm64, the update check, winget, and the `photon-v*` suite bundle (`photon-v1.0.0` in Phase 40, and `photon-v1.1.0` in Phase 45 after the post-release phases the operator added on 2026-09-27). The per-app release sections live in each app's domain and consume what this domain builds.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-release-pipeline.md) | Distribution: Clean-Machine Proof, Signing, arm64, Updates, winget, and the Suite Bundle | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- `scripts/publish.ps1`, `scripts/package.ps1`, `installer/`, `.github/workflows/release.yml` changes beyond the workspace spine
- Signing, architectures, update checks, package managers, and the suite bundle

## Out of scope

- Each app's own release section (its changelog, its tag) in 02, 03, and 04
- The workspace spine's first pipeline dry run (00)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
