## Build, CI, and Distribution

The `build/` folder standardizes how Bezier, Imago, and shared components are built, tested, and packaged.

Recommended structure:

- `build/scripts/`
  - Shared PowerShell scripts (e.g., `build.ps1`, `test.ps1`, `publish.ps1`).
- `build/innosetup/`
  - Inno Setup scripts for installers (e.g., `bezier.iss`, `imago.iss`).
- `build/artifacts/`
  - `Debug/` and `Release/` build outputs from CI and local builds.
  - Logs and crash dumps (referenced by `standards/shared.md`).

CI workflows should:

- Build and test Bezier and Imago.
- Publish artifacts into `build/artifacts/`.
- Optionally produce signed installers using the scripts in `build/innosetup/`.


