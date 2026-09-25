using System.Collections.ObjectModel;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG mask element - defines an opacity mask.
/// The alpha/luminance of mask content determines visibility.
/// </summary>
public class SvgMask : SvgGroup
{
    private string _maskUnits = "objectBoundingBox";
    private string _maskContentUnits = "userSpaceOnUse";
    private double _x = -0.1;
    private double _y = -0.1;
    private double _width = 1.2;
    private double _height = 1.2;

    /// <summary>Coordinate system for x, y, width, height ("userSpaceOnUse" or "objectBoundingBox").</summary>
    public string MaskUnits
    {
        get => _maskUnits;
        set 
        { 
            var newValue = value is "userSpaceOnUse" or "objectBoundingBox" ? value : "objectBoundingBox";
            if (_maskUnits == newValue) return; 
            _maskUnits = newValue; 
            OnPropertyChanged(nameof(MaskUnits)); 
        }
    }

    /// <summary>Coordinate system for mask content ("userSpaceOnUse" or "objectBoundingBox").</summary>
    public string MaskContentUnits
    {
        get => _maskContentUnits;
        set 
        { 
            var newValue = value is "userSpaceOnUse" or "objectBoundingBox" ? value : "userSpaceOnUse";
            if (_maskContentUnits == newValue) return; 
            _maskContentUnits = newValue; 
            OnPropertyChanged(nameof(MaskContentUnits)); 
        }
    }

    /// <summary>X position of the mask region.</summary>
    public double X
    {
        get => _x;
        set { if (Math.Abs(_x - value) < 0.0001) return; _x = value; OnPropertyChanged(nameof(X)); }
    }

    /// <summary>Y position of the mask region.</summary>
    public double Y
    {
        get => _y;
        set { if (Math.Abs(_y - value) < 0.0001) return; _y = value; OnPropertyChanged(nameof(Y)); }
    }

    /// <summary>Width of the mask region.</summary>
    public double Width
    {
        get => _width;
        set { if (Math.Abs(_width - value) < 0.0001) return; _width = value; OnPropertyChanged(nameof(Width)); }
    }

    /// <summary>Height of the mask region.</summary>
    public double Height
    {
        get => _height;
        set { if (Math.Abs(_height - value) < 0.0001) return; _height = value; OnPropertyChanged(nameof(Height)); }
    }

    public override VectorElement Clone()
    {
        var clone = new SvgMask
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
            MaskUnits = MaskUnits,
            MaskContentUnits = MaskContentUnits,
            X = X,
            Y = Y,
            Width = Width,
            Height = Height
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
        var attrs = new List<string>();
        if (MaskUnits != "objectBoundingBox") attrs.Add($"maskUnits=\"{MaskUnits}\"");
        if (MaskContentUnits != "userSpaceOnUse") attrs.Add($"maskContentUnits=\"{MaskContentUnits}\"");
        if (Math.Abs(X - (-0.1)) > 0.0001) attrs.Add($"x=\"{X}\"");
        if (Math.Abs(Y - (-0.1)) > 0.0001) attrs.Add($"y=\"{Y}\"");
        if (Math.Abs(Width - 1.2) > 0.0001) attrs.Add($"width=\"{Width}\"");
        if (Math.Abs(Height - 1.2) > 0.0001) attrs.Add($"height=\"{Height}\"");
        
        var attrsStr = attrs.Count > 0 ? " " + string.Join(" ", attrs) : "";
        var childrenSvg = string.Join("\n  ", Children.Select(c => c.ToSvgString()));
        return $"<mask{GetCommonSvgAttributes()}{attrsStr}>\n  {childrenSvg}\n</mask>";
    }
}
