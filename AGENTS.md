# AGENTS.md

Agent instructions for this repository. Human orientation lives in `README.md`. Claude Code loads this file through the `CLAUDE.md` import stub.

## What this project is

`Photon` is the monorepo of the **Photon Graphics Suite**: three standalone creative applications for Windows 11, built on .NET 11 and WPF.

| App | Kind | State |
| --- | ---- | ----- |
| **Nodus** | Vector editor (Illustrator alternative) | Imported from Bezier under `src/Nodus/`; projects still named `Bezier.*` until renamed |
| **Imago** | Raster editor (Photoshop alternative) | Imported under `src/Imago/` |
| **Lumen** | Digital darkroom and asset manager (Lightroom alternative) | Planned in `todo/04-lumen/`; no code yet |
| **Photon.Core** | Shared non-UI library | Planned; created when two apps first need the same code |
| **Photon.UI** | Shared WPF library (house style, shared controls and windows) | Planned; created when the first duplicated control moves out of Nodus and Imago |

**Develop together, distribute separately.** The apps share one repository, one solution (`Photon.slnx`), one set of gates, and one plan, but each ships as its own product: its own installer, its own version, its own changelog, its own user guide. An app may never depend at runtime on another app, and nothing it ships may assume another app is installed.

| Path | Purpose |
| ---- | ------- |
| `src/Nodus/` | Nodus, the vector editor |
| `src/Imago/` | Imago, the raster editor (`src/` projects and `tests/` test projects inside it) |
| `src/Lumen/` | Lumen, the darkroom (planned) |
| `src/Photon.Core/`, `src/Photon.UI/` | Shared libraries, only what two apps need (planned); the target layout is in `docs/dev/architecture.md` |
| `Photon.slnx` | The one solution every build, test, and publish goes through |
| `scripts/` | `build.ps1`, `publish.ps1`, `package.ps1`, `check-all.ps1`, and the stdlib Python TODO tooling (`todo-graph.py`, validator, claims, findings, runs, review prompt, panel slots, campaign guard) |
| `tools/` | `provision.ps1` (sets up a clone, including the commit hook) and `githooks/pre-commit` |
| `todo/` | The live execution plan; read `todo/README.md` before authoring or implementing |
| `todo/implementation-plan.md` | Ordered phase plan; its boxes are synchronized through `scripts/todo-graph.py` |
| `todo/budget.json`, `todo/backlog.md` | The plan's ceilings and their history; the capped list of deferred ideas that are not sections |
| `standards/` | Coding, design, testing, and release standards; the design contract every surface answers to |
| `docs/dev/`, `docs/user/` | Developer documentation and each app's user guide |
| `docs/legacy/` | The imported apps' pre-monorepo roadmaps, kept for reference only; `todo/` is the plan |
| `docs/reviews/` | Per-section review findings, attestations, the derived findings ledger, run records |
| `docs/phase-runs/` | One findings file per phase run, written as the run goes |
| `docs/captures/<app>/` | Committed captures of rendered surfaces, the visual reference for review |
| `resources/` | Brand, icons, screens |
| `.claude/` | Claude Code skills, the Stop hook, and settings |
| `.conclave/panel.toml` | The review panel wiring: writer, model registry, and every review slot |
| `artifacts/` | Build output (`UseArtifactsOutput`); ignored, never authoritative |
| `build/` | Scratch, caches, and campaign guard state; ignored, never authoritative |

Everything here is Windows-only. The TODO tooling is stdlib Python 3 (`python` on Windows) and needs no install step.

## The decisions this project runs on

- **.NET 11 and C# `latest`**, SDK pinned by `global.json` (the 11.0.100 release candidate until .NET 11 ships; `D00 T02 §8` moves the pin to GA), built from `Photon.slnx`, warnings as errors through `Directory.Build.props`, packages centrally versioned in `Directory.Packages.props`.
- **WPF only, standard controls with custom theming. No WPF-UI** and no other UI framework: a WPF-UI reference is a defect.
- **CommunityToolkit.Mvvm** for view models (`ObservableObject`, `RelayCommand`, source generators). Logic lives in view models and services; code-behind is for view-only concerns.
- **Microsoft.Extensions.DependencyInjection** for composition: one composition root per app, constructor injection, no static service locator.
- **Serilog** for logging: one configuration per app, structured events, one log line per action that changes a document or a setting.
- **xUnit v3** (the `xunit.v3.mtp-off` package, run on VSTest) with **AwesomeAssertions** where fluent assertions are used, run through `dotnet test Photon.slnx`.
- **Shared code goes to `Photon.Core` only when two apps need it.** One app's need stays in that app, with a note naming when it would move. A second copy of a behavior in a second app is a defect; so is a `Photon.Core` type only one app consumes.
- **Per-app versioning.** Each app releases on its own tag: `nodus-v*`, `imago-v*`, `lumen-v*`. A suite release that bundles a set of app versions tags `photon-v*`. No app's version moves because another app shipped.
- **Build output lives under `artifacts/`**, scratch and guard state under `build/`; both are gitignored and neither is ever cited as a record.
- **A dependency is a decision.** Adding a package outside the stack above records the reason in the section that adds it.

