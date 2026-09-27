namespace Bezier.Core.Services;

using Bezier.Core.Models;

/// <summary>
/// Types of snap targets.
/// </summary>
[Flags]
public enum SnapTarget
{
    None = 0,
    Grid = 1,
    Guides = 2,
    Objects = 4,
    SmartGuides = 8,
    All = Grid | Guides | Objects | SmartGuides
}

/// <summary>
/// Result of a snap operation.
/// </summary>
public record SnapResult(
    double X,
    double Y,
    bool SnappedX,
    bool SnappedY,
    double? SnapLineX,
    double? SnapLineY,
    string? SnapDescription
);

/// <summary>
/// A smart guide line shown during dragging.
/// </summary>
public record SmartGuide(
    GuideOrientation Orientation,
    double Position,
    double Start,
    double End,
    SmartGuideType Type
);

/// <summary>
/// Types of smart guides.
/// </summary>
public enum SmartGuideType
{
    Alignment,
    Edge,
    Center,
    Spacing
}

/// <summary>
/// Manages snapping behavior for the canvas.
/// </summary>
public class SnapManager
{
    private readonly List<Guide> _guides = [];
    private readonly List<SmartGuide> _activeSmartGuides = [];

    /// <summary>
    /// Gets or sets whether snapping is enabled.
    /// </summary>
    public bool IsEnabled { get; set; } = true;

    /// <summary>
    /// Gets or sets the snap tolerance in pixels.
    /// </summary>
    public double Tolerance { get; set; } = 8;

    /// <summary>
    /// Gets or sets the grid size.
    /// </summary>
    public double GridSize { get; set; } = 10;

    /// <summary>
    /// Gets or sets whether grid snapping is enabled.
    /// </summary>
    public bool SnapToGrid { get; set; } = true;

    /// <summary>
    /// Gets or sets whether guide snapping is enabled.
    /// </summary>
    public bool SnapToGuides { get; set; } = true;

    /// <summary>
    /// Gets or sets whether object snapping is enabled.
    /// </summary>
    public bool SnapToObjects { get; set; } = true;

    /// <summary>
    /// Gets or sets whether smart guides are enabled.
    /// </summary>
    public bool SmartGuidesEnabled { get; set; } = true;

    /// <summary>
    /// Gets the list of guides.
    /// </summary>
    public IReadOnlyList<Guide> Guides => _guides;

    /// <summary>
    /// Gets the active smart guides for the current drag operation.
    /// </summary>
    public IReadOnlyList<SmartGuide> ActiveSmartGuides => _activeSmartGuides;

    /// <summary>
    /// Event raised when guides change.
    /// </summary>
    public event EventHandler? GuidesChanged;

    /// <summary>
    /// Event raised when smart guides update.
    /// </summary>
    public event EventHandler? SmartGuidesChanged;

