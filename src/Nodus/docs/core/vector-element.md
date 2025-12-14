# Vector Element

`VectorElement` is the abstract base class for all shapes and objects in a Bezier document, including rectangles, circles, paths, text, images, and groups.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `Id` | `Guid` | Unique identifier (auto-generated) |
| `Name` | `string` | User-facing label, used as SVG `id` attribute |
| `IsVisible` | `bool` | Whether element is rendered (default: true) |
| `IsLocked` | `bool` | Whether element can be selected/edited (default: false) |
| `Opacity` | `double` | 0.0 (transparent) to 1.0 (opaque), auto-clamped |
| `BlendMode` | `BlendMode` | Compositing mode (Normal, Multiply, Screen, etc.) |
| `Transform` | `Transform` | Transformation matrix (translate, rotate, scale, skew) |
| `Parent` | `VectorElement?` | Parent group if nested |
| `Fill` | `IFill?` | Fill appearance (solid, gradient, pattern, or none) |
| `Stroke` | `Stroke?` | Outline appearance or none |

## Blend Modes

| Mode | Description |
|------|-------------|
| Normal | Standard compositing |
| Multiply | Darkens by multiplying colors |
| Screen | Lightens by inverting, multiplying, inverting |
| Overlay | Combines Multiply and Screen |
| Darken | Keeps darker pixels |
| Lighten | Keeps lighter pixels |
| ColorDodge | Brightens to reflect blend color |
| ColorBurn | Darkens to reflect blend color |
| HardLight | Intense highlight/shadow |
| SoftLight | Subtle highlight/shadow |
| Difference | Subtracts darker from lighter |
| Exclusion | Lower contrast version of Difference |

## Methods

### `Clone()`
Creates a deep copy of the element with a new Id.

### `HitTest(x, y)`
Tests if a point (in world coordinates) intersects this element. Accounts for transform.

### `GetBoundingBox()`
Returns the axis-aligned bounding box in world coordinates as `(X, Y, Width, Height)`.

### `ToSvgString()`
Serializes the element to an SVG string.

## Element Types

| Type | Description |
|------|-------------|
| `SvgRect` | Rectangle with optional rounded corners |
| `SvgCircle` | Circle defined by center and radius |
| `SvgEllipse` | Ellipse defined by center and radii |
| `SvgLine` | Line between two points |
| `SvgPath` | Arbitrary path with bezier curves |
| `SvgPolygon` | Closed polygon |
| `SvgPolyline` | Open polyline |
| `SvgText` | Text with font properties |
| `SvgImage` | Embedded or linked raster image |
| `SvgGroup` | Container for child elements |

## Example

```csharp
// Create a rectangle
var rect = new SvgRect
{
    Name = "my-rectangle",
    X = 100,
    Y = 50,
    Width = 200,
    Height = 100,
    Fill = new SolidFill(Color.Blue),
    Stroke = new Stroke { Width = 2, Fill = new SolidFill(Color.Black) },
    Opacity = 0.8
};

// Transform it
rect.Transform = Transform.Identity
    .Rotate(45)
    .Scale(1.5, 1.5);

// Check visibility
if (rect.IsVisible && !rect.IsLocked)
{
    // Element can be rendered and edited
}
```

## Related

- [Vector Document](vector-document.md) — Document container
- [Fill Types](../fills/README.md) — SolidFill, GradientFill, PatternFill
- [Transform](transform.md) — Transformation matrix
