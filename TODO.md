## Photon Monorepo Roadmap (Rizonesoft Graphics Suite)

> **Goal**: Unified monorepo for **Rizonesoft Graphics Suite** (codename: Project Photon) containing three standalone creative applications that share `Photon.Core` but distribute separately: **Rizonesoft Nodus** (vector editor), **Rizonesoft Imago** (raster editor), and **Rizonesoft Lumen** (digital darkroom & asset manager).

### 0. Bootstrap & Structure
- [ ] Create GitHub repo for `Photon` and push the existing workspace.
- [ ] Adopt this root `TODO.md` as the **single entry point** for work planning.
- [ ] Create top‑level folders:
  - [ ] `src/Photon.Core` — shared class library (rendering, file I/O, plugins, color science).
  - [ ] `src/Nodus.UI` — vector editor app (WPF, SkiaSharp, based on previous Bezier project). **Note: WPF-UI will NOT be used; standard WPF with custom theming.**
  - [ ] `src/Imago.UI` — raster editor app (WPF, SkiaSharp/ComputeSharp). **Note: WPF-UI will NOT be used; standard WPF with custom theming.**
  - [ ] `src/Lumen.UI` — digital darkroom & asset manager app (WPF, planned). **Note: WPF-UI will NOT be used; standard WPF with custom theming.**
  - [ ] `standards/` — coding, UX, testing, release standards.
  - [ ] `docs/` — `docs/dev/` for developer docs, `docs/user/` for end‑user docs.
  - [ ] `build/` — build scripts, CI helpers, installers, and build output.
  - [ ] `prompts/` — prompt templates for the AI coding workflow.
- [ ] Create unified solution file `ProjectPhoton.sln` that includes all projects.

### 1. Standards & Governance
- [ ] Move application coding standards into `standards/`:
  - [ ] `standards/nodus.md` (copy from `previous-dev/Bezier/STANDARDS.md`).
  - [ ] `standards/imago.md` (copy from `previous-dev/Imago/STANDARDS.md`).
  - [ ] `standards/lumen.md` (create new, based on shared patterns).
  - [ ] `standards/shared.md` (shared conventions, logging, error handling, versioning for Photon.Core).
- [ ] Add `standards/release.md` (versioning scheme, release checklist, packaging rules).
- [ ] Add `standards/testing.md` (test strategy, coverage targets, regression policy).
- [ ] Ensure every `TODO.md` explicitly points to the relevant `standards/*.md`.

### 2. Apps Layout & Code Reuse
- [ ] Create `src/Photon.Core` class library as the shared foundation:
  - [ ] Rendering pipeline (high-performance 2D drawing primitives).
  - [ ] File I/O (unified handling of complex formats).
  - [ ] Plugin system (common interface for extensions).
  - [ ] Color science (shared color management).
  - [ ] Geometry, transforms, color utilities.
  - [ ] Command/undo infrastructure patterns.
  - [ ] Common logging/error‑handling abstractions.
- [ ] Under `src/Nodus.UI`, copy the existing Bezier solution from `previous-dev/Bezier` as a starting point and rename projects/namespaces to `Photon.Nodus.*`.
- [ ] Under `src/Imago.UI`, copy the existing Imago solution from `previous-dev/Imago` as a starting point and align namespaces to `Photon.Imago.*`.
- [ ] Create `src/Lumen.UI` project structure (new, planned for digital darkroom/asset management).
- [ ] Update all app projects to reference `src/Photon.Core`.
- [ ] Ensure `ProjectPhoton.sln` includes all projects and builds successfully.

### 3. Build, CI, and Distribution
- [ ] In `build/`:
  - [ ] Copy existing `build.ps1` / `publish.ps1` scripts from previous-dev projects and consolidate.
  - [ ] Add `build/innosetup/` with installer scripts for each app (nodus.iss, imago.iss, lumen.iss).
  - [ ] Add `build/artifacts/Debug` and `build/artifacts/Release` as standard output folders.
  - [ ] Ensure each app builds into its own executable directory (no shared installation folders).
- [ ] Add CI workflows (GitHub Actions) that:
  - [ ] Build and test **Nodus**, **Imago**, and **Lumen** (when ready) on every push.
  - [ ] Build `ProjectPhoton.sln` as the unified solution.
  - [ ] Produce versioned artifacts into `build/artifacts/`.
- [ ] Define a **versioning system** in `standards/release.md` (e.g. SemVer with app‑specific prefixes: `nodus-1.0.0`, `imago-1.0.0`, `lumen-1.0.0`).

### 4. Documentation (Dev + User)
- [ ] `docs/dev/`:
  - [ ] `architecture.md` — high‑level architecture for Photon.Core and all three apps (Nodus, Imago, Lumen).
  - [ ] `build-and-run.md` — how to build `ProjectPhoton.sln`, run, and debug each app.
  - [ ] `contributing.md` — how to use `TODO.md`, prompts, and `standards/`.
- [ ] `docs/user/`:
  - [ ] `nodus-getting-started.md` — link to/merge with existing Bezier docs.
  - [ ] `imago-getting-started.md` — link to/merge with existing Imago docs.
  - [ ] `lumen-getting-started.md` — new user guide for digital darkroom workflows.
  - [ ] `troubleshooting.md` — common errors and how to capture logs.

### 5. Tooling, Debugging, and Error Handling
- [ ] Define a **shared error handling system** in `Photon.Core` (referenced from `standards/shared.md`):
  - [ ] Unified logging format and sinks (Serilog).
  - [ ] Consistent global exception handling story for all three apps.
  - [ ] Crash‑report artifacts stored under `build/artifacts/logs`.
- [ ] Standardize developer/debug tools:
  - [ ] Bring Nodus (Bezier)’s debug/dev tools into a shared pattern described in `docs/dev/debug-tools.md`.
  - [ ] Ensure all apps expose a predictable debug window/hotkey.
  - [ ] Implement "Edit In" workflows (e.g., sending RAW from Lumen to Imago).

### 6. Release & Distribution
- [ ] Implement **installer** flows for all three apps (Inno Setup or MSIX, defined under `build/innosetup/`).
- [ ] Document distribution channels and update flow in `standards/release.md`.
- [ ] Ensure each app installs into separate directories (no shared installation folders) to prevent cross-app breakage.
- [ ] Ensure every release step:
  - [ ] Runs tests.
  - [ ] Builds installers/bundles.
  - [ ] Updates `CHANGELOG.md` and relevant `docs/user/` guides.

> **Rule for AI tools**: Before doing work, read this root `TODO.md`, the relevant app or shared `TODO.md`, and the relevant files in `standards/`. Always update docs, run build/tests, and commit + push at the end of a completed step.


