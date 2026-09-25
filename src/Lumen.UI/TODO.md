## Lumen in Photon – Roadmap

> **Goal**: Create **Rizonesoft Lumen**, a digital darkroom and asset manager that bridges camera workflows with Imago, sharing infrastructure via `src/Photon.Core`.

### 0. Grounding
- [ ] Read:
  - [ ] Root `TODO.md` at repo root.
  - [ ] `standards/lumen.md` and `standards/shared.md` (once created).
  - [ ] `src/Imago.UI/TODO.md` and `src/Nodus.UI/TODO.md` for integration patterns.
- [ ] Define Lumen's core workflows:
  - [ ] RAW image processing and non-destructive editing.
  - [ ] Batch adjustments and presets.
  - [ ] Library management and organization.
  - [ ] "Edit In" workflows (send to Imago, export to Nodus).

### 1. Project Structure
- [ ] Create `src/Lumen.UI/` project structure:
  - [ ] `Lumen.Core` — domain model, library management, RAW processing pipeline.
  - [ ] `Lumen.UI` — WPF shell, library browser, adjustment panels.
  - [ ] `Lumen.Tests` — tests.
- [ ] Set namespaces to `Photon.Lumen.*`.
- [ ] Add projects to unified `ProjectPhoton.sln` solution.
- [ ] Reference `src/Photon.Core` for shared infrastructure.

### 2. Photon.Core Integration
- [ ] Use `src/Photon.Core` for:
  - [ ] Color science (color management, profiles).
  - [ ] File I/O (RAW format support, metadata handling).
  - [ ] Logging and error handling.
  - [ ] Plugin system (for RAW processors, export formats).
- [ ] Contribute Lumen-specific primitives to `src/Photon.Core` if beneficial:
  - [ ] Non-destructive adjustment pipeline patterns.
  - [ ] Library indexing and search utilities.

### 3. Core Features
- [ ] RAW Processing:
  - [ ] Support major RAW formats (CR2, NEF, ARW, DNG, etc.).
  - [ ] Non-destructive adjustment pipeline (exposure, white balance, curves, etc.).
  - [ ] Batch processing capabilities.
- [ ] Library Management:
  - [ ] Import and organize photos.
  - [ ] Metadata editing and search.
  - [ ] Collections and smart collections.
- [ ] "Edit In" Workflows:
  - [ ] Send RAW/processed image to Imago for pixel-level editing.
  - [ ] Export vector paths to Nodus (if applicable).

### 4. Documentation
- [ ] `docs/user/lumen-getting-started.md`:
  - [ ] Overview of digital darkroom workflows.
  - [ ] How to import, organize, and process RAW files.
  - [ ] Integration with Imago and Nodus.
- [ ] `docs/dev/architecture.md`:
  - [ ] Section describing Lumen's architecture and how it uses Photon.Core.

### 5. Production Readiness & Distribution
- [ ] Integrate Lumen into unified build:
  - [ ] Ensure `ProjectPhoton.sln` builds Lumen projects correctly.
  - [ ] Ensure Lumen builds/tests as part of CI.
  - [ ] Drop binaries into `build/artifacts/{Debug,Release}`.
- [ ] Add installer script under `build/innosetup/lumen.iss`.
- [ ] Define Lumen versioning rules in `standards/release.md` (e.g. `lumen-1.0.0`).
- [ ] Ensure Lumen installs into its own directory (separate from Nodus/Imago).
- [ ] Validate:
  - [ ] Clean install and basic workflows on a fresh machine.
  - [ ] "Edit In" workflows work correctly.
  - [ ] Logging and error handling match shared expectations.

> **Rule for AI tools**: When working on Lumen, always read this file, the root `TODO.md`, `standards/lumen.md`, and `standards/shared.md` first. For each completed step: update docs, run build + tests, then commit and push.

