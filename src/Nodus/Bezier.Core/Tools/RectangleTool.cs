namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

/// <summary>
/// Tool for creating rectangle shapes.
/// </summary>
public class RectangleTool : ToolBase
{
    private SvgRect? _previewRect;
    private bool _isDrawing;

    /// <inheritdoc/>
    public override string Name => "Rectangle";

    /// <inheritdoc/>
    public override string Icon => "Square";

    /// <inheritdoc/>
    public override ToolCursor Cursor => ToolCursor.Cross;

    /// <inheritdoc/>
    public override string? Shortcut => "R";

    /// <summary>
    /// Gets or sets the default fill color for new rectangles.
    /// </summary>
    public uint DefaultFillColor { get; set; } = 0xFF89B4FA;

    /// <summary>
    /// Gets or sets the default stroke color for new rectangles.
    /// </summary>
    public uint DefaultStrokeColor { get; set; } = 0x00000000;

    /// <summary>
    /// Gets or sets the default stroke width for new rectangles.
    /// </summary>
    public double DefaultStrokeWidth { get; set; } = 0;

    /// <summary>
    /// Gets or sets the default corner radius for new rectangles.
    /// </summary>
    public double DefaultCornerRadius { get; set; } = 0;

    /// <summary>
    /// Event raised when drawing dimensions change.
    /// </summary>
    public event EventHandler<(double Width, double Height)>? DimensionsChanged;

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        _previewRect = null;
        _isDrawing = false;
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

        _isDrawing = true;
        _previewRect = new SvgRect
        {
            X = point.X,
            Y = point.Y,
            Width = 0,
            Height = 0,
            Fill = new SolidFill { Color = DefaultFillColor },
            Stroke = DefaultStrokeWidth > 0 ? new Stroke { Fill = new SolidFill { Color = DefaultStrokeColor }, Width = DefaultStrokeWidth } : null,
            Rx = DefaultCornerRadius,
            Ry = DefaultCornerRadius,
            Name = GenerateName()
        };

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseMove(point, modifiers);

        if (!_isDrawing || _previewRect is null) return false;

        UpdatePreviewRect(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (!_isDrawing || _previewRect is null || Document is null)
        {
            base.OnMouseUp(point, modifiers);
            return false;
        }

        UpdatePreviewRect(point, modifiers);

        // Only add if rectangle has meaningful size
        if (_previewRect.Width > 1 && _previewRect.Height > 1)
        {
            var command = new AddElementCommand(Document, _previewRect);
            History?.ExecuteCommand(command);
        }

        _previewRect = null;
        _isDrawing = false;
        base.OnMouseUp(point, modifiers);
        return true;
    }

    private void UpdatePreviewRect(ToolPoint point, KeyModifiers modifiers)
    {
        if (_previewRect is null) return;

        var startX = DragStartPoint.X;
        var startY = DragStartPoint.Y;
        var endX = point.X;
        var endY = point.Y;

        var width = endX - startX;
        var height = endY - startY;

        // Alt: Draw from center
        if (modifiers.HasFlag(KeyModifiers.Alt))
        {
            width *= 2;
            height *= 2;
            startX -= Math.Abs(width) / 2;
            startY -= Math.Abs(height) / 2;
        }

        // Shift: Constrain to square
        if (modifiers.HasFlag(KeyModifiers.Shift))
        {
            var size = Math.Max(Math.Abs(width), Math.Abs(height));
            width = width >= 0 ? size : -size;
            height = height >= 0 ? size : -size;
        }

        // Handle negative dimensions (dragging up/left)
        if (width < 0)
        {
            startX += width;
            width = -width;
        }
        if (height < 0)
        {
            startY += height;
            height = -height;
        }

        _previewRect.X = startX;
        _previewRect.Y = startY;
        _previewRect.Width = width;
        _previewRect.Height = height;

        DimensionsChanged?.Invoke(this, (width, height));
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (!_isDrawing || _previewRect is null) return;

        const uint previewColor = 0xFF89B4FA; // Blue
        const uint previewFill = 0x2089B4FA; // Semi-transparent blue

        // Draw preview rectangle
        context.DrawRect(
            _previewRect.X, _previewRect.Y,
            _previewRect.Width, _previewRect.Height,
            previewFill, 1f, true);
        context.DrawRect(
            _previewRect.X, _previewRect.Y,
            _previewRect.Width, _previewRect.Height,
            previewColor, 1.5f, false);

        // Draw dimensions text
        var dimText = $"{_previewRect.Width:0.#} × {_previewRect.Height:0.#}";
        context.DrawText(dimText, 
            _previewRect.X + _previewRect.Width / 2, 
            _previewRect.Y + _previewRect.Height + 16,
            0xFFFFFFFF, 11f);
    }

    private string GenerateName()
    {
        return $"Rectangle {DateTime.Now:HHmmss}";
    }
}
