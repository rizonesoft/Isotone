namespace Bezier.Core.Services;

/// <summary>
/// Types of canvas tooltips.
/// </summary>
public enum TooltipType
{
    None,
    Dimensions,
    Angle,
    Distance,
    Position,
    Custom
}

/// <summary>
/// Data for a canvas tooltip.
/// </summary>
public record CanvasTooltip(
    double X,
    double Y,
    string Text,
    TooltipType Type = TooltipType.Custom
);

/// <summary>
/// Service for managing canvas tooltips that appear during drawing operations.
/// </summary>
public class CanvasTooltipService
{
    private CanvasTooltip? _activeTooltip;

    /// <summary>
    /// Gets or sets whether tooltips are enabled.
    /// </summary>
    public bool IsEnabled { get; set; } = true;

    /// <summary>
    /// Gets or sets the offset from the cursor position.
    /// </summary>
    public double OffsetX { get; set; } = 15;

    /// <summary>
    /// Gets or sets the offset from the cursor position.
    /// </summary>
    public double OffsetY { get; set; } = 15;

    /// <summary>
    /// Gets the active tooltip, if any.
    /// </summary>
    public CanvasTooltip? ActiveTooltip => _activeTooltip;

    /// <summary>
    /// Event raised when the tooltip changes.
    /// </summary>
    public event EventHandler<CanvasTooltip?>? TooltipChanged;

    /// <summary>
    /// Shows a dimensions tooltip (width x height).
    /// </summary>
    public void ShowDimensions(double x, double y, double width, double height)
    {
        if (!IsEnabled) return;

        var text = $"{Math.Abs(width):F1} × {Math.Abs(height):F1}";
        SetTooltip(new CanvasTooltip(x + OffsetX, y + OffsetY, text, TooltipType.Dimensions));
    }

    /// <summary>
    /// Shows an angle tooltip.
    /// </summary>
    public void ShowAngle(double x, double y, double angleDegrees)
    {
        if (!IsEnabled) return;

        var normalizedAngle = ((angleDegrees % 360) + 360) % 360;
        var text = $"{normalizedAngle:F1}°";
        SetTooltip(new CanvasTooltip(x + OffsetX, y + OffsetY, text, TooltipType.Angle));
    }

    /// <summary>
    /// Shows an angle and distance tooltip.
    /// </summary>
    public void ShowAngleAndDistance(double x, double y, double angleDegrees, double distance)
    {
        if (!IsEnabled) return;

        var normalizedAngle = ((angleDegrees % 360) + 360) % 360;
        var text = $"{normalizedAngle:F1}° | {distance:F1}";
        SetTooltip(new CanvasTooltip(x + OffsetX, y + OffsetY, text, TooltipType.Angle));
    }

    /// <summary>
    /// Shows a distance tooltip.
    /// </summary>
    public void ShowDistance(double x, double y, double distance)
    {
        if (!IsEnabled) return;

        var text = $"{distance:F1} px";
        SetTooltip(new CanvasTooltip(x + OffsetX, y + OffsetY, text, TooltipType.Distance));
    }

    /// <summary>
    /// Shows a position tooltip.
    /// </summary>
    public void ShowPosition(double x, double y)
    {
        if (!IsEnabled) return;

        var text = $"X: {x:F1}, Y: {y:F1}";
        SetTooltip(new CanvasTooltip(x + OffsetX, y + OffsetY, text, TooltipType.Position));
    }

    /// <summary>
    /// Shows a custom tooltip.
    /// </summary>
    public void ShowCustom(double x, double y, string text)
    {
        if (!IsEnabled) return;

        SetTooltip(new CanvasTooltip(x + OffsetX, y + OffsetY, text, TooltipType.Custom));
    }

    /// <summary>
    /// Hides the current tooltip.
    /// </summary>
    public void Hide()
    {
        if (_activeTooltip != null)
        {
            _activeTooltip = null;
            TooltipChanged?.Invoke(this, null);
        }
    }

    private void SetTooltip(CanvasTooltip tooltip)
    {
        _activeTooltip = tooltip;
        TooltipChanged?.Invoke(this, tooltip);
    }

    /// <summary>
    /// Calculates angle between two points in degrees.
    /// </summary>
    public static double CalculateAngle(double x1, double y1, double x2, double y2)
    {
        var deltaX = x2 - x1;
        var deltaY = y2 - y1;
        var radians = Math.Atan2(deltaY, deltaX);
        return radians * 180.0 / Math.PI;
    }

    /// <summary>
    /// Calculates distance between two points.
    /// </summary>
    public static double CalculateDistance(double x1, double y1, double x2, double y2)
    {
        var deltaX = x2 - x1;
        var deltaY = y2 - y1;
        return Math.Sqrt(deltaX * deltaX + deltaY * deltaY);
    }
}
