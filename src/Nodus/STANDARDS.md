# Bezier Coding Standards

## .NET 10 & C# 14 (November 2025)

This document defines coding standards for the Bezier project, leveraging the latest .NET 10 (LTS) and C# 14 features.

---

## C# 14 New Features to Use

### 1. `field` Keyword for Auto-Properties
Use the `field` keyword to access the backing field directly in property accessors:

```csharp
// ✅ C# 14 - Use field keyword
public string Name
{
    get => field;
    set => field = value?.Trim() ?? throw new ArgumentNullException(nameof(value));
}

// ❌ Old way - Manual backing field
private string _name;
public string Name
{
    get => _name;
    set => _name = value?.Trim() ?? throw new ArgumentNullException(nameof(value));
}
```

### 2. Extension Members (Properties & Static)
Use extension blocks for static extension methods and properties:

```csharp
// ✅ C# 14 - Extension block syntax
public static class StringExtensions
{
    extension(string s)
    {
        public bool IsNullOrEmpty => string.IsNullOrEmpty(s);
        public string Reversed => new string(s.Reverse().ToArray());
    }
}

// Usage
if (myString.IsNullOrEmpty) { ... }
```

### 3. Null-Conditional Assignment
Use `?.=` for safer null-conditional assignments:

```csharp
// ✅ C# 14 - Null-conditional assignment
customer?.Address?.City = "New York";
list?[0] = newValue;

// ❌ Old way
if (customer?.Address != null)
{
    customer.Address.City = "New York";
}
```

### 4. `nameof` with Unbound Generic Types
Use `nameof` with unbound generics for cleaner reflection/logging:

```csharp
// ✅ C# 14
var typeName = nameof(List<>);        // Returns "List"
var dictName = nameof(Dictionary<,>); // Returns "Dictionary"

// ❌ Old way - Required closed generic
var typeName = nameof(List<object>);  // Returns "List"
```

### 5. Lambda Parameter Modifiers
Use modifiers directly on lambda parameters:

```csharp
// ✅ C# 14 - Modifiers without explicit types
var process = (ref int x, in string y) => x + y.Length;

// ❌ Old way - Required explicit types
Func<int, string, int> process = (ref int x, in string y) => x + y.Length;
```

### 6. Partial Constructors and Events
Extend partial members to constructors and events:

```csharp
// In file1.cs
public partial class ViewModel
{
    public partial event EventHandler? PropertyChanged;
    public partial ViewModel();
}

// In file2.cs (generated or manual)
public partial class ViewModel
{
    public partial event EventHandler? PropertyChanged
    {
        add => _handlers += value;
        remove => _handlers -= value;
    }
    
    public partial ViewModel()
    {
        InitializeComponent();
    }
}
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes, Records, Structs | PascalCase | `VectorElement`, `SvgDocument` |
| Interfaces | IPascalCase | `IFill`, `IEditorCommand` |
| Public Methods/Properties | PascalCase | `GetBounds()`, `FillColor` |
| Private Fields | _camelCase | `_backgroundColor`, `_isLoading` |
| Parameters, Local Variables | camelCase | `fileName`, `elementIndex` |
| Constants | PascalCase | `MaxZoomLevel`, `DefaultOpacity` |
| Type Parameters | T/TPascalCase | `T`, `TElement`, `TResult` |

---

## Code Style Rules

### File Organization
```csharp
// 1. File-scoped namespace (prefer)
namespace Bezier.Desktop.ViewModels;

// 2. Usings inside namespace (optional, project preference)
// 3. Order: using System.*, using Microsoft.*, using third-party, using project

// 4. Class members order:
//    - Constants
//    - Static fields
//    - Instance fields
//    - Constructors
//    - Properties
//    - Public methods
//    - Private methods
```

### Use Modern Patterns

```csharp
// ✅ Primary constructors (C# 12+)
public class SvgRect(double x, double y, double width, double height) : VectorElement
{
    public double X => x;
    public double Y => y;
}

// ✅ Target-typed new
private readonly List<VectorElement> _elements = new();

// ✅ Pattern matching
if (element is SvgRect { Width: > 0, Height: > 0 } rect)
{
    ProcessRect(rect);
}

