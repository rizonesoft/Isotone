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

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2025 | Initial .NET 10 / C# 14 standards |
