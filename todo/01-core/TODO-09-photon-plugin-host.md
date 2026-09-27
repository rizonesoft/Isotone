---
schema_version: 1
id: photon-plugin-host
domain: 01-core
status: draft
title: "TODO-09 -- Photon.Core Plug-in Host: Photoshop-Compatible Filter, Format, and Acquire Plug-ins"
depends_on: []
frozen: false
track: C9
---

# TODO-09 -- Photon.Core Plug-in Host: Photoshop-Compatible Filter, Format, and Acquire Plug-ins

> **Goal:** Nodus and Imago (and later Lumen) run third-party Photoshop-compatible plug-ins (8BF filters, format plug-ins, and acquire plug-ins) through one host in `Photon.Core`: every plug-in runs in an isolated `Photon.PluginHost.exe` process (x64, with an x86 build for 32-bit plug-ins), never inside an app, talking to the app over a named pipe with pixel tiles in shared memory, so a plug-in that crashes, hangs, or corrupts memory costs the user one dialog, not their document; plug-ins are discovered from their PiPL resources in user-chosen folders; the filter record and its callback suites are emulated from observable behavior with PSFilterPdn (MIT) as the porting reference; and one plug-in manager in `Photon.UI` lists folders, detected plug-ins, and their support status, disables a failing plug-in with a message, and shows About Plug-ins. The consuming apps own their menus and document commands (`D02 T12 §10`, `D03 T14 §11`), and Imago's G'MIC collection (`D03 T14 §13`) runs its native core in the same host process.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** There is no `src/Photon.Core/` project yet (`D01 T02 §1` creates it in Phase 2) and no plug-in host process anywhere in the suite: no `src/Photon.PluginHost/` folder, and no source file mentions PiPL, a filter record, or an 8BF file. Imago's only plug-in contract is its managed `IFilterPlugin` in `src/Imago/src/Imago.Plugins.Abstractions/IFilterPlugin.cs`, which processes 8-bit bytes in-process and is Imago-only (its managed extension modules are `D03 T14 §12`, not this file). The Nodus and Imago catalog rows for third-party plug-ins (NP-2027; IP-1033, IP-2250 to IP-2254) were backlog B-012 until the operator's 2026-09-27 decision planned them.
<!-- claim: absent src/Photon.Core -->
<!-- claim: absent src/Photon.PluginHost -->
<!-- claim: count "public interface IFilterPlugin" src/Imago/src/Imago.Plugins.Abstractions/IFilterPlugin.cs = 1 -->
<!-- claim: count "PiPL|FilterRecord|8bf" src/**/*.cs = 0 -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- refusals that name the file and the reason, progress and Cancel over one second, one log line per change, a dependency is a decision
- [`standards/testing.md`](../../standards/testing.md) -- driven runs with evidence and the unit tests each section cites
- [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) and [`docs/parity/imago-parity.md`](../../docs/parity/imago-parity.md) -- the rows the consuming sections own; this file owns no catalog rows
- Licensing, verified 2026-09-27: PSFilterPdn (github 0xC0000054/PSFilterPdn, the Paint.NET 8bf host) is MIT and is the porting reference for structure layouts and callback behavior, with its copyright notice kept in every file translated from it; PSFilterHost (same author) is MS-PL, which is not GPL-compatible, so none of its code is read into this project; Adobe's Photoshop Plug-in SDK is under Adobe's proprietary SDK license, so none of its headers or samples are copied, and the ABI is taken from PSFilterPdn and the plug-ins' observable behavior; G'MIC (CeCILL-2.1 or CeCILL-C) is consumed by `D03 T14 §13`, not here
- Test plug-ins: `tests/fixtures/plugins/` holds own filter, format, and acquire plug-ins written in C for this repository (MIT, own code), built with the MSVC toolset, with the build commands recorded; freely downloadable third-party 8BF filters are used only in driven runs, named with their version in the evidence, and never committed
- -> XREF: D02 T12 §10 -- Nodus's Bitmaps, Plug-ins menu and effect-stack entries consume §2 and §4
- -> XREF: D03 T14 §11 -- Imago's plug-in filters, format and acquire plug-ins, and plug-in preferences consume §2, §3, and §4
- -> XREF: D03 T14 §13 -- Imago's G'MIC collection runs its native core in §1's host process
- -> XREF: D04 T04 §15 -- Lumen's viewer effects browser and plug-in folders consume §2 and §4, and Lumen's publish carries §1's host (the former B-012 rows LP-1157, LP-1159, and LP-1224)
- -> XREF: D04 T11 §7 -- Lumen's batch edit pipeline runs §2's filters as a batch step with stored parameters (LP-1160)
- Prose references (no XREF because the target files are not edited here): `D01 T02 §1` (the project, app-data paths, and logging), `D01 T02 §2` (the settings store), `D01 T01 §1` and `D01 T01 §3` (the icon catalog and theme resources the manager uses), `D01 T03 §1` (`PixelBuffer<TPixel>` and tiles), `D01 T04 §1` (the gray, CMYK, and Lab conversions plug-ins may request)

