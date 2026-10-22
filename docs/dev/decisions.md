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
  - FluentAssertions 8.x: the Xceed Software "Community License Agreement ... (for Non-Commercial Use)", shipped as the package's `LICENSE` file, with no SPDX expression (license text <https://raw.githubusercontent.com/fluentassertions/fluentassertions/8.11.0/LICENSE>; nuspec <https://api.nuget.org/v3-flatcontainer/fluentassertions/8.11.0/fluentassertions.nuspec>).
  - FluentAssertions 7.x: Apache-2.0 (nuspec <https://api.nuget.org/v3-flatcontainer/fluentassertions/7.2.2/fluentassertions.nuspec>, license <https://licenses.nuget.org/Apache-2.0>, the license text at the 7.2.2 tag <https://raw.githubusercontent.com/fluentassertions/fluentassertions/7.2.2/LICENSE>). Xceed's FAQ (question 3, <https://xceed.com/fluent-assertions-faq/>, read 2026-10-22) says version 7 "will remain fully open-source indefinitely and receive bugfixes and other important corrections", so it is maintained for fixes; new features land in the commercial 8.x line.
  - AwesomeAssertions: Apache-2.0 (nuspec <https://api.nuget.org/v3-flatcontainer/awesomeassertions/9.6.0/awesomeassertions.nuspec>, license <https://licenses.nuget.org/Apache-2.0>, the license text at the 9.6.0 tag <https://raw.githubusercontent.com/AwesomeAssertions/AwesomeAssertions/9.6.0/LICENSE>), the community fork of FluentAssertions 7 with the same API, maintained at <https://github.com/AwesomeAssertions/AwesomeAssertions>.
  - Plain xUnit `Assert` (`xunit.v3.assert`): Apache-2.0 (license <https://licenses.nuget.org/Apache-2.0>, the license text at xUnit's `v3-4.0.1` tag <https://raw.githubusercontent.com/xunit/xunit/v3-4.0.1/LICENSE>), already in every test project.
- **Evidence:** the FluentAssertions 8 license defines non-commercial use as including open-source development, but also excludes use "by or for an organisation, group of persons, legal entity, or company, that charges fees or earns revenues". Isotone is GPL-3.0 and published by a company, and a GPL distributor cannot pass a non-commercial restriction on to its recipients, nor can every contributor meet it. Five Gesso test files used the FluentAssertions syntax (`Should()`), and the 2026-09-26 toolchain upgrade switched them to AwesomeAssertions 9.6.0 with the Gesso test count unchanged (41 before and after).
- **Choice:** AwesomeAssertions, confirmed by the operator. It keeps the existing tests' syntax and an Apache-2.0 license, as FluentAssertions 7.x would, and it is developed in the open as a community project, where 7.x receives fixes but its new work goes to the commercial line. FluentAssertions 7.x stays the fallback if the fork ever stalls: the API is the same. Plain `Assert` stays allowed beside it; `standards/testing.md` keeps one fluent library for the whole suite.
- **Cost of change:** one `using` per test file (five today), the `PackageReference` in each of the two Gesso test projects (`Gesso.Core.Tests.csproj`, `Gesso.Rendering.Tests.csproj`), and the `PackageVersion` line in `Directory.Packages.props`; moving to plain `Assert` instead would mean rewriting those files' assertions.
- **Owner:** `D00 T02 §5`.

## 2026-10-22: The native stack, C++20 with our own UI

- **Date:** decided by the operator on 2026-10-22, the same day the operator first wrote "please note that we will stay with WPF" and then reopened the question: "Then I do dissagree with you about staying with C# and WPF. We can do so much more, and if we get it rignt it will be eppic, if we move to C++ 20 and WinUI3."; asked "What will give us the most control and speed. + small output sizes and dependencies?"; and concluded "I feel that C++ and our own UI will get is much closer to Photoshop quality.", confirming "Yes, record it and spec it" to the question "Make C++20 with our own UI (Win32, Direct2D, DirectWrite, Direct3D) the suite's stack, and start the architecture spec?". It replaces the WPF-only decision in `AGENTS.md` (The decisions this project runs on) and that day's "stay with WPF" note.
- **Question:** which language and UI stack the three apps are built on, judged on control, speed, output size, and dependencies.
- **Options:**
  - C# on .NET 11 with WPF (the current stack, and the imported Stilus and Gesso): WPF is MIT (<https://raw.githubusercontent.com/dotnet/wpf/main/LICENSE.TXT>); ships the .NET runtime with each app, cannot be compiled ahead of time to native code, and draws through WPF's own renderer.
  - C# with WinUI 3: WinUI and the Windows App SDK are MIT (<https://raw.githubusercontent.com/microsoft/microsoft-ui-xaml/main/LICENSE>, <https://raw.githubusercontent.com/microsoft/WindowsAppSDK/main/LICENSE>); ships the .NET runtime and the Windows App SDK runtime.
  - C++20 with WinUI 3 (C++/WinRT): the same licenses; native code for our logic, with the Windows App SDK runtime and Microsoft's XAML controls and renderer between our design and the screen.
  - C++20 on Win32 with Direct2D, DirectWrite, and Direct3D, and our own UI toolkit: these are Windows system components, nothing to redistribute; every control, the docking system, text input with IME, accessibility through UI Automation, high DPI, and pen input are ours to build.
- **Evidence:** the current publish folders, measured 2026-10-22 from `pwsh scripts/publish.ps1` output: Stilus 233 MB in 292 files and Gesso 259 MB in 321 files, the largest Gesso files being `Microsoft.Windows.SDK.NET.dll` (57 MB), `Microsoft.CodeAnalysis.CSharp.dll` (18 MB), `System.Private.CoreLib.dll` (17 MB), `PresentationFramework.dll` (15 MB), and `libSkiaSharp.dll` (13 MB). The machine has Visual Studio Professional 2026 (18.11) with MSVC and Windows SDK 10.0.26100. The professional editors the suite measures itself against draw their interface with their own frameworks over the operating system's graphics rather than a general-purpose toolkit.
- **Choice:** C++20 with our own UI on Win32, Direct2D, DirectWrite, and Direct3D, decided by the operator. It gives the most control (every pixel and frame is ours, so the design system and the layout maps are implemented with nothing in between), the most speed (no runtime, no garbage collector, direct GPU access), the smallest output (one executable per app, libraries linked statically), and the fewest dependencies (Windows itself plus the libraries we choose). The architecture, the toolchain, and the migration are specified in `docs/specs/2026-10-22-native-stack-design.md`.
- **Cost of change:** the imported C# Stilus and Gesso are rewritten in C++ rather than ported line by line, with the C# code kept as a behavior reference until each native app reaches its first release; most implementation sections of `todo/` are re-planned against the spec, while the parity catalogs, the design system, the layout maps, and the TODO and review tooling carry over. Reversing it later would mean rebuilding the UI toolkit's surfaces in another framework.
- **Owner:** the architecture spec above, and the re-plan filed from it.
- **Amended:** the language standard is C++23, not C++20 (next entry).

## 2026-10-22: The C++ language standard

- **Date:** 2026-10-22, after the operator remarked "Looks like C++ 20 is not the latest".
- **Question:** which ISO C++ standard the native stack pins.
- **Options:** C++20 (`/std:c++20`, MSVC's newest stable, ABI-stable switch); C++23 (`/std:c++23preview`, which Microsoft documents may change and may not be ABI compatible across releases, until `/std:c++23` ships); the working draft (`/std:c++latest`, which adds in-progress and experimental features).
- **Evidence:** C++23 is the current published ISO standard; MSVC Build Tools 14.51 (Visual Studio 2026 18.11, on the development machine) offers `/std:c++20`, `/std:c++23preview`, and `/std:c++latest`, and no `/std:c++23` yet (Microsoft Learn, `/std` (Specify Language Standard Version), and What's new for MSVC Build Tools 14.51).
- **Choice:** C++23 through `/std:c++23preview`, then `/std:c++23` when MSVC ships it, and C++26 when MSVC ships a switch scoped to that standard; never `/std:c++latest`. The preview ABI caveat is contained because the toolset is pinned and every library is linked statically and built by that same toolset, so a toolset move rebuilds the whole program.
- **Cost of change:** falling back to C++20 means replacing the C++23 features in use (for example `std::expected`, deducing `this`, `std::print`), mechanical but proportional to their use; each forward move is a section that rebuilds and retests everything.
- **Owner:** `docs/specs/2026-10-22-native-stack-design.md` (The toolchain), and the native spine section that pins the toolset.
