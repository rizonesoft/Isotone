# Bezier - Production Roadmap

> **Vision**: The ultimate open-source SVG editor that rivals and surpasses Inkscape, Figma, Illustrator, and CorelDRAW — with innovative features they don't have.

---

## 🔧 Quick Fix Prompt
*Use for: Bug fixes, small improvements, one-off tasks*

```
You are developing Bezier, a professional SVG editor in C# / WPF.

TASK: [DESCRIBE THE FIX OR IMPROVEMENT]

RULES:
✓ Read TODO.md and STANDARDS.md first
✓ Put logic in Bezier.Core, UI in Bezier.Desktop
✓ Use existing patterns from the codebase
✓ Build and test before committing
✗ Don't add unrelated features
✗ Don't refactor unrelated code

STEPS:
1. Understand the issue → read relevant files
2. Implement the fix → minimal, focused changes
3. Build: dotnet build Bezier.sln
4. Test: dotnet run --project Bezier.Desktop
5. Commit: git add -A && git commit -m "fix: [description]"
6. Push: git push origin master
```

---

## 🤖 Feature Development Prompt
*Use for: Implementing TODO items, building new features*

```
You are developing Bezier, a professional SVG editor in C# / WPF.

TASK: Implement section [PHASE.SECTION] from TODO.md
Example: "Implement section 3.2" or "Implement 4.3 Advanced Path Operations"

RULES:
✓ Check TODO.md for the exact requirements
✓ Mark items [x] when complete
✓ Put models/interfaces in Bezier.Core
✓ Put UI/rendering in Bezier.Desktop
✓ Follow STANDARDS.md (.NET 10 / C# 14)
✓ Match existing code style
✗ Don't skip items — implement ALL sub-items
✗ Don't mark items [x] unless fully working

WORKFLOW:
1. Read the section in TODO.md
2. Read related existing code
3. Implement each item, one by one
4. Build: dotnet build Bezier.sln
5. Run & verify: dotnet run --project Bezier.Desktop
6. Mark completed items with [x] in TODO.md
7. Commit: git add -A && git commit -m "feat: [section] - [description]"
8. Push: git push origin master
```

---

## ✨ Vibe Coding Prompt
*Use for: Polish, enhancement, making features production-ready*

```
You are a senior developer polishing Bezier, a professional SVG editor.

TASK: Make [FEATURE] production-ready and delightful.

YOUR MISSION:
1. VERIFY — Does it exist? Is it complete? Test it.
2. FIX — If broken or missing, implement it properly.
3. POLISH — Add edge case handling, validation, error messages.
4. ENHANCE — Better UX: animations, tooltips, keyboard shortcuts.
5. INTEGRATE — Ensure it works with related features.

QUALITY CHECKLIST:
□ Feature works as described in TODO.md
□ UI is accessible (keyboard, tooltips, cursors, buttons)
□ Errors are handled gracefully
□ Code follows existing patterns
□ No console errors or warnings

STRUCTURE:
- Bezier.Core → Models, interfaces, business logic (no UI)
- Bezier.Desktop → WPF views, controls, rendering
- Bezier.Tests → Unit tests

FINISH:
1. Build: dotnet build Bezier.sln
2. Test manually: dotnet run --project Bezier.Desktop
3. Update TODO.md: mark [x] for completed items
4. Commit: git add -A && git commit -m "feat: [feature] polished"
5. Push: git push origin master
```

---

## 🎯 Precision Prompt
*Use for: Very specific, single-item tasks*

