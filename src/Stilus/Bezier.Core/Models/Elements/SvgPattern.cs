using Bezier.Core.Models;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Specifies the units for pattern geometry.
/// </summary>
public enum PatternUnits
{
    UserSpaceOnUse,
    ObjectBoundingBox
}

/// <summary>
/// Represents an SVG pattern definition.
/// </summary>
public class SvgPattern : SvgGroup
{
    private double _x;
    private double _y;
    private double _width;
    private double _height;
    private PatternUnits _patternUnits = PatternUnits.ObjectBoundingBox;
    private PatternUnits _patternContentUnits = PatternUnits.UserSpaceOnUse;
    private ViewBox? _viewBox;
    private string _href = string.Empty;

    /// <summary>
    /// X coordinate of the pattern tile.
    /// </summary>
    public double X
    {
        get => _x;
        set { _x = value; OnPropertyChanged(nameof(X)); }
    }

    /// <summary>
    /// Y coordinate of the pattern tile.
    /// </summary>
    public double Y
    {
        get => _y;
        set { _y = value; OnPropertyChanged(nameof(Y)); }
    }

    /// <summary>
    /// Width of the pattern tile.
    /// </summary>
    public double Width
    {
        get => _width;
        set { _width = value; OnPropertyChanged(nameof(Width)); }
    }

    /// <summary>
    /// Height of the pattern tile.
    /// </summary>
    public double Height
    {
        get => _height;
        set { _height = value; OnPropertyChanged(nameof(Height)); }
    }

    /// <summary>
    /// Units for the pattern geometry (X, Y, Width, Height).
    /// </summary>
    public PatternUnits PatternUnits
    {
        get => _patternUnits;
        set { _patternUnits = value; OnPropertyChanged(nameof(PatternUnits)); }
    }

    /// <summary>
    /// Units for the pattern content's geometry.
    /// </summary>
    public PatternUnits PatternContentUnits
    {
        get => _patternContentUnits;
        set { _patternContentUnits = value; OnPropertyChanged(nameof(PatternContentUnits)); }
    }

    /// <summary>
    /// ViewBox for the pattern.
    /// </summary>
    public ViewBox? ViewBox
    {
        get => _viewBox;
        set { _viewBox = value; OnPropertyChanged(nameof(ViewBox)); }
    }

    /// <summary>
    /// Reference to another pattern to inherit attributes from.
    /// </summary>
    public string Href
    {
        get => _href;
        set { _href = value; OnPropertyChanged(nameof(Href)); }
    }

    public override VectorElement Clone()
    {
        var clone = new SvgPattern
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
            X = X,
            Y = Y,
            Width = Width,
            Height = Height,
            PatternUnits = PatternUnits,
            PatternContentUnits = PatternContentUnits,
            ViewBox = ViewBox,
            Href = Href
        };

        foreach (var child in Children)
        {
            var childClone = child.Clone();
            childClone.Parent = clone;
            clone.Children.Add(childClone);
        }

        return clone;
    }

    public override string ToSvgString()
    {
        var units = PatternUnits == PatternUnits.UserSpaceOnUse ? "userSpaceOnUse" : "objectBoundingBox";
        var contentUnits = PatternContentUnits == PatternUnits.ObjectBoundingBox ? "objectBoundingBox" : "userSpaceOnUse";
        
        var viewBoxAttr = ViewBox.HasValue 
            ? $" viewBox=\"{ViewBox.Value.MinX} {ViewBox.Value.MinY} {ViewBox.Value.Width} {ViewBox.Value.Height}\"" 
            : "";
            
        var hrefAttr = !string.IsNullOrEmpty(Href) ? $" href=\"{Href}\"" : "";

        var childrenSvg = string.Join("\n  ", Children.Select(c => c.ToSvgString()));
        
        return $"<pattern id=\"{Name}\" x=\"{X}\" y=\"{Y}\" width=\"{Width}\" height=\"{Height}\" " +
               $"patternUnits=\"{units}\" patternContentUnits=\"{contentUnits}\"{viewBoxAttr}{hrefAttr}>\n" +
               $"  {childrenSvg}\n" +
               $"</pattern>";
    }
}
