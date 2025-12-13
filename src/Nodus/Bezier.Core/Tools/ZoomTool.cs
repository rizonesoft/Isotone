namespace Bezier.Core.Tools;

using Bezier.Core.Interfaces;

/// <summary>
/// Tool for zooming the canvas view.
/// </summary>
public class ZoomTool : ToolBase
{
    private bool _isZoomOut;

    /// <inheritdoc/>
    public override string Name => "Zoom";

    /// <inheritdoc/>
    public override string Icon => "ZoomIn";

    /// <inheritdoc/>
    public override ToolCursor Cursor => _isZoomOut ? ToolCursor.ZoomOut : ToolCursor.ZoomIn;

    /// <inheritdoc/>
    public override string? Shortcut => "Z";

    /// <summary>
    /// Event raised when zoom is requested.
    /// </summary>
    public event EventHandler<(double CenterX, double CenterY, double Factor)>? ZoomRequested;

    /// <summary>
    /// Event raised when zoom to area is requested.
    /// </summary>
    public event EventHandler<(double X, double Y, double Width, double Height)>? ZoomToAreaRequested;

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);
        _isZoomOut = modifiers.HasFlag(KeyModifiers.Alt);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        _isZoomOut = modifiers.HasFlag(KeyModifiers.Alt);
        base.OnMouseMove(point, modifiers);
        return IsDragging;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (!IsDragging)
        {
            base.OnMouseUp(point, modifiers);
            return false;
        }

        var (x, y, w, h) = GetDragBounds();

        // If drag was minimal, treat as click zoom
        if (w < 5 && h < 5)
        {
            var factor = _isZoomOut ? 0.5 : 2.0;
            ZoomRequested?.Invoke(this, (point.X, point.Y, factor));
        }
        else
        {
            // Zoom to dragged area
            ZoomToAreaRequested?.Invoke(this, (x, y, w, h));
        }

        base.OnMouseUp(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnKeyDown(string key, KeyModifiers modifiers)
    {
        if (key == "Alt")
        {
            _isZoomOut = true;
            return true;
        }
        return false;
    }

    /// <inheritdoc/>
    public override bool OnKeyUp(string key, KeyModifiers modifiers)
    {
        if (key == "Alt")
        {
            _isZoomOut = false;
            return true;
        }
        return false;
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (!IsDragging) return;

        var (x, y, w, h) = GetDragBounds();
        
        // Only draw if significant drag
        if (w > 5 || h > 5)
        {
            const uint zoomAreaColor = 0x4089B4FA; // Semi-transparent blue
            const uint zoomBorderColor = 0xFF89B4FA; // Blue

            context.DrawRect(x, y, w, h, zoomAreaColor, 1f, true);
            context.DrawRect(x, y, w, h, zoomBorderColor, 1.5f, false);
        }
    }
}
