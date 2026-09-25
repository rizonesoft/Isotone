# 📐 Imago Coding Standards

> C# 14 / .NET 10 / High-Performance Graphics Application

---

## 🎯 Core Principles

1. **Performance First** - Zero allocations in hot paths (rendering, input handling)
2. **Readability** - Code should be self-documenting
3. **Consistency** - Follow established patterns throughout
4. **Testability** - Design for unit testing

---

## 📝 Naming Conventions

### General Rules

| Element | Convention | Example |
|---------|------------|---------|
| Namespace | PascalCase | `Imago.Rendering.Shaders` |
| Class | PascalCase | `TileCache` |
| Interface | IPascalCase | `IRenderNode` |
| Method | PascalCase | `RenderTile()` |
| Property | PascalCase | `LayerCount` |
| Field (private) | _camelCase | `_tileCache` |
| Field (const) | PascalCase | `MaxTileSize` |
| Parameter | camelCase | `layerIndex` |
| Local variable | camelCase | `currentTile` |
| Generic type | T + PascalCase | `TPixel`, `TState` |

### Specific Patterns

```csharp
// ✅ Good
public class LayerManager
{
    private readonly ITileCache _tileCache;
    private int _activeLayerIndex;
    
    public int LayerCount { get; private set; }
    
    public void AddLayer(Layer layer) { }
}

// ❌ Bad
public class layerManager
{
    private ITileCache tileCache;
    private int ActiveLayerIndex;
    
    public int layerCount { get; private set; }
    
    public void addLayer(Layer Layer) { }
}
```

---

## 🏗 Code Structure

### File Organization

```csharp
// 1. File-scoped namespace (C# 10+)
namespace Imago.Core.Layers;

// 2. Using statements (inside namespace for file-scoped)
using System.Buffers;
using Imago.Core.Rendering;

// 3. Type definition
public sealed class RasterLayer : Layer
{
    // 4. Constants
    private const int DefaultTileSize = 256;
    
    // 5. Static fields
    private static readonly ArrayPool<byte> s_pixelPool = ArrayPool<byte>.Shared;
    
    // 6. Instance fields
    private readonly ITileCache _tileCache;
    private bool _isDirty;
    
    // 7. Constructors
    public RasterLayer(int width, int height) { }
    
    // 8. Properties
    public int Width { get; }
    public int Height { get; }
    
    // 9. Public methods
    public void Render(RenderContext context) { }
    
    // 10. Private methods
    private void InvalidateTiles() { }
}
```

### Class Design

```csharp
// Prefer sealed classes unless inheritance is intended
public sealed class TileCache : ITileCache
{
    // Use primary constructors where appropriate (C# 12+)
}

// Use records for immutable data
public readonly record struct TileCoordinate(int X, int Y);

// Use init-only properties for immutable configuration
public sealed class RenderSettings
{
    public required int MaxTiles { get; init; }
    public required bool UseGpu { get; init; }
}
```

---

## ⚡ Performance Guidelines

### Zero-Allocation Hot Paths

```csharp
// ✅ Good - Stack allocation
public void ProcessPixels(ReadOnlySpan<byte> source, Span<byte> destination)
{
    Span<float> temp = stackalloc float[4]; // Stack allocated
    // Process...
}

// ❌ Bad - Heap allocation in hot path
public void ProcessPixels(byte[] source, byte[] destination)
{
    var temp = new float[4]; // Heap allocation!
    // Process...
}
```

### Use Span<T> and Memory<T>

```csharp
// ✅ Good
public void CopyTile(ReadOnlySpan<byte> source, Span<byte> destination)
{
    source.CopyTo(destination);
}

// ❌ Bad
public void CopyTile(byte[] source, byte[] destination)
{
    Array.Copy(source, destination, source.Length);
}
```

### Object Pooling

```csharp
// Use ArrayPool for temporary buffers
public void ProcessImage()
{
    byte[] buffer = ArrayPool<byte>.Shared.Rent(1024);
    try
    {
        // Use buffer...
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}

// Or use ObjectPool<T> for complex objects
private static readonly ObjectPool<RenderContext> s_contextPool = 
    new DefaultObjectPool<RenderContext>(new RenderContextPolicy());
```

### SIMD Operations

```csharp
using System.Numerics;
using System.Runtime.Intrinsics;
using System.Runtime.Intrinsics.X86;

// Use Vector<T> for portable SIMD
public static void MultiplyAlpha(Span<float> pixels, float alpha)
{
    var alphaVec = new Vector<float>(alpha);
    int vectorSize = Vector<float>.Count;
    
    int i = 0;
    for (; i <= pixels.Length - vectorSize; i += vectorSize)
    {
        var vec = new Vector<float>(pixels.Slice(i));
        (vec * alphaVec).CopyTo(pixels.Slice(i));
    }
    
    // Handle remainder
    for (; i < pixels.Length; i++)
    {
        pixels[i] *= alpha;
    }
}
```

