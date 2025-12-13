namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

/// <summary>
/// Tool for creating line shapes.
/// </summary>
public class LineTool : ToolBase
{
    private SvgLine? _previewLine;
    private bool _isDrawing;

    /// <inheritdoc/>
    public override string Name => "Line";

    /// <inheritdoc/>
    public override string Icon => "LineHorizontal1";

    /// <inheritdoc/>
    public override ToolCursor Cursor => ToolCursor.Cross;

    /// <inheritdoc/>
    public override string? Shortcut => "L";

    /// <summary>
    /// Gets or sets the default stroke color for new lines.
    /// </summary>
    public uint DefaultStrokeColor { get; set; } = 0xFFCDD6F4;

    /// <summary>
    /// Gets or sets the default stroke width for new lines.
    /// </summary>
    public double DefaultStrokeWidth { get; set; } = 2;

    /// <summary>
    /// Event raised when drawing dimensions change.
    /// </summary>
    public event EventHandler<(double Length, double Angle)>? DimensionsChanged;

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        _previewLine = null;
        _isDrawing = false;
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

        _isDrawing = true;
        _previewLine = new SvgLine
        {
            X1 = point.X,
            Y1 = point.Y,
            X2 = point.X,
            Y2 = point.Y,
            Stroke = new Stroke { Fill = new SolidFill { Color = DefaultStrokeColor }, Width = DefaultStrokeWidth },
            Name = GenerateName()
        };

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseMove(point, modifiers);

        if (!_isDrawing || _previewLine is null) return false;

        UpdatePreviewLine(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (!_isDrawing || _previewLine is null || Document is null)
        {
            base.OnMouseUp(point, modifiers);
            return false;
        }

        UpdatePreviewLine(point, modifiers);

        // Only add if line has meaningful length
        var length = CalculateLength(_previewLine);
        if (length > 1)
        {
            var command = new AddElementCommand(Document, _previewLine);
            History?.ExecuteCommand(command);
        }

        _previewLine = null;
        _isDrawing = false;
        base.OnMouseUp(point, modifiers);
        return true;
    }

    private void UpdatePreviewLine(ToolPoint point, KeyModifiers modifiers)
    {
        if (_previewLine is null) return;

        var endX = point.X;
        var endY = point.Y;

        // Shift: Constrain to 45° angles
        if (modifiers.HasFlag(KeyModifiers.Shift))
        {
            var dx = endX - _previewLine.X1;
            var dy = endY - _previewLine.Y1;
            var angle = Math.Atan2(dy, dx);
            
            // Snap to nearest 45° (π/4 radians)
            var snappedAngle = Math.Round(angle / (Math.PI / 4)) * (Math.PI / 4);
            var length = Math.Sqrt(dx * dx + dy * dy);
            
            endX = _previewLine.X1 + length * Math.Cos(snappedAngle);
            endY = _previewLine.Y1 + length * Math.Sin(snappedAngle);
        }

        _previewLine.X2 = endX;
        _previewLine.Y2 = endY;

        var lineLength = CalculateLength(_previewLine);
        var lineAngle = CalculateAngle(_previewLine);
        DimensionsChanged?.Invoke(this, (lineLength, lineAngle));
    }

    private static double CalculateLength(SvgLine line)
    {
        var dx = line.X2 - line.X1;
        var dy = line.Y2 - line.Y1;
        return Math.Sqrt(dx * dx + dy * dy);
    }

    private static double CalculateAngle(SvgLine line)
    {
        var dx = line.X2 - line.X1;
        var dy = line.Y2 - line.Y1;
        var angle = Math.Atan2(dy, dx) * (180 / Math.PI);
        return angle;
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (!_isDrawing || _previewLine is null) return;

        const uint previewColor = 0xFFCDD6F4; // Text color

        // Draw preview line
        context.DrawLine(
            _previewLine.X1, _previewLine.Y1,
            _previewLine.X2, _previewLine.Y2,
            previewColor, 2f);

        // Draw endpoint markers
        const double markerSize = 4;
        context.DrawEllipse(_previewLine.X1, _previewLine.Y1, markerSize, markerSize, previewColor, 1f, true);
        context.DrawEllipse(_previewLine.X2, _previewLine.Y2, markerSize, markerSize, previewColor, 1f, true);

        // Draw dimensions text
        var length = CalculateLength(_previewLine);
        var angle = CalculateAngle(_previewLine);
        var midX = (_previewLine.X1 + _previewLine.X2) / 2;
        var midY = (_previewLine.Y1 + _previewLine.Y2) / 2;
        var dimText = $"{length:0.#}px  {angle:0.#}°";
        context.DrawText(dimText, midX, midY - 12, 0xFFFFFFFF, 11f);
    }

    private string GenerateName()
    {
        return $"Line {DateTime.Now:HHmmss}";
    }
}
