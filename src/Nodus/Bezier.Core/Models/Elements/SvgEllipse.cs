namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG ellipse element.
/// </summary>
public class SvgEllipse : VectorElement
{
    private double _cx;
    private double _cy;
    private double _rx = 50;
    private double _ry = 30;

    /// <summary>Center X coordinate.</summary>
    public double Cx
    {
        get => _cx;
        set { _cx = value; OnPropertyChanged(nameof(Cx)); }
    }

    /// <summary>Center Y coordinate.</summary>
    public double Cy
    {
        get => _cy;
        set { _cy = value; OnPropertyChanged(nameof(Cy)); }
    }

    /// <summary>Horizontal radius.</summary>
    public double Rx
    {
        get => _rx;
        set { _rx = Math.Max(0, value); OnPropertyChanged(nameof(Rx)); }
    }

    /// <summary>Vertical radius.</summary>
    public double Ry
    {
        get => _ry;
        set { _ry = Math.Max(0, value); OnPropertyChanged(nameof(Ry)); }
    }

    public override VectorElement Clone() => new SvgEllipse
    {
        Id = Guid.NewGuid(),
        Name = Name,
        Cx = Cx,
        Cy = Cy,
        Rx = Rx,
        Ry = Ry,
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
        if (Rx <= 0 || Ry <= 0) return false;
        var dx = (x - Cx) / Rx;
        var dy = (y - Cy) / Ry;
        return dx * dx + dy * dy <= 1;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        return (Cx - Rx, Cy - Ry, Rx * 2, Ry * 2);
    }

    public override string ToSvgString()
    {
        return $"<ellipse cx=\"{Cx:G6}\" cy=\"{Cy:G6}\" rx=\"{Rx:G6}\" ry=\"{Ry:G6}\"{GetCommonSvgAttributes()}/>";
    }
}
