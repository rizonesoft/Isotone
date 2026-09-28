---
schema_version: 1
id: gesso-parity-type-vector
domain: 03-gesso
status: draft
title: "TODO-16 -- Gesso Parity: Type, Paths, Shapes, and Vector Layers"
depends_on: []
track: I16
---

# TODO-16 -- Gesso Parity: Type, Paths, Shapes, and Vector Layers

> **Goal:** A Gesso user sets live point, paragraph, and frame text in any script with full character, paragraph, OpenType, and style control, draws and edits paths with the pen family, keeps a Paths panel with clipping paths and path booleans, and builds live shapes, GIMP-style vector layers, and frames, exporting them as SVG; everything stays editable until the user rasterizes. The code is the suite's, not a copy: §1 to §4 move the Stilus text engine, rich-text model, fonts, composers, styles, spell checking, and type panels (`D02 T10 §1` to `D02 T10 §13`) into `src/Isotone.Core/Text/` and `src/Isotone.UI/Text/`, and §5 to §7 move path geometry, booleans, node editing, and live-shape generators (`D02 T08 §1`, `D02 T08 §4`, `D02 T08 §6`, `D02 T08 §7`, `D02 T08 §10`) into `src/Isotone.Core/Vector/`, with Gesso-specific layers in `src/Gesso/Isotone.Gesso.Core/Layers/` and tools in `src/Gesso/Isotone.Gesso.Desktop/Tools/`. Text, shape, vector, and frame layers persist through the `D03 T08 §1` contract as `gesso:` elements beside a rendered PNG, paths as `gesso:paths`; every edit is one undoable command with one Serilog Information line.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Gesso's `TextLayer` (`src/Gesso/src/Gesso.Core/Layers/TextLayer.cs`, 118 lines) is a flat single-style model: one font family defaulting to Segoe UI, one size, one color, no runs, no shaping, no paragraphs. Its `ShapeLayer` (`src/Gesso/src/Gesso.Core/Layers/ShapeLayer.cs`, 92 lines) names eight fixed shape kinds ending in `RoundedRectangle` and holds no path geometry of its own. Its vector mask (`src/Gesso/src/Gesso.Core/Masks/VectorMask.cs`, 291 lines) keeps its own `VectorPathSegment` type, which §5 re-bases on the shared geometry so one path type remains. No shaping package is referenced in `Directory.Packages.props` and Stilus has no text folder yet (`src/Stilus/Bezier.Core/Text` is absent); `D02 T10 §1` adds both before this file runs. Stilus's path booleans and SVG reader live today in `src/Stilus/Bezier.Core/Services/PathOperationsService.cs` (351 lines) and `src/Stilus/Bezier.Core/Services/SvgParser.cs` (907 lines), which the Stilus parity sections extend and §5 then moves. Backlog B-018 (text layers) and B-019 (shape layers and vector tools) are promoted into §1 and §7; the integration that lands this file deletes both entries.
<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/TextLayer.cs = 118 -->
<!-- claim: count "_fontFamily = .Segoe UI." src/Gesso/src/Gesso.Core/Layers/TextLayer.cs = 1 -->
<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/ShapeLayer.cs = 92 -->
<!-- claim: count "^    RoundedRectangle$" src/Gesso/src/Gesso.Core/Layers/ShapeLayer.cs = 1 -->
<!-- claim: lines src/Gesso/src/Gesso.Core/Masks/VectorMask.cs = 291 -->
<!-- claim: count "class VectorPathSegment" src/Gesso/src/Gesso.Core/Masks/VectorMask.cs = 1 -->
<!-- claim: count "HarfBuzz" Directory.Packages.props = 0 -->
<!-- claim: absent src/Stilus/Bezier.Core/Text -->
<!-- claim: lines src/Stilus/Bezier.Core/Services/PathOperationsService.cs = 351 -->
<!-- claim: lines src/Stilus/Bezier.Core/Services/SvgParser.cs = 907 -->

## Inputs

- [`standards/gesso.md`](../../standards/gesso.md) -- tiles, fidelity proofs, and the hot-path rules text and path rendering follow
- [`standards/shared.md`](../../standards/shared.md) -- the shared-once rule every move here follows, settings, logging, and one command per edit
- [`docs/parity/gesso-section-design.md`](../../docs/parity/gesso-section-design.md) -- the blueprint for this file; [`docs/parity/gesso-parity.md`](../../docs/parity/gesso-parity.md) -- the catalog rows each section owns
- Unicode 16.0 UAX #9, UAX #14, and UAX #24 (the conformance suites move with the engine); OpenType 1.9.1 (GSUB, GPOS, fvar, STAT, COLR v1, SVG, name IDs 16 and 17); HarfBuzz 10.x `hb-shape` and `hb-view` goldens; W3C SVG 2 path data
- Adobe Photoshop File Formats Specification (text engine data and vector mask blocks, referenced for the later PSD mapping in `D03 T17 §13`); Adobe Illustrator File Format Specification v7 (the paths-only Illustrator 3 subset Photoshop exports); Schneider 1990 (Graphics Gems curve fitting); Microsoft Learn Windows Spell Checking API; TeX hyph-utf8 patterns (licenses per file)
- Inkscape 1.4 and resvg 0.45 as SVG render oracles; GIMP 3.2.6 as the vector layer and text behavior reference and, through `gimp-console-3.2`, the `.ora` fallback oracle
- [`todo/backlog.md`](../backlog.md) -- B-018 (`legacy-gesso-4.8`) is promoted into §1 and B-019 (`legacy-gesso-4.7`) into §7; both entries leave the backlog in the integration commit
- -> XREF: D02 T10 §1 -- the shaping engine §1 moves
- -> XREF: D02 T10 §2 -- the rich-text model and edit session §1 moves
- -> XREF: D02 T10 §3 -- fonts and font filters §2 moves
- -> XREF: D02 T10 §16 -- the font substitution service §2 moves (split out of D02 T10 §3 on 2026-09-27)
- -> XREF: D02 T10 §4 -- character formatting and optical kerning §2 moves
- -> XREF: D02 T10 §5 -- OpenType features, glyphs, and variable fonts §2 moves
- -> XREF: D02 T10 §6 -- the composers and hyphenation §3 moves
- -> XREF: D02 T10 §7 -- lists and protrusion §3 moves
- -> XREF: D02 T10 §8 -- text frames §3 moves
- -> XREF: D02 T10 §9 -- path text layout §4 moves
- -> XREF: D02 T10 §10 -- the CJK composer §4 moves
- -> XREF: D02 T10 §11 -- text search §4 moves
- -> XREF: D02 T10 §12 -- character and paragraph styles §4 moves
- -> XREF: D02 T10 §13 -- spell checking §4 moves
- -> XREF: D02 T08 §1 -- pen math §6 moves
- -> XREF: D02 T08 §4 -- live-shape generators §7 moves
- -> XREF: D02 T08 §6 -- node operations §6 moves
- -> XREF: D02 T08 §7 -- curve actions §6 moves
- -> XREF: D02 T08 §10 -- path geometry and booleans §5 moves
- -> XREF: D02 T14 §1 -- the SVG export options §8 moves and shares
- -> XREF: D02 T14 §4 -- Stilus's legacy AI reader, the read-back oracle for §5's Illustrator paths
- -> XREF: D01 T05 §5 -- brand kit type styles shown in §4's styles panels
- -> XREF: D03 T08 §1 -- the native-format contract every layer kind here registers with
- -> XREF: D03 T08 §4 -- snapping for the pen and shape tools
- -> XREF: D03 T09 §1 -- text, shape, vector, and frame layer kinds
- -> XREF: D03 T09 §4 -- vector masks re-based on §5's geometry
- -> XREF: D03 T09 §9 -- frame content as smart objects
- -> XREF: D03 T10 §1 -- path to and from selection, and type mask output
- -> XREF: D03 T10 §5 -- the intelligent scissors engine for the magnetic pen and content-aware tracing
- -> XREF: D03 T12 §8 -- the fill and stroke path engine
- -> XREF: D03 T12 §9 -- gradient paint for shapes and text outline
- -> XREF: D03 T12 §10 -- pattern paint for shapes and text outline
- -> XREF: D03 T13 §5 -- transform handles for paths and anchors
- -> XREF: D03 T13 §6 -- warp envelope math for warp text
- -> XREF: D03 T17 §1 -- the format registry that lists §8's SVG writer
- -> XREF: D03 T17 §3 -- PSD text, shape, and vector mask read into §1, §5, and §7
- -> XREF: D03 T17 §13 -- PSD text, shape, and vector mask write from §1, §5, and §7
- -> XREF: D03 T17 §4 -- XCF text and vector layers map onto §1 and §7
- -> XREF: D03 T17 §7 -- moves only the SVG renderer, since §5 moves the reader
- -> XREF: D03 T17 §11 -- clipping paths written into JPEG and TIFF from §5's flag
- -> XREF: D03 T19 §11 -- match font on §2's font list
- -> XREF: D03 T20 §4 -- type preferences surface the `Gesso.Type.*` keys
- -> XREF: D03 T18 §7 -- contact sheet and PDF Presentation captions set in §1's text layers
- -> XREF: D01 T06 §2 -- the shape blur kernel §7's rasterized custom shapes feed
- -> XREF: D01 T06 §9 -- the flame renderer §5's active path feeds
- -> XREF: D03 T08 §5 -- the scale marker label §1 turns into a text layer
- -> XREF: D03 T08 §8 -- Paste without Formatting, which §1 enables
- -> XREF: D03 T10 §9 -- the Selection to Path and Path to Selection commands §5 enables
- -> XREF: D03 T12 §11 -- symmetry from a path, which §5 enables
- -> XREF: D03 T13 §11 -- the Path transform target §5 enables
- -> XREF: D03 T14 §9 -- the Slide label and Filmstrip numbering fields §1 enables
- -> XREF: D04 T11 §8 -- the Albumen batch tools cites §1: the shared text engine D04 T11 §8 shapes overlay text with
- -> XREF: D04 T12 §1 -- Albumen parity output cites §1: the suite text engine for slideshow and book text
- -> XREF: D04 T13 §8 -- Albumen parity formats cites §1: the shared text engine D04 T13 §8 renders font sample sheets and D04 T13 §4 renders text files through
- -> XREF: D03 T22 §6 -- Gesso variables cites §1: text layers that text replacement variables bind to

## Outcome

