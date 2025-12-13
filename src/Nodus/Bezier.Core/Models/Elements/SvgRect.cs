namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG rectangle element.
/// </summary>
public class SvgRect : VectorElement
{
    private double _x;
    private double _y;
    private double _width = 100;
    private double _height = 100;
    private double _rx;
    private double _ry;

    /// <summary>X position of the rectangle.</summary>
    public double X
    {
        get => _x;
        set { _x = value; OnPropertyChanged(nameof(X)); }
    }

    /// <summary>Y position of the rectangle.</summary>
    public double Y
    {
        get => _y;
        set { _y = value; OnPropertyChanged(nameof(Y)); }
    }

    /// <summary>Width of the rectangle.</summary>
    public double Width
    {
        get => _width;
        set { _width = value; OnPropertyChanged(nameof(Width)); }
    }

    /// <summary>Height of the rectangle.</summary>
    public double Height
    {
        get => _height;
        set { _height = value; OnPropertyChanged(nameof(Height)); }
    }

    /// <summary>Horizontal corner radius.</summary>
    public double Rx
    {
        get => _rx;
        set { _rx = value; OnPropertyChanged(nameof(Rx)); }
    }

    /// <summary>Vertical corner radius.</summary>
    public double Ry
    {
        get => _ry;
        set { _ry = value; OnPropertyChanged(nameof(Ry)); }
    }

    public override VectorElement Clone() => new SvgRect
    {
        Id = Guid.NewGuid(),
        Name = Name,
        X = X,
        Y = Y,
        Width = Width,
        Height = Height,
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

    public override bool HitTest(double x, double y)
    {
        // TODO: Apply transform inverse for proper hit testing
        return x >= X && x <= X + Width && y >= Y && y <= Y + Height;
    }

    public override (double X, double Y, double Width, double Height) GetBoundingBox()
    {
        // TODO: Apply transform for accurate bounding box
        return (X, Y, Width, Height);
    }

    public override string ToSvgString()
    {
        var attrs = new List<string>
        {
            $"x=\"{X:G6}\"",
            $"y=\"{Y:G6}\"",
            $"width=\"{Width:G6}\"",
            $"height=\"{Height:G6}\""
        };

        if (Rx > 0) attrs.Add($"rx=\"{Rx:G6}\"");
        if (Ry > 0) attrs.Add($"ry=\"{Ry:G6}\"");

        return $"<rect {string.Join(" ", attrs)}{GetCommonSvgAttributes()}/>";
    }
}

