# Local Tool Capability Safety Rules

Isotone local tool integrations follow these rules:

1. Never assume a hardcoded user path; resolve pinned configuration (`native/toolchain.json`) or discover the capability cleanly.
2. Prefer global/user-level tool installs and keep repository assets limited to Isotone-specific scripts, schemas, wrappers, hooks, tests, and docs.
3. Execute safe local development, build, test, and self-healing workflows inside the repository autonomously without repeated confirmation.
4. Obtain explicit operator consent before anything that sends, deletes, or mutates state outside the repository: outbound email, production deploys, cloud/DNS/account changes, SQL writes, external deletions, or paid services.
5. Never store or guess OS administrator/sudo passwords in `.secrets`, environment files, logs, or notes.

## Capability Resolution

- [ ] Prefer explicit pinned config (`native/toolchain.json`), then platform discovery (`vswhere.exe`, `Get-Command`), then a clear setup-required diagnostic.
- [ ] Store transient local discovery caches only under gitignored `build/`.
- [ ] Never hardcode `C:\Users\<user>\...` or `/home/<user>/...` in production or gate logic.
- [ ] Never expose secret or token values in logs, UI surfaces, or test snapshots.

## Health States

`available`, `missing`, `degraded`, `auth-required`, `blocked`.