- Text layers are live stories of styled runs in any script, shaped by the one suite text engine in `src/Isotone.Core/Text/`, edited on the canvas with IME support, and saved as `gesso:text` beside a pixel fallback that GIMP and Krita open.
- The Character, Paragraph, Glyphs, and styles panels are the moved `Isotone.UI/Text/` panels bound through an adapter, with OpenType, variable, and color fonts, composers, hyphenation, lists, spelling, find and replace, type on a path, and live warp text.
- Documents keep a work path and saved paths in a Paths panel, with fill, stroke, selection conversion, booleans, clipping paths, and SVG and Illustrator path exchange, on one path type in `src/Isotone.Core/Vector/`.
- The pen family, anchor tools, and path and direct selection edit paths on node math shared with Stilus.
- Shape, vector, and frame layers stay live and resolution-independent, persist as `gesso:shape`, `gesso:vector`, and `gesso:frame`, and export as SVG with one element per vector layer.
- A grep finds one `TextShaper`, one `TextLayoutEngine`, one path type, and one set of type panels in `src/`.

**Adjacency:** list=applicable @ D03 T16 §5; document=not-applicable (this file prints nothing; print is D03 T18 §6); settings=applicable @ D03 T16 §2; reporting=applicable @ D03 T16 §4; notifications=applicable @ D03 T16 §8; permissions=applicable @ D03 T16 §7; audit=applicable @ D03 T16 §1; exchange=applicable @ D03 T16 §5; reverse=applicable @ D03 T16 §1

**Adjacency rationale:** The lists are the Paths panel (§5), the Shapes panel (§7), the Glyphs panel search and the font list filters and favorites (§2), and the character and paragraph styles panels (§4). Settings are the `Gesso.Type.*`, `Gesso.Paths.*`, and `Gesso.Shapes.*` keys, each with a default and a named consumer, surfaced in the preference pages of `D03 T20 §4`. Reporting is the missing-fonts report and the spelling results of §4. Notifications are the font list refresh progress (§2) and the SVG export completion (§8). Restricted-embedding fonts, unreadable CSH or SVG files, and locked layers are refused by name (§7 and §8). Every command is one history entry with one Serilog Information line, starting with §1. Exchange is SVG path import and export and Illustrator path export (§5), CSH import (§7), and SVG export with Copy SVG and Copy CSS (§8). Every command is undoable, rasterize included (§1, §7).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
| 1 |   §1    | Text layers on the shared text engine | D02 T10 §1, D03 T09 §1 |  [ ]   |
| 2 |   §9    | Type tools and on-canvas text editing | §1 |  [ ]   |
| 3 |   §5    | Paths, the Paths panel, and path geometry in Isotone.Core | D02 T08 §10, D03 T10 §1 |  [ ]   |
| 4 |   §10   | Path exchange and path commands: SVG, Illustrator, clipping paths, booleans, and align | §5 |  [ ]   |
| 5 |   §2    | Character formatting, OpenType, glyphs, and fonts | §1, D02 T10 §16 |  [ ]   |
| 6 |   §3    | Paragraph formatting and text frames | §1 |  [ ]   |
| 7 |   §4    | Type styles and text commands | §2, §3, §5, §9 |  [ ]   |
| 8 |   §6    | Pen and path editing tools | §5 |  [ ]   |
| 9 |   §7    | Shape layers and shape tools | §5, D03 T09 §4 |  [ ]   |
| 10 |   §11   | Custom shapes, vector layers, and the Gfig job | §7, §6 |  [ ]   |
| 11 |   §8    | Frames and vector output | §7, §11 |  [ ]   |

---

## 1. Text Layers on the Shared Text Engine

Gesso's text layer today is one font, one size, and one color drawn as a bitmap, which cannot join Arabic, reorder Devanagari, or hold two styles in one line. Stilus already built the suite's HarfBuzz engine and rich-text model (`D02 T10 §1`, `D02 T10 §2`), so Gesso becomes its second consumer and the engine moves into `Isotone.Core/Text/` in this section instead of being copied. Text layers become live stories of runs and paragraphs (point or paragraph, horizontal or vertical) and persist as `gesso:text` beside a rendered PNG so other OpenRaster readers still see pixels; the type tools, the mask tools, and on-canvas editing that create and edit them are §9, split out on 2026-09-27 so each half stays reviewable in one pass. This promotes backlog B-018. Catalog: IP-1582, IP-1590, IP-1591 (3 features: the type layer, rasterize type, and the world-ready text engine option). -> SOURCE: legacy-gesso-4.8

**Fidelity:** Gesso text layers and Rasterize Type -- docs/design/components/ (LayersRow, Panel, Canvas, Menu), per standards/design-contract.md; goldens under docs/captures/golden/gesso/type/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/LayersRow/README.md, docs/design/components/Panel/README.md, docs/design/components/Canvas/README.md, docs/design/components/Menu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer's text stays live in Latin, Arabic, Devanagari, or CJK, renders exactly as Stilus renders the same story, and stays editable until rasterizing. Consumer: the layer renderer, the `.gesso` save, §9's editing tools, and the later PSD and XCF mappings.
**Treatment:** text layers in the Layers panel with the T badge, the Type, Rasterize Type command, and the text engine choice in the type options. Cheaper substitute that fails the checkpoint: a text layer that stores only a bitmap and a string.
**Chrome:** consume the moved engine, the tool options strip of `D03 T03 §4`, the `Isotone.UI` dialog styles, and the suite history. Do not add a second shaper or text model.

**Requires:** display-session -- typing into a layer, IME composition, and the captures need an interactive desktop

- [ ] Move first: `src/Stilus/Isotone.Stilus.Core/Text/` Unicode, Shaping, Fonts (`FontCatalog`, the `FontFaceInfo` cache, `FontFallbackChain`), and Layout (`TextLayoutEngine`) into `src/Isotone.Core/Text/`, with their tests into `tests/Isotone.Core.Tests/Text/`, and repoint Stilus. Done when: Stilus's text tests pass unchanged from the new location and `grep -rn "class TextShaper\|class TextLayoutEngine" src` prints one path each, under `src/Isotone.Core/`.
- [ ] Move the story model and `TextEditSession` of `D02 T10 §2` into `src/Isotone.Core/Text/Model/`, repointing Stilus. Done when: `grep -rn "class TextStory\|class TextEditSession" src` prints one path each, under `src/Isotone.Core/`.
- [ ] Move `TextInputBridge` (the IME and caret bridge) into `src/Isotone.UI/Text/`, repointing Stilus. Done when: one definition remains and Stilus's IME driven check still shows the composition underline.
- [ ] Move the `HarfBuzzSharp` and `SkiaSharp.HarfBuzz` references from `Isotone.Stilus.Core` to `src/Isotone.Core/Isotone.Core.csproj` and update the `docs/dev/decisions.md` row to say the move trigger fired with this section's ref. Done when: `dotnet list src/Isotone.Core package` shows both and the Stilus core project no longer references them directly.
- [ ] Move the font cache to `%LOCALAPPDATA%\Rizonesoft\Isotone\FontCache\`, migrating an existing Stilus cache on first run. Done when: a test with a seeded old cache finds it at the new path and the old folder is removed.
- [ ] Rewrite `src/Gesso/Isotone.Gesso.Core/Layers/TextLayer.cs` over `Isotone.Core.Text.Model.TextStory` with `TextKind` Point or Paragraph (box size, GIMP dynamic or fixed box), transform, and anti-aliasing (IP-1582, IP-1584). Done when: `TextLayerTests` create both kinds and a two-run story keeps both runs' attributes.
- [ ] Add orientation to `TextLayer`: horizontal or vertical, mixed or upright, and vertical Roman alignment (IP-1585). Done when: a vertical CJK fixture renders within 1/255 of the Stilus render of the same story.
- [ ] Re-render a text layer's tiles from the layout only when the story or transform changes, caching the shaped layout per story version. Done when: a test asserts moving another layer re-shapes nothing and editing one character re-shapes only that layer.
- [ ] Register `gesso:text` (the story as XML runs with a schema version) beside the rendered PNG with the `D03 T08 §1` contract. Done when: `TextLayerFormatTests` save a document with Arabic and Latin runs, reopen it, and the story is equal run by run.
- [ ] Add Rasterize Type (IP-1590) as one undo step "Rasterize Type" that replaces the text layer with a pixel layer of the same render. Done when: a test rasterizes, compares pixels within 1/255 of the live render, and undo restores the live layer.
- [ ] Add `Gesso.Type.TextEngine` (East Asian or World-Ready, IP-1591) choosing which panel feature sets show, while one engine shapes every script. Done when: a test switches the setting and the Devanagari fixture still shapes identically.
- [ ] Enable the controls earlier sections deferred to text layers, removing each tooltip: Paste without Formatting (`D03 T08 §8`), the scale marker's text label (`D03 T08 §5`), text bases for fill text with an image (`D03 T09 §4`), and the Slide label and Filmstrip numbering fields (`D03 T14 §9`). Done when: each owning section's disabled-state test is updated to assert the enabled control and passes.
- [ ] Name the history steps "Add Text Layer" and "Edit Text", and log one Information line per commit (`Text layer {Id} committed ({Chars} chars, {Runs} runs)`) as the audit trail. Done when: a Serilog test logger asserts the line and the history shows both names.
- [ ] Add `tests/Isotone.Gesso.Core.Tests/Text/TextEditBudgetTests.cs`: a keystroke in a 2,000-character paragraph at 300 ppi re-lays out and re-renders its tiles within 16 ms. Done when: the test prints the measured time and passes.
- [ ] Commit fixtures under `tests/fixtures/gesso/text/` (Arabic, Devanagari, vertical CJK, and Latin stories with the Stilus renders as goldens) with `reference.txt`. Done when: `TextLayerRenderTests` render each within 1/255 of its Stilus golden.
- [ ] Add a GIMP fallback check: `gimp-console-3.2` opens a saved `.gesso` renamed to `.ora` and its composite matches Gesso's within 1/255 (GIMP version recorded; skipped with a reason where GIMP is absent). Done when: the test result is quoted with GIMP's version.
- [ ] Write `docs/user/gesso/type.md` covering text layers, the text engine choice, and rasterize; §9 adds the tools and editing. Done when: the page documents every control on this surface.
- [ ] Commit: `"gesso: live text layers on the HarfBuzz engine moved to Isotone.Core"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Core.Tests.Text|FullyQualifiedName~Isotone.Gesso.Core.Tests.Text"` exits 0 with the moved `ShaperGoldenTests` and conformance suites, `TextLayerRenderTests` (Arabic and Devanagari within 1/255 of the Stilus render), `TextLayerFormatTests`, and `TextEditBudgetTests` reporting; the `gimp-console-3.2` fallback comparison is quoted within 1/255. Cheaper substitute that fails: a Gesso-local `DrawText` path, which the one-definition grep and the Arabic golden catch.

