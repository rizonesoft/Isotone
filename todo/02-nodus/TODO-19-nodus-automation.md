---
schema_version: 1
id: nodus-automation
domain: 02-nodus
status: draft
title: "TODO-19 -- Nodus Automation: the Object Model, Actions, Scripts, and Batch"
depends_on: []
frozen: true
track: N19
---

# TODO-19 -- Nodus Automation: the Object Model, Actions, Scripts, and Batch

> **Goal:** After the first release, Nodus takes part in the suite-wide automation system of `D01 T10` (operator decision 2026-09-27, planning the work deferred "after the first release" as real sections because the operator worried "features will be left behind"): every Nodus command is recordable into actions and playable back as one undo step, a documented C# object model drives documents, pages, layers, elements, styles, symbols, and export from scripts, the Scripts menu and Scripts docker list and run scripts, macros can travel inside a Nodus document without ever running on open, the automation and MCP servers expose Nodus to outside tools behind explicit permissions, extensions add panels and commands, and files are batch processed through actions from the Batch dialog, droplets, and the command line. Every Illustrator and CorelDRAW automation row of the parity catalog (NP-2751 to NP-2761) is planned here.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Nodus has no automation of any kind. Its projects are still `src/Nodus/Bezier.Core` and `src/Nodus/Bezier.Desktop` (renamed `Photon.Nodus.*` by `D02 T01 §1`); no Nodus source file mentions a macro, a script engine, or Roslyn, and there is no Scripts menu. The suite scripting engine is Imago's 62-line Roslyn `ScriptEngine` in `src/Imago/src/Imago.Scripting/`, which `D01 T10 §4` moves to `src/Photon.Core/Scripting/`. `Photon.Core` and `Photon.UI` do not exist yet. The eleven automation rows of `docs/parity/nodus-parity.md` (NP-2751 to NP-2761) were backlog B-041 and B-042 until this file planned them.
<!-- claim: exists src/Nodus/Bezier.Core -->
<!-- claim: count "Macro|ScriptEngine|Roslyn" src/Nodus/**/*.cs = 0 -->
<!-- claim: lines src/Imago/src/Imago.Scripting/ScriptEngine.cs = 62 -->
<!-- claim: absent src/Photon.Core -->
<!-- claim: exists docs/parity/nodus-parity.md -->

## Inputs

