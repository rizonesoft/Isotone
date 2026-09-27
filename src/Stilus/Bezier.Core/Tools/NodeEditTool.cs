namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;

/// <summary>
/// What part of a node is being interacted with.
/// </summary>
public enum NodeHitType
{
    None,
    Anchor,
    InHandle,
    OutHandle
}

/// <summary>
/// Represents a selected node reference.
/// </summary>
public record NodeSelection(SvgPath Path, int NodeIndex, ControlPoint Node);

/// <summary>
/// Tool for editing nodes on bezier paths.
/// </summary>
public class NodeEditTool : ToolBase
{
    private readonly List<NodeSelection> _selectedNodes = [];
    private readonly List<ControlPoint> _pathNodes = [];
    private SvgPath? _activePath;
    private NodeHitType _dragHitType = NodeHitType.None;
    private int _dragNodeIndex = -1;
    private (double X, double Y) _dragStartNodePos;
    private (double X, double Y)? _dragStartHandlePos;
    private bool _isMarqueeSelecting;
    private (double X, double Y) _marqueeStart;
    private (double X, double Y) _marqueeEnd;

    /// <inheritdoc/>
    public override string Name => "Node Edit";

    /// <inheritdoc/>
    public override string Icon => "Edit";

    /// <inheritdoc/>
    public override ToolCursor Cursor => ToolCursor.Arrow;

    /// <inheritdoc/>
    public override string? Shortcut => "A";

    /// <summary>
    /// Gets the currently selected nodes.
    /// </summary>
    public IReadOnlyList<NodeSelection> SelectedNodes => _selectedNodes;

    /// <summary>
    /// Gets the active path being edited.
    /// </summary>
    public SvgPath? ActivePath => _activePath;

    /// <summary>
    /// Event raised when node selection changes.
    /// </summary>
    public event EventHandler? SelectionChanged;