## 2. Character Formatting, OpenType, Glyphs, and Fonts

Character formatting is where a text tool earns trust: every attribute, every OpenType feature, variable axes, color fonts, and a font picker that finds the right face. Stilus built these as panels and services (`D02 T10 §3` to `D02 T10 §5`), so they move into `Isotone.Core/Text/` and `Isotone.UI/Text/` here and each app binds them through an `ITextFormattingTarget` adapter; Gesso gets no fork of any panel. Catalog: IP-1592 to IP-1610 (19 features: the Character panel with toggles and reset, true face grouping, changing the font on several layers, leading, kerning, and tracking, scale and baseline shift, float-precision color, faux styles and case, anti-aliasing and hinting, fractional widths and no break, language per run, the font menu filters and similar fonts, the Fonts dialog, OpenType features, variable axes, color fonts and emoji, the Glyphs panel, glyph protection, the non-destructive text outline, and the Character and Glyphs panels together).

**Fidelity:** Gesso Character and Glyphs panels and font menus -- docs/design/components/ (Panel, ComboBox, NumberBox, Slider, ToggleSwitch, Swatches, ListTree, TextBox, Menu), per standards/design-contract.md; goldens under docs/captures/golden/gesso/character-panel/, docs/captures/golden/gesso/glyphs-panel/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Slider/README.md, docs/design/components/ToggleSwitch/README.md, docs/design/components/Swatches/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/Menu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer sets every character attribute, OpenType feature, and font on one or many text layers. Consumer: the text layer's story and its render.
**Treatment:** the Character panel with toggles and reset, the font picker with filters, favorites, similar fonts, and preview size, a Fonts dialog in grid and list, the OpenType submenu and on-canvas alternates, variable axis sliders, and a Glyphs panel. Cheaper substitute that fails the checkpoint: a font combo box with bold and italic toggles only.
**Chrome:** consume the moved `CharacterPanel`, `OpenTypePanel`, `GlyphsPanel`, and `FontPicker` from `Isotone.UI/Text/`. Do not fork them.

**Requires:** display-session -- the panels and on-canvas alternates need an interactive desktop

- [ ] Move first: `FontFilter` (`D02 T10 §3`) and `FontSubstitutionService` (`D02 T10 §16`, split out of `D02 T10 §3` on 2026-09-27) into `src/Isotone.Core/Text/Fonts/`, repointing Stilus. Done when: `grep -rn "class FontSubstitutionService" src` prints one path, under `src/Isotone.Core/`.
- [ ] Move `OpticalKerner` and `FontFeatureSet` (`D02 T10 §4`, `D02 T10 §5`) and `GlyphSnapProvider` into `src/Isotone.Core/Text/`, repointing Stilus. Done when: one definition of each remains and Stilus's formatting tests pass.
- [ ] Move the view models and XAML of `CharacterPanel`, `OpenTypePanel`, `GlyphsPanel`, and `FontPicker` into `src/Isotone.UI/Text/`, bound through an `ITextFormattingTarget` adapter each app implements, repointing Stilus. Done when: one definition of each remains and Stilus's driven Character panel check still passes.
- [ ] Add `src/Gesso/Isotone.Gesso.Desktop/Text/GessoTextFormattingTarget.cs`, applying panel changes to the selected runs of the edited layer or to whole selected text layers. Done when: `GessoTextFormattingTargetTests` set size on a selection of runs and on two whole layers.
- [ ] Wire the Character panel core (IP-1592, IP-1610): family, style, size, panel toggles, and reset. Done when: a driven run changes each on a fixture layer and reset restores the defaults.
- [ ] Add leading, kerning (metrics, optical through `OpticalKerner`, manual), and tracking with GIMP's line and letter spacing mapped onto them (IP-1595). Done when: `CharacterFormattingTests` render each on the Latin fixture within 1/255 of goldens.
- [ ] Add vertical and horizontal scale and baseline shift (IP-1596). Done when: `CharacterFormattingTests` render each within 1/255 of goldens.
- [ ] Add float-precision text color with live preview through the color picker (IP-1597). Done when: a 16-bit document's text color round-trips a 0.5 channel value exactly through `gesso:text`.
- [ ] Add faux bold and italic, all caps, small caps, superscript, subscript, underline, and strikethrough (IP-1598), applying faux styles only when the family lacks the face. Done when: a test asserts a family with a true bold uses it and a family without one uses faux bold.
- [ ] Add anti-aliasing None, Sharp, Crisp, Strong, and Smooth and hinting (IP-1599) mapped to `SKFontEdging` and `SKFontHinting`. Done when: each mode renders a distinct golden within 1/255.
- [ ] Add fractional widths, system layout, and no break (IP-1600). Done when: a test asserts no-break text never breaks at a width that would otherwise break it.
- [ ] Add the language dictionary per run (IP-1601), read by hyphenation (§3) and spelling (§4). Done when: a run's language round-trips through `gesso:text`.
- [ ] Add true face grouping (IP-1593) by typographic family and subfamily (name IDs 16 and 17). Done when: `FontGroupingTests` group committed OFL families into their true faces.
- [ ] Apply a change on several selected text layers as one compound undo step (IP-1594). Done when: a test changes the font on three layers and one undo restores all three.
- [ ] Add the font menu filters (classification from PANOSE and OS/2), favorites, similar fonts by a local metrics distance (x-height, cap height, stem weight, width class; no cloud), and preview size (IP-1602). Done when: `SimilarFontTests` rank a committed sans family above a committed serif family for a sans query.
- [ ] Add the Fonts dialog (IP-1603): grid and list views, search, Refresh Font List with status-strip progress, and fast loading from the moved cache. Done when: a driven refresh shows progress and a second launch lists fonts from the cache without rescanning, measured and quoted.
- [ ] Add OpenType feature buttons offered per font (liga, dlig, swsh, calt, ordn, frac, titl, ss01 to ss20, cv01 to cv99), the OpenType submenu, and on-canvas alternates for the selected glyph (IP-1604). Done when: a driven run swaps a glyph for an alternate on canvas and the capture shows the alternates popup.
- [ ] Add variable fonts (IP-1605): fvar axis sliders and STAT named instances. Done when: `VariableFontTests` render three axis settings of an OFL variable font within 1/255 of `hb-view` (HarfBuzz 10) output.
- [ ] Add color fonts and emoji (IP-1606): COLR v0 and v1, OpenType SVG, sbix, and CBDT through Skia, with ZWJ sequences composed by the shaper. Done when: a family emoji ZWJ sequence renders as one glyph within 1/255 of its golden.
- [ ] Wire the Glyphs panel (IP-1607): filters, recent glyphs, search by name or code point, and zoom. Done when: a driven search for U+00E9 inserts it at the caret.
- [ ] Add glyph protection (IP-1608) from the moved missing-glyph logic, controlled by `Gesso.Type.GlyphProtection` (default true). Done when: a test types a Cyrillic letter in a Latin-only font and it falls back to a font that has it only when protection is on.
- [ ] Add the non-destructive text outline (IP-1609): fill, outline, or both, direction inside, center, or outside, color or pattern, width, caps, joins, miter, and dashes, stored in `gesso:text` with the `StrokeStyle` record in `src/Isotone.Core/Vector/StrokeStyle.cs` that §7 shares. Done when: an outlined layer reopens live and renders within 1/255 of its golden.
- [ ] Add the settings `Gesso.Type.DefaultAntiAlias`, `Gesso.Type.FontPreviewSize`, and `Gesso.Type.Units`, each with a default and a named consumer (the type tools, the font picker, and the Character panel). Done when: a test reads each default through `ISettingsStore` and a change is picked up without a restart.
- [ ] Commit OFL fonts and goldens under `tests/fixtures/gesso/fonts/` with each license and `reference.txt` naming HarfBuzz 10 `hb-view`. Done when: every font carries its license file.
- [ ] Commit captures under `docs/captures/gesso/character-panel/` and `docs/captures/gesso/glyphs-panel/`, and write `docs/user/gesso/character.md`. Done when: every control in the Treatment appears in a capture and the page documents it.
- [ ] Commit: `"gesso: character formatting, OpenType, glyphs, and fonts on the shared type panels"`

**Test checkpoint:** Unit test with goldens and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CharacterFormattingTests|FullyQualifiedName~FontGroupingTests|FullyQualifiedName~VariableFontTests|FullyQualifiedName~SimilarFontTests"` exits 0, with each attribute on the Latin fixture within 1/255 of its golden and the variable font within 1/255 of `hb-view` output; the captures under `docs/captures/gesso/character-panel/` and `glyphs-panel/` are committed. Cheaper substitute that fails: faux bold and italic for every family, which the true-face test catches.

## 3. Paragraph Formatting and Text Frames

Paragraph text in Gesso must lay out like a layout tool: alignment, indents, spacing, hyphenation, justification with the every-line composer, hanging punctuation, lists, and Affinity's frame text with vertical alignment. The composers and paragraph model already exist in Stilus (`D02 T10 §6` to `D02 T10 §8`), so they move into `Isotone.Core/Text/` and the panel into `Isotone.UI/Text/` here. Catalog: IP-1611 to IP-1618 (8 features: alignment and justification with reset, indents and spacing, hyphenation, justification settings and the composers, Roman hanging punctuation, bulleted and numbered lists, the frame text tool with vertical alignment, and the Paragraph panel).

**Fidelity:** Gesso Paragraph panel and text frames -- docs/design/components/ (Panel, NumberBox, ComboBox, TextBox, Canvas, ToolRail), per standards/design-contract.md; goldens under docs/captures/golden/gesso/paragraph-panel/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/TextBox/README.md, docs/design/components/Canvas/README.md, docs/design/components/ToolRail/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer sets paragraph layout on text layers as in a layout tool. Consumer: the text layer's story and its line breaking.
**Treatment:** the moved `ParagraphPanel` with hyphenation and justification dialogs, bullets and numbering, and the frame text tool. Cheaper substitute that fails the checkpoint: left, center, and right buttons only.
**Chrome:** consume the `Isotone.UI/Text/` panels, the §2 formatting adapter, and the suite history. Do not add a second composer.

**Requires:** display-session -- the panel and the frame text tool need an interactive desktop

