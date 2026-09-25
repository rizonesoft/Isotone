namespace Bezier.Core.Services;

/// <summary>
/// Types of visual feedback indicators.
/// </summary>
public enum FeedbackType
{
    SnapLine,
    SelectionHighlight,
    HandleHover,
    DragGhost,
    AlignmentGuide
}

/// <summary>
/// A visual feedback indicator.
/// </summary>
public record FeedbackIndicator(
    FeedbackType Type,
    double X1,
    double Y1,
    double X2,
    double Y2,
    uint Color,
    DateTime CreatedAt
);

/// <summary>
/// Service for managing visual feedback indicators on the canvas.
/// </summary>
public class VisualFeedbackService
{
    private readonly List<FeedbackIndicator> _indicators = [];
    private readonly object _lock = new();

    /// <summary>
    /// Gets or sets whether visual feedback is enabled.
    /// </summary>
    public bool IsEnabled { get; set; } = true;

    /// <summary>
    /// Gets or sets the duration for flash effects in milliseconds.
    /// </summary>
    public int FlashDurationMs { get; set; } = 300;

    /// <summary>
    /// Gets or sets the snap line color.
    /// </summary>
    public uint SnapLineColor { get; set; } = 0xFFFF6B6B;

    /// <summary>
    /// Gets or sets the alignment guide color.
    /// </summary>
    public uint AlignmentGuideColor { get; set; } = 0xFF89B4FA;

    /// <summary>
    /// Gets or sets the selection highlight color.
    /// </summary>
    public uint SelectionHighlightColor { get; set; } = 0x4089B4FA;

    /// <summary>
    /// Gets the active indicators.
    /// </summary>
    public IReadOnlyList<FeedbackIndicator> ActiveIndicators
    {
        get
        {
            lock (_lock)
            {
                CleanupExpiredIndicators();
                return [.. _indicators];
            }
        }
    }

    /// <summary>
    /// Event raised when indicators change.
    /// </summary>
    public event EventHandler? IndicatorsChanged;

    /// <summary>
    /// Shows a snap line flash.
    /// </summary>
    public void ShowSnapLine(double x1, double y1, double x2, double y2)
    {
        if (!IsEnabled) return;

        AddIndicator(new FeedbackIndicator(
            FeedbackType.SnapLine,
            x1, y1, x2, y2,
            SnapLineColor,
            DateTime.UtcNow
        ));
    }

    /// <summary>
    /// Shows a vertical snap line.
    /// </summary>
    public void ShowVerticalSnapLine(double x, double top, double bottom)
    {
        ShowSnapLine(x, top, x, bottom);
    }

    /// <summary>
    /// Shows a horizontal snap line.
    /// </summary>
    public void ShowHorizontalSnapLine(double y, double left, double right)
    {
        ShowSnapLine(left, y, right, y);
    }

    /// <summary>
    /// Shows an alignment guide.
    /// </summary>
    public void ShowAlignmentGuide(double x1, double y1, double x2, double y2)
    {
        if (!IsEnabled) return;

        AddIndicator(new FeedbackIndicator(
            FeedbackType.AlignmentGuide,
            x1, y1, x2, y2,
            AlignmentGuideColor,
            DateTime.UtcNow
        ));
    }

    /// <summary>
    /// Shows a selection highlight rectangle.
    /// </summary>
    public void ShowSelectionHighlight(double x, double y, double width, double height)
    {
        if (!IsEnabled) return;

        AddIndicator(new FeedbackIndicator(
            FeedbackType.SelectionHighlight,
            x, y, x + width, y + height,
            SelectionHighlightColor,
            DateTime.UtcNow
        ));
    }

    /// <summary>
    /// Shows handle hover feedback.
    /// </summary>
    public void ShowHandleHover(double x, double y, double size = 10)
    {
        if (!IsEnabled) return;

        var half = size / 2;
        AddIndicator(new FeedbackIndicator(
            FeedbackType.HandleHover,
            x - half, y - half, x + half, y + half,
            SelectionHighlightColor,
            DateTime.UtcNow
        ));
    }

    /// <summary>
    /// Clears all indicators.
    /// </summary>
    public void Clear()
    {
        lock (_lock)
        {
            if (_indicators.Count > 0)
            {
                _indicators.Clear();
                IndicatorsChanged?.Invoke(this, EventArgs.Empty);
            }
        }
    }

    /// <summary>
    /// Clears indicators of a specific type.
    /// </summary>
    public void Clear(FeedbackType type)
    {
        lock (_lock)
        {
            var removed = _indicators.RemoveAll(i => i.Type == type);
            if (removed > 0)
            {
                IndicatorsChanged?.Invoke(this, EventArgs.Empty);
            }
        }
    }

    private void AddIndicator(FeedbackIndicator indicator)
    {
        lock (_lock)
        {
            _indicators.Add(indicator);
            IndicatorsChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    private void CleanupExpiredIndicators()
    {
        var cutoff = DateTime.UtcNow.AddMilliseconds(-FlashDurationMs);
        _indicators.RemoveAll(i => i.CreatedAt < cutoff);
    }

    /// <summary>
    /// Gets opacity for a flash indicator (fades out over time).
    /// </summary>
    public double GetIndicatorOpacity(FeedbackIndicator indicator)
    {
        var elapsed = (DateTime.UtcNow - indicator.CreatedAt).TotalMilliseconds;
        var remaining = Math.Max(0, FlashDurationMs - elapsed);
        return remaining / FlashDurationMs;
    }
}
