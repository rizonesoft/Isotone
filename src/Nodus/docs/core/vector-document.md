# Vector Document

The `VectorDocument` class is the root container for all SVG content in Bezier. It holds the canvas dimensions, metadata, elements, and definitions.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `Width` | `double` | Canvas width in pixels (must be > 0) |
| `Height` | `double` | Canvas height in pixels (must be > 0) |
| `ViewBox` | `ViewBox` | SVG viewBox for coordinate mapping |
| `Title` | `string` | Document title |
| `Author` | `string` | Author name |
| `Description` | `string` | Document description |
| `License` | `string` | License information |
| `Background` | `IFill?` | Background fill (null = transparent) |
| `IsDirty` | `bool` | True if document has unsaved changes |
| `Elements` | `ObservableCollection<VectorElement>` | All document elements |
| `Defs` | `ObservableCollection<VectorElement>` | Definitions (gradients, patterns, symbols) |

## Methods

### `MarkAsSaved()`
Sets `IsDirty` to false. Call this after saving the document.

### `Clear()`
Resets the document to default state, clearing all elements and metadata.

## Change Tracking

The document automatically tracks changes:
- Property changes set `IsDirty = true`
- Adding/removing elements sets `IsDirty = true`
- Adding/removing definitions sets `IsDirty = true`

## Validation

- **Width** and **Height** must be greater than 0
- Setting invalid values throws `ArgumentOutOfRangeException`

## Example

```csharp
var doc = new VectorDocument
{
    Width = 1920,
    Height = 1080,
    Title = "My Design",
    Background = new SolidFill(Colors.White)
};

doc.Elements.Add(new SvgRect { X = 10, Y = 10, Width = 100, Height = 100 });

// Check for unsaved changes
if (doc.IsDirty)
{
    // Save document...
    doc.MarkAsSaved();
}
```

## Related

- [Fill Types](fills.md) - SolidFill, GradientFill, PatternFill
- [Vector Elements](elements.md) - SvgRect, SvgCircle, SvgPath, etc.
