namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG path element with path data string.
/// </summary>
public class SvgPath : VectorElement
{
    private string _pathData = string.Empty;

    /// <summary>SVG path data string (d attribute).</summary>
    public string PathData
    {
        get => _pathData;
        set { _pathData = value ?? string.Empty; OnPropertyChanged(nameof(PathData)); }
    }

    public override VectorElement Clone() => new SvgPath
    {
        Id = Guid.NewGuid(),
        Name = Name,
        PathData = PathData,
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
        // TODO: Implement proper path hit testing using path parsing
        // For now, use bounding box as approximation
        var box = GetBoundingBox();
        return x >= box.X && x <= box.X + box.Width && 
               y >= box.Y && y <= box.Y + box.Height;
    }

    public override (double X, double Y, double Width, double Height) GetBoundingBox()
    {
        // TODO: Parse path data and calculate accurate bounding box
        // For now, return a placeholder
        return (0, 0, 100, 100);
    }

    public override string ToSvgString()
    {
        return $"<path d=\"{PathData}\"{GetCommonSvgAttributes()}/>";
    }

    // TODO: Add path parsing and node manipulation methods
    // - Parse path data to segments (M, L, C, Q, A, Z)
    // - Get/set individual nodes
    // - Convert relative to absolute commands
}
