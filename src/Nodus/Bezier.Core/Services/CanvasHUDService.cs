using System.ComponentModel;
using Bezier.Core.Models;

namespace Bezier.Core.Services;

/// <summary>
/// Position anchor for HUD elements.
/// </summary>
public enum HUDAnchor
{
    TopLeft,
    TopCenter,
    TopRight,
    MiddleLeft,
    MiddleCenter,
    MiddleRight,
    BottomLeft,
    BottomCenter,
    BottomRight
}

/// <summary>
/// Quick action for the contextual toolbar.
/// </summary>
public record HUDAction(
    string Id,
    string Name,
    string? Icon = null,
    string? Tooltip = null,
    Action? Execute = null,
    Func<bool>? CanExecute = null
);

/// <summary>
/// Information about the current selection.
/// </summary>
public class SelectionInfo : INotifyPropertyChanged
{
    private int _count;
    private string _elementType = "Nothing";
    private double _x;
    private double _y;
    private double _width;
    private double _height;
    private double _rotation;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets or sets the number of selected elements.
    /// </summary>
    public int Count
    {
        get => _count;
        set { _count = value; OnPropertyChanged(nameof(Count)); OnPropertyChanged(nameof(HasSelection)); OnPropertyChanged(nameof(Summary)); }
    }

    /// <summary>
    /// Gets or sets the element type description.
    /// </summary>
    public string ElementType
    {
        get => _elementType;
        set { _elementType = value; OnPropertyChanged(nameof(ElementType)); OnPropertyChanged(nameof(Summary)); }
    }

    /// <summary>
    /// Gets or sets the X position.
    /// </summary>
    public double X
    {
        get => _x;
        set { _x = value; OnPropertyChanged(nameof(X)); OnPropertyChanged(nameof(PositionText)); }
    }

    /// <summary>
    /// Gets or sets the Y position.
    /// </summary>
    public double Y
    {
        get => _y;
        set { _y = value; OnPropertyChanged(nameof(Y)); OnPropertyChanged(nameof(PositionText)); }
    }

    /// <summary>
    /// Gets or sets the width.
    /// </summary>
    public double Width
    {
        get => _width;
        set { _width = value; OnPropertyChanged(nameof(Width)); OnPropertyChanged(nameof(DimensionsText)); }
    }

    /// <summary>
    /// Gets or sets the height.
    /// </summary>
    public double Height
    {
        get => _height;
        set { _height = value; OnPropertyChanged(nameof(Height)); OnPropertyChanged(nameof(DimensionsText)); }
    }

    /// <summary>
    /// Gets or sets the rotation angle in degrees.
    /// </summary>
    public double Rotation
    {
        get => _rotation;
        set { _rotation = value; OnPropertyChanged(nameof(Rotation)); OnPropertyChanged(nameof(RotationText)); }
    }

    /// <summary>
    /// Gets whether there is a selection.
    /// </summary>
    public bool HasSelection => Count > 0;

    /// <summary>
    /// Gets the selection summary text.
    /// </summary>
    public string Summary => Count switch
    {
        0 => "Nothing selected",
        1 => ElementType,
        _ => $"{Count} objects"
    };

    /// <summary>
    /// Gets the position text.
    /// </summary>
    public string PositionText => $"X: {X:F1}  Y: {Y:F1}";

    /// <summary>
    /// Gets the dimensions text.
    /// </summary>
    public string DimensionsText => $"W: {Width:F1}  H: {Height:F1}";

    /// <summary>
    /// Gets the rotation text.
    /// </summary>
    public string RotationText => $"{Rotation:F1}°";

    /// <summary>
    /// Clears the selection info.
    /// </summary>
    public void Clear()
    {
        Count = 0;
        ElementType = "Nothing";
        X = 0;
        Y = 0;
        Width = 0;
        Height = 0;
        Rotation = 0;
    }

    /// <summary>
    /// Updates from a single element.
    /// </summary>
    public void UpdateFromElement(VectorElement element)
    {
        Count = 1;
        ElementType = element.GetType().Name.Replace("Svg", "");
        var bounds = element.GetBoundingBox();
        X = bounds.X;
        Y = bounds.Y;
        Width = bounds.Width;
        Height = bounds.Height;
        // Calculate rotation from transform matrix (atan2 of skew components)
        Rotation = Math.Atan2(element.Transform.SkewY, element.Transform.ScaleX) * 180 / Math.PI;
    }