// ✅ Switch expressions
public string GetToolName(ToolType type) => type switch
{
    ToolType.Select => "Selection Tool",
    ToolType.Pen => "Pen Tool",
    ToolType.Rectangle => "Rectangle Tool",
    _ => "Unknown"
};

// ✅ Collection expressions (C# 12+)
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];
```

### Async/Await Best Practices

```csharp
// ✅ Use async suffix for async methods
public async Task<Document> LoadDocumentAsync(string path)
{
    await using var stream = File.OpenRead(path);
    return await ParseAsync(stream);
}

// ✅ Use ValueTask for hot paths that often complete synchronously
public ValueTask<int> GetCachedValueAsync(string key)
{
    if (_cache.TryGetValue(key, out var value))
        return ValueTask.FromResult(value);
    return new ValueTask<int>(LoadFromDiskAsync(key));
}

// ✅ Use ConfigureAwait(false) in library code
var data = await httpClient.GetAsync(url).ConfigureAwait(false);

// ❌ Avoid async void (except for event handlers)
// ❌ Avoid .Result or .Wait() (causes deadlocks)
```

### Null Safety

```csharp
// ✅ Use nullable reference types
public string? OptionalName { get; set; }
public string RequiredName { get; set; } = string.Empty;

// ✅ Use null-coalescing operators
var name = input ?? "default";
var length = text?.Length ?? 0;

// ✅ Use required members (C# 11+)
public required string Id { get; init; }

// ✅ Use ArgumentNullException.ThrowIfNull (modern)
public void Process(Document document)
{
    ArgumentNullException.ThrowIfNull(document);
    // ...
}
```

---

## .NET 10 Runtime Features

### Use Span<T> for Performance
```csharp
// ✅ Use Span for non-allocating operations
public void ProcessData(ReadOnlySpan<byte> data)
{
    foreach (var b in data)
    {
        // No heap allocation
    }
}

// ✅ String operations without allocation
ReadOnlySpan<char> slice = text.AsSpan()[10..20];
```

### Use Records for DTOs and Value Types
```csharp
// ✅ Use records for immutable data
public record Point(double X, double Y);
public record struct Color(byte R, byte G, byte B, byte A);

// ✅ With-expressions for immutability
var moved = point with { X = point.X + 10 };
```

### Use Source Generators
```csharp
// ✅ Use [JsonSerializable] for AOT-friendly JSON
[JsonSerializable(typeof(AppSettings))]
public partial class AppSettingsContext : JsonSerializerContext { }

// ✅ Use [ObservableProperty] from CommunityToolkit.Mvvm
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string _title = "Bezier";
}
```

---

## WPF-Specific Guidelines

### MVVM Pattern
```csharp
// ✅ Use CommunityToolkit.Mvvm source generators
public partial class EditorViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(CanSave))]
    private string _fileName = "";
    
    [ObservableProperty]
    private bool _isDirty;
    
    public bool CanSave => !string.IsNullOrEmpty(FileName) && IsDirty;
    
    [RelayCommand(CanExecute = nameof(CanSave))]
    private void Save()
    {
        // Save logic
    }
}
```

### XAML Best Practices
```xml
<!-- ✅ Use StaticResource for static resources -->
<Border Background="{StaticResource BaseBrush}"/>

<!-- ✅ Use DynamicResource for theme-switchable resources -->
<TextBlock Foreground="{DynamicResource TextBrush}"/>

<!-- ✅ Use x:Bind in UWP/WinUI, Binding in WPF -->
<TextBox Text="{Binding FileName, UpdateSourceTrigger=PropertyChanged}"/>

<!-- ✅ Use compiled bindings where possible -->
<TextBlock Text="{Binding Path=Name, Mode=OneWay}"/>
```

---

## Error Handling

### Exception Guidelines
```csharp
// ✅ Use specific exception types
throw new ArgumentOutOfRangeException(nameof(zoom), zoom, "Zoom must be between 10% and 800%");
throw new InvalidOperationException("Cannot modify a locked layer");

// ✅ Use exception filters for conditional catching
try
{
    await LoadDocumentAsync(path);
}
catch (IOException ex) when (ex.HResult == -2147024864) // File in use
{
    ShowRetryDialog();
}

// ✅ Wrap and rethrow with context
catch (XmlException ex)
{
    throw new SvgParseException($"Invalid SVG at line {ex.LineNumber}", ex);
}

