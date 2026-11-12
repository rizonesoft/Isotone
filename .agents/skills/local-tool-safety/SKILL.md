---
name: local-tool-safety
description: Use when adding, reviewing, or invoking Isotone local tools, Windows/Linux/WSL integrations, connector-backed workflows, automation launchers, CLI wrappers, or any operation that might send outbound data, delete data, change infrastructure, modify accounts, run SQL writes, install tools, or use discovered executable paths.
---

# Local Tool Safety

## Rule

Local, reversible work inside this repository proceeds autonomously without asking (`AGENTS.md`). Ask the operator once in attended sessions (or park with the question in unattended campaigns) before any action that sends, deletes, or changes something outside the repository: outbound mail, production publishing, cloud/infrastructure mutations, SQL writes, dropping external data, or credentials. Privileged OS commands are handed to the operator rather than guessing or storing OS passwords.

Detailed checklist: `references/local-tool-capability-safety.md`.

## Required Pattern

1. Resolve capability (pinned config in `native/toolchain.json` or explicit environment variables first, then safe discovery, then a clear setup-required state), never hardcoded user home paths.
2. Keep discovery output bounded: inspect executable version and only the targeted subcommand `--help` lines needed.
3. Prefer global/user-level installs for vendor CLIs, SDKs, compilers, and desktop tools; keep only Isotone-specific scripts, wrappers, schemas, hooks, tests, and docs in git.
4. Store machine-local discovered paths only in gitignored files under `build/`.
5. Report tool health explicitly (`available`, `missing`, `degraded`, `auth-required`, or `blocked`).
6. Run safe local read, build, test, and inspection workflows directly without prompting.
7. Never log, echo, or commit secrets, tokens, or credentials.