## Outcome

- A third-party 8BF filter runs on a Nodus bitmap object and an Imago layer through the same host, with its own dialog, its progress, Cancel, and its parameters remembered for Repeat.
- Every plug-in runs out of process; killing the host or a plug-in crash mid-filter leaves the app running and the document unchanged, and the plug-in is disabled with a message naming it.
- Format and acquire plug-ins open, save, and import through the host, with saves written by the consuming app's atomic writer.
- One plug-in manager in `Photon.UI` shows folders, detected plug-ins with their support status, and About Plug-ins in every app that hosts.
- The licensing and isolation decision is recorded, and `grep` finds no Adobe SDK header and no MS-PL-derived file in the tree.

**Adjacency:** list=applicable @ D01 T09 §4; document=not-applicable (plug-ins produce pixels and files that the consumers print and export); settings=applicable @ D01 T09 §4; reporting=applicable @ D01 T09 §4; notifications=applicable @ D01 T09 §1; permissions=applicable @ D01 T09 §1; audit=applicable @ D01 T09 §1; exchange=applicable @ D01 T09 §3; reverse=not-applicable (a filter run is one undoable command in the consumer's history, D02 T12 §10 and D03 T14 §11; the host itself changes no document)

**Adjacency rationale:** The detected-plug-in list with its search, sort, and status filter is the list surface (§4). Settings are the plug-in folders, allow-unknown, disabled plug-ins, and remembered parameters, each an app-scoped key read by the host client. Reporting is the support status and the failure reason per plug-in. Notifications are progress and Cancel for a running plug-in and the message when one fails. Permissions is exercised on refusal: an unsigned or unknown plug-in with allow-unknown off, a folder that cannot be read, a plug-in whose architecture has no host, and a crashed plug-in are each refused by name. The audit trail is one Serilog line per plug-in load, run, failure, and disable. Exchange is the format and acquire plug-ins (§3), which read and write files other software authored.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The plug-in host decision and the isolated host process | D01 T02 §1, D01 T02 §2, D01 T03 §1 |  [ ]   |
|   2   |   §2    | 8BF filter plug-ins: discovery, the filter record, suites, and Repeat parameters | §1, D01 T04 §1 |  [ ]   |
|   3   |   §3    | Format and acquire plug-ins | §2 |  [ ]   |
|   4   |   §4    | The plug-in manager in Photon.UI | §2, D01 T01 §1, D01 T01 §3 |  [ ]   |

---

## 1. The Plug-in Host Decision and the Isolated Host Process

Photoshop plug-ins are native DLLs written against a 1990s callback ABI; loaded into an app, one bad plug-in takes the document down with it. This section records the licensing and isolation decision and builds the process every plug-in runs in: `Photon.PluginHost.exe`, a console-subsystem .NET executable with no window of its own, started per app session, talking to the app's `PluginHostClient` over a named pipe with pixel tiles in a shared `MemoryMappedFile`. It builds no plug-in ABI yet (§2 and §3 do); it proves the channel, the crash and hang handling, and the disable-on-failure record every later section relies on. Owns no catalog rows. -> SOURCE: legacy-nodus-7.4

**Fidelity:** no surface of its own (the failure message is shown by the consumers through D01 T09 §4's manager; the host has no window of its own)

- [ ] Add the decision row to `docs/dev/decisions.md`: plug-ins run only out of process in `Photon.PluginHost.exe` (x64, plus an x86 build for 32-bit plug-ins; on Windows on Arm the x64 host runs under emulation and that is stated), PSFilterPdn (MIT) is the porting reference with its notice kept, PSFilterHost (MS-PL, GPL-incompatible) and Adobe's SDK headers (proprietary) are not used, and plug-ins are third-party code the user installs at their own choice. Done when: the row names this section, the PSFilterPdn commit checked, and all three license verdicts dated 2026-09-27.
- [ ] Create `src/Photon.PluginHost/Photon.PluginHost.csproj` (console subsystem with no console window, `win-x64` and `win-x86` runtime identifiers, self-contained publish) and add it to `Photon.slnx`. Done when: `dotnet build Photon.slnx -c Release` exits 0 and both runtime identifiers publish.
- [ ] Add `src/Photon.Core/Plugins/Hosting/PluginHostProtocol.cs`: length-prefixed binary messages over a named pipe (`\\.\pipe\photon-plugin-<app pid>-<guid>`, current-user ACL only) for load, about, parameters, run, progress, cancel, callback requests, result, and error, with a protocol version checked on connect. Done when: `PluginHostProtocolTests` round-trip every message type and a version mismatch is refused by name.
- [ ] Add `SharedTileBuffer` over `MemoryMappedFile` so tiles cross the process boundary without copying through the pipe, sized from the `D01 T03 §1` tile size with a cap from settings. Done when: a test writes a 256 by 256 RGBA16 tile in one process and reads it identically in a child process.
- [ ] Add `src/Photon.Core/Plugins/Hosting/PluginHostClient.cs`: starts the host matching the plug-in's architecture on first use, connects, forwards progress to an `IProgress<PluginProgress>`, and maps Cancel to the cancel message. Done when: `PluginHostClientTests` start the host, run a no-op request, and shut it down with the process exit code 0.
- [ ] Handle host death: if the host process exits or the pipe breaks mid-request, the client returns a `PluginFailure` naming the plug-in and the exit code, restarts the host on the next request, and the caller's pixels are untouched. Done when: a test kills the host mid-request and asserts the failure, the restart, and byte-identical source tiles.
- [ ] Handle hangs: a request with no progress message for `Photon.Plugins.HangTimeoutSeconds` (default 120) offers the consumer a Wait or Stop decision, and Stop kills the host. Done when: a test with a hanging test plug-in stub asserts the timeout event and the kill.
- [ ] Add `PluginFailureRegistry`: a plug-in that crashed or hung is recorded as disabled with the reason and date in the app's settings (`<App>.Plugins.Disabled`) until the user re-enables it. Done when: a settings readback after a simulated crash shows the entry, and a new session does not load the plug-in.
- [ ] Run the host with the least privilege available: the same user, no elevation, a job object that kills the host when the app exits, and the working directory set to the plug-in's folder. Done when: a test closes the client process and asserts the host is gone within 2 seconds.
- [ ] Log one Serilog line per host start, connect, request, failure, disable, and exit in the app's log through `D01 T02 §1`, and have the host write its own log file beside the app's. Done when: a test asserts the start, request, and failure lines.
- [ ] Add the host to each app's publish output: a `PluginHost` item in the shared publish props so `Nodus`, `Imago`, and later `Lumen` each ship their own copy of the x64 and x86 host, and no app depends on another app being installed. Done when: `pwsh scripts/publish.ps1 -App Nodus` output contains `Photon.PluginHost.exe` and its x86 twin.
- [ ] Commit: `"core: the isolated plug-in host process and its client"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~PluginHost"` exits 0 with the protocol, shared-tile, client, host-death, hang, and failure-registry tests passing, and the host-death test quoted showing the source tiles byte-identical after the kill. Cheaper substitute that fails: loading plug-ins with `NativeLibrary.Load` inside the app, which the host-death test cannot survive.

## 2. 8BF Filter Plug-ins: Discovery, the Filter Record, Suites, and Repeat Parameters

The filter plug-in is what users mean by "a Photoshop plug-in": an 8BF DLL with a PiPL resource, called through `filterSelectorAbout`, `Parameters`, `Prepare`, `Start`, `Continue`, and `Finish` with a filter record full of callbacks. This section implements discovery and that record inside the host process, ported in structure from PSFilterPdn (MIT), so any consumer asks the client to run a filter on a region of pixels with an optional selection mask and gets pixels back. Filter Factory filters are ordinary 8BF files and run the same way. Owns no catalog rows (NP-2027 sits on `D02 T12 §10`; IP-1033, IP-2250, and IP-2251 on `D03 T14 §11`; Lumen's LP-1157, LP-1159, and LP-1224 on `D04 T04 §15` and LP-1160 on `D04 T11 §7`).

**Fidelity:** no surface of its own (the plug-in's own dialog is the plug-in's; menus belong to D02 T12 §10 and D03 T14 §11)

- [ ] Add `src/Photon.Core/Plugins/Discovery/PiplReader.cs` reading the PiPL resource as data (kind `8BFM`, entry points `8664` and `wx86`, name, category, supported modes, filter case info, and the `enable` info expression), with the PE resource parsed without loading the DLL. Done when: `PiplReaderTests` read every committed test plug-in and report its name, category, architecture, and modes.
- [ ] Add `PluginScanner` walking the configured folders (recursing into subfolders and following `.lnk` shortcuts as Photoshop does), returning each plug-in with its support status: supported, unsupported with a named reason (no PiPL, wrong kind, missing entry point, unsupported mode), or disabled. Done when: a scan of `tests/fixtures/plugins/` lists every plug-in with its expected status.
- [ ] Add `src/Photon.PluginHost/Filters/FilterRecord.cs`: the filter record layout for x64 and x86 with the fields filters read (image size, planes, rectangles, `inData`, `outData`, `maskData`, `maxSpace`, `imageMode`, `filterCase`, colors, resolution, and the callback pointers), with a layout test against the offsets PSFilterPdn documents. Done when: `FilterRecordLayoutTests` assert every field offset for both architectures.
- [ ] Implement the phase sequence `About`, `Parameters`, `Prepare`, `Start`, `Continue`, `Finish` with `advanceState` tiling through `inRect` and `outRect`, and the result codes mapped to `PluginFailure` messages. Done when: the committed invert test filter inverts a gradient exactly, tile by tile, and a filter returning `userCanceledErr` reports Cancel.
- [ ] Implement the buffer and handle suites (allocate, lock, unlock, dispose, size, and the legacy procs) and `maxSpace` accounting. Done when: the committed allocator test filter exercises every proc and the host reports zero leaked handles after `Finish`.
- [ ] Implement `displayPixels`, `progressProc`, `abortProc`, and `testAbortProc`, forwarding progress to the client and Cancel back to the plug-in. Done when: a slow test filter reports monotone progress through the client and stops within 1 second of Cancel.
- [ ] Implement color services (pick color through a Windows color dialog owned by the app window handle passed in, and color-space conversion through `D01 T04 §1`) and the channel ports suite for the read and write of layer, mask, and composite channels. Done when: the committed color-services test filter converts RGB to Lab through the host within 1 of the `D01 T04 §1` result.
- [ ] Pass gray, RGB, CMYK, and Lab images at 8 and 16 bits per channel where the PiPL declares the mode, converting from the consumer's buffer through `D01 T04 §1`, and refuse other modes by name. Done when: the mode test filter reports the mode it received for each supported combination and an undeclared mode is refused before the plug-in loads.
- [ ] Pass the selection as `maskData` with `filterCase` set for flat, floating, and editable-transparency cases, and apply the plug-in's output through the mask on the consumer side. Done when: a feathered-mask test blends the inverted result by the mask within 1 of 255.
- [ ] Implement parameters for Repeat and presets: the plug-in's `parameters` handle and its scripting descriptor (the `PIDescriptorParameters` read and write procs) are serialized per plug-in into a `FilterParameterBlob` the consumer stores, and replayed without showing the dialog. Done when: running the parameterized test filter once with a dialog value and once through Repeat produces identical pixels.
- [ ] Parent the plug-in's dialog to the consuming app's window through the handle the client passes (`platformData.hwnd`), so it is modal over the app, not a stray window. Done when: a driven run with a freely downloadable third-party filter (named with its version) shows its dialog over the Nodus window, capture committed to `docs/captures/nodus/plugin-dialog/`.
- [ ] Commit the test plug-ins under `tests/fixtures/plugins/filters/` (invert, allocator, slow, mode, color services, parameterized, and a crashing filter; x64 and x86 builds) with their C sources, `LICENSE` (MIT, own code), and the `cl.exe` build command in `reference.txt`. Done when: every binary's build command is recorded and reproduces the committed hash.
- [ ] Commit: `"core: 8BF filter plug-ins in the isolated host"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~FilterPlugin|FullyQualifiedName~PiplReader|FullyQualifiedName~FilterRecordLayout"` exits 0 with the invert filter exact, Repeat identical to the dialog run, the crashing filter reported as a `PluginFailure` with the app process alive, and the third-party filter's driven run captured. Cheaper substitute that fails: a host that only calls `filterSelectorStart` once over the whole image, which tiling filters and the `advanceState` test reject.

## 3. Format and Acquire Plug-ins

Photoshop's format plug-ins (kind `8BIF`) open and save file types the app does not know, and acquire plug-ins (kind `8BAM`) import from scanners and cameras through vendor drivers; Imago's catalog asks for both (IP-2252), and the host from §1 and the record machinery from §2 carry them. The host returns decoded pixels and writes encoded bytes to the consumer's stream, so every save is written by the consuming app's atomic writer, never by the plug-in to the user's file. Owns no catalog rows (IP-2252 sits on `D03 T14 §11`).

**Fidelity:** no surface of its own (File menu entries and format lists belong to D03 T14 §11; the plug-in's own options dialog is the plug-in's)

- [ ] Extend `PiplReader` and `PluginScanner` for kinds `8BIF` (with the format's extensions, file types, and read, write, and layers flags) and `8BAM`. Done when: the committed test format and acquire plug-ins are listed with their extensions and kinds.
- [ ] Add `src/Photon.PluginHost/Formats/FormatRecord.cs` and the read phases (`ReadPrepare`, `ReadStart`, `ReadContinue`, `ReadFinish`) with the host feeding the file through a read-only stream proxy from the consumer. Done when: the committed test format plug-in opens its fixture file to the expected pixels exactly.
- [ ] Add the write phases (`OptionsPrepare`, `OptionsStart`, `EstimatePrepare`, `EstimateStart`, `WritePrepare`, `WriteStart`, `WriteContinue`, `WriteFinish`), with the plug-in's writes captured into a buffer that the client hands to the consumer's `Stream`; the plug-in never receives the destination path. Done when: saving through the test format plug-in produces bytes identical to its reference encoder, and the destination file is written only by the consumer's atomic writer (asserted by a file-watcher test seeing one rename).
- [ ] Add `src/Photon.PluginHost/Acquire/AcquireRecord.cs` and the acquire phases (`Prepare`, `Start`, `Continue`, `Finish`, `Finalize`), returning each acquired image to the client as pixels with resolution and mode. Done when: the committed test acquire plug-in returns its generated image exactly.
- [ ] Map format and acquire errors (`formatCannotRead`, `userCanceledErr`, memory errors, and plug-in crashes) to `PluginFailure` messages naming the plug-in and the file. Done when: a corrupt fixture read through the test format plug-in is refused by name and the host keeps running for the next request.
- [ ] Add `IFormatPluginSource` for consumers to list format plug-ins as extra open and save formats with their extensions and capabilities. Done when: a test lists the test format plug-in's extension with read and write flags.
- [ ] Commit the test format and acquire plug-ins under `tests/fixtures/plugins/formats/` and `acquire/` with their C sources, MIT `LICENSE`, fixture files, and build commands. Done when: every binary's build command is recorded.
- [ ] Commit: `"core: format and acquire plug-ins in the isolated host"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~FormatPlugin|FullyQualifiedName~AcquirePlugin"` exits 0 with the test format plug-in's open matching its fixture pixel-exact, its save byte-identical to the reference encoder and written through one atomic rename, and the acquire plug-in's image exact. Cheaper substitute that fails: handing the plug-in the destination path, which the one-rename assertion catches.

## 4. The Plug-in Manager in Photon.UI

Every competitor has a place to point at plug-in folders and see what loaded: Photoshop's Plug-ins preferences and About Plug-ins, Affinity's Photoshop plug-in settings (default folder, search folders, support folder authorization, detected list with support status, allow unknown, restart), and CorelDRAW's Plug-ins option page. This section builds that one surface in `Photon.UI` so each hosting app embeds the same view with its own settings scope, rather than each app drawing its own. Owns no catalog rows (IP-2253 and IP-2254 sit on `D03 T14 §11`; NP-2027's option page on `D02 T12 §10`).

**Fidelity:** new build, no baseline; captured through the first consumer to `docs/captures/nodus/plugin-manager/`.
**Job:** a user can add and remove plug-in folders, see which plug-ins loaded and why others did not, re-enable one that was disabled after a failure, and read a plug-in's About box. Consumer: `PluginScanner` and `PluginFailureRegistry`, which read the folders, allow-unknown, and disabled settings this surface writes.
**Treatment:** a settings page with a folder list (add, remove, open in Explorer), an allow-unknown check box, a detected-plug-ins list (name, kind, category, architecture, file, and status with the reason as a tooltip) with search and a status filter, Enable and Disable, About, and Rescan, plus a restart banner when a change needs one. Cheaper substitute that fails the checkpoint: a single folder text box with no status list, which cannot show why a plug-in did not load.
**Chrome:** consume the `D01 T01 §3` theme resources, the `D01 T01 §1` icon catalog, and the `D01 T02 §2` settings store through an app-scoped key prefix. Do not add a second list control style or a second folder picker.

**Requires:** display-session -- the manager page, its lists, and the About box need an interactive desktop

- [ ] Add `src/Photon.UI/Plugins/PluginManagerViewModel.cs` (CommunityToolkit.Mvvm) over `PluginScanner`, taking an app scope (`Nodus`, `Imago`, `Lumen`) that prefixes every settings key. Done when: `PluginManagerViewModelTests` load a scan of the fixtures and expose each plug-in with its status.
- [ ] Add the folder list: the default folder `%LOCALAPPDATA%\Photon\<App>\Plug-ins` created on first use, add and remove search folders through the shared folder picker, and store them in `<App>.Plugins.Folders`. Done when: a settings readback after adding and removing a folder shows the list and the default folder exists.
- [ ] Add the support-folder authorization Affinity requires: a folder outside the user profile is added only after the user confirms it, recorded in `<App>.Plugins.AuthorizedFolders`. Done when: a view-model test asserts an unconfirmed outside folder is not scanned.
- [ ] Add the allow-unknown setting (`<App>.Plugins.AllowUnknown`, default off): plug-ins whose PiPL declares no supported host or an unrecognized kind are listed as unsupported unless it is on. Done when: toggling it moves the unknown test plug-in between unsupported and supported in the list.
- [ ] Add the detected list with search, a status filter (all, supported, unsupported, disabled), and the reason as a tooltip, one row per plug-in. Done when: filtering by status shows exactly the expected fixtures and the tooltip names the reason.
- [ ] Add Enable and Disable over `PluginFailureRegistry` and `<App>.Plugins.Disabled`, including re-enabling a plug-in disabled after a failure with its failure reason shown first. Done when: a settings readback after disabling and re-enabling the crashing test filter shows the entry removed and the reason was displayed.
- [ ] Add About and About Plug-ins: About runs the plug-in's `filterSelectorAbout` in the host with the dialog parented to the app window, and About Plug-ins lists every loaded plug-in with its version from the PE version resource. Done when: a driven run shows the invert test filter's About box, capture committed.
- [ ] Add Rescan and the restart banner: changes to folders take effect on Rescan, and a change that requires restarting the host (architecture set, allow-unknown) shows the banner with a Restart Host button. Done when: a view-model test asserts which changes raise the banner.
- [ ] Add `src/Photon.UI/Plugins/PluginManagerView.xaml` in the house style as a page the consumers embed in their preferences, reachable by keyboard with automation names on every control. Done when: an automation-tree test finds every control by name and the capture shows the page in both themes.
- [ ] Add `PluginFailureNotice`, the one message every consumer shows when a plug-in fails ("<plug-in> stopped responding and was disabled. Your document was not changed."), with a link to the manager. Done when: a view-model test asserts the text names the plug-in and the link opens the manager page.
- [ ] Log one Serilog Information line per folder change, enable, disable, and rescan. Done when: a test asserts each line.
- [ ] Commit captures under `docs/captures/nodus/plugin-manager/` (folders, the detected list with each status, the restart banner, and an About box) and write `docs/user/shared/plugins.md` that each app's user guide links to. Done when: every control appears in a capture and the page documents it.
- [ ] Commit: `"ui: the shared plug-in manager"`

**Test checkpoint:** Driven run with evidence and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~PluginManager"` exits 0; in a driven run of the built manager page, adding the fixtures folder lists every test plug-in with its expected status, disabling and re-enabling the crashing filter round-trips through settings (readback quoted), and the About box capture is committed under `docs/captures/nodus/plugin-manager/`. Cheaper substitute that fails: a folder text box with no detected list, which cannot show the unsupported reasons the filter test asserts.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every `PluginHost`, `FilterPlugin`, `FormatPlugin`, `AcquirePlugin`, and `PluginManager` class reporting
- [ ] `grep -rln "PIFilter.h\|PIGeneral.h\|Adobe Systems Incorporated" src` prints nothing (no Adobe SDK header or sample in the tree), and every file translated from PSFilterPdn keeps its MIT notice
- [ ] `grep -rn "NativeLibrary.Load\|LoadLibrary" src --include=*.cs` prints paths only under `src/Photon.PluginHost/`
- [ ] Killing `Photon.PluginHost.exe` during a filter run in each hosting app leaves the app running and the document unchanged (driven run quoted per app)
- [ ] `python scripts/todo-graph.py validate` clean
