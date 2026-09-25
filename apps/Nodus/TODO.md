## Nodus (formerly Bezier) in Photon – Roadmap

> **Goal**: Bring the existing Bezier app into the `Photon` monorepo under its new name **Nodus**, keeping its polished UI, themes, icons, and dev tools while aligning with shared standards and infrastructure.

### 0. Grounding
- [ ] Read:
  - [ ] Root `TODO.md` at repo root.
  - [ ] `previous-dev/Bezier/TODO.md` (detailed feature roadmap).
  - [ ] `standards/nodus.md` and `standards/shared.md` (once created).
- [ ] Decide which Bezier/Nodus branch/revision to treat as the **canonical source** for the import.

### 1. Import & Structure
- [ ] Create `src/Nodus.UI/` project structure based on `previous-dev/Bezier/Bezier.sln` (copy, don't start from empty, then gradually rename projects/namespaces).
- [ ] Keep project separation:
  - [ ] `Nodus.Core` (from `Bezier.Core`) → core logic, SVG model, tools, services.
  - [ ] `Nodus.Desktop` (from `Bezier.Desktop`) → WPF UI, themes, icons, command palette, debug tools. **Note: Remove WPF-UI dependencies; use standard WPF with custom theming.**
  - [ ] `Nodus.Tests` (from `Bezier.Tests`) → tests.
- [ ] Update namespaces/project root namespaces to sit under `Photon.Nodus.*`.
- [ ] Add projects to unified `ProjectPhoton.sln` solution.
- [ ] Ensure the solution builds from the monorepo root.

### 2. Shared Code Integration
- [ ] Identify Nodus/Bezier pieces that should move into `src/Photon.Core`:
  - [ ] Geometry, transforms, vector math.
  - [ ] Command/undo abstractions that Imago and Lumen can reuse.
  - [ ] Logging + error‑handling patterns.
  - [ ] Color science utilities.
- [ ] For each candidate:
  - [ ] Copy to `src/Photon.Core`, preserving behavior.
  - [ ] Wire Nodus to use the shared implementation.
  - [ ] Add or update tests to cover the shared code.
  - [ ] Ensure Nodus references `src/Photon.Core` project.

### 3. Dev Tools & Debugging
- [ ] Port Nodus (Bezier)’s debug/dev tools (debug window, HUD, performance tabs) into the new layout.
- [ ] Document them in `docs/dev/debug-tools.md` with a “Nodus” section:
  - [ ] What hotkeys to open.
  - [ ] What data each tab shows.
  - [ ] How logs/crash info end up under `build/artifacts/`.
- [ ] Align error dialogs and crash handling with `standards/shared.md`.

### 4. Documentation
- [ ] In `docs/user/nodus-getting-started.md`:
  - [ ] High‑level overview, supported workflows.
  - [ ] How to install (link to `build/innosetup` or installer artifacts).
- [ ] In `docs/dev/architecture.md`:
  - [ ] Short subsection describing Nodus/Bezier architecture, pointing to `previous-dev/Bezier/docs`.
- [ ] Ensure every user‑facing feature you touch has at least a bullet in `docs/user/` or an existing doc linked.

### 5. Production Readiness & Distribution
- [ ] Hook Nodus into unified build:
  - [ ] Ensure `ProjectPhoton.sln` builds Nodus projects correctly.
  - [ ] Update root/build scripts to build + test Nodus and drop binaries in `build/artifacts/{Debug,Release}`.
  - [ ] Add/port Inno Setup or other installer script under `build/innosetup/nodus.iss`.
  - [ ] Define Nodus's versioning rules in `standards/release.md` (e.g. `nodus-1.0.0`).
  - [ ] Ensure Nodus installs into its own directory (separate from Imago/Lumen).
- [ ] Verify:
  - [ ] Clean install on a fresh Windows machine.
  - [ ] Logging, error dialogs, and debug tools all behave as documented.
  - [ ] "Edit In" workflows work (e.g., sending SVG from Nodus to Imago).

> **Rule for AI tools**: When working on Nodus (formerly Bezier), always read this file, the root `TODO.md`, `standards/nodus.md`, and `standards/shared.md` first, then build + test (`dotnet build` / `dotnet test`) and update both dev + user docs before committing and pushing.


