namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG image element (embedded or linked raster image).
/// </summary>
public class SvgImage : VectorElement
{
    private double _x;
    private double _y;
    private double _width = 100;
    private double _height = 100;
    private string? _href;
    private byte[]? _embeddedData;
    private string _mimeType = "image/png";

    /// <summary>X position of the image.</summary>
    public double X
    {
        get => _x;
        set { _x = value; OnPropertyChanged(nameof(X)); }
    }

    /// <summary>Y position of the image.</summary>
    public double Y
    {
        get => _y;
        set { _y = value; OnPropertyChanged(nameof(Y)); }
    }

    /// <summary>Width of the image.</summary>
    public double Width
    {
        get => _width;
        set { _width = Math.Max(0, value); OnPropertyChanged(nameof(Width)); }
    }

    /// <summary>Height of the image.</summary>
    public double Height
    {
        get => _height;
        set { _height = Math.Max(0, value); OnPropertyChanged(nameof(Height)); }
    }

    /// <summary>External href (URL or path) for linked images.</summary>
    public string? Href
    {
        get => _href;
        set { _href = value; OnPropertyChanged(nameof(Href)); }
    }

    /// <summary>Embedded image data (base64 decoded).</summary>
    public byte[]? EmbeddedData
    {
        get => _embeddedData;
        set { _embeddedData = value; OnPropertyChanged(nameof(EmbeddedData)); }
    }

    /// <summary>MIME type for embedded data (e.g., "image/png", "image/jpeg").</summary>
    public string MimeType
    {
        get => _mimeType;
        set { _mimeType = value ?? "image/png"; OnPropertyChanged(nameof(MimeType)); }
    }

    /// <summary>Whether this image uses embedded data.</summary>
    public bool IsEmbedded => EmbeddedData is not null && EmbeddedData.Length > 0;

    public override VectorElement Clone() => new SvgImage
    {
        Id = Guid.NewGuid(),
        Name = Name,
        X = X,
        Y = Y,
        Width = Width,
        Height = Height,
        Href = Href,
        EmbeddedData = EmbeddedData?.ToArray(),
        MimeType = MimeType,
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
        return x >= X && x <= X + Width && y >= Y && y <= Y + Height;
    }

    public override (double X, double Y, double Width, double Height) GetBoundingBox()
    {
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

        if (IsEmbedded)
        {
            var base64 = Convert.ToBase64String(EmbeddedData!);
            attrs.Add($"href=\"data:{MimeType};base64,{base64}\"");
        }
        else if (!string.IsNullOrEmpty(Href))
        {
            attrs.Add($"href=\"{Href}\"");
        }

        return $"<image {string.Join(" ", attrs)}{GetCommonSvgAttributes()}/>";
    }
}
