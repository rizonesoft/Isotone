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
        Name = this.Name,
        X = this.X,
        Y = this.Y,
        Width = this.Width,
        Height = this.Height,
        Rx = this.Rx,
        Ry = this.Ry,
        IsVisible = this.IsVisible,
        IsLocked = this.IsLocked,
        Opacity = this.Opacity,
        BlendMode = this.BlendMode
    };

    public override bool HitTest(double x, double y)
    {
        return x >= X && x <= X + Width && y >= Y && y <= Y + Height;
    }

    public override (double X, double Y, double Width, double Height) GetBoundingBox()
    {
        return (X, Y, Width, Height);
    }
}
