# Bezier - Production Roadmap

> **Vision**: The ultimate open-source SVG editor that rivals and surpasses Inkscape, Figma, Illustrator, and CorelDRAW — with innovative features they don't have.

## 🔧 Quick Fix Prompt
```
Continue developing Bezier SVG Editor and work on the following: [REQUEST]
Reference this file for context.
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

## 🤖 Feature Development Prompt
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

## ✨ Vibe Coding Prompt
```
Continue developing Bezier SVG Editor.
Task: Fully Implement and Polish [FEATURE ITEM]
Reference this file for context.
Follow coding standards in STANDARDS.md.

**Objectives:**
1. **Analyze & Implement**: Review the codebase. Implement the feature if missing or incomplete.
2. **Production Ready**: Ensure the code is robust, follows patterns, and handles edge cases.
3. **Enhance**: Improve the feature with better logic, performance, or visual "juice".
4. **Suggestions**: Briefly propose small tweaks to further elevate the feature.
5. **UI/UX Check**: Ensure all interface elements (Buttons, Commands, Cursors, Shortcuts) are implemented and accessible.
6. **Integration**: Verify that this feature works seamlessly with related systems.

**Workflow:**
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

### 2.6 Advanced Panel & Toolbar System
> Professional-grade UI organization like CorelDRAW, Illustrator, Photoshop

#### 2.6.1 Tabbed Panel Groups
- [ ] Implement tabbed panel containers (multiple panels sharing one area)
  - [ ] Tab strip at top of panel group
  - [ ] Drag tabs to reorder within group
  - [ ] Drag tabs between panel groups
  - [ ] Tab overflow menu when too many tabs
  - [ ] Close button on tab hover
- [ ] Default panel groupings:
  - [ ] Right dock: Properties + Layers + History (tabbed)
  - [ ] Left dock: Tools + Symbols/Assets (tabbed)
  - [ ] Bottom dock: Code Editor + Output/Messages (tabbed)
- [ ] Panel group collapse/expand (minimize to icon strip)
- [ ] Save/restore panel group configurations

#### 2.6.2 Contextual Property Bars (Options Bar)
> Secondary toolbar that changes based on active tool/selection (like Photoshop/Illustrator)

- [ ] Create `PropertyBar` control (horizontal toolbar below main toolbar)
  - [ ] Dynamic content based on context
  - [ ] Consistent height and styling
  - [ ] Separator groups for related options
- [ ] Tool-specific property bars:
  - [ ] **Select Tool**: X, Y, W, H inputs, rotation, scale, flip buttons
  - [ ] **Rectangle Tool**: Corner radius, width, height, from center toggle
  - [ ] **Ellipse Tool**: Width, height, pie/arc options
  - [ ] **Pen Tool**: Path mode (add/subtract), close path, curve options
  - [ ] **Text Tool**: Font family, size, weight, alignment, spacing
  - [ ] **Zoom Tool**: Zoom level dropdown, fit options
- [ ] Selection-based property bars:
  - [ ] **No Selection**: Document properties (size, background)
  - [ ] **Single Element**: Element-specific properties
  - [ ] **Multi-Selection**: Alignment, distribute, group options
  - [ ] **Path Selected**: Node editing options, path operations
  - [ ] **Text Selected**: Typography options
- [ ] Quick action buttons in property bar (context-sensitive)

#### 2.6.3 Contextual Panels (Docker Windows)
> Panels that auto-show/hide based on selection or tool

- [ ] Implement panel visibility rules system
  - [ ] Rule: Show when tool X is active
  - [ ] Rule: Show when element type Y is selected
  - [ ] Rule: Show when selection count > N
  - [ ] User can override (pin panel open/closed)
- [ ] Context-aware panels:
  - [ ] **Transform Panel**: Shows when elements selected (X, Y, W, H, rotation, skew)
  - [ ] **Fill & Stroke Panel**: Shows for shape/path elements
  - [ ] **Typography Panel**: Shows when text selected
  - [ ] **Path Operations Panel**: Shows when paths selected
  - [ ] **Align & Distribute Panel**: Shows for multi-selection
  - [ ] **Symbol Options Panel**: Shows when symbol selected
- [ ] Panel state indicators:
  - [ ] Pinned icon (always visible)
  - [ ] Auto icon (context-sensitive)
  - [ ] Hidden icon (manually hidden)

#### 2.6.4 Secondary Toolbars
- [ ] Implement dockable secondary toolbar system
  - [ ] Can dock top, bottom, left, right, or float
  - [ ] Collapsible to single row
  - [ ] Customizable button arrangement
- [ ] Standard secondary toolbars:
  - [ ] **Formatting Toolbar**: Fill, stroke, font options
  - [ ] **Arrange Toolbar**: Order, align, distribute, group
  - [ ] **View Toolbar**: Zoom controls, view modes, rulers, grid
  - [ ] **Path Toolbar**: Path operations, boolean ops, convert
- [ ] Tool-specific floating toolbars:
  - [ ] Pen tool: Node type buttons, path actions
  - [ ] Text tool: Quick formatting
  - [ ] Shape tool: Shape variants
- [ ] Toolbar customization dialog
  - [ ] Add/remove buttons
  - [ ] Reorder buttons
  - [ ] Create custom toolbars
  - [ ] Reset to defaults

#### 2.6.5 Panel Organization Features
- [ ] Panel quick access sidebar (icon strip when panels collapsed)
- [ ] "Workspaces" - saved panel/toolbar configurations
  - [ ] Built-in workspaces: Default, Minimal, Illustration, Typography
  - [ ] User custom workspaces
  - [ ] Quick workspace switcher (dropdown or shortcuts)