    /// <summary>
    /// Updates from multiple elements.
    /// </summary>
    public void UpdateFromElements(IEnumerable<VectorElement> elements)
    {
        var list = elements.ToList();
        Count = list.Count;

        if (list.Count == 0)
        {
            Clear();
            return;
        }

        if (list.Count == 1)
        {
            UpdateFromElement(list[0]);
            return;
        }

        // Multiple selection
        var types = list.Select(e => e.GetType().Name).Distinct().ToList();
        ElementType = types.Count == 1 ? $"{types[0].Replace("Svg", "")}s" : "Mixed";

        var first = list[0].GetBoundingBox();
        var minX = first.X;
        var minY = first.Y;
        var maxX = first.X + first.Width;
        var maxY = first.Y + first.Height;

        foreach (var element in list.Skip(1))
        {
            var bounds = element.GetBoundingBox();
            minX = Math.Min(minX, bounds.X);
            minY = Math.Min(minY, bounds.Y);
            maxX = Math.Max(maxX, bounds.X + bounds.Width);
            maxY = Math.Max(maxY, bounds.Y + bounds.Height);
        }

        X = minX;
        Y = minY;
        Width = maxX - minX;
        Height = maxY - minY;
        Rotation = 0;
    }
}

/// <summary>
/// Element tooltip information.
/// </summary>
public class ElementTooltip
{
    public string Type { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public string Dimensions { get; init; } = string.Empty;
    public double X { get; init; }
    public double Y { get; init; }
    public bool IsVisible { get; set; }

    public static ElementTooltip FromElement(VectorElement element, double mouseX, double mouseY)
    {
        var bounds = element.GetBoundingBox();
        return new ElementTooltip
        {
            Type = element.GetType().Name.Replace("Svg", ""),
            Name = element.Name ?? "Unnamed",
            Dimensions = $"{bounds.Width:F0} × {bounds.Height:F0}",
            X = mouseX + 15,
            Y = mouseY + 15,
            IsVisible = true
        };
    }
}

/// <summary>
/// Service for managing on-canvas HUD elements.
/// </summary>
public class CanvasHUDService : INotifyPropertyChanged
{
    private bool _showContextualToolbar = true;
    private bool _showSelectionInfo = true;
    private bool _showZoomIndicator = true;
    private bool _showRulerCursor = true;
    private bool _showDistanceIndicators;
    private double _zoomLevel = 1.0;
    private (double X, double Y) _cursorPosition;
    private (double X, double Y, double Width, double Height)? _selectionBounds;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets the selection info.
    /// </summary>
    public SelectionInfo Selection { get; } = new();

    /// <summary>
    /// Gets the element tooltip.
    /// </summary>
    public ElementTooltip? Tooltip { get; private set; }

    /// <summary>
    /// Gets the quick actions for the contextual toolbar.
    /// </summary>
    public List<HUDAction> QuickActions { get; } = [];

    /// <summary>
    /// Gets or sets whether to show the contextual toolbar.
    /// </summary>
    public bool ShowContextualToolbar
    {
        get => _showContextualToolbar;
        set { _showContextualToolbar = value; OnPropertyChanged(nameof(ShowContextualToolbar)); }
    }

    /// <summary>
    /// Gets or sets whether to show selection info.
    /// </summary>
    public bool ShowSelectionInfo
    {
        get => _showSelectionInfo;
        set { _showSelectionInfo = value; OnPropertyChanged(nameof(ShowSelectionInfo)); }
    }

    /// <summary>
    /// Gets or sets whether to show the zoom indicator.
    /// </summary>
    public bool ShowZoomIndicator
    {
        get => _showZoomIndicator;
        set { _showZoomIndicator = value; OnPropertyChanged(nameof(ShowZoomIndicator)); }
    }

    /// <summary>
    /// Gets or sets whether to show ruler cursor marks.
    /// </summary>
    public bool ShowRulerCursor
    {
        get => _showRulerCursor;
        set { _showRulerCursor = value; OnPropertyChanged(nameof(ShowRulerCursor)); }
    }

    /// <summary>
    /// Gets or sets whether to show distance indicators (Alt key).
    /// </summary>
    public bool ShowDistanceIndicators
    {
        get => _showDistanceIndicators;
        set { _showDistanceIndicators = value; OnPropertyChanged(nameof(ShowDistanceIndicators)); }
    }

