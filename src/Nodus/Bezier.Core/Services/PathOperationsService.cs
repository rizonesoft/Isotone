namespace Bezier.Core.Services;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;

/// <summary>
/// Type of boolean operation.
/// </summary>
public enum BooleanOperation
{
    /// <summary>Union - Combine shapes into one.</summary>
    Union,
    /// <summary>Subtract - Cut the second shape from the first.</summary>
    Subtract,
    /// <summary>Intersect - Keep only the common area.</summary>
    Intersect,
    /// <summary>Exclude - XOR, remove overlap.</summary>
    Exclude
}

/// <summary>
/// Join type for path offset operations.
/// </summary>
public enum PathJoinType
{
    Miter,
    Round,
    Bevel
}

/// <summary>
/// Result of a path operation.
/// </summary>
public record PathOperationResult(
    bool Success,
    string? PathData,
    string? ErrorMessage
);

/// <summary>
/// Service for advanced path operations like boolean operations, simplification, and offset.
/// </summary>
public class PathOperationsService
{
    /// <summary>
    /// Performs a boolean operation on two paths.
    /// </summary>
    /// <param name="pathData1">First path data (SVG path string).</param>
    /// <param name="pathData2">Second path data (SVG path string).</param>
    /// <param name="operation">The boolean operation to perform.</param>
    /// <returns>Result containing the combined path data.</returns>
    public PathOperationResult BooleanOp(string pathData1, string pathData2, BooleanOperation operation)
    {
        if (string.IsNullOrEmpty(pathData1))
            return new PathOperationResult(false, null, "First path is empty");
        if (string.IsNullOrEmpty(pathData2))
            return new PathOperationResult(false, null, "Second path is empty");

        // This will be implemented with SkiaSharp in the Desktop layer
        // For now, return a placeholder that indicates the operation type
        return new PathOperationResult(true, pathData1, null);
    }

    /// <summary>
    /// Performs a boolean operation on multiple paths.
    /// </summary>
    public PathOperationResult BooleanOpMultiple(IEnumerable<string> pathDataList, BooleanOperation operation)
    {
        var paths = pathDataList.ToList();
        if (paths.Count == 0)
            return new PathOperationResult(false, null, "No paths provided");
        if (paths.Count == 1)
            return new PathOperationResult(true, paths[0], null);

        var result = paths[0];
        for (var i = 1; i < paths.Count; i++)
        {
            var opResult = BooleanOp(result, paths[i], operation);
            if (!opResult.Success)
                return opResult;
            result = opResult.PathData!;
        }

        return new PathOperationResult(true, result, null);
    }

    /// <summary>
    /// Simplifies a path by reducing the number of points.
    /// </summary>
    /// <param name="pathData">The path data to simplify.</param>
    /// <param name="tolerance">Tolerance for point removal (higher = more simplification).</param>
    /// <returns>Simplified path data.</returns>
    public PathOperationResult Simplify(string pathData, double tolerance = 1.0)
    {
        if (string.IsNullOrEmpty(pathData))
            return new PathOperationResult(false, null, "Path is empty");

        // Placeholder - actual implementation uses SkiaSharp
        return new PathOperationResult(true, pathData, null);
    }

    /// <summary>
    /// Creates an offset path (inset or outset).
    /// </summary>
    /// <param name="pathData">The path data to offset.</param>
    /// <param name="distance">Offset distance (positive = outset, negative = inset).</param>
    /// <param name="joinType">How corners are handled.</param>
    /// <param name="miterLimit">Miter limit for sharp corners.</param>
    /// <returns>Offset path data.</returns>
    public PathOperationResult Offset(string pathData, double distance, PathJoinType joinType = PathJoinType.Round, double miterLimit = 4.0)
    {
        if (string.IsNullOrEmpty(pathData))
            return new PathOperationResult(false, null, "Path is empty");
        if (Math.Abs(distance) < 0.001)
            return new PathOperationResult(true, pathData, null);

        // Placeholder - actual implementation uses SkiaSharp path effects
        return new PathOperationResult(true, pathData, null);
    }

    /// <summary>
    /// Converts a stroked path to a filled outline path.
    /// </summary>
    /// <param name="pathData">The path data.</param>
    /// <param name="strokeWidth">Width of the stroke to convert.</param>
    /// <param name="lineCap">Line cap style.</param>
    /// <param name="lineJoin">Line join style.</param>
    /// <param name="miterLimit">Miter limit for joins.</param>
    /// <returns>Outline path data.</returns>
    public PathOperationResult StrokeToPath(
        string pathData,
        double strokeWidth,
        LineCap lineCap = LineCap.Butt,
        LineJoin lineJoin = LineJoin.Miter,
        double miterLimit = 4.0)
    {
        if (string.IsNullOrEmpty(pathData))
            return new PathOperationResult(false, null, "Path is empty");
        if (strokeWidth <= 0)
            return new PathOperationResult(false, null, "Stroke width must be positive");

        // Placeholder - actual implementation uses SkiaSharp
        return new PathOperationResult(true, pathData, null);
    }

    /// <summary>
    /// Converts text to a path.
    /// </summary>
    /// <param name="text">The text to convert.</param>
    /// <param name="fontFamily">Font family name.</param>
    /// <param name="fontSize">Font size in pixels.</param>
    /// <param name="fontWeight">Font weight (100-900).</param>
    /// <param name="italic">Whether the font is italic.</param>
    /// <returns>Path data representing the text.</returns>
    public PathOperationResult TextToPath(
        string text,
        string fontFamily = "Arial",
        double fontSize = 24,
        int fontWeight = 400,
        bool italic = false)
    {
        if (string.IsNullOrEmpty(text))
            return new PathOperationResult(false, null, "Text is empty");

        // Placeholder - actual implementation uses SkiaSharp
        return new PathOperationResult(true, "M0,0", null);
    }

