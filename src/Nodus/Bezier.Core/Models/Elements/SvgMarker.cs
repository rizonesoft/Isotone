using System.Collections.ObjectModel;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG marker element - defines arrow heads and path markers.
/// Can be used on path start, end, and vertices.
/// </summary>
public class SvgMarker : SvgGroup
{
    private double _refX;
    private double _refY;
    private double _markerWidth = 3;
    private double _markerHeight = 3;
    private string _markerUnits = "strokeWidth";
    private string _orient = "auto";
    private double _viewBoxX;
    private double _viewBoxY;
    private double _viewBoxWidth;
    private double _viewBoxHeight;

    /// <summary>X coordinate of the reference point (where marker attaches to path).</summary>
    public double RefX
    {
        get => _refX;
        set { if (Math.Abs(_refX - value) < 0.0001) return; _refX = value; OnPropertyChanged(nameof(RefX)); }
    }

    /// <summary>Y coordinate of the reference point.</summary>
    public double RefY
    {
        get => _refY;
        set { if (Math.Abs(_refY - value) < 0.0001) return; _refY = value; OnPropertyChanged(nameof(RefY)); }
    }

    /// <summary>Marker width.</summary>
    public double MarkerWidth
    {
        get => _markerWidth;
        set { if (Math.Abs(_markerWidth - value) < 0.0001) return; _markerWidth = Math.Max(0, value); OnPropertyChanged(nameof(MarkerWidth)); }
    }

    /// <summary>Marker height.</summary>
    public double MarkerHeight
    {
        get => _markerHeight;
        set { if (Math.Abs(_markerHeight - value) < 0.0001) return; _markerHeight = Math.Max(0, value); OnPropertyChanged(nameof(MarkerHeight)); }
    }

    /// <summary>Units for marker size ("strokeWidth" or "userSpaceOnUse").</summary>
    public string MarkerUnits
    {
        get => _markerUnits;
        set 
        { 
            var newValue = value is "strokeWidth" or "userSpaceOnUse" ? value : "strokeWidth";
            if (_markerUnits == newValue) return; 
            _markerUnits = newValue; 
            OnPropertyChanged(nameof(MarkerUnits)); 
        }
    }

    /// <summary>Orientation ("auto", "auto-start-reverse", or angle in degrees).</summary>
    public string Orient
    {
        get => _orient;
        set { if (_orient == value) return; _orient = value ?? "auto"; OnPropertyChanged(nameof(Orient)); }
    }

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

    /// <summary>Whether this marker has a viewBox defined.</summary>
    public bool HasViewBox => ViewBoxWidth > 0 && ViewBoxHeight > 0;

    public override VectorElement Clone()
    {
        var clone = new SvgMarker
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
            RefX = RefX,
            RefY = RefY,
            MarkerWidth = MarkerWidth,
            MarkerHeight = MarkerHeight,
            MarkerUnits = MarkerUnits,
            Orient = Orient,
            ViewBoxX = ViewBoxX,
            ViewBoxY = ViewBoxY,
            ViewBoxWidth = ViewBoxWidth,
            ViewBoxHeight = ViewBoxHeight
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
        if (RefX != 0) attrs.Add($"refX=\"{RefX}\"");
        if (RefY != 0) attrs.Add($"refY=\"{RefY}\"");
        attrs.Add($"markerWidth=\"{MarkerWidth}\"");
        attrs.Add($"markerHeight=\"{MarkerHeight}\"");
        if (MarkerUnits != "strokeWidth") attrs.Add($"markerUnits=\"{MarkerUnits}\"");
        if (Orient != "auto") attrs.Add($"orient=\"{Orient}\"");
        if (HasViewBox) attrs.Add($"viewBox=\"{ViewBoxX} {ViewBoxY} {ViewBoxWidth} {ViewBoxHeight}\"");
        
        var attrsStr = " " + string.Join(" ", attrs);
        var childrenSvg = string.Join("\n  ", Children.Select(c => c.ToSvgString()));
        return $"<marker{GetCommonSvgAttributes()}{attrsStr}>\n  {childrenSvg}\n</marker>";
    }
}