    /// <summary>
    /// Gets or sets the current zoom level.
    /// </summary>
    public double ZoomLevel
    {
        get => _zoomLevel;
        set { _zoomLevel = value; OnPropertyChanged(nameof(ZoomLevel)); OnPropertyChanged(nameof(ZoomText)); }
    }

    /// <summary>
    /// Gets the zoom level text.
    /// </summary>
    public string ZoomText => $"{ZoomLevel * 100:F0}%";

    /// <summary>
    /// Gets or sets the cursor position.
    /// </summary>
    public (double X, double Y) CursorPosition
    {
        get => _cursorPosition;
        set { _cursorPosition = value; OnPropertyChanged(nameof(CursorPosition)); OnPropertyChanged(nameof(CursorText)); }
    }

    /// <summary>
    /// Gets the cursor position text.
    /// </summary>
    public string CursorText => $"{CursorPosition.X:F0}, {CursorPosition.Y:F0}";

    /// <summary>
    /// Gets or sets the selection bounds.
    /// </summary>
    public (double X, double Y, double Width, double Height)? SelectionBounds
    {
        get => _selectionBounds;
        set { _selectionBounds = value; OnPropertyChanged(nameof(SelectionBounds)); OnPropertyChanged(nameof(ToolbarPosition)); }
    }

    /// <summary>
    /// Gets the contextual toolbar position.
    /// </summary>
    public (double X, double Y) ToolbarPosition
    {
        get
        {
            if (SelectionBounds == null)
                return (0, 0);

            var bounds = SelectionBounds.Value;
            // Position above selection, centered
            return (bounds.X + bounds.Width / 2, bounds.Y - 40);
        }
    }

    /// <summary>
    /// Event raised when HUD needs to be redrawn.
    /// </summary>
    public event EventHandler? HUDChanged;

    /// <summary>
    /// Registers default quick actions.
    /// </summary>
    public void RegisterDefaultActions()
    {
        QuickActions.Clear();
        QuickActions.AddRange([
            new HUDAction("group", "Group", "group", "Group selected objects (Ctrl+G)"),
            new HUDAction("ungroup", "Ungroup", "ungroup", "Ungroup selected objects (Ctrl+Shift+G)"),
            new HUDAction("union", "Union", "union", "Boolean union"),
            new HUDAction("subtract", "Subtract", "subtract", "Boolean subtract"),
            new HUDAction("duplicate", "Duplicate", "copy", "Duplicate selection (Ctrl+D)"),
            new HUDAction("delete", "Delete", "trash", "Delete selection (Del)"),
        ]);
    }

