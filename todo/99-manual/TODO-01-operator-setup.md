---
schema_version: 1
id: operator-setup
domain: 99-manual
status: draft
title: "TODO-01 -- Operator Setup (Manual)"
depends_on: []
---

# TODO-01 -- Operator Setup (Manual)

> **Goal:** The steps no agent session can perform are done by the operator from exact instructions: the repository's About bar, topics, and social preview are set; `main` is protected by the real required checks; a code-signing certificate exists and is available to the packaging scripts without entering the repository; the licenses of the app icon art are confirmed; each app's accent color is chosen; the project's copyright rests with Rizonetech (Pty) Ltd by a signed assignment; the names are cleared and filed as trademarks; the download storage behind `download.rizonesoft.com` exists with its GitHub secrets; the product page URLs are decided; and the contributor agreement question is answered before outside contributions are accepted.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The repository is `github.com/rizonesoft/Isotone` with default settings as far as this plan knows. `resources/brand/social-preview.jpg` exists for the social preview. The CI checks are named `build` (workflow `build.yml`) and `plan-gates` (workflow `plan.yml`). There is no code-signing certificate (operator statement, 2026-09-26). The app icon candidates `resources/icons/art-and-design.png` (Pinxit) and `resources/icons/lens.png` (Albumen) arrived with the initial commit with no recorded source or license. The design contract in `standards/shared.md` leaves each app's accent color to the operator. Until `D00 T01 §2` ships, these rows cannot carry the `**Requires:** operator` mark; they depend on that section so no runner takes them before it does. **Corrected 2026-09-27:** the operator answered three of these rows that day: the social preview is uploaded (§1), the operator holds the rights to `resources/icons/art-and-design.png` and `resources/icons/lens.png` (§4), and the accents are chosen and recorded in `standards/shared.md` (§5); what each section still owes is its record and its verification, and every row still flips only through a review stamp. **Corrected 2026-09-27, later the same day:** the §4 answer is superseded. The operator chose project-created icons (Direction C, "C it is"), so `resources/icons/art-and-design.png`, `resources/icons/lens.png`, and `resources/icons/stilus_512.png` were removed, and `resources/icons/README.md` records every app icon as created for the project on 2026-09-27 and licensed GPL-3.0 with the repository, with no third-party art. **Corrected 2026-09-27, operator decisions on ownership and distribution:** the copyright holder is Rizonetech (Pty) Ltd (the operator's company) and Rizonesoft is its brand; the repository now says "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd" and "Rizonesoft is a brand of Rizonetech (Pty) Ltd." (`README.md`, `CONTRIBUTING.md`, `Directory.Build.props`, `installer/common.iss`, the splash cards) and has a trademark policy (`TRADEMARKS.md`, no registration claimed). Binaries ship only from rizonesoft.com through S3-compatible storage behind `download.rizonesoft.com`, which does not exist yet (no provider is chosen, and none of the `ISOTONE_DL_S3_*` secrets is set, so `release.yml` refuses a tag release); the product page URLs are undecided, so `ISOTONE_SITE_URL` defaults to `https://www.rizonesoft.com/`; contributors keep their copyright under the GPL with the DCO, and a CLA is undecided. No written assignment from Derick Payne to Rizonetech (Pty) Ltd exists yet, and no trademark search or filing has been made. §6 to §10 are those operator steps. **Corrected 2026-09-27, after the rename to Isotone:** the operator removed the neon brand images ("Remove the neon banners"): `resources/brand/social-preview.jpg`, `resources/brand/isotone-banner.jpg`, and `resources/brand/isotone.png` are deleted, because they spelled the retired Photon name; the social preview still uploaded on GitHub is that image, so §1 now removes or replaces it.
<!-- claim: exists TRADEMARKS.md -->
<!-- claim: count "ISOTONE_DL_S3_ENDPOINT" .github/workflows/release.yml = 5 -->
<!-- claim: absent resources/brand/social-preview.jpg -->
<!-- claim: absent resources/icons/art-and-design.png -->
<!-- claim: absent resources/icons/lens.png -->
<!-- claim: exists resources/icons/README.md -->

## Inputs

- `https://github.com/rizonesoft/Isotone` -- every click path below starts here, logged in as the owner
- [`.github/workflows/build.yml`](../../.github/workflows/build.yml), [`.github/workflows/plan.yml`](../../.github/workflows/plan.yml) -- the check names §2 requires
- [`standards/release.md`](../../standards/release.md) -- the signing policy §3 satisfies
- -> XREF: D00 T01 §2 -- adds the `operator` requirement these rows carry once it ships
- -> XREF: D05 T01 §2 -- the signing plumbing that consumes §3's certificate
- -> XREF: D00 T03 §3 -- the app icon raster export (generates the rasters of the project-created icons whose license §4 confirms)
- -> XREF: D05 T01 §4 -- the update check that reads the feed on §8's storage and links §9's product page
- -> XREF: D02 T05 §4 -- the first real release, which depends on §8's storage and secrets
- [`TRADEMARKS.md`](../../TRADEMARKS.md) -- the trademark policy §7 clears and registers the names for
- [`docs/dev/versioning.md`](../../docs/dev/versioning.md) -- the download layout, the update feed, and the secrets and variables §8 and §9 set

## Outcome

- The repository page shows a description, topics, and the social preview.
- `main` refuses direct pushes that skip the `build` and `plan-gates` checks.
- A code-signing certificate is installed where `scripts/sign.ps1` can use it by thumbprint, or a cloud signing account is configured, and nothing about it is in the repository.
- `resources/icons/README.md` records a confirmed license for every icon the apps ship.
- The design contract names each app's accent color.
- A signed assignment vests the copyright in Bezier (Stilus), Pinxit, Isotone, and all prior work of Derick Payne in them in Rizonetech (Pty) Ltd, and `docs/dev/decisions.md` records its date (never the document).
- The trademark search results are recorded, and the cleared names are filed with CIPC with their application numbers recorded.
- `download.rizonesoft.com` serves files from S3-compatible storage over HTTPS, and the four `ISOTONE_DL_S3_*` secrets exist, so `release.yml` can publish.
- The product page URLs are decided and `ISOTONE_SITE_URL` is set.
- A recorded decision says whether outside contributions need a CLA, made before the first outside pull request is merged.

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
|   6   |   §6    | Assign the copyright to Rizonetech (Pty) Ltd  | D00 T01 §2             |  [ ]   |
|   7   |   §7    | Trademark clearance and CIPC filing           | §6                     |  [ ]   |
|   8   |   §8    | Download storage and the release secrets      | D00 T01 §2             |  [ ]   |
|   9   |   §9    | Decide the product page URLs                  | D00 T01 §2             |  [ ]   |
|  10   |   §10   | Decide on a CLA before outside contributions  | §6                     |  [ ]   |

---

## 1. About Bar, Topics, and Social Preview

The About bar is the repository's first impression and the social preview is its face in every link. Both need the owner's logged-in session.

**Corrected 2026-09-27:** the operator uploaded the social preview (`resources/brand/social-preview.jpg`) on 2026-09-27, so its item is now a verification of the upload rather than the click path; the description and topics are still owed.

- [ ] Set the description. Done when: the repository page shows it under the name.
  1. Open `https://github.com/rizonesoft/Isotone` logged in as the owner.
  2. Click the gear icon beside **About** on the right.
  3. Paste the one-line description from the top of `README.md` into **Description**, then click **Save changes**.
- [ ] Set the topics. Done when: the About bar lists them.
  1. Open the About gear again.
  2. In **Topics**, add: `graphics`, `vector-editor`, `image-editor`, `raw-processing`, `wpf`, `dotnet`, `windows`, `open-source`.
  3. Click **Save changes**.
- [ ] Remove the neon social preview uploaded on 2026-09-27 (it spells the retired Photon name), or replace it with a new Isotone image committed under `resources/brand/` first (**Corrected 2026-09-27:** said confirm that the upload is `resources/brand/social-preview.jpg`, which the operator removed with the neon banners). Done when: **Settings**, **Social preview** at `https://github.com/rizonesoft/Isotone/settings` shows no image or the committed replacement, and a logged-out link unfurl shows the same (capture).
- [ ] Agent verification: the agent reads `gh repo view rizonesoft/Isotone --json description,repositoryTopics` and quotes it. Done when: the description and all eight topics are quoted.
- [ ] Commit: `"docs: record the repository About bar setup"` -- the operator ticks the items above in the GitHub web editor; the agent verifies, ticks its item, and commits.

**Test checkpoint:** `gh repo view rizonesoft/Isotone --json description,repositoryTopics` returns the description and the eight topics; a logged-out browser shows the social preview in a link unfurl (capture). Cheaper substitute that fails: trusting the settings form without reloading the public page.

## 2. Branch Protection with the Required Checks

A protected `main` keeps a red build from landing. The checks must be the real job names from the workflows, which exist only after `D00 T01 §5` has run them once.

- [ ] Protect `main`. Done when: the rule lists both checks.
  1. Open `https://github.com/rizonesoft/Isotone/settings/rules` (or **Settings**, **Branches**), click **New branch ruleset** (or **Add branch protection rule**).
  2. Target `main`; enable **Require status checks to pass**; search and add `build` and `plan-gates`.
  3. Enable **Block force pushes**; leave **Require a pull request** off (the single-writer workflow commits to `main` directly; revisit if contributors join).
  4. Save.
- [ ] Agent verification: `gh api repos/rizonesoft/Isotone/rules/branches/main` lists the required checks. Done when: the output is quoted.
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

`resources/icons/art-and-design.png` (planned as Pinxit's icon) and `resources/icons/lens.png` (planned as Albumen's) look like stock illustrations. Shipping them inside an installer requires a license that allows redistribution in a GPL-3.0 application, with attribution if the license asks for it.

**Corrected 2026-09-27:** the operator answered this row: the operator holds the rights to `resources/icons/art-and-design.png` and `resources/icons/lens.png` (2026-09-27), and both stay as the Pinxit and Albumen icons. Finding a source or replacing the art is no longer needed, and no third-party attribution applies; what is left is recording the statement where the Outcome says it lives.

**Corrected 2026-09-27, later the same day:** superseded. The operator then chose new icons for all three apps (Direction C, "C it is"), drawn for the project as SVG under `resources/icons/<app>/`; `art-and-design.png`, `lens.png`, and `stilus_512.png` were removed, and `resources/icons/README.md` was written with the icon set, its construction rules, and its license: created for the project on 2026-09-27, GPL-3.0 with the repository, no third-party art, no attribution owed. The rasters the apps ship are generated from those SVGs by `D00 T03 §3`. No stock-art question is left; what this row still owes is the operator's confirmation that the README's license statement is right, checked by the agent below.

- [ ] Write `resources/icons/README.md` with one row per app icon: Stilus (`resources/icons/stilus/` and `stilus_512.png`, its source as recorded in git history), Pinxit (`art-and-design.png`), and Albumen (`lens.png`), the last two stating "the operator holds the rights (operator statement 2026-09-27); no attribution required" (**Corrected 2026-09-27:** the README now exists and names project-created icons for all three apps; this item confirms its License section states created for the project on 2026-09-27, GPL-3.0 with the repository, and no third-party art, and that every file the export in `D00 T03 §3` produces comes from an SVG it lists). Done when: the README has the three rows and says no attribution is required for the two operator-owned files (**Corrected 2026-09-27:** read as: the README covers Stilus, Pinxit, and Albumen and says no attribution is owed).
- [ ] Commit: `"docs: confirm the app icon licenses"` -- ticked as in §1.

**Test checkpoint:** `resources/icons/README.md` has a license row for Stilus, Pinxit, and Albumen with a source URL or an ownership statement (**Corrected 2026-09-27:** its License section covers all three apps' SVGs with a project-created, GPL-3.0 statement). Cheaper substitute that fails: "found on the internet".

## 5. Choose Each App's Accent Color

The design contract gives the suite one neutral grey ramp and lets each app name one accent for focus and selection. Until chosen, the accent is a grey. This is a taste decision.

**Corrected 2026-09-27:** the operator chose the accents on 2026-09-27: Stilus cyan (the pen nib), Pinxit orange (the paintbrush), and Albumen green (the aperture), tuned for contrast in light and dark themes. The values and their ratios are recorded in `standards/shared.md`'s Color section (dark `#29C5E6`, `#F5923E`, `#4CC47A` against `Base`; light `#00758C`, `#B04F00`, `#1B7A3D` against white). What is left is an independent check of the ratios.

**Corrected 2026-09-27:** the design system import (`standards/ui.md`, `docs/design/`) makes the app accent identity only (title-bar mark, splash, the one primary button); selection and focus use the Highlight color (`state*` tokens, Blue by default). The accent values are the `accent-<app>` tokens in `docs/design/tokens.json` (one value for Dark, Darkest, and Medium Gray, one for Light), the same hex values as before; the check below measures each `-on` label against its accent fill, not the accent against the retired `Base` `#1A1A1A`.

- [ ] Check each accent in `docs/design/tokens.json` with WebAIM's contrast checker (https://webaim.org/resources/contrastchecker/): the label `accent-<app>-on` against the fill `accent-<app>` (the primary button) in each of the four themes, at least 4.5:1 (**Corrected 2026-09-27:** said the dark-theme value against `Base` `#1A1A1A` and the light-theme value against `#FFFFFF` from `standards/shared.md`'s accent table, which the design system import retired). Done when: the ratios the checker reports are quoted and each is at least 4.5:1.
- [ ] Commit: `"docs: verify each app's accent color"` -- the agent quotes the ratios; the operator's choice is already recorded.

**Test checkpoint:** `docs/design/tokens.json` names three accents whose `-on` labels contrast at least 4.5:1 with them in all four themes, `standards/ui.md` quotes the same hex values, and `ThemeTokensTests` (from `D01 T01 §3`) passes on the dictionaries generated from those tokens. Cheaper substitute that fails: an accent chosen without a contrast check.

## 6. Assign the Copyright to Rizonetech (Pty) Ltd

Operator decision 2026-09-27: the copyright holder is Rizonetech (Pty) Ltd, the operator's company, and Rizonesoft is its brand. The repository already says so, but the work was written by Derick Payne personally (Bezier, now Stilus; Pinxit; and Isotone, including the MIT-licensed releases Bezier and Pinxit published before the monorepo), so the company holds the copyright only once a written assignment says it does. This is a legal document only the operator can sign. Advice: have a South African intellectual property attorney draft or review it; South African copyright law (the Copyright Act 98 of 1978) expects an assignment in writing signed by the assignor, and the attorney confirms the form.

- [ ] Consult a South African IP attorney about the assignment: its scope (all copyright in Bezier, Pinxit, Isotone, and all prior work in their histories, code, documentation, and art, including the earlier MIT-licensed releases), the waiver of moral rights where the law allows, and whether anything else the operator wrote should be included. Done when: the operator has the attorney's draft or approval.
- [ ] Sign the deed of assignment from Derick Payne (assignor) to Rizonetech (Pty) Ltd (assignee), signed on the company's behalf by an authorised director, and keep it with the company's records, never in the repository. Done when: the operator states the signing date.
- [ ] Record the fact, not the document, in `docs/dev/decisions.md`: "Copyright in Bezier (Stilus), Pinxit, Isotone, and all prior work of Derick Payne in them assigned to Rizonetech (Pty) Ltd on <date>; the deed is held by the company." Done when: the entry exists.
- [ ] Agent verification: `git grep -n "Copyright (C)" -- ':!LICENSE' ':!docs/parity'` lists only the "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd" wording, and `git grep -n -E "Copyright \(C\) [0-9-]+ Rizonesoft|© [0-9]+ Rizonesoft"` prints nothing. Done when: both outputs are quoted.
- [ ] Commit: `"docs: record the copyright assignment to Rizonetech (Pty) Ltd"` -- ticked as in §1.

**Test checkpoint:** the `docs/dev/decisions.md` entry names the assignment date, and the two `git grep` outputs show no copyright line naming anyone but Rizonetech (Pty) Ltd outside third-party notices. Cheaper substitute that fails: changing the copyright lines without a signed assignment, which leaves the company claiming a copyright it does not hold.

## 7. Trademark Clearance and CIPC Filing

`TRADEMARKS.md` says "Rizonesoft", "Isotone Graphics Suite", "Stilus", "Pinxit", and "Albumen" and the app icons are trademarks of Rizonetech (Pty) Ltd, without claiming registration. Before relying on the names (and before the first release makes them public), the operator clears them against existing marks and files the ones that clear. "Pinxit", "Albumen", and "Stilus" are common words and may already be registered for software, so a conflict may mean renaming an app, which is far cheaper before its first release than after.

**Corrected 2026-09-27:** the agent's first-pass screen (WIPO Global Brand Database, classes 9 and 42, plus a web search for software already using each name) found live software marks or same-category products for Photon (Exit Games; Photon Studio), Lumen (Lumen Technologies in 15+ countries; two photo apps), and Imago (Monotype in the UK and EU; Nuvio Imago), so the operator renamed the suite and apps ("doit, let's replace all 4 names"). The new names screened as follows: Isotone, no live class 9 or 42 mark; Pinxit, no class 9 mark; Albumen, only food and pharmaceutical marks; Stilus, one live class 9 registration in Spain (a private individual, 2011) that the operator accepted and the attorney should weigh. Rizonesoft has no mark anywhere. The screen is not a clearance: the CIPC register, similar spellings, and unregistered use still need the searches below.

- [ ] Search each name in the CIPC trade mark register (South Africa) and the WIPO Global Brand Database, in Nice classes 9 (downloadable software) and 42 (software services), ideally through a trademark attorney who also advises on conflicts. Done when: `docs/dev/decisions.md` records per name: the searches run, the conflicts found, and the attorney's view.
- [ ] For a name that does not clear, decide: keep it (with the attorney's risk view), or rename the app; a rename is filed through `add-todo` as agent work before that app's first release. Done when: every name has a recorded decision.
- [ ] File trade mark applications with CIPC for the cleared names (and the Rizonesoft logo and app icons if the attorney advises), classes 9 and 42. Done when: the application numbers and filing dates are recorded in `docs/dev/decisions.md`.
- [ ] Once a registration is granted, the agent updates `TRADEMARKS.md` to say that mark is registered in South Africa (and may use the registered symbol for it); until then the policy keeps its "trademarks of" wording with no registration claim. Done when: the policy matches the register (quoted).
- [ ] Commit: `"docs: record the trademark clearance and filings"` -- ticked as in §1.

**Test checkpoint:** `docs/dev/decisions.md` lists all five names with their search results and a decision each, and every filed name has an application number; `TRADEMARKS.md` claims registration only for a mark whose registration is recorded. Cheaper substitute that fails: filing without a search, or claiming a registration that was only applied for.

## 8. Download Storage and the Release Secrets

Operator decision 2026-09-27: binaries are distributed only from rizonesoft.com, through S3-compatible object storage behind the CDN host `download.rizonesoft.com`; the provider is not chosen. `release.yml` uploads there with rclone and fails a tag release when any of its four secrets is missing, so no app can release until this row is done (`D02 T05 §4` depends on it). The layout, the feed, and the settings are in `docs/dev/versioning.md`.

- [ ] Choose the provider (for example Cloudflare R2, Backblaze B2 with a CDN, Wasabi, DigitalOcean Spaces, or Amazon S3 with CloudFront) and record the choice, its egress cost, and the reason in `docs/dev/decisions.md`. Done when: the entry exists.
- [ ] Create the bucket (listing disabled, objects publicly readable only through the CDN host) and point `download.rizonesoft.com` at it with a DNS CNAME and HTTPS. Done when: a test object uploaded as `healthcheck.txt` downloads from `https://download.rizonesoft.com/healthcheck.txt`.
- [ ] Create an access key limited to that bucket (read, write, and delete objects; no account-wide rights). Done when: the key exists and nothing else can be done with it (the provider's policy view).
- [ ] Add the secrets and the variable without writing them anywhere else: run `gh secret set ISOTONE_DL_S3_ENDPOINT`, `gh secret set ISOTONE_DL_S3_BUCKET`, `gh secret set ISOTONE_DL_S3_ACCESS_KEY_ID`, and `gh secret set ISOTONE_DL_S3_SECRET_ACCESS_KEY` and paste each value at the prompt; set `gh variable set ISOTONE_DL_BASE_URL --body https://download.rizonesoft.com` only if the host differs from the default. Done when: `gh secret list` names all four.
- [ ] Agent verification: `gh secret list` and `gh variable list` are quoted (names only), `curl -sI https://download.rizonesoft.com/healthcheck.txt` returns 200, and the next `release.yml` draft dispatch (`D00 T02 §7`) uploads under `drafts/` instead of printing the "Upload skipped" notice. Done when: the three outputs are quoted.
- [ ] Commit: `"docs: record the download storage behind download.rizonesoft.com"` -- ticked as in §1.

**Test checkpoint:** `gh secret list` names `ISOTONE_DL_S3_ENDPOINT`, `ISOTONE_DL_S3_BUCKET`, `ISOTONE_DL_S3_ACCESS_KEY_ID`, and `ISOTONE_DL_S3_SECRET_ACCESS_KEY`; `https://download.rizonesoft.com/healthcheck.txt` answers 200 over HTTPS; a draft run of `release.yml` shows the upload step ran. Cheaper substitute that fails: attaching the installers to the GitHub release instead, which the operator refused and the workflow no longer does.

## 9. Decide the Product Page URLs

Every link to a product page (the installer's publisher URL, the About dialog, the update check's Open Download Page, the README, the release body, and winget's `PackageUrl`) reads one value, `ISOTONE_SITE_URL`, which defaults to `https://www.rizonesoft.com/` because the pages on rizonesoft.com are not decided. Links from GitHub surfaces add `?utm_source=github&utm_medium=<place>`.

- [ ] Decide the pages: one suite page, or one page per app (for example `https://www.rizonesoft.com/stilus/`), and publish them on rizonesoft.com. Done when: `docs/dev/decisions.md` records the URLs and each page answers 200.
- [ ] Set the value: `gh variable set ISOTONE_SITE_URL --body <the suite or default page>`. Done when: `gh variable list` shows it.
- [ ] If per-app pages need more than the one value, the agent files the change through `add-todo` (a per-app value in `AppIdentity`, the installer, and the feed's `page`) rather than typing URLs into surfaces. Done when: the filing exists or the one value is recorded as enough.
- [ ] Commit: `"docs: record the product page URLs"` -- ticked as in §1.

**Test checkpoint:** `gh variable list` shows `ISOTONE_SITE_URL` equal to the recorded page, and `curl -sI` of each recorded URL returns 200 (quoted). Cheaper substitute that fails: typing a per-app URL into the README or a dialog, which leaves the one value and the surfaces disagreeing.

## 10. Decide on a CLA Before Outside Contributions

Contributors keep the copyright of their contributions and license them under GPL-3.0 with the DCO sign-off (`CONTRIBUTING.md`); there is no contributor license agreement. That keeps contributing simple, but it means Rizonetech (Pty) Ltd could not relicense or dual-license code others wrote. The operator decides, with the IP attorney of §6, before the first pull request from someone other than the operator is merged.

- [ ] Decide between keeping the DCO only, a CLA granting Rizonetech (Pty) Ltd a broad license to contributions (for example modelled on the Apache Individual CLA), or a copyright assignment agreement. Done when: `docs/dev/decisions.md` records the choice, the reason, and the attorney's view.
- [ ] If a CLA or an assignment is chosen, the agent files the work through `add-todo`: the agreement text in the repository, a check that refuses an unsigned pull request, and the `CONTRIBUTING.md` section announcing it before it applies. Done when: the filing exists, or the DCO-only decision is recorded and `CONTRIBUTING.md` needs no change.
- [ ] Until this row is stamped, no pull request authored by anyone but the operator is merged. Done when: `gh pr list --state merged --json author` shows only the operator's account since 2026-09-27 (quoted at stamping).
- [ ] Commit: `"docs: record the contributor agreement decision"` -- ticked as in §1.

**Test checkpoint:** the decision is recorded in `docs/dev/decisions.md`, and `CONTRIBUTING.md`'s Licensing and sign-off section matches it (DCO only, or the agreement with its check). Cheaper substitute that fails: accepting outside code first and deciding later, which cannot be undone for code already merged.

## Verification

- [ ] Every row above carries `**Requires:** operator` once `D00 T01 §2` ships
- [ ] Each agent verification item is quoted in its section's stamp
- [ ] `python scripts/todo-graph.py validate` clean