    /// <inheritdoc/>
    public override void OnActivate()
    {
        base.OnActivate();
        _selectedNodes.Clear();
        _dragHitType = NodeHitType.None;
        _dragNodeIndex = -1;
        _isMarqueeSelecting = false;
    }

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        ClearSelection();
    }

    /// <summary>
    /// Sets the active path for node editing.
    /// </summary>
    public void SetActivePath(SvgPath? path)
    {
        if (_activePath != path)
        {
            _selectedNodes.Clear();
            _activePath = path;
            
            if (path != null)
            {
                ParsePathNodes(path);
            }
            else
            {
                _pathNodes.Clear();
            }
            
            SelectionChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (_activePath is null || Document is null) return false;

        // Check if clicking on a node or handle
        var (hitType, nodeIndex) = HitTestNodes(point.X, point.Y);

        if (hitType != NodeHitType.None && nodeIndex >= 0)
        {
            _dragHitType = hitType;
            _dragNodeIndex = nodeIndex;
            var node = _pathNodes[nodeIndex];
            _dragStartNodePos = node.Position;

            if (hitType == NodeHitType.InHandle)
            {
                _dragStartHandlePos = node.InHandle;
            }
            else if (hitType == NodeHitType.OutHandle)
            {
                _dragStartHandlePos = node.OutHandle;
            }

            // Handle selection
            if (hitType == NodeHitType.Anchor)
            {
                var existingSelection = _selectedNodes.FindIndex(s => s.NodeIndex == nodeIndex);

                if (modifiers.HasFlag(KeyModifiers.Shift))
                {
                    // Shift+Click: Add to selection
                    if (existingSelection < 0)
                    {
                        _selectedNodes.Add(new NodeSelection(_activePath, nodeIndex, node));
                    }
                }
                else if (modifiers.HasFlag(KeyModifiers.Control))
                {
                    // Ctrl+Click: Toggle selection
                    if (existingSelection >= 0)
                    {
                        _selectedNodes.RemoveAt(existingSelection);
                    }
                    else
                    {
                        _selectedNodes.Add(new NodeSelection(_activePath, nodeIndex, node));
                    }
                }
                else
                {
                    // Click: Select only this node
                    if (existingSelection < 0)
                    {
                        _selectedNodes.Clear();
                        _selectedNodes.Add(new NodeSelection(_activePath, nodeIndex, node));
                    }
                }

                SelectionChanged?.Invoke(this, EventArgs.Empty);
            }

            return true;
        }

        // Start marquee selection if clicking on empty space
        if (!modifiers.HasFlag(KeyModifiers.Shift) && !modifiers.HasFlag(KeyModifiers.Control))
        {
            _selectedNodes.Clear();
            SelectionChanged?.Invoke(this, EventArgs.Empty);
        }

        _isMarqueeSelecting = true;
        _marqueeStart = (point.X, point.Y);
        _marqueeEnd = (point.X, point.Y);

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseMove(point, modifiers);

        if (_isMarqueeSelecting)
        {
            _marqueeEnd = (point.X, point.Y);
            return true;
        }

        if (_dragHitType == NodeHitType.None || _dragNodeIndex < 0) return false;

        var node = _pathNodes[_dragNodeIndex];
        var dx = point.X - DragStartPoint.X;
        var dy = point.Y - DragStartPoint.Y;

        switch (_dragHitType)
        {
            case NodeHitType.Anchor:
                // Move the anchor point
                node.Position = (_dragStartNodePos.X + dx, _dragStartNodePos.Y + dy);
                break;

            case NodeHitType.InHandle:
                // Move the incoming handle (relative to anchor)
                if (_dragStartHandlePos.HasValue)
                {
                    var newHandleX = point.X - node.Position.X;
                    var newHandleY = point.Y - node.Position.Y;
                    node.SetInHandle(newHandleX, newHandleY);
                }
                break;

            case NodeHitType.OutHandle:
                // Move the outgoing handle (relative to anchor)
                if (_dragStartHandlePos.HasValue)
                {
                    var newHandleX = point.X - node.Position.X;
                    var newHandleY = point.Y - node.Position.Y;
                    node.SetOutHandle(newHandleX, newHandleY);
                }
                break;
        }

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (_isMarqueeSelecting)
        {
            _marqueeEnd = (point.X, point.Y);
            SelectNodesInMarquee(modifiers);
            _isMarqueeSelecting = false;
            base.OnMouseUp(point, modifiers);
            return true;
        }

        if (_dragHitType != NodeHitType.None && _dragNodeIndex >= 0 && _activePath != null)
        {
            // Rebuild path from modified nodes
            RebuildPathFromNodes();
        }

        _dragHitType = NodeHitType.None;
        _dragNodeIndex = -1;
        _dragStartHandlePos = null;

        base.OnMouseUp(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnKeyDown(string key, KeyModifiers modifiers)
    {
        switch (key)
        {
            case "Delete":
            case "Back":
            case "Backspace":
                if (_selectedNodes.Count > 0)
                {
                    DeleteSelectedNodes();
                    return true;
                }
                break;

            case "A":
                if (modifiers.HasFlag(KeyModifiers.Control))
                {
                    SelectAllNodes();
                    return true;
                }
                break;

            case "D1":
            case "1":
                // Convert to corner
                ConvertSelectedNodes(ControlPointType.Corner);
                return true;

            case "D2":
            case "2":
                // Convert to smooth
                ConvertSelectedNodes(ControlPointType.Smooth);
                return true;

            case "D3":
            case "3":
                // Convert to symmetric
                ConvertSelectedNodes(ControlPointType.Symmetric);
                return true;
        }

        return base.OnKeyDown(key, modifiers);
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (_activePath is null || _pathNodes.Count == 0) return;

        const uint pathColor = 0xFFCDD6F4;
        const uint handleColor = 0xFF89B4FA;
        const uint selectedColor = 0xFFF9E2AF;
        const uint anchorColor = 0xFFFFFFFF;
        const uint marqueeColor = 0x4089B4FA;

        // Draw path segments
        for (var i = 0; i < _pathNodes.Count - 1; i++)
        {
            DrawSegment(context, _pathNodes[i], _pathNodes[i + 1], pathColor, 1.5f);
        }

        // Draw handles and anchor points
        for (var i = 0; i < _pathNodes.Count; i++)
        {
            var node = _pathNodes[i];
            var isSelected = _selectedNodes.Any(s => s.NodeIndex == i);

            // Draw handles
            DrawHandles(context, node, handleColor);

            // Draw anchor point
            var color = isSelected ? selectedColor : anchorColor;
            context.DrawRect(node.Position.X - 4, node.Position.Y - 4, 8, 8, color, 1f, true);
            context.DrawRect(node.Position.X - 4, node.Position.Y - 4, 8, 8, pathColor, 1f, false);
        }

        // Draw marquee selection box
        if (_isMarqueeSelecting)
        {
            var x = Math.Min(_marqueeStart.X, _marqueeEnd.X);
            var y = Math.Min(_marqueeStart.Y, _marqueeEnd.Y);
            var w = Math.Abs(_marqueeEnd.X - _marqueeStart.X);
            var h = Math.Abs(_marqueeEnd.Y - _marqueeStart.Y);

            context.DrawRect(x, y, w, h, marqueeColor, 1f, true);
            context.DrawRect(x, y, w, h, handleColor, 1f, false);
        }
    }

    private void DrawSegment(IToolRenderContext context, ControlPoint from, ControlPoint to, uint color, float width)
    {
        var hasOutHandle = from.OutHandleAbsolute.HasValue;
        var hasInHandle = to.InHandleAbsolute.HasValue;

        if (hasOutHandle || hasInHandle)
        {
            var (x1, y1) = from.Position;
            var (cx1, cy1) = from.OutHandleAbsolute ?? from.Position;
            var (cx2, cy2) = to.InHandleAbsolute ?? to.Position;
            var (x2, y2) = to.Position;
            var pathData = $"M {x1:0.###} {y1:0.###} C {cx1:0.###} {cy1:0.###}, {cx2:0.###} {cy2:0.###}, {x2:0.###} {y2:0.###}";
            context.DrawPath(pathData, color, width);
        }
        else
        {
            context.DrawLine(from.Position.X, from.Position.Y, to.Position.X, to.Position.Y, color, width);
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

    private (NodeHitType Type, int Index) HitTestNodes(double x, double y)
    {
        // Check handles first (smaller targets)
        for (var i = 0; i < _pathNodes.Count; i++)
        {
            var node = _pathNodes[i];

            if (node.HitTestInHandle(x, y))
                return (NodeHitType.InHandle, i);

            if (node.HitTestOutHandle(x, y))
                return (NodeHitType.OutHandle, i);
        }

        // Then check anchor points
        for (var i = 0; i < _pathNodes.Count; i++)
        {
            if (_pathNodes[i].HitTestAnchor(x, y))
                return (NodeHitType.Anchor, i);
        }

        return (NodeHitType.None, -1);
    }

    private void SelectNodesInMarquee(KeyModifiers modifiers)
    {
        if (_activePath is null) return;

        var minX = Math.Min(_marqueeStart.X, _marqueeEnd.X);
        var minY = Math.Min(_marqueeStart.Y, _marqueeEnd.Y);
        var maxX = Math.Max(_marqueeStart.X, _marqueeEnd.X);
        var maxY = Math.Max(_marqueeStart.Y, _marqueeEnd.Y);

        var nodesInRect = new List<int>();
        for (var i = 0; i < _pathNodes.Count; i++)
        {
            var pos = _pathNodes[i].Position;
            if (pos.X >= minX && pos.X <= maxX && pos.Y >= minY && pos.Y <= maxY)
            {
                nodesInRect.Add(i);
            }
        }

        if (!modifiers.HasFlag(KeyModifiers.Shift))
        {
            _selectedNodes.Clear();
        }

        foreach (var idx in nodesInRect)
        {
            if (!_selectedNodes.Any(s => s.NodeIndex == idx))
            {
                _selectedNodes.Add(new NodeSelection(_activePath, idx, _pathNodes[idx]));
            }
        }

        SelectionChanged?.Invoke(this, EventArgs.Empty);
    }

    private void SelectAllNodes()
    {
        if (_activePath is null) return;

        _selectedNodes.Clear();
        for (var i = 0; i < _pathNodes.Count; i++)
        {
            _selectedNodes.Add(new NodeSelection(_activePath, i, _pathNodes[i]));
        }

        SelectionChanged?.Invoke(this, EventArgs.Empty);
    }

    private void ClearSelection()
    {
        _selectedNodes.Clear();
        _activePath = null;
        _pathNodes.Clear();
        _dragHitType = NodeHitType.None;
        _dragNodeIndex = -1;
        _isMarqueeSelecting = false;
        SelectionChanged?.Invoke(this, EventArgs.Empty);
    }

    private void DeleteSelectedNodes()
    {
        if (_activePath is null || _selectedNodes.Count == 0) return;

        // Remove nodes in reverse order to preserve indices
        var indicesToRemove = _selectedNodes.Select(s => s.NodeIndex).OrderByDescending(i => i).ToList();
        
        foreach (var idx in indicesToRemove)
        {
            if (idx >= 0 && idx < _pathNodes.Count)
            {
                _pathNodes.RemoveAt(idx);
            }
        }

        _selectedNodes.Clear();
        RebuildPathFromNodes();
        SelectionChanged?.Invoke(this, EventArgs.Empty);
    }

    private void ConvertSelectedNodes(ControlPointType type)
    {
        foreach (var selection in _selectedNodes)
        {
            if (selection.NodeIndex >= 0 && selection.NodeIndex < _pathNodes.Count)
            {
                var node = _pathNodes[selection.NodeIndex];
                switch (type)
                {
                    case ControlPointType.Corner:
                        node.ConvertToCorner();
                        break;
                    case ControlPointType.Smooth:
                        node.ConvertToSmooth();
                        break;
                    case ControlPointType.Symmetric:
                        node.ConvertToSymmetric();
                        break;
                }
            }
        }

        RebuildPathFromNodes();
    }

    private void ParsePathNodes(SvgPath path)
    {
        _pathNodes.Clear();
        
        // Simple path parser for M, L, C commands
        var pathData = path.PathData;
        if (string.IsNullOrEmpty(pathData)) return;

        var tokens = TokenizePath(pathData);
        var i = 0;
        double currentX = 0, currentY = 0;
        ControlPoint? lastPoint = null;

        while (i < tokens.Count)
        {
            var cmd = tokens[i];
            i++;

            switch (cmd.ToUpperInvariant())
            {
                case "M": // Move to
                    currentX = double.Parse(tokens[i++]);
                    currentY = double.Parse(tokens[i++]);
                    lastPoint = ControlPoint.CreateCorner(currentX, currentY);
                    _pathNodes.Add(lastPoint);
                    break;

                case "L": // Line to
                    currentX = double.Parse(tokens[i++]);
                    currentY = double.Parse(tokens[i++]);
                    lastPoint = ControlPoint.CreateCorner(currentX, currentY);
                    _pathNodes.Add(lastPoint);
                    break;

                case "C": // Cubic bezier
                    var cx1 = double.Parse(tokens[i++]);
                    var cy1 = double.Parse(tokens[i++]);
                    SkipComma(tokens, ref i);
                    var cx2 = double.Parse(tokens[i++]);
                    var cy2 = double.Parse(tokens[i++]);
                    SkipComma(tokens, ref i);
                    var x2 = double.Parse(tokens[i++]);
                    var y2 = double.Parse(tokens[i++]);

                    // Set outgoing handle on last point
                    if (lastPoint != null)
                    {
                        lastPoint.OutHandle = (cx1 - lastPoint.Position.X, cy1 - lastPoint.Position.Y);
                        if (lastPoint.InHandle.HasValue || lastPoint.OutHandle.HasValue)
                        {
                            lastPoint.Type = ControlPointType.Smooth;
                        }
                    }

                    // Create new point with incoming handle
                    var newPoint = ControlPoint.CreateCorner(x2, y2);
                    newPoint.InHandle = (cx2 - x2, cy2 - y2);
                    newPoint.Type = ControlPointType.Smooth;
                    _pathNodes.Add(newPoint);

                    currentX = x2;
                    currentY = y2;
                    lastPoint = newPoint;
                    break;

                case "Z": // Close path
                    // Path is closed, handled separately
                    break;
            }
        }
    }

    private static List<string> TokenizePath(string pathData)
    {
        var tokens = new List<string>();
        var current = new System.Text.StringBuilder();

        foreach (var c in pathData)
        {
            if (char.IsLetter(c))
            {
                if (current.Length > 0)
                {
                    tokens.Add(current.ToString().Trim());
                    current.Clear();
                }
                tokens.Add(c.ToString());
            }
            else if (c == ',' || char.IsWhiteSpace(c))
            {
                if (current.Length > 0)
                {
                    tokens.Add(current.ToString().Trim());
                    current.Clear();
                }
                if (c == ',')
                {
                    tokens.Add(",");
                }
            }
            else if (c == '-' && current.Length > 0)
            {
                tokens.Add(current.ToString().Trim());
                current.Clear();
                current.Append(c);
            }
            else
            {
                current.Append(c);
            }
        }

        if (current.Length > 0)
        {
            tokens.Add(current.ToString().Trim());
        }

        return tokens.Where(t => !string.IsNullOrWhiteSpace(t)).ToList();
    }

    private static void SkipComma(List<string> tokens, ref int i)
    {
        if (i < tokens.Count && tokens[i] == ",") i++;
    }

    private void RebuildPathFromNodes()
    {
        if (_activePath is null || _pathNodes.Count < 2) return;

        var pathData = new System.Text.StringBuilder();

        // Move to first point
        var first = _pathNodes[0];
        pathData.Append($"M {first.Position.X:0.###} {first.Position.Y:0.###}");

        // Draw segments
        for (var i = 1; i < _pathNodes.Count; i++)
        {
            var prev = _pathNodes[i - 1];
            var curr = _pathNodes[i];

            var hasOutHandle = prev.OutHandleAbsolute.HasValue;
            var hasInHandle = curr.InHandleAbsolute.HasValue;

            if (hasOutHandle || hasInHandle)
            {
                var (cx1, cy1) = prev.OutHandleAbsolute ?? prev.Position;
                var (cx2, cy2) = curr.InHandleAbsolute ?? curr.Position;
                pathData.Append($" C {cx1:0.###} {cy1:0.###}, {cx2:0.###} {cy2:0.###}, {curr.Position.X:0.###} {curr.Position.Y:0.###}");
            }
            else
            {
                pathData.Append($" L {curr.Position.X:0.###} {curr.Position.Y:0.###}");
            }
        }

        // Check if path was closed (simplified check)
        if (_activePath.PathData?.Contains("Z", StringComparison.OrdinalIgnoreCase) == true)
        {
            pathData.Append(" Z");
        }

        _activePath.PathData = pathData.ToString();
    }

    /// <summary>
    /// Adds a new node at the specified position on the path.
    /// </summary>
    public void AddNodeAtPosition(double x, double y, int afterIndex)
    {
        if (afterIndex < 0 || afterIndex >= _pathNodes.Count - 1) return;

        var newNode = ControlPoint.CreateCorner(x, y);
        _pathNodes.Insert(afterIndex + 1, newNode);
        RebuildPathFromNodes();
    }

    /// <summary>
    /// Gets the number of nodes in the active path.
    /// </summary>
    public int NodeCount => _pathNodes.Count;
}
