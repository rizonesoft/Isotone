---
schema_version: 1
id: operator-setup
domain: 99-manual
status: draft
title: "TODO-01 -- Operator Setup (Manual)"
depends_on: []
---

# TODO-01 -- Operator Setup (Manual)

> **Goal:** The steps no agent session can perform are done by the operator from exact instructions: the repository's About bar, topics, and social preview are set; `main` is protected by the real required checks; a code-signing certificate exists and is available to the packaging scripts without entering the repository; the licenses of the app icon art are confirmed; and each app's accent color is chosen.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The repository is `github.com/rizonesoft/Photon` with default settings as far as this plan knows. `resources/brand/social-preview.jpg` exists for the social preview. The CI checks are named `build` (workflow `build.yml`) and `plan-gates` (workflow `plan.yml`). There is no code-signing certificate (operator statement, 2026-09-26). The app icon candidates `resources/icons/art-and-design.png` (Imago) and `resources/icons/lens.png` (Lumen) arrived with the initial commit with no recorded source or license. The design contract in `standards/shared.md` leaves each app's accent color to the operator. Until `D00 T01 §2` ships, these rows cannot carry the `**Requires:** operator` mark; they depend on that section so no runner takes them before it does. **Corrected 2026-09-27:** the operator answered three of these rows that day: the social preview is uploaded (§1), the operator holds the rights to `resources/icons/art-and-design.png` and `resources/icons/lens.png` (§4), and the accents are chosen and recorded in `standards/shared.md` (§5); what each section still owes is its record and its verification, and every row still flips only through a review stamp. **Corrected 2026-09-27, later the same day:** the §4 answer is superseded. The operator chose project-created icons (Direction C, "C it is"), so `resources/icons/art-and-design.png`, `resources/icons/lens.png`, and `resources/icons/nodus_512.png` were removed, and `resources/icons/README.md` records every app icon as created for the project on 2026-09-27 and licensed GPL-3.0 with the repository, with no third-party art.
<!-- claim: exists resources/brand/social-preview.jpg -->
<!-- claim: absent resources/icons/art-and-design.png -->
<!-- claim: absent resources/icons/lens.png -->
<!-- claim: exists resources/icons/README.md -->

## Inputs

- `https://github.com/rizonesoft/Photon` -- every click path below starts here, logged in as the owner
- [`.github/workflows/build.yml`](../../.github/workflows/build.yml), [`.github/workflows/plan.yml`](../../.github/workflows/plan.yml) -- the check names §2 requires
- [`standards/release.md`](../../standards/release.md) -- the signing policy §3 satisfies
- -> XREF: D00 T01 §2 -- adds the `operator` requirement these rows carry once it ships
- -> XREF: D05 T01 §2 -- the signing plumbing that consumes §3's certificate
- -> XREF: D00 T03 §3 -- the app icon raster export (generates the rasters of the project-created icons whose license §4 confirms)

## Outcome

- The repository page shows a description, topics, and the social preview.
- `main` refuses direct pushes that skip the `build` and `plan-gates` checks.
- A code-signing certificate is installed where `scripts/sign.ps1` can use it by thumbprint, or a cloud signing account is configured, and nothing about it is in the repository.
- `resources/icons/README.md` records a confirmed license for every icon the apps ship.
- The design contract names each app's accent color.

**Adjacency:** all=not-applicable (operator actions in GitHub settings and vendor accounts: no runtime behavior, no records, no reversible user actions)

**Adjacency rationale:** Every row is a click path or a purchase; the agent-side work each enables is owned by the section it names.

## Implementation Order

| Order | Section | Deliverable                                   | Depends On             | Status |
| :---: | :-----: | --------------------------------------------- | ---------------------- | :----: |
|   1   |   §1    | About bar, topics, and social preview         | D00 T01 §2             |  [ ]   |
|   2   |   §2    | Branch protection with the required checks    | D00 T01 §2, D00 T01 §5 |  [ ]   |
|   3   |   §3    | A code-signing certificate                    | D00 T01 §2             |  [ ]   |
|   4   |   §4    | Confirm the icon art licenses                 | D00 T01 §2             |  [ ]   |
|   5   |   §5    | Choose each app's accent color                | D00 T01 §2             |  [ ]   |

---

## 1. About Bar, Topics, and Social Preview

The About bar is the repository's first impression and the social preview is its face in every link. Both need the owner's logged-in session.

**Corrected 2026-09-27:** the operator uploaded the social preview (`resources/brand/social-preview.jpg`) on 2026-09-27, so its item is now a verification of the upload rather than the click path; the description and topics are still owed.

