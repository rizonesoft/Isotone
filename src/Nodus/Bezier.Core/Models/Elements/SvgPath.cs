using Bezier.Core.Utilities;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG path element with path data string.
/// </summary>
public class SvgPath : VectorElement
{
    private string _pathData = string.Empty;
    private (double X, double Y, double Width, double Height)? _cachedBounds;

    /// <summary>SVG path data string (d attribute).</summary>
    public string PathData
    {
        get => _pathData;
        set 
        { 
            _pathData = value ?? string.Empty; 
            _cachedBounds = null; // Invalidate cache
            OnPropertyChanged(nameof(PathData)); 
        }
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
        // Use bounding box with stroke tolerance for hit testing
        var strokeWidth = Stroke?.Width ?? 0;
        var tolerance = Math.Max(5.0, strokeWidth / 2);
        
        var bounds = GetBoundingBox();
        
        // Expand bounds by tolerance for easier selection
        return x >= bounds.X - tolerance && 
               x <= bounds.X + bounds.Width + tolerance &&
               y >= bounds.Y - tolerance && 
               y <= bounds.Y + bounds.Height + tolerance;
    }

    public override (double X, double Y, double Width, double Height) GetBoundingBox()
    {
        // Use cached bounds if available
        if (_cachedBounds.HasValue)
            return _cachedBounds.Value;

        // Parse path data and calculate accurate bounding box
        _cachedBounds = SvgPathParser.GetBoundingBox(_pathData);
        return _cachedBounds.Value;
    }

    /// <summary>
    /// Gets all points extracted from the path data for advanced operations.
    /// </summary>
    public List<(double X, double Y)> GetPathPoints()
    {
        return SvgPathParser.ExtractAllPoints(_pathData);
    }

    /// <summary>
    /// Invalidates the cached bounding box, forcing recalculation on next access.
    /// </summary>
    public void InvalidateBounds()
    {
        _cachedBounds = null;
    }

    public override string ToSvgString()
    {
        return $"<path d=\"{PathData}\"{GetCommonSvgAttributes()}/>";
    }
}
