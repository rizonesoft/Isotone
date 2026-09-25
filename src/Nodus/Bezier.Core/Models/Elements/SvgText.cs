namespace Bezier.Core.Models.Elements;

/// <summary>
/// SVG text anchor alignment.
/// </summary>
public enum TextAnchor
{
    Start,
    Middle,
    End
}

/// <summary>
/// SVG dominant baseline alignment.
/// </summary>
public enum DominantBaseline
{
    Auto,
    Middle,
    Hanging,
    Central,
    TextTop,
    TextBottom
}

/// <summary>
/// Represents an SVG text element.
/// </summary>
public class SvgText : VectorElement
{
    private double _x;
    private double _y;
    private string _text = "Text";
    private string _fontFamily = "Arial";
    private double _fontSize = 16;
    private int _fontWeight = 400;
    private bool _italic;
    private TextAnchor _textAnchor = TextAnchor.Start;
    private DominantBaseline _dominantBaseline = DominantBaseline.Auto;

    /// <summary>X position of the text.</summary>
    public double X
    {
        get => _x;
        set { _x = value; OnPropertyChanged(nameof(X)); }
    }

    /// <summary>Y position of the text.</summary>
    public double Y
    {
        get => _y;
        set { _y = value; OnPropertyChanged(nameof(Y)); }
    }

    /// <summary>The text content.</summary>
    public string Text
    {
        get => _text;
        set { _text = value ?? string.Empty; OnPropertyChanged(nameof(Text)); }
    }

    /// <summary>Font family name.</summary>
    public string FontFamily
    {
        get => _fontFamily;
        set { _fontFamily = value ?? "Arial"; OnPropertyChanged(nameof(FontFamily)); }
    }

    /// <summary>Font size in pixels.</summary>
    public double FontSize
    {
        get => _fontSize;
        set { _fontSize = Math.Max(1, value); OnPropertyChanged(nameof(FontSize)); }
    }

    /// <summary>Font weight (100-900).</summary>
    public int FontWeight
    {
        get => _fontWeight;
        set { _fontWeight = Math.Clamp(value, 100, 900); OnPropertyChanged(nameof(FontWeight)); }
    }

    /// <summary>Whether the text is italic.</summary>
    public bool Italic
    {
        get => _italic;
        set { _italic = value; OnPropertyChanged(nameof(Italic)); }
    }

    /// <summary>Text anchor alignment.</summary>
    public TextAnchor TextAnchor
    {
        get => _textAnchor;
        set { _textAnchor = value; OnPropertyChanged(nameof(TextAnchor)); }
    }

    /// <summary>Dominant baseline alignment.</summary>
    public DominantBaseline DominantBaseline
    {
        get => _dominantBaseline;
        set { _dominantBaseline = value; OnPropertyChanged(nameof(DominantBaseline)); }
    }

    public override VectorElement Clone() => new SvgText
    {
        Id = Guid.NewGuid(),
        Name = Name,
        X = X,
        Y = Y,
        Text = Text,
        FontFamily = FontFamily,
        FontSize = FontSize,
        FontWeight = FontWeight,
        Italic = Italic,
        TextAnchor = TextAnchor,
        DominantBaseline = DominantBaseline,
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
        // Approximate text bounding box (real measurement requires font metrics)
        var estimatedWidth = Text.Length * FontSize * 0.6;
        var estimatedHeight = FontSize * 1.2;
        
        var boxX = TextAnchor switch
        {
            TextAnchor.Middle => X - estimatedWidth / 2,
            TextAnchor.End => X - estimatedWidth,
            _ => X
        };
        var boxY = Y - estimatedHeight;

        return x >= boxX && x <= boxX + estimatedWidth && 
               y >= boxY && y <= boxY + estimatedHeight;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        var estimatedWidth = Text.Length * FontSize * 0.6;
        var estimatedHeight = FontSize * 1.2;
        
        var boxX = TextAnchor switch
        {
            TextAnchor.Middle => X - estimatedWidth / 2,
            TextAnchor.End => X - estimatedWidth,
            _ => X
        };
        
        return (boxX, Y - estimatedHeight, estimatedWidth, estimatedHeight);
    }

    public override string ToSvgString()
    {
        var attrs = new List<string>
        {
            $"x=\"{X:G6}\"",
            $"y=\"{Y:G6}\"",
            $"font-family=\"{FontFamily}\"",
            $"font-size=\"{FontSize:G6}\""
        };

        if (FontWeight != 400)
            attrs.Add($"font-weight=\"{FontWeight}\"");
        if (Italic)
            attrs.Add("font-style=\"italic\"");
        if (TextAnchor != TextAnchor.Start)
            attrs.Add($"text-anchor=\"{TextAnchor.ToString().ToLowerInvariant()}\"");
        if (DominantBaseline != DominantBaseline.Auto)
            attrs.Add($"dominant-baseline=\"{ConvertBaseline(DominantBaseline)}\"");

        var escapedText = Text.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;");
        return $"<text {string.Join(" ", attrs)}{GetCommonSvgAttributes()}>{escapedText}</text>";
    }

    private static string ConvertBaseline(DominantBaseline baseline) => baseline switch
    {
        DominantBaseline.Middle => "middle",
        DominantBaseline.Hanging => "hanging",
        DominantBaseline.Central => "central",
        DominantBaseline.TextTop => "text-top",
        DominantBaseline.TextBottom => "text-bottom",
        _ => "auto"
    };
}
