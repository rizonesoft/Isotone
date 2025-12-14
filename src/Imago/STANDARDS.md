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

---

*Last Updated: December 2024*
