namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG polygon element (closed shape with straight edges).
/// </summary>
public class SvgPolygon : VectorElement
{
    private List<(double X, double Y)> _points = [];

    /// <summary>List of polygon points.</summary>
    public List<(double X, double Y)> Points
    {
        get => _points;
        set { _points = value ?? []; OnPropertyChanged(nameof(Points)); }
    }

    public override VectorElement Clone()
    {
        var clone = new SvgPolygon
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
        if (Points.Count < 3) return false;
        
        // Ray casting algorithm for point-in-polygon
        var inside = false;
        for (int i = 0, j = Points.Count - 1; i < Points.Count; j = i++)
        {
            var xi = Points[i].X;
            var yi = Points[i].Y;
            var xj = Points[j].X;
            var yj = Points[j].Y;
            
            if (((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi))
                inside = !inside;
        }
        return inside;
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
        return $"<polygon points=\"{pointsStr}\"{GetCommonSvgAttributes()}/>";
    }
}