- [ ] Set the description. Done when: the repository page shows it under the name.
  1. Open `https://github.com/rizonesoft/Photon` logged in as the owner.
  2. Click the gear icon beside **About** on the right.
  3. Paste the one-line description from the top of `README.md` into **Description**, then click **Save changes**.
- [ ] Set the topics. Done when: the About bar lists them.
  1. Open the About gear again.
  2. In **Topics**, add: `graphics`, `vector-editor`, `image-editor`, `raw-processing`, `wpf`, `dotnet`, `windows`, `open-source`.
  3. Click **Save changes**.
- [ ] Confirm the social preview the operator uploaded on 2026-09-27 is the committed image. Done when: **Settings**, **Social preview** at `https://github.com/rizonesoft/Photon/settings` shows `resources/brand/social-preview.jpg`, and a logged-out link unfurl shows it (capture).
- [ ] Agent verification: the agent reads `gh repo view rizonesoft/Photon --json description,repositoryTopics` and quotes it. Done when: the description and all eight topics are quoted.
- [ ] Commit: `"docs: record the repository About bar setup"` -- the operator ticks the items above in the GitHub web editor; the agent verifies, ticks its item, and commits.

**Test checkpoint:** `gh repo view rizonesoft/Photon --json description,repositoryTopics` returns the description and the eight topics; a logged-out browser shows the social preview in a link unfurl (capture). Cheaper substitute that fails: trusting the settings form without reloading the public page.

## 2. Branch Protection with the Required Checks

A protected `main` keeps a red build from landing. The checks must be the real job names from the workflows, which exist only after `D00 T01 §5` has run them once.

- [ ] Protect `main`. Done when: the rule lists both checks.
  1. Open `https://github.com/rizonesoft/Photon/settings/rules` (or **Settings**, **Branches**), click **New branch ruleset** (or **Add branch protection rule**).
  2. Target `main`; enable **Require status checks to pass**; search and add `build` and `plan-gates`.
  3. Enable **Block force pushes**; leave **Require a pull request** off (the single-writer workflow commits to `main` directly; revisit if contributors join).
  4. Save.
- [ ] Agent verification: `gh api repos/rizonesoft/Photon/rules/branches/main` lists the required checks. Done when: the output is quoted.
- [ ] Commit: `"docs: record branch protection on main"` -- ticked as in §1.

**Test checkpoint:** the `gh api` output names `build` and `plan-gates` as required; a test push of a commit that fails `plan-gates` (on a scratch branch merged by PR) is blocked. Cheaper substitute that fails: a rule with no required checks.

## 3. A Code-Signing Certificate

Unsigned installers show SmartScreen warnings. Signing (`D05 T01 §2`) is written to use a certificate by thumbprint from the Windows certificate store or a cloud signing service, and never a file in the repository. Obtaining one is a purchase and an identity check only the operator can do.

