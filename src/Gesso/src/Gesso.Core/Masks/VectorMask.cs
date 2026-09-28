namespace Gesso.Core.Masks;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Represents a resolution-independent vector mask using path data.
/// </summary>
public sealed partial class VectorMask : ObservableObject
{
    [ObservableProperty]
    private bool _isEnabled = true;

    [ObservableProperty]
    private bool _isLinked = true;

    [ObservableProperty]
    private bool _isInverted;

    [ObservableProperty]
    private float _feather;

    [ObservableProperty]
    private float _density = 1.0f;

    /// <summary>
    /// Gets or sets the path data in SVG path format.
    /// </summary>
    public string PathData { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the list of path segments.
    /// </summary>
    public List<VectorPathSegment> Segments { get; } = [];

    /// <summary>
    /// Adds a move-to command.
    /// </summary>
    public void MoveTo(float x, float y)
    {
        Segments.Add(new VectorPathSegment(PathCommand.MoveTo, x, y));
    }

    /// <summary>
    /// Adds a line-to command.
    /// </summary>
    public void LineTo(float x, float y)
    {
        Segments.Add(new VectorPathSegment(PathCommand.LineTo, x, y));
    }

    /// <summary>
    /// Adds a cubic bezier curve.
    /// </summary>
    public void CurveTo(float cp1X, float cp1Y, float cp2X, float cp2Y, float endX, float endY)
    {
        Segments.Add(new VectorPathSegment(PathCommand.CurveTo, cp1X, cp1Y, cp2X, cp2Y, endX, endY));
    }

    /// <summary>
    /// Adds a quadratic bezier curve.
    /// </summary>
    public void QuadTo(float cpX, float cpY, float endX, float endY)
    {
        Segments.Add(new VectorPathSegment(PathCommand.QuadTo, cpX, cpY, endX, endY));
    }

    /// <summary>
    /// Closes the current path.
    /// </summary>
    public void ClosePath()
    {
        Segments.Add(new VectorPathSegment(PathCommand.Close));
    }

    /// <summary>
    /// Clears all path segments.
    /// </summary>
    public void Clear()
    {
        Segments.Clear();
        PathData = string.Empty;
    }

    /// <summary>
    /// Rasterizes the vector mask to a LayerMask at the specified resolution.
    /// </summary>
    public LayerMask Rasterize(int width, int height)
    {
        var mask = new LayerMask(width, height, 0);

        if (Segments.Count == 0)
            return mask;

        // Simple scanline rasterization
        var points = GetPathPoints(width, height);
        if (points.Count < 3)
            return mask;

        RasterizePolygon(mask, points);

        if (IsInverted)
            mask.InvertData();

        if (Feather > 0)
            mask.ApplyFeather(Feather);

        return mask;
    }

    private List<(float X, float Y)> GetPathPoints(int width, int height)
    {
        var points = new List<(float X, float Y)>();
        float currentX = 0, currentY = 0;

        foreach (var segment in Segments)
        {
            switch (segment.Command)
            {
                case PathCommand.MoveTo:
                    currentX = segment.Points[0];
                    currentY = segment.Points[1];
                    points.Add((currentX, currentY));
                    break;

                case PathCommand.LineTo:
                    currentX = segment.Points[0];
                    currentY = segment.Points[1];
                    points.Add((currentX, currentY));
                    break;

                case PathCommand.CurveTo:
                    // Flatten cubic bezier to line segments
                    FlattenCubicBezier(points, currentX, currentY,
                        segment.Points[0], segment.Points[1],
                        segment.Points[2], segment.Points[3],
                        segment.Points[4], segment.Points[5]);
                    currentX = segment.Points[4];
                    currentY = segment.Points[5];
                    break;

                case PathCommand.QuadTo:
                    // Flatten quadratic bezier to line segments
                    FlattenQuadBezier(points, currentX, currentY,
                        segment.Points[0], segment.Points[1],
                        segment.Points[2], segment.Points[3]);
                    currentX = segment.Points[2];
                    currentY = segment.Points[3];
                    break;

                case PathCommand.Close:
                    // Path will be closed automatically
                    break;
            }
        }

        return points;
    }

    private static void FlattenCubicBezier(List<(float X, float Y)> points,
        float x0, float y0, float x1, float y1, float x2, float y2, float x3, float y3,
        int segments = 16)
    {
        for (int i = 1; i <= segments; i++)
        {
            float t = i / (float)segments;
            float u = 1 - t;
            float tt = t * t;
            float uu = u * u;
            float uuu = uu * u;
            float ttt = tt * t;

            float x = uuu * x0 + 3 * uu * t * x1 + 3 * u * tt * x2 + ttt * x3;
            float y = uuu * y0 + 3 * uu * t * y1 + 3 * u * tt * y2 + ttt * y3;

            points.Add((x, y));
        }
    }

    private static void FlattenQuadBezier(List<(float X, float Y)> points,
        float x0, float y0, float x1, float y1, float x2, float y2,
        int segments = 12)
    {
        for (int i = 1; i <= segments; i++)
        {
            float t = i / (float)segments;
            float u = 1 - t;
            float tt = t * t;
            float uu = u * u;

            float x = uu * x0 + 2 * u * t * x1 + tt * x2;
            float y = uu * y0 + 2 * u * t * y1 + tt * y2;

            points.Add((x, y));
        }
    }

    private static void RasterizePolygon(LayerMask mask, List<(float X, float Y)> points)
    {
        int minY = (int)points.Min(p => p.Y);
        int maxY = (int)points.Max(p => p.Y);

        minY = Math.Max(0, minY);
        maxY = Math.Min(mask.Height - 1, maxY);

        for (int y = minY; y <= maxY; y++)
        {
            var intersections = new List<float>();

            for (int i = 0; i < points.Count; i++)
            {
                int j = (i + 1) % points.Count;
                var p1 = points[i];
                var p2 = points[j];

                if ((p1.Y <= y && p2.Y > y) || (p2.Y <= y && p1.Y > y))
                {
                    float x = p1.X + (y - p1.Y) / (p2.Y - p1.Y) * (p2.X - p1.X);
                    intersections.Add(x);
                }
            }

            intersections.Sort();

            for (int i = 0; i < intersections.Count - 1; i += 2)
            {
                int x1 = Math.Max(0, (int)intersections[i]);
                int x2 = Math.Min(mask.Width - 1, (int)intersections[i + 1]);

                for (int x = x1; x <= x2; x++)
                {
                    mask.SetValue(x, y, 255);
                }
            }
        }
    }

    /// <summary>
    /// Creates a copy of this vector mask.
    /// </summary>
    public VectorMask Clone()
    {
        var clone = new VectorMask
        {
            IsEnabled = IsEnabled,
            IsLinked = IsLinked,
            IsInverted = IsInverted,
            Feather = Feather,
            Density = Density,
            PathData = PathData
        };

        foreach (var segment in Segments)
        {
            clone.Segments.Add(segment.Clone());
        }

        return clone;
    }
}

/// <summary>
/// Vector path commands.
/// </summary>
public enum PathCommand
{
    MoveTo,
    LineTo,
    CurveTo,
    QuadTo,
    Close
}

/// <summary>
/// A single segment of a vector path.
/// </summary>
public sealed class VectorPathSegment
{
    public PathCommand Command { get; }
    public float[] Points { get; }

    public VectorPathSegment(PathCommand command, params float[] points)
    {
        Command = command;
        Points = points;
    }

    public VectorPathSegment Clone()
    {
        return new VectorPathSegment(Command, (float[])Points.Clone());
    }
}
