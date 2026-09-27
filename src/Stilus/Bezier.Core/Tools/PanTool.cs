namespace Bezier.Core.Tools;

using Bezier.Core.Interfaces;

/// <summary>
/// Tool for panning the canvas view.
/// </summary>
public class PanTool : ToolBase
{
    /// <inheritdoc/>
    public override string Name => "Pan";

    /// <inheritdoc/>
    public override string Icon => "HandLeft";

    /// <inheritdoc/>
    public override ToolCursor Cursor => IsDragging ? ToolCursor.Hand : ToolCursor.Hand;

    /// <inheritdoc/>
    public override string? Shortcut => "H";

    /// <summary>
    /// Event raised when pan delta changes during drag.
    /// </summary>
    public event EventHandler<(double DeltaX, double DeltaY)>? PanDelta;

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        if (!IsDragging) return false;

        var previousPoint = CurrentPoint;
        base.OnMouseMove(point, modifiers);

        // Calculate delta from last position (not from start)
        var deltaX = point.X - previousPoint.X;
        var deltaY = point.Y - previousPoint.Y;

        PanDelta?.Invoke(this, (deltaX, deltaY));
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseUp(point, modifiers);
        return true;
    }
}