- [ ] "Focus Mode" - hide all panels except canvas (Tab key toggle)
- [ ] Panel search/filter (quickly find and open any panel)
- [ ] Recently used panels list
- [ ] Panel grouping presets (reset to specific configurations)

#### 2.6.6 Responsive Layout
- [ ] Adapt panel layout based on window size
  - [ ] Small window: Collapse panels to icons
  - [ ] Medium window: Single column panels
  - [ ] Large window: Full multi-column layout
- [ ] Minimum panel sizes with scroll
- [ ] Panel content adapts to available width
- [ ] Touch-friendly mode (larger buttons, spacing)

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
- [x] Implement "Invert Selection" (Ctrl+Shift+I)

### 3.2 Basic Shape Tools
- [x] `RectangleTool`: Drag to create
  - [x] Shift for square
  - [x] Alt for center origin
  - [ ] Corner radius handle post-creation
  - [ ] Individual corner radius controls
  - [x] Live dimensions tooltip
- [x] `EllipseTool`: Center/Corner modes
  - [x] Shift for circle
  - [ ] Pie/arc mode (start angle, end angle)
  - [x] Live dimensions tooltip
- [x] `LineTool`: Simple two-point lines
  - [x] Shift for 45° snap
  - [x] Live length/angle tooltip
  - [ ] Arrow heads (start, end, both)
  - [ ] Connector line mode (auto-route between objects)
- [ ] `PolygonTool`: N-sided polygons
  - [ ] Options bar: number of sides (3-100)
  - [ ] Corner rounding
  - [ ] Rotation angle offset
- [ ] `StarTool`: N-pointed stars
  - [ ] Options bar: number of points (3-100)
  - [ ] Inner/outer radius ratio
  - [ ] Corner rounding (inner/outer)
  - [ ] Smooth points option
- [ ] `SpiralTool`: Spiral paths
  - [ ] Number of turns
  - [ ] Decay/growth rate
  - [ ] Clockwise/counter-clockwise
- [ ] `GridTool`: Create grids of rectangles
  - [ ] Rows and columns
  - [ ] Gutter spacing
  - [ ] Individual cell selection
- [ ] `ArcTool`: Circular arcs
  - [ ] Start/end angle
  - [ ] Chord/pie/arc modes
- [ ] `ArrowTool`: Pre-styled arrows
  - [ ] Arrow head styles
  - [ ] Curved/straight options
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
  - [ ] Select all nodes (Ctrl+A in node mode)
  - [ ] Select inverse nodes
- [x] Drag nodes to reshape
- [x] Drag control handles to adjust curvature
  - [ ] Retract handles (double-click)
  - [ ] Extend handles (drag from node)
- [x] Convert node types (Corner <-> Smooth <-> Symmetric)
  - [x] Keyboard shortcut (1, 2, 3 keys)
  - [ ] Context menu
- [x] Add/Remove nodes on path segment
  - [ ] Double-click to add
  - [x] Delete key to remove
  - [ ] Add nodes at equal intervals
- [ ] "Simplify Path" command (reduce nodes)
  - [ ] Tolerance slider
  - [ ] Preview before applying
- [ ] "Smooth Path" command (add curves)
  - [ ] Smoothness slider
  - [ ] Preserve corners option
- [ ] "Roughen Path" command (add jitter)
- [ ] "Break Path" at node
- [ ] "Join Paths" command
  - [ ] Connect endpoints
  - [ ] Average endpoints
  - [ ] Extend and connect
- [ ] "Reverse Path" command
- [ ] "Close Path" command
- [ ] "Open Path" command (break at start)
- [ ] Fillet/Chamfer corners
  - [ ] Radius input
  - [ ] Apply to selected corners
- [ ] Align nodes (horizontal, vertical)
- [ ] Distribute nodes evenly

### 3.5 Text Tool
- [x] Click to create text block (point text)
- [ ] Drag to create area text (text box)
  - [ ] Text wraps within bounds
  - [ ] Resize to reflow
  - [ ] Auto-size height option
- [x] Inline text editing on canvas
  - [x] Blinking cursor
  - [x] Text selection
  - [ ] Copy/paste (requires clipboard integration)
  - [ ] Find and replace
  - [ ] Spell check integration
- [x] Font picker (family, weight, style)
  - [ ] System fonts list with preview
  - [ ] Recent fonts section
  - [ ] Font search/filter
  - [ ] Variable fonts support (weight axis, etc.)
- [x] Font size, line height, letter spacing
  - [ ] Character spacing (tracking)
  - [ ] Word spacing
  - [ ] Baseline shift
  - [ ] Kerning (auto/manual/optical)
- [x] Text alignment (left, center, right, justify)
  - [ ] Vertical alignment (top, center, bottom)
  - [ ] Last line alignment
- [ ] Text on path feature
  - [ ] Attach text to path
  - [ ] Offset along path
  - [ ] Flip text direction
  - [ ] Gravity (top/bottom of path)
- [ ] Text inside shape (area type)
  - [ ] Flow text into shape
  - [ ] Inset margin
- [ ] Text columns
  - [ ] Number of columns
  - [ ] Column gutter
  - [ ] Balance columns
- [x] Text outline and fill
  - [ ] Multiple fills/strokes
- [ ] OpenType features panel
  - [ ] Ligatures (standard, discretionary)
  - [ ] Stylistic alternates
  - [ ] Swashes
  - [ ] Small caps
  - [ ] Fractions
  - [ ] Ordinals
  - [ ] Superscript/subscript
- [ ] Paragraph styles
  - [ ] Create/edit styles
  - [ ] Apply to text
  - [ ] Update style from selection
- [ ] Character styles
  - [ ] Override paragraph formatting
  - [ ] Color, weight, style
