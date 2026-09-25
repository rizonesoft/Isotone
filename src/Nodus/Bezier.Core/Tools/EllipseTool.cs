namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

/// <summary>
/// Tool for creating ellipse shapes.
/// </summary>
public class EllipseTool : ToolBase
{
    private SvgEllipse? _previewEllipse;
    private bool _isDrawing;

    /// <inheritdoc/>
    public override string Name => "Ellipse";

    /// <inheritdoc/>
    public override string Icon => "Circle";

    /// <inheritdoc/>
    public override ToolCursor Cursor => ToolCursor.Cross;

    /// <inheritdoc/>
    public override string? Shortcut => "E";

    /// <summary>
    /// Gets or sets the default fill color for new ellipses.
    /// </summary>
    public uint DefaultFillColor { get; set; } = 0xFFA6E3A1;

    /// <summary>
    /// Gets or sets the default stroke color for new ellipses.
    /// </summary>
    public uint DefaultStrokeColor { get; set; } = 0x00000000;

    /// <summary>
    /// Gets or sets the default stroke width for new ellipses.
    /// </summary>
    public double DefaultStrokeWidth { get; set; } = 0;

    /// <summary>
    /// Event raised when drawing dimensions change.
    /// </summary>
    public event EventHandler<(double Width, double Height)>? DimensionsChanged;

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        _previewEllipse = null;
        _isDrawing = false;
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

        _isDrawing = true;
        _previewEllipse = new SvgEllipse
        {
            Cx = point.X,
            Cy = point.Y,
            Rx = 0,
            Ry = 0,
            Fill = new SolidFill { Color = DefaultFillColor },
            Stroke = DefaultStrokeWidth > 0 ? new Stroke { Fill = new SolidFill { Color = DefaultStrokeColor }, Width = DefaultStrokeWidth } : null,
            Name = GenerateName()
        };

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseMove(point, modifiers);

        if (!_isDrawing || _previewEllipse is null) return false;

        UpdatePreviewEllipse(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (!_isDrawing || _previewEllipse is null || Document is null)
        {
            base.OnMouseUp(point, modifiers);
            return false;
        }

        UpdatePreviewEllipse(point, modifiers);

        // Only add if ellipse has meaningful size
        if (_previewEllipse.Rx > 1 && _previewEllipse.Ry > 1)
        {
            var command = new AddElementCommand(Document, _previewEllipse);
            History?.ExecuteCommand(command);
        }

        _previewEllipse = null;
        _isDrawing = false;
        base.OnMouseUp(point, modifiers);
        return true;
    }

    private void UpdatePreviewEllipse(ToolPoint point, KeyModifiers modifiers)
    {
        if (_previewEllipse is null) return;

        var startX = DragStartPoint.X;
        var startY = DragStartPoint.Y;
        var endX = point.X;
        var endY = point.Y;

        var width = Math.Abs(endX - startX);
        var height = Math.Abs(endY - startY);

        // Shift: Constrain to circle
        if (modifiers.HasFlag(KeyModifiers.Shift))
        {
            var size = Math.Max(width, height);
            width = size;
            height = size;
        }

        var rx = width / 2;
        var ry = height / 2;

        // Alt: Draw from center
        double cx, cy;
        if (modifiers.HasFlag(KeyModifiers.Alt))
        {
            cx = startX;
            cy = startY;
            rx = width;
            ry = height;
        }
        else
        {
            // Draw from corner - calculate center
            var minX = Math.Min(startX, endX);
            var minY = Math.Min(startY, endY);
            cx = minX + rx;
            cy = minY + ry;
        }

        _previewEllipse.Cx = cx;
        _previewEllipse.Cy = cy;
        _previewEllipse.Rx = rx;
        _previewEllipse.Ry = ry;

        DimensionsChanged?.Invoke(this, (rx * 2, ry * 2));
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (!_isDrawing || _previewEllipse is null) return;

        const uint previewColor = 0xFFA6E3A1; // Green
        const uint previewFill = 0x20A6E3A1; // Semi-transparent green

        // Draw preview ellipse
        context.DrawEllipse(
            _previewEllipse.Cx, _previewEllipse.Cy,
            _previewEllipse.Rx, _previewEllipse.Ry,
            previewFill, 1f, true);
        context.DrawEllipse(
            _previewEllipse.Cx, _previewEllipse.Cy,
            _previewEllipse.Rx, _previewEllipse.Ry,
            previewColor, 1.5f, false);

        // Draw dimensions text
        var dimText = $"{_previewEllipse.Rx * 2:0.#} × {_previewEllipse.Ry * 2:0.#}";
        context.DrawText(dimText,
            _previewEllipse.Cx,
            _previewEllipse.Cy + _previewEllipse.Ry + 16,
            0xFFFFFFFF, 11f);
    }

    private string GenerateName()
    {
        return $"Ellipse {DateTime.Now:HHmmss}";
    }
}