    /// <summary>
    /// Reverses the direction of a path.
    /// </summary>
    public PathOperationResult ReversePath(string pathData)
    {
        if (string.IsNullOrEmpty(pathData))
            return new PathOperationResult(false, null, "Path is empty");

        // Placeholder - actual implementation parses and reverses commands
        return new PathOperationResult(true, pathData, null);
    }

    /// <summary>
    /// Closes all open subpaths.
    /// </summary>
    public PathOperationResult ClosePath(string pathData)
    {
        if (string.IsNullOrEmpty(pathData))
            return new PathOperationResult(false, null, "Path is empty");

        // Simple implementation: ensure path ends with Z
        var trimmed = pathData.TrimEnd();
        if (!trimmed.EndsWith('Z') && !trimmed.EndsWith('z'))
        {
            return new PathOperationResult(true, trimmed + " Z", null);
        }

        return new PathOperationResult(true, pathData, null);
    }

    /// <summary>
    /// Gets the bounding box of a path.
    /// </summary>
    public (double X, double Y, double Width, double Height)? GetPathBounds(string pathData)
    {
        if (string.IsNullOrEmpty(pathData))
            return null;

        // Placeholder - actual implementation parses path and calculates bounds
        return (0, 0, 100, 100);
    }

    /// <summary>
    /// Checks if a point is inside a path.
    /// </summary>
    public bool ContainsPoint(string pathData, double x, double y)
    {
        if (string.IsNullOrEmpty(pathData))
            return false;

        // Placeholder - actual implementation uses SkiaSharp contains
        return false;
    }

    /// <summary>
    /// Splits a path at the specified parameter (0-1).
    /// </summary>
    public (PathOperationResult First, PathOperationResult Second) SplitPath(string pathData, double t)
    {
        if (string.IsNullOrEmpty(pathData))
        {
            var error = new PathOperationResult(false, null, "Path is empty");
            return (error, error);
        }

        t = Math.Clamp(t, 0, 1);

        // Placeholder - actual implementation splits at parameter
        return (
            new PathOperationResult(true, pathData, null),
            new PathOperationResult(true, pathData, null)
        );
    }

    /// <summary>
    /// Flattens curves to line segments.
    /// </summary>
    /// <param name="pathData">Path data with curves.</param>
    /// <param name="tolerance">Flatness tolerance.</param>
    /// <returns>Path data with only line segments.</returns>
    public PathOperationResult FlattenPath(string pathData, double tolerance = 0.5)
    {
        if (string.IsNullOrEmpty(pathData))
            return new PathOperationResult(false, null, "Path is empty");

        // Placeholder - actual implementation uses SkiaSharp
        return new PathOperationResult(true, pathData, null);
    }

    /// <summary>
    /// Converts a rectangle to a path.
    /// </summary>
    public string RectToPath(double x, double y, double width, double height, double rx = 0, double ry = 0)
    {
        if (rx <= 0 && ry <= 0)
        {
            return $"M {x} {y} L {x + width} {y} L {x + width} {y + height} L {x} {y + height} Z";
        }

        // Rounded rectangle
        rx = Math.Min(rx, width / 2);
        ry = Math.Min(ry, height / 2);

        return $"M {x + rx} {y} " +
               $"L {x + width - rx} {y} " +
               $"A {rx} {ry} 0 0 1 {x + width} {y + ry} " +
               $"L {x + width} {y + height - ry} " +
               $"A {rx} {ry} 0 0 1 {x + width - rx} {y + height} " +
               $"L {x + rx} {y + height} " +
               $"A {rx} {ry} 0 0 1 {x} {y + height - ry} " +
               $"L {x} {y + ry} " +
               $"A {rx} {ry} 0 0 1 {x + rx} {y} Z";
    }

    /// <summary>
    /// Converts an ellipse to a path.
    /// </summary>
    public string EllipseToPath(double cx, double cy, double rx, double ry)
    {
        return $"M {cx - rx} {cy} " +
               $"A {rx} {ry} 0 1 0 {cx + rx} {cy} " +
               $"A {rx} {ry} 0 1 0 {cx - rx} {cy} Z";
    }

    /// <summary>
    /// Converts a circle to a path.
    /// </summary>
    public string CircleToPath(double cx, double cy, double r)
    {
        return EllipseToPath(cx, cy, r, r);
    }

    /// <summary>
    /// Converts a line to a path.
    /// </summary>
    public string LineToPath(double x1, double y1, double x2, double y2)
    {
        return $"M {x1} {y1} L {x2} {y2}";
    }

    /// <summary>
    /// Converts a polygon points string to a path.
    /// </summary>
    public string PolygonToPath(string points)
    {
        if (string.IsNullOrEmpty(points))
            return string.Empty;

        var coords = points.Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
        if (coords.Length < 4)
            return string.Empty;

        var path = $"M {coords[0]} {coords[1]}";
        for (var i = 2; i < coords.Length - 1; i += 2)
        {
            path += $" L {coords[i]} {coords[i + 1]}";
        }
        path += " Z";

        return path;
    }

    /// <summary>
    /// Converts a polyline points string to a path.
    /// </summary>
    public string PolylineToPath(string points)
    {
        if (string.IsNullOrEmpty(points))
            return string.Empty;

        var coords = points.Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
        if (coords.Length < 4)
            return string.Empty;

        var path = $"M {coords[0]} {coords[1]}";
        for (var i = 2; i < coords.Length - 1; i += 2)
        {
            path += $" L {coords[i]} {coords[i + 1]}";
        }

        return path;
    }
}
