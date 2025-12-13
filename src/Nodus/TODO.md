# Bezier - Production Roadmap

> **Vision**: A production-ready SVG editor that rivals Inkscape, Figma, Illustrator, and CorelDRAW.

## 🤖 Prompt Template
```
Continue developing Bezier SVG Editor. Focus on: [PHASE NUMBER]
Reference this file for context and mark completed items with [x].
Follow coding standards in STANDARDS.md (.NET 10 / C# 14 best practices).
Ensure code follows the project structure:
- Bezier.Core: Domain models, interfaces, pure logic
- Bezier.Desktop: WPF UI, SkiaSharp rendering, Services
- Bezier.Tests: Unit and integration tests

After completing each task set:
1. Build: dotnet build Bezier.sln
2. Run: dotnet run --project Bezier.Desktop
3. Commit: git add -A; git commit -m "feat: [description]"
4. Push: git push origin master
```

---

## Technology Decisions

### Code Editor: AvalonEdit vs Monaco

| Feature | AvalonEdit | Monaco (WebView2) |
|---------|------------|-------------------|
| **Integration** | Native WPF, simple | WebView2 interop required |
| **Performance** | Excellent, native | Good, but WebView overhead |
| **Syntax Highlighting** | Good (custom XSHD) | Excellent (built-in SVG/XML) |
| **IntelliSense/Autocomplete** | Manual implementation | Built-in, extensible |
| **Minimap** | No | Yes |
| **Multi-cursor** | Limited | Yes |
| **Code Folding** | Yes | Yes |
| **Find & Replace** | Basic | Advanced (regex, in selection) |
| **Theming** | Manual styling | VS Code themes supported |
| **Memory Footprint** | Small (~5MB) | Larger (~50MB) |
| **Startup Time** | Instant | 1-2 seconds |

**Decision**: Use **Monaco Editor** for production quality. The WebView2 overhead is acceptable for the significantly better feature set. AvalonEdit can be kept as a fallback for systems without WebView2 runtime.