- [ ] Bullets and numbering
  - [ ] Custom bullet characters
  - [ ] Numbered lists
  - [ ] Indentation
- [ ] Tabs and leaders
  - [ ] Tab stops (left, center, right, decimal)
  - [ ] Leader characters
- [ ] Drop caps
  - [ ] Number of lines
  - [ ] Character count
- [ ] Text wrap around objects
  - [ ] Wrap modes (bounding box, shape)
  - [ ] Offset distance

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
  - [ ] Eyedropper tool (pick from canvas)
  - [ ] Pick from screen (anywhere on desktop)
  - [ ] Saved swatches
  - [ ] Recently used colors (last 20)
  - [ ] Color harmonies generator
    - [ ] Complementary
    - [ ] Analogous
    - [ ] Triadic
    - [ ] Split-complementary
    - [ ] Tetradic
  - [ ] Global colors (linked swatches)
  - [ ] Spot colors (for print)
  - [ ] Color books (Pantone, etc.)
- [x] Gradient Editor
  - [x] Add/remove stops
  - [x] Drag stops to reposition
  - [x] Angle/position controls
  - [x] Linear/Radial/Conic types
  - [ ] Preset gradients library
  - [ ] Gradient on stroke
  - [ ] Freeform gradient (mesh-like)
  - [ ] Noise gradient
- [x] Stroke controls (Width, Dash Array, Cap, Join)
  - [x] Width input with slider
  - [x] Preset dash patterns
  - [x] Cap style icons
  - [x] Join style icons
  - [ ] Variable width stroke (pressure-like)
  - [ ] Stroke position (center, inside, outside)
  - [ ] Multiple strokes per object
- [x] Geometry properties (X, Y, Width, Height, Rotation)
  - [x] Numeric inputs
  - [x] Constrain proportions toggle
  - [x] Rotation input with dial
  - [ ] Skew X/Y controls
  - [ ] Flip horizontal/vertical buttons
- [x] Transform Origin selection (9-point grid)
  - [x] Visual 9-point selector
  - [x] Custom origin coordinates
- [x] Opacity & Blending modes
  - [x] Opacity slider
  - [x] Blend mode dropdown
  - [ ] Knockout group
  - [ ] Isolate blending
- [x] Corner radius controls
  - [x] Uniform radius
  - [ ] Individual corner radii
  - [ ] Radius units (px, %)
- [ ] Appearance panel (multiple fills/strokes)
  - [ ] Add fill layer
  - [ ] Add stroke layer
  - [ ] Reorder appearance items
  - [ ] Toggle visibility per item
  - [ ] Opacity per item
  - [ ] Blend mode per item
- [ ] Effects stack (shadows, blurs)
  - [ ] Add effect button
  - [ ] Reorder effects
  - [ ] Toggle effect visibility
  - [ ] Delete effect
  - [ ] Available effects:
    - [ ] Drop shadow
    - [ ] Inner shadow
    - [ ] Outer glow
    - [ ] Inner glow
    - [ ] Gaussian blur
    - [ ] Motion blur
    - [ ] Radial blur
    - [ ] Feather
    - [ ] Bevel & emboss
- [ ] Graphic styles panel
  - [ ] Save appearance as style
  - [ ] Apply style to selection
  - [ ] Update style from selection
  - [ ] Style library
  - [ ] Break link to style

### 4.3 Advanced Path Operations
- [x] Implement Boolean Operations via `SkiaSharp.SKPath.Op`
  - [x] Union (Combine shapes)
  - [x] Subtract (Cut out)
  - [x] Intersect (Common area)
  - [x] Exclude (XOR)
  - [ ] Divide (split by intersections)
  - [ ] Trim (cut overlapping areas)
  - [ ] Merge (combine like paths)
  - [ ] Crop (clip to shape)
  - [ ] Preview before applying
- [x] Implement "Text to Path" conversion
- [x] Implement "Stroke to Path" (Outline)
- [x] Path Simplify (Decimate nodes)
  - [x] Tolerance slider
  - [ ] Preview
  - [ ] Preserve corners option
- [x] Path Offset (Inset/Outset)
  - [x] Distance input
  - [x] Join type
  - [x] Miter limit
  - [ ] Steps (multiple offsets)
- [ ] Contour (parallel outlines)
  - [ ] Number of contours
  - [ ] Spacing
  - [ ] Color progression
- [x] Path Division (knife tool)
  - [x] Draw cut line
  - [x] Split path at intersection
- [ ] Scissors tool (cut path at point)
- [ ] Eraser tool (erase portions of path)
- [ ] Path effects (non-destructive)
  - [ ] Zig-zag
  - [ ] Wave/sine
  - [ ] Roughen
  - [ ] Tweak
  - [ ] Jitter
  - [ ] Round corners
  - [ ] Dashes to path
- [ ] Envelope distortion
  - [ ] Preset envelopes (arc, bulge, flag, wave)
  - [ ] Custom mesh envelope
  - [ ] Make with warp
  - [ ] Make with mesh
  - [ ] Make with top object
- [ ] Pattern along path (brush stroke)
  - [ ] Select pattern
  - [ ] Spacing
  - [ ] Scale
  - [ ] Rotation
- [ ] Blend tool (morph between shapes)
  - [ ] Specified steps
  - [ ] Specified distance
  - [ ] Smooth color transition
  - [ ] Spine (custom path)
  - [ ] Expand blend
- [ ] Live Paint (isolated fills)
  - [ ] Paint Bucket tool
  - [ ] Live Paint groups
  - [ ] Gap detection
- [ ] Perspective distort
  - [ ] One-point perspective
  - [ ] Two-point perspective
  - [ ] Free distort
