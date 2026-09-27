namespace Bezier.Core.Tools;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Services;

/// <summary>
/// Base class for tools providing common functionality.
/// </summary>
public abstract class ToolBase : ITool
{
    protected VectorDocument? Document { get; private set; }
    protected HistoryManager? History { get; private set; }
    protected bool IsDragging { get; set; }
    protected ToolPoint DragStartPoint { get; set; }
    protected ToolPoint CurrentPoint { get; set; }

    /// <inheritdoc/>
    public abstract string Name { get; }

    /// <inheritdoc/>
    public abstract string Icon { get; }

    /// <inheritdoc/>
    public virtual ToolCursor Cursor => ToolCursor.Arrow;

    /// <inheritdoc/>
    public virtual string? Shortcut => null;

    /// <summary>
    /// Sets the document context for the tool.
    /// </summary>
    public void SetContext(VectorDocument? document, HistoryManager? history)
    {
        Document = document;
        History = history;
    }

    /// <inheritdoc/>
    public virtual void OnActivate() { }

    /// <inheritdoc/>
    public virtual void OnDeactivate()
    {
        IsDragging = false;
    }

    /// <inheritdoc/>
    public virtual bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        DragStartPoint = point;
        CurrentPoint = point;
        IsDragging = true;
        return false;
    }

    /// <inheritdoc/>
    public virtual bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        CurrentPoint = point;
        return false;
    }

    /// <inheritdoc/>
    public virtual bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        CurrentPoint = point;
        IsDragging = false;
        return false;
    }

    /// <inheritdoc/>
    public virtual bool OnKeyDown(string key, KeyModifiers modifiers) => false;

    /// <inheritdoc/>
    public virtual bool OnKeyUp(string key, KeyModifiers modifiers) => false;

    /// <inheritdoc/>
    public virtual void RenderOverlay(IToolRenderContext context) { }

    /// <summary>
    /// Gets the drag delta from start to current point.
    /// </summary>
    protected (double DeltaX, double DeltaY) GetDragDelta()
    {
        return (CurrentPoint.X - DragStartPoint.X, CurrentPoint.Y - DragStartPoint.Y);
    }

    /// <summary>
    /// Gets the bounding rectangle of the drag operation.
    /// </summary>
    protected (double X, double Y, double Width, double Height) GetDragBounds()
    {
        var x = Math.Min(DragStartPoint.X, CurrentPoint.X);
        var y = Math.Min(DragStartPoint.Y, CurrentPoint.Y);
        var width = Math.Abs(CurrentPoint.X - DragStartPoint.X);
        var height = Math.Abs(CurrentPoint.Y - DragStartPoint.Y);
        return (x, y, width, height);
    }
}