- [ ] Move first: `Hyphenator` with its TeX pattern files (`D02 T10 §6`) into `src/Isotone.Core/Text/Hyphenation/`, keeping each pattern's license file beside it, and repoint Stilus. Done when: `grep -rn "class Hyphenator" src` prints one path, under `src/Isotone.Core/`.
- [ ] Move `Composer`, `ProtrusionTable`, and `ListAttributes` (`D02 T10 §7`) and `TextFrame` (`D02 T10 §8`) into `src/Isotone.Core/Text/Layout/`, repointing Stilus. Done when: one definition of each remains and Stilus's composer tests pass from `tests/Isotone.Core.Tests/Text/`.
- [ ] Move `ParagraphPanel.xaml` and its view model into `src/Isotone.UI/Text/`, bound through `ITextFormattingTarget`. Done when: one definition remains and Stilus's paragraph panel still drives.
- [ ] Wire alignment (left, center, right, justify last left, center, or right, justify all) and reset (IP-1611, IP-1618). Done when: a driven run applies each and the capture shows the panel.
- [ ] Add left, right, and first-line indents and space before and after (IP-1612). Done when: a paragraph render matches its golden within 1/255 for each.
- [ ] Add hyphenation (IP-1613): on or off, words longer than, after first, before last, hyphen limit, zone, and capitalized words, per the run's language from the moved patterns, in a Hyphenation dialog. Done when: `HyphenationTests` pass the pattern fixtures for English and German.
- [ ] Add justification settings (IP-1614): word, letter, and glyph spacing minimum, desired, and maximum; auto leading; and the single-line, every-line (Knuth and Plass), and world-ready composers, in a Justification dialog. Done when: `ComposerTests` break the committed paragraph at the same points as the Stilus goldens for both composers.
- [ ] Add Roman hanging punctuation (IP-1615) through `ProtrusionTable`. Done when: a test asserts a line-final period protrudes past the text box edge by its table amount.
- [ ] Add bulleted and numbered lists with nesting (IP-1616) through `ListAttributes`. Done when: a nested list renders its markers within 1/255 of the golden.
- [ ] Add the Frame Text tool (IP-1617) in `src/Gesso/Isotone.Gesso.Desktop/Tools/Type/FrameTextTool.cs`: Affinity frame text as paragraph text with vertical alignment top, center, bottom, and justify, sharing the list attributes. Done when: a driven run draws a frame and vertical centering places the text block's center within 0.5 px of the frame's.
- [ ] Serialize every paragraph attribute inside the `gesso:text` paragraphs. Done when: `TextLayerFormatTests.ParagraphRoundTrip` saves and reopens every attribute equal.
- [ ] Commit paragraph fixtures and the Stilus goldens under `tests/fixtures/gesso/paragraph/` with `reference.txt`. Done when: every golden carries its note.
- [ ] Commit captures under `docs/captures/gesso/paragraph-panel/` (the panel, both dialogs, the frame text tool) and write `docs/user/gesso/paragraph.md`. Done when: every control appears in a capture and the page documents it.
- [ ] Commit: `"gesso: paragraph formatting, composers, lists, and frame text"`

**Test checkpoint:** Unit test with goldens: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ComposerTests|FullyQualifiedName~HyphenationTests|FullyQualifiedName~TextLayerFormatTests"` exits 0, the every-line composer breaks the committed paragraph at the Stilus golden's points, and paragraph renders match goldens within 1/255; captures committed under `docs/captures/gesso/paragraph-panel/`. Cheaper substitute that fails: greedy breaking under the every-line composer, which the Knuth and Plass break test catches.

## 4. Type Styles and Text Commands

Consistency across many text layers needs styles, find and replace, and spelling, and expressive type needs type on a path and warp text. The services and panels come from Stilus (`D02 T10 §9` to `D02 T10 §13`) and move here; warp text reuses the envelope math of `D03 T13 §6`, so warped text stays live and editable. Loading styles from a PSD waits for `D03 T17 §3`, which reads PSD text, and says so by name until then. Catalog: IP-1619 to IP-1634, IP-2371 (17 features: check spelling, find and replace, type on a path and text to path, point and paragraph conversion, placeholder text, character and paragraph styles, find and replace and spelling as their Affinity and GIMP rows, missing fonts, East Asian options, right-to-left options, warp text, dynamic text presets, the styles panels, the additional spelling dictionary folder, and inserting metadata fields as text).

**Fidelity:** Gesso type styles panels, text commands, and Warp Text -- docs/design/components/ (Panel, ListTree, Dialog, ComboBox, Slider, NumberBox), per standards/design-contract.md; goldens under docs/captures/golden/gesso/type-styles/, docs/captures/golden/gesso/warp-text/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer keeps type consistent across layers and bends it onto paths and shapes. Consumer: every text layer's story.
**Treatment:** character and paragraph styles panels, Find and Replace and Check Spelling dialogs, the Warp Text dialog, the missing fonts dialog, and type-on-path handles. Cheaper substitute that fails the checkpoint: warp by rasterizing the text.
**Chrome:** consume the moved panels and services, §5's paths, and the suite history. Do not add a second spell checker.

**Requires:** display-session -- the dialogs, path handles, and captures need an interactive desktop

- [ ] Move first: `TextSearchService` (`D02 T10 §11`) and the `Text/Styles/` model (`D02 T10 §12`) into `src/Isotone.Core/Text/`, repointing Stilus. Done when: one definition of each remains and Stilus's search and style tests pass from `tests/Isotone.Core.Tests/Text/`.
- [ ] Move `ISpellCheckService` into `src/Isotone.Core/Text/Spelling/` and `WindowsSpellCheckService` into `src/Isotone.UI/Text/` (`D02 T10 §13`), repointing Stilus. Done when: `grep -rn "class WindowsSpellCheckService" src` prints one path, under `src/Isotone.UI/`.
- [ ] Move `JapaneseComposer` with its presets (`D02 T10 §10`) and `PathTextLayout` (`D02 T10 §9`) into `src/Isotone.Core/Text/`, repointing Stilus. Done when: one definition of each remains.
- [ ] Add the Check Spelling dialog (IP-1619, IP-1626) over every text layer through the Windows Spell Checking API per run language; a missing language dictionary is refused by name. Done when: `SpellCheckTests` flag the misspelling in the fixture, skipping with the language name where the Windows dictionary is absent.
- [ ] Add user word lists from `Gesso.Type.UserDictionaryFolder` (IP-1634). Done when: a word added to a list file in that folder is no longer flagged.
- [ ] Add Find and Replace (IP-1620, IP-1625) across every text layer with case and whole-word options, as one compound undo step. Done when: `FindReplaceTests` replace across three layers and one undo restores all three.
- [ ] Add type on a path (IP-1621, IP-1631): on an open path or inside a closed shape (§5 paths, §7 shapes), with flip, start and end markers, and edit path, stored live in `gesso:text` with its path reference. Done when: `PathTextTests` render the committed story on a path within 1/255 of the Stilus render.
- [ ] Add the Text to Path command (IP-1621) that converts the laid-out glyphs on a path to a work path through §5. Done when: a test converts and the work path's figure count equals the glyph outline count.
- [ ] Add Convert to Point Text and Convert to Paragraph Text (IP-1622). Done when: a round trip keeps every run's attributes and the text.
- [ ] Add placeholder text (IP-1623): `Gesso.Type.FillNewWithPlaceholder` (default false) and Paste Lorem Ipsum. Done when: with the setting on, a new text layer starts with placeholder text.
- [ ] Add the character and paragraph styles panels (IP-1624, IP-1633) with style options, redefine, clear override, default styles, and load from another `.gesso`; Load from PSD is disabled with a tooltip naming `D03 T17 §3`, which enables it. Done when: a test applies a style to two layers, redefines it, and both update, and `python scripts/todo-graph.py resolve 'D03 T17 §3'` resolves.
- [ ] Show brand kit type styles (`D01 T05 §5`) as a read-only group in the styles panels. Done when: a test with a fixture brand kit lists its styles and refuses an edit to them by name.
- [ ] Add the missing fonts report and replacement (IP-1627) through `FontSubstitutionService` with installed fonts only, updating every text layer; no Adobe Fonts activation. Done when: opening the missing-font fixture shows the report listing the family, and replacement updates all its layers in one undo step.
- [ ] Add East Asian options (IP-1628): tsume, kinsoku hard and soft, and mojikumi through `JapaneseComposer`. Done when: a kinsoku fixture never starts a line with a prohibited character.
- [ ] Add right-to-left and Middle Eastern options (IP-1629): paragraph direction, digit shapes (Arabic, Hindi, Farsi), diacritic position, and kashida. Done when: an Arabic paragraph with Hindi digits renders within 1/255 of its golden.
- [ ] Add Warp Text (IP-1630): arc, arc lower, arc upper, arch, bulge, shell lower and upper, flag, wave, fish, rise, fisheye, inflate, squeeze, and twist with bend and horizontal and vertical distortion, on the `D03 T13 §6` envelope math applied to the glyph outlines and stored live in `gesso:text`. Done when: `WarpTextTests` assert the text stays editable after warp and the render matches the envelope applied to the outlines within 1/255.
- [ ] Add dynamic text presets (IP-1632): path-text presets with spacing, position, direction, dynamic fit, and on-canvas endpoint handles. Done when: a test applies a preset and dragging an endpoint handle refits the text.
- [ ] Add Type, Insert Metadata Field (IP-2371; ACDSee Edit mode, Albumen row LP-1333): inserts a live field token (file name, dimensions, dates, camera, lens, exposure, author, copyright, caption, keywords) at the caret of a text layer, resolved from the document's metadata and file properties and re-resolved on save or on the Refresh Fields command; the file properties work now and the EXIF, IPTC, and XMP fields fill as `D03 T17 §10` extends the metadata reader, each field listed disabled with the tooltip "Planned: D03 T17 §10" until then. Done when: `MetadataFieldTests` insert the file-name and dimensions tokens, rename the document, refresh, and assert the new name, and assert the EXIF fields' tooltip resolves. Cheaper substitute: pasting the values as static text.
- [ ] Commit fixtures under `tests/fixtures/gesso/text-commands/` (misspelling, missing font, kinsoku, Arabic, path text, warp) with goldens and `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/gesso/type-styles/` and `docs/captures/gesso/warp-text/` and write `docs/user/gesso/type-commands.md`. Done when: every dialog in the Treatment appears in a capture and the page documents it.
- [ ] Commit: `"gesso: type styles, spelling, find and replace, type on a path, and warp text"`

