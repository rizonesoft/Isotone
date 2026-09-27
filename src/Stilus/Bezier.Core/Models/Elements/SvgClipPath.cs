using System.Collections.ObjectModel;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG clipPath element - defines a clipping region.
/// Elements inside the clipPath define the clipping shape.
/// </summary>
public class SvgClipPath : SvgGroup
{
    private string _clipPathUnits = "userSpaceOnUse";

    /// <summary>Coordinate system for clipPath content ("userSpaceOnUse" or "objectBoundingBox").</summary>
    public string ClipPathUnits
    {
        get => _clipPathUnits;
        set 
        { 
            var newValue = value is "userSpaceOnUse" or "objectBoundingBox" ? value : "userSpaceOnUse";
            if (_clipPathUnits == newValue) return; 
            _clipPathUnits = newValue; 
            OnPropertyChanged(nameof(ClipPathUnits)); 
        }
    }

    public override VectorElement Clone()
    {
        var clone = new SvgClipPath
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
            ClipPathUnits = ClipPathUnits
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
        var unitsAttr = ClipPathUnits != "userSpaceOnUse" ? $" clipPathUnits=\"{ClipPathUnits}\"" : "";
        var childrenSvg = string.Join("\n  ", Children.Select(c => c.ToSvgString()));
        return $"<clipPath{GetCommonSvgAttributes()}{unitsAttr}>\n  {childrenSvg}\n</clipPath>";
    }
}