    /// <summary>
    /// Adds a new guide.
    /// </summary>
    public void AddGuide(Guide guide)
    {
        _guides.Add(guide);
        GuidesChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Removes a guide.
    /// </summary>
    public bool RemoveGuide(Guide guide)
    {
        var removed = _guides.Remove(guide);
        if (removed)
        {
            GuidesChanged?.Invoke(this, EventArgs.Empty);
        }
        return removed;
    }

    /// <summary>
    /// Removes a guide by ID.
    /// </summary>
    public bool RemoveGuide(Guid id)
    {
        var guide = _guides.FirstOrDefault(g => g.Id == id);
        return guide != null && RemoveGuide(guide);
    }

    /// <summary>
    /// Clears all guides.
    /// </summary>
    public void ClearGuides()
    {
        _guides.Clear();
        GuidesChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Finds a guide at the specified position.
    /// </summary>
    public Guide? HitTestGuide(double x, double y)
    {
        return _guides.FirstOrDefault(g => g.HitTest(x, y, Tolerance));
    }

    /// <summary>
    /// Snaps a point to the nearest snap target.
    /// </summary>
    public SnapResult Snap(double x, double y, VectorDocument? document = null, VectorElement? exclude = null)
    {
        if (!IsEnabled)
        {
            return new SnapResult(x, y, false, false, null, null, null);
        }

        var snappedX = x;
        var snappedY = y;
        var didSnapX = false;
        var didSnapY = false;
        double? snapLineX = null;
        double? snapLineY = null;
        string? description = null;

        // Clear previous smart guides
        _activeSmartGuides.Clear();

        // Snap to grid
        if (SnapToGrid && GridSize > 0)
        {
            var gridSnapX = Math.Round(x / GridSize) * GridSize;
            var gridSnapY = Math.Round(y / GridSize) * GridSize;

            if (Math.Abs(gridSnapX - x) <= Tolerance)
            {
                snappedX = gridSnapX;
                didSnapX = true;
                description = "Grid";
            }

            if (Math.Abs(gridSnapY - y) <= Tolerance)
            {
                snappedY = gridSnapY;
                didSnapY = true;
                description = "Grid";
            }
        }

        // Snap to guides (higher priority than grid)
        if (SnapToGuides)
        {
            foreach (var guide in _guides)
            {
                if (guide.Orientation == GuideOrientation.Vertical)
                {
                    if (Math.Abs(guide.Position - x) <= Tolerance)
                    {
                        snappedX = guide.Position;
                        snapLineX = guide.Position;
                        didSnapX = true;
                        description = "Guide";
                    }
                }
                else
                {
                    if (Math.Abs(guide.Position - y) <= Tolerance)
                    {
                        snappedY = guide.Position;
                        snapLineY = guide.Position;
                        didSnapY = true;
                        description = "Guide";
                    }
                }
            }
        }

        // Snap to objects
        if (SnapToObjects && document != null)
        {
            foreach (var element in document.Elements)
            {
                if (element == exclude || !element.IsVisible) continue;

                var bounds = element.GetBoundingBox();
                var centerX = bounds.X + bounds.Width / 2;
                var centerY = bounds.Y + bounds.Height / 2;

                // Snap to edges
                var snapPoints = new[]
                {
                    (bounds.X, "Left edge"),
                    (bounds.X + bounds.Width, "Right edge"),
                    (centerX, "Center")
                };

                foreach (var (px, desc) in snapPoints)
                {
                    if (Math.Abs(px - x) <= Tolerance)
                    {
                        snappedX = px;
                        snapLineX = px;
                        didSnapX = true;
                        description = desc;

                        if (SmartGuidesEnabled)
                        {
                            _activeSmartGuides.Add(new SmartGuide(
                                GuideOrientation.Vertical,
                                px,
                                Math.Min(y, bounds.Y),
                                Math.Max(y, bounds.Y + bounds.Height),
                                SmartGuideType.Edge
                            ));
                        }
                    }
                }

                var snapPointsY = new[]
                {
                    (bounds.Y, "Top edge"),
                    (bounds.Y + bounds.Height, "Bottom edge"),
                    (centerY, "Center")
                };

                foreach (var (py, desc) in snapPointsY)
                {
                    if (Math.Abs(py - y) <= Tolerance)
                    {
                        snappedY = py;
                        snapLineY = py;
                        didSnapY = true;
                        description = desc;

                        if (SmartGuidesEnabled)
                        {
                            _activeSmartGuides.Add(new SmartGuide(
                                GuideOrientation.Horizontal,
                                py,
                                Math.Min(x, bounds.X),
                                Math.Max(x, bounds.X + bounds.Width),
                                SmartGuideType.Edge
                            ));
                        }
                    }
                }
            }
        }

        if (_activeSmartGuides.Count > 0)
        {
            SmartGuidesChanged?.Invoke(this, EventArgs.Empty);
        }

        return new SnapResult(snappedX, snappedY, didSnapX, didSnapY, snapLineX, snapLineY, description);
    }

    /// <summary>
    /// Snaps a bounding box, checking all corners and edges.
    /// </summary>
    public SnapResult SnapBounds(
        double x, double y, double width, double height,
        VectorDocument? document = null, VectorElement? exclude = null)
    {
        if (!IsEnabled)
        {
            return new SnapResult(x, y, false, false, null, null, null);
        }

        // Test snap points: corners and center
        var testPoints = new[]
        {
            (x, y),                           // Top-left
            (x + width, y),                   // Top-right
            (x, y + height),                  // Bottom-left
            (x + width, y + height),          // Bottom-right
            (x + width / 2, y + height / 2)   // Center
        };

        double bestDx = double.MaxValue;
        double bestDy = double.MaxValue;
        double? snapLineX = null;
        double? snapLineY = null;
        string? description = null;

        _activeSmartGuides.Clear();

        foreach (var (px, py) in testPoints)
        {
            var result = SnapSinglePoint(px, py, document, exclude);

            if (result.SnappedX && Math.Abs(result.X - px) < Math.Abs(bestDx))
            {
                bestDx = result.X - px;
                snapLineX = result.SnapLineX;
                description = result.SnapDescription;
            }

            if (result.SnappedY && Math.Abs(result.Y - py) < Math.Abs(bestDy))
            {
                bestDy = result.Y - py;
                snapLineY = result.SnapLineY;
                description = result.SnapDescription;
            }
        }

        var snappedX = bestDx != double.MaxValue ? x + bestDx : x;
        var snappedY = bestDy != double.MaxValue ? y + bestDy : y;

        return new SnapResult(
            snappedX,
            snappedY,
            bestDx != double.MaxValue,
            bestDy != double.MaxValue,
            snapLineX,
            snapLineY,
            description
        );
    }

    private SnapResult SnapSinglePoint(double x, double y, VectorDocument? document, VectorElement? exclude)
    {
        // Simplified snap without modifying smart guides list
        var snappedX = x;
        var snappedY = y;
        var didSnapX = false;
        var didSnapY = false;
        double? snapLineX = null;
        double? snapLineY = null;
        string? description = null;

        // Snap to grid
        if (SnapToGrid && GridSize > 0)
        {
            var gridSnapX = Math.Round(x / GridSize) * GridSize;
            var gridSnapY = Math.Round(y / GridSize) * GridSize;

            if (Math.Abs(gridSnapX - x) <= Tolerance)
            {
                snappedX = gridSnapX;
                didSnapX = true;
            }

            if (Math.Abs(gridSnapY - y) <= Tolerance)
            {
                snappedY = gridSnapY;
                didSnapY = true;
            }
        }

        // Snap to guides
        if (SnapToGuides)
        {
            foreach (var guide in _guides)
            {
                if (guide.Orientation == GuideOrientation.Vertical)
                {
                    if (Math.Abs(guide.Position - x) <= Tolerance)
                    {
                        snappedX = guide.Position;
                        snapLineX = guide.Position;
                        didSnapX = true;
                        description = "Guide";
                    }
                }
                else
                {
                    if (Math.Abs(guide.Position - y) <= Tolerance)
                    {
                        snappedY = guide.Position;
                        snapLineY = guide.Position;
                        didSnapY = true;
                        description = "Guide";
                    }
                }
            }
        }

        // Snap to objects
        if (SnapToObjects && document != null)
        {
            foreach (var element in document.Elements)
            {
                if (element == exclude || !element.IsVisible) continue;

                var bounds = element.GetBoundingBox();
                var centerX = bounds.X + bounds.Width / 2;
                var centerY = bounds.Y + bounds.Height / 2;

                // Check X snap points
                foreach (var px in new[] { bounds.X, bounds.X + bounds.Width, centerX })
                {
                    if (Math.Abs(px - x) <= Tolerance && Math.Abs(px - x) < Math.Abs(snappedX - x))
                    {
                        snappedX = px;
                        snapLineX = px;
                        didSnapX = true;
                    }
                }

                // Check Y snap points
                foreach (var py in new[] { bounds.Y, bounds.Y + bounds.Height, centerY })
                {
                    if (Math.Abs(py - y) <= Tolerance && Math.Abs(py - y) < Math.Abs(snappedY - y))
                    {
                        snappedY = py;
                        snapLineY = py;
                        didSnapY = true;
                    }
                }
            }
        }

        return new SnapResult(snappedX, snappedY, didSnapX, didSnapY, snapLineX, snapLineY, description);
    }

    /// <summary>
    /// Clears active smart guides.
    /// </summary>
    public void ClearSmartGuides()
    {
        if (_activeSmartGuides.Count > 0)
        {
            _activeSmartGuides.Clear();
            SmartGuidesChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    /// <summary>
    /// Snaps a value to the grid.
    /// </summary>
    public double SnapToGridValue(double value)
    {
        if (!SnapToGrid || GridSize <= 0) return value;
        return Math.Round(value / GridSize) * GridSize;
    }
}