- [ ] Choose a route and record the choice (not the secret) in `docs/dev/decisions.md`. Done when: the entry names the route and its yearly cost.
  1. Options: an OV or EV code-signing certificate from a certificate authority (hardware token or cloud key storage), Azure Trusted Signing (Microsoft's managed service), or SignPath's free program for open-source projects (check its current eligibility terms).
  2. Complete the vendor's identity validation for Rizonesoft.
- [ ] Make the certificate available to the packaging machine and CI without committing it. Done when: `Get-ChildItem Cert:\CurrentUser\My | Where-Object HasPrivateKey` lists it on the packaging machine, or the cloud service's CLI signs a test file.
  1. Set the thumbprint (or service settings) as an environment variable on the packaging machine and as a repository secret for `release.yml`.
- [ ] Agent verification: after `D05 T01 §2` ships, a signed test file passes `signtool verify /pa`. Done when: the output is quoted.
- [ ] Commit: `"docs: record the code-signing route"` -- ticked as in §1.

**Test checkpoint:** `signtool verify /pa` passes on a file signed through `scripts/sign.ps1` (quoted), and `git grep -n "BEGIN CERTIFICATE\|\.pfx"` finds nothing in the repository. Cheaper substitute that fails: a self-signed certificate.

## 4. Confirm the Icon Art Licenses

`resources/icons/art-and-design.png` (planned as Imago's icon) and `resources/icons/lens.png` (planned as Lumen's) look like stock illustrations. Shipping them inside an installer requires a license that allows redistribution in a GPL-3.0 application, with attribution if the license asks for it.

**Corrected 2026-09-27:** the operator answered this row: the operator holds the rights to `resources/icons/art-and-design.png` and `resources/icons/lens.png` (2026-09-27), and both stay as the Imago and Lumen icons. Finding a source or replacing the art is no longer needed, and no third-party attribution applies; what is left is recording the statement where the Outcome says it lives.

**Corrected 2026-09-27, later the same day:** superseded. The operator then chose new icons for all three apps (Direction C, "C it is"), drawn for the project as SVG under `resources/icons/<app>/`; `art-and-design.png`, `lens.png`, and `nodus_512.png` were removed, and `resources/icons/README.md` was written with the icon set, its construction rules, and its license: created for the project on 2026-09-27, GPL-3.0 with the repository, no third-party art, no attribution owed. The rasters the apps ship are generated from those SVGs by `D00 T03 §3`. No stock-art question is left; what this row still owes is the operator's confirmation that the README's license statement is right, checked by the agent below.

- [ ] Write `resources/icons/README.md` with one row per app icon: Nodus (`resources/icons/nodus/` and `nodus_512.png`, its source as recorded in git history), Imago (`art-and-design.png`), and Lumen (`lens.png`), the last two stating "the operator holds the rights (operator statement 2026-09-27); no attribution required" (**Corrected 2026-09-27:** the README now exists and names project-created icons for all three apps; this item confirms its License section states created for the project on 2026-09-27, GPL-3.0 with the repository, and no third-party art, and that every file the export in `D00 T03 §3` produces comes from an SVG it lists). Done when: the README has the three rows and says no attribution is required for the two operator-owned files (**Corrected 2026-09-27:** read as: the README covers Nodus, Imago, and Lumen and says no attribution is owed).
- [ ] Commit: `"docs: confirm the app icon licenses"` -- ticked as in §1.

**Test checkpoint:** `resources/icons/README.md` has a license row for Nodus, Imago, and Lumen with a source URL or an ownership statement (**Corrected 2026-09-27:** its License section covers all three apps' SVGs with a project-created, GPL-3.0 statement). Cheaper substitute that fails: "found on the internet".

## 5. Choose Each App's Accent Color

The design contract gives the suite one neutral grey ramp and lets each app name one accent for focus and selection. Until chosen, the accent is a grey. This is a taste decision.

**Corrected 2026-09-27:** the operator chose the accents on 2026-09-27: Nodus cyan (the pen nib), Imago orange (the paintbrush), and Lumen green (the aperture), tuned for contrast in light and dark themes. The values and their ratios are recorded in `standards/shared.md`'s Color section (dark `#29C5E6`, `#F5923E`, `#4CC47A` against `Base`; light `#00758C`, `#B04F00`, `#1B7A3D` against white). What is left is an independent check of the ratios.

**Corrected 2026-09-27:** the design system import (`standards/ui.md`, `docs/design/`) makes the app accent identity only (title-bar mark, splash, the one primary button); selection and focus use the Highlight color (`state*` tokens, Blue by default). The accent values are the `accent-<app>` tokens in `docs/design/tokens.json` (one value for Dark, Darkest, and Medium Gray, one for Light), the same hex values as before; the check below measures each `-on` label against its accent fill, not the accent against the retired `Base` `#1A1A1A`.

- [ ] Check each accent in `docs/design/tokens.json` with WebAIM's contrast checker (https://webaim.org/resources/contrastchecker/): the label `accent-<app>-on` against the fill `accent-<app>` (the primary button) in each of the four themes, at least 4.5:1 (**Corrected 2026-09-27:** said the dark-theme value against `Base` `#1A1A1A` and the light-theme value against `#FFFFFF` from `standards/shared.md`'s accent table, which the design system import retired). Done when: the ratios the checker reports are quoted and each is at least 4.5:1.
- [ ] Commit: `"docs: verify each app's accent color"` -- the agent quotes the ratios; the operator's choice is already recorded.

**Test checkpoint:** `docs/design/tokens.json` names three accents whose `-on` labels contrast at least 4.5:1 with them in all four themes, `standards/ui.md` quotes the same hex values, and `ThemeTokensTests` (from `D01 T01 §3`) passes on the dictionaries generated from those tokens. Cheaper substitute that fails: an accent chosen without a contrast check.

## Verification

- [ ] Every row above carries `**Requires:** operator` once `D00 T01 §2` ships
- [ ] Each agent verification item is quoted in its section's stamp
- [ ] `python scripts/todo-graph.py validate` clean
