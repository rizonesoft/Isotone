namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG polyline element (open shape with straight edges).
/// </summary>
public class SvgPolyline : VectorElement
{
    private List<(double X, double Y)> _points = [];

    /// <summary>List of polyline points.</summary>
    public List<(double X, double Y)> Points
    {
        get => _points;
        set { _points = value ?? []; OnPropertyChanged(nameof(Points)); }
    }

    public override VectorElement Clone()
    {
        var clone = new SvgPolyline
        {
            Id = Guid.NewGuid(),
            Name = Name,
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            Transform = Transform,
            Fill = Fill?.Clone(),
            Stroke = Stroke?.Clone()
        };
        clone.Points = [.. Points];
        return clone;
    }

    protected override bool HitTestLocal(double x, double y)
    {
        const double tolerance = 5.0;
        
        // Check if point is within tolerance of any line segment
        for (int i = 0; i < Points.Count - 1; i++)
        {
            var x1 = Points[i].X;
            var y1 = Points[i].Y;
            var x2 = Points[i + 1].X;
            var y2 = Points[i + 1].Y;
            
            var dx = x2 - x1;
            var dy = y2 - y1;
            var lengthSq = dx * dx + dy * dy;
            
            if (lengthSq < double.Epsilon)
            {
                if (Math.Sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1)) <= tolerance)
                    return true;
                continue;
            }

            var t = Math.Clamp(((x - x1) * dx + (y - y1) * dy) / lengthSq, 0, 1);
            var projX = x1 + t * dx;
            var projY = y1 + t * dy;
            
            if (Math.Sqrt((x - projX) * (x - projX) + (y - projY) * (y - projY)) <= tolerance)
                return true;
        }
        return false;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        if (Points.Count == 0) return (0, 0, 0, 0);
        
        var minX = Points.Min(p => p.X);
        var minY = Points.Min(p => p.Y);
        var maxX = Points.Max(p => p.X);
        var maxY = Points.Max(p => p.Y);
        return (minX, minY, maxX - minX, maxY - minY);
    }

    public override string ToSvgString()
    {
        var pointsStr = string.Join(" ", Points.Select(p => $"{p.X:G6},{p.Y:G6}"));
        return $"<polyline points=\"{pointsStr}\"{GetCommonSvgAttributes()}/>";
    }
}
