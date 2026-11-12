---
name: plan-new-feature
description: Plan a new Isotone app feature, or a whole new standalone native C++23 app (Stilus, Gesso, Albumen, Tinctura, Capio, Folium), from an idea to a distribution-ready TODO file -- job definition, competitor survey, Exceed improvements, full design-contract surface and behavior plan, and finer details. Use when a feature or an app needs creating from nothing.
---

# Plan New Feature

Turn a feature or standalone app concept into a complete, zero-gap TODO file on Isotone's native C++23 + Win32/Direct2D/DirectWrite/Direct3D stack (`docs/specs/2026-10-22-native-stack-design.md`, `standards/cpp.md`, `standards/design-contract.md`). Every Isotone app develops together in this repository and distributes separately (`<app>-v*` tags, standalone installer, zero runtime dependency on sibling Isotone apps).

## Workflow

### 1. Define the job, non-goals, and home

Write the user job paragraph (who, what situation, what done looks like), explicit non-goals, working name, tooltip/About one-liner, and target audience. Search `todo/` and `todo/backlog.md` via `add-todo` so nothing duplicates an existing owner. Place shared capabilities in `01-core` (`isotone::core` / shared native UI) only when at least two apps consume them now; otherwise own them in the single app's domain with a note naming when they would move.

### 2. Survey the competition and define `**Exceed:**`

Survey two or three leading applications that perform this job (Illustrator, CorelDRAW, Photoshop, Affinity, GIMP, Lightroom Classic, ACDSee, IrfanView, InDesign, ShareX, PicPick -- naming exact versions or official documentation). Compare surfaces, shortcuts, modifiers, empty/error states, presets, undo granularity, and pain points (fanning out read-only `research` subagents in parallel if helpful per `standards/delegation.md`). Every feature section authored from this plan must include an `**Exceed:**` paragraph (`AGENTS.md`) naming at least one concrete, measurable advantage over the competition (speed/memory benchmark on `D00 T04 §2`, removed workflow steps, capability rivals miss, or superior output quality), built by a checklist item and proved by `Test checkpoint`.

### 3. Specify surfaces 1:1 against `docs/design/`

List every tool-rail entry, icon, cursor, shortcut, options bar, menu item, command palette entry, panel, dialog, canvas handle/overlay, Preferences control, status strip message, and structured log event, along with empty, loading, busy, disabled-with-reason, and error states. Every UI section carries validating `**Fidelity:**`, `**Design:**`, `**Job:**`, `**Treatment:**`, and `**Chrome:**` lines (`todo/README.md`, `standards/design-contract.md`); if `docs/design/` lacks a component spec or token, set `new surface: docs/design/<path>.md` and make authoring the spec + `docs/design/tokens.json` update item 1 before any UI code. Plan no literal color, size, or font: `scripts/design-lint.py` refuses one in the UI sources, so every value a surface needs is a token before the section is written.

### 4. Specify behaviors, safety, and finer details

Plan every applicable requirement with zero "details at build time" placeholders:

- Typed settings keys with defaults and live consumers, plus structured logging for every document or setting mutation.
- Full undo/redo, dirty-state tracking, crash-safe autosave/recovery participation, cancellation on operations over 1 second, and large-document performance budgets (e.g., 100 MP raster, 10,000-node vector path, 50,000-photo catalog).
- Atomic temp-file-then-replace writes with read-back, plus round-trip fidelity or explicit warn/flatten behavior per file format.
- Accessibility names, keyboard navigation/tab order, tooltips with shortcuts, 100%/150%/200% DPI scaling, all four themes, both densities, reduced motion, high contrast, and same-commit `docs/user/` documentation.
- **Whole new app additions:** `native/` CMake targets, dependency register entries (`docs/dev/native-libraries.md`), single-instance/file-association wiring, About dialog, standalone packaging/installer (`05-release`), `<app>-v*` release tags, and user guide (`06-docs`).

### 5. Author via `create-todo`, wire, validate, and commit

Author the TODO file through `create-todo` (stamping `**Origin:** discovered run=<run id> <YYYY-MM-DD>` on campaign-discovered sections and routing non-admitted nice-to-haves to `todo/backlog.md`), update `docs/parity/*-parity.md` if parity rows change, reciprocate all `-> XREF:` links, place rows in `todo/implementation-plan.md`, and run:

```powershell
python scripts/todo-claims.py
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --sync
python scripts/todo-graph.py plan --check
```

Commit on `main` as one `todo:` commit and report the new file, competitor comparison with `**Exceed:**` wins, any `todo/backlog.md` additions, and updated plan totals.

## Guardrails

- Never omit the job definition, competitor survey, `**Exceed:**` paragraph, undo/redo, or atomic save/read-back paths.
- Never file vague "polish later" sections, and never use em/en dashes (`--` only).
