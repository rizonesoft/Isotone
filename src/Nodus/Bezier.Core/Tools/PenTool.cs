namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

/// <summary>
/// Tool for creating bezier paths with control points.
/// </summary>
public class PenTool : ToolBase
{
    private readonly List<ControlPoint> _points = [];
    private ControlPoint? _currentPoint;
    private bool _isDragging;
    private bool _isDrawing;
    private (double X, double Y)? _previewPoint;

    private const double SnapRadius = 10.0;

    /// <inheritdoc/>
    public override string Name => "Pen";

    /// <inheritdoc/>
    public override string Icon => "Pen";

    /// <inheritdoc/>
    public override ToolCursor Cursor => ToolCursor.Cross;

    /// <inheritdoc/>
    public override string? Shortcut => "P";

    /// <summary>
    /// Gets or sets the default stroke color for new paths.
    /// </summary>
    public uint DefaultStrokeColor { get; set; } = 0xFFCDD6F4;

    /// <summary>
    /// Gets or sets the default stroke width for new paths.
    /// </summary>
    public double DefaultStrokeWidth { get; set; } = 2;

    /// <summary>
    /// Gets or sets whether to fill closed paths.
    /// </summary>
    public bool FillClosedPaths { get; set; } = true;

    /// <summary>
    /// Gets or sets the default fill color for closed paths.
    /// </summary>
    public uint DefaultFillColor { get; set; } = 0x4089B4FA;

    /// <summary>
    /// Event raised when the path points change.
    /// </summary>
    public event EventHandler? PathChanged;

    /// <summary>
    /// Event raised when near the first point (can close path).
    /// </summary>
    public event EventHandler<bool>? CanCloseChanged;

    /// <inheritdoc/>
    public override void OnActivate()
    {
        base.OnActivate();
        ClearPath();
    }

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        if (_isDrawing && _points.Count >= 2)
        {
            FinishPath(false);
        }
        ClearPath();
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

        // Check if clicking on first point to close path
        if (_points.Count >= 2 && IsNearFirstPoint(point.X, point.Y))
        {
            FinishPath(true);
            return true;
        }

        _isDrawing = true;
        _isDragging = false;

        // Create new control point
        _currentPoint = ControlPoint.CreateCorner(point.X, point.Y);

        // Alt modifier creates a cusp (corner) point even when dragging
        if (modifiers.HasFlag(KeyModifiers.Alt))
        {
            _currentPoint.Type = ControlPointType.Corner;
        }

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseMove(point, modifiers);

        _previewPoint = (point.X, point.Y);

        // Check if we can close the path
        var canClose = _points.Count >= 2 && IsNearFirstPoint(point.X, point.Y);
        CanCloseChanged?.Invoke(this, canClose);

        if (_currentPoint is null) return false;

        // If we've moved enough, start dragging to create handles
        var dx = point.X - _currentPoint.Position.X;
        var dy = point.Y - _currentPoint.Position.Y;
        var distance = Math.Sqrt(dx * dx + dy * dy);

        if (distance > 3)
        {
            _isDragging = true;

            // Alt modifier: break tangent (create corner with one handle)
            if (modifiers.HasFlag(KeyModifiers.Alt))
            {
                _currentPoint.Type = ControlPointType.Corner;
                _currentPoint.OutHandle = (dx, dy);
            }
            else
            {
                // Normal drag creates smooth point
                _currentPoint.Type = ControlPointType.Smooth;
                _currentPoint.SetOutHandle(dx, dy);
            }
        }

        PathChanged?.Invoke(this, EventArgs.Empty);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (_currentPoint is null)
        {
            base.OnMouseUp(point, modifiers);
            return false;
        }

        // Finalize the current point
        if (!_isDragging)
        {
            // Click without drag = corner point
            _currentPoint.Type = ControlPointType.Corner;
            _currentPoint.InHandle = null;
            _currentPoint.OutHandle = null;
        }

        _points.Add(_currentPoint);
        _currentPoint = null;
        _isDragging = false;