- [`standards/nodus.md`](../../standards/nodus.md) -- SVG is native and one reader and one writer own it; embedded macros ride the `nodus:` namespace through them
- [`standards/shared.md`](../../standards/shared.md) -- one undo history, one log line per document change, atomic saves, a dependency is a decision
- [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the Automation area rows NP-2751 to NP-2761 this file owns, and NP-0631 whose note names §1
- Illustrator scripting and actions help (Automation with actions, Scripting) and the CorelDRAW macro and scripting help (Scripts docker, Script editor, macro security) -- the observable behaviors the rows cite
- -> XREF: D01 T10 §1 -- the action model, recorder, and player every Nodus command records into
- -> XREF: D01 T10 §2 -- the Actions panel §1 docks in Nodus
- -> XREF: D01 T10 §4 -- the scripting host, trust rules, and Scripts menu model §2 hosts
- -> XREF: D01 T10 §5 -- the script editor and console §2 hosts
- -> XREF: D01 T10 §6 -- the automation and MCP servers §2 registers Nodus tools with
- -> XREF: D01 T10 §7 -- the extension SDK whose Nodus contributions §2 wires
- -> XREF: D01 T10 §8 -- the command-line parser §3 registers Nodus's switch table with
- -> XREF: D01 T10 §9 -- the suite batch runner and droplets §3 hosts
- -> XREF: D02 T07 §1 -- the live-object contract and the `nodus:` namespace embedded scripts persist through (§2)
- -> XREF: D02 T14 §15 -- Export for Screens presets the batch export of §3 reuses
- -> XREF: D02 T16 §3 -- Nodus menus and shortcut sets the Scripts menu and recordable commands join
- -> XREF: D02 T17 §12 -- Nodus 1.2.0 releases this file

## Outcome

- Every command in Nodus's `CommandIndex` records into an action with its parameters, and playing the action on another document reproduces the edit as one undo step.
- `Photon.Nodus.Scripting` documents the Nodus object model, and a C# script can create, inspect, restyle, and export a document.
- The Scripts menu and Scripts docker list user and startup scripts; the script editor and console run them with line-numbered errors.
- Macros embedded in a Nodus document survive save and reopen, never run on open, and run only after the user trusts them.
- The automation and MCP servers expose Nodus tools only behind their permission categories, all off by default.
- The Batch dialog, droplets, and `Nodus.exe --batch` or `--export` process folders through actions without ever overwriting a source unless the user chose save and close.

**Adjacency:** list=applicable @ D02 T19 §2; document=not-applicable (automation prints nothing; exports are D02 T14's); settings=applicable @ D02 T19 §2; reporting=applicable @ D02 T19 §3; notifications=applicable @ D02 T19 §3; permissions=applicable @ D02 T19 §2; audit=applicable @ D02 T19 §1; exchange=applicable @ D02 T19 §2; reverse=applicable @ D02 T19 §1

**Adjacency rationale:** Scripts, actions, and extensions are listed in the Scripts docker, the Actions panel, and the extension manager. Script trust, server permissions, and the embedded-macro policy are settings with named consumers. The batch run writes a report and a completion toast. Refusals are exercised: an untrusted embedded macro, a refused MCP permission, a read-only destination. Every recording and playback writes a log line, and every playback is one undo step, so the reverse is Undo; exchange is action files, script files, and embedded macros travelling in documents.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The Nodus object model and recordable commands | D01 T10 §1, D01 T10 §2, D01 T10 §4, D02 T17 §11 |  [ ]   |
|   2   |   §2    | Scripts, extensions, and macros in Nodus documents | §1, D01 T10 §5, D01 T10 §6, D01 T10 §7, D02 T07 §1 |  [ ]   |
|   3   |   §3    | Batch processing and the command line in Nodus | §1, D01 T10 §8, D01 T10 §9, D02 T14 §15 |  [ ]   |

---

## 1. The Nodus Object Model and Recordable Commands

Illustrator records actions from menu commands and tool operations and replays them on other documents; CorelDRAW records macros and saves the undo list as a script. Nodus gets both through the suite system of `D01 T10 §1`: every Nodus command implements `IRecordableCommand` with typed parameters, tool drags record as paths, the Actions panel of `D01 T10 §2` docks in Nodus, and the typed object model a script drives is the same surface the recorder records against, so a recorded action and a script never disagree about what a command does. Playback is one undo transaction; nothing here writes a file. Catalog: NP-2752, NP-2753, NP-2761 (3 features: record and play back actions or macros; action sets and recording project management; save undo history as a script). NP-0631 (align and distribute shortcuts) keeps its row in `D02 T08 §14` and records through this section. -> SOURCE: parity-nodus-automation

**Fidelity:** Nodus Actions panel and its recording state -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/ActionsPanel/.
**Design:** new surface: docs/design/components/ActionsPanel/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md, docs/design/components/StatusBar/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a Nodus user records a sequence of edits once and replays it on other objects and documents. Consumer: `ActionPlayer` replaying into `UndoHistory`, and the scripts `ActionScriptWriter` produces.
**Treatment:** the suite Actions panel docked in Nodus's panel area with Nodus's built-in action set, a red recording dot in the status bar while recording, and Edit, Save Undo History as Script. Cheaper substitute that fails the checkpoint: a macro that replays mouse coordinates, which the different-document playback test catches.
**Chrome:** consume `ActionRecorder`, `ActionPlayer`, `ActionsPanelView` from `Photon.UI`, `CommandIndex`, and `UndoHistory`. Do not build a Nodus-only recorder or panel.

**Requires:** display-session -- recording from the canvas and the panel capture need an interactive desktop

- [ ] Before any XAML, extend `docs/design/components/ActionsPanel/README.md` (written by `D01 T10 §2`) with Nodus's step kinds (tool drag recorded as a path, selection by name, artboard target) and its preview card, and regenerate the design page with `python scripts/build-design-site.py`. Done when: the spec lists the step kinds and `python scripts/build-design-site.py --check` passes.
- [ ] Add the object model project `src/Nodus/Photon.Nodus.Scripting/` (referencing `Photon.Nodus.Core` and `Photon.Core`) with `NodusApp`, `NodusDocument`, `Pages`, `Artboards`, `Layers`, `Element` (with `Path`, `Shape`, `Text`, `Group`, `Bitmap`, `SymbolInstance` subtypes), `Selection`, `Styles`, `Swatches`, `Symbols`, and `ExportOptions`, each member XML-documented. Done when: the project builds with `GenerateDocumentationFile` and warnings as errors, so an undocumented public member fails the build.
- [ ] Make every object-model setter go through the command it names (for example `Element.Fill = ...` executes `SetFillCommand`), never the model directly. Done when: `NodusObjectModelTests.SettersRecordCommands` asserts one history entry per setter and an architecture test finds no object-model type referencing a mutable model field.
- [ ] Implement `IRecordableCommand` (from `D01 T10 §1`) on every command in Nodus's `CommandIndex`: a stable command id, typed parameters (`Point`, `Size`, `Color`, `string`, enums), and `Describe()` text for the panel. Done when: `NodusRecordableCommandTests.EveryIndexedCommandIsRecordable` enumerates the index and finds none without a descriptor.
- [ ] Record tool operations as parameterized steps: a rectangle, ellipse, polygon, or star drag records its bounds, a pen or pencil stroke records its path data, a move or transform records its matrix, relative to the selection when `Photon.Automation.RecordRelative` is on (Illustrator records transforms, not mouse moves). Done when: a recorded rectangle drag replays at the same bounds in a new document and, with relative recording, at the same offset from a different selection.
- [ ] Record selection by name and by kind (`SelectByName`, `SelectSameFill`) and target artboards by index or name, with an explicit "no selection" refusal on playback. Done when: playback over a document missing the named element stops with "Step 3: no element named 'Logo'" and leaves the document unchanged.
- [ ] Host `ActionsPanelView` as a dockable Nodus panel through the `D01 T01 §8` dock, with Window, Actions and its shortcut from `D02 T16 §3`. Done when: a driven run opens the panel from the menu and from the shortcut, and the capture is committed.
- [ ] Ship the built-in Nodus action set (`resources/actions/nodus-default.photon-actions`: outline stroke and expand, convert text to outlines, fit artboard to artwork, release all clipping masks, export selection as SVG, rasterize at 300 ppi) loaded through `D01 T10 §3`. Done when: `NodusDefaultActionsTests` plays each action on a fixture and asserts the result.
- [ ] Play an action on the whole document, the selection, or every artboard (`ActionPlayTarget`), each as one undo transaction named "Action: <name>". Done when: `NodusActionPlaybackTests.OneUndoStep` plays a five-step action and one Ctrl+Z restores the document hash.
- [ ] Record the dialog-driven commands (Offset Path, Transform Each, Export) with their dialog values and honour the dialog toggle: on, the dialog opens pre-filled; off, the recorded values apply silently. Done when: tests assert both modes for Transform Each.
- [ ] Record action projects (CorelDRAW recording project management, NP-2753): named sets saved per user in the suite actions folder, with rename, duplicate, and delete through the panel. Done when: a set created, renamed, and deleted leaves the folder listing as expected and each change writes one log line.
- [ ] Add Edit, Save Undo History as Script (NP-2761): the current history converted by `ActionScriptWriter` into a C# `.csx` file through the Save dialog. Done when: `SaveHistoryAsScriptTests` saves a history of six edits, runs the script on the original document through `D01 T10 §4`, and the result's SVG equals the edited document's SVG.
- [ ] Show recording state: the status bar's red dot and "Recording: <action>" text, and Escape or the panel's Stop ends recording. Done when: a driven run captures the recording state and the log shows `Action recording started` and `stopped` lines.
- [ ] Commit the panel captures under `docs/captures/nodus/actions/` and write `docs/user/nodus/actions.md` (recording, relative recording, dialogs, sets, saving history as a script). Done when: every control of the Treatment appears in a capture and the page documents it.
- [ ] Commit: `"nodus: the Nodus object model and recordable actions"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~NodusRecordableCommandTests|FullyQualifiedName~NodusActionPlaybackTests|FullyQualifiedName~SaveHistoryAsScriptTests|FullyQualifiedName~NodusObjectModelTests"` exits 0, proving every indexed command is recordable, playback is one undo step, and a history saved as a script reproduces the edited SVG; a driven run records a rectangle and a fill change, plays the action on a second document, and commits the capture under `docs/captures/nodus/actions/`. Cheaper substitute that fails: recording mouse coordinates, which the different-document playback test catches.

## 2. Scripts, Extensions, and Macros in Nodus Documents

CorelDRAW users run macros from the Scripts docker and keep macro projects inside documents; Illustrator users run scripts from File, Scripts and add extension panels; both now expose an MCP server to outside AI tools. Nodus does these jobs on the suite system: C# scripts through `D01 T10 §4` (decision 1: one language for the suite; VBA, VSTA, and JavaScript are not provided, and other languages drive Nodus from outside through the automation server of `D01 T10 §6`), the editor and console of `D01 T10 §5`, extensions from `D01 T10 §7`, and macros embedded in the SVG document through the `D02 T07 §1` contract. An embedded macro never runs on open. Catalog: NP-2751, NP-2755, NP-2756, NP-2757, NP-2758, NP-2759, NP-2760 (7 features: extension panels and plug-in SDKs; scripts menu and scripts docker; scripting languages and macro runtimes; MCP server for external AI tools; macro projects embedded in documents; macro security and trusted publishers; script editor and object model reference). -> SOURCE: parity-nodus-scripts

**Fidelity:** Nodus Scripts menu, Scripts docker, and the embedded-macro trust prompt -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/scripts/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/Toast/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a Nodus user runs, writes, and shares scripts and macros, and lets trusted outside tools drive Nodus. Consumer: `ScriptHost` running the script, the document writer persisting embedded macros, and MCP clients reading tool results.
**Treatment:** File, Scripts with the user and startup scripts and Other Script; a Scripts docker (CorelDRAW's) listing scripts, embedded macros, and extension commands with Run, Edit, and New; a trust prompt naming each embedded macro with its code viewable before anything runs. Cheaper substitute that fails the checkpoint: running embedded macros on open, which the never-runs-on-open test catches.
**Chrome:** consume `ScriptHost`, `ScriptMenuBuilder`, `ScriptEditorView`, `AutomationServer`, `ExtensionHost`, and the trust store from `Photon.Core` and `Photon.UI`. Do not add a Nodus script runner or trust list.

**Requires:** display-session -- the Scripts menu, docker, editor, and trust prompt captures need an interactive desktop

**Freeze check:** Embedded macros are written only through the atomic SVG writer of `D02 T04 §1`; a document with no embedded scripts saves byte-identical to the save before this section (hash comparison in `EmbeddedScriptSerializationTests.NoScripts_ByteIdentical`); killing the process mid-save leaves the original byte-identical. Fixture source: `tests/fixtures/nodus/automation/embedded-macros.svg` (created by this section).

- [ ] Register `NodusScriptGlobals : IScriptGlobals` exposing `App` (`NodusApp`), `ActiveDocument`, `Log`, and read-only `Settings`, with the script references limited to `Photon.Nodus.Scripting` and the BCL. Done when: `NodusScriptGlobalsTests` run a script that adds a rectangle and asserts one undo step, and a script referencing `Photon.Nodus.Desktop` fails to compile with a named error.
- [ ] Build File, Scripts from `ScriptMenuBuilder` over `%APPDATA%\Rizonesoft\Photon\Scripts\Nodus\` and the startup folder, with Other Script (NP-2755, Illustrator AI-1231). Done when: dropping a `.csx` into the folder adds a menu item without restart and running it logs `Script run {Name} {Milliseconds}`.
- [ ] Add the Scripts docker `src/Nodus/Photon.Nodus.Desktop/Views/Automation/ScriptsDockerView.xaml` (CorelDRAW CD-2920 to CD-2929): script folders, embedded macros of the active document, and extension commands in one tree with Run, Edit, New, Rename, Delete, and Reveal in Explorer. Done when: a driven run creates, runs, renames, and deletes a script from the docker and the capture is committed.
- [ ] Host `ScriptEditorView` from `D01 T10 §5` for Edit and New (NP-2760), with the object model reference browser generated from `Photon.Nodus.Scripting`'s XML documentation. Done when: the browser lists `NodusDocument.Export` with its summary and a compile error in the editor jumps to its line.
- [ ] Record the language decision in `docs/user/nodus/scripting.md` (NP-2756): C# scripts cover the jobs of Illustrator's JavaScript and CorelDRAW's VBA and VSTA macros; VBA, VSTA, and ExtendScript files are not run; Python, JavaScript, and other languages drive Nodus from outside through the automation server's documented protocol. Done when: the page carries a table mapping each language to its Photon route, and running a `.vba` or `.jsx` file is refused with that message.
- [ ] Add the embedded macro model: a `<nodus:scripts>` element under the SVG root holding `<nodus:script name="..." sha256="...">` entries with the C# source as CDATA, read and written through the `D02 T07 §1` contract and the `nodus:` namespace (NP-2758, CD-2912, CD-2926). Done when: `EmbeddedScriptSerializationTests.RoundTrip` saves two scripts, reopens, and asserts names, sources, and hashes equal.
- [ ] Never run an embedded macro on open: opening a document with embedded scripts shows the trust prompt listing each script with View Code, Trust Once, Always Trust This Document (by content hash), and Don't Run. Done when: `EmbeddedScriptTrustTests.NeverRunsOnOpen` opens the fixture and asserts zero `ScriptHost` runs until a trust decision.
- [ ] Apply macro security (NP-2759, CD-2916 to CD-2919, CD-2951) through the `D01 T10 §4` trust store: trusted folders, trusted publishers for signed `.photon-script` packages, the never-run list, and a policy setting `Nodus.Scripts.EmbeddedPolicy` (Prompt default, Disable, Trusted Publishers Only). Done when: tests assert each policy's behavior over a signed and an unsigned fixture.
- [ ] Add File, Document Properties, Scripts to view, add from a file, remove embedded scripts, and the export option "Strip embedded scripts" (default on for SVG export and web exports). Done when: an exported SVG carries no `nodus:scripts` element by default and does with the option off.
- [ ] Register Nodus tools with the MCP server of `D01 T10 §6` (NP-2757, AI-1242, AI-1243): `nodus.document.info`, `nodus.elements.list`, `nodus.elements.select`, `nodus.style.apply`, `nodus.export`, and `nodus.script.run`, each tagged with its permission category (files, scripts, AI tools). Done when: `NodusMcpToolTests` call each tool through the in-process test client with its permission granted and assert a refusal naming the category with it denied.
- [ ] Contribute Nodus's extension points to `D01 T10 §7` (NP-2751, AI-1210, AI-1233): dockable panels, commands in `CommandIndex`, menu contributions, a selection-changed event, and an export-provider contract (`INodusExportProvider`). Done when: the sample extension from `samples/extensions/` adds a panel and a command to Nodus in a driven run and the capture is committed.
- [ ] Add Nodus's scripting examples (`resources/scripts/nodus/`: batch rename layers, export each artboard as PNG, replace a color across the document, create a calendar grid). Done when: `NodusScriptExamplesTests` run each example on a fixture and assert the result.
- [ ] Commit captures under `docs/captures/nodus/scripts/` and extend `docs/user/nodus/scripting.md` with the Scripts menu, the docker, embedded macros, security, extensions, and MCP permissions. Done when: every Treatment control appears in a capture and the page documents it.
- [ ] Commit: `"nodus: scripts, extensions, MCP tools, and macros embedded in documents"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~EmbeddedScript|FullyQualifiedName~NodusScriptGlobalsTests|FullyQualifiedName~NodusMcpToolTests|FullyQualifiedName~NodusScriptExamplesTests"` exits 0, proving embedded macros round-trip, never run on open, a document without macros saves byte-identical, and every MCP tool is refused without its permission; a driven run opens the fixture, captures the trust prompt, trusts once, runs a macro, and commits the captures under `docs/captures/nodus/scripts/`. Cheaper substitute that fails: auto-running embedded macros, which `EmbeddedScriptTrustTests.NeverRunsOnOpen` catches.

## 3. Batch Processing and the Command Line in Nodus

Illustrator's Batch runs an action over a folder of documents with save and export options, and CorelDRAW users script conversions from the command line. Nodus hosts the suite batch runner of `D01 T10 §9` with Nodus's own open, save, and export options, adds droplets, and registers a Nodus switch table with the `D01 T10 §8` parser so `Nodus.exe --export png --artboards all *.svg` works without the window. Sources are never overwritten unless the user chose save and close, and then atomically. Catalog: NP-2754 (1 feature: batch processing of files). -> SOURCE: parity-nodus-batch

**Fidelity:** the suite Batch dialog hosted in Nodus with Nodus's options -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/batch/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Progress/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a Nodus user converts or exports a folder of vector files through an action without opening each one. Consumer: the written output files and the batch report.
**Treatment:** File, Automate, Batch opening the suite Batch dialog with a Nodus options group (open as: all pages or first page; export: format, artboards, scale; save: SVG options), Create Droplet, and the command line. Cheaper substitute that fails the checkpoint: a loop that opens each file in a window, which the headless run catches.
**Chrome:** consume `BatchRunner`, `ActionBatchOperation`, `BatchDialogView`, `DropletWriter`, `CommandLineParser`, and `TokenEngine` from `Photon.Core` and `Photon.UI`. Do not add a Nodus batch engine.

**Requires:** display-session -- the Batch dialog and droplet captures need an interactive desktop

**Freeze check:** Batch outputs are new files written through `AtomicFileWriter`; save and close over a source runs only when chosen, through the atomic SVG writer; killing a run leaves every source byte-identical or fully replaced, never partial (`NodusBatchFreezeTests`). Fixture source: `tests/fixtures/nodus/batch/` (created by this section).

- [ ] Add `NodusOpenOperation` and `NodusSaveOperation` implementing `IBatchOperation` (open all pages or the first, suppress font substitution dialogs with a report line, save as SVG with the D02 T14 §1 options). Done when: `NodusBatchOperationTests` open and save the fixtures headless and the report lists each substitution.
- [ ] Add `NodusExportOperation` over Export for Screens presets of `D02 T14 §15` (formats, scales, artboards, pages, and suffix tokens). Done when: exporting three fixtures at 1x and 2x PNG writes six files named by the token pattern.
- [ ] Register the Nodus options group in the suite Batch dialog through `IBatchOptionsProvider`, with File, Automate, Batch in the menu of `D02 T16 §3`. Done when: a driven run opens the dialog from the menu and the Nodus group shows, and the capture is committed.
- [ ] Run a recorded action per file through `ActionBatchOperation`, with "Override action Open commands" and "Override action Save As commands" honoured for Nodus's open and export commands. Done when: a test action containing an Export step writes to the batch destination, not the recorded path, with the override on.
- [ ] Add Create Droplet for Nodus through `DropletWriter`, writing the `.photon-droplet` and the `.lnk` targeting `Nodus.exe --droplet`. Done when: `NodusDropletTests` create a droplet, invoke `Nodus.exe --droplet <file> <fixture>` as the shortcut would, and assert the output file.
- [ ] Register the Nodus switch table with `D01 T10 §8` through `NodusSwitchProvider`: `--export <format>`, `--scale`, `--pages`, `--artboards`, `--convert <format>`, `--out <folder>`, `--script <file.csx>`, `--action "<set>/<action>"`, and `--batch <profile>`. Done when: `NodusCommandLineTests` parse each switch, and `docs/user/photon/command-line.md` regenerates with the Nodus table.
- [ ] Run command-line work headless: no main window, progress to standard error when attached to a console, results to the log, and the exit codes of the suite table. Done when: `Nodus.exe --export pdf --out <temp> <fixture>.svg` exits 0 with a PDF written and no window created (asserted through the process's main window handle being zero).
- [ ] Refuse a read-only or locked destination by name before any output is written, and a source another process holds with a skip line in the report. Done when: tests over a read-only folder and a locked file assert the refusal and the skip.
- [ ] Write the batch report (`batch-report.txt` beside the outputs when `Photon.Batch.WriteReport` is on) and the completion toast notification with Open Folder. Done when: a run with one failing file reports it and the notification shows the count.
- [ ] Commit fixtures `tests/fixtures/nodus/batch/` (five SVG, one AI, one PDF, one corrupt SVG) and add `NodusBatchFreezeTests` killing a save-and-close run mid-way. Done when: the test asserts every source is byte-identical or fully replaced.
- [ ] Commit captures under `docs/captures/nodus/batch/` and write `docs/user/nodus/batch.md` (the dialog, overrides, droplets, and command-line examples). Done when: the page documents every option and switch.
- [ ] Commit: `"nodus: batch processing, droplets, and the Nodus command line"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~NodusBatch|FullyQualifiedName~NodusDropletTests|FullyQualifiedName~NodusCommandLineTests"` exits 0, proving the override semantics, the headless export, the refusals, and the freeze check; a driven batch over `tests/fixtures/nodus/batch/` writes the expected outputs with its report quoted and the dialog captured under `docs/captures/nodus/batch/`. Cheaper substitute that fails: opening each file in a window, which the zero-window-handle assertion catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Nodus.Scripting|FullyQualifiedName~NodusBatch|FullyQualifiedName~EmbeddedScript"` exits 0
- [ ] `grep -rn "class ActionRecorder\|class ScriptHost\|class BatchRunner" src` prints only paths under `src/Photon.Core/`, so Nodus added no second engine
- [ ] Every row NP-2751 to NP-2761 in `docs/parity/nodus-parity.md` names a section of this file, and each section's Catalog line matches
- [ ] `python scripts/todo-graph.py validate` clean
