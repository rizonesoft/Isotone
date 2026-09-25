## Standards Overview

This folder centralizes all project standards for the Photon monorepo (Rizonesoft Graphics Suite: Nodus, Imago, Lumen).

- `nodus.md` — Nodus‑specific coding, UI, and architectural standards (copied from `previous-dev/Bezier/STANDARDS.md`).
- `imago.md` — Imago‑specific coding and performance standards (copied from `previous-dev/Imago/STANDARDS.md`).
- `lumen.md` — Lumen‑specific standards (to be created based on shared patterns).
- `shared.md` — Cross‑cutting standards (logging, error handling, versioning, testing, prompts).
- `release.md` — Versioning, release process, distribution channels, installer conventions.
- `testing.md` — Test strategy, coverage targets, regression policy.

## Important Technical Decisions

### UI Framework
- **WPF-UI will NOT be used**. All apps use standard WPF with custom theming and controls.
- Use `CommunityToolkit.Mvvm` for MVVM patterns (ObservableObject, RelayCommand, etc.).
- Custom WPF controls and styling will be developed as needed.

> **Rule**: Every `TODO.md` and prompt template must point to this folder so that tools and contributors read the relevant standards before making changes.