    /// <summary>
    /// Updates selection from elements.
    /// </summary>
    public void UpdateSelection(IEnumerable<VectorElement> elements)
    {
        var list = elements.ToList();
        Selection.UpdateFromElements(list);

        if (list.Count > 0)
        {
            var first = list[0].GetBoundingBox();
            var minX = first.X;
            var minY = first.Y;
            var maxX = first.X + first.Width;
            var maxY = first.Y + first.Height;

            foreach (var element in list.Skip(1))
            {
                var bounds = element.GetBoundingBox();
                minX = Math.Min(minX, bounds.X);
                minY = Math.Min(minY, bounds.Y);
                maxX = Math.Max(maxX, bounds.X + bounds.Width);
                maxY = Math.Max(maxY, bounds.Y + bounds.Height);
            }

            SelectionBounds = (minX, minY, maxX - minX, maxY - minY);
        }
        else
        {
            SelectionBounds = null;
        }

        HUDChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Shows tooltip for an element.
    /// </summary>
    public void ShowTooltip(VectorElement element, double mouseX, double mouseY)
    {
        Tooltip = ElementTooltip.FromElement(element, mouseX, mouseY);
        OnPropertyChanged(nameof(Tooltip));
        HUDChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Hides the tooltip.
    /// </summary>
    public void HideTooltip()
    {
        if (Tooltip != null)
        {
            Tooltip = null;
            OnPropertyChanged(nameof(Tooltip));
            HUDChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    /// <summary>
    /// Calculates toolbar position ensuring it stays on screen.
    /// </summary>
    public (double X, double Y) CalculateToolbarPosition(double canvasWidth, double canvasHeight, double toolbarWidth = 200, double toolbarHeight = 40)
    {
        if (SelectionBounds == null)
            return (canvasWidth / 2 - toolbarWidth / 2, 10);

        var bounds = SelectionBounds.Value;
        var x = bounds.X + bounds.Width / 2 - toolbarWidth / 2;
        var y = bounds.Y - toolbarHeight - 10;

        // Keep on screen
        x = Math.Max(10, Math.Min(x, canvasWidth - toolbarWidth - 10));

        // If above selection is off screen, place below
        if (y < 10)
        {
            y = bounds.Y + bounds.Height + 10;
        }

        // Still off screen? Place at top
        if (y + toolbarHeight > canvasHeight - 10)
        {
            y = 10;
        }

        return (x, y);
    }

    /// <summary>
    /// Calculates distances from selection to nearby elements.
    /// </summary>
    public IEnumerable<DistanceIndicator> CalculateDistances(IEnumerable<VectorElement> allElements, IEnumerable<VectorElement> selectedElements)
    {
        if (!ShowDistanceIndicators || SelectionBounds == null)
            yield break;

        var selected = selectedElements.ToHashSet();
        var bounds = SelectionBounds.Value;

        foreach (var element in allElements.Where(e => !selected.Contains(e)))
        {
            var otherBounds = element.GetBoundingBox();

            // Horizontal distance
            if (Math.Abs((bounds.Y + bounds.Height / 2) - (otherBounds.Y + otherBounds.Height / 2)) < 50)
            {
                double distance;
                double y = bounds.Y + bounds.Height / 2;
                double x1, x2;

                if (bounds.X > otherBounds.X + otherBounds.Width)
                {
                    // Selection is to the right
                    distance = bounds.X - (otherBounds.X + otherBounds.Width);
                    x1 = otherBounds.X + otherBounds.Width;
                    x2 = bounds.X;
                }
                else if (otherBounds.X > bounds.X + bounds.Width)
                {
                    // Selection is to the left
                    distance = otherBounds.X - (bounds.X + bounds.Width);
                    x1 = bounds.X + bounds.Width;
                    x2 = otherBounds.X;
                }
                else
                {
                    continue;
                }

                if (distance > 0 && distance < 500)
                {
                    yield return new DistanceIndicator
                    {
                        StartX = x1,
                        StartY = y,
                        EndX = x2,
                        EndY = y,
                        Distance = distance,
                        IsHorizontal = true
                    };
                }
            }

            // Vertical distance
            if (Math.Abs((bounds.X + bounds.Width / 2) - (otherBounds.X + otherBounds.Width / 2)) < 50)
            {
                double distance;
                double x = bounds.X + bounds.Width / 2;
                double y1, y2;

                if (bounds.Y > otherBounds.Y + otherBounds.Height)
                {
                    // Selection is below
                    distance = bounds.Y - (otherBounds.Y + otherBounds.Height);
                    y1 = otherBounds.Y + otherBounds.Height;
                    y2 = bounds.Y;
                }
                else if (otherBounds.Y > bounds.Y + bounds.Height)
                {
                    // Selection is above
                    distance = otherBounds.Y - (bounds.Y + bounds.Height);
                    y1 = bounds.Y + bounds.Height;
                    y2 = otherBounds.Y;
                }
                else
                {
                    continue;
                }

                if (distance > 0 && distance < 500)
                {
                    yield return new DistanceIndicator
                    {
                        StartX = x,
                        StartY = y1,
                        EndX = x,
                        EndY = y2,
                        Distance = distance,
                        IsHorizontal = false
                    };
                }
            }
        }
    }
}

/// <summary>
/// Represents a distance indicator line.
/// </summary>
public class DistanceIndicator
{
    public double StartX { get; init; }
    public double StartY { get; init; }
    public double EndX { get; init; }
    public double EndY { get; init; }
    public double Distance { get; init; }
    public bool IsHorizontal { get; init; }

    /// <summary>
    /// Gets the label position.
    /// </summary>
    public (double X, double Y) LabelPosition => ((StartX + EndX) / 2, (StartY + EndY) / 2);

    /// <summary>
    /// Gets the formatted distance text.
    /// </summary>
    public string DistanceText => $"{Distance:F0}";
}
