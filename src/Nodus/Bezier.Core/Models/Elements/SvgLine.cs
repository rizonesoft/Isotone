namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG line element.
/// </summary>
public class SvgLine : VectorElement
{
    private double _x1;
    private double _y1;
    private double _x2 = 100;
    private double _y2 = 100;

    /// <summary>Start X coordinate.</summary>
    public double X1
    {
        get => _x1;
        set { _x1 = value; OnPropertyChanged(nameof(X1)); }
    }

    /// <summary>Start Y coordinate.</summary>
    public double Y1
    {
        get => _y1;
        set { _y1 = value; OnPropertyChanged(nameof(Y1)); }
    }

    /// <summary>End X coordinate.</summary>
    public double X2
    {
        get => _x2;
        set { _x2 = value; OnPropertyChanged(nameof(X2)); }
    }

    /// <summary>End Y coordinate.</summary>
    public double Y2
    {
        get => _y2;
        set { _y2 = value; OnPropertyChanged(nameof(Y2)); }
    }

    public override VectorElement Clone() => new SvgLine
    {
        Id = Guid.NewGuid(),
        Name = Name,
        X1 = X1,
        Y1 = Y1,
        X2 = X2,
        Y2 = Y2,
        IsVisible = IsVisible,
        IsLocked = IsLocked,
        Opacity = Opacity,
        BlendMode = BlendMode,
        Transform = Transform,
        Fill = Fill?.Clone(),
        Stroke = Stroke?.Clone()
    };

    protected override bool HitTestLocal(double x, double y)
    {
        // Check if point is within tolerance of the line segment
        const double tolerance = 5.0;
        
        var dx = X2 - X1;
        var dy = Y2 - Y1;
        var lengthSq = dx * dx + dy * dy;
        
        if (lengthSq < double.Epsilon)
            return Math.Sqrt((x - X1) * (x - X1) + (y - Y1) * (y - Y1)) <= tolerance;

        var t = Math.Clamp(((x - X1) * dx + (y - Y1) * dy) / lengthSq, 0, 1);
        var projX = X1 + t * dx;
        var projY = Y1 + t * dy;
        
        return Math.Sqrt((x - projX) * (x - projX) + (y - projY) * (y - projY)) <= tolerance;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        var minX = Math.Min(X1, X2);
        var minY = Math.Min(Y1, Y2);
        var maxX = Math.Max(X1, X2);
        var maxY = Math.Max(Y1, Y2);
        return (minX, minY, maxX - minX, maxY - minY);
    }

    public override string ToSvgString()
    {
        return $"<line x1=\"{X1:G6}\" y1=\"{Y1:G6}\" x2=\"{X2:G6}\" y2=\"{Y2:G6}\"{GetCommonSvgAttributes()}/>";
    }
}
