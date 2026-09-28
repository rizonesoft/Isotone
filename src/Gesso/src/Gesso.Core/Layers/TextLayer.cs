namespace Gesso.Core.Layers;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// A layer containing editable text content.
/// </summary>
public sealed partial class TextLayer : Layer
{
    [ObservableProperty]
    private string _text = string.Empty;

    [ObservableProperty]
    private string _fontFamily = "Segoe UI";

    [ObservableProperty]
    private double _fontSize = 24.0;

    [ObservableProperty]
    private TextFontWeight _fontWeight = TextFontWeight.Normal;

    [ObservableProperty]
    private TextFontStyle _fontStyle = TextFontStyle.Normal;

    [ObservableProperty]
    private uint _textColor = 0xFFFFFFFF; // ARGB white

    [ObservableProperty]
    private TextHorizontalAlignment _textAlignment = TextHorizontalAlignment.Left;

    [ObservableProperty]
    private double _lineSpacing = 1.0;

    [ObservableProperty]
    private double _letterSpacing;

    [ObservableProperty]
    private double _positionX;

    [ObservableProperty]
    private double _positionY;

    [ObservableProperty]
    private bool _isAntiAliased = true;

    public override LayerType LayerType => LayerType.Text;

    public TextLayer()
    {
        Name = "Text";
    }

    public TextLayer(string text) : this()
    {
        Text = text;
        Name = text.Length > 20 ? text[..20] + "..." : text;
    }

    public override Layer Clone()
    {
        return new TextLayer(Text)
        {
            Name = Name + " Copy",
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            FontFamily = FontFamily,
            FontSize = FontSize,
            FontWeight = FontWeight,
            FontStyle = FontStyle,
            TextColor = TextColor,
            TextAlignment = TextAlignment,
            LineSpacing = LineSpacing,
            LetterSpacing = LetterSpacing,
            PositionX = PositionX,
            PositionY = PositionY,
            IsAntiAliased = IsAntiAliased
        };
    }
}

/// <summary>
/// Font weight for text layers.
/// </summary>
public enum TextFontWeight
{
    Thin = 100,
    ExtraLight = 200,
    Light = 300,
    Normal = 400,
    Medium = 500,
    SemiBold = 600,
    Bold = 700,
    ExtraBold = 800,
    Black = 900
}

/// <summary>
/// Font style for text layers.
/// </summary>
public enum TextFontStyle
{
    Normal,
    Italic,
    Oblique
}

/// <summary>
/// Horizontal text alignment.
/// </summary>
public enum TextHorizontalAlignment
{
    Left,
    Center,
    Right,
    Justify
}