### Avoid Boxing

```csharp
// ✅ Good - Generic constraint
public void Log<T>(T value) where T : struct
{
    _logger.Information("{Value}", value);
}

// ❌ Bad - Boxing occurs
public void Log(object value)
{
    _logger.Information("{Value}", value);
}
```

---

## 🔒 Null Safety

### Enable Nullable Reference Types

```xml
<!-- In .csproj -->
<Nullable>enable</Nullable>
```

```csharp
// Be explicit about nullability
public Layer? FindLayer(string name) { }

public void ProcessLayer(Layer layer)
{
    ArgumentNullException.ThrowIfNull(layer);
    // ...
}

// Use null-coalescing operators
var name = layer.Name ?? "Untitled";
var count = cache?.Count ?? 0;
```

---

## 🧪 Testing Standards

### Test Naming

```csharp
// Pattern: MethodName_Scenario_ExpectedResult
[Fact]
public void AddLayer_WhenDocumentIsEmpty_ShouldCreateFirstLayer()
{
    // Arrange
    var document = new ImagoDocument();
    var layer = new RasterLayer(100, 100);
    
    // Act
    document.AddLayer(layer);
    
    // Assert
    Assert.Single(document.Layers);
}
```

### Test Organization

```csharp
public class LayerTests
{
    public class AddLayer
    {
        [Fact]
        public void WhenDocumentIsEmpty_ShouldCreateFirstLayer() { }
        
        [Fact]
        public void WhenLayerExists_ShouldAddAboveCurrentLayer() { }
    }
    
    public class RemoveLayer
    {
        [Fact]
        public void WhenLayerExists_ShouldRemoveFromDocument() { }
    }
}
```

---

## 📊 Logging Standards

### Use Structured Logging

```csharp
// ✅ Good - Structured logging with Serilog
_logger.Information("Loading document {DocumentPath} with {LayerCount} layers", 
    path, document.Layers.Count);

// ❌ Bad - String interpolation
_logger.Information($"Loading document {path} with {document.Layers.Count} layers");
```

### Log Levels

| Level | Usage |
|-------|-------|
| Verbose | Extremely detailed, for debugging only |
| Debug | Internal system events |
| Information | Normal operations, milestones |
| Warning | Abnormal but recoverable situations |
| Error | Failures that need attention |
| Fatal | Application-stopping errors |

---

## 🖥 GPU & Shader Standards

### ComputeSharp Patterns

```csharp
// Use readonly partial struct for GPU shaders
[ThreadGroupSize(DefaultThreadGroupSizes.X)]
[GeneratedComputeShaderDescriptor]
public readonly partial struct GrayscaleShader(ReadWriteTexture2D<Rgba32, float4> texture) 
    : IComputeShader
{
    public void Execute()
    {
        float4 pixel = texture[ThreadIds.XY];
        float gray = (pixel.R * 0.299f) + (pixel.G * 0.587f) + (pixel.B * 0.114f);
        texture[ThreadIds.XY] = new float4(gray, gray, gray, pixel.A);
    }
}
```

### GPU Resource Management

```csharp
// Always dispose GPU resources
public sealed class GpuRenderer : IDisposable
{
    private readonly GraphicsDevice _device;
    private ReadWriteTexture2D<Rgba32, float4>? _texture;
    private bool _disposed;

    public void Dispose()
    {
        if (_disposed) return;
        _texture?.Dispose();
        _device.Dispose();
        _disposed = true;
    }
}

// Use using statements for temporary GPU buffers
public void ProcessOnGpu(ReadOnlySpan<byte> data)
{
    using var buffer = _device.AllocateReadOnlyBuffer(data);
    // Process...
}
```

### HLSL Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Constant Buffer | PascalCase | `cbPerFrame` |
| Texture | t + PascalCase | `tDiffuseMap` |
| Sampler | s + PascalCase | `sLinearWrap` |
| Function | PascalCase | `CalculateLighting()` |
| Local variable | camelCase | `worldPosition` |

---

## 🔄 MVVM Patterns

### ViewModel Base

```csharp
// Use ReactiveUI for reactive ViewModels
public class MainWindowViewModel : ReactiveObject
{
    private string _title = "Imago";
    
    public string Title
    {
        get => _title;
        set => this.RaiseAndSetIfChanged(ref _title, value);
    }
    
    // Use ReactiveCommand for commands
    public ReactiveCommand<Unit, Unit> SaveCommand { get; }
    
    public MainWindowViewModel()
    {
        var canSave = this.WhenAnyValue(x => x.HasUnsavedChanges);
        SaveCommand = ReactiveCommand.CreateFromTask(SaveAsync, canSave);
    }
}
```

### View-ViewModel Binding

