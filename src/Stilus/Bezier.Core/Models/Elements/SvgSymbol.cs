using System.Collections.ObjectModel;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG symbol element - a reusable definition that can be instantiated with SvgUse.
/// Symbols are not rendered directly; they define reusable graphics.
/// </summary>
public class SvgSymbol : SvgGroup
{
    private double _viewBoxX;
    private double _viewBoxY;
    private double _viewBoxWidth;
    private double _viewBoxHeight;
    private string _preserveAspectRatio = "xMidYMid meet";

    /// <summary>ViewBox X origin.</summary>
    public double ViewBoxX
    {
        get => _viewBoxX;
        set { if (Math.Abs(_viewBoxX - value) < 0.0001) return; _viewBoxX = value; OnPropertyChanged(nameof(ViewBoxX)); }
    }

    /// <summary>ViewBox Y origin.</summary>
    public double ViewBoxY
    {
        get => _viewBoxY;
        set { if (Math.Abs(_viewBoxY - value) < 0.0001) return; _viewBoxY = value; OnPropertyChanged(nameof(ViewBoxY)); }
    }

    /// <summary>ViewBox width.</summary>
    public double ViewBoxWidth
    {
        get => _viewBoxWidth;
        set { if (Math.Abs(_viewBoxWidth - value) < 0.0001) return; _viewBoxWidth = value; OnPropertyChanged(nameof(ViewBoxWidth)); }
    }

    /// <summary>ViewBox height.</summary>
    public double ViewBoxHeight
    {
        get => _viewBoxHeight;
        set { if (Math.Abs(_viewBoxHeight - value) < 0.0001) return; _viewBoxHeight = value; OnPropertyChanged(nameof(ViewBoxHeight)); }
    }

    /// <summary>Aspect ratio preservation mode (e.g., "xMidYMid meet").</summary>
    public string PreserveAspectRatio
    {
        get => _preserveAspectRatio;
        set { if (_preserveAspectRatio == value) return; _preserveAspectRatio = value ?? "xMidYMid meet"; OnPropertyChanged(nameof(PreserveAspectRatio)); }
    }

    /// <summary>Whether this symbol has a viewBox defined.</summary>
    public bool HasViewBox => ViewBoxWidth > 0 && ViewBoxHeight > 0;

    public override VectorElement Clone()
    {
        var clone = new SvgSymbol
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
            ViewBoxX = ViewBoxX,
            ViewBoxY = ViewBoxY,
            ViewBoxWidth = ViewBoxWidth,
            ViewBoxHeight = ViewBoxHeight,
            PreserveAspectRatio = PreserveAspectRatio
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
        var viewBoxAttr = HasViewBox ? $" viewBox=\"{ViewBoxX} {ViewBoxY} {ViewBoxWidth} {ViewBoxHeight}\"" : "";
        var preserveAttr = PreserveAspectRatio != "xMidYMid meet" ? $" preserveAspectRatio=\"{PreserveAspectRatio}\"" : "";
        var childrenSvg = string.Join("\n  ", Children.Select(c => c.ToSvgString()));
        return $"<symbol{GetCommonSvgAttributes()}{viewBoxAttr}{preserveAttr}>\n  {childrenSvg}\n</symbol>";
    }
}
