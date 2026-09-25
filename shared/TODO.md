## Photon.Core – Shared Infrastructure Roadmap

> **Goal**: Extract and evolve common functionality used by **Nodus** (vector), **Imago** (raster), and **Lumen** (darkroom) into `src/Photon.Core` with clear standards and documentation.

### 0. Grounding
- [ ] Read:
  - [ ] Root `TODO.md` at repo root.
  - [ ] `src/Nodus.UI/TODO.md`, `src/Imago.UI/TODO.md`, and `src/Lumen.UI/TODO.md` (when created).
  - [ ] `standards/shared.md` plus `standards/nodus.md`, `standards/imago.md`, and `standards/lumen.md`.
- [ ] Create `src/Photon.Core` class library project structure:
  - [ ] Core rendering pipeline (high-performance 2D drawing primitives).
  - [ ] File I/O (unified handling of complex formats).
  - [ ] Plugin system (common interface for extensions).
  - [ ] Color science (shared color management).
  - [ ] Math, primitives, infrastructure.
  - [ ] Logging, error handling, debug tooling contracts.

### 1. Core Primitives & Math
- [ ] Define shared types that all three apps can use:
  - [ ] Geometry & transforms (matrix math, points, rectangles).
  - [ ] Color utilities and conversions (RGB, CMYK, LAB, etc.).
  - [ ] Common result/error types (e.g. `Result<T>` patterns).
- [ ] Copy existing implementations from Nodus (Bezier)/Imago into `src/Photon.Core`, preserving behavior.
- [ ] Add focused tests to validate shared behavior without pulling in full app dependencies.
- [ ] Ensure `ProjectPhoton.sln` includes `src/Photon.Core` and all apps reference it.

### 2. Commands, History, and Tools Infrastructure
- [ ] Extract reusable concepts:
  - [ ] Command/undo interfaces and base implementations.
  - [ ] History/transaction abstractions that can be reused across vector, raster, and asset management workflows.
  - [ ] Common tool/kernel patterns (input handling, modifiers, overlays) where feasible.
- [ ] Document these patterns in `docs/dev/architecture.md` under a "Photon.Core Infrastructure" section.

### 3. Logging, Error Handling, and Diagnostics
- [ ] Implement shared diagnostics in `src/Photon.Core`:
  - [ ] Common logging interface and Serilog configuration defaults.
  - [ ] Shared error/exception patterns, as defined in `standards/shared.md`.
  - [ ] Contracts for debug windows/panels (so each app can plug its own implementation in a consistent way).
- [ ] Ensure logs and crash artifacts are written into predictable locations under `build/artifacts/logs`.
- [ ] Support "Edit In" workflows (e.g., sending RAW from Lumen to Imago, SVG from Nodus to Imago).

### 4. Standards & Cross‑Cutting Concerns
- [ ] Finalize `standards/shared.md`:
  - [ ] Coding style decisions that must be consistent across all three apps.
  - [ ] Error handling and logging rules.
  - [ ] Versioning rules and how Photon.Core is versioned relative to apps.
- [ ] Reference `standards/shared.md` from all app‑level `TODO.md` files (Nodus, Imago, Lumen).

### 5. Developer Experience & Prompts
- [ ] Work with the `prompts/` templates so that:
  - [ ] Any shared change automatically checks for breakage in all three apps.
  - [ ] Docs in `docs/dev/` and `docs/user/` are updated when shared behavior changes.
  - [ ] Version numbers and changelogs are updated for Photon.Core where relevant.
- [ ] Ensure `ProjectPhoton.sln` builds successfully when Photon.Core changes.

> **Rule for AI tools**: When touching anything in `src/Photon.Core`, always consider impact on all three apps: run relevant tests for Nodus, Imago, and Lumen, update shared + app docs, and follow `standards/shared.md` strictly.


