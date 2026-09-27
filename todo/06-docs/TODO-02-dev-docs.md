---
schema_version: 1
id: dev-docs
domain: 06-docs
status: draft
title: "TODO-02 -- Developer Documentation and the Project Site"
depends_on: []
track: D2
---

# TODO-02 -- Developer Documentation and the Project Site

> **Goal:** A contributor can understand the suite from the developer docs alone, and they stay true: the architecture page matches the tree after each restructure, the README shows the real apps, and the user guides are published as a browsable site.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `docs/dev/architecture.md` was written on 2026-09-26 from the old `Description.md` (removed the same day) and describes the target layout, not the current one: `src/Isotone.Core/`, `src/Isotone.UI/`, and `src/Albumen/` do not exist yet. `docs/dev/` also holds `build.md`, `versioning.md`, and `README.md`. The README's screenshots come from `resources/screens/web/`, which are concept renders rather than captures of the built apps. There is no published site; the guides render only on GitHub. **Corrected 2026-09-28:** the README leads with `resources/brand/isotone-cover.png` (labelled a design concept) and its per-app row shows the splash cards; the neon art under `resources/screens/` was removed on 2026-09-28 with the other neon brand images (operator: "Remove the neon banners"), so §2 writes its captures into a new `resources/screens/web/`. GitHub Pages already serves the design system from `.github/workflows/pages.yml` (https://rizonesoft.github.io/Isotone/design/, the root redirecting there), so the guides join that one site rather than a second one.
<!-- claim: exists docs/dev/architecture.md -->
<!-- claim: absent src/Isotone.UI -->
<!-- claim: exists resources/brand/isotone-cover.png -->

## Inputs

- [`docs/dev/architecture.md`](../../docs/dev/architecture.md), [`docs/dev/README.md`](../../docs/dev/README.md) -- what §1 keeps true
- [`README.md`](../../README.md) -- the screenshots §2 replaces (the repository face's owner reviews the change)
- -> XREF: D01 T01 §2 -- the Isotone.UI work whose landing §1 documents
- -> XREF: D04 T14 §7 -- Albumen parity workspace cites §3: the published guide site D04 T14 §7 opens

## Outcome

- `docs/dev/architecture.md` describes the tree as it is, with a project dependency diagram generated from the `.csproj` files so it cannot drift.
- The README's app images are captures of the released apps.
- The user guides are published as a site (GitHub Pages) built from `docs/user/` by a workflow, with the apps' Help, Documentation links pointing at it.

**Adjacency:** all=not-applicable (developer documentation and a static site: no runtime records, settings, or reversible actions)

**Adjacency rationale:** Nothing here runs in an app; the Help links the site changes are one-line edits in each app's Help section.

## Implementation Order

| Order | Section | Deliverable                                        | Depends On                              | Status |
| :---: | :-----: | -------------------------------------------------- | --------------------------------------- | :----: |
|   1   |   §1    | The architecture page matches the tree             | D01 T01 §2, D01 T02 §3                  |  [ ]   |
|   2   |   §2    | README images from real captures                   | D02 T05 §4, D03 T06 §3, D04 T02 §8      |  [ ]   |
|   3   |   §3    | The user guides as a published site                | D06 T01 §4                              |  [ ]   |

---

## 1. The Architecture Page Matches the Tree

Once Stilus is restructured and the two shared libraries exist, the architecture page's "target layout" becomes the actual layout. A hand-drawn dependency picture drifts; one generated from the project files does not.

- [ ] Add `scripts/project-graph.ps1` that reads every `.csproj` in `Isotone.slnx` and emits a Mermaid graph of project references into `docs/dev/architecture.md` between marker comments. Done when: running it twice produces no diff.
- [ ] Rewrite the layout section as current fact, keeping planned parts (Albumen before `D04 T01 §2`) marked planned. Done when: every path in the page exists or is marked planned.
- [ ] Add a check to `scripts/check-all.ps1` that fails when the generated graph is stale. Done when: adding a project reference without regenerating fails the check.
- [ ] Write `docs/dev/debugging.md` (each app's log path under `%LOCALAPPDATA%\Rizonesoft\<App>\logs\`, the debug window, the exception report) and remove its Planned entry from `docs/dev/README.md` (**Groomed 2026-09-28:** the page was listed as planned with no owner). Done when: every path it names exists after a Debug run (quoted).
- [ ] Commit: `"docs: an architecture page generated from the project files"`

**Test checkpoint:** `pwsh scripts/project-graph.ps1` followed by `git diff --exit-code docs/dev/architecture.md` exits 0; after adding a dummy reference in a scratch branch, `pwsh scripts/check-all.ps1` fails on the stale graph. Cheaper substitute that fails: a hand-drawn diagram.

## 2. README Images from Real Captures

The README shows concept renders. Once the apps are released, the images should show the real apps. The README belongs to the repository-face owner; this section supplies the images and a one-line change per image.

- [ ] Produce web-sized captures (1,600 px wide, JPEG quality 85) of each released app's main window with a sample document, from `docs/captures/<app>/`, into `resources/screens/web/`. Done when: three new images exist, each under 400 KB.
- [ ] Replace the README's image references with them and credit nothing that is not in the repository. Done when: the README renders the new images on GitHub (checked on the pushed branch).
- [ ] Commit: `"docs: show the released apps in the README"`

**Requires:** display-session -- taking the web captures of each released app needs an interactive desktop
**Test checkpoint:** each README image path exists and is a capture of the built app (its capture record under `docs/captures/<app>/` names the commit); `Get-Item` sizes are under 400 KB (quoted). Cheaper substitute that fails: keeping the concept renders.

## 3. The User Guides as a Published Site

Help, Documentation links to GitHub's Markdown view today. A small static site built from `docs/user/` reads better and can be searched.

- [ ] Choose the site generator by recorded decision (a static generator run in CI with a license compatible with the repository, for example MkDocs with the Material theme, or plain GitHub Pages Jekyll) in `docs/dev/decisions.md`. Done when: the entry exists.
- [ ] Extend `.github/workflows/pages.yml` to build the guides from `docs/user/` into `_site/guide/` beside `_site/design/`, add `docs/user/**` to its path triggers, and make `_site/index.html` a landing page linking both instead of a redirect (**Corrected 2026-09-28:** said add a separate `docs.yml`; a repository has one Pages site, so a second deploying workflow would overwrite the design page). Done when: a push produces a green `design-pages` run and https://rizonesoft.github.io/Isotone/guide/ and .../design/ both return 200 (quoted).
- [ ] Point each app's Help, Documentation at its section of the site. Done when: each app opens the site URL (driven, log line quoted).
- [ ] Commit: `"docs: publish the user guides as a site"`

**Requires:** display-session -- confirming each app's Help link opens the site needs an interactive desktop

**Test checkpoint:** the `pages.yml` run is `success` and the site URL returns 200 for each app's guide (quoted `Invoke-WebRequest` status codes). Cheaper substitute that fails: linking to raw Markdown.

## Verification

- [ ] The architecture graph check passes in `pwsh scripts/check-all.ps1`
- [ ] The site is live and each app links to it
- [ ] `python scripts/todo-graph.py validate` clean