```csharp
// Use WhenActivated for lifecycle management
public partial class MainWindow : ReactiveWindow<MainWindowViewModel>
{
    public MainWindow()
    {
        InitializeComponent();
        
        this.WhenActivated(disposables =>
        {
            this.OneWayBind(ViewModel, vm => vm.Title, v => v.Title)
                .DisposeWith(disposables);
                
            this.BindCommand(ViewModel, vm => vm.SaveCommand, v => v.SaveButton)
                .DisposeWith(disposables);
        });
    }
}
```

### Command Patterns

```csharp
// ✅ Good - Async command with cancellation
public ReactiveCommand<Unit, Unit> LoadCommand { get; }

LoadCommand = ReactiveCommand.CreateFromTask(
    async ct => await LoadDocumentAsync(ct),
    outputScheduler: RxApp.MainThreadScheduler);

// ❌ Bad - Sync command blocking UI
public ICommand LoadCommand => new RelayCommand(() => 
    LoadDocument()); // Blocks UI thread!
```

---

## 🎨 XAML Standards

### Naming in XAML

```xml
<!-- Use x:Name for elements referenced in code-behind -->
<Button x:Name="SaveButton" Content="Save" />

<!-- Use descriptive names -->
<Grid x:Name="LayerPanelContainer">
    <ListView x:Name="LayerListView" />
</Grid>
```

### Resource Organization

```xml
<!-- App.xaml -->
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ResourceDictionary Source="Themes/Colors.xaml" />
            <ResourceDictionary Source="Themes/Brushes.xaml" />
            <ResourceDictionary Source="Themes/Styles.xaml" />
            <ResourceDictionary Source="Themes/Templates.xaml" />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

---

## 📦 Dependency Injection

### Registration Pattern

```csharp
// In Startup/App configuration
services.AddSingleton<IDocumentManager, DocumentManager>();
services.AddSingleton<ITileCache, TileCache>();
services.AddTransient<IFilterFactory, FilterFactory>();
services.AddScoped<IRenderContext, RenderContext>();
```

### Constructor Injection

```csharp
public class DocumentService
{
    private readonly IDocumentManager _documentManager;
    private readonly ILogger<DocumentService> _logger;
    
    public DocumentService(
        IDocumentManager documentManager,
        ILogger<DocumentService> logger)
    {
        _documentManager = documentManager;
        _logger = logger;
    }
}
```

---

## 🔄 Async/Await Patterns

### Naming

```csharp
// Async methods end with Async
public async Task<Document> LoadDocumentAsync(string path, CancellationToken ct = default)
{
    // Always pass CancellationToken
    await using var stream = File.OpenRead(path);
    return await DeserializeAsync(stream, ct);
}
```

### ConfigureAwait

```csharp
// In library code, use ConfigureAwait(false)
public async Task ProcessAsync()
{
    await SomeOperationAsync().ConfigureAwait(false);
}

// In UI code, don't use ConfigureAwait (need UI context)
private async void OnButtonClick(object sender, RoutedEventArgs e)
{
    await LoadDocumentAsync();
    UpdateUI(); // Needs UI thread
}
```

---

## 🚫 Anti-Patterns to Avoid

### Don't

```csharp
// ❌ async void (except event handlers)
public async void LoadDocument() { }

// ❌ .Result or .Wait() - causes deadlocks
var result = SomeAsync().Result;

// ❌ Empty catch blocks
try { } catch { }

// ❌ Magic numbers
if (layer.Opacity > 0.5) { }

// ❌ God classes
public class DocumentManagerAndRendererAndIOAndEverything { }

// ❌ Mutable statics
public static List<Layer> AllLayers = new();
```

### Do

```csharp
// ✅ Return Task
public async Task LoadDocumentAsync() { }

// ✅ Await properly
var result = await SomeAsync();

// ✅ Log exceptions
try { } 
catch (Exception ex) 
{ 
    _logger.Error(ex, "Failed to process");
    throw;
}

// ✅ Named constants
private const double OpacityThreshold = 0.5;
if (layer.Opacity > OpacityThreshold) { }

// ✅ Single responsibility
public class DocumentManager { }
public class RenderEngine { }
public class FileIOService { }

// ✅ Immutable or thread-safe
private static readonly ImmutableList<Layer> s_defaultLayers = ImmutableList<Layer>.Empty;
```

---

## ✨ Modern C# 14 Features

### Collection Expressions (C# 12+)

```csharp
// ✅ Good - Collection expressions
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alpha", "Beta", "Gamma"];
Span<byte> bytes = stackalloc byte[] { 0xFF, 0x00, 0xFF };

// Spread operator
int[] combined = [..firstArray, ..secondArray, 42];