- [ ] 3D effects
  - [ ] Extrude & bevel
  - [ ] Revolve
  - [ ] Rotate in 3D space
  - [ ] Map artwork to surfaces
- [ ] Mesh tool
  - [ ] Create mesh from shape
  - [ ] Add/remove mesh points
  - [ ] Color mesh points
  - [ ] Gradient mesh

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
- [x] Dark theme (default) with Catppuccin Mocha colors
  - [x] Background: #1e1e2e
  - [x] Surface: #313244
  - [x] Text: #cdd6f4
  - [x] Accent: #89b4fa
- [x] Light theme option
  - [x] Catppuccin Latte colors
- [x] Accent color customization
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
- [x] Implement `Mica` window backdrop (Windows 11 native feel)
  - [x] Fallback to solid color on older Windows
- [x] Add `XamlFlair` animations for panel transitions (Slide/Fade in)
- [x] Implement "Micro-interactions"
  - [x] Buttons scale on click (0.95 -> 1.0)
  - [x] Toggles animate on/off
  - [x] Checkboxes animate
  - [x] Hover effects (subtle glow)
- [x] Add "Glassmorphism" effect to floating panels (Blur behind)
- [x] Smooth zoom animation (ease in/out)
  - [x] Duration: 200ms
  - [x] Easing: CubicEaseOut
- [x] Canvas pan momentum (inertia)
  - [x] Physics-based deceleration
- [x] Selection bounding box animate on change
- [x] Toast notifications (slide in/out)
  - [x] Success, warning, error styles
  - [x] Auto-dismiss
  - [x] Action buttons
- [x] Panel open/close animations
- [x] Dialog appear/disappear animations

### 5.3 Command Palette (Ctrl+K)
- [x] Create overlay UI for global command search
  - [x] Centered modal
  - [x] Search input with focus
  - [x] Results list
  - [x] Keyboard navigation
- [x] Index all available commands and tools
  - [x] Menu items
  - [x] Tools
  - [x] Recent files
  - [x] Settings
- [x] Implement "Fuzzy Search" logic
  - [x] Match anywhere in string
  - [x] Score by match quality
  - [x] Highlight matched characters
- [x] Add "Recent Commands" history
- [x] Show keyboard shortcuts inline
- [x] Quick file open (recent files)
- [x] Quick action suggestions

### 5.4 On-Canvas "HUD"
- [x] Implement contextual toolbar appearing near selection (Figma style)
  - [x] Appears on selection
  - [x] Position relative to bounding box
  - [x] Auto-reposition to stay on screen
- [x] Quick actions: Boolean ops, Group/Ungroup, Color swatch
- [x] Distance indicators when holding Alt (Smart Guides)
- [x] Tooltip with element info on hover
  - [x] Element type
  - [x] Name
  - [x] Dimensions
- [x] Zoom level indicator (bottom right)
- [x] Selection info bar (count, type, dimensions)
- [x] Ruler tick marks on cursor position

### 5.5 Keyboard Shortcuts
- [x] Keyboard shortcut system with central registry
- [x] Customizable shortcut editor
  - [x] List all actions
  - [x] Filter/search
  - [x] Record new shortcut
  - [x] Reset to default
- [x] Preset profiles (Illustrator, Inkscape, Figma)
- [x] Cheat sheet overlay (hold Ctrl+/)
  - [x] Group by category
  - [x] Searchable
- [x] Conflict detection
- [x] Export/import shortcuts

### 5.6 Code Integration (Monaco Editor)
- [x] Set up WebView2 with Monaco Editor
  - [x] Configure WebView2 environment
  - [x] Load Monaco HTML/JS locally
- [x] Host Monaco files locally in Resources
  - [x] Download Monaco package
  - [x] Include in build
- [x] Create C# <-> JS bridge for content sync
  - [x] `SetContent(string)` method
  - [x] `GetContent()` method
  - [x] `OnContentChanged` event
- [x] SVG/XML syntax highlighting
- [x] Code folding
- [x] Line numbers
- [x] Minimap
- [x] Error highlighting (invalid XML)
  - [x] Parse SVG on change
  - [x] Mark error lines
  - [x] Hover for error message
- [x] Implementation Bi-directional Sync (Canvas <-> Code)
  - [x] Debounced update (300ms)
  - [x] Diff-based sync (minimal re-render)
  - [x] Lock sync during drag operations
- [x] "Hover to Highlight" in Code (find element in canvas)
  - [x] Hover over element in code
  - [x] Highlight corresponding element on canvas
- [x] "Click to Navigate" in canvas (jump to code line)
  - [x] Select element on canvas
  - [x] Scroll code to element definition
- [x] Format/Prettify command
- [ ] (Fallback) AvalonEdit for systems without WebView2

---

## Phase 6: Import/Export & Assets

### 6.1 File Operations
- [x] New document wizard (presets: icon, web, print)
  - [x] Preset sizes
  - [x] Custom size
  - [x] Units (px, mm, in)
  - [x] Color mode
- [x] Open recent files list
  - [x] Last 10 files
  - [x] Clear recent list
- [x] Auto-save drafts
  - [x] Save every 2 minutes
  - [x] Store in temp folder
- [x] Document recovery on crash
  - [x] Check for recovery files on startup
  - [x] Offer to restore

### 6.2 Import Formats
- [x] SVG (primary)
- [x] AI (Adobe Illustrator) - basic support
- [x] EPS (Encapsulated PostScript) - basic support
- [x] PDF (vector content extraction)
- [x] PNG/JPG (as embedded image)
- [x] Clipboard paste (image, SVG)

