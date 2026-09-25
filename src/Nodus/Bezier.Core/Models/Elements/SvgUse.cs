namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG use element - an instance of a symbol or other element.
/// References another element by href and can override position and dimensions.
/// </summary>
public class SvgUse : VectorElement
{
    private string _href = string.Empty;
    private double _x;
    private double _y;
    private double _width;
    private double _height;

    /// <summary>Reference to the element to use (href attribute, e.g., "#symbolId").</summary>
    public string Href
    {
        get => _href;
        set { if (_href == value) return; _href = value ?? string.Empty; OnPropertyChanged(nameof(Href)); }
    }

    /// <summary>X position offset for the use instance.</summary>
    public double X
    {
        get => _x;
        set { if (Math.Abs(_x - value) < 0.0001) return; _x = value; OnPropertyChanged(nameof(X)); }
    }

    /// <summary>Y position offset for the use instance.</summary>
    public double Y
    {
        get => _y;
        set { if (Math.Abs(_y - value) < 0.0001) return; _y = value; OnPropertyChanged(nameof(Y)); }
    }

    /// <summary>Width override (0 = use symbol's width).</summary>
    public double Width
    {
        get => _width;
        set { if (Math.Abs(_width - value) < 0.0001) return; _width = Math.Max(0, value); OnPropertyChanged(nameof(Width)); }
    }

    /// <summary>Height override (0 = use symbol's height).</summary>
    public double Height
    {
        get => _height;
        set { if (Math.Abs(_height - value) < 0.0001) return; _height = Math.Max(0, value); OnPropertyChanged(nameof(Height)); }
    }

    /// <summary>The ID of the referenced element (extracted from Href).</summary>
    public string ReferencedId => Href.TrimStart('#');

    public override VectorElement Clone() => new SvgUse
    {
        Id = Guid.NewGuid(),
        Name = Name,
        IsVisible = IsVisible,
        IsLocked = IsLocked,
        Opacity = Opacity,
        BlendMode = BlendMode,
        Transform = Transform,
        Fill = Fill?.Clone(),
        Stroke = Stroke?.Clone(),
        Href = Href,
        X = X,
        Y = Y,
        Width = Width,
        Height = Height
    };

    protected override bool HitTestLocal(double x, double y)
    {
        var bounds = GetLocalBoundingBox();
        return x >= bounds.X && x <= bounds.X + bounds.Width &&
               y >= bounds.Y && y <= bounds.Y + bounds.Height;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        // Use provided dimensions or default to 100x100 if referencing a symbol
        var w = Width > 0 ? Width : 100;
        var h = Height > 0 ? Height : 100;
        return (X, Y, w, h);
    }

    public override string ToSvgString()
    {
        var attrs = new List<string> { $"href=\"{Href}\"" };
        if (X != 0) attrs.Add($"x=\"{X}\"");
        if (Y != 0) attrs.Add($"y=\"{Y}\"");
        if (Width > 0) attrs.Add($"width=\"{Width}\"");
        if (Height > 0) attrs.Add($"height=\"{Height}\"");
        return $"<use {string.Join(" ", attrs)}{GetCommonSvgAttributes()}/>";
    }
}