## The TODO system

`todo/` is the live execution plan; **format spec: `todo/README.md`.** Markdown is canonical and `build/` holds derived, gitignored projections.

Domains are flat-numbered from `00`, allocated in order, and read from the tree: `00-workspace` (toolchain, solution, gates, CI, this system), `01-core` (`Photon.Core` and `Photon.UI`), `02-nodus`, `03-imago`, `04-lumen`, `05-release` (per-app packaging, signing, tags, the suite bundle), `06-docs`, and `99-manual` (operator-only rows no agent session can perform). Numbers are stable addresses: a new domain appends after the last one. `todo/TODO-00-INDEX.md` is the authority for which exist.

**The plan is bounded** (operator decision, 2026-09-26). `todo/budget.json` caps the sections each phase may hold (open plus shipped), the total at their sum, the backlog, and the new sections one phase run may add; `validate` refuses a breach. New work becomes a section only when it is a defect in shipped or in-flight work, something an acceptance-bar aim requires, or a prerequisite of a planned row, and its phase has room; everything else goes to `todo/backlog.md`, which is never runnable. At a ceiling, merge, supersede, or backlog. Only the operator raises a ceiling, in words a new history entry quotes. The rules are in `todo/README.md` under "The budget and the backlog".

Files are `todo/NN-domain/TODO-NN-short-name.md`. The **Implementation Order table is the dependency graph**: every `## N.` section has exactly one row and vice versa, and a row flips to `[x]` only when a `Verified:` stamp covers it. Cross-references use section marks in the forms `§N`, `TNN §N`, and `DNN TNN §N` as spelled out in `todo/README.md`, and must be bidirectional. Every section sits in exactly one phase table of `todo/implementation-plan.md`.

## Choose the work contract

For TODO work, read the target section, `todo/README.md`, its dependencies, and the applicable skill under `.claude/skills/`: capture through `add-todo`, author a file through `create-todo`, plan a new feature or a new app through `plan-new-feature`, build through `process-todo-section` (gate card: `.claude/skills/process-todo-section/gates.md`), stamp through `review-todo-section`, close a file through `process-todo-file`, run a phase or the plan through `process-phase` or `process-plan`, harden the tree through `groom-plan`.

The lifecycle is: capture, author, validate the plan and source claims, record `Started:`, implement, run the section's gates, commit, independent review, panel review and stamp, then sync the plan. Each section must be executable with zero conversation context. **One section = one commit.** Preserve section addresses and bidirectional cross-references. A TODO Implementation Order row turns `[x]` only with its `Verified:` stamp through the review skill. Do not rewrite a stamped checklist or transfer evidence across changed candidates. File new work with its own owner and dependency.

`/process-plan` is the campaign front door: it audits the plan, starts the run guard (the Stop hook in `.claude/settings.json`, the guard file under `build/`, and a heartbeat job), and runs phase after phase until every row is shipped, parked, or blocked.

## What counts as proof

A Test checkpoint cites one or more of five proofs, spelled out in `todo/README.md`:

1. **Builds clean**: Debug and Release, warnings as errors, analyzers on.
2. **Static analysis clean**: nothing new from the configured analyzers, and `dotnet format --verify-no-changes` clean on the touched projects.
3. **Unit test**: an xUnit test in the solution, cited by name.
4. **Driven run with evidence**: a Serilog log line, a settings readback, a saved file inspected, or a capture under `docs/captures/<app>/`.
5. **Format fidelity proof**: a committed fixture opened, saved, reopened, and compared element by element or pixel by pixel within a stated tolerance. Every file-format reader or writer owes this one.

A checkpoint citing a gate that does not exist yet is unfalsifiable and is not allowed.

## Working rules