### 6.3 Export Formats
- [x] SVG (optimized, minified)
  - [x] Standard SVG 1.1
  - [x] Optimized (SVGO-style)
  - [x] Minified (no whitespace)
- [x] PNG (with transparency, custom DPI)
  - [x] Scale options (1x, 2x, 3x, custom)
  - [x] Background options
- [x] JPG (quality slider)
- [x] PDF (vector)
- [x] XAML (WPF resource)
- [x] React/Vue component
- [x] CSS clip-path
- [x] ICO (multi-resolution icon)
- [x] WebP

### 6.4 Export Dialog
- [x] Format selection
- [x] Preview
- [x] Size options
- [x] Quality options
- [x] Filename template
- [x] Export all artboards option
- [x] Batch export

### 6.5 Asset Management
- [x] Built-in icon library (browse, search, insert)
  - [x] Categories
  - [x] Search
  - [x] Preview
  - [x] Drag to canvas
- [x] Template gallery
  - [x] Categories
  - [x] Preview
  - [x] Create from template
- [x] User asset library (drag files to save)
  - [x] Import SVG files
  - [x] Organize in folders
  - [x] Quick access

---

## Phase 7: Brushes & Artistic Tools

### 7.1 Brush System
- [ ] Brush library panel
  - [ ] Built-in brushes
  - [ ] Custom brush creation
  - [ ] Brush categories
  - [ ] Search/filter
- [ ] Calligraphic brush
  - [ ] Angle
  - [ ] Roundness
  - [ ] Pressure sensitivity (for pen tablets)
- [ ] Scatter brush
  - [ ] Scatter amount
  - [ ] Rotation variation
  - [ ] Scale variation
  - [ ] Spacing
- [ ] Art brush (stretch artwork along path)
  - [ ] Create from selection
  - [ ] Scale options
  - [ ] Flip options
- [ ] Pattern brush (repeat artwork along path)
  - [ ] Start/end tiles
  - [ ] Corner tiles
  - [ ] Auto-generate corners
- [ ] Bristle brush (realistic brush strokes)
  - [ ] Brush shape
  - [ ] Bristle length
  - [ ] Bristle density
  - [ ] Bristle stiffness
- [ ] Blob brush (paint filled shapes)
  - [ ] Merge with same color
  - [ ] Keep selected
  - [ ] Fidelity

### 7.2 Artistic Tools
- [ ] Pencil tool (freehand drawing)
  - [ ] Fidelity slider
  - [ ] Smoothness slider
  - [ ] Keep selected
  - [ ] Edit selected paths
- [ ] Paintbrush tool (apply brushes)
  - [ ] Brush picker
  - [ ] Size
  - [ ] Pressure sensitivity
- [ ] Shaper tool (draw rough shapes, auto-recognize)
  - [ ] Recognize circles, rectangles, triangles
  - [ ] Combine touching shapes
  - [ ] Tap to complete
- [ ] Width tool (variable stroke width)
  - [ ] Add width points
  - [ ] Drag to adjust width
  - [ ] Delete width points
  - [ ] Width profiles
- [ ] Smooth tool (smooth existing paths)
- [ ] Path eraser tool (erase path segments)
- [ ] Symbol sprayer (spray symbol instances)
  - [ ] Instance density
  - [ ] Symbol stainer (colorize)
  - [ ] Symbol sizer (scale)
  - [ ] Symbol shifter (move)
  - [ ] Symbol spinner (rotate)
  - [ ] Symbol screener (opacity)

### 7.3 Pattern & Texture Tools
- [ ] Pattern maker
  - [ ] Create seamless patterns
  - [ ] Pattern tile types (grid, brick, hex)
  - [ ] Preview tiled
  - [ ] Edit pattern
- [ ] Halftone generator
  - [ ] Dot patterns
  - [ ] Line patterns
  - [ ] Custom shapes
- [ ] Texture fills
  - [ ] Noise textures
  - [ ] Grain effects
  - [ ] Paper textures
- [ ] Live trace (bitmap to vector)
  - [ ] High fidelity photo
  - [ ] Low fidelity photo
  - [ ] Grayscale
  - [ ] Black and white
  - [ ] Sketched art
  - [ ] Silhouettes
  - [ ] Line art
  - [ ] Technical drawing
  - [ ] Custom settings
  - [ ] Expand result

---

## Phase 8: AI & Generation

### 8.1 Generative Vectors
- [ ] "Text to Icon" generator (Integration with OpenAI/DALL-E 3 API)
  - [ ] Prompt input
  - [ ] Style selection (flat, outline, 3D, hand-drawn)
  - [ ] Color scheme input
  - [ ] Multiple results to choose from (4-8)
  - [ ] Refine prompt
  - [ ] Variation generator
- [ ] "Vectorize Bitmap" (Trace raster images to SVG paths)
  - [ ] Threshold/detail controls
  - [ ] Color simplification
  - [ ] Smoothness slider
  - [ ] Preview
  - [ ] Progress indicator
  - [ ] Mode presets (logo, photo, line art)
- [ ] "Generate from Reference" (upload image, generate similar style)
  - [ ] Style extraction
  - [ ] Color palette extraction
  - [ ] Shape suggestion

### 8.2 Smart Assist
- [ ] "Auto-Name Layers" (AI analyzes shape to name layer)
- [ ] "Generate Pattern" (Create repeating patterns from selection)
- [ ] "Suggest Colors" (AI color palette from image or prompt)
- [ ] "Complete Shape" (AI predicts incomplete path)
- [ ] "Auto-Align" suggestions
- [ ] "Similar Element Finder" (find elements with similar properties)
- [ ] "Auto Layout" (suggest optimal arrangement)
- [ ] "Accessibility Suggestions" (contrast, text size, etc.)

