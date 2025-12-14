# SVG Path Element

`SvgPath` represents an arbitrary path defined by SVG path commands. It's the most flexible shape type, supporting lines, curves, and arcs.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `PathData` | `string` | SVG path data (d attribute) |
| *Inherited* | | All properties from [VectorElement](vector-element.md) |

## Methods

### `GetPathPoints()`
Returns all points from the path (including control points) as a list of `(X, Y)` tuples.

### `InvalidateBounds()`
Clears the cached bounding box, forcing recalculation on next access.

## Path Data Syntax

SVG paths use a series of commands:

| Command | Name | Parameters | Description |
|---------|------|------------|-------------|
| `M` / `m` | Move to | x, y | Start a new subpath |
| `L` / `l` | Line to | x, y | Draw a straight line |
| `H` / `h` | Horizontal | x | Horizontal line |
| `V` / `v` | Vertical | y | Vertical line |
| `C` / `c` | Cubic Bezier | x1, y1, x2, y2, x, y | Smooth curve with 2 control points |
| `S` / `s` | Smooth Cubic | x2, y2, x, y | Continues previous curve |
| `Q` / `q` | Quadratic | x1, y1, x, y | Curve with 1 control point |
| `T` / `t` | Smooth Quad | x, y | Continues previous quadratic |
| `A` / `a` | Arc | rx, ry, rotation, large, sweep, x, y | Elliptical arc |
| `Z` / `z` | Close | — | Close path to start |

- **Uppercase** = absolute coordinates
- **Lowercase** = relative to current position

## Examples

```csharp
// Simple triangle
var triangle = new SvgPath
{
    PathData = "M 100,10 L 40,180 L 190,60 Z",
    Fill = new SolidFill(Colors.Blue)
};

// Bezier curve
var curve = new SvgPath
{
    PathData = "M 10,80 C 40,10 65,10 95,80 S 150,150 180,80",
    Stroke = new Stroke { Width = 2, Fill = new SolidFill(Colors.Red) }
};

// Heart shape
var heart = new SvgPath
{
    PathData = "M 10,30 A 20,20 0,0,1 50,30 A 20,20 0,0,1 90,30 Q 90,60 50,90 Q 10,60 10,30 Z"
};

// Get all path points
var points = curve.GetPathPoints();
Console.WriteLine($"Path has {points.Count} points");
```

## Performance

- Bounding box is **cached** — first access parses the path, subsequent accesses are instant
- Call `InvalidateBounds()` if you modify `PathData` and need to recalculate
- Hit testing uses bounding box + stroke tolerance for efficiency

## Related

- [Vector Element](vector-element.md) — Base class
- [Pen Tool](../tools/pen-tool.md) — Creating paths interactively
- [Node Editing](../tools/node-editing.md) — Editing path nodes
