namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG circle element.
/// </summary>
public class SvgCircle : VectorElement
{
    private double _cx;
    private double _cy;
    private double _r = 50;

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

    /// <summary>Radius of the circle.</summary>
    public double R
    {
        get => _r;
        set { _r = Math.Max(0, value); OnPropertyChanged(nameof(R)); }
    }

    public override VectorElement Clone() => new SvgCircle
    {
        Id = Guid.NewGuid(),
        Name = Name,
        Cx = Cx,
        Cy = Cy,
        R = R,
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
        var dx = x - Cx;
        var dy = y - Cy;
        return dx * dx + dy * dy <= R * R;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        return (Cx - R, Cy - R, R * 2, R * 2);
    }

    public override string ToSvgString()
    {
        return $"<circle cx=\"{Cx:G6}\" cy=\"{Cy:G6}\" r=\"{R:G6}\"{GetCommonSvgAttributes()}/>";
    }
}