// ❌ Never catch and swallow silently
catch (Exception) { } // BAD!

// ❌ Avoid catching Exception in most cases
catch (Exception ex) { Log.Error(ex); } // Only at top-level handlers
```

### Result Pattern for Expected Failures
```csharp
// ✅ Use Result type for operations that can fail expectedly
public record Result<T>
{
    public bool IsSuccess { get; init; }
    public T? Value { get; init; }
    public string? Error { get; init; }
    
    public static Result<T> Success(T value) => new() { IsSuccess = true, Value = value };
    public static Result<T> Failure(string error) => new() { IsSuccess = false, Error = error };
}

// Usage
public Result<VectorDocument> LoadSvg(string path)
{
    if (!File.Exists(path))
        return Result<VectorDocument>.Failure("File not found");
    
    try
    {
        var doc = ParseSvg(path);
        return Result<VectorDocument>.Success(doc);
    }
    catch (XmlException ex)
    {
        return Result<VectorDocument>.Failure($"Invalid XML: {ex.Message}");
    }
}
```

---

## Logging with Serilog

### Log Levels
| Level | Usage |
|-------|-------|
| `Verbose` | Detailed debugging, inner loops |
| `Debug` | Development diagnostics |
| `Information` | Normal operations (file opened, saved) |
| `Warning` | Recoverable issues, deprecated usage |
| `Error` | Errors that affect operation but app continues |
| `Fatal` | Application-terminating errors |

### Structured Logging
```csharp
// ✅ Use structured logging with properties
Log.Information("Document {FileName} loaded in {Duration}ms", 
    fileName, stopwatch.ElapsedMilliseconds);

Log.Warning("Layer {LayerId} has {ElementCount} elements, consider grouping", 
    layer.Id, layer.Elements.Count);

Log.Error(ex, "Failed to export {FileName} to {Format}", fileName, format);

// ❌ Avoid string interpolation (loses structure)
Log.Information($"Document {fileName} loaded"); // BAD - not structured

// ✅ Include context in scopes
using (Log.Logger.BeginScope("Document: {DocumentId}", doc.Id))
{
    // All logs in this scope include DocumentId
    ProcessDocument(doc);
}
```

### Logger Configuration
```csharp
// In App.xaml.cs
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .WriteTo.File(
        path: "logs/bezier-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 7,
        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{Level:u3}] {Message:lj}{NewLine}{Exception}")
    .CreateLogger();
```

---

## Dependency Injection

### Service Lifetimes
| Lifetime | Usage | Example |
|----------|-------|---------|
| `Singleton` | Shared state, expensive to create | `ILogger`, `ISettingsService` |
| `Scoped` | Per-operation state | `IUndoService` (per document) |
| `Transient` | Lightweight, stateless | `ISvgParser`, `IExporter` |

### Registration Patterns
```csharp
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddBezierServices(this IServiceCollection services)
    {
        // Core services
        services.AddSingleton<ISettingsService, SettingsService>();
        services.AddSingleton<IThemeService, ThemeService>();
        
        // Document services (transient - new instance per request)
        services.AddTransient<ISvgParser, SvgParser>();
        services.AddTransient<ISvgExporter, SvgExporter>();
        
        // ViewModels (transient for fresh instances)
        services.AddTransient<MainWindowViewModel>();
        services.AddTransient<PropertiesViewModel>();
        
        // Factory pattern for complex creation
        services.AddSingleton<IDocumentFactory, DocumentFactory>();
        
        return services;
    }
}

// ✅ Use constructor injection
public class EditorViewModel(
    ISettingsService settings,
    ISvgParser parser,
    ILogger<EditorViewModel> logger)
{
    // Primary constructor captures dependencies
}

// ❌ Avoid service locator pattern
var service = App.Services.GetService<IFoo>(); // BAD in most cases
```

---

## Git Commit Conventions

### Conventional Commits Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Commit Types
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |

### Examples
```bash
# Features
feat(editor): add pen tool with bezier curve support
feat(export): implement PNG export with transparency

# Fixes
fix(renderer): correct anti-aliasing on retina displays
fix(layers): prevent crash when deleting active layer

# Docs
docs: update README with installation instructions
docs(api): add XML comments to VectorElement