### 8.3 Optimization Assistant
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
  - [ ] Convert shapes to paths
  - [ ] Remove empty groups
- [ ] Before/after preview
- [ ] Optimization presets (web, print, minimal)
- [ ] Optimization history (undo optimization)

---

## Phase 9: Grids & Perspective

### 9.1 Advanced Grids
- [ ] Perspective grid
  - [ ] One-point perspective
  - [ ] Two-point perspective
  - [ ] Three-point perspective
  - [ ] Custom vanishing points
  - [ ] Draw on perspective planes
  - [ ] Snap to perspective
- [ ] Isometric grid
  - [ ] 30° isometric preset
  - [ ] Custom angles
  - [ ] Snap to isometric
  - [ ] Isometric transform
- [ ] Polar grid
  - [ ] Concentric circles
  - [ ] Radial dividers
  - [ ] Center point
- [ ] Custom modular grid
  - [ ] Column grid
  - [ ] Row grid
  - [ ] Gutters
  - [ ] Margins
  - [ ] Grid presets

### 9.2 Pixel Perfect Mode
- [ ] Pixel preview (render at 1x)
- [ ] Pixel grid (visible at high zoom)
- [ ] Snap to pixel
- [ ] Align to pixel grid command
- [ ] Half-pixel stroke adjustment
- [ ] Crisp edges option

---

## Phase 10: Print & Prepress

### 10.1 Print Features
- [ ] Print preview
  - [ ] Page setup
  - [ ] Artboard selection
  - [ ] Tile large artwork
  - [ ] Scale to fit
- [ ] Print dialog
  - [ ] Printer selection
  - [ ] Color management
  - [ ] Copies
  - [ ] Page range

### 10.2 Color Management
- [ ] Color profiles (ICC)
  - [ ] Assign profile
  - [ ] Convert to profile
  - [ ] Proof colors
- [ ] CMYK mode
  - [ ] CMYK color picker
  - [ ] CMYK preview
  - [ ] Out-of-gamut warning
- [ ] Spot colors
  - [ ] Pantone integration
  - [ ] Custom spot colors
  - [ ] Mixed ink
- [ ] Overprint preview
- [ ] Ink coverage analysis

### 10.3 Prepress Features
- [ ] Crop marks
- [ ] Registration marks
- [ ] Color bars
- [ ] Page information
- [ ] Bleed setup
  - [ ] Bleed guides
  - [ ] Bleed area preview
- [ ] Trim marks
- [ ] Fold marks
- [ ] Color separations preview
- [ ] Trapping settings
- [ ] Flatten transparency
- [ ] PDF/X export (print-ready)

---

## Phase 11: Settings & Preferences

### 11.1 Settings Dialog
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

### 11.2 Settings Storage
- [ ] JSON settings file
- [ ] User AppData location
- [ ] Migrate settings on update
- [ ] Reset to defaults

---

## Phase 12: Performance & Stability

### 12.1 Performance Tuning
- [ ] Implement R-Tree spatial index for fast hit-testing (1000s of objects)
- [ ] Render caching (cache static layers to bitmaps)
- [ ] Memory profiling for large SVGs
- [ ] Lazy rendering (only render visible area)
- [ ] Worker thread for expensive operations (boolean ops)
- [ ] Profile startup time, optimize
- [ ] Virtualize layer list for large documents
- [ ] Throttle rendering during pan/zoom

### 12.2 Error Handling
- [ ] Global exception handler
- [ ] User-friendly error dialogs
  - [ ] Error description
  - [ ] Stack trace (hidden, copyable)
  - [ ] Report issue link
- [ ] Crash reporter (optional telemetry)
- [ ] Log file rotation
  - [ ] Keep last 5 log files
  - [ ] Max size per file

### 12.3 Testing
- [ ] Unit tests for Core services
  - [ ] Model tests
  - [ ] Command tests
  - [ ] SVG bridge tests
- [ ] Integration tests for SVG import/export
- [ ] UI automation tests (basic flows)
- [ ] Performance benchmarks
- [ ] Test coverage target: 80%

---

## Phase 13: Accessibility & Localization

### 13.1 Accessibility
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

### 13.2 Localization
- [ ] Externalize all strings to resources
- [ ] English (default)
- [ ] Spanish, French, German (community)
- [ ] RTL layout support
- [ ] Date/number formatting
- [ ] Pluralization support

---

## Phase 14: Distribution & Marketing

### 14.1 Packaging
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

### 14.2 Updates
- [ ] Auto-updater mechanism (check on startup)
  - [ ] Version check API
  - [ ] Download in background
  - [ ] Prompt to install
- [ ] Release notes dialog
  - [ ] What's new
  - [ ] Changelog link
- [ ] Changelog.md

### 14.3 Marketing
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

## Phase 15: Developer Tools

### 15.1 Debug Window (Chrome DevTools-style)
- [x] Separate debug window (opens from Help menu or F12)
  - [x] Dockable/floating window
  - [x] Always on top option
  - [x] Persistent across sessions

### 15.2 Console Tab
- [x] Real-time log output from DebugLogger
  - [x] Color-coded log levels (Debug, Info, Warning, Error)
  - [x] Timestamp display
  - [x] Category filtering
- [x] Search/filter functionality
- [x] Clear console button
- [x] Copy selected logs to clipboard
- [x] Copy all logs to clipboard
- [x] Export logs to file
- [x] Auto-scroll toggle

### 15.3 Coordinates Tab
- [x] Mouse coordinates panel
  - [x] Screen coordinates (WPF)
  - [x] Document coordinates (canvas space)
  - [x] Artboard-relative coordinates
