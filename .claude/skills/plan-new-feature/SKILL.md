---
name: plan-new-feature
description: Plan a new Photon app feature, or a whole new app such as Lumen, from an idea to a distribution-ready TODO file -- job definition, competitor survey, full surface and behavior plan, finer details included. Use when a feature or an app needs creating from nothing.
---

# Plan New Feature

A feature planned as "a panel with the thing in it" ships as a demo with a version number, and an app planned as "a window with the features" ships as three demos. This skill exists to prevent that: it defines the job, surveys what the competition ships, and plans every surface, behavior, state, and string the feature needs to be whole, down to the tooltips, the empty states, and the undo entry.

It covers two sizes of the same work. A **feature** lands in an existing app (a gradient tool in Nodus, a healing brush in Imago) or in `Photon.Core` when two apps need it now. A **new app** (Lumen is the planned one) is a feature set with its own executable, its own installer, its own version tag, and its own user guide, planned the same way with the app-level items in step 4 added.

## Workflow

### 1. Define the job

Write one paragraph: whose problem, in what situation, and what "done" looks like to them. Then write the non-goals: the adjacent problems this feature does not solve, so scope has a fence. Then search the tree (`add-todo`) for an existing section, file, or app that owns any of it; a feature that duplicates one is a defect at birth.

Record the working name, the one-line purpose (it will be quoted by the menu or tool rail tooltip, the About page for a new app, and the user guide), and the audience: a feature for a production illustrator and a feature for someone touching up a holiday photo are specified differently.

Decide the home with a reason: the one app that needs it, or `Photon.Core` because a second app needs it now. "Might be shared one day" is not a reason; the day a second app needs it, a section moves it.

### 2. Survey the competition

Find two or three applications that do this job today, from Photoshop, Illustrator, Lightroom, the Affinity suite (Designer, Photo), Inkscape, GIMP, and darktable, whichever genuinely do it. Use each one, and write the feature table: their surfaces, their behaviors, their finer details (empty states, failure messages, keyboard shortcuts and modifiers, on-canvas handles and snapping, first-run, presets, export, undo granularity), and what each does badly. Every row names the version used. Where an application cannot be run here, cite its documentation page and say so in the row.

The table is the bar: the plan matches every detail that matters and names what beats each competitor, feature by feature. A plan written without touching the competition invents a market that does not exist.

### 3. Define the surfaces

Specify the feature control by control: the tool on the tool rail with its icon, cursor, and shortcut; its context toolbar or options bar with every control; the menu items and their shortcuts; panels and their docking; dialogs; the on-canvas handles, guides, and overlays; the Preferences page entries; the status strip text; and the log lines. For each surface name its controls, its strings, its states, and its empty, loading, busy, and failure presentations. No placeholder, no hardcoded string, no "details at build time": a builder who must invent a control inherits a gap, not a freedom.

Every surface names its capture home under `docs/captures/<app>/` and its `Fidelity:` source in the design contract under `standards/`; a surface with no counterpart anywhere in the suite says `new build, no baseline`.

Decide document participation with a reason: if the feature changes a document it records an undo step for every edit, marks the document dirty, and survives save and reopen in every format that can carry it; if it cannot be carried by a format, the plan says what the save does instead (flatten, warn, or refuse) and why.

### 4. Define the behaviors

Every feature, no exceptions, plans its share of: settings keys with defaults through the app's settings service, a Serilog log line per user action that changes a document or a setting, undo and redo, keyboard access and shortcuts that do not collide with the app's existing map, performance on a large document (name the size: a 100-megapixel image, a 10,000-node path set, a 50,000-photo library) with the budget it must meet, cancellation for anything slower than a second, crash safety (autosave or recovery participation), file-format behavior for every format the app reads and writes, and the same-commit user-guide page under `docs/user/`. Anything genuinely not applicable carries a stated reason; silence is not a reason.

A **new app** additionally plans: its project layout under `src/` and its entry in `Photon.slnx`; its composition root (Microsoft.Extensions.DependencyInjection) and its Serilog configuration; single instance and file associations; its About page and version source; its own `scripts/publish.ps1` and `scripts/package.ps1` targets and installer; its tag prefix (`<app>-v*`) and its changelog; its first-run experience; and what it shares with the other apps through `Photon.Core` versus what it owns. It is distributed separately: it may never depend at runtime on another Photon app.

### 5. Define acceptance

Each section is born complete per `create-todo`: context, micro-step checklist with Done-when per item, Test checkpoint with a cheaper-substitute-that-fails line, Fidelity/Job/Treatment/Chrome on UI sections, Commit item. New behavior has no baseline, so every Test checkpoint drives the behavior and quotes it, including the failure path: a corrupted or truncated input file, a read-only target, an unsupported color mode, a full disk, an out-of-memory document. Logic is proven by xUnit tests run with `dotnet test Photon.slnx`; every file-format reader or writer owes a format fidelity proof (`todo/README.md`) against a committed fixture; UI sections owe the gate card's launch smoke (`.claude/skills/process-todo-section/gates.md`) and their captures as checkpoint evidence.

### 6. Finer-details pass

Walk every section and confirm each of these is owned somewhere: tooltips on every icon-only control, with the shortcut in the tooltip; accessible names (AutomationProperties) on everything; logical tab order and full keyboard operation of every dialog; DPI scaling at 100, 150, and 200 percent and every theme the app ships; high contrast; reduced motion for animated feedback; modifier keys on canvas tools (Shift constrains, Alt from center, and so on, matched to the competitor norm the survey recorded); first-run; upgrade from a previous version's settings and presets; export formats that match the rendered view, including color profile and bit depth; confirmation texts naming what, how many, and how large; and refusal texts naming the action and what it needed. Anything unowned gets an item on its section now, not a wish for later.

### 7. Author, wire, validate, commit

Author the file through `create-todo` in the domain that owns the home step 1 chose (`02-nodus`, `03-imago`, `04-lumen`, or `01-core`), creating the domain with its `INDEX.md` when it does not exist yet. Packaging and release items for a new app land in `05-release`, and its user guide in `06-docs`, each as sections XREFed both ways. Wire the plan rows with Depends On edges so `Photon.Core` dependencies sequence first and distribution items sequence after the behavior they ship, and place every section in a phase of `todo/implementation-plan.md`. A feature the operator asked for is operator-directed: its sections carry no Origin line and no cap limits them, so plan the whole feature, and file as backlog entries in `todo/backlog.md` only what the operator deferred. When a campaign invokes this skill for a feature it discovered on its own, every section carries `**Origin:** discovered run=<run id> <YYYY-MM-DD>` and counts against the run's cap, and what does not fit goes to the backlog (`todo/README.md`, "The budget and the backlog"). Then:

```bash
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --sync
python scripts/todo-graph.py plan --check
```

Commit as one `todo:` commit. Report the file, its sections, the competitor table with what beats each rival, the backlog entries it added, and the size line the Progress block now shows.

## Guardrails

- Do not plan without the job paragraph and the non-goals. A feature without a fence grows until it ships nothing.
- Do not skip the competitors. An unbeaten rival the plan never looked at beats it by default.
- Do not plan a second implementation of anything another app or `Photon.Core` already owns, and do not plan into `Photon.Core` what only one app needs.
- Do not leave a surface half-specified. Empty, loading, busy, and failure presentations are part of the surface.
- Do not plan an edit without its undo, or a document change without its save-and-reopen behavior.
- Do not file a "polish" section. Finer details live as items on the sections that own them.
- Do not invent competitor features. The table comes from using the competitors, and each row names the version used.
- Do not plan a new app that needs another Photon app at runtime. Develop together, distribute separately.
