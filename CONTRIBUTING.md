# Contributing to the Isotone Graphics Suite

Thank you for helping build Isotone. This guide covers how work is organized, how to build and test, and what a pull request needs before it can merge.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Security problems go through the private process in [SECURITY.md](SECURITY.md), never through public issues.

## Contents

- [Ways to contribute](#ways-to-contribute)
- [How work is organized: the TODO tree](#how-work-is-organized-the-todo-tree)
- [Set up and build](#set-up-and-build)
- [Code style](#code-style)
- [Commit messages](#commit-messages)
- [Pull requests](#pull-requests)
- [Licensing and sign-off](#licensing-and-sign-off)
- [Names and icons](#names-and-icons)

## Ways to contribute

- **Report a bug** with the [bug report form](https://github.com/rizonesoft/Isotone/issues/new?template=bug_report.yml). Include the app, its version, your Windows version, and steps to reproduce.
- **Suggest a feature** with the [feature request form](https://github.com/rizonesoft/Isotone/issues/new?template=feature_request.yml). Describe the problem first, then the solution you have in mind.
- **Ask a question** in [Discussions](https://github.com/rizonesoft/Isotone/discussions) rather than an issue.
- **Improve the docs**: fixes to `docs/` and the READMEs are always welcome.
- **Send code**: pick an open item from the plan (below) or an issue labelled for help, and say so on the issue before starting large work.

Search existing issues and discussions before opening a new one.

## How work is organized: the TODO tree

Development is driven by a plan that lives in the repository, not in a tracker.

- [`todo/`](todo/) holds the TODO tree: one folder per domain, one file per task, and numbered sections inside each task. Start with [`todo/README.md`](todo/README.md).
- [`todo/implementation-plan.md`](todo/implementation-plan.md) is the ordered plan: which sections run next and what each depends on.
- Every section has checkbox items, a "Done when" condition per item, and a test checkpoint. A section is finished when its checkpoint passes, not when the code compiles.
- Sections are referenced as `DNN TNN §N` (domain, task, section), for example `D01 T02 §3`. Use that reference in commit bodies and pull requests so work traces back to the plan.

If your change is not covered by an existing section, open an issue first so it can be planned. Small fixes (typos, obvious bugs) do not need a plan entry.

## Set up and build

You need Windows 11 (x64; Windows 10 22H2 may work but is unsupported), [PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell-on-windows), and Git. The .NET SDK is pinned to **11.0.100-rc.1.26425.128** in `global.json`; the provisioning script installs it, and Inno Setup 7 for building installers.

```powershell
git clone https://github.com/rizonesoft/Isotone.git
cd Isotone

pwsh tools/provision.ps1              # install the pinned SDK and tools
dotnet build Isotone.slnx              # build everything
pwsh scripts/check-all.ps1            # run every gate: build, tests, analyzers, plan checks
pwsh scripts/package.ps1 -App Stilus   # optional: build an installer and portable ZIP
```

`scripts/check-all.ps1` is the same gate CI runs. If it is green locally, CI should be green too. See [docs/dev/build.md](docs/dev/build.md) for details and troubleshooting.

## Code style

- **Formatting** is defined by [`.editorconfig`](.editorconfig) at the repository root. Your editor and `dotnet format` both honor it; please do not reformat unrelated code.
- **No new warnings.** Keep the build and analyzer output clean; fix a warning rather than suppress it.
- **Modern C#:** file-scoped namespaces, primary constructors where they help, `var` when the type is obvious, nullable reference types enabled.
- **Separation:** domain logic stays out of the UI layer. Core projects (`*.Core`, and later `Isotone.Core`) must not reference WPF.
- **MVVM** with CommunityToolkit.Mvvm; no third-party UI frameworks. Standard WPF controls only.
- **Tests:** new behavior comes with tests (xUnit). Bug fixes come with a test that fails before the fix.
- **Docs:** user-visible changes update the matching guide under [`docs/user/`](docs/user/README.md); architectural changes update [`docs/dev/`](docs/dev/README.md).
- Coding standards live in [`standards/`](standards/): `shared.md` for suite-wide rules plus one file per app (`stilus.md`, `pinxit.md`, `albumen.md`).

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <summary>

<body: what and why, with the plan reference, e.g. D01 T02 §3>

Signed-off-by: Your Name <you@example.com>
```

- **Types:** `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- **Scopes:** the app or area, such as `stilus`, `pinxit`, `albumen`, `core`, `installer`, `ci`, `docs`.
- Keep the summary under about 72 characters, in the imperative mood ("add", not "added").

Examples:

```text
feat(stilus): add corner radius to rectangle tool
fix(pinxit): keep layer order when undoing a merge
ci: cache NuGet packages in build workflow
```

## Pull requests

1. Fork the repository and branch from `main` (`feat/stilus-corner-radius`, `fix/pinxit-merge-undo`).
2. Keep each pull request focused on one change.
3. Fill in the pull request template: the plan reference, what changed, and how you tested it.
4. Before requesting review, make sure that:
   - `pwsh scripts/check-all.ps1` is green,
   - docs are updated for anything user-visible,
   - [`CHANGELOG.md`](CHANGELOG.md) has an entry under **Unreleased**, in the section for the app you changed,
   - every commit is signed off (see below).
5. A maintainer reviews, may ask for changes, and merges once CI is green.

Do not bump version numbers; versions come from Git tags (see [docs/dev/versioning.md](docs/dev/versioning.md)).

## Licensing and sign-off

The Isotone Graphics Suite is licensed under the [GNU General Public License v3.0](LICENSE). The project copyright is held by Rizonetech (Pty) Ltd ("Copyright (C) 2025-2026 Rizonetech (Pty) Ltd"); Rizonesoft is a brand of Rizonetech (Pty) Ltd.

You keep the copyright of your own contributions. By contributing, you license your contribution under GPL-3.0, the same license as the rest of the project, and certify the DCO below; you do not assign your copyright to anyone. There is no contributor license agreement today; if one is ever introduced it will be announced here before it applies, and it will not apply to contributions made before it.

We use the [Developer Certificate of Origin](https://developercertificate.org/) (DCO) instead of a contributor license agreement. The DCO is a short statement that you wrote the change, or otherwise have the right to submit it under the project's license. You certify it by adding a sign-off line to every commit:

```text
Signed-off-by: Your Name <you@example.com>
```

Git adds it for you with `git commit -s`. The name and email must match the commit author. Pull requests with unsigned commits cannot be merged; fix them with `git rebase --signoff main` and force-push your branch.

Do not submit code copied from projects with incompatible licenses, or from any source you are not sure about. When you include third-party code under a GPL-compatible license, keep its copyright notice and mention it in the pull request.

## Names and icons

The GPL covers the code, not the names and logos. "Rizonesoft", "Isotone Graphics Suite", "Stilus", "Pinxit", and "Albumen" and the app icons are trademarks of Rizonetech (Pty) Ltd; the [trademark policy](TRADEMARKS.md) explains what you may do with them. In short: contributing to this repository is always fine, but a fork or modified build that you distribute needs its own name and icons.