        PathChanged?.Invoke(this, EventArgs.Empty);
        base.OnMouseUp(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnKeyDown(string key, KeyModifiers modifiers)
    {
        switch (key)
        {
            case "Escape":
                if (_isDrawing)
                {
                    ClearPath();
                    return true;
                }
                break;

            case "Enter":
                if (_isDrawing && _points.Count >= 2)
                {
                    FinishPath(false);
                    return true;
                }
                break;

            case "Back":
            case "Backspace":
                if (_points.Count > 0)
                {
                    _points.RemoveAt(_points.Count - 1);
                    PathChanged?.Invoke(this, EventArgs.Empty);
                    return true;
                }
                break;
        }

        return base.OnKeyDown(key, modifiers);
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (!_isDrawing && _points.Count == 0) return;

        const uint pathColor = 0xFFCDD6F4;
        const uint handleColor = 0xFF89B4FA;
        const uint pointColor = 0xFFFFFFFF;
        const uint previewColor = 0x80CDD6F4;
        const uint closeIndicatorColor = 0xFFA6E3A1;

        // Draw the path segments
        for (var i = 0; i < _points.Count - 1; i++)
        {
            DrawSegment(context, _points[i], _points[i + 1], pathColor, 2f);
        }

        // Draw preview segment from last point to current position
        if (_points.Count > 0 && _previewPoint.HasValue)
        {
            var lastPoint = _points[^1];
            
            if (_currentPoint != null && _isDragging)
            {
                // Draw segment to current point being dragged
                DrawSegment(context, lastPoint, _currentPoint, previewColor, 1.5f);
            }
            else
            {
                // Draw rubber band line to mouse position
                var (px, py) = _previewPoint.Value;
                if (lastPoint.OutHandleAbsolute.HasValue)
                {
                    var (hx, hy) = lastPoint.OutHandleAbsolute.Value;
                    var pathData = $"M {lastPoint.Position.X:0.###} {lastPoint.Position.Y:0.###} C {hx:0.###} {hy:0.###}, {px:0.###} {py:0.###}, {px:0.###} {py:0.###}";
                    context.DrawPath(pathData, previewColor, 1.5f);
                }
                else
                {
                    context.DrawLine(
                        lastPoint.Position.X, lastPoint.Position.Y,
                        px, py,
                        previewColor, 1.5f);
                }
            }
        }

        // Draw control handles for all points
        foreach (var point in _points)
        {
            DrawHandles(context, point, handleColor);
        }

        // Draw current point being created
        if (_currentPoint != null)
        {
            DrawHandles(context, _currentPoint, handleColor);
        }

        // Draw anchor points
        foreach (var point in _points)
        {
            context.DrawEllipse(point.Position.X, point.Position.Y, 4, 4, pointColor, 1f, true);
            context.DrawEllipse(point.Position.X, point.Position.Y, 4, 4, pathColor, 1f, false);
        }

        if (_currentPoint != null)
        {
            context.DrawEllipse(_currentPoint.Position.X, _currentPoint.Position.Y, 4, 4, pointColor, 1f, true);
            context.DrawEllipse(_currentPoint.Position.X, _currentPoint.Position.Y, 4, 4, pathColor, 1f, false);
        }

        // Draw close indicator if near first point
        if (_points.Count >= 2 && _previewPoint.HasValue && IsNearFirstPoint(_previewPoint.Value.X, _previewPoint.Value.Y))
        {
            var firstPoint = _points[0];
            context.DrawEllipse(firstPoint.Position.X, firstPoint.Position.Y, 8, 8, closeIndicatorColor, 2f, false);
        }

        // Draw info text
        if (_points.Count > 0 && _previewPoint.HasValue)
        {
            var (px, py) = _previewPoint.Value;
            var lastPoint = _points[^1];
            var dx = px - lastPoint.Position.X;
            var dy = py - lastPoint.Position.Y;
            var length = Math.Sqrt(dx * dx + dy * dy);
            var angle = Math.Atan2(dy, dx) * (180 / Math.PI);

            var infoText = $"{length:0.#}px  {angle:0.#}°";
            context.DrawText(infoText, px + 15, py - 15, 0xFFFFFFFF, 11f);
        }
    }

    private void DrawSegment(IToolRenderContext context, ControlPoint from, ControlPoint to, uint color, float width)
    {
        var (x1, y1) = from.Position;
        var (x2, y2) = to.Position;

        var hasOutHandle = from.OutHandleAbsolute.HasValue;
        var hasInHandle = to.InHandleAbsolute.HasValue;

        if (hasOutHandle || hasInHandle)
        {
            var (cx1, cy1) = from.OutHandleAbsolute ?? from.Position;
            var (cx2, cy2) = to.InHandleAbsolute ?? to.Position;
            var pathData = $"M {x1:0.###} {y1:0.###} C {cx1:0.###} {cy1:0.###}, {cx2:0.###} {cy2:0.###}, {x2:0.###} {y2:0.###}";
            context.DrawPath(pathData, color, width);
        }
        else
        {
            context.DrawLine(x1, y1, x2, y2, color, width);
        }
    }

    private void DrawHandles(IToolRenderContext context, ControlPoint point, uint color)
    {
        var (px, py) = point.Position;

        if (point.InHandleAbsolute.HasValue)
        {
            var (hx, hy) = point.InHandleAbsolute.Value;
            context.DrawLine(px, py, hx, hy, color, 1f);
            context.DrawEllipse(hx, hy, 3, 3, color, 1f, true);
        }

        if (point.OutHandleAbsolute.HasValue)
        {
            var (hx, hy) = point.OutHandleAbsolute.Value;
            context.DrawLine(px, py, hx, hy, color, 1f);
            context.DrawEllipse(hx, hy, 3, 3, color, 1f, true);
        }
    }

    private bool IsNearFirstPoint(double x, double y)
    {
        if (_points.Count == 0) return false;
        var first = _points[0];
        var dx = first.Position.X - x;
        var dy = first.Position.Y - y;
        return dx * dx + dy * dy <= SnapRadius * SnapRadius;
    }

    private void FinishPath(bool closePath)
    {
        if (Document is null || _points.Count < 2) return;

        var path = CreatePathFromPoints(closePath);
        if (path != null)
        {
            var command = new AddElementCommand(Document, path);
            History?.ExecuteCommand(command);
        }

        ClearPath();
    }

    private SvgPath? CreatePathFromPoints(bool closePath)
    {
        if (_points.Count < 2) return null;

        var pathData = new System.Text.StringBuilder();

        // Move to first point
        var first = _points[0];
        pathData.Append($"M {first.Position.X:0.###} {first.Position.Y:0.###}");

        // Draw segments
        for (var i = 1; i < _points.Count; i++)
        {
            var prev = _points[i - 1];
            var curr = _points[i];

            var hasOutHandle = prev.OutHandleAbsolute.HasValue;
            var hasInHandle = curr.InHandleAbsolute.HasValue;

            if (hasOutHandle || hasInHandle)
            {
                // Cubic bezier
                var (cx1, cy1) = prev.OutHandleAbsolute ?? prev.Position;
                var (cx2, cy2) = curr.InHandleAbsolute ?? curr.Position;
                pathData.Append($" C {cx1:0.###} {cy1:0.###}, {cx2:0.###} {cy2:0.###}, {curr.Position.X:0.###} {curr.Position.Y:0.###}");
            }
            else
            {
                // Line
                pathData.Append($" L {curr.Position.X:0.###} {curr.Position.Y:0.###}");
            }
        }

        // Close path if requested
        if (closePath)
        {
            var last = _points[^1];
            var hasLastOutHandle = last.OutHandleAbsolute.HasValue;
            var hasFirstInHandle = first.InHandleAbsolute.HasValue;

            if (hasLastOutHandle || hasFirstInHandle)
            {
                var (cx1, cy1) = last.OutHandleAbsolute ?? last.Position;
                var (cx2, cy2) = first.InHandleAbsolute ?? first.Position;
                pathData.Append($" C {cx1:0.###} {cy1:0.###}, {cx2:0.###} {cy2:0.###}, {first.Position.X:0.###} {first.Position.Y:0.###}");
            }

            pathData.Append(" Z");
        }

        return new SvgPath
        {
            PathData = pathData.ToString(),
            Stroke = new Stroke { Fill = new SolidFill { Color = DefaultStrokeColor }, Width = DefaultStrokeWidth },
            Fill = closePath && FillClosedPaths ? new SolidFill { Color = DefaultFillColor } : null,
            Name = GenerateName()
        };
    }

    private void ClearPath()
    {
        _points.Clear();
        _currentPoint = null;
        _isDragging = false;
        _isDrawing = false;
        _previewPoint = null;
        PathChanged?.Invoke(this, EventArgs.Empty);
    }

    private string GenerateName()
    {
        return $"Path {DateTime.Now:HHmmss}";
    }

    /// <summary>
    /// Gets the current number of points in the path being drawn.
    /// </summary>
    public int PointCount => _points.Count;

    /// <summary>
    /// Gets whether a path is currently being drawn.
    /// </summary>
    public bool IsDrawingPath => _isDrawing;
}
