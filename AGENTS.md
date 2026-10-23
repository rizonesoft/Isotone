# AGENTS.md

Agent instructions for this repository. Human orientation lives in `README.md`. Claude Code loads this file through the `CLAUDE.md` import stub.

## What this project is

`Isotone` is the monorepo of the **Isotone Graphics Suite**: three standalone creative applications for Windows 11, built on .NET 11 and WPF.

| App | Kind | State |
| --- | ---- | ----- |
| **Stilus** | Vector editor (Illustrator alternative) | Imported from Bezier under `src/Stilus/`; projects still named `Bezier.*` until renamed |
| **Gesso** | Raster editor (Photoshop alternative) | Imported under `src/Gesso/` |
| **Albumen** | Digital darkroom, photo manager, and fast image viewer (Lightroom, ACDSee, and IrfanView alternative) | Planned in `todo/04-albumen/`; no code yet |
| **Tinctura** | Color picker and color studio | Added 2026-10-23; planned by the campaign in Phases 41 and 42 from `todo/07-tinctura/` |
| **Capio** | Screenshot and screen recording app (ShareX and PicPick alternative: capture, annotate, record) | Added 2026-10-23; planned by the campaign in Phases 43 and 44 from `todo/08-capio/` |
| **Folium** | Page layout and publishing (InDesign alternative) | Added 2026-10-23; planned by the campaign in Phases 45 and 46 from `todo/09-folium/` |
| **Isotone.Core** | Shared non-UI library | Planned; created when two apps first need the same code |
| **Isotone.UI** | Shared WPF library (house style, shared controls and windows) | Planned; created when the first duplicated control moves out of Stilus and Gesso |

**Develop together, distribute separately.** The apps share one repository, one solution (`Isotone.slnx`), one set of gates, and one plan, but each ships as its own product: its own installer, its own version, its own changelog, its own user guide. An app may never depend at runtime on another app, and nothing it ships may assume another app is installed.