- [x] Selected element info
  - [x] Element type and name
  - [x] Position (X, Y)
  - [x] Size (Width, Height)
  - [x] Transform matrix values
  - [x] Bounding box coordinates
  - [x] Fill/Stroke properties
- [x] Canvas state info
  - [x] Current zoom level
  - [x] Pan offset
  - [x] Viewport dimensions
- [x] Copy all info button (formatted text)
- [x] Live update toggle

### 15.4 Elements Inspector
- [x] Tree view of document elements
- [x] Select element in canvas from tree
- [x] Highlight element on hover
- [x] Show/hide visibility
- [x] Lock/unlock elements
- [x] View raw SVG output

### 15.5 Performance Tab
- [x] Frame rate display
- [x] Render time metrics
- [x] Memory usage
- [x] Element count
- [x] Undo/Redo stack size

### 15.6 Crash Detection & Error Handling
- [x] Global unhandled exception handler (App.xaml.cs)
  - [x] Catch DispatcherUnhandledException
  - [x] Catch AppDomain.UnhandledException
  - [x] Catch TaskScheduler.UnobservedTaskException
- [x] Exception Window (not MessageBox)
  - [x] Show exception type and message
  - [x] Show stack trace (expandable)
  - [x] Copy full exception to clipboard button
  - [x] Option to continue or exit
  - [x] Distinguish handled vs unhandled exceptions
  - [x] Show inner exception details
- [ ] Crash report logging
  - [ ] Write to crash log file
  - [ ] Include system info (OS, .NET version)
  - [ ] Include app version
  - [ ] Include recent DebugLogger entries
- [ ] Recovery options
  - [ ] Auto-save before crash
  - [ ] Restore last session option

---

## Phase 16: Workflow & Automation
> *Features that save hours of repetitive work*

### 16.1 Actions & Macros
- [ ] Actions panel
  - [ ] Record actions
  - [ ] Play actions
  - [ ] Edit action steps
  - [ ] Save action sets
  - [ ] Load action sets
- [ ] Batch processing
  - [ ] Apply actions to multiple files
  - [ ] Progress indicator
  - [ ] Error logging
  - [ ] Resume on error
- [ ] Droplets (drag files to run action)

### 16.2 Scripting
- [ ] JavaScript scripting engine
  - [ ] Script editor panel
  - [ ] Script console
  - [ ] API documentation
- [ ] Python scripting support
  - [ ] Python environment setup
  - [ ] Script examples
- [ ] Script library (built-in useful scripts)
- [ ] Script shortcuts (assign scripts to keys)

### 16.3 Plugin System
- [ ] Plugin API
  - [ ] Tool plugins
  - [ ] Panel plugins
  - [ ] Filter plugins
  - [ ] Export plugins
- [ ] Plugin manager
  - [ ] Browse plugins
  - [ ] Install/uninstall
  - [ ] Enable/disable
  - [ ] Update plugins
- [ ] Plugin development documentation
- [ ] Plugin template project

---

## Phase 17: Collaboration & Cloud
> *Work together, anywhere*

### 17.1 Comments & Annotations
- [ ] Comment tool
  - [ ] Add comments to canvas
  - [ ] Pin to elements
  - [ ] Thread replies
- [ ] Comment panel
  - [ ] List all comments
  - [ ] Filter by status
  - [ ] Resolve comments
- [ ] Markup tools
  - [ ] Arrows
  - [ ] Callouts
  - [ ] Highlight areas

### 17.2 Version Control
- [ ] Built-in version history
  - [ ] Auto-save versions
  - [ ] Named versions
  - [ ] Compare versions
  - [ ] Restore version
- [ ] Git integration
  - [ ] Initialize repo
  - [ ] Commit changes
  - [ ] View diff
  - [ ] Branch management
- [ ] File comparison view
  - [ ] Side-by-side
  - [ ] Overlay
  - [ ] Difference highlight

### 17.3 Cloud Sync (Optional Service)
- [ ] Cloud storage integration
  - [ ] Save to cloud
  - [ ] Auto-sync
  - [ ] Conflict resolution
- [ ] Team libraries
  - [ ] Shared symbols
  - [ ] Shared styles
  - [ ] Shared colors
- [ ] Real-time collaboration (future)
  - [ ] See others' cursors
  - [ ] Live edits
  - [ ] User presence

---

## Phase 18: Beyond The Competition
> *Innovative features that set Bezier apart*

### 18.1 Parametric & Procedural Design
- [ ] Parametric shapes
  - [ ] Define parameters (width, height, segments, etc.)
  - [ ] Slider controls
  - [ ] Link parameters between shapes
  - [ ] Save parametric presets
- [ ] Repeat grids
  - [ ] Repeat selection in grid
  - [ ] Adjust spacing
  - [ ] Edit one to update all
  - [ ] Convert to individual
- [ ] Procedural generators
  - [ ] Generative patterns
  - [ ] Math-based shapes
  - [ ] Recursive shapes (fractals)
  - [ ] L-system patterns

### 18.2 Constraint-Based Design
- [ ] Constraints panel
  - [ ] Pin edges to parent
  - [ ] Maintain aspect ratio
  - [ ] Min/max sizes
  - [ ] Spacing constraints
- [ ] Responsive artboards
  - [ ] Artboard size presets
  - [ ] See how design adapts
  - [ ] Breakpoint system
- [ ] Smart layout
  - [ ] Auto-layout containers
  - [ ] Stack (horizontal/vertical)
  - [ ] Wrap
  - [ ] Gap spacing

### 18.3 Design Tokens & Variables
- [ ] Design tokens panel
  - [ ] Color tokens
  - [ ] Size tokens
  - [ ] Spacing tokens
  - [ ] Typography tokens
