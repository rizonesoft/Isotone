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
> **Current state (verified 2026-09-26):** The repository is `github.com/rizonesoft/Photon` with default settings as far as this plan knows. `resources/brand/social-preview.jpg` exists for the social preview. The CI checks are named `build` (workflow `build.yml`) and `plan-gates` (workflow `plan.yml`). There is no code-signing certificate (operator statement, 2026-09-26). The app icon candidates `resources/icons/art-and-design.png` (Imago) and `resources/icons/lens.png` (Lumen) arrived with the initial commit with no recorded source or license. The design contract in `standards/shared.md` leaves each app's accent color to the operator. Until `D00 T01 §2` ships, these rows cannot carry the `**Requires:** operator` mark; they depend on that section so no runner takes them before it does.
<!-- claim: exists resources/brand/social-preview.jpg -->
<!-- claim: exists resources/icons/art-and-design.png -->
<!-- claim: exists resources/icons/lens.png -->

## Inputs

- `https://github.com/rizonesoft/Photon` -- every click path below starts here, logged in as the owner
- [`.github/workflows/build.yml`](../../.github/workflows/build.yml), [`.github/workflows/plan.yml`](../../.github/workflows/plan.yml) -- the check names §2 requires
- [`standards/release.md`](../../standards/release.md) -- the signing policy §3 satisfies
- -> XREF: D00 T01 §2 -- adds the `operator` requirement these rows carry once it ships
- -> XREF: D05 T01 §2 -- the signing plumbing that consumes §3's certificate

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

- [ ] Set the description. Done when: the repository page shows it under the name.
  1. Open `https://github.com/rizonesoft/Photon` logged in as the owner.
  2. Click the gear icon beside **About** on the right.
  3. Paste the one-line description from the top of `README.md` into **Description**, then click **Save changes**.
- [ ] Set the topics. Done when: the About bar lists them.
  1. Open the About gear again.
  2. In **Topics**, add: `graphics`, `vector-editor`, `image-editor`, `raw-processing`, `wpf`, `dotnet`, `windows`, `open-source`.
  3. Click **Save changes**.
- [ ] Set the social preview. Done when: **Settings**, **Social preview** shows the image.
  1. Open `https://github.com/rizonesoft/Photon/settings`, scroll to **Social preview**, click **Edit**, **Upload an image**.
  2. Choose `resources/brand/social-preview.jpg` from a local clone, then **Save**.
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

- [ ] Find the source of each file and its license terms, or replace it with art Rizonesoft owns. Done when: `resources/icons/README.md` names the source, license, and any required attribution for each app icon.
- [ ] If attribution is required, add it to the About dialog's credits (the agent does this on request). Done when: the credits list it, or the README says none is required.
- [ ] Commit: `"docs: confirm the app icon licenses"` -- ticked as in §1.

**Test checkpoint:** `resources/icons/README.md` has a license row for Nodus, Imago, and Lumen with a source URL or an ownership statement. Cheaper substitute that fails: "found on the internet".

## 5. Choose Each App's Accent Color

The design contract gives the suite one neutral grey ramp and lets each app name one accent for focus and selection. Until chosen, the accent is a grey. This is a taste decision.

- [ ] Choose an accent for Nodus, Imago, and Lumen (hex values), checking each against `Base` (`#1A1A1A`) for at least 4.5:1 contrast with WebAIM's contrast checker (https://webaim.org/resources/contrastchecker/). Done when: the three values and their contrast ratios are written in `standards/shared.md`'s Color section.
- [ ] Commit: `"docs: name each app's accent color"` -- the operator edits `standards/shared.md` in the web editor; the agent verifies the ratios.

**Test checkpoint:** `standards/shared.md` names three accents with contrast ratios of at least 4.5:1 against `Base`, and `ThemeTokensTests` (from `D01 T01 §3`) passes after the agent mirrors them into the theme. Cheaper substitute that fails: an accent chosen without a contrast check.

## Verification

- [ ] Every row above carries `**Requires:** operator` once `D00 T01 §2` ships
- [ ] Each agent verification item is quoted in its section's stamp
- [ ] `python scripts/todo-graph.py validate` clean
