## Prompt – General Request / Small Change

Use this for smaller tasks: bug fixes, UI tweaks, refactors, or clarifications that don’t correspond to a big roadmap section.

```text
You are working in the Photon monorepo (Rizonesoft Graphics Suite):
- src/Photon.Core (shared library), src/Nodus.UI, src/Imago.UI, src/Lumen.UI
- standards/, docs/dev, docs/user, build/

TASK
- Perform this smaller change or investigation:
  [DESCRIBE THE REQUEST CLEARLY]

CONTEXT & RULES
- Read the relevant TODO.md (root + app/shared) and the relevant standards in /standards first.
- Prefer copying/adapting existing patterns in the codebase over introducing new ones.
- Keep the change minimal and focused on the requested behavior.
- If the change is user‑visible, also update docs in docs/user.
- If touching src/Photon.Core, consider impact on all three apps (Nodus, Imago, Lumen).

STEPS
1. Identify the affected project(s) and files.
2. Implement the minimal fix or improvement.
3. Build and test the relevant solution(s).
4. If needed, update docs/dev and/or docs/user to reflect the change.
5. Commit and push with a clear Conventional Commit message (fix, chore, refactor, etc.).

OUTPUT
- Short explanation of what changed, where, and how it was validated (build/tests/manual checks).
```


