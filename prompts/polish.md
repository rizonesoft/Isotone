## Prompt – Polish & Production-Ready Pass

Use this when a feature exists but needs to be hardened, refined, and documented to be truly production‑ready.

```text
You are a senior engineer polishing an existing feature in the Photon monorepo (Rizonesoft Graphics Suite).

FEATURE
- Make this feature/area production‑ready:
  [NAME OR LINK TO THE FEATURE / TODO ITEM]

CONTEXT
- Photon contains src/Photon.Core (shared), src/Nodus.UI (vector), src/Imago.UI (raster), src/Lumen.UI (darkroom), standards/, docs/dev, docs/user, build/.
- Nodus focuses on vector editing; Imago on raster editing; Lumen on digital darkroom/asset management; Photon.Core holds common infrastructure.

READ FIRST
- Root TODO.md and the relevant app/shared TODO.
- standards/shared.md plus the app‑specific standards file (nodus.md, imago.md, or lumen.md).
- Any existing docs in docs/dev and docs/user that mention this feature.

MISSION
- VERIFY → FIX → POLISH → ENHANCE (lightly) → INTEGRATE → DOCUMENT.

POLISH CHECKLIST
- Correctness: passes existing tests and adds missing edge‑case coverage.
- UX: behavior is consistent, discoverable, and matches app style.
- Error handling: follows standards/shared.md (clear messages, logging, no silent failures).
- Performance: avoid unnecessary allocations and regressions in hot paths.
- Diagnostics: logs and debug tools expose enough info for troubleshooting.

REQUIRED OUTPUTS
1. Updated implementation with clear, minimal diffs.
2. Tests added/updated where gaps existed.
3. docs/dev updated with any architectural or behavior changes.
4. docs/user updated if the user experience changed or was undocumented.
5. Build + tests run and passed for the relevant solution(s).
6. Git commit and push with a Conventional Commit message like:
   - feat(scope): [feature] polished
   - fix(scope): harden [feature]
```