# Refactor
refactor(core): extract fill logic to IFill interface
refactor: simplify undo/redo command pattern

# Performance
perf(canvas): use object pooling for shape rendering
perf: reduce memory allocations in hot path
```

---

## XML Documentation

### When to Document
- ✅ All public APIs (classes, methods, properties)
- ✅ Complex algorithms or non-obvious logic
- ✅ Parameters with specific constraints
- ❌ Private implementation details (unless complex)
- ❌ Self-explanatory code

### Documentation Format
```csharp
/// <summary>
/// Represents a rectangle element in an SVG document.
/// </summary>
/// <remarks>
/// Supports rounded corners via <see cref="CornerRadius"/>.
/// </remarks>
public class SvgRect : VectorElement
{
    /// <summary>
    /// Gets or sets the corner radius for rounded rectangles.
    /// </summary>
    /// <value>
    /// A value of 0 creates sharp corners. Values greater than half 
    /// the width or height are clamped.
    /// </value>
    public double CornerRadius { get; set; }
    
    /// <summary>
    /// Transforms this rectangle by the specified matrix.
    /// </summary>
    /// <param name="matrix">The transformation matrix to apply.</param>
    /// <exception cref="ArgumentNullException">
    /// Thrown when <paramref name="matrix"/> is null.
    /// </exception>
    /// <returns>A new transformed rectangle.</returns>
    public SvgRect Transform(Matrix matrix)
    {
        ArgumentNullException.ThrowIfNull(matrix);
        // ...
    }
}
```

---

## Performance Guidelines

### Memory Allocation
```csharp
// ✅ Use ArrayPool for temporary buffers
var buffer = ArrayPool<byte>.Shared.Rent(4096);
try
{
    ProcessData(buffer);
}
finally
{
    ArrayPool<byte>.Shared.Return(buffer);
}

// ✅ Use stackalloc for small, fixed-size allocations
Span<byte> buffer = stackalloc byte[256];

// ✅ Avoid LINQ in hot paths (allocates iterators)
// Instead of: elements.Where(e => e.IsVisible).ToList()
foreach (var element in elements)
{
    if (element.IsVisible)
        ProcessElement(element);
}

// ✅ Use StringBuilder for string concatenation in loops
var sb = new StringBuilder();
foreach (var item in items)
    sb.Append(item);

// ❌ Avoid boxing value types
object boxed = 42; // Allocates!
```

### Object Pooling (for hot paths like rendering)
```csharp
// ✅ Use ObjectPool for frequently created objects
public class ShapeRendererPool
{
    private static readonly ObjectPool<ShapeRenderer> _pool = 
        new DefaultObjectPool<ShapeRenderer>(new DefaultPooledObjectPolicy<ShapeRenderer>());
    
    public static ShapeRenderer Rent() => _pool.Get();
    public static void Return(ShapeRenderer renderer) => _pool.Return(renderer);
}

// Usage in render loop
var renderer = ShapeRendererPool.Rent();
try
{
    renderer.Render(canvas, element);
}
finally
{
    ShapeRendererPool.Return(renderer);
}
```

### Caching Strategies
```csharp
// ✅ Cache computed values that are expensive
private SKPath? _cachedPath;
private bool _pathDirty = true;

public SKPath GetPath()
{
    if (_pathDirty || _cachedPath == null)
    {
        _cachedPath = ComputePath();
        _pathDirty = false;
    }
    return _cachedPath;
}

// Invalidate on change
public double X
{
    get => field;
    set
    {
        if (field != value)
        {
            field = value;
            _pathDirty = true;
        }
    }
}
```

### Avoid Common Pitfalls
```csharp
// ❌ Creating delegates in loops
foreach (var item in items)
    button.Click += (s, e) => Process(item); // Allocates each iteration!

// ✅ Use a method group or cached delegate
foreach (var item in items)
    item.Process(); // Or cache the delegate

// ❌ Frequent small allocations in render loop
void Render()
{
    var brush = new SolidColorBrush(color); // Allocates every frame!
}

// ✅ Cache or pool resources
private readonly SolidColorBrush _brush = new();
void Render()
{
    _brush.Color = color; // Reuse existing object
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2025 | Initial .NET 10 / C# 14 standards |
| 1.1 | Dec 2025 | Added Error Handling, Logging, DI, Git, Docs, Performance |