### WebView2 Deployment Strategy
- **Fixed Version** runtime bundled with application (~150MB)
- Self-contained: No internet required, works offline
- Download: [WebView2 Fixed Version Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
- Set `browserExecutableFolder` in code to bundled runtime path

### Rendering: SkiaSharp + Svg.Skia
- SkiaSharp provides GPU-accelerated 2D rendering
- Svg.Skia handles accurate SVG parsing with full spec compliance
- WriteableBitmap integration for WPF display

### UI Framework: WPF + WPF-UI + AvalonDock
- WPF-UI for Fluent Design / Mica effects
- AvalonDock (dirkster99 fork) for dockable panels
- XamlFlair for fluid animations

---

## Phase 0: Foundation & Setup

### 0.1 Solution Architecture
- [x] Create `Bezier.sln` with proper separation of concerns
- [x] Project: `Bezier.Core` (.NET 9 Class Library) - *The "Brain"*
  - [x] Create project with `dotnet new classlib`
  - [x] Models (VectorElement, VectorDocument)
  - [x] Interfaces (IFill, IEditorCommand)
- [x] Project: `Bezier.Desktop` (.NET 10 WPF) - *The "Face"*
  - [x] Create project with `dotnet new wpf`
  - [x] MVVM structure (ViewModels, Views)
  - [x] Custom Controls
- [x] Project: `Bezier.Tests` (xUnit)
  - [x] Create project with `dotnet new xunit`
  - [x] Add reference to Bezier.Core
- [x] Set up Dependency Injection (Microsoft.Extensions.DependencyInjection)
  - [x] Create `ServiceCollectionExtensions.cs`
  - [x] Register all services in `App.xaml.cs`

### 0.2 Folder Structure
- [x] `Bezier.Core/Models/` - Domain entities
- [x] `Bezier.Core/Models/Elements/` - VectorElement subclasses
- [x] `Bezier.Core/Models/Fills/` - Fill types
- [x] `Bezier.Core/Interfaces/` - Contracts
- [x] `Bezier.Core/Services/` - Business logic
- [x] `Bezier.Core/Commands/` - Editor commands
- [x] `Bezier.Desktop/Views/` - XAML views
- [x] `Bezier.Desktop/Views/Panels/` - Dockable panels
- [x] `Bezier.Desktop/Views/Dialogs/` - Modal dialogs
- [x] `Bezier.Desktop/ViewModels/` - VM classes
- [x] `Bezier.Desktop/Controls/` - Custom WPF controls
- [x] `Bezier.Desktop/Controls/Canvas/` - SkiaCanvas control
- [x] `Bezier.Desktop/Controls/ColorPicker/` - Color picker control
- [x] `Bezier.Desktop/Resources/` - Icons, styles, themes
- [x] `Bezier.Desktop/Resources/Icons/` - SVG/XAML icons
- [x] `Bezier.Desktop/Resources/Themes/` - Light/Dark themes
- [x] `Bezier.Desktop/Assets/` - Fonts, images
- [x] `Bezier.Desktop/Assets/Fonts/` - Custom fonts
- [x] `Bezier.Desktop/Services/` - Desktop-specific services

### 0.3 Version Control & CI
- [x] Initialize Git repository with `.gitignore` (Visual Studio template)
- [x] Create `README.md` with project overview and screenshots
- [x] Create `CONTRIBUTING.md` with code style guidelines
- [x] Create `LICENSE` file (MIT or similar)
- [x] Create `.editorconfig` for code formatting
- [x] Create `.github/workflows/build.yml` for automated CI builds
  - [x] Build on push/PR
  - [x] Run tests
  - [x] Create artifacts
- [x] Set up `dependabot.yml` for NuGet updates
- [ ] Configure branch protection rules
- [x] Create `CHANGELOG.md`

### 0.4 Core Dependencies
- [x] Install `SkiaSharp` & `SkiaSharp.Views.WPF` (Rendering)
- [x] Install `Svg.Skia` (SVG Parsing)
- [x] Install `Dirkster.AvalonDock` (Docking Layout)
- [x] Install `CommunityToolkit.Mvvm` (MVVM)
- [x] Install `Microsoft.Web.WebView2` (Monaco)
- [x] ~~Install `XamlFlair`~~ → Using native WPF Storyboards + AnimationHelper.cs
- [x] Install `WPF-UI` (Fluent Design / Mica)
- [x] Install `Serilog` (Logging)
- [x] Install `Serilog.Sinks.File` (Log to file)
- [x] Install `Newtonsoft.Json` (Settings serialization)
- [x] Install `Microsoft.Extensions.DependencyInjection` (DI)

### 0.5 Initial UI Shell (Early WOW Factor)
- [x] Create main window with Mica/Acrylic backdrop
  - [x] Set window style to None
  - [x] Implement custom chrome
  - [x] Add resize grips
- [x] Set up dark theme with custom color palette (Catppuccin Mocha)
  - [x] Define color resources in `Themes/Dark.xaml`
  - [x] Define brush resources
  - [x] Define control styles
- [x] Create app icon (multiple sizes: 16, 32, 48, 256)
- [x] Implement basic title bar
  - [x] App icon and name
  - [x] Minimize button
  - [x] Maximize/Restore button
  - [x] Close button
  - [x] Double-click to maximize
  - [x] Drag to move window
- [x] Add splash screen
  - [x] Logo animation (fade in, scale)
  - [x] Loading progress text
  - [x] Version number
- [x] Set up AvalonDock skeleton (empty panels)

### 0.6 Main Menu Bar
- [x] File menu
  - [x] New (Ctrl+N)
  - [x] Open (Ctrl+O)
  - [x] Open Recent >
  - [x] Save (Ctrl+S)
  - [x] Save As (Ctrl+Shift+S)
  - [x] Export >
  - [x] Close (Ctrl+W)
  - [x] Exit (Alt+F4)
- [x] Edit menu
  - [x] Undo (Ctrl+Z)
  - [x] Redo (Ctrl+Y)
  - [x] Cut (Ctrl+X)
  - [x] Copy (Ctrl+C)
  - [x] Paste (Ctrl+V)
  - [x] Duplicate (Ctrl+D)
  - [x] Delete (Del)
  - [x] Select All (Ctrl+A)
  - [x] Preferences/Settings
- [x] View menu
  - [x] Zoom In (Ctrl++)
  - [x] Zoom Out (Ctrl+-)
  - [x] Fit to Window (Ctrl+0)
  - [x] Actual Size (Ctrl+1)
  - [x] Show Grid (Ctrl+')
  - [x] Show Rulers
  - [x] Show Guides
  - [x] Outline Mode
  - [x] Panels submenu (toggle each panel)
- [x] Object menu
  - [x] Group (Ctrl+G)
  - [x] Ungroup (Ctrl+Shift+G)
  - [x] Bring to Front
  - [x] Send to Back
  - [x] Bring Forward
  - [x] Send Backward
  - [x] Align >
  - [x] Distribute >
  - [x] Transform >
- [x] Path menu
  - [x] Union
  - [x] Subtract
  - [x] Intersect
  - [x] Exclude
  - [x] Simplify
  - [x] Stroke to Path
  - [x] Text to Path
- [x] Help menu
  - [x] Documentation
  - [x] Keyboard Shortcuts
  - [x] About

### 0.7 Main Toolbar
- [x] New document button
- [x] Open button
- [x] Save button
- [x] Separator
- [x] Undo button
- [x] Redo button
- [x] Separator
- [x] Zoom dropdown
- [x] Fit to window button
- [x] Separator
- [x] Toggle grid
- [x] Toggle rulers
- [x] Toggle snap

---

## Phase 1: Core Engine & Rendering

### 1.1 The Data Model (Bezier.Core)
- [x] Define `VectorDocument` (root object)
  - [x] Add `Width`, `Height`, `ViewBox` properties
  - [ ] Add `Layers` collection
  - [x] Add `Metadata` (title, author, license, description)
  - [ ] Add `Defs` collection (gradients, patterns, symbols)
  - [x] Add `IsDirty` property for unsaved changes
  - [x] Implement `INotifyPropertyChanged`
- [x] Define abstract `VectorElement` base class
  - [x] Add `Id` (GUID)
  - [x] Add `Name` (user-facing label)
  - [x] Add `IsVisible`, `IsLocked` properties
  - [x] Add `Opacity` property (0-1)
  - [x] Add `BlendMode` property (enum)
  - [x] Add `Transform` property
  - [x] Add `Parent` reference
  - [x] Add `Fill` property (IFill)
  - [x] Add `Stroke` property
  - [x] Implement `INotifyPropertyChanged`
- [x] Implement `SvgPath` (with `PathData` string)
  - [ ] Parse path data to segments
  - [ ] Get/set individual nodes
- [x] Implement `SvgRect` (x, y, width, height, rx, ry)
- [x] Implement `SvgCircle` (cx, cy, r)
- [x] Implement `SvgEllipse` (cx, cy, rx, ry)
- [x] Implement `SvgLine` (x1, y1, x2, y2)
- [x] Implement `SvgPolygon` / `SvgPolyline`
- [x] Implement `SvgText` (with font properties)
  - [x] FontFamily, FontSize, FontWeight, FontStyle
  - [x] TextAnchor, DominantBaseline
- [x] Implement `SvgImage` (embedded/linked raster)
  - [x] Base64 embedded data
  - [x] External href
- [x] Implement `SvgGroup` (container with children)
  - [x] Children collection
  - [ ] Recursive transform
- [x] Implement `Transform` struct (Matrix 3x3: translate, rotate, scale, skew)
  - [x] Multiply method
  - [x] Invert method
  - [x] TransformPoint method
- [x] Add `HitTest(Point)` virtual methods to elements
- [x] Implement `BoundingBox` calculation with transform support
- [x] Implement `Clone()` method for deep copy
- [x] Implement `ToSvgString()` for each element

### 1.2 Fill & Stroke System
- [x] Define `IFill` interface
  - [x] `ToSkiaPaint()` method (via FillConverter extension in Desktop)
  - [x] `Clone()` method
- [x] Implement `NoneFill` (transparent)
- [x] Implement `SolidFill` (color)
  - [x] RGBA color
  - [x] Opacity
- [x] Implement `LinearGradientFill` (stops, angle)
  - [x] Start/End points
  - [x] GradientStops collection
  - [x] SpreadMode (pad, reflect, repeat)
- [x] Implement `RadialGradientFill` (stops, center, radius)
  - [x] Center point
  - [x] Radius
  - [x] Focal point
  - [x] GradientStops collection
- [x] Implement `PatternFill` (tiled element reference)
- [x] Define `Stroke` class
  - [x] Width
  - [x] Color/Fill
  - [x] Dash array
  - [x] Dash offset
  - [x] Line cap (butt, round, square)
  - [x] Line join (miter, round, bevel)
  - [x] Miter limit
- [x] Implement `StrokeConverter` (via StrokeConverter extension in Desktop)

### 1.3 SkiaSharp Rendering System
- [x] Create `SkiaCanvas` WPF control (inherits `SKElement`)
  - [x] Override `OnPaintSurface`
  - [x] Handle mouse events
  - [x] Handle keyboard events
- [x] Implement `RenderLoop` (InvalidateVisual on changes) with 60fps target
  - [x] Dirty flag optimization
  - [x] Render on demand
- [x] Create `SkiaRenderer` service translating Domain Models -> Skia Draw Calls
  - [x] Render VectorDocument
  - [x] Render each element type
  - [x] Apply transforms
  - [x] Apply fills and strokes
- [x] Implement infinite canvas: Pan (Translate) and Zoom (Scale) logic
  - [x] Store viewTransform matrix
  - [x] Mouse wheel zoom (center on cursor)
  - [x] Pan with middle mouse or spacebar+drag
  - [x] Smooth animated zoom
- [x] Add Grid rendering (Adaptive: dots/lines fade in/out based on zoom)
  - [x] Minor grid lines
  - [x] Major grid lines
  - [x] Grid origin indicator
- [x] Add Rulers rendering (Canvas-aligned, independent of zoom)
  - [x] Horizontal ruler
  - [x] Vertical ruler
  - [x] Cursor position indicator on rulers
  - [x] Tick marks and labels
- [x] Implement "Pixel Preview" mode (show actual pixels at high zoom)
- [x] Implement "Outline Mode" (wireframe view, no fills)
- [x] Implement background rendering
  - [x] Checkerboard pattern (transparency)
  - [x] Solid color option
  - [x] Artboard background

### 1.4 SVG Bridge
- [x] Implement `SvgImporter`: Clean SVG -> `VectorDocument`
  - [x] Parse root `<svg>` attributes
  - [x] Handle namespaces (inkscape, sodipodi)
  - [x] Preserve IDs
  - [x] Handle `<defs>` and gradients
  - [x] Handle `<use>` (symbol instances) - partial, creates placeholder
  - [ ] Handle `<clipPath>` and `<mask>`
  - [x] Handle CSS styles
  - [x] Handle inline styles
  - [x] Error handling for invalid SVG
- [x] Implement `SvgExporter`: `VectorDocument` -> Optimized SVG string
  - [x] Generate valid SVG 1.1
  - [x] Minify output option
  - [x] Inline styles vs. CSS classes option
  - [x] Preserve IDs option
  - [x] Include viewBox
- [x] Verify rigorous round-trip fidelity (Load -> Save -> Load)

### 1.5 Phase 1 UI Polish
- [x] Status bar with zoom level and cursor position
  - [x] Zoom percentage display
  - [x] X, Y cursor coordinates
  - [x] Selection info (count, dimensions)
  - [x] Document info (size, element count)
- [x] Zoom controls in toolbar (dropdown + fit buttons)
  - [x] Preset zoom levels (25%, 50%, 100%, 200%, etc.)
  - [x] Fit to window
  - [ ] Fit to selection
  - [x] Actual pixels
- [x] Pan/zoom with mouse wheel and drag (implemented in SkiaCanvas)
- [x] Loading indicator for large files
  - [x] Progress ring
  - [ ] Cancel button
- [x] Error toast for invalid SVG files
  - [ ] Slide-in animation
  - [x] Auto-dismiss after 5s
  - [x] Dismiss button
- [x] Keyboard shortcuts for common actions

---

## Phase 2: Editor Architecture

### 2.1 Undo/Redo System (Command Pattern)
- [x] Create `IEditorCommand` interface (not WPF ICommand)
  - [x] `Execute()` method
  - [x] `Undo()` method
  - [x] `Description` property (for UI display)
  - [x] `IsUndoable` property
- [x] Implement `HistoryManager` class (UndoStack, RedoStack)
  - [x] `CanUndo`, `CanRedo` observable properties
  - [x] `MaxHistorySize` setting
  - [x] `Clear()` method
  - [x] `HistoryChanged` event
- [x] Create core commands:
  - [x] `MoveCommand`
  - [x] `RotateCommand`
  - [x] `ScaleCommand`
  - [x] `PropertyChangeCommand`
  - [x] `AddElementCommand`
  - [x] `DeleteElementCommand`
  - [x] `ReorderCommand`
  - [x] `GroupCommand`
  - [x] `UngroupCommand`
  - [ ] `DuplicateCommand`
- [ ] Implement transaction/batching support (for continuous drag operations)
  - [ ] `BeginTransaction()`
  - [ ] `CommitTransaction()`
  - [ ] `RollbackTransaction()`
- [ ] Implement `MacroCommand` (group multiple commands)

### 2.2 Tool System
- [x] Define `ITool` interface
  - [x] `Name` property
  - [x] `Icon` property
  - [x] `Cursor` property
  - [x] `Shortcut` property
  - [x] `OnActivate()` method
  - [x] `OnDeactivate()` method
  - [x] `OnMouseDown(Point, Modifiers)`
  - [x] `OnMouseMove(Point, Modifiers)`
  - [x] `OnMouseUp(Point, Modifiers)`
  - [x] `OnKeyDown(Key, Modifiers)`
  - [x] `OnKeyUp(Key, Modifiers)`
  - [x] `RenderOverlay(Canvas)` for tool-specific guides
- [x] Implement `ToolManager` to handle active tool state and cursor changes
  - [x] `ActiveTool` property
  - [x] `SetTool(ITool)` method
  - [x] `Tools` collection
  - [x] Handle keyboard shortcuts for tool switching
- [x] Create `SelectTool` (Hit testing logic + Adorner rendering)
  - [x] Click to select
  - [x] Click empty to deselect
  - [x] Shift+Click to add to selection
  - [x] Ctrl+Click to toggle selection
  - [x] Drag to move selection
  - [x] Marquee selection
- [x] Create `PanTool` (Spacebar override, Middle-mouse drag)
- [x] Create `ZoomTool` (Ctrl+Scroll, Z key)
  - [x] Click to zoom in
  - [x] Alt+Click to zoom out
  - [x] Drag to zoom to area

### 2.3 Application Layout (AvalonDock)
- [x] Set up `DockingManager` in MainWindow with dark theme
  - [x] Configure AvalonDock theme
  - [x] Set default layout
- [x] Create `DocumentPane` (The Canvas)
  - [ ] Support multiple documents (tabs)
  - [ ] Tab header with filename and close button
  - [ ] Dirty indicator (asterisk)
  - [ ] "Close", "Close All", "Close Others" context menu
  - [ ] Drag tabs to reorder
  - [ ] Drag tab out to create new window
- [x] Create `AnchorablePane`s:
  - [x] Layers Panel (right, with element list)
  - [x] Properties Panel (right)
  - [x] Toolbox Panel (left, vertical icons)
  - [ ] Code Editor Panel (bottom)
  - [x] History Panel (Undo/Redo list)
  - [ ] Assets Panel (symbols, templates)
- [ ] Implement Save/Load layout state feature
  - [ ] Save to JSON on exit
  - [ ] Load on startup
- [x] Implement "Reset Layout" command
- [x] Implement "Window" menu with panel toggles

### 2.4 Selection Manager
- [x] Maintain `SelectedElements` observable collection
- [x] Implement selection change events
- [x] Compute aggregate bounding box for multi-selection
- [x] Handle selection during group/ungroup
- [x] Selection highlight rendering (via SelectTool)
- [x] Selection handles rendering (via SelectTool)

### 2.5 Phase 2 UI Polish
- [x] Toolbox icons with hover tooltips
  - [x] 24x24 icons
  - [x] Active tool highlight (orange border when selected)
  - [x] Tooltip with name and shortcut
- [x] Panel headers with collapse/expand animation
- [ ] Tab close button with hover effect
- [x] Keyboard shortcuts visible in menus
- [ ] Context menus with icons
- [ ] Drag handle visual for dockable panels

---

## Phase 3: Visual Editing Features

### 3.1 Selection & Transform
- [x] Implement Bounding Box rendering (Selection Adorner)
  - [x] Dashed border (2px, blue)
  - [x] Semi-transparent fill (10% opacity)
- [x] Implement Resize Handles (8 points) logic
  - [x] Corner handles
  - [x] Edge midpoint handles
  - [x] Proportional resize (Shift)
  - [x] Center resize (Alt)
  - [x] Cursor change on hover
- [x] Implement Rotate Handle logic
  - [x] Handle above center top
  - [x] 15° snap (Shift)
  - [x] Show angle tooltip
  - [x] Rotation cursor
- [ ] Implement Skew handles (optional Advanced mode)
- [x] Add Multi-select support
  - [x] Shift+Click to add/remove
  - [x] Ctrl+Click for toggle
  - [x] Marquee (lasso) selection
  - [x] Aggregate bounding box
- [ ] Implement "Deep Select" (Ctrl+Click to select in group)
- [ ] Implement "Select Same" (by fill, stroke, type)
- [x] Implement "Select All" (Ctrl+A)
- [ ] Implement "Invert Selection"

### 3.2 Basic Shape Tools
- [x] `RectangleTool`: Drag to create
  - [x] Shift for square
  - [x] Alt for center origin
  - [ ] Corner radius handle post-creation
  - [x] Live dimensions tooltip
- [x] `EllipseTool`: Center/Corner modes
  - [x] Shift for circle
  - [x] Live dimensions tooltip
- [x] `LineTool`: Simple two-point lines
  - [x] Shift for 45° snap
  - [x] Live length/angle tooltip
- [ ] `PolygonTool`: N-sided polygons
  - [ ] Options bar: number of sides (3-100)
  - [ ] Inner/outer radius for stars
- [ ] `StarTool`: N-pointed stars
  - [ ] Options bar: number of points
  - [ ] Inner/outer radius controls
- [ ] `SpiralTool`: Spiral paths
- [x] Live preview during creation (ghost shapes)
- [x] Default fill/stroke for new shapes

### 3.3 The Pen Tool (Bezier) - *The "Inkscape Killer"*
- [x] Implement Node/Control Point data structure
  - [x] `ControlPoint { Position, InHandle, OutHandle, Type }`
  - [x] Type: Corner, Smooth, Symmetric
- [x] Create `PenTool`:
  - [x] Click: Corner point
  - [x] Click+Drag: Smooth point (Quadratic/Cubic bezier)
  - [x] Alt+Drag: Break tangent (Cusp)
  - [x] Click on first point: Close path
  - [ ] Click on existing node: Select node
- [x] Implement path closing logic with magnetic snap
  - [x] Snap radius: 10px
  - [x] Visual indicator when in snap range
- [x] Render path preview ("rubber band") while drawing
- [x] Show angle/length tooltip while drawing
- [x] Escape to cancel current path
- [x] Enter to finish open path
- [x] Backspace to delete last point

### 3.4 Node Editing Tool
- [x] Select individual nodes on a path
  - [x] Click to select node
  - [x] Shift+Click to add to selection
  - [x] Marquee to select multiple nodes
- [x] Drag nodes to reshape
- [x] Drag control handles to adjust curvature
- [x] Convert node types (Corner <-> Smooth <-> Symmetric)
  - [x] Keyboard shortcut (1, 2, 3 keys)
  - [ ] Context menu
- [x] Add/Remove nodes on path segment
  - [ ] Double-click to add
  - [x] Delete key to remove
- [ ] "Simplify Path" command (reduce nodes)
- [ ] "Smooth Path" command (add curves)
- [ ] "Break Path" at node
- [ ] "Join Paths" command
- [ ] "Reverse Path" command

### 3.5 Text Tool
- [x] Click to create text block
- [x] Inline text editing on canvas
  - [x] Blinking cursor
  - [x] Text selection
  - [ ] Copy/paste (requires clipboard integration)
- [x] Font picker (family, weight, style)
  - [ ] System fonts list
  - [ ] Font preview
- [x] Font size, line height, letter spacing
- [x] Text alignment (left, center, right, justify)
- [ ] Text on path feature
  - [ ] Attach text to path
  - [ ] Offset along path
- [x] Text outline and fill

### 3.6 Guides & Snapping
- [x] Draggable guides from rulers
  - [x] Drag from ruler to create
  - [x] Drag guide to move
  - [x] Delete key or drag off canvas to remove
  - [ ] Double-click to set position numerically
- [x] Snap to grid
  - [x] Configurable grid size
  - [x] Grid visible toggle
- [x] Snap to guides
- [x] Snap to other objects (edges, centers)
- [x] Smart guides (alignment lines) when dragging
  - [x] Horizontal alignment
  - [x] Vertical alignment
  - [ ] Size matching
  - [ ] Spacing equalization
- [ ] Distance indicators (hold Alt)
- [x] Snap tolerance setting

### 3.7 Alignment & Distribution
- [x] Align left, center, right (horizontal)
- [x] Align top, middle, bottom (vertical)
- [x] Distribute horizontally (spacing)
- [x] Distribute vertically (spacing)
- [x] Align to canvas
- [x] Align to selection bounds
- [x] Align to key object

### 3.8 Phase 3 UI Polish
- [x] Tool options bar (context-sensitive, below toolbar)
  - [x] Shows options for active tool
  - [x] Number inputs, dropdowns, toggles
- [x] Cursor changes per tool
  - [x] Custom cursors for each tool
  - [x] Crosshair cursor for precision
- [x] Visual feedback on snap (line flash)
- [x] Tooltip on canvas showing dimensions while drawing
- [x] Animate selection handles on hover
- [x] Ghost preview of shape being created

---

## Phase 4: Professional Features

### 4.1 Layers & Groups
- [x] Implement `LayersPanel` UI (Tree view) with thumbnails
  - [x] Layer row with thumbnail, name, visibility, lock
  - [x] Expand/collapse groups
  - [x] Selection highlight
  - [x] Active layer indicator
- [x] Drag-and-drop reordering
  - [x] Drag indicator
  - [x] Drop target highlight
  - [x] Into group nesting
- [x] Visibility (Eye icon) and Lock toggles
  - [x] Click to toggle
  - [x] Alt+Click to solo
- [x] Opacity slider per layer
- [x] Blend mode dropdown per layer
- [x] Group/Ungroup commands (Ctrl+G, Ctrl+Shift+G)
- [x] Isolation Mode (Double click group to edit only that group)
  - [x] Breadcrumb navigation
  - [x] Dimmed elements outside group
- [ ] Layer search/filter
- [x] Rename layer (double-click or F2)
- [x] Duplicate layer
- [x] Delete layer with confirmation
- [x] Merge layers

### 4.2 Property Inspector
- [x] Create `PropertiesPanel` View
  - [x] Collapsible sections
  - [x] Dynamic content based on selection
- [x] Implement Color Picker
  - [x] Color wheel
  - [x] Saturation/brightness square
  - [x] Sliders (RGB, HSL, HEX)
  - [x] Alpha slider
  - [ ] Eyedropper tool
  - [ ] Saved swatches
  - [ ] Recently used colors
- [x] Gradient Editor
  - [x] Add/remove stops
  - [x] Drag stops to reposition
  - [x] Angle/position controls
  - [x] Linear/Radial/Conic types
  - [ ] Preset gradients
- [x] Stroke controls (Width, Dash Array, Cap, Join)
  - [x] Width input with slider
  - [x] Preset dash patterns
  - [x] Cap style icons
  - [x] Join style icons
- [x] Geometry properties (X, Y, Width, Height, Rotation)
  - [x] Numeric inputs
  - [x] Constrain proportions toggle
  - [x] Rotation input with dial
- [x] Transform Origin selection (9-point grid)
  - [x] Visual 9-point selector
  - [x] Custom origin coordinates
- [x] Opacity & Blending modes
  - [x] Opacity slider
  - [x] Blend mode dropdown
- [x] Corner radius controls
  - [x] Uniform radius
  - [ ] Individual corner radii
- [ ] Effects stack (shadows, blurs)
  - [ ] Add effect button
  - [ ] Reorder effects
  - [ ] Toggle effect visibility
  - [ ] Delete effect

### 4.3 Advanced Path Operations
- [x] Implement Boolean Operations via `SkiaSharp.SKPath.Op`
  - [x] Union (Combine shapes)
  - [x] Subtract (Cut out)
  - [x] Intersect (Common area)
  - [x] Exclude (XOR)
  - [ ] Preview before applying
- [x] Implement "Text to Path" conversion
- [x] Implement "Stroke to Path" (Outline)
- [x] Path Simplify (Decimate nodes)
  - [x] Tolerance slider
  - [ ] Preview
- [x] Path Offset (Inset/Outset)
  - [x] Distance input
  - [x] Join type
  - [x] Miter limit
- [x] Path Division (knife tool)
  - [x] Draw cut line
  - [x] Split path at intersection

### 4.4 Symbols & Components
- [x] Create symbol from selection
  - [x] Name symbol
  - [x] Save to library
- [x] Symbol library panel
  - [x] Grid view
  - [x] Search
  - [x] Categories
- [x] Symbol instances on canvas
  - [x] Drag from library
  - [x] Linked to master
- [x] Edit master symbol (updates all instances)
  - [x] Double-click to edit
  - [x] Breadcrumb navigation
  - [x] Changes propagate
- [x] Override instance properties
  - [x] Fill, stroke
  - [x] Size
  - [x] Detach from master

### 4.5 Artboards
- [x] Multiple artboards per document
- [x] Artboard tool (create/resize)
  - [x] Drag to create
  - [x] Resize handles
- [x] Artboard properties
  - [x] Name
  - [x] Size (presets + custom)
  - [x] Background color
- [x] Artboard list in Layers panel
- [x] Export individual artboards
- [x] Artboard navigation

### 4.6 Phase 4 UI Polish
- [x] Collapsible sections in Properties panel with animation
- [x] Preset dropdown for common values (stroke widths, colors)
- [x] Layer thumbnail updates live
- [x] Smooth reorder animation in Layers panel
- [x] Boolean operation preview before applying
- [x] Color picker with smooth animations
- [x] Gradient editor with live preview

---

## Phase 5: Next-Gen UI/UX ("The WOW Factor")

### 5.1 Theming & Branding
- [ ] Dark theme (default) with Catppuccin Mocha colors
  - [ ] Background: #1e1e2e
  - [ ] Surface: #313244
  - [ ] Text: #cdd6f4
  - [ ] Accent: #89b4fa
- [ ] Light theme option
  - [ ] Catppuccin Latte colors
- [ ] Accent color customization
- [ ] Custom icon set (Phosphor or Lucide)
  - [ ] 200+ icons for all actions
  - [ ] SVG format
  - [ ] Theme-aware colors
- [ ] Splash screen with animated logo
  - [ ] Fade in
  - [ ] Logo animation
  - [ ] Loading progress
- [ ] About dialog with version, credits, links
  - [ ] Logo
  - [ ] Version number
  - [ ] Copyright
  - [ ] Links to docs, GitHub, website

### 5.2 Fluid Motion & Visuals
- [ ] Implement `Mica` window backdrop (Windows 11 native feel)
  - [ ] Fallback to solid color on older Windows
- [ ] Add `XamlFlair` animations for panel transitions (Slide/Fade in)
- [ ] Implement "Micro-interactions"
  - [ ] Buttons scale on click (0.95 -> 1.0)
  - [ ] Toggles animate on/off
  - [ ] Checkboxes animate
  - [ ] Hover effects (subtle glow)
- [ ] Add "Glassmorphism" effect to floating panels (Blur behind)
- [ ] Smooth zoom animation (ease in/out)
  - [ ] Duration: 200ms
  - [ ] Easing: CubicEaseOut
- [ ] Canvas pan momentum (inertia)
  - [ ] Physics-based deceleration
- [ ] Selection bounding box animate on change
- [ ] Toast notifications (slide in/out)
  - [ ] Success, warning, error styles
  - [ ] Auto-dismiss
  - [ ] Action buttons
- [ ] Panel open/close animations
- [ ] Dialog appear/disappear animations

### 5.3 Command Palette (Ctrl+K)
- [ ] Create overlay UI for global command search
  - [ ] Centered modal
  - [ ] Search input with focus
  - [ ] Results list
  - [ ] Keyboard navigation
- [ ] Index all available commands and tools
  - [ ] Menu items
  - [ ] Tools
  - [ ] Recent files
  - [ ] Settings
- [ ] Implement "Fuzzy Search" logic
  - [ ] Match anywhere in string
  - [ ] Score by match quality
  - [ ] Highlight matched characters
- [ ] Add "Recent Commands" history
- [ ] Show keyboard shortcuts inline
- [ ] Quick file open (recent files)
- [ ] Quick action suggestions

### 5.4 On-Canvas "HUD"
- [ ] Implement contextual toolbar appearing near selection (Figma style)
  - [ ] Appears on selection
  - [ ] Position relative to bounding box
  - [ ] Auto-reposition to stay on screen
- [ ] Quick actions: Boolean ops, Group/Ungroup, Color swatch
- [ ] Distance indicators when holding Alt (Smart Guides)
- [ ] Tooltip with element info on hover
  - [ ] Element type
  - [ ] Name
  - [ ] Dimensions
- [ ] Zoom level indicator (bottom right)
- [ ] Selection info bar (count, type, dimensions)
- [ ] Ruler tick marks on cursor position

### 5.5 Keyboard Shortcuts
- [ ] Keyboard shortcut system with central registry
- [ ] Customizable shortcut editor
  - [ ] List all actions
  - [ ] Filter/search
  - [ ] Record new shortcut
  - [ ] Reset to default
- [ ] Preset profiles (Illustrator, Inkscape, Figma)
- [ ] Cheat sheet overlay (hold Ctrl+/)
  - [ ] Group by category
  - [ ] Searchable
- [ ] Conflict detection
- [ ] Export/import shortcuts

### 5.6 Code Integration (Monaco Editor)
- [ ] Set up WebView2 with Monaco Editor
  - [ ] Configure WebView2 environment
  - [ ] Load Monaco HTML/JS locally
- [ ] Host Monaco files locally in Resources
  - [ ] Download Monaco package
  - [ ] Include in build
- [ ] Create C# <-> JS bridge for content sync
  - [ ] `SetContent(string)` method
  - [ ] `GetContent()` method
  - [ ] `OnContentChanged` event
- [ ] SVG/XML syntax highlighting
- [ ] Code folding
- [ ] Line numbers
- [ ] Minimap
- [ ] Error highlighting (invalid XML)
  - [ ] Parse SVG on change
  - [ ] Mark error lines
  - [ ] Hover for error message
- [ ] Implementation Bi-directional Sync (Canvas <-> Code)
  - [ ] Debounced update (300ms)
  - [ ] Diff-based sync (minimal re-render)
  - [ ] Lock sync during drag operations
- [ ] "Hover to Highlight" in Code (find element in canvas)
  - [ ] Hover over element in code
  - [ ] Highlight corresponding element on canvas
- [ ] "Click to Navigate" in canvas (jump to code line)
  - [ ] Select element on canvas
  - [ ] Scroll code to element definition
- [ ] Format/Prettify command
- [ ] (Fallback) AvalonEdit for systems without WebView2

---

## Phase 6: Import/Export & Assets

### 6.1 File Operations
- [ ] New document wizard (presets: icon, web, print)
  - [ ] Preset sizes
  - [ ] Custom size
  - [ ] Units (px, mm, in)
  - [ ] Color mode
- [ ] Open recent files list
  - [ ] Last 10 files
  - [ ] Clear recent list
- [ ] Auto-save drafts
  - [ ] Save every 2 minutes
  - [ ] Store in temp folder
- [ ] Document recovery on crash
  - [ ] Check for recovery files on startup
  - [ ] Offer to restore

### 6.2 Import Formats
- [ ] SVG (primary)
- [ ] AI (Adobe Illustrator) - basic support
- [ ] EPS (Encapsulated PostScript) - basic support
- [ ] PDF (vector content extraction)
- [ ] PNG/JPG (as embedded image)
- [ ] Clipboard paste (image, SVG)

### 6.3 Export Formats
- [ ] SVG (optimized, minified)
  - [ ] Standard SVG 1.1
  - [ ] Optimized (SVGO-style)
  - [ ] Minified (no whitespace)
- [ ] PNG (with transparency, custom DPI)
  - [ ] Scale options (1x, 2x, 3x, custom)
  - [ ] Background options
- [ ] JPG (quality slider)
- [ ] PDF (vector)
- [ ] XAML (WPF resource)
- [ ] React/Vue component
- [ ] CSS clip-path
- [ ] ICO (multi-resolution icon)
- [ ] WebP

### 6.4 Export Dialog
- [ ] Format selection
- [ ] Preview
- [ ] Size options
- [ ] Quality options
- [ ] Filename template
- [ ] Export all artboards option
- [ ] Batch export

### 6.5 Asset Management
- [ ] Built-in icon library (browse, search, insert)
  - [ ] Categories
  - [ ] Search
  - [ ] Preview
  - [ ] Drag to canvas
- [ ] Template gallery
  - [ ] Categories
  - [ ] Preview
  - [ ] Create from template
- [ ] User asset library (drag files to save)
  - [ ] Import SVG files
  - [ ] Organize in folders
  - [ ] Quick access

---

## Phase 7: AI & Generation

### 7.1 Generative Vectors
- [ ] "Text to Icon" generator (Integration with OpenAI/DALL-E 3 API)
  - [ ] Prompt input
  - [ ] Style selection (flat, outline, 3D)
  - [ ] Color scheme
  - [ ] Multiple results to choose from
  - [ ] Refine prompt
- [ ] "Vectorize Bitmap" (Trace raster images to SVG paths)
  - [ ] Threshold/detail controls
  - [ ] Color simplification
  - [ ] Smoothness slider
  - [ ] Preview
  - [ ] Progress indicator

### 7.2 Smart Assist
- [ ] "Auto-Name Layers" (AI analyzes shape to name layer)
- [ ] "Generate Pattern" (Create repeating patterns from selection)
- [ ] "Suggest Colors" (AI color palette from image or prompt)
- [ ] "Complete Shape" (AI predicts incomplete path)
- [ ] "Auto-Align" suggestions

### 7.3 Optimization Assistant
- [ ] "Analyze SVG" panel
  - [ ] File size
  - [ ] Element count
  - [ ] Complexity score
  - [ ] Issues list
- [ ] "Optimize" button (run SVGO-like optimizations)
  - [ ] Remove hidden elements
  - [ ] Merge paths
  - [ ] Round coordinates
  - [ ] Remove metadata
  - [ ] Collapse groups
- [ ] Before/after preview
- [ ] Optimization presets (web, print, minimal)

---

## Phase 8: Settings & Preferences

### 8.1 Settings Dialog
- [ ] General settings
  - [ ] Language
  - [ ] Auto-save interval
  - [ ] Recent files count
  - [ ] Default units
- [ ] Appearance settings
  - [ ] Theme (dark/light)
  - [ ] Accent color
  - [ ] Interface scale
  - [ ] Font size
- [ ] Canvas settings
  - [ ] Default canvas size
  - [ ] Background color
  - [ ] Grid size
  - [ ] Snap tolerance
- [ ] Tool settings
  - [ ] Default fill color
  - [ ] Default stroke color
  - [ ] Default stroke width
- [ ] Export settings
  - [ ] Default format
  - [ ] Default quality
  - [ ] Default location
- [ ] Keyboard shortcuts
  - [ ] Shortcut editor
  - [ ] Import/export

### 8.2 Settings Storage
- [ ] JSON settings file
- [ ] User AppData location
- [ ] Migrate settings on update
- [ ] Reset to defaults

---

## Phase 9: Performance & Stability

### 9.1 Performance Tuning
- [ ] Implement R-Tree spatial index for fast hit-testing (1000s of objects)
- [ ] Render caching (cache static layers to bitmaps)
- [ ] Memory profiling for large SVGs
- [ ] Lazy rendering (only render visible area)
- [ ] Worker thread for expensive operations (boolean ops)
- [ ] Profile startup time, optimize
- [ ] Virtualize layer list for large documents
- [ ] Throttle rendering during pan/zoom

### 9.2 Error Handling
- [ ] Global exception handler
- [ ] User-friendly error dialogs
  - [ ] Error description
  - [ ] Stack trace (hidden, copyable)
  - [ ] Report issue link
- [ ] Crash reporter (optional telemetry)
- [ ] Log file rotation
  - [ ] Keep last 5 log files
  - [ ] Max size per file

### 9.3 Testing
- [ ] Unit tests for Core services
  - [ ] Model tests
  - [ ] Command tests
  - [ ] SVG bridge tests
- [ ] Integration tests for SVG import/export
- [ ] UI automation tests (basic flows)
- [ ] Performance benchmarks
- [ ] Test coverage target: 80%

---

## Phase 10: Accessibility & Localization

### 10.1 Accessibility
- [ ] Screen reader support (UI Automation)
  - [ ] All controls labeled
  - [ ] Reading order correct
  - [ ] Live regions for updates
- [ ] High contrast mode
  - [ ] Detect system setting
  - [ ] High contrast theme
- [ ] Keyboard navigation for canvas (Arrow keys to move)
  - [ ] Tab through elements
  - [ ] Arrow keys to move
  - [ ] Enter to select
- [ ] Focus indicators
  - [ ] Visible focus ring
  - [ ] High contrast focus
- [ ] Reduced motion option
  - [ ] Disable animations
  - [ ] Instant transitions

### 10.2 Localization
- [ ] Externalize all strings to resources
- [ ] English (default)
- [ ] Spanish, French, German (community)
- [ ] RTL layout support
- [ ] Date/number formatting
- [ ] Pluralization support

---

## Phase 11: Distribution & Marketing

### 11.1 Packaging
- [ ] MSIX Installer creation
  - [ ] Configure manifest
  - [ ] Icons
  - [ ] Capabilities
- [ ] Portable ZIP distribution
  - [ ] Self-contained
  - [ ] No installation required
- [ ] Microsoft Store submission
  - [ ] Store listing
  - [ ] Screenshots
  - [ ] Description

### 11.2 Updates
- [ ] Auto-updater mechanism (check on startup)
  - [ ] Version check API
  - [ ] Download in background
  - [ ] Prompt to install
- [ ] Release notes dialog
  - [ ] What's new
  - [ ] Changelog link
- [ ] Changelog.md

### 11.3 Marketing
- [ ] Landing page (bezier.app)
  - [ ] Hero section
  - [ ] Feature highlights
  - [ ] Screenshots
  - [ ] Download buttons
- [ ] Demo video (60-90 seconds)
  - [ ] Key features
  - [ ] Professional editing
- [ ] Product Hunt launch
- [ ] GitHub "Awesome" lists submission
- [ ] Social media presence

---

## Priority Order

### Immediate (Week 1)
1. **[0.1-0.7]** Foundation, UI Shell, Menus & Toolbar

### Core Development (Week 2-5)
2. **[1.1-1.5]** Core Data Model, Rendering & UI Polish
3. **[2.1-2.5]** Editor Architecture, Layout & UI Polish
4. **[3.1-3.8]** Visual Editing Features & UI Polish

### Feature Complete (Week 6-9)
5. **[4.1-4.6]** Professional Features & UI Polish
6. **[5.1-5.6]** Next-Gen UI/UX & Code Integration
7. **[6.1-6.5]** Import/Export & Assets

### Polish & Release (Week 10-14)
8. **[7.1-7.3]** AI Features
9. **[8.1-8.2]** Settings & Preferences
10. **[9.1-9.3]** Performance & Testing (Ongoing)
11. **[10.1-10.2]** Accessibility & Localization (Pre-release)
12. **[11.1-11.3]** Distribution & Marketing (Release)