**Test checkpoint:** Unit test with goldens: `dotnet test Isotone.slnx --filter "FullyQualifiedName~FindReplaceTests|FullyQualifiedName~SpellCheckTests|FullyQualifiedName~PathTextTests|FullyQualifiedName~WarpTextTests"` exits 0 (spelling cases skip naming the language where the dictionary is absent), with path text within 1/255 of the Stilus render and warp text still editable and within 1/255 of the envelope render; captures committed. Cheaper substitute that fails: warping rasterized text, which the still-editable assertion catches.

## 5. Paths, the Paths Panel, and Path Geometry in Isotone.Core

Retouchers keep precise outlines as paths and reuse them as selections, strokes, fills, and clipping paths. Stilus owns the suite's path model and booleans (`D02 T08 §10`) and its SVG document reader, so both move into `Isotone.Core/Vector/` here as Gesso becomes their second consumer, and Gesso's own `VectorPathSegment` is re-based on the shared geometry so one path type remains. The SVG reader moves in this phase rather than with `D03 T17 §7` because SVG path import needs it now; `D03 T17 §7` then moves only the renderer. Path exchange (SVG import and export, Illustrator export, the export clipping path) and path editing commands (merge, copy and paste, path operations, align) are §10, split out on 2026-09-27 so each half stays reviewable in one pass. Catalog: IP-1637, IP-1641 to IP-1648, and IP-1655 (10 features: show target path, the Paths panel with its options, path management, visibility and locks and color tags, fill path, stroke path, path to selection, selection to path, clipping paths with flatness, and the Paths panel itself).

**Fidelity:** Gesso Paths panel -- docs/design/components/ (Panel, LayersRow, ListTree, Menu, ContextMenu, Dialog, TextBox), per standards/design-contract.md; goldens under docs/captures/golden/gesso/paths-panel/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/LayersRow/README.md, docs/design/components/ListTree/README.md, docs/design/components/Menu/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a retoucher can keep, name, and reuse precise outlines as selections, strokes, fills, and clipping paths. Consumer: selections, the fill and stroke engine, and the JPEG and TIFF writers.
**Treatment:** a Paths panel (work path in italics, thumbnails, rename in place, multi-select, color tags, lock, visibility, panel options) merging GIMP's Paths dialog, with context and panel menus for every command. Cheaper substitute that fails the checkpoint: paths kept only as vector masks.
**Chrome:** consume the dock, the icon catalog, `D03 T10 §1` selections, the `D03 T12 §8` fill and stroke engine, and the suite history. Do not add a second path type.

**Requires:** display-session -- the Paths panel drive and captures need an interactive desktop

- [ ] Move first: the path model, `PlanarFaces`, and the boolean service of `D02 T08 §10` (with the geometry parts of `PathOperationsService`) into `src/Isotone.Core/Vector/` as `PathGeometry`, `PathFigure`, cubic `BezierSegment` in double precision, `PathBooleans`, and `PlanarFaces`, with tests into `tests/Isotone.Core.Tests/Vector/`, repointing Stilus. Done when: the moved `PathBooleansTests` pass from the new location and Stilus's pathfinder tests pass.
- [ ] Add `src/Isotone.Core/Vector/SvgPathData.cs` (parse and format SVG 2 path data) beside the moved geometry, or move Stilus's parser if it is already separate, leaving one. Done when: `SvgPathDataTests` round-trip the W3C path-data examples within 1e-9.
- [ ] Re-base Gesso's `VectorMask` and `VectorPathSegment` on `PathGeometry`, deleting `VectorPathSegment`. Done when: `grep -rn "class VectorPathSegment" src` prints nothing and Gesso's vector mask tests pass.
- [ ] Move the Stilus SVG document reader into `src/Isotone.Core/Vector/Svg/`, repointing Stilus's SVG open; `D03 T17 §7` later moves only the renderer. Done when: one SVG reader definition remains and Stilus's `D02 T04 §2` SVG round-trip fixtures still pass.
- [ ] Add `src/Gesso/Isotone.Gesso.Core/Paths/GessoPathSet.cs`: one work path and saved paths with name, color tag, lock, and visibility (IP-1643). Done when: `PathSetTests` add, rename, lock, and hide paths.
- [ ] Add a clipping-path flag with flatness (IP-1648) to `GessoPathSet`, and persist the set as `gesso:paths` (SVG path data per path) through the `D03 T08 §1` contract. Done when: `PathSetTests.RoundTrip` saves and reopens every attribute and geometry within 1e-6.
- [ ] Add `src/Gesso/Isotone.Gesso.Desktop/Views/Panels/PathsPanel.xaml` (IP-1641, IP-1655): a list of the work path in italics and the saved paths, with thumbnails, rename in place, deselect, multi-select, and panel options (thumbnail size). Done when: a driven run renames a path in place and the capture shows the panel. Cheaper substitute: paths shown only in the Layers panel as vector masks.
- [ ] Add Show Target Path (IP-1637), which toggles the on-canvas display of the selected path. Done when: a driven run toggles it and the capture shows both states.
- [ ] Add path management commands (IP-1642): new path, save work path, duplicate, delete, raise, and lower. Done when: a test runs each and undo reverses each.
- [ ] Add Fill Path (IP-1644) with color, pattern, or history source through `D03 T12 §8`. Done when: filling a closed fixture path matches its golden within 1/255.
- [ ] Add Stroke Path (IP-1645) with a painting tool along the flattened path with simulated pressure tapers, or with a line style. Done when: a stroke with simulated pressure is thinner at both ends than in the middle, measured on the result.
- [ ] Add Make Selection from a path (IP-1646) with replace, add, subtract, and intersect, feather, and anti-alias, producing a `D03 T10 §1` selection. Done when: a circle path's selection matches the analytic coverage within 1/255.
- [ ] Add Make Work Path from a selection (IP-1647): marching squares on the mask then Schneider 1990 fitting with tolerance and GIMP's advanced settings (corner threshold, line and curve error). Done when: `SelectionToPathTests` fit a circular selection within 0.5 px using at most eight segments.
- [ ] Enable Convert to Work Path for text layers (IP-1589) from §1 through glyph outlines (`SKFont.GetGlyphPath` into `PathGeometry`). Done when: converting the Latin fixture yields one figure per glyph contour and the menu item is enabled.
- [ ] Register the path implementations earlier sections wait on and enable their controls, removing each tooltip: Vector Mask from Current Path (`D03 T09 §4`), the Selection Editor's To Path button (`D03 T10 §1`), Selection to Path and Path to Selection (`D03 T10 §9`), Place Along Path and the fill and stroke path commands (`D03 T12 §8`), symmetry from a path (`D03 T12 §11`), the Path transform target (`D03 T13 §11`), and path key points as `D03 T08 §4` snap candidates. Done when: each owning section's disabled-state test is updated to assert the enabled control and passes.
- [ ] Add Filter, Render, Flame Along Path, passing the active path flattened to a `Polyline` into the `D01 T06 §9` `Flame` effect's dialog in place of the polyline drawn on canvas. Done when: a test renders a flame along a fixture path and the effect's `Polyline` parameter equals the flattened path within 0.25 px.
- [ ] Name the history steps "New Path", "Save Path", "Stroke Path", "Fill Path", "Make Selection", and "Make Work Path", each with one Serilog Information line. Done when: a Serilog test logger asserts each line.
- [ ] Commit fixtures under `tests/fixtures/gesso/paths/` (circle selection, fill and stroke goldens) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/gesso/paths-panel/` and write `docs/user/gesso/paths.md`. Done when: every panel and menu command appears in a capture and the page documents it.
- [ ] Commit: `"gesso: paths and the Paths panel on path geometry moved to Isotone.Core"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Core.Tests.Vector|FullyQualifiedName~PathSetTests|FullyQualifiedName~SelectionToPathTests"` exits 0 with the moved `PathBooleansTests` passing and `PathSetTests.RoundTrip` reopening every attribute within 1e-6; a filled fixture path matches its golden within 1/255; `grep -rn "class VectorPathSegment" src` prints nothing. Cheaper substitute that fails: a second Gesso path type, which the one-path-type grep catches.

## 6. Pen and Path Editing Tools

Paths are only as good as the tools that draw them. This section builds the pen family of all three competitors (Photoshop's pen, freeform, magnetic, curvature, and content-aware tracing pens, GIMP's Paths tool modes, and Affinity's pen and node behavior) and the anchor, curve, and selection tools, on node-editing math moved from Stilus (`D02 T08 §1`, `D02 T08 §6`, `D02 T08 §7`) into `Isotone.Core/Vector/Editing/`. The magnetic pen and content-aware tracing use the classical live-wire engine of `D03 T10 §5`, with no model. Catalog: IP-1656 to IP-1672 (17 features: the pen tool, GIMP's edit modes, smart, polygon, and line modes, the freeform pen, the magnetic pen, the curvature pen, content-aware tracing, the anchor tools, curve actions, pen output modes, make selection or shape, rubber band, path display options, pixel-grid alignment, snapping options, path and direct selection, and transform path).