// ❌ Bad - Verbose initialization
var numbers = new int[] { 1, 2, 3, 4, 5 };
var names = new List<string> { "Alpha", "Beta", "Gamma" };
```

### Primary Constructors (C# 12+)

```csharp
// ✅ Good - Primary constructor for simple DI
public class DocumentService(ILogger<DocumentService> logger, IFileSystem fileSystem)
{
    public async Task LoadAsync(string path)
    {
        logger.Information("Loading {Path}", path);
        // Use fileSystem...
    }
}

// Use when: Simple dependency injection, data carriers
// Avoid when: Complex initialization logic, need field validation
```

### Pattern Matching Enhancements

```csharp
// Extended property patterns
if (layer is { Opacity: > 0.5, Visible: true, Parent.Name: "Background" })
{
    // Process visible layer with opacity > 50% in Background group
}

// List patterns
if (args is [var first, .., var last])
{
    Console.WriteLine($"First: {first}, Last: {last}");
}

// Switch expressions with patterns
string GetLayerIcon(Layer layer) => layer switch
{
    RasterLayer { HasMask: true } => "raster-masked",
    RasterLayer => "raster",
    VectorLayer => "vector",
    GroupLayer { Children.Count: 0 } => "folder-empty",
    GroupLayer => "folder",
    _ => "unknown"
};
```

### Required Members (C# 11+)

```csharp
// Use required for mandatory properties
public class ExportSettings
{
    public required string OutputPath { get; init; }
    public required ImageFormat Format { get; init; }
    public int Quality { get; init; } = 90; // Optional with default
}

// Must be set at initialization
var settings = new ExportSettings
{
    OutputPath = @"C:\output.png",
    Format = ImageFormat.Png
};
```

---

## 📄 Documentation Standards

### XML Documentation

```csharp
/// <summary>
/// Renders a tile at the specified coordinates.
/// </summary>
/// <param name="x">The X coordinate of the tile.</param>
/// <param name="y">The Y coordinate of the tile.</param>
/// <param name="cancellationToken">Token to cancel the operation.</param>
/// <returns>The rendered tile data, or <c>null</c> if the tile is empty.</returns>
/// <exception cref="ArgumentOutOfRangeException">
/// Thrown when coordinates are outside the document bounds.
/// </exception>
public async Task<TileData?> RenderTileAsync(
    int x, 
    int y, 
    CancellationToken cancellationToken = default)
{
    // Implementation
}
```

### Documentation Requirements

| Element | Required | Notes |
|---------|----------|-------|
| Public types | ✅ Yes | Summary required |
| Public methods | ✅ Yes | Summary + params + returns |
| Public properties | ✅ Yes | Summary required |
| Internal types | ⚠️ Recommended | For complex logic |
| Private members | ❌ No | Only if non-obvious |
| Test methods | ❌ No | Test name should be self-documenting |

---

## 🛡 Error Handling

### Exception Patterns

```csharp
// Use guard clauses with modern syntax
public void ProcessLayer(Layer layer, int index)
{
    ArgumentNullException.ThrowIfNull(layer);
    ArgumentOutOfRangeException.ThrowIfNegative(index);
    ArgumentOutOfRangeException.ThrowIfGreaterThanOrEqual(index, _layers.Count);
    
    // Main logic...
}

// Custom exceptions for domain errors
public class DocumentCorruptedException : Exception
{
    public string FilePath { get; }
    
    public DocumentCorruptedException(string filePath, string message, Exception? inner = null)
        : base(message, inner)
    {
        FilePath = filePath;
    }
}
```

### Result Pattern (for expected failures)

```csharp
// Use Result<T> for operations that can fail expectedly
public readonly record struct Result<T>
{
    public T? Value { get; }
    public string? Error { get; }
    public bool IsSuccess => Error is null;
    
    public static Result<T> Success(T value) => new() { Value = value };
    public static Result<T> Failure(string error) => new() { Error = error };
}

// Usage
public Result<Document> TryLoadDocument(string path)
{
    if (!File.Exists(path))
        return Result<Document>.Failure($"File not found: {path}");
        
    // Load and return success...
}
```

---

## 📋 Code Review Checklist

- [ ] No allocations in hot paths
- [ ] Proper null handling
- [ ] Async methods properly awaited
- [ ] CancellationToken passed through
- [ ] Exceptions logged with context
- [ ] Unit tests included
- [ ] XML documentation on public APIs
- [ ] No magic numbers
- [ ] Follows naming conventions
- [ ] No compiler warnings
- [ ] GPU resources properly disposed
- [ ] MVVM bindings use WhenActivated
- [ ] Collection expressions used where applicable

---

## 🔗 Related Resources

- [.editorconfig](/.editorconfig) - Automated style enforcement
- [CONTRIBUTING.md](/CONTRIBUTING.md) - Contribution guidelines
- [Microsoft C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [Performance Best Practices](https://learn.microsoft.com/en-us/dotnet/framework/performance/)

---

*Last Updated: December 2024*