- **Output discipline:** bound every command (`dotnet build -v q`, `dotnet test --filter`, `tail`/`head` on logs, field extraction on JSON). Keep full logs in ignored scratch under `build/`.
- **Act, then report:** complete authorized work and report evidence. Explicit operator stop instructions take effect immediately.
- **One writer, and it never reviews itself:** Claude Code is the only writer (operator decision); no other harness edits, commits, or runs campaigns here. Every other model takes part only as a headless reviewer through a slot in `.conclave/panel.toml`, run by `python scripts/panel_slots.py exec <slot>` (GPT review slots run through the `codex` CLI), which names the writer, registers the models, and pins every review role; `scripts/panel_slots.py` refuses a table where any slot shares the writer's family. There are no fallback slots: a failed round waits for the operator. Skills name slots, never models: a re-pin is one edit to that file plus a fresh probe date.
- **Writes are serial:** one session owns the working tree. Check `git status` before building over unfamiliar work.
- **Section atomicity is the candidate range:** one section ships as one logical change, and review fix-loop commits append to that range (never amend); each fix is re-reviewed and the stamp names the whole range. "One section = one commit" never means "one hash".
- **User documents first:** atomic writes, readback, skip-and-report, confirmed destructive paths, an undo for every edit, and originals never written by a non-destructive workflow. Checkpoints prove the failure path too.
- **One suite, shared deliberately:** shared behavior is consumed from `Photon.Core` once two apps need it, never reimplemented in a second app, and never moved there speculatively.
- **Every surface answers to the design contract under `standards/`,** with the captures under `docs/captures/<app>/` as its visual reference. A surface never hardcodes a color, a size, or a spacing value its theme resources name.
- **No em dashes** in authored prose; use `--`, a colon, or a new sentence. One line per paragraph and list item in Markdown.
- **Source of truth:** file formats via their specifications and reference implementations, WPF and .NET behavior via Microsoft Learn, competitor behavior via a driven run of the competitor (with its version), plan state via `todo/`. Disagreements are recorded decisions, not silent reinterpretations.
- **Completion-first, no partial ships:** a runner finishes what it starts: a section, feature, or app is complete only when every micro-step is `[x]`, its checkpoint is quoted from a real run, and review stamped it. Anything genuinely unshippable now files through `add-todo` with an owner (debt with a collector, never a silent drop), and waiting is never a strategy. Reviewers refuse stamps on partial scope.

## The commit hook

`tools/githooks/pre-commit` refuses a commit whose **staged** tree fails `python scripts/todo-graph.py validate`, checked in a temp checkout of the index. It must stay a POSIX shell script with LF endings and index mode `100755`. `tools/provision.ps1` points `core.hooksPath` at `tools/githooks` for each clone; run it once after cloning. A red hook is a defect to fix, never a gate to skip.

## A measurement recorded is a measurement re-checked

`validate` proves the tree is internally consistent. It cannot tell whether a `Current state` block is still **true**, because a stale figure and a correct one look identical as prose. So **a TODO that measures something records it as a claim**, and `scripts/todo-claims.py` re-measures it:

```
<!-- claim: exists src/Nodus/Bezier.sln -->
<!-- claim: absent src/Photon.Core/Photon.Core.csproj -->
<!-- claim: lines src/Nodus/Bezier.Core/Bezier.Core.csproj = 9 -->
```

**When a claim goes stale the TODO is wrong, not the repository.** Fix the claim and the sentence it supports in the same commit, and if the change invalidates the section's reasoning, say so rather than quietly updating a number.

## Unknowns and questions

Answer from source first: the code, the format specification, Microsoft Learn, or a driven run of a competitor. When an unanswered question would change implementation, take a justified default, record that it is a default with its cost of changing, and carry on. Do not stall a section waiting for an answer; do not silently reinterpret a section into something buildable.

## Validation

```powershell
pwsh scripts/check-all.ps1                   # build Debug and Release, test, and every TODO gate below that it runs
dotnet build Photon.slnx -c Release          # the build alone
dotnet test Photon.slnx                      # the whole suite; iterate with --filter
```

```bash
python scripts/todo-graph.py self-test       # must stay green; the run prints its own total
python scripts/todo-graph.py validate        # FATAL blocks; new WARN blocks until fixed or accepted
python scripts/todo-graph.py plan --sync     # re-derive the plan projection after TODO edits
python scripts/todo-graph.py plan --check    # fail if the projection went stale
python scripts/todo-graph.py query ready     # dependency-safe work right now
python scripts/todo-graph.py query blocked   # sections waiting on something
python scripts/todo-graph.py query stats     # tree health
python scripts/todo-graph.py query budget    # sections per phase against each ceiling, the backlog against its cap
python scripts/todo-graph.py query growth --since <ref> --check   # a run's new sections against the per-run cap
python scripts/todo-graph.py resolve 'DNN TNN §N'   # ref -> file, section, deps, status
python scripts/todo-claims.py                # re-measure what the TODOs claim about the repo
python scripts/todo-claims.py --coverage     # name every Current state block nothing re-measures
python scripts/todo-findings.py --check      # fail if docs/reviews/findings.md is stale
python scripts/todo-runs.py --check          # run records agree with the review files
python scripts/campaign_guard.py --self-test # the Stop hook and guard lifecycle, in a throwaway workspace
python scripts/panel_slots.py validate       # the review panel wiring holds
```

Run checks owed by the task. Report only commands actually run, and distinguish static evidence, test output, driven-run output, fidelity output, and review proof.

Use trunk-based `main` for routine work and concise imperative commits. Respect exact candidate identity and one-section scope. Never bypass hooks with `--no-verify`, amend a recorded candidate, or force-push.

## Credentials

Credentials never enter tracked files, arguments, logs, or handoff prose. The code-signing certificate and its password are supplied to the packaging scripts from outside the repository.