| Path | Purpose |
| ---- | ------- |
| `src/Stilus/` | Stilus, the vector editor |
| `src/Gesso/` | Gesso, the raster editor (`src/` projects and `tests/` test projects inside it) |
| `src/Albumen/` | Albumen, the darkroom (planned) |
| `src/Isotone.Core/`, `src/Isotone.UI/` | Shared libraries, only what two apps need (planned); the target layout is in `docs/dev/architecture.md` |
| `Isotone.slnx` | The one solution every build, test, and publish goes through |
| `scripts/` | `build.ps1`, `publish.ps1`, `package.ps1`, `release-manifest.ps1` (release body and update feed), `check-all.ps1`, and the stdlib Python TODO tooling (`todo-graph.py`, validator, claims, findings, runs, review prompt, panel slots and delegation checks, weakening scan, campaign guard, the parity checks `todo-parity.py`), the dependency pull request merger `merge_prs.py`, the section-boundary CI watch `ci_watch.py`, the pin checks `check-dotnet-pin.py`, `check-vulnerable-packages.py`, and `check-local-tools.py` with their shared `lib/pin_proposal.py` and `lib/pin_sources.py`, with tests under `tests/` |
| `tools/` | `provision.ps1` (sets up a clone, including the commit hook) and `githooks/pre-commit` |
| `todo/` | The live execution plan; read `todo/README.md` before authoring or implementing |
| `todo/implementation-plan.md` | Ordered phase plan; its boxes are synchronized through `scripts/todo-graph.py` |
| `todo/budget.json`, `todo/backlog.md` | The budget decisions and their history (no caps since 2026-09-27); the uncapped list of deferred ideas that are not sections, which loses nothing without a trace |
| `standards/` | Coding, design, testing, and release standards; `ui.md` is the UI standard every surface answers to, `design-contract.md` the binding contract that holds the code to `docs/design/`, and `delegation.md` the routing of work to subagents |
| `docs/dev/`, `docs/user/` | Developer documentation and each app's user guide |
| `docs/design/` | The Isotone Interface design system, canonical: `tokens.json` (the source of every UI value), the component specs, the shell layout, the app icon guide, and `EDITING.md` (how to change it and regenerate the published page at https://rizonesoft.github.io/Isotone/design/) |
| `docs/legacy/` | The imported apps' pre-monorepo roadmaps, kept for reference only; `todo/` is the plan |
| `docs/parity/` | The parity evidence for all three apps: the Illustrator 30.8 and CorelDRAW 2026 inventories with the Stilus catalog (`stilus-parity.md`), the Photoshop 27.10, Affinity 3.3, and GIMP 3.2.6 inventories with the Gesso catalog (`gesso-parity.md`), the Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 inventories with the Albumen catalog (`albumen-parity.md`), one status per feature, and the three section designs the parity TODO files were authored from |
| `docs/reviews/` | Per-section review findings, attestations, the derived findings ledger, run records |
| `docs/phase-runs/` | One findings file per phase run, written as the run goes |
| `docs/captures/<app>/` | Committed captures of the imported apps' surfaces, a before record only (never a fidelity source) |
| `docs/captures/golden/` | Approved golden renders of every control and surface, per state, theme, Highlight, density, and scale; written only by `review-todo-section` through the visual harness's approve path (`standards/design-contract.md`) |
| `resources/` | Brand, icons, screens |
| `.claude/` | Claude Code skills, the delegate agent definitions under `agents/`, the output and safety rule under `rules/`, the Stop hook, the agent-routing hook, and settings. Every file here is Isotone's own: the operator cut the link to the Conclave SDK on 2026-10-21, so nothing is synced from, compared with, or refreshed from another repository |
| `.conclave/reviewers.toml` | The reviewer pin (schema 2: one `[writer]`, Claude Code on Opus 5.5, and one `[reviewer]` with its CLI, model, and effort, no fallback), read by `scripts/review-dispatch.py`, which runs every review round |
| `.conclave/automations/` | The scheduled jobs (Windows Task Scheduler, under `\Isotone\`, in RectoPDF's shape): the task list `tasks.json` with the checks only this PC can see and the `isotone-pr-merge` fallback, the runner, alert, and installers, and the README listing both those and what the daily `.github/workflows/pins.yml` and Dependabot keep current on GitHub (the .NET 11 SDK with its runtime packages, vulnerable packages, NuGet, Actions) |
| `artifacts/` | Build output (`UseArtifactsOutput`); ignored, never authoritative |
| `build/` | Scratch, caches, and campaign guard state; ignored, never authoritative |

Everything here is Windows-only. The TODO tooling is stdlib Python 3 (`python` on Windows) and needs no install step.

## The decisions this project runs on

- **We build a better product, not a clone** (operator principle 2026-10-23: "we are not just creating another clone, we are building a better product. We are not scared to take on the giants and do things better. We do not just implement a feature, we optimise it, we thing of ways to improve it, and we blow the competition away. When people use our software, they should think, 'how is this possible'. We do not take shortcuts or workarounds and we are not scared of something being difficult or complicated."). Every feature first matches its competitor where users expect it (the layout maps, the terminology, the parity rows), then beats it: it is planned with an `**Exceed:**` paragraph naming at least one concrete, measurable improvement (faster or lighter than the competitor measured on the reference machine, a workflow step removed, a capability the competitor lacks, a quality it misses), built with the item that delivers it, and proved by its Test checkpoint; the completion review checks that the improvement is real. Difficulty or complexity is never a reason to scope a feature or an improvement down, and no improvement is a shortcut or a workaround. Think outside the box: question how the competitor does it, and do it better.
- **The stack is moving to C++23 with our own UI** on Win32, Direct2D, DirectWrite, and Direct3D (operator decision 2026-10-22: "I feel that C++ and our own UI will get is much closer to Photoshop quality."; the standard pinned to C++23 the same day; `docs/dev/decisions.md`). The architecture, toolchain, and migration are specified in `docs/specs/2026-10-22-native-stack-design.md`, and the TODO tree is re-planned from it. Until that re-plan lands, the .NET and WPF bullets below describe the imported C# code, which stays a behavior reference and is not extended.
- **.NET 11 and C# `latest`**, SDK pinned by `global.json` (the 11.0.100 release candidate until .NET 11 ships; `D00 T02 §8` moves the pin to GA), built from `Isotone.slnx`, warnings as errors through `Directory.Build.props`, packages centrally versioned in `Directory.Packages.props`.
- **WPF only, standard controls with custom theming. No WPF-UI** and no other UI framework: a WPF-UI reference is a defect.
- **CommunityToolkit.Mvvm** for view models (`ObservableObject`, `RelayCommand`, source generators). Logic lives in view models and services; code-behind is for view-only concerns.
- **Microsoft.Extensions.DependencyInjection** for composition: one composition root per app, constructor injection, no static service locator.
- **Serilog** for logging: one configuration per app, structured events, one log line per action that changes a document or a setting.
- **xUnit v3** (the `xunit.v3.mtp-off` package, run on VSTest) with **AwesomeAssertions** where fluent assertions are used, run through `dotnet test Isotone.slnx`.
- **Shared code goes to `Isotone.Core` only when two apps need it.** One app's need stays in that app, with a note naming when it would move. A second copy of a behavior in a second app is a defect; so is an `Isotone.Core` type only one app consumes.
- **Per-app versioning.** Each app releases on its own tag: `stilus-v*`, `gesso-v*`, `albumen-v*`. A suite release that bundles a set of app versions tags `isotone-v*`. No app's version moves because another app shipped.
- **Build output lives under `artifacts/`**, scratch and guard state under `build/`; both are gitignored and neither is ever cited as a record.
- **Ownership and distribution** (operator decisions 2026-09-27): the copyright holder is Rizonetech (Pty) Ltd ("Copyright (C) 2025-2026 Rizonetech (Pty) Ltd"; "Rizonesoft is a brand of Rizonetech (Pty) Ltd."), and the publisher users see stays Rizonesoft. The names and icons are trademarks under `TRADEMARKS.md`. Binaries ship only from rizonesoft.com, served from `download.rizonesoft.com` (`<slug>/<version>/<file>`, the update feed at `update/<slug>.json`); a GitHub release carries notes, source archives, the SHA-256 table, and links, never an installer or ZIP. The product page is one value, `ISOTONE_SITE_URL` (default `https://www.rizonesoft.com/`). Contributors keep their copyright under the GPL with the DCO; a CLA is an open operator decision (`D99 T01 §10`). The license is GPL-3.0 plus one section 7 additional permission (operator decision 2026-10-19, `LICENSE-EXCEPTION.md`): the apps may be conveyed combined with AvalonDock, whose Ms-PL the FSF lists as GPL-incompatible. It names AvalonDock only: any other GPL-incompatible dependency is refused or needs its own operator decision, and `scripts/publish.ps1` ships both files in every publish folder.
- **Names** (operator decision 2026-09-27, "doit, let's replace all 4 names", then "Let's go with latin names"): after a trademark pre-screen found live software marks on the old names, the suite and apps were renamed before any release: Photon Graphics Suite to **Isotone Graphics Suite** (the operator owns isotone.co.za; the name of the operator's older `rizonesoft/isotone` CMS repository was freed for it), Nodus to **Stilus** (vector), Imago to **Pinxit** and then, on 2026-09-28, to **Gesso** (raster; the operator found Pinxit hard to say and remember), and Lumen to **Albumen** (darkroom). Paths, projects, namespaces, tags (`stilus-v`, `gesso-v`, `albumen-v`, `isotone-v`), tokens, and icons follow. Three verbatim operator quotes, the budget history, historic `git show` paths, and `docs/legacy/` keep the old names. The GitHub repository became `rizonesoft/Isotone` the same day (GitHub redirects the old `rizonesoft/Photon` links), with the design page at https://rizonesoft.github.io/Isotone/design/.
- **A dependency is a decision.** Adding a package outside the stack above records the reason in the section that adds it.

## The TODO system

`todo/` is the live execution plan; **format spec: `todo/README.md`.** Markdown is canonical and `build/` holds derived, gitignored projections.

Domains are flat-numbered from `00`, allocated in order, and read from the tree: `00-workspace` (toolchain, solution, gates, CI, this system), `01-core` (`Isotone.Core` and `Isotone.UI`), `02-stilus`, `03-gesso`, `04-albumen`, `05-release` (per-app packaging, signing, tags, the suite bundle), `06-docs`, `07-tinctura`, `08-capio`, `09-folium` (the three apps added on 2026-10-23), and `99-manual` (operator-only rows no agent session can perform). Numbers are stable addresses: a new domain appends after the last one. `todo/TODO-00-INDEX.md` is the authority for which exist.

**Nothing in the plan is capped, and no feature is left behind** (operator decisions, 2026-09-26 and 2026-09-27: "the cap is worrying me, because I'm worried features will be left behind."). Sections the operator asks for in an attended session carry nothing extra. A section a campaign files on its own carries `**Origin:** discovered run=<run id> <YYYY-MM-DD>` under its heading (provenance for reporting, never a quota) and must be a defect in shipped or in-flight work, something an acceptance-bar aim requires, or a prerequisite of a planned row; anything else goes to `todo/backlog.md` (never runnable, never capped). A backlog entry leaves only by promotion (a live section carries its source key), by merge (the survivor keeps ``merged: `<key>` ``), or with the operator's words in a removal record under `## Removed with operator approval`; `validate` fails anything else as `backlog-dropped`. Every release section carries a backlog review item and stamps only when every backlog entry for its app or `suite` (every entry for `isotone-v`) was promoted or carries a `reviewed: <tag> <date> ...` field quoting the operator's deferral. `todo/budget.json` records the decisions (schema 3, both caps `null`); only the operator changes it, in words a new history entry quotes. The rules are in `todo/README.md` under "The budget and the backlog". The structural limits (30 items per section, 55 sections per file) are unchanged. The operator's 2026-09-26 parity decision ("For Nodus, we need to add all(and I mean), all CorelDraw features and All Illustrator Features.") added the Stilus parity phases 4 to 13, and the operator's decision the same day for Gesso ("now, imago, all the photoshop and at least 2 other similar popular programs of the same type. All features without leaving anything behind.") added the Gesso parity phases 16 to 27, renumbering Albumen, distribution, and the later phases to 28 to 32. The operator's 2026-09-27 decision for Albumen ("Now Lumen. I want features from Lightroom, but I've alwyas been loving ACDSee photo manager and IrfanView") added the Albumen parity phases 30 to 39 after Albumen 0.1.0, on three pillars (a fast default image viewer, browsing without importing, and batch tools as core Albumen features), renumbering distribution to 40 and the Gesso and Stilus shared-decoder imports to 41, and retiring the old Albumen accessibility phase into Phase 39; Albumen originals are safe by default with opt-in writes ("Safe by default, opt-in writes"). Suite-wide scripting and macros, action-based batch processing, video and audio, and animation were deferred to after the first release; on 2026-09-27, because the operator worried "features will be left behind", they became real sections in the post-release Phases 48 to 51 (automation, video and audio with animation, on-device models with the GPU develop path, and Albumen's remaining formats through Stilus's moved CAD readers, an own SWF parser, an optional user-installed GDAL, and clean-room analysis), each phase ending in app releases and the last in the `isotone-v1.1.0` suite bundle. A catalog row in `docs/parity/stilus-parity.md`, `docs/parity/gesso-parity.md`, or `docs/parity/albumen-parity.md` changes status in the same commit that changes the section or backlog entry it names. On 2026-10-23 the operator added three apps ("let's als oinclude planning for 3 more additions to the suite. Indesign clone, professional screenshot app, modeled after ShareX and PickPick, but not all the features. and a professional color picker and color studio"), named Tinctura, Capio, and Folium, placed after the first suite release in Phases 41 to 46 (renumbering the post-release phases to 47 to 51), each planned by the campaign just ahead of building it from its `TODO-01` (`docs/dev/decisions.md`, "2026-10-23: Three more apps").

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
- **One writer, and it never reviews itself:** Claude Code on Claude Opus 5.5 is always the solo writer (operator decision 2026-10-23, "I decided that Opus 5.5 will always be the solo writer"); no other harness or model edits, commits, or runs campaigns here. The writer session may delegate to its own Claude subagents (below), and stays the writer of record. Every other model takes part only as a headless reviewer: every review round (the panel rounds, the completion review, the architecture gate, the plan review, the stamp review, and the independent pass) runs through `python scripts/review-dispatch.py --writer claude` on `.conclave/reviewers.toml` (operator decision 2026-10-21, "Full adoption", which retired the panel slots). The pin's shape (schema 2, 2026-10-23) holds exactly one `[writer]` (`claude`, `claude-opus-5-5`) and one `[reviewer]`: GPT-6.1 Sol through the `codex` CLI at medium effort (operator decision 2026-10-23, "set the reviewer effort level to medium"; Sol was pinned at xhigh on 2026-10-22, "Pin GPT6.1-sol at xhigh as the reviewer in place of Astra 6 medium without stopping", replacing GPT-6 Astra at medium, the 2026-10-21 pin), with no fallback (keeping the 2026-09-25 decision): a round that returns no review is retried with backoff over hours and then parks only that section while the campaign carries on (operator decision 2026-10-23, `docs/dev/decisions.md`, "The unattended campaign"). A review loop runs at most 33 rounds (operator decision 2026-10-23, raised from 22: "This is an extremely complicated build, so let's bump the cap up to 33") and, from round 9, stops on a round whose findings are all P3 (operator decision 2026-10-21, RectoPDF's loop; `review-todo-section`, The loop). The dispatcher refuses a second writer, a fallback, and a reviewer of the writer's family, and `python scripts/panel_slots.py validate` also refuses a pin whose writer model is not the recorded writer. Work outside a TODO section gets its independent review the same way, through the `independent-review` skill. `reviewers.toml` is the only review pin (renamed from `panel.toml` on 2026-10-20, operator instruction: "rename panel.toml to reviewers.toml and update all references."). Skills name the writer, never a model: a re-pin is one edit to that file.
- **Writes are serial:** one session owns the working tree. Check `git status` before building over unfamiliar work.
- **Dependency pull requests merge at section boundaries** (operator request 2026-10-21, "merge PRs inside the loop, at section boundaries"): `python scripts/merge_prs.py run --campaign` runs after each stamp push's green CI read-back and merges at most one green Dependabot or pins pull request (never a .NET SDK pin, which is `D00 T02 §8`'s), by rebase, only when the tree is clean, `HEAD` equals `origin/main`, and no section is in progress; the `isotone-pr-merge` task does the same when no campaign runs, and `merge_prs.py recover` (which never merges) settles any earlier merge's intent before a campaign's first or resumed section. A failure stops it and leaves the pull request for the operator.
- **Section atomicity is the candidate range:** one section ships as one logical change, and review fix-loop commits append to that range (never amend); each fix is re-reviewed and the stamp names the whole range. "One section = one commit" never means "one hash".
- **User documents first:** atomic writes, readback, skip-and-report, confirmed destructive paths, an undo for every edit, and originals never written by a non-destructive workflow. Checkpoints prove the failure path too.
- **One suite, shared deliberately:** shared behavior is consumed from `Isotone.Core` once two apps need it, never reimplemented in a second app, and never moved there speculatively.
- **Every surface answers to the design contract, `standards/design-contract.md` (binding):** `docs/design/` is the source and code implements it 1:1 (exact tokens, geometry within 1 DIP at 100, 150, and 200 percent, every state and theme the spec lists, approved goldens); a change to how something looks goes to `docs/design/` first. Every surface section carries a `**Design:**` line (`todo/README.md`, Surface fidelity), `scripts/design-lint.py` fails any new literal color, size, or font in the UI sources, and a deviation needs a `**Design deviation:**` line with a follow-up section. A surface never hardcodes a color, a size, or a spacing value its theme resources name.
- **UI follows `standards/ui.md`;** `docs/design/tokens.json` is canonical and the `Isotone.UI` theme dictionaries are generated from it, never hand-edited; after a design change, regenerate the design page as `docs/design/EDITING.md` describes.
- **No em dashes** in authored prose; use `--`, a colon, or a new sentence. One line per paragraph and list item in Markdown.
- **Source of truth:** file formats via their specifications and reference implementations, WPF and .NET behavior via Microsoft Learn, competitor behavior via a driven run of the competitor (with its version), plan state via `todo/`. Disagreements are recorded decisions, not silent reinterpretations.
- **Completion-first, no partial ships:** a runner finishes what it starts: a section, feature, or app is complete only when every micro-step is `[x]`, its checkpoint is quoted from a real run, and review stamped it. Anything genuinely unshippable now files through `add-todo` with an owner (debt with a collector, never a silent drop), and waiting is never a strategy. Reviewers refuse stamps on partial scope.

## Subagents

- Subagents read and run; they never write. Every Claude subagent declares an explicit `tools:` list without Edit, Write, MultiEdit, NotebookEdit or `*`. The main loop makes every change and verifies what subagents return. `python scripts/panel_slots.py validate` refuses a definition that grants a write tool, and the `agent-gate` hook refuses a fork or a built-in agent, both of which carry edit tools.
- **Delegate within the bar, never below it** (operator decision 2026-10-01): research, gate runs, and the first-pass review sweep go to the read-only `.claude/agents/` subagents (`isotone-researcher`, `isotone-verifier`, `isotone-reviewer`, `code-explorer`, `debug-evidence`, `git-runner`, `test-runner`, and `mutation-tester`, which mutates only a scratch copy outside the repository), each naming the delegate alias and effort that `scripts/panel_slots.py` pins (`DELEGATE`: Sonnet at high effort), under `standards/delegation.md`. The lead session writes every change, code and documentation prose alike (operator decision 2026-10-02: "I am not confortable with having a sonnet writer"; the last writing delegate, `isotone-docs`, was removed on 2026-10-17), and keeps architecture, consequential design, security, privacy, data integrity, integration, every commit and record, and final acceptance; every gate, the independent review, and the GPT panel run unchanged. Briefs are bounded, with falsifiable acceptance criteria and one corrected re-brief at most before the lead takes the work back or escalates. A scope check after every delegate proves it wrote nothing. Evidence the lead quotes comes from logs it read, never from a delegate's summary.

## The commit hook

`tools/githooks/pre-commit` refuses a commit whose **staged** tree fails `python scripts/todo-graph.py validate` or `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json`, checked in a temp checkout of the index. It must stay a POSIX shell script with LF endings and index mode `100755`. `tools/githooks/commit-msg` strips any AI-assistant attribution (a `Co-Authored-By:` trailer naming Claude, Anthropic, or another assistant, and "Generated with" footers) from every commit message, so GitHub never lists an assistant as a contributor (operator decision 2026-09-28); never add such lines to commits or pull requests, and keep `.claude/settings.json`'s `includeCoAuthoredBy: false` and empty `attribution`. `tools/provision.ps1` points `core.hooksPath` at `tools/githooks` for each clone; run it once after cloning. A red hook is a defect to fix, never a gate to skip.

## A measurement recorded is a measurement re-checked

`validate` proves the tree is internally consistent. It cannot tell whether a `Current state` block is still **true**, because a stale figure and a correct one look identical as prose. So **a TODO that measures something records it as a claim**, and `scripts/todo-claims.py` re-measures it:

```
<!-- claim: exists src/Stilus/Bezier.sln -->
<!-- claim: absent src/Isotone.Core/Isotone.Core.csproj -->
<!-- claim: lines src/Stilus/Bezier.Core/Bezier.Core.csproj = 9 -->
```

**When a claim goes stale the TODO is wrong, not the repository.** Fix the claim and the sentence it supports in the same commit, and if the change invalidates the section's reasoning, say so rather than quietly updating a number.

## Unknowns and questions

Answer from source first: the code, the format specification, Microsoft Learn, or a driven run of a competitor. When an unanswered question would change implementation, take a justified default, record that it is a default with its cost of changing, and carry on. Do not stall a section waiting for an answer; do not silently reinterpret a section into something buildable.

## Validation

```powershell
pwsh scripts/check-all.ps1                   # build Debug and Release, test, and every TODO gate below that it runs
dotnet build Isotone.slnx -c Release          # the build alone
dotnet test Isotone.slnx                      # the whole suite; iterate with --filter
```

```bash
python scripts/todo-graph.py self-test       # must stay green; the run prints its own total
python scripts/todo-graph.py validate        # FATAL blocks; new WARN blocks until fixed or accepted
python scripts/todo-graph.py plan --sync     # re-derive the plan projection after TODO edits
python scripts/todo-graph.py plan --check    # fail if the projection went stale
python scripts/todo-graph.py query ready     # dependency-safe work right now
python scripts/todo-graph.py query blocked   # sections waiting on something
python scripts/todo-graph.py query stats     # tree health
python scripts/todo-graph.py query plan      # the plan as JSON (title, phases, every row with its status), the shape the Conclave editor extension reads
python scripts/todo-graph.py query budget    # sections and discovered sections per phase, discovered sections per run (provenance), the backlog count
python scripts/todo-graph.py query growth --since <ref>   # a run's added sections (discovered ones with their run) and backlog changes
python scripts/todo-graph.py resolve 'DNN TNN §N'   # ref -> file, section, deps, status
python scripts/todo-claims.py                # re-measure what the TODOs claim about the repo
python scripts/todo-claims.py --coverage     # name every Current state block nothing re-measures
python scripts/todo-findings.py --check      # fail if docs/reviews/findings.md is stale
python scripts/todo-runs.py --check          # run records agree with the review files
python scripts/campaign_guard.py --self-test # the Stop hook and guard lifecycle, in a throwaway workspace
python scripts/panel_slots.py validate       # the reviewer pin (dispatcher rules plus no fallback), the delegate pin, and the agent definitions hold
python scripts/panel_slots.py --self-test    # the pin rules, delegate, audit, agent-gate, and shell-gate logic
python scripts/review-dispatch.py --check-pin --json   # the reviewer pin loads under the dispatcher's rules, and which reviewer CLIs are on PATH
python scripts/tests/test_review_dispatch.py  # the dispatcher's routing, read-only invocations, records, and --keep, with fake CLIs
python scripts/panel_slots.py delegate-probe # live: the delegate alias still serves the pinned model at the pinned effort
python scripts/panel_slots.py delegate-audit # this session's subagents ran at the pin (none below it)
python scripts/weakening-scan.py --base <rev> # every hunk that could weaken an implementation, for the lead to clear
python scripts/weakening-scan.py --snapshot <file>; python scripts/weakening-scan.py --scope <file> --   # a delegate wrote nothing and changed no ref, config, or remote
python scripts/weakening-scan.py --self-test  # the scan's own fixtures
python scripts/ci_watch.py                    # every workflow's latest run on main, scheduled ones included, red ones named (campaign section boundaries)
python scripts/ci_watch.py --self-test        # the watch's own fixtures
python scripts/completion_check.py --self-test  # the completion review's reply gate
python scripts/tests/test_automations.py      # the scheduled tasks, their runner, alert, and installers
python scripts/tests/test_pin_automations.py  # the pin checks, the notice and pull-request plumbing, and the settings hook scripts
python scripts/check-dotnet-pin.py check      # the .NET SDK pin is the newest release of its channel
python scripts/design-lint.py --baseline docs/design/.lint-baseline.json   # no new design-contract violation in the UI sources
python scripts/design-lint.py --self-test    # the lint's own fixtures
python scripts/todo-graph.py query design    # surfaces with a Design line, the baseline, open deviations
python scripts/render-design-reference.py    # design reference renders + side-by-side report under build/design-reference/
```

Run checks owed by the task. Report only commands actually run, and distinguish static evidence, test output, driven-run output, fidelity output, and review proof.

Use trunk-based `main` for routine work and concise imperative commits. Respect exact candidate identity and one-section scope. Never bypass hooks with `--no-verify`, amend a recorded candidate, or force-push.

## Credentials

Credentials never enter tracked files, arguments, logs, or handoff prose. The code-signing certificate and its password are supplied to the packaging scripts from outside the repository.