```
CONTEXT: Bezier is a C#/WPF SVG editor. See TODO.md for roadmap.

DO THIS ONE THING: [EXACT TASK]

CONSTRAINTS:
- Change only what's needed for this task
- Follow patterns in existing code
- Build must pass: dotnet build Bezier.sln
- Test by running: dotnet run --project Bezier.Desktop

OUTPUT: Show me the code changes, then run build + commit + push.
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | .NET 10 / C# 14 | Core platform |
| **UI** | WPF + WPF-UI | Native Windows with Fluent Design |
| **Rendering** | SkiaSharp + Svg.Skia | GPU-accelerated 2D graphics |
| **Layout** | AvalonDock | Dockable panels |
| **Code Editor** | Monaco (WebView2) | SVG/XML editing with IntelliSense |
| **MVVM** | CommunityToolkit.Mvvm | Data binding & commands |
| **Logging** | Serilog | Structured logging |
| **Settings** | Newtonsoft.Json | Configuration storage |
| **DI** | Microsoft.Extensions.DependencyInjection | Service container |

---

# PHASE 0: Foundation & Setup

## 0.1 Solution Architecture
- [x] Create `Bezier.sln` with proper separation of concerns
- [x] **Bezier.Core** (.NET 10 Class Library)
  - [x] Models (VectorElement, VectorDocument, Transform)
  - [x] Interfaces (IFill, IEditorCommand, ITool)
  - [x] Services (SelectionManager, HistoryManager, ToolManager)
  - [x] Commands (Move, Rotate, Scale, Add, Delete)
- [x] **Bezier.Desktop** (.NET 10 WPF)
  - [x] MVVM structure (ViewModels, Views, Commands)
  - [x] Custom Controls (SkiaCanvas, ColorPicker)
  - [x] Services (SkiaRenderer, FileService, ClipboardService)
- [x] **Bezier.Tests** (xUnit)
  - [x] Unit tests for Core services
  - [x] Integration tests for import/export
- [x] Set up Dependency Injection

## 0.2 Project Structure
- [x] `Bezier.Core/Models/` — Domain entities
- [x] `Bezier.Core/Models/Elements/` — VectorElement subclasses
- [x] `Bezier.Core/Models/Fills/` — Fill types (Solid, Gradient, Pattern)
- [x] `Bezier.Core/Interfaces/` — Contracts
- [x] `Bezier.Core/Services/` — Business logic
- [x] `Bezier.Core/Commands/` — Editor commands
- [x] `Bezier.Core/Tools/` — Tool implementations
- [x] `Bezier.Desktop/Views/` — XAML views
- [x] `Bezier.Desktop/Views/Panels/` — Dockable panels
- [x] `Bezier.Desktop/Views/Dialogs/` — Modal dialogs
- [x] `Bezier.Desktop/ViewModels/` — ViewModel classes
- [x] `Bezier.Desktop/Controls/` — Custom WPF controls
- [x] `Bezier.Desktop/Resources/` — Icons, styles, themes
- [x] `Bezier.Desktop/Assets/` — Fonts, images
- [x] `Bezier.Desktop/Services/` — Platform-specific services

## 0.3 Core Dependencies
- [x] SkiaSharp & SkiaSharp.Views.WPF
- [x] Svg.Skia
- [x] Dirkster.AvalonDock
- [x] CommunityToolkit.Mvvm
- [x] Microsoft.Web.WebView2
- [x] WPF-UI (Fluent Design)
- [x] Serilog + Serilog.Sinks.File
- [x] Newtonsoft.Json
- [x] Microsoft.Extensions.DependencyInjection

## 0.4 Version Control & CI
- [x] Initialize Git with .gitignore
- [x] README.md with project overview
- [x] CONTRIBUTING.md with code style guidelines
- [x] LICENSE file (MIT)
- [x] .editorconfig for formatting
- [x] .github/workflows/build.yml for CI
- [x] dependabot.yml for NuGet updates
- [x] CHANGELOG.md
- [ ] Branch protection rules

## 0.5 Initial UI Shell
- [x] Main window with Mica/Acrylic backdrop
  - [x] Custom chrome with resize grips
  - [x] Title bar (icon, name, min/max/close)
- [x] Dark theme (Catppuccin Mocha)
  - [x] Light theme option (Catppuccin Latte)
- [x] App icon (16, 32, 48, 256px)
- [x] Splash screen with logo animation
- [x] AvalonDock skeleton

## 0.6 Main Menu Bar
- [x] **File**: New, Open, Open Recent, Save, Save As, Export, Close, Exit
- [x] **Edit**: Undo, Redo, Cut, Copy, Paste, Duplicate, Delete, Select All, Preferences
- [x] **View**: Zoom In/Out, Fit, 100%, Grid, Rulers, Guides, Outline Mode, Panels
- [x] **Object**: Group, Ungroup, Order (Front/Back/Forward/Backward), Align, Distribute, Transform
- [x] **Path**: Union, Subtract, Intersect, Exclude, Simplify, Stroke to Path, Text to Path
- [x] **Help**: Documentation, Keyboard Shortcuts, About

## 0.7 Main Toolbar
- [x] New, Open, Save
- [x] Undo, Redo
- [x] Zoom dropdown, Fit to window
- [x] Toggle grid, rulers, snap

---

# PHASE 1: Core Rendering Engine

## 1.1 Document Model
- [x] `VectorDocument` (root)
  - [x] Width, Height, ViewBox
  - [x] Metadata (title, author, license, description)
  - [x] IsDirty flag
  - [ ] Layers collection
  - [ ] Defs collection (gradients, patterns, symbols)
  - [ ] Background color/pattern
- [x] `VectorElement` (abstract base)
  - [x] Id (GUID), Name
  - [x] IsVisible, IsLocked
  - [x] Opacity (0-1)
  - [x] BlendMode
  - [x] Transform
  - [x] Parent reference
  - [x] Fill, Stroke
  - [x] INotifyPropertyChanged

## 1.2 Element Types
- [x] `SvgPath` — PathData string, nodes collection
- [x] `SvgRect` — x, y, width, height, rx, ry
- [x] `SvgCircle` — cx, cy, r
- [x] `SvgEllipse` — cx, cy, rx, ry
- [x] `SvgLine` — x1, y1, x2, y2
- [x] `SvgPolygon` / `SvgPolyline` — points array
- [x] `SvgText` — content, font properties, text alignment
- [x] `SvgImage` — embedded base64 or external href
- [x] `SvgGroup` — children collection, recursive transform
- [ ] `SvgSymbol` — reusable definition with use instances
- [ ] `SvgUse` — symbol instance with overrides
- [ ] `SvgClipPath` — clipping mask definition
- [ ] `SvgMask` — opacity mask definition
- [ ] `SvgMarker` — arrow heads and path markers
- [ ] `SvgPattern` — repeating pattern definition
- [ ] `SvgGradient` — gradient definition (referenced by fills)

## 1.3 Transform System
- [x] `Transform` struct (3x3 matrix)
  - [x] Translate, Rotate, Scale, Skew methods
  - [x] Multiply, Invert, TransformPoint
  - [x] Identity static property
- [x] HitTest(Point) for each element
- [x] BoundingBox calculation with transform
- [x] Clone() for deep copy
- [x] ToSvgString() serialization

## 1.4 Fill & Stroke System
- [x] `IFill` interface with ToSkiaPaint(), Clone()
- [x] `NoneFill` — transparent
- [x] `SolidFill` — RGBA color, opacity
- [x] `LinearGradientFill` — start/end points, stops, spread mode
- [x] `RadialGradientFill` — center, radius, focal point, stops
- [x] `PatternFill` — tiled element reference
- [ ] `ConicGradientFill` — angle-based gradient
- [ ] `MeshGradientFill` — freeform gradient mesh
- [x] `Stroke` class
  - [x] Width, Color/Fill
  - [x] Dash array, Dash offset
  - [x] Line cap (butt, round, square)
  - [x] Line join (miter, round, bevel), Miter limit
  - [ ] Variable width (pressure)
  - [ ] Position (center, inside, outside)
  - [ ] Multiple strokes per element

## 1.5 SkiaSharp Rendering
- [x] `SkiaCanvas` WPF control (inherits SKElement)
  - [x] OnPaintSurface override
  - [x] Mouse & keyboard event handling
- [x] Render loop with 60fps target
  - [x] Dirty flag optimization
  - [x] Render on demand
- [x] `SkiaRenderer` service
  - [x] Render VectorDocument
  - [x] Apply transforms, fills, strokes
- [x] Infinite canvas (pan/zoom)
  - [x] View transform matrix
  - [x] Mouse wheel zoom (center on cursor)
  - [x] Pan with middle mouse / spacebar
  - [x] Smooth animated zoom
- [x] Grid rendering (adaptive dots/lines)
- [x] Ruler rendering (cursor indicators, tick marks)
- [x] Pixel Preview mode
- [x] Outline Mode (wireframe)
- [x] Background (checkerboard, solid color)

## 1.6 SVG Import/Export
- [x] `SvgImporter`
  - [x] Parse SVG attributes and namespaces
  - [x] Handle defs, gradients, CSS styles
  - [x] Error handling for invalid SVG
  - [ ] Handle clipPath and mask
  - [ ] Handle markers (arrows)
- [x] `SvgExporter`
  - [x] Generate valid SVG 1.1
  - [x] Minify option
  - [x] Inline vs CSS styles
  - [x] Preserve IDs option
- [x] Round-trip fidelity verification

## 1.7 Status Bar
- [x] Zoom percentage
- [x] Cursor X, Y coordinates
- [x] Selection info (count, dimensions)
- [x] Document info (size, element count)
- [ ] Color mode indicator
- [ ] Snap status indicator
- [ ] Tool hint text

---

# PHASE 2: Editor Architecture

## 2.1 Undo/Redo System
- [x] `IEditorCommand` interface
  - [x] Execute(), Undo()
  - [x] Description, IsUndoable
- [x] `HistoryManager` (undo/redo stacks)
  - [x] CanUndo, CanRedo observables
  - [x] MaxHistorySize setting
  - [x] Clear(), HistoryChanged event
- [x] Core commands
  - [x] MoveCommand, RotateCommand, ScaleCommand
  - [x] PropertyChangeCommand
  - [x] AddElementCommand, DeleteElementCommand
  - [x] ReorderCommand
  - [x] GroupCommand, UngroupCommand
  - [ ] DuplicateCommand
- [ ] Transaction/batching support
  - [ ] BeginTransaction()
  - [ ] CommitTransaction()
  - [ ] RollbackTransaction()
- [ ] MacroCommand (group multiple commands)

## 2.2 Tool System
- [x] `ITool` interface
  - [x] Name, Icon, Cursor, Shortcut
  - [x] OnActivate(), OnDeactivate()
  - [x] OnMouseDown/Move/Up(Point, Modifiers)
  - [x] OnKeyDown/Up(Key, Modifiers)
  - [x] RenderOverlay(Canvas)
- [x] `ToolManager`
  - [x] ActiveTool property
  - [x] Tools collection
  - [x] Keyboard shortcut handling
- [x] `SelectTool` — selection, move, resize, rotate
- [x] `PanTool` — spacebar/middle-mouse drag
- [x] `ZoomTool` — click/drag to zoom

## 2.3 Selection Manager
- [x] SelectedElements observable collection
- [x] SelectionChanged event
- [x] Aggregate bounding box for multi-selection
- [x] Handle selection during group/ungroup
- [x] Selection highlight/handles rendering

## 2.4 Docking Layout (AvalonDock)
- [x] DockingManager with dark theme
- [x] Document pane (canvas)
  - [ ] Multiple document tabs
  - [ ] Tab header with dirty indicator
  - [ ] Close/Close All/Close Others context menu
- [x] Anchorable panes
  - [x] Layers Panel
  - [x] Properties Panel
  - [x] Toolbox Panel
  - [x] History Panel
  - [ ] Code Editor Panel
  - [ ] Assets Panel
  - [ ] Symbols Panel
  - [ ] Navigator Panel (minimap)
  - [ ] Info Panel (coordinates, measurements)
- [ ] Save/Load layout state to JSON
- [x] Reset Layout command
- [x] Window menu with panel toggles

## 2.5 Contextual Property Bar
> Secondary toolbar that changes based on active tool/selection

- [ ] PropertyBar control (below main toolbar)
  - [ ] Dynamic content based on context
  - [ ] Consistent height and styling
- [ ] Tool-specific bars:
  - [ ] **Select Tool**: X, Y, W, H, rotation, flip buttons
  - [ ] **Rectangle Tool**: Corner radius, dimensions, from center
  - [ ] **Ellipse Tool**: Dimensions, pie/arc options
  - [ ] **Pen Tool**: Path mode, close path, curve options
  - [ ] **Text Tool**: Font, size, weight, alignment
  - [ ] **Zoom Tool**: Level dropdown, fit options
- [ ] Selection-specific bars:
  - [ ] No Selection: Document properties
  - [ ] Single Element: Element properties
  - [ ] Multi-Selection: Align, distribute, group
  - [ ] Path Selected: Node editing options
  - [ ] Text Selected: Typography options

## 2.6 Tabbed Panel Groups
- [ ] Tabbed panel containers
  - [ ] Tab strip at top
  - [ ] Drag tabs to reorder
  - [ ] Tab overflow menu
- [ ] Default groupings:
  - [ ] Right: Properties + Layers + History
  - [ ] Left: Tools + Symbols
  - [ ] Bottom: Code Editor + Messages
- [ ] Panel collapse to icon strip
- [ ] Save/restore configurations

## 2.7 Workspaces
- [ ] Saved panel/toolbar configurations
  - [ ] Built-in: Default, Minimal, Illustration, Typography
  - [ ] User custom workspaces
- [ ] Quick workspace switcher
- [ ] Focus Mode (Tab key — hide all panels)
- [ ] Panel search/filter

---

# PHASE 3: Drawing & Editing Tools

## 3.1 Selection & Transform
- [x] Bounding box rendering (dashed border, semi-transparent fill)
- [x] Resize handles (8 points — corners + edges)
  - [x] Proportional resize (Shift)
  - [x] Center resize (Alt)
  - [x] Cursor change on hover
- [x] Rotate handle (above center)
  - [x] 15° snap (Shift)
  - [x] Angle tooltip
- [ ] Skew handles (edge midpoints with Alt)
- [x] Multi-select (Shift+Click, Ctrl+Click, Marquee)
- [ ] Deep Select (Ctrl+Click into group)
- [ ] Select Same (by fill, stroke, type)
- [x] Select All (Ctrl+A)
- [x] Invert Selection (Ctrl+Shift+I)
- [ ] Free Transform mode (distort corners freely)
- [ ] Numeric transform input (property bar)

## 3.2 Basic Shape Tools
- [x] **Rectangle Tool**
  - [x] Drag to create
  - [x] Shift for square
  - [x] Alt for center origin
  - [x] Live dimensions tooltip
  - [ ] Corner radius handles (post-creation)
  - [ ] Individual corner radius controls
- [x] **Ellipse Tool**
  - [x] Shift for circle
  - [x] Live dimensions tooltip
  - [ ] Pie mode (start/end angle)
  - [ ] Arc mode (open arc)
- [x] **Line Tool**
  - [x] Shift for 45° snap
  - [x] Live length/angle tooltip
  - [ ] Arrow heads (start, end, both)
  - [ ] Connector mode (auto-route between objects)
- [ ] **Polygon Tool**
  - [ ] Sides: 3-100 (property bar)
  - [ ] Corner rounding
  - [ ] Star mode (inner radius)
- [ ] **Star Tool**
  - [ ] Points: 3-100
  - [ ] Inner/outer radius ratio
  - [ ] Smooth points option
- [ ] **Spiral Tool**
  - [ ] Number of turns
  - [ ] Decay rate
  - [ ] Direction (CW/CCW)
- [ ] **Arc Tool**
  - [ ] Start/end angle
  - [ ] Chord/pie/arc modes
- [ ] **Grid Tool**
  - [ ] Rows and columns
  - [ ] Gutter spacing
- [ ] **Arrow Tool** (preset arrow shapes)
- [ ] **Callout Shapes** (speech bubbles, labels)
- [ ] **Flowchart Shapes** (decision, process, data)
- [ ] **Banner Shapes** (ribbons, scrolls)
- [x] Live preview during creation
- [x] Default fill/stroke for new shapes

## 3.3 Pen Tool (Bezier Curves)
- [x] Node/Control Point structure
  - [x] Position, InHandle, OutHandle
  - [x] Type: Corner, Smooth, Symmetric
- [x] Click for corner point
- [x] Click+Drag for smooth curve
- [x] Alt+Drag to break tangent (cusp)
- [x] Click on first point to close
- [x] Magnetic snap to close (10px radius)
- [x] Rubber band preview
- [x] Angle/length tooltip
- [x] Escape to cancel, Enter to finish
- [x] Backspace to delete last point
- [ ] Click on existing node to select
- [ ] Continue existing open path
- [ ] Add to existing closed path

## 3.4 Node Editing Tool
- [x] Select nodes (click, Shift+click, marquee)
- [x] Drag nodes to reshape
- [x] Drag control handles for curvature
- [x] Convert node types (1, 2, 3 keys)
- [x] Add/Remove nodes (double-click/Delete)
- [ ] Select all nodes (Ctrl+A in node mode)
- [ ] Retract handles (double-click on handle)
- [ ] Extend handles (drag from node)
- [ ] Add nodes at equal intervals
- [ ] Simplify path (reduce nodes with tolerance)
- [ ] Smooth path (add curves with smoothness)
- [ ] Roughen path (add jitter)
- [ ] Break path at node
- [ ] Join paths (connect/average endpoints)
- [ ] Reverse path direction
- [ ] Close/Open path
- [ ] Fillet corners (radius)
- [ ] Chamfer corners
- [ ] Align nodes (horizontal/vertical)
- [ ] Distribute nodes evenly

## 3.5 Text Tool
- [x] Click to create point text
- [x] Inline editing on canvas (cursor, selection)
- [x] Font picker (family, weight, style)
- [x] Font size, line height, letter spacing
- [x] Text alignment (left, center, right, justify)
- [x] Fill and stroke
- [ ] Drag to create area text (text box)
  - [ ] Text wraps within bounds
  - [ ] Auto-size height option
- [ ] Font features:
  - [ ] System fonts list with preview
  - [ ] Recent fonts
  - [ ] Search/filter
  - [ ] Variable fonts (weight axis)
- [ ] Advanced typography:
  - [ ] Character spacing (tracking)
  - [ ] Word spacing
  - [ ] Baseline shift
  - [ ] Kerning (auto/optical/metrics)
  - [ ] Leading (line spacing)
- [ ] Text on path
  - [ ] Attach text to path
  - [ ] Offset along path
  - [ ] Flip direction
- [ ] Text inside shape (area type)
- [ ] Text columns
- [ ] OpenType features panel
  - [ ] Ligatures
  - [ ] Stylistic alternates
  - [ ] Small caps
  - [ ] Fractions, ordinals
  - [ ] Superscript/subscript
- [ ] Paragraph styles
- [ ] Character styles
- [ ] Bullets and numbering
- [ ] Tabs and leaders
- [ ] Drop caps
- [ ] Text wrap around objects
- [ ] Find and replace text
- [ ] Spell check

## 3.6 Freehand Tools
- [ ] **Pencil Tool**
  - [ ] Fidelity slider
  - [ ] Smoothness slider
  - [ ] Edit selected paths
- [ ] **Brush Tool**
  - [ ] Brush picker
  - [ ] Size, pressure sensitivity
- [ ] **Blob Brush** (paint filled shapes)
  - [ ] Merge with same color
  - [ ] Fidelity
- [ ] **Eraser Tool**
  - [ ] Erase path segments
  - [ ] Erase within selection

## 3.7 Guides & Snapping
- [x] Draggable guides from rulers
- [x] Snap to grid
- [x] Snap to guides
- [x] Snap to objects (edges, centers)
- [x] Smart guides (alignment lines)
- [x] Snap tolerance setting
- [ ] Double-click guide to set position numerically
- [ ] Rotated guides (angled)
- [ ] Guide colors
- [ ] Size matching guides
- [ ] Spacing equalization guides
- [ ] Distance indicators (hold Alt)
- [ ] Snap to pixel (pixel-perfect mode)
- [ ] Snap to artboard
- [ ] Snap to key points (intersections)

## 3.8 Measurement Tools
- [ ] **Measure Tool**
  - [ ] Click-drag to measure distance
  - [ ] Show angle
  - [ ] Show dx, dy
- [ ] **Dimension Lines**
  - [ ] Linear dimensions
  - [ ] Angular dimensions
  - [ ] Radius/diameter
- [ ] Automatic dimension labels
- [ ] Area calculation (selected shapes)
- [ ] Perimeter calculation
- [ ] Document scale setting (1:1, 1:10, etc.)

## 3.9 Alignment & Distribution
- [x] Align left, center, right (horizontal)
- [x] Align top, middle, bottom (vertical)
- [x] Distribute horizontally
- [x] Distribute vertically
- [x] Align to canvas
- [x] Align to selection bounds
- [x] Align to key object
- [ ] Distribute spacing (equal gaps)
- [ ] Align to artboard
- [ ] Alignment panel with visual buttons
- [ ] Keyboard shortcuts for alignment

---

# PHASE 4: Professional Features

## 4.1 Layers System
- [x] Layers Panel (tree view with thumbnails)
  - [x] Layer row: thumbnail, name, visibility, lock
  - [x] Expand/collapse groups
  - [x] Active layer indicator
- [x] Drag-and-drop reordering
- [x] Visibility toggle (Eye icon)
- [x] Lock toggle
- [x] Opacity slider per layer
- [x] Blend mode per layer
- [x] Group/Ungroup (Ctrl+G, Ctrl+Shift+G)
- [x] Isolation Mode (double-click to edit)
- [x] Rename (double-click or F2)
- [x] Duplicate layer
- [x] Delete with confirmation
- [x] Merge layers
- [ ] Layer search/filter
- [ ] Color labels for layers
- [ ] Layer effects (non-destructive)
- [ ] Clipping mask to layer below
- [ ] Layer comp (save layer states)

## 4.2 Property Inspector
- [x] Collapsible sections
- [x] Dynamic content based on selection
- [x] **Color Picker**
  - [x] Color wheel
  - [x] Saturation/brightness square
  - [x] RGB, HSL, HEX sliders
  - [x] Alpha slider
  - [ ] Eyedropper (pick from canvas)
  - [ ] Pick from screen (anywhere)
  - [ ] Saved swatches
  - [ ] Recent colors (last 20)
  - [ ] Color harmonies (complementary, analogous, triadic)
  - [ ] Global colors (linked swatches)
  - [ ] Spot colors (print)
  - [ ] Color books (Pantone)
- [x] **Gradient Editor**
  - [x] Add/remove/drag stops
  - [x] Angle/position controls
  - [x] Linear/Radial/Conic types
  - [ ] Preset gradients library
  - [ ] Gradient on stroke
  - [ ] Freeform gradient (mesh-like)
  - [ ] Noise gradient
- [x] **Stroke Controls**
  - [x] Width with slider
  - [x] Preset dash patterns
  - [x] Cap and join style icons
  - [ ] Variable width stroke
  - [ ] Stroke position (center/inside/outside)
  - [ ] Multiple strokes per object
- [x] **Geometry Properties**
  - [x] X, Y, Width, Height inputs
  - [x] Constrain proportions toggle
  - [x] Rotation input with dial
  - [ ] Skew X/Y controls
  - [ ] Flip H/V buttons
- [x] **Transform Origin** (9-point grid)
- [x] **Opacity & Blend Mode**
- [x] **Corner Radius**
  - [x] Uniform radius
  - [ ] Individual corners
- [ ] **Appearance Panel** (multiple fills/strokes)
  - [ ] Add fill/stroke layers
  - [ ] Reorder appearance items
  - [ ] Toggle visibility per item
  - [ ] Opacity/blend per item
- [ ] **Effects Stack**
  - [ ] Drop shadow
  - [ ] Inner shadow
  - [ ] Outer/inner glow
  - [ ] Gaussian blur
  - [ ] Motion blur
  - [ ] Feather
  - [ ] Bevel & emboss
- [ ] **Graphic Styles Panel**
  - [ ] Save appearance as style
  - [ ] Apply style to selection
  - [ ] Style library

## 4.3 Path Operations
- [x] Boolean operations (SKPath.Op)
  - [x] Union, Subtract, Intersect, Exclude
  - [ ] Divide (split by intersections)
  - [ ] Trim (cut overlaps)
  - [ ] Merge (combine like paths)
  - [ ] Crop (clip to shape)
  - [ ] Preview before applying
- [x] Text to Path
- [x] Stroke to Path (outline)
- [x] Path Simplify (decimate nodes)
- [x] Path Offset (inset/outset)
- [x] Path Division (knife tool)
- [ ] Contour (parallel outlines)
  - [ ] Number of contours
  - [ ] Spacing and color progression
- [ ] Scissors Tool (cut at point)
- [ ] Path Effects (non-destructive)
  - [ ] Zig-zag
  - [ ] Wave/sine
  - [ ] Roughen
  - [ ] Round corners
  - [ ] Dashes to path
- [ ] Envelope Distort
  - [ ] Preset envelopes (arc, bulge, flag, wave)
  - [ ] Custom mesh
  - [ ] Make with warp/mesh/top object
- [ ] Pattern Along Path
- [ ] Blend Tool (morph between shapes)
  - [ ] Specified steps/distance
  - [ ] Smooth color transition
  - [ ] Custom spine
- [ ] Live Paint (isolated fills)
  - [ ] Paint Bucket tool
  - [ ] Gap detection
- [ ] Perspective Distort
  - [ ] 1-point, 2-point perspective
  - [ ] Free distort
- [ ] 3D Effects
  - [ ] Extrude & bevel
  - [ ] Revolve
  - [ ] Rotate in 3D
  - [ ] Map artwork to surfaces
- [ ] Mesh Tool
  - [ ] Create mesh from shape
  - [ ] Color mesh points

## 4.4 Clipping & Masking
- [ ] **Clipping Paths**
  - [ ] Set as clipping mask
  - [ ] Release clipping mask
  - [ ] Edit clip path
  - [ ] Nested clipping
- [ ] **Opacity Masks**
  - [ ] Grayscale mask
  - [ ] Alpha mask
  - [ ] Invert mask
  - [ ] Edit mask mode
- [ ] **Compound Paths**
  - [ ] Make compound path
  - [ ] Release compound
  - [ ] Winding rule (even-odd/non-zero)

## 4.5 Symbols & Components
- [x] Create symbol from selection
- [x] Symbol library panel (grid, search, categories)
- [x] Symbol instances on canvas
- [x] Edit master symbol (updates all)
- [x] Override instance properties
- [ ] Symbol sets (organize related symbols)
- [ ] 9-slice scaling for symbols
- [ ] Symbol sprayer tool
  - [ ] Density, size variation
  - [ ] Symbol stainer, sizer, shifter
- [ ] Dynamic symbols (parameter overrides)

## 4.6 Artboards
- [x] Multiple artboards per document
- [x] Artboard tool (create/resize)
- [x] Artboard properties (name, size, background)
- [x] Artboard list in Layers panel
- [x] Export individual artboards
- [x] Artboard navigation
- [ ] Artboard presets (device sizes)
- [ ] Copy artboards with contents
- [ ] Duplicate artboard
- [ ] Artboard grid (arrange artboards)
- [ ] Fit artboard to artwork
- [ ] Artboard rulers

## 4.7 Object Management
- [ ] **Object Manager Panel**
  - [ ] Full object list (not just layers)
  - [ ] Search/filter objects
  - [ ] Batch select by type
  - [ ] Batch property edit
- [ ] **Find & Replace Objects**
  - [ ] Find by color
  - [ ] Find by stroke
  - [ ] Find by font
  - [ ] Replace properties
- [ ] **Select Same**
  - [ ] Same fill
  - [ ] Same stroke
  - [ ] Same opacity
  - [ ] Same type
- [ ] Object locking (by type, layer)
- [ ] Object hiding (by type, layer)

---

# PHASE 5: Advanced UI/UX

## 5.1 Theming & Branding
- [x] Dark theme (Catppuccin Mocha)
- [x] Light theme (Catppuccin Latte)
- [x] Accent color customization
- [ ] Custom icon set (Phosphor/Lucide, 200+)
- [ ] Animated splash screen
- [ ] About dialog (version, credits, links)
- [ ] Custom theme creator

## 5.2 Motion & Polish
- [x] Mica window backdrop
- [x] Panel slide/fade animations
- [x] Micro-interactions (button scale, hover effects)
- [x] Glassmorphism for floating panels
- [x] Smooth zoom animation
- [x] Pan momentum/inertia
- [x] Selection box animation
- [x] Toast notifications
- [x] Dialog animations
- [ ] Skeleton loading states
- [ ] Smooth scrolling everywhere

## 5.3 Command Palette (Ctrl+K)
- [x] Overlay search for commands
- [x] Fuzzy search with highlighting
- [x] Index all commands, tools, settings
- [x] Recent commands history
- [x] Keyboard shortcuts inline
- [x] Quick file open
- [ ] Actions (like VS Code: > prefix)
- [ ] Go to line in code
- [ ] Go to element by name

## 5.4 On-Canvas HUD
- [x] Contextual toolbar near selection
- [x] Quick actions (Boolean, Group, Color)
- [x] Distance indicators (Alt key)
- [x] Tooltip with element info on hover
- [x] Zoom level indicator
- [x] Selection info bar
- [x] Ruler tick marks at cursor
- [ ] Smart dimensions while dragging
- [ ] Color preview swatch
- [ ] Quick property edit popups

## 5.5 Keyboard Shortcuts
- [x] Central shortcut registry
- [x] Customizable shortcut editor
- [x] Preset profiles (Illustrator, Inkscape, Figma)
- [x] Cheat sheet overlay (Ctrl+/)
- [x] Conflict detection
- [x] Export/import shortcuts
- [ ] Touch Bar support (if applicable)
- [ ] Gesture shortcuts

## 5.6 Code Integration (Monaco)
- [x] WebView2 with Monaco
- [x] Monaco files hosted locally
- [x] C# ↔ JS bridge (SetContent, GetContent, OnChange)
- [x] SVG/XML syntax highlighting
- [x] Code folding, line numbers, minimap
- [x] Error highlighting (invalid XML)
- [x] Bi-directional sync (Canvas ↔ Code)
- [x] Hover to highlight (code → canvas)
- [x] Click to navigate (canvas → code)
- [x] Format/Prettify
- [ ] AvalonEdit fallback (no WebView2)
- [ ] Autocomplete for SVG elements/attributes
- [ ] Snippets

## 5.7 Navigator Panel
- [ ] Minimap of entire canvas
- [ ] Viewport rectangle (draggable)
- [ ] Quick zoom controls
- [ ] Zoom to selection
- [ ] Zoom history

---

# PHASE 6: Brushes & Artistic Tools

## 6.1 Brush System
- [ ] Brush library panel
  - [ ] Built-in brushes
  - [ ] Custom brush creation
  - [ ] Categories, search
- [ ] **Calligraphic Brush**
  - [ ] Angle, roundness
  - [ ] Pressure sensitivity
- [ ] **Scatter Brush**
  - [ ] Scatter amount
  - [ ] Rotation/scale variation
  - [ ] Spacing
- [ ] **Art Brush** (stretch along path)
- [ ] **Pattern Brush** (repeat along path)
  - [ ] Start/end/corner tiles
- [ ] **Bristle Brush**
  - [ ] Shape, length, density, stiffness
- [ ] **Blob Brush** (paint filled shapes)

## 6.2 Artistic Effects
- [ ] Pencil Tool (freehand with smoothing)
- [ ] Paintbrush Tool
- [ ] Shaper Tool (auto-recognize shapes)
- [ ] Width Tool (variable stroke width)
- [ ] Smooth Tool
- [ ] Path Eraser Tool
- [ ] Symbol Sprayer
  - [ ] Stainer, sizer, shifter, spinner

## 6.3 Patterns & Textures
- [ ] Pattern maker
  - [ ] Seamless patterns
  - [ ] Tile types (grid, brick, hex)
  - [ ] Preview tiled
- [ ] Halftone generator (dots, lines)
- [ ] Texture fills (noise, grain, paper)
- [ ] Live Trace (bitmap to vector)
  - [ ] Presets: photo, logo, line art
  - [ ] Custom settings
  - [ ] Preview, expand result

---

# PHASE 7: AI & Automation

## 7.1 Generative AI
- [ ] Text to Icon generator (DALL-E 3 / local model)
  - [ ] Style selection (flat, outline, 3D)
  - [ ] Multiple results
  - [ ] Variation generator
- [ ] Vectorize Bitmap (image trace)
  - [ ] Threshold/detail controls
  - [ ] Color simplification
  - [ ] Mode presets
- [ ] Generate from Reference (style transfer)
  - [ ] Color palette extraction
  - [ ] Style extraction

## 7.2 Smart Assist
- [ ] Auto-Name Layers (AI analysis)
- [ ] Generate Pattern from selection
- [ ] Suggest Colors (AI palette)
- [ ] Complete Shape (AI prediction)
- [ ] Auto-Align suggestions
- [ ] Similar Element Finder
- [ ] Auto Layout suggestions
- [ ] Accessibility Suggestions

## 7.3 Optimization
- [ ] Analyze SVG panel
  - [ ] File size, element count
  - [ ] Complexity score
  - [ ] Issues list
- [ ] Optimize button (SVGO-like)
  - [ ] Remove hidden elements
  - [ ] Merge paths
  - [ ] Round coordinates
  - [ ] Remove metadata
- [ ] Before/after preview
- [ ] Optimization presets

## 7.4 Automation
- [ ] Actions Panel
  - [ ] Record actions
  - [ ] Play actions
  - [ ] Edit steps
  - [ ] Save/load action sets
- [ ] Batch Processing
  - [ ] Apply to multiple files
  - [ ] Progress indicator
- [ ] Scripting (JavaScript)
  - [ ] Script editor panel
  - [ ] API documentation
  - [ ] Script library
- [ ] Plugin System
  - [ ] Plugin API (tools, panels, filters, export)
  - [ ] Plugin manager

---

# PHASE 8: Grids & Perspective

## 8.1 Advanced Grids
- [ ] Perspective Grid
  - [ ] 1-point, 2-point, 3-point
  - [ ] Custom vanishing points
  - [ ] Draw on perspective planes
  - [ ] Snap to perspective
- [ ] Isometric Grid
  - [ ] 30° preset
  - [ ] Custom angles
  - [ ] Snap to isometric
- [ ] Polar Grid (concentric circles + radials)
- [ ] Modular Grid
  - [ ] Columns, rows, gutters
  - [ ] Margins
  - [ ] Grid presets

## 8.2 Pixel Perfect Mode
- [ ] Pixel preview (1x render)
- [ ] Pixel grid at high zoom
- [ ] Snap to pixel
- [ ] Align to pixel grid command
- [ ] Half-pixel stroke adjustment
- [ ] Crisp edges option

---

# PHASE 9: Print & Prepress

## 9.1 Print Features
- [ ] Print preview
  - [ ] Page setup
  - [ ] Tile large artwork
  - [ ] Scale to fit
- [ ] Print dialog
  - [ ] Printer selection
  - [ ] Color management
  - [ ] Copies, page range

## 9.2 Color Management
- [ ] ICC color profiles
  - [ ] Assign profile
  - [ ] Convert to profile
  - [ ] Proof colors
- [ ] CMYK mode
  - [ ] CMYK color picker
  - [ ] Out-of-gamut warning
- [ ] Spot colors (Pantone)
- [ ] Overprint preview
- [ ] Ink coverage analysis

## 9.3 Prepress
- [ ] Crop marks
- [ ] Registration marks
- [ ] Color bars
- [ ] Page information
- [ ] Bleed setup
- [ ] Trim marks, fold marks
- [ ] Color separations preview
- [ ] Trapping settings
- [ ] Flatten transparency
- [ ] PDF/X export

---

# PHASE 10: Import/Export

## 10.1 File Operations
- [x] New document wizard (presets, custom, units)
- [x] Open recent files (last 10, clear)
- [x] Auto-save drafts (every 2 min)
- [x] Document recovery on crash
- [ ] Templates (create, save, browse)
- [ ] Place linked files
- [ ] Update links

## 10.2 Import Formats
- [x] SVG (primary)
- [x] AI (Adobe Illustrator) — basic
- [x] EPS — basic
- [x] PDF (vector extraction)
- [x] PNG/JPG (embedded image)
- [x] Clipboard paste (image, SVG)
- [ ] Figma import (experimental)
- [ ] Sketch import (experimental)
- [ ] XD import (experimental)
- [ ] DXF/DWG (CAD)
- [ ] WMF/EMF (Windows Metafile)
- [ ] CorelDRAW CDR (experimental)

## 10.3 Export Formats
- [x] SVG (optimized, minified)
- [x] PNG (transparency, DPI, scale)
- [x] JPG (quality slider)
- [x] PDF (vector)
- [x] XAML (WPF resource)
- [x] React/Vue component
- [x] CSS clip-path
- [x] ICO (multi-resolution)
- [x] WebP
- [ ] GIF (animated SVG)
- [ ] TIFF
- [ ] BMP
- [ ] EMF/WMF
- [ ] EPS
- [ ] Lottie JSON (animated)
- [ ] Android Vector Drawable
- [ ] iOS Asset Catalog

## 10.4 Export Dialog
- [x] Format selection
- [x] Preview
- [x] Size options
- [x] Quality options
- [x] Filename template
- [x] Export all artboards
- [x] Batch export
- [ ] Export presets (save settings)
- [ ] Slice tool (define export areas)
- [ ] Asset export (like Figma)

## 10.5 Asset Management
- [x] Built-in icon library
- [x] Template gallery
- [x] User asset library
- [ ] Stock integrations (Unsplash, Noun Project)
- [ ] Google Fonts integration
- [ ] Asset tagging and search

---

# PHASE 11: Settings & Preferences

## 11.1 Settings Dialog
- [ ] **General**
  - [ ] Language
  - [ ] Auto-save interval
  - [ ] Recent files count
  - [ ] Default units (px, mm, in, pt)
  - [ ] Startup behavior
- [ ] **Appearance**
  - [ ] Theme (dark/light/system)
  - [ ] Accent color
  - [ ] Interface scale
  - [ ] Font size
- [ ] **Canvas**
  - [ ] Default canvas size
  - [ ] Background color
  - [ ] Grid size and color
  - [ ] Snap tolerance
- [ ] **Tools**
  - [ ] Default fill color
  - [ ] Default stroke color/width
  - [ ] Pen tool behavior
- [ ] **Export**
  - [ ] Default format
  - [ ] Default quality
  - [ ] Default location
- [ ] **Performance**
  - [ ] GPU acceleration
  - [ ] Memory limit
  - [ ] Cache size
- [ ] **Keyboard Shortcuts**
  - [ ] Shortcut editor
  - [ ] Import/export

## 11.2 Settings Storage
- [ ] JSON settings file
- [ ] User AppData location
- [ ] Migrate settings on update
- [ ] Reset to defaults
- [ ] Export/import settings

---

# PHASE 12: Performance & Stability

## 12.1 Performance
- [ ] R-Tree spatial index (fast hit-testing)
- [ ] Render caching (static layers to bitmaps)
- [ ] Lazy rendering (visible area only)
- [ ] Worker threads for expensive ops
- [ ] Memory profiling
- [ ] Startup optimization
- [ ] Virtualized lists (layers, assets)
- [ ] Throttled rendering during pan/zoom

## 12.2 Error Handling
- [x] Global exception handler
- [x] User-friendly error dialogs
- [x] Stack trace (hidden, copyable)
- [ ] Crash reporter (optional telemetry)
- [ ] Log file rotation (last 5, max size)
- [ ] Error recovery (auto-save before crash)

## 12.3 Testing
- [ ] Unit tests for Core services (80% coverage)
- [ ] Integration tests for import/export
- [ ] UI automation tests
- [ ] Performance benchmarks
- [ ] Regression test suite

---

# PHASE 13: Accessibility & Localization

## 13.1 Accessibility
- [ ] Screen reader support (UI Automation)
  - [ ] All controls labeled
  - [ ] Correct reading order
  - [ ] Live regions for updates
- [ ] High contrast mode
- [ ] Keyboard navigation for canvas
  - [ ] Tab through elements
  - [ ] Arrow keys to move
- [ ] Focus indicators
- [ ] Reduced motion option
- [ ] Font size scaling
- [ ] Color blind friendly themes

## 13.2 Localization
- [ ] Externalize all strings to resources
- [ ] English (default)
- [ ] Spanish, French, German
- [ ] RTL layout support
- [ ] Date/number formatting
- [ ] Community translation system

---

# PHASE 14: Distribution

## 14.1 Packaging
- [ ] MSIX installer
- [ ] Portable ZIP
- [ ] Microsoft Store submission
- [ ] Chocolatey package
- [ ] WinGet package

## 14.2 Updates
- [ ] Auto-updater (check on startup)
- [ ] Download in background
- [ ] Release notes dialog
- [ ] Changelog in-app

## 14.3 Marketing
- [ ] Landing page (bezier.app)
- [ ] Demo video (60-90 sec)
- [ ] Product Hunt launch
- [ ] GitHub Awesome lists
- [ ] Social media presence

---

# PHASE 15: Developer Tools

## 15.1 Debug Window
- [x] Separate window (F12)
- [x] Always on top option
- [x] Persistent across sessions

## 15.2 Console Tab
- [x] Real-time logs (color-coded levels)
- [x] Timestamp, category filtering
- [x] Search/filter, clear
- [x] Copy/export logs
- [x] Auto-scroll toggle

## 15.3 Coordinates Tab
- [x] Mouse coordinates (screen, document, artboard)
- [x] Selected element info (position, size, transform, fill, stroke)
- [x] Canvas state (zoom, pan, viewport)
- [x] Copy all info
- [x] Live update toggle

## 15.4 Elements Inspector
- [x] Tree view of document elements
- [x] Select element in canvas from tree
- [x] Highlight on hover
- [x] Show/hide visibility
- [x] Lock/unlock
- [x] View raw SVG

## 15.5 Performance Tab
- [x] Frame rate, render time
- [x] Memory usage
- [x] Element count
- [x] Undo/redo stack size

## 15.6 Crash Handling
- [x] Global unhandled exception handler
- [x] Exception dialog (type, message, stack trace)
- [x] Copy exception, continue or exit
- [ ] Crash log file
- [ ] Recovery options

---

# PHASE 16: Collaboration

## 16.1 Comments & Annotations
- [ ] Comment tool (pin to elements)
- [ ] Comment panel (list, filter, resolve)
- [ ] Markup tools (arrows, callouts, highlights)

## 16.2 Version Control
- [ ] Built-in version history
  - [ ] Auto-save versions
  - [ ] Named versions
  - [ ] Compare, restore
- [ ] Git integration
  - [ ] Initialize, commit, diff
  - [ ] Branch management
- [ ] File comparison view

## 16.3 Cloud (Optional)
- [ ] Cloud storage (save, auto-sync)
- [ ] Team libraries (symbols, styles, colors)
- [ ] Real-time collaboration (future)
  - [ ] Cursors, live edits, presence

---

# PHASE 17: Beyond The Competition
> *Innovative features that set Bezier apart*

## 17.1 Parametric Design
- [ ] Parametric shapes (define parameters, sliders)
- [ ] Repeat grids (edit one to update all)
- [ ] Procedural generators
  - [ ] Generative patterns
  - [ ] Math-based shapes
  - [ ] Fractals, L-systems

## 17.2 Constraint-Based Design
- [ ] Constraints panel (pin edges, aspect ratio, min/max)
- [ ] Responsive artboards (breakpoints)
- [ ] Smart layout (auto-layout containers, stack, wrap)

## 17.3 Design Tokens
- [ ] Design tokens panel (colors, sizes, spacing, typography)
- [ ] Token aliases (semantic naming)
- [ ] Theme switching (swap token values)
- [ ] Export tokens (JSON, CSS variables)
- [ ] Import tokens (Figma, Tokens Studio)

## 17.4 Animation Timeline
- [ ] Animation panel (timeline, keyframes, easing)
- [ ] Animate properties (position, scale, rotation, opacity, fill, path morph)
- [ ] Export animated SVG (CSS, SMIL, Lottie)
- [ ] Preview animation

## 17.5 Component Variants
- [ ] Components with variants (size, state)
- [ ] Interactive components (hover, pressed, disabled, focused)
- [ ] Slot overrides (nested placeholders)

## 17.6 Accessibility Checker
- [ ] Color contrast checker (WCAG AA/AAA)
- [ ] Touch target size checker
- [ ] Text size recommendations
- [ ] Alt text for images
- [ ] Auto-fix suggestions
- [ ] Export accessibility report

## 17.7 Developer Handoff
- [ ] Inspect mode (click to see properties)
- [ ] Copy CSS, dimensions, assets
- [ ] Design specs export (HTML inspection page)
- [ ] Code generation (React, Vue, SwiftUI, Flutter, XAML)

## 17.8 Advanced Selection
- [ ] Select by property (fill, stroke, font, size)
- [ ] Find and replace properties
- [ ] Global edit mode (edit all instances at once)

## 17.9 Integrations
- [ ] Figma import (experimental)
- [ ] Sketch import (experimental)
- [ ] Canva asset import
- [ ] Noun Project integration
- [ ] Unsplash integration
- [ ] Google Fonts integration

---

# Priority Order

## Immediate (Weeks 1-2)
1. **Phase 0** — Foundation, UI Shell, Menus, Toolbar

## Core Development (Weeks 3-8)
2. **Phase 1** — Core Rendering Engine
3. **Phase 2** — Editor Architecture
4. **Phase 3** — Drawing & Editing Tools

## Feature Complete (Weeks 9-14)
5. **Phase 4** — Professional Features
6. **Phase 5** — Advanced UI/UX
7. **Phase 6** — Brushes & Artistic Tools

## Professional Polish (Weeks 15-20)
8. **Phase 7** — AI & Automation
9. **Phase 8** — Grids & Perspective
10. **Phase 9** — Print & Prepress
11. **Phase 10** — Import/Export
12. **Phase 11** — Settings & Preferences

## Release Preparation (Weeks 21-24)
13. **Phase 12** — Performance & Stability
14. **Phase 13** — Accessibility & Localization
15. **Phase 14** — Distribution
16. **Phase 15** — Developer Tools

## Post-Launch (Ongoing)
17. **Phase 16** — Collaboration
18. **Phase 17** — Beyond The Competition

---

# Feature Comparison Matrix

| Feature | Bezier | Illustrator | CorelDRAW | Inkscape | Figma |
|---------|--------|-------------|-----------|----------|-------|
| **Core Vector Editing** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **SVG-First Workflow** | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ |
| **Live Code Sync** | ✅ | ❌ | ❌ | ⚠️ | ❌ |
| **Monaco Code Editor** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Mica/Fluent Design** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Command Palette** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Design Tokens** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Animation Timeline** | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **Parametric Shapes** | ✅ | ❌ | ❌ | ⚠️ | ❌ |
| **Component Variants** | ✅ | ⚠️ | ❌ | ❌ | ✅ |
| **Accessibility Checker** | ✅ | ❌ | ❌ | ❌ | ⚠️ |
| **Git Integration** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Developer Handoff** | ✅ | ⚠️ | ❌ | ❌ | ✅ |
| **AI Generation** | ✅ | ✅ | ⚠️ | ❌ | ✅ |
| **CMYK/Print** | ✅ | ✅ | ✅ | ⚠️ | ❌ |
| **Scripting/Plugins** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Real-time Collab** | 🔜 | ❌ | ❌ | ❌ | ✅ |
| **Open Source** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Cross-Platform** | 🔜 | ✅ | ❌ | ✅ | ✅ |
| **Free** | ✅ | ❌ | ❌ | ✅ | ⚠️ |
| **Offline** | ✅ | ✅ | ✅ | ✅ | ⚠️ |

Legend: ✅ Full | ⚠️ Limited | ❌ No | 🔜 Planned

---

# Unique Selling Points (Bezier Differentiators)

1. **SVG-Native** — Built from ground up for SVG, not adapted from proprietary formats
2. **Live Code Sync** — Monaco editor with bi-directional canvas ↔ code sync
3. **Modern Windows UX** — Mica backdrop, Fluent Design, dark-first
4. **Open Source** — Free forever, community-driven, no vendor lock-in
5. **Developer-Friendly** — Code export (React, Vue, XAML), design tokens, Git integration
6. **AI-Powered** — Text-to-icon, smart trace, auto-name, color suggestions
7. **Parametric Design** — Constraint-based, responsive artboards, repeat grids
8. **Accessibility Built-In** — WCAG checker, screen reader support, high contrast
9. **Lightweight** — Fast startup, low memory, no bloat
10. **Extensible** — Plugin system, scripting, open API

---

*Last Updated: 2025-01-14*
