## Imago in Photon – Roadmap

> **Goal**: Host **Rizonesoft Imago** inside the `Photon` monorepo, keeping its high‑performance architecture and standards while sharing infrastructure via `src/Photon.Core` with Nodus and Lumen.

### 0. Grounding
- [ ] Read:
  - [ ] Root `TODO.md` at repo root.
  - [ ] `previous-dev/Imago/TODO.md` (detailed roadmap).
  - [ ] `standards/imago.md` and `standards/shared.md` (once created).
- [ ] Decide which Imago branch/revision is the **source of truth** for this import.

### 1. Import & Structure
- [ ] Create `src/Imago.UI/` project structure based on `previous-dev/Imago/Imago.sln` (copy, don't recreate).
- [ ] Preserve the project breakdown:
  - [ ] `Imago.Core` — domain model, layers, selections, history.
  - [ ] `Imago.Rendering` — SkiaSharp/ComputeSharp rendering.
  - [ ] `Imago.UI` — WPF shell, panels, tools.
  - [ ] `Imago.*.Tests` — tests.
- [ ] Adjust namespaces/root namespaces to sit under `Photon.Imago.*`.
- [ ] Add projects to unified `ProjectPhoton.sln` solution.
- [ ] Confirm build works from the monorepo root.

### 2. Shared Code Integration
- [ ] Compare with Nodus/Lumen and `src/Photon.Core`:
  - [ ] Reuse `src/Photon.Core` where it overlaps (math, transforms, logging contracts, color science).
  - [ ] Contribute Imago-specific primitives to `src/Photon.Core` if they benefit other apps (e.g., tiled image system, GPU compute patterns).
- [ ] For each shared piece:
  - [ ] Copy from existing Imago source to `src/Photon.Core` (no rewrites yet).
  - [ ] Update Imago references to use `src/Photon.Core` project.
  - [ ] Add tests or reuse existing tests to guard behavior.
  - [ ] Ensure "Edit In" workflows work (e.g., receiving RAW from Lumen, SVG from Nodus).

### 3. Debugging, Error Handling, and Dev Tools
- [ ] Align Imago's logging, global exception handling, and crash reporting with the patterns in `standards/shared.md`.
- [ ] Document Imago‑specific debug/dev tools in `docs/dev/debug-tools.md`:
  - [ ] GPU diagnostics, performance views, or any special tooling.
- [ ] Ensure error messages and diagnostics land in the same log/artifact locations as Nodus/Lumen (under `build/artifacts/logs`).

### 4. Documentation
- [ ] `docs/user/imago-getting-started.md`:
  - [ ] Basic concepts, typical workflows, and differences from Bezier.
  - [ ] Installation notes referencing `build/innosetup/imago.iss` or other installers.
- [ ] `docs/dev/architecture.md`:
  - [ ] Section outlining Imago’s architecture and pointing to `previous-dev/Imago/docs`.
- [ ] Keep TODOs in sync:
  - [ ] When you complete a step here that corresponds to a bigger section in `previous-dev/Imago/TODO.md`, mark it in both places.

### 5. Production Readiness & Distribution
- [ ] Integrate Imago into unified build:
  - [ ] Ensure `ProjectPhoton.sln` builds Imago projects correctly.
  - [ ] Ensure Imago builds/tests as part of CI.
  - [ ] Drop binaries into `build/artifacts/{Debug,Release}`.
- [ ] Add/port installer script under `build/innosetup/imago.iss`.
- [ ] Define Imago versioning rules in `standards/release.md` (e.g. `imago-1.0.0`).
- [ ] Ensure Imago installs into its own directory (separate from Nodus/Lumen).
- [ ] Validate:
  - [ ] Clean install, run, edit, and export flows on a fresh machine.
  - [ ] Logging, error dialogs, and dev tools match shared expectations.
  - [ ] "Edit In" workflows work (receiving files from Lumen/Nodus).

> **Rule for AI tools**: When working on Imago, always read this file, the root `TODO.md`, `standards/imago.md`, and `standards/shared.md` first. For each completed step: update docs, run build + tests, then commit and push.


