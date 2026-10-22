# Decisions

The decisions this suite has made with evidence, one entry each, newest last. Every "decide with evidence" section in `todo/` writes its decision here, and a later change of mind adds a new entry that names the one it replaces, never an edit that hides it.

Each entry holds:

- **Date** of the decision, and who confirmed it when the operator did.
- **Question**: what had to be decided, in one sentence.
- **Options**: each one considered, with its license and the URL of the license text or the package metadata that states it.
- **Evidence**: what was measured or read to choose, with sources.
- **Choice**, and why it won.
- **Cost of change**: what reversing it would take.
- **Owner**: the section that recorded it (and any that act on it).

## 2026-09-26: The assertion library

- **Date:** chosen as the justified default on 2026-09-26; confirmed by the operator on 2026-09-27 ("keep AwesomeAssertions"), so it is a decision, not a default awaiting review.
- **Question:** which assertion library the suite's tests use, given that FluentAssertions 8 is no longer open source.
- **Options:**
  - FluentAssertions 8.x: the Xceed Software "Community License Agreement ... (for Non-Commercial Use)", shipped as the package's `LICENSE` file (no SPDX expression; nuspec <https://api.nuget.org/v3-flatcontainer/fluentassertions/8.11.0/fluentassertions.nuspec>, product page <https://xceed.com/products/unit-testing/fluent-assertions/>).
  - FluentAssertions 7.x pinned: Apache-2.0 (nuspec <https://api.nuget.org/v3-flatcontainer/fluentassertions/7.2.2/fluentassertions.nuspec>, license <https://licenses.nuget.org/Apache-2.0>), frozen: 7.2.2 is its last release.
  - AwesomeAssertions: Apache-2.0 (nuspec <https://api.nuget.org/v3-flatcontainer/awesomeassertions/9.6.0/awesomeassertions.nuspec>, license <https://licenses.nuget.org/Apache-2.0>), the community fork of FluentAssertions 7 with the same API, maintained at <https://github.com/AwesomeAssertions/AwesomeAssertions>.
  - Plain xUnit `Assert` (`xunit.v3.assert`): Apache-2.0 (license <https://licenses.nuget.org/Apache-2.0>), already in every test project.
- **Evidence:** the FluentAssertions 8 license defines non-commercial use as including open-source development, but also excludes use "by or for an organisation, group of persons, legal entity, or company, that charges fees or earns revenues". Isotone is GPL-3.0 and published by a company, and a GPL distributor cannot pass a non-commercial restriction on to its recipients, nor can every contributor meet it. Five Gesso test files used the FluentAssertions syntax (`Should()`), and the 2026-09-26 toolchain upgrade switched them to AwesomeAssertions 9.6.0 with the Gesso test count unchanged (41 before and after).
- **Choice:** AwesomeAssertions. It keeps the existing tests' syntax, carries a license the GPL can live with, and still receives fixes, unlike a pinned 7.x. Plain `Assert` stays allowed beside it; `standards/testing.md` keeps one fluent library for the whole suite.
- **Cost of change:** one `using` per test file (five today) and one package line in `Directory.Packages.props`; moving to plain `Assert` instead would mean rewriting those files' assertions.
- **Owner:** `D00 T02 §5`.