**Fidelity:** Gesso pen and path editing tools -- docs/design/components/ (ToolRail, OptionsBar, Canvas, Slider, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/gesso/pen-tools/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a retoucher draws exact outlines and edits their anchors. Consumer: §5's path set, shape layers (§7), and selections.
**Treatment:** the pen tool group with GIMP Paths tool modes and Affinity pen and node behavior, options for output mode, rubber band, and snapping, and on-canvas anchor and handle editing. Cheaper substitute that fails the checkpoint: a polygon-only path tool.
**Chrome:** consume `D03 T08 §4` snapping, the `D03 T10 §5` scissors engine, the `D03 T13 §5` transform handles, and the suite history. Do not add a second node editor.

**Requires:** display-session -- drawing and editing paths need an interactive desktop

- [ ] Move first: pen anchor placement and handle constraints from `D02 T08 §1` `PenTool` and the node operations of `D02 T08 §6` and `D02 T08 §7` (`PathEditCommand` and the node parts of `PathOperationsService`) into `src/Isotone.Core/Vector/Editing/PathEditor.cs` over `PathGeometry`, with tests, so Stilus's tools call it. Done when: the moved `PathEditorTests` pass from `tests/Isotone.Core.Tests/Vector/` and Stilus's pen tests pass.
- [ ] Add `src/Gesso/Isotone.Gesso.Desktop/Tools/Pen/PenTool.cs` (IP-1656): Bezier anchors, close and continue, Ctrl direct select, Alt convert, Shift 45-degree constraint, and adding subpaths to the selected curves. Done when: `PenToolTests` replay scripted gestures into the expected geometry.
- [ ] Add GIMP's Paths tool modes design, edit, and move with their modifiers (IP-1657) as a pen option. Done when: a scripted gesture in edit mode inserts an anchor on a segment.
- [ ] Add smart, polygon, and line pen modes (IP-1658). Done when: polygon mode produces only line segments in a scripted gesture.
- [ ] Add the freeform pen with curve fit (IP-1659) through §5's Schneider fitting. Done when: a scripted freehand circle fits within 1 px with at most eight segments.
- [ ] Add the magnetic pen (IP-1660) with width, contrast, frequency, and pressure on the `D03 T10 §5` live-wire engine. Done when: `MagneticPenTests` follow a committed edge fixture within 1.5 px.
- [ ] Add the curvature pen (IP-1661). Done when: three scripted clicks produce a smooth curve through all three points.
- [ ] Add the content-aware tracing tool (IP-1662) from the same engine's edges with a detail slider, classical, no model. Done when: tracing the committed edge fixture yields a path within 1.5 px of the edge.
- [ ] Add the add, delete, and convert anchor point tools (IP-1663) with auto add and delete and sharp, smooth, and smart node types. Done when: a test converts a smooth anchor to sharp and back with the handles restored.
- [ ] Add curve actions (IP-1664): split, break, close, join, reverse, smooth, shift start, and delete segment, each through `PathEditor`. Done when: a test runs each action and undo reverses it.
- [ ] Add pen output modes (IP-1665): shape layer, path, or pixels, with line style and fill while drawing. Done when: a scripted gesture in each mode produces a shape layer, a work path, or painted pixels respectively.
- [ ] Add Make Selection and Make Shape buttons in the pen options (IP-1666). Done when: each produces a selection or a shape layer from the active path.
- [ ] Add the rubber band preview (IP-1667). Done when: a driven capture shows the next segment previewed before the click.
- [ ] Add path display options (IP-1668): `Gesso.Paths.Thickness`, `Gesso.Paths.Color`, and a direction indicator. Done when: changing each setting redraws the overlay without a restart.
- [ ] Add align vector edges and snap vector tools to the pixel grid on create and transform (IP-1669). Done when: a test asserts a rectangle drawn with the option has integer-aligned edges.
- [ ] Add node and pen snapping options (IP-1670) through `D03 T08 §4`. Done when: a scripted anchor near a guide lands on it with snapping on and not with it off.
- [ ] Add the path selection and direct selection tools (IP-1671) with layer scope, marquee selection, Alt-drag duplicate, and transform controls (Affinity's Node tool merged). Done when: a scripted marquee selects exactly the anchors inside it.
- [ ] Add transform path and transform selected anchors (IP-1672) with the `D03 T13 §5` handles. Done when: rotating two selected anchors by 90 degrees moves only them, asserted in a test.
- [ ] Make each gesture one undo step with a named command and one Serilog Information line per committed path. Done when: a Serilog test logger asserts the line and one undo reverses one gesture.
- [ ] Commit the edge fixture and scripted gestures under `tests/fixtures/gesso/pen/` with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit a driven drawing session capture under `docs/captures/gesso/pen-tools/` and write `docs/user/gesso/pen-tools.md`. Done when: every tool and option appears in a capture and the page documents it.
- [ ] Commit: `"gesso: the pen family and path editing on node math moved to Isotone.Core"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~PathEditorTests|FullyQualifiedName~PenToolTests|FullyQualifiedName~MagneticPenTests"` exits 0, with the magnetic pen within 1.5 px of the committed edge; a driven drawing session is captured under `docs/captures/gesso/pen-tools/`. Cheaper substitute that fails: a Gesso-only pen editing its own segment lists, which the one-path-type grep of §5 catches.

## 7. Shape Layers and Shape Tools

Shapes must stay resolution-independent and editable: per-corner radii, custom shapes, fill and stroke paint, live combine, and GIMP 3.2's vector layers bound to paths. The live-shape generators and corner model come from Stilus (`D02 T08 §4`) and move into `Isotone.Core/Vector/Shapes/`; `ShapeLayer` is rewritten over §5's geometry. Custom shapes, GIMP's vector layers, and the Gfig job are §11, split out on 2026-09-27 so each half stays reviewable in one pass. This promotes backlog B-019. Catalog: IP-1676, IP-1678 to IP-1683, IP-1685 to IP-1692, and IP-1695 (16 features: the shape layer, combine shapes, the rectangle and ellipse tools with corner widgets, corner types, the triangle tool, polygon and star, the line tool, Affinity's extra shape tools, fill and stroke paint, stroke options and presets, shape geometry, live shape properties and conversion to a path, pixels mode, merge shape layers, rasterize shape, and live properties in the Properties panel). -> SOURCE: legacy-gesso-4.7

**Fidelity:** Gesso shape tools, shape layers, and shape properties -- docs/design/components/ (ToolRail, OptionsBar, Panel, Canvas, NumberBox, Swatches, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/gesso/shapes/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Panel/README.md, docs/design/components/Canvas/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Swatches/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer draws resolution-independent shapes that stay editable. Consumer: the layer renderer, the `.gesso` save, and the later PSD and XCF mappings.
**Treatment:** the shape tool group with on-canvas corner widgets, live shape properties in the Properties panel, and fill and stroke paint pickers with stroke presets. Cheaper substitute that fails the checkpoint: shapes rasterized at creation.
**Chrome:** consume §5's geometry, the `D03 T12 §9` gradients, the `D03 T12 §10` patterns, the Properties panel, and the suite history. Do not add a second corner model.

**Requires:** display-session -- the shape tools and captures need an interactive desktop

- [ ] Move first: the live-shape generators and corner model of `D02 T08 §4` (`LiveShape`: rounded, concave, straight, cutout, absolute or relative radii) into `src/Isotone.Core/Vector/Shapes/`, with tests, repointing Stilus. Done when: `LiveShapeTests` pass from `tests/Isotone.Core.Tests/Vector/` against the Stilus corner goldens and one `LiveShape` definition remains.
- [ ] Rewrite `src/Gesso/Isotone.Gesso.Core/Layers/ShapeLayer.cs` over `PathGeometry` plus an optional `LiveShapeSpec`, replacing the fixed shape-kind enum (IP-1676). Done when: every former shape kind maps to a `LiveShapeSpec` and `ShapeLayerTests` render each.
- [ ] Register `gesso:shape` with the PNG fallback through the `D03 T08 §1` contract. Done when: a shape layer round-trips `.gesso` live and `gimp-console-3.2` renders the fallback within 1/255.
- [ ] Add the rectangle and ellipse tools (IP-1679) with per-corner radius and on-canvas corner widgets. Done when: dragging one corner widget in a driven run changes only that corner's radius.
- [ ] Add corner types rounded, straight, concave, and cutout with absolute or relative radii (IP-1680). Done when: each renders within 1/255 of the moved Stilus golden.
- [ ] Add the triangle tool with corner radius (IP-1681). Done when: a test asserts the three corner radii render as specified.
- [ ] Add the polygon and star tool (IP-1682): sides, star ratio, smooth indents, and smooth corners. Done when: a 5-point star at ratio 0.5 matches its golden geometry within 1e-6.
- [ ] Add the line tool with weight and arrowheads (IP-1683). Done when: a line with both arrowheads matches its golden within 1/255.
- [ ] Add Affinity's extra shape tools (IP-1685): rounded rectangle, star variants, diamond, trapezoid, cog, crescent, donut, pie, tear, heart, cloud, callouts, and arrow, each as a `LiveShapeSpec` generator. Done when: each renders a committed golden within 1/255.
- [ ] Add shape fill and stroke paint (IP-1686): solid, gradient (through `D03 T12 §9`), pattern (through `D03 T12 §10`), or none, with gradient and pattern options. Done when: a gradient-filled shape reopens live with equal gradient stops.
- [ ] Add stroke options (IP-1687): align inside, center, or outside, caps, corners, dashes, and saved stroke presets as the `StrokeStyle` record §2 shares. Done when: a saved preset applies to a second shape with equal fields.
- [ ] Add shape geometry fields (IP-1688): W, H, X, Y, drawing constraints, and keep selected. Done when: typing W and H resizes the shape exactly.
- [ ] Add live shape properties in the Properties panel with per-corner radii and shape operations (IP-1689, IP-1695), and Convert to Regular Path. Done when: converting drops the `LiveShapeSpec` and keeps the geometry within 1e-6, and undo restores the live shape.
- [ ] Add Combine Shapes (IP-1678): unite, subtract, intersect, and exclude as live operations inside one layer through `PathBooleans`. Done when: editing a combined component updates the result live and matches its golden.
- [ ] Add Merge Shape Layers (IP-1691). Done when: merging two shape layers yields one shape layer with both figures.
- [ ] Add the shape pixels mode (IP-1690), which paints the shape into the active pixel layer. Done when: a scripted drag in pixels mode adds no layer and paints the expected coverage.
- [ ] Add Rasterize Shape (IP-1692) as one undo step. Done when: rasterized pixels match the live render within 1/255 and undo restores the live layer.
- [ ] Enable Convert to Shape for text layers (IP-1589) from §1, producing a shape layer from the glyph outlines. Done when: converting the Latin fixture yields a shape layer whose geometry matches §5's work-path conversion.
- [ ] Enable the controls earlier sections deferred to shape layers: shape key points as snap candidates and New Guides from shape layers (`D03 T08 §4`), and the gradient stroke context on shape layers (`D03 T12 §9`), and supply rasterized custom shapes as the aux kernel of the `D01 T06 §2` shape blur. Done when: each owning section's disabled-state test is updated to assert the enabled control and passes, and a shape blur with a custom heart shape matches its golden.
- [ ] Commit captures of every shape tool and the live shape properties under `docs/captures/gesso/shapes/`, and write `docs/user/gesso/shapes.md`. Done when: every tool appears in a capture and the page documents it.
- [ ] Commit: `"gesso: live shape layers and the shape tools"`

**Test checkpoint:** Format fidelity proof and unit test: shape layer fixtures under `tests/fixtures/gesso/shapes/` round-trip `.gesso` live (geometry within 1e-6, paint fields equal) and `gimp-console-3.2` renders their fallbacks within 1/255 (GIMP version quoted); `dotnet test Isotone.slnx --filter "FullyQualifiedName~LiveShapeTests|FullyQualifiedName~ShapeLayerTests"` exits 0 against the moved Stilus corner goldens; a driven capture of every shape tool is committed. Cheaper substitute that fails: rasterizing on creation, which the reopen-live assertion catches.

## 8. Frames and Vector Output

Designers crop content into frames and hand vector work to the web. Frame layers pair a shape with placed content (a `D03 T09 §9` smart object), and SVG export writes vector, shape, and text layers as real elements with raster layers embedded or omitted, sharing the SVG export options record that Stilus defined (`D02 T14 §1`), moved here into `Isotone.Core/Vector/Svg/`. The export has its own dialog on the `Isotone.UI` dialog chrome because the format registry of `D03 T17 §1` lands in a later phase; that section then lists this writer in its registry. Catalog: IP-1697 to IP-1703 (7 features: SVG export of vector layers with raster layers embedded or omitted, frames from layers and convert to frame, Copy CSS and SVG, the SVG export options, the frame tool, frame properties, and copy items as SVG).

**Fidelity:** Gesso frame tools and SVG export dialog -- docs/design/components/ (ToolRail, OptionsBar, Dialog, ComboBox, Checkbox, Swatches, Menu), per standards/design-contract.md; goldens under docs/captures/golden/gesso/frames/, docs/captures/golden/gesso/svg-export/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Swatches/README.md, docs/design/components/Menu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer crops content into frames and hands vector work to the web. Consumer: the `.gesso` save for frames, and browsers and vector editors for the exported SVG.
**Treatment:** the frame tool (rectangle and ellipse), Convert to Frame, frame or content selection with properties, an SVG Export dialog with its options, and Copy SVG and Copy CSS in the Layer menu. Cheaper substitute that fails the checkpoint: an SVG that embeds one flattened PNG.
**Chrome:** consume §5's `SvgPathData`, the `D03 T09 §9` smart objects, the `Isotone.UI` dialog chrome, `AtomicFileWriter`, and the suite history. Do not add a second SVG writer.

**Requires:** display-session -- the frame tool and the export dialog need an interactive desktop

- [ ] Move first: the `SvgExportOptions` record of `D02 T14 §1` into `src/Isotone.Core/Vector/Svg/`, repointing Stilus, so both apps share its semantics. Done when: one `SvgExportOptions` definition remains and Stilus's SVG option tests pass.
- [ ] Add `src/Gesso/Isotone.Gesso.FileFormats/Svg/GessoSvgExporter.cs` writing vector and shape layers as `<path>` elements through `SvgPathData` with their fill and stroke (IP-1697). Done when: the exported SVG of the committed vector fixture contains one element per vector layer.
- [ ] Write text layers as `<text>` spans with their runs, or as outlines when the option says so (IP-1700). Done when: a test asserts the span count equals the story's run count in spans mode and no `<text>` element in outlines mode.
- [ ] Write raster layers embedded as PNG or JPEG data URIs, or omit them (IP-1697). Done when: a test asserts each mode's element count and MIME type.
- [ ] Add the options hex colors, flatten transforms, viewBox, and relative coordinates (IP-1700) to the export through the shared record. Done when: each option changes the output as specified in `SvgExportOptionsTests`.
- [ ] Add `src/Gesso/Isotone.Gesso.Desktop/Views/Export/SvgExportDialog.xaml` on the `Isotone.UI` dialog chrome with the options and a target folder, writing through `AtomicFileWriter`; a read-only target folder is refused by name, and a status-strip notification reports completion. Done when: a driven export writes the file, the capture shows the dialog, and exporting to a read-only folder shows the refusal. Cheaper substitute: one embedded PNG.
- [ ] Add Copy SVG (IP-1703) for the selected layers as an `image/svg+xml` clipboard flavor with plain-text SVG beside it. Done when: pasting into Inkscape 1.4 yields the same element count (driven, captured).
- [ ] Add Copy CSS (IP-1699): size, position, colors, radii, gradients, and box-shadow from mappable styles as CSS text. Done when: `CopyCssTests` produce the expected CSS for a rounded, gradient-filled shape with a drop shadow.
- [ ] Add `src/Gesso/Isotone.Gesso.Core/Layers/FrameLayer.cs` (IP-1698, IP-1701): a shape plus a content layer (a `D03 T09 §9` smart object), persisted as `gesso:frame` through the `D03 T08 §1` contract. Done when: a frame round-trips `.gesso` with its content live.
- [ ] Add the Frame tool with rectangle and ellipse frames, Frame from Layers, and Convert to Frame (IP-1698, IP-1701). Done when: converting a raster layer yields a frame whose content renders unchanged within 1/255.
- [ ] Add frame or content selection and frame properties (IP-1702): stroke, W, H, X, Y, and placed-content status. Done when: moving content inside the frame changes only the content's offset, asserted in a test.
- [ ] Name the history steps "Convert to Frame" and "Place in Frame", and log one Serilog Information line per SVG export (path, elements, milliseconds). Done when: a Serilog test logger asserts the line.
- [ ] Commit the vector fixture and its Inkscape 1.4 and resvg 0.45 renders under `tests/fixtures/gesso/svg-export/` with `reference.txt`. Done when: both renders carry their tool versions.
- [ ] Commit captures under `docs/captures/gesso/frames/` and `docs/captures/gesso/svg-export/` and write `docs/user/gesso/frames-and-svg.md`. Done when: every control appears in a capture and the page documents it.
- [ ] Commit: `"gesso: frames and SVG export"`

**Test checkpoint:** Format fidelity proof: the exported SVG of the committed vector fixture renders in Inkscape 1.4 and resvg 0.45 within 1/255 of Gesso's render and contains one element per vector layer, and a frame round-trips `.gesso` with its content live, all reported by `dotnet test Isotone.slnx --filter "FullyQualifiedName~GessoSvgExporterTests|FullyQualifiedName~FrameLayerTests"`. Cheaper substitute that fails: one embedded PNG, which the element-count assertion catches.

## 9. Type Tools and On-Canvas Text Editing

Split from §1 on 2026-09-27 so each half stays reviewable in one pass: §1 moves the engine and builds the live text layer, and this section builds the surfaces that create and edit it, the four type tools (T cycles), the type mask tools, the Toggle Text Orientation command, on-canvas editing with caret, selection, IME composition, commit and cancel, GIMP's floating style editor, the Text Editor window, and the Convert to Work Path and Convert to Shape entries §5 and §7 enable. Catalog: IP-1583 to IP-1589 (7 features: on-canvas editing from the Layers panel, the horizontal type tool with point and paragraph text and GIMP's dynamic or fixed box, the vertical type tool with orientation toggle and vertical Roman alignment, the type mask tools, on-canvas editing behavior with the floating style editor, the Text Editor window, and convert to work path or shape).

**Fidelity:** Gesso type tools and on-canvas text editing -- docs/design/components/ (ToolRail, OptionsBar, Canvas, TextBox, ComboBox, NumberBox, Swatches), per standards/design-contract.md; goldens under docs/captures/golden/gesso/type-tools/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Swatches/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer can add live text in any script with the type tools and edit it on the canvas. Consumer: §1's text layers and their stories.
**Treatment:** the type tool group (horizontal, vertical, horizontal mask, vertical mask; T cycles), click for point text or drag a paragraph box (GIMP dynamic or fixed box), an on-canvas editor with caret, selection, IME underline, commit (Ctrl+Enter or the check) and cancel (Esc), transform handles while editing, GIMP's floating style editor, and a Text Editor window. Cheaper substitute that fails the checkpoint: a modal text dialog that stamps a bitmap.
**Chrome:** consume §1's text layer and the moved `TextEditSession` and `TextInputBridge`, the tool options strip of `D03 T03 §4`, the `Isotone.UI` dialog styles, and the suite history. Do not add a second text editor model.

**Requires:** display-session -- typing into a layer, IME composition, and the captures need an interactive desktop

- [ ] Add `HorizontalTypeTool` and `VerticalTypeTool` in `src/Gesso/Isotone.Gesso.Desktop/Tools/Type/`: click for point text, drag for a paragraph box, T cycling the group. Done when: a driven run creates one point and one paragraph layer and the capture shows both. Cheaper substitute: a text dialog that stamps pixels.
- [ ] Add `HorizontalTypeMaskTool` and `VerticalTypeMaskTool` that produce a `D03 T10 §1` selection from the glyph outlines, never a layer (IP-1586). Done when: a test commits a mask entry and the document gains a selection whose bounds equal the glyph outline bounds and no new layer.
- [ ] Add the Toggle Text Orientation command for the active text layer (IP-1585). Done when: a test toggles a layer and undo restores the original orientation.
- [ ] Add on-canvas editing (IP-1583, IP-1587): double-click a text layer or its Layers-panel thumbnail to edit, caret and selection through the moved `TextEditSession`, IME composition through `TextInputBridge`, commit with Ctrl+Enter or the check, and cancel with Esc. Done when: a driven run types Arabic through the Windows IME and the capture shows the joined text; Esc after typing restores the previous story.
- [ ] Keep transform handles live while editing and keep masked text layers clickable by a layer-bounds hit test. Done when: a driven run scales a text box mid-edit and the story is unchanged.
- [ ] Add GIMP's floating style editor as a draggable overlay above the text box, shown when `Gesso.Type.ShowOnCanvasEditor` is true (default true). Done when: toggling the setting hides the overlay without a restart.
- [ ] Add the Text Editor window (IP-1588): multi-line editing of the active layer with Load from File (UTF-8 and UTF-16) and Clear All. Done when: loading a UTF-16 fixture fills the layer with its text exactly.
- [ ] Add Convert to Work Path and Convert to Shape (IP-1589) to the Type menu, disabled with tooltips naming `D03 T16 §5` (work path) and `D03 T16 §7` (shape layer), which enable them. Done when: `python scripts/todo-graph.py resolve 'D03 T16 §5'` and `'D03 T16 §7'` both resolve and the tooltips name them.
- [ ] Commit captures of the type tools, on-canvas editing, IME composition, the style editor, and the Text Editor window under `docs/captures/gesso/type-tools/`. Done when: each capture exists and the Treatment's controls each appear in one.
- [ ] Extend `docs/user/gesso/type.md` with the type tools, the mask tools, on-canvas editing, the style editor, and the Text Editor. Done when: the page documents every control on this surface.
- [ ] Commit: `"gesso: the type tools and on-canvas text editing"`

**Test checkpoint:** Driven run with evidence and unit test: a driven run creates one point and one paragraph layer with the type tools, types Arabic through the Windows IME, and cancels an edit with Esc, captured under `docs/captures/gesso/type-tools/` with the committed story read back equal; `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Gesso.Core.Tests.Text"` exits 0 with the mask-tool selection-bounds test and the orientation-toggle undo test reporting. Cheaper substitute that fails: a modal dialog that stamps pixels, which the still-live story readback catches.

## 10. Path Exchange and Path Commands: SVG, Illustrator, Clipping Paths, Booleans, and Align

Split from §5 on 2026-09-27 so each half stays reviewable in one pass: §5 moves the geometry, builds the path set and the Paths panel, and bridges paths to selections, fills, and strokes; this section moves paths in and out of Gesso and edits many at once: SVG path import and export through the SVG reader §5 moved, the Illustrator paths export, the clipping path flagged for JPEG and TIFF export, merge visible paths, copy and paste between images, path booleans, and component alignment. Catalog: IP-1638 to IP-1640, IP-1649 to IP-1654 (9 features: SVG path import with scale to fit, export to Illustrator, clipping paths on JPEG and TIFF export, Illustrator export as its second row, merge visible paths, copy and paste paths, SVG import and export, path operations, and align and distribute components).

**Fidelity:** Gesso path exchange and path command dialogs -- docs/design/components/ (Dialog, Menu, Panel, OptionsBar, Canvas, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/gesso/paths-exchange/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Menu/README.md, docs/design/components/Panel/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a retoucher brings paths in from and sends them out to vector apps and combines and aligns path components. Consumer: the path set, the JPEG and TIFF writers of `D03 T17 §11`, and the SVG and Illustrator files other apps read.
**Treatment:** Paths panel menu entries for import, export, merge, and operations, an SVG import options dialog (merged or separate, scale to fit), and path operation and align buttons in the options bar for the path selection tool. Cheaper substitute that fails the checkpoint: exporting paths only as raster masks.
**Chrome:** consume §5's Paths panel, path set, `SvgPathData`, and moved SVG reader, `PathBooleans`, `AtomicFileWriter`, and the suite history. Do not add a second SVG path parser.

**Requires:** display-session -- the import dialog, the panel commands, and the captures need an interactive desktop

- [ ] Add Merge Visible Paths (IP-1650). Done when: a test merges two visible paths and a hidden one stays separate.
- [ ] Add copy and paste of paths between images (IP-1651) as an internal clipboard flavor plus SVG text. Done when: a path pasted into a second document keeps its geometry within 1e-6, and pasting into a text editor yields SVG path data.
- [ ] Add path operations (IP-1653): combine, subtract front, intersect, exclude, and merge components on `PathBooleans`. Done when: each operation on two overlapping fixture figures matches its golden geometry within 1e-6.
- [ ] Add align, distribute, and arrange for path components (IP-1654). Done when: a test aligns three components' left edges to within 1e-9.
- [ ] Add SVG path import (IP-1638, IP-1652) through the moved reader: merged or separate paths, with scale to fit the image. Done when: importing the fixture SVG yields the expected path count and fits within the canvas.
- [ ] Add SVG path export (IP-1652) of the selected or all paths through `SvgPathData`, written through `AtomicFileWriter`. Done when: exported paths re-import through Inkscape 1.4 (version recorded) within 0.01 px.
- [ ] Add Export Paths to Illustrator (IP-1639, IP-1649): one writer for both rows, a PostScript Illustrator 3 path file (the paths-only subset of the Illustrator File Format Specification v7) with the canvas as crop marks, in `src/Gesso/Isotone.Gesso.FileFormats/Illustrator/IllustratorPathWriter.cs`. Done when: the file reads back through Stilus's `D02 T14 §4` legacy AI reader with equal geometry.
- [ ] Mark a top-level clipping path for export (IP-1640) so `D03 T17 §11`'s JPEG and TIFF writers turn it into a clipping path resource. Done when: `GessoPathSet.ExportClippingPath` returns the flagged path and its flatness, asserted in a test.
- [ ] Commit fixtures under `tests/fixtures/gesso/paths/` (SVG input, boolean pairs) with goldens and `reference.txt` naming Inkscape 1.4. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/gesso/paths-exchange/` and extend `docs/user/gesso/paths.md` with import, export, merge, operations, and align. Done when: every command appears in a capture and the page documents it.
- [ ] Commit: `"gesso: path exchange with SVG and Illustrator, clipping paths for export, and path commands"`

**Test checkpoint:** Format fidelity proof and unit test: exported SVG paths re-import through Inkscape 1.4 (version recorded) within 0.01 px; the Illustrator path file reads back through Stilus's `D02 T14 §4` legacy AI reader with equal geometry; `dotnet test Isotone.slnx --filter "FullyQualifiedName~PathSetTests|FullyQualifiedName~Isotone.Gesso.Core.Tests.Paths"` exits 0 with each boolean operation on the fixture pairs matching its golden geometry within 1e-6 and the flagged clipping path returned with its flatness. Cheaper substitute that fails: a writer proven only by Gesso's own reader, which the Inkscape re-import catches.

## 11. Custom Shapes, Vector Layers, and the Gfig Job

Split from §7 on 2026-09-27 so each half stays reviewable in one pass: §7 builds live shape layers and the shape tools, and this section adds the user's own shape library (the Shapes panel, Define Custom Shape, the custom shape tool, and CSH import from the user's files), GIMP 3.2's vector layers bound to paths with their fill, stroke, and on-canvas editing, and GIMP's Gfig job met by arc and spiral generators with no gfig file reader. Catalog: IP-1673 to IP-1675, IP-1677, IP-1684, IP-1693, IP-1694, and IP-1696 (8 features: the Shapes panel, define custom shape, Gfig figures, editing vector layers on canvas, the custom shape tool, vector layers from paths, vector layer fill and stroke, and the legacy shape option).

**Fidelity:** Gesso custom shapes panel and vector layers -- docs/design/components/ (Panel, ListTree, ToolRail, OptionsBar, Canvas), per standards/design-contract.md; goldens under docs/captures/golden/gesso/custom-shapes/, docs/captures/golden/gesso/vector-layers/. **Corrected 2026-09-27:** this line cited `docs/captures/gesso/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer keeps a personal shape library and draws GIMP-style vector layers that follow their paths. Consumer: the layer renderer, the `.gesso` save, and the later PSD and XCF mappings.
**Treatment:** the Shapes panel with Isotone's own shape set, the custom shape picker, and GIMP-style vector layer options. Cheaper substitute that fails the checkpoint: shapes stamped as pixels from a bundled image list.
**Chrome:** consume §7's shape layer and `LiveShapeSpec`, §5's saved paths, §6's path tools, the Properties panel, and the suite history. Do not add a second shape library store.

**Requires:** display-session -- the Shapes panel, the custom shape tool, and vector layer editing need an interactive desktop

- [ ] Add the Shapes panel (IP-1673, IP-1696) with Isotone's own shape set (no Adobe shapes bundled) and the legacy shape tool option. Done when: a driven run places a shape from the panel and the capture shows it.
- [ ] Add Define Custom Shape (IP-1674) from the active path into the user's shape library. Done when: a defined shape appears in the panel after reopening Gesso.
- [ ] Add the custom shape tool with its shape picker (IP-1684). Done when: a scripted drag places the picked shape at the dragged size.
- [ ] Add CSH import from the user's own files only, with a reader built from the published reverse-engineered layout named in a `docs/dev/decisions.md` row; unknown versions, and files the file system's permissions deny, are refused by name. Done when: a CSH fixture made for the tests imports its shapes, and an unknown-version fixture is refused with its name.
- [ ] Add a `VectorLayer` kind (`D03 T09 §1`) in `src/Gesso/Isotone.Gesso.Core/Layers/VectorLayer.cs` bound to a saved path, with non-destructive transform and drop to fill (IP-1693). Done when: editing the bound path updates the vector layer render.
- [ ] Add vector layer fill and stroke (IP-1694): color or pattern, antialias, width, cap, join, miter, and dashes. Done when: each option renders within 1/255 of a GIMP 3.2 golden of the same vector layer.
- [ ] Add on-canvas editing of vector layers with the §6 tools (IP-1677). Done when: a driven run moves an anchor of a vector layer's path and the layer re-renders.
- [ ] Register `gesso:vector` with the PNG fallback through the `D03 T08 §1` contract. Done when: a vector layer round-trips `.gesso` live and the fallback renders in `gimp-console-3.2` within 1/255.
- [ ] Meet the Gfig job (IP-1675) with arc and spiral generators added to `src/Isotone.Core/Vector/Shapes/` and grid snap; no gfig file reader is built, recorded in `docs/user/gesso/shapes.md`. Done when: the arc and spiral generators render their goldens.
- [ ] Commit captures of the Shapes panel, the custom shape tool, and vector layer options under `docs/captures/gesso/custom-shapes/` and `docs/captures/gesso/vector-layers/`, and extend `docs/user/gesso/shapes.md`. Done when: every control appears in a capture and the page documents it.
- [ ] Commit: `"gesso: custom shapes, vector layers, and the Gfig generators"`

**Test checkpoint:** Format fidelity proof and unit test: vector layer fixtures under `tests/fixtures/gesso/shapes/` round-trip `.gesso` live and `gimp-console-3.2` renders their fallbacks within 1/255 (GIMP version quoted), each vector layer fill and stroke option renders within 1/255 of its GIMP 3.2 golden, and `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Gesso.Core.Tests.Shapes"` exits 0 with a defined shape surviving a Gesso restart and the unknown-version CSH fixture refused by name. Cheaper substitute that fails: vector layers baked to pixels, which the edit-the-bound-path re-render test catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 with every `tests/Isotone.Core.Tests/Text/`, `tests/Isotone.Core.Tests/Vector/`, and Gesso text, path, shape, and SVG test class reporting
- [ ] `grep -rn "class TextShaper\|class TextLayoutEngine\|class PathBooleans\|class LiveShape\b" src` prints one path each, all under `src/Isotone.Core/`, and `grep -rn "class VectorPathSegment" src` prints nothing
- [ ] Every `.gesso` fixture with text, shape, vector, or frame layers opens renamed to `.ora` in `gimp-console-3.2` with its fallback composite within 1/255
- [ ] Every disabled control on this file's surfaces names a section that `python scripts/todo-graph.py resolve` resolves (`D03 T17 §3`)
- [ ] B-018 and B-019 are gone from `todo/backlog.md`, and their source keys `legacy-gesso-4.8` and `legacy-gesso-4.7` are carried by §1 and §7 alone
- [ ] `python scripts/todo-graph.py validate` clean