- [ ] Token aliases (semantic naming)
- [ ] Theme switching (swap token values)
- [ ] Export tokens (JSON, CSS variables)
- [ ] Import tokens (Figma, Tokens Studio)

### 18.4 Animation Timeline
- [ ] Animation panel
  - [ ] Timeline view
  - [ ] Keyframe editor
  - [ ] Easing curves
- [ ] Animate properties
  - [ ] Position
  - [ ] Scale
  - [ ] Rotation
  - [ ] Opacity
  - [ ] Fill/Stroke
  - [ ] Path morphing
- [ ] Export animated SVG
  - [ ] CSS animations
  - [ ] SMIL animations
  - [ ] Lottie export
- [ ] Preview animation

### 18.5 Component Variants
- [ ] Component with variants
  - [ ] Define variant properties (size, state, etc.)
  - [ ] Switch variants in properties
  - [ ] Combine variant properties
- [ ] Interactive components
  - [ ] Hover state
  - [ ] Pressed state
  - [ ] Disabled state
  - [ ] Focused state
- [ ] Slot overrides (nested component placeholders)

### 18.6 Accessibility Checker
- [ ] Accessibility panel
  - [ ] Color contrast checker (WCAG AA/AAA)
  - [ ] Touch target size checker
  - [ ] Text size recommendations
  - [ ] Alt text for images
- [ ] Auto-fix suggestions
- [ ] Export accessibility report

### 18.7 Developer Handoff
- [ ] Inspect mode
  - [ ] Click element to see properties
  - [ ] Copy CSS
  - [ ] Copy dimensions
  - [ ] Export assets
- [ ] Design specs export
  - [ ] HTML inspection page
  - [ ] Shareable link
  - [ ] Measurements overlay
- [ ] Code generation
  - [ ] React components
  - [ ] Vue components
  - [ ] SwiftUI views
  - [ ] Flutter widgets
  - [ ] XAML (WPF/UWP)

### 18.8 Advanced Selection & Editing
- [ ] Select by property
  - [ ] Same fill color
  - [ ] Same stroke color
  - [ ] Same stroke width
  - [ ] Same font
  - [ ] Same size
- [ ] Find and replace (properties)
  - [ ] Find color, replace with color
  - [ ] Find font, replace with font
- [ ] Global edit mode
  - [ ] Edit all instances at once
  - [ ] Scope to selection/document

### 18.9 Integration & Interop
- [ ] Figma import (experimental)
- [ ] Sketch import (experimental)
- [ ] XD import (experimental)
- [ ] Canva asset import
- [ ] Noun Project integration
- [ ] Unsplash integration
- [ ] Google Fonts integration
- [ ] Adobe Fonts integration (licensed)

---

## Priority Order

### Immediate (Week 1)
1. **[0.1-0.7]** Foundation, UI Shell, Menus & Toolbar

### Core Development (Week 2-6)
2. **[1.1-1.5]** Core Data Model, Rendering & UI Polish
3. **[2.1-2.6]** Editor Architecture, Layout, Advanced Panels & UI Polish
4. **[3.1-3.8]** Visual Editing Features & UI Polish

### Feature Complete (Week 7-12)
5. **[4.1-4.6]** Professional Features & UI Polish
6. **[5.1-5.6]** Next-Gen UI/UX & Code Integration
7. **[6.1-6.5]** Import/Export & Assets
8. **[7.1-7.3]** Brushes & Artistic Tools

### Professional Polish (Week 13-18)
9. **[8.1-8.3]** AI & Generation
10. **[9.1-9.2]** Grids & Perspective
11. **[10.1-10.3]** Print & Prepress
12. **[11.1-11.2]** Settings & Preferences
13. **[12.1-12.3]** Performance & Testing

### Release Preparation (Week 19-24)
14. **[13.1-13.2]** Accessibility & Localization
15. **[14.1-14.3]** Distribution & Marketing
16. **[15.1-15.6]** Developer Tools

### Post-Launch Innovation (Ongoing)
17. **[16.1-16.3]** Workflow & Automation
18. **[17.1-17.3]** Collaboration & Cloud
19. **[18.1-18.9]** Beyond The Competition (Differentiators)

---

## Feature Comparison Matrix

| Feature | Bezier | Illustrator | CorelDRAW | Inkscape |
|---------|--------|-------------|-----------|----------|
| **Core Vector Editing** | ✅ | ✅ | ✅ | ✅ |
| **SVG-First Workflow** | ✅ | ⚠️ | ⚠️ | ✅ |
| **Live Code Sync** | ✅ | ❌ | ❌ | ⚠️ |
| **Monaco Code Editor** | ✅ | ❌ | ❌ | ❌ |
| **Mica/Fluent Design** | ✅ | ❌ | ❌ | ❌ |
| **Command Palette** | ✅ | ✅ | ❌ | ❌ |
| **Design Tokens** | ✅ | ❌ | ❌ | ❌ |
| **Animation Timeline** | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **Parametric Shapes** | ✅ | ❌ | ❌ | ⚠️ |
| **Component Variants** | ✅ | ⚠️ | ❌ | ❌ |
| **Accessibility Checker** | ✅ | ❌ | ❌ | ❌ |
| **Git Integration** | ✅ | ❌ | ❌ | ❌ |
| **Developer Handoff** | ✅ | ⚠️ | ❌ | ❌ |
| **AI Generation** | ✅ | ✅ | ⚠️ | ❌ |
| **Open Source** | ✅ | ❌ | ❌ | ✅ |
| **Cross-Platform** | 🔜 | ✅ | ❌ | ✅ |
| **Free** | ✅ | ❌ | ❌ | ✅ |

Legend: ✅ Yes | ⚠️ Limited | ❌ No | 🔜 Planned
