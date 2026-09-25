## Prompt – Complete a Feature/Step Fully

Use this when you want the AI tool to take a TODO item or feature from **start to production‑ready**, including docs, tests, build, and git.

```text
You are working in the Photon monorepo (Rizonesoft Graphics Suite), which contains:
- src/Photon.Core  → Shared class library (rendering, file I/O, plugins, color science)
- src/Nodus.UI     → Vector editor (WPF, SkiaSharp, formerly Bezier)
- src/Imago.UI     → Raster editor (WPF, SkiaSharp/ComputeSharp)
- src/Lumen.UI     → Digital darkroom & asset manager (WPF, planned)
- standards/       → Coding, testing, release, and logging standards
- docs/dev and docs/user → Developer and user docs

TASK
- Complete this TODO item in full (no partial work):
  [PASTE THE EXACT TODO LINE OR SECTION]

BEFORE CODING
1. Read:
   - Root TODO.md
   - The relevant app/shared TODO (src/Nodus.UI/TODO.md, src/Imago.UI/TODO.md, src/Lumen.UI/TODO.md, or shared/TODO.md)
   - The relevant standards in /standards (nodus.md, imago.md, lumen.md, shared.md, release.md, testing.md)
2. Locate existing code, patterns, and tests that are closest to this feature.

IMPLEMENTATION RULES
- Reuse and copy from existing Nodus (Bezier)/Imago/Lumen code where possible instead of inventing new patterns.
- Keep shared logic in src/Photon.Core, UI-specific code in src/*.UI projects.
- Follow error‑handling and logging rules from standards/shared.md.
- Keep changes tightly scoped to the feature/step and its direct dependencies.
- Remember: "Develop Together, Distribute Separately" — shared core, separate installers.

DOCS & TESTS
- Update developer docs in docs/dev (architecture, build-and-run, debug-tools) if behavior or flows change.
- Update or create user docs in docs/user if the feature is user‑visible.
- Add or update tests as required by standards/testing.md.

BUILD & RUN
- Build and test the unified solution:
  - dotnet build ProjectPhoton.sln
  - dotnet test ProjectPhoton.sln
- Or build/test individual apps:
  - For Nodus: dotnet build src/Nodus.UI && dotnet test src/Nodus.Tests
  - For Imago: dotnet build src/Imago.UI && dotnet test src/Imago.Tests
- If applicable, ensure artifacts land under build/artifacts/.

GIT
- Stage, commit, and push using Conventional Commits:
  - git add -A
  - git commit -m "[TYPE](scope): [short description]"
  - git push

OUTPUT
- Show a concise summary of:
  - Files changed
  - Tests added/updated
  - Docs updated
  - Build/test commands run and their results
```


