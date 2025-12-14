namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Services;

/// <summary>
/// Selection mode for the select tool.
/// </summary>
public enum SelectMode
{
    None,
    Selecting,
    Moving,
    MarqueeSelect,
    Resizing,
    Rotating
}

/// <summary>
/// Resize handle positions.
/// </summary>
public enum ResizeHandle
{
    None,
    TopLeft,
    TopCenter,
    TopRight,
    MiddleLeft,
    MiddleRight,
    BottomLeft,
    BottomCenter,
    BottomRight,
    Rotate
}

/// <summary>
/// Tool for selecting and manipulating elements.
/// </summary>
public class SelectTool : ToolBase
{
    private SelectMode _mode = SelectMode.None;
    private ResizeHandle _activeHandle = ResizeHandle.None;
    private ResizeHandle _hoveredHandle = ResizeHandle.None;
    private readonly List<VectorElement> _selectedElements = [];
    private readonly List<VectorElement> _previewSelection = [];
    private MoveCommand? _moveCommand;
    
    // Resize/rotate state
    private (double X, double Y, double Width, double Height) _originalBounds;
    private readonly Dictionary<VectorElement, (double X, double Y, double Width, double Height)> _originalElementBounds = [];
    private double _rotationStartAngle;
    private double _currentRotationAngle;
    
    // Handle size (in screen pixels)
    private const double HandleSize = 8;
    private const double HandleHitRadius = 6;
    private const double RotateHandleOffset = 24;

    /// <inheritdoc/>
    public override string Name => "Select";

    /// <inheritdoc/>
    public override string Icon => "CursorClick";

    /// <inheritdoc/>
    public override ToolCursor Cursor => GetCurrentCursor();

    /// <inheritdoc/>
    public override string? Shortcut => "V";

    /// <summary>
    /// Gets the currently selected elements.
    /// </summary>
    public IReadOnlyList<VectorElement> SelectedElements => _selectedElements;

    /// <summary>
    /// Event raised when selection changes.
    /// </summary>
    public event EventHandler<IReadOnlyList<VectorElement>>? SelectionChanged;

    private ToolCursor GetCurrentCursor()
    {
        if (_mode == SelectMode.Moving) return ToolCursor.Move;
        if (_mode == SelectMode.Rotating) return ToolCursor.Rotate;
        
        return _hoveredHandle switch
        {
            ResizeHandle.TopLeft or ResizeHandle.BottomRight => ToolCursor.SizeNWSE,
            ResizeHandle.TopRight or ResizeHandle.BottomLeft => ToolCursor.SizeNESW,
            ResizeHandle.TopCenter or ResizeHandle.BottomCenter => ToolCursor.SizeNS,
            ResizeHandle.MiddleLeft or ResizeHandle.MiddleRight => ToolCursor.SizeWE,
            ResizeHandle.Rotate => ToolCursor.Rotate,
            _ => _mode == SelectMode.Resizing ? GetResizeCursor(_activeHandle) : ToolCursor.Arrow
        };
    }

    private static ToolCursor GetResizeCursor(ResizeHandle handle) => handle switch
    {
        ResizeHandle.TopLeft or ResizeHandle.BottomRight => ToolCursor.SizeNWSE,
        ResizeHandle.TopRight or ResizeHandle.BottomLeft => ToolCursor.SizeNESW,
        ResizeHandle.TopCenter or ResizeHandle.BottomCenter => ToolCursor.SizeNS,
        ResizeHandle.MiddleLeft or ResizeHandle.MiddleRight => ToolCursor.SizeWE,
        _ => ToolCursor.Arrow
    };

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        _mode = SelectMode.None;
        _activeHandle = ResizeHandle.None;
        _hoveredHandle = ResizeHandle.None;
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

        // Check if clicking on a resize/rotate handle first
        if (_selectedElements.Count > 0)
        {
            var bounds = GetAggregateBounds();
            var handle = HitTestHandle(point.X, point.Y, bounds);
            
            if (handle != ResizeHandle.None)
            {
                _activeHandle = handle;
                _originalBounds = bounds;
                
                // Store original bounds for each element
                _originalElementBounds.Clear();
                foreach (var elem in _selectedElements)
                {
                    var b = elem.GetBoundingBox();
                    _originalElementBounds[elem] = (b.X, b.Y, b.Width, b.Height);
                }
                
                if (handle == ResizeHandle.Rotate)
                {
                    _mode = SelectMode.Rotating;
                    var centerX = bounds.X + bounds.Width / 2;
                    var centerY = bounds.Y + bounds.Height / 2;
                    _rotationStartAngle = Math.Atan2(point.Y - centerY, point.X - centerX);
                    _currentRotationAngle = 0;
                }
                else
                {
                    _mode = SelectMode.Resizing;
                }
                
                return true;
            }
        }

        // Try to hit test an element
        var hitElement = HitTest(point);

        if (hitElement is not null)
        {
            // Handle selection based on modifiers
            if (modifiers.HasFlag(KeyModifiers.Shift))
            {
                // Add to selection
                if (!_selectedElements.Contains(hitElement))
                {
                    _selectedElements.Add(hitElement);
                    OnSelectionChanged();
                }
            }
            else if (modifiers.HasFlag(KeyModifiers.Control))
            {
                // Toggle selection
                if (_selectedElements.Contains(hitElement))
                {
                    _selectedElements.Remove(hitElement);
                }
                else
                {
                    _selectedElements.Add(hitElement);
                }
                OnSelectionChanged();
            }
            else
            {
                // Single select (unless already selected for moving)
                if (!_selectedElements.Contains(hitElement))
                {
                    _selectedElements.Clear();
                    _selectedElements.Add(hitElement);
                    OnSelectionChanged();
                }
            }

            // Start moving if we have selection
            if (_selectedElements.Count > 0)
            {
                _mode = SelectMode.Moving;
                
                // Store original bounds for each element
                _originalElementBounds.Clear();
                foreach (var elem in _selectedElements)
                {
                    var b = elem.GetBoundingBox();
                    _originalElementBounds[elem] = (b.X, b.Y, b.Width, b.Height);
                }
            }
        }
        else
        {
            // Clicked on empty space
            if (!modifiers.HasFlag(KeyModifiers.Shift) && !modifiers.HasFlag(KeyModifiers.Control))
            {
                // Clear selection and start marquee
                _selectedElements.Clear();
                OnSelectionChanged();
            }
            _mode = SelectMode.MarqueeSelect;
            _previewSelection.Clear();
        }

        return true;
    }

    /// <inheritdoc/>
    public override bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseMove(point, modifiers);

        // Update hovered handle when not dragging
        if (!IsDragging && _selectedElements.Count > 0)
        {
            var bounds = GetAggregateBounds();
            _hoveredHandle = HitTestHandle(point.X, point.Y, bounds);
            return true;
        }

        if (!IsDragging) return false;

        switch (_mode)
        {
            case SelectMode.Moving:
                // Preview move (we'll commit on mouse up)
                return true;

            case SelectMode.MarqueeSelect:
                // Update preview selection
                UpdateMarqueeSelection();
                return true;

            case SelectMode.Resizing:
                // Apply resize preview
                ApplyResize(point, modifiers);
                return true;

            case SelectMode.Rotating:
                // Apply rotation preview
                ApplyRotation(point, modifiers);
                return true;
        }

        return false;
    }

    /// <inheritdoc/>
    public override bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        if (!IsDragging)
        {
            base.OnMouseUp(point, modifiers);
            return false;
        }

        var (deltaX, deltaY) = GetDragDelta();

        switch (_mode)
        {
            case SelectMode.Moving:
                // Commit move if there was actual movement
                if (Math.Abs(deltaX) > 0.5 || Math.Abs(deltaY) > 0.5)
                {
                    _moveCommand = new MoveCommand(_selectedElements, deltaX, deltaY);
                    History?.ExecuteCommand(_moveCommand);
                }
                break;

            case SelectMode.MarqueeSelect:
                // Finalize marquee selection
                if (modifiers.HasFlag(KeyModifiers.Shift))
                {
                    // Add to existing selection
                    foreach (var element in _previewSelection)
                    {
                        if (!_selectedElements.Contains(element))
                        {
                            _selectedElements.Add(element);
                        }
                    }
                }
                else
                {
                    _selectedElements.Clear();
                    _selectedElements.AddRange(_previewSelection);
                }
                _previewSelection.Clear();
                OnSelectionChanged();
                break;

            case SelectMode.Resizing:
                // Commit resize - transforms are already applied during drag
                // TODO: Add ResizeCommand for undo support
                DebugLogger.Instance.Log("SelectTool", "Resize completed");
                break;

            case SelectMode.Rotating:
                // Commit rotation - transforms are already applied during drag
                // TODO: Add RotateCommand for undo support
                DebugLogger.Instance.Log("SelectTool", $"Rotation completed: {_currentRotationAngle * 180 / Math.PI:F1}°");
                break;
        }

        _mode = SelectMode.None;
        _activeHandle = ResizeHandle.None;
        _originalElementBounds.Clear();
        base.OnMouseUp(point, modifiers);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnKeyDown(string key, KeyModifiers modifiers)
    {
        if (key == "Delete" || key == "Back")
        {
            DeleteSelected();
            return true;
        }

        if (key == "Escape")
        {
            ClearSelection();
            return true;
        }

        if (modifiers.HasFlag(KeyModifiers.Control) && key == "A")
        {
            SelectAll();
            return true;
        }

        // Invert Selection: Ctrl+Shift+I
        if (modifiers.HasFlag(KeyModifiers.Control) && modifiers.HasFlag(KeyModifiers.Shift) && key == "I")
        {
            InvertSelection();
            return true;
        }

        return false;
    }

    private void ApplyResize(ToolPoint point, KeyModifiers modifiers)
    {
        if (_selectedElements.Count == 0) return;

        var proportional = modifiers.HasFlag(KeyModifiers.Shift);
        var fromCenter = modifiers.HasFlag(KeyModifiers.Alt);
        
        var orig = _originalBounds;
        var deltaX = point.X - DragStartPoint.X;
        var deltaY = point.Y - DragStartPoint.Y;

        // Calculate new bounds based on handle
        double newX = orig.X, newY = orig.Y, newW = orig.Width, newH = orig.Height;

        switch (_activeHandle)
        {
            case ResizeHandle.TopLeft:
                newX = orig.X + deltaX;
                newY = orig.Y + deltaY;
                newW = orig.Width - deltaX;
                newH = orig.Height - deltaY;
                break;
            case ResizeHandle.TopCenter:
                newY = orig.Y + deltaY;
                newH = orig.Height - deltaY;
                break;
            case ResizeHandle.TopRight:
                newY = orig.Y + deltaY;
                newW = orig.Width + deltaX;
                newH = orig.Height - deltaY;
                break;
            case ResizeHandle.MiddleLeft:
                newX = orig.X + deltaX;
                newW = orig.Width - deltaX;
                break;
            case ResizeHandle.MiddleRight:
                newW = orig.Width + deltaX;
                break;
            case ResizeHandle.BottomLeft:
                newX = orig.X + deltaX;
                newW = orig.Width - deltaX;
                newH = orig.Height + deltaY;
                break;
            case ResizeHandle.BottomCenter:
                newH = orig.Height + deltaY;
                break;
            case ResizeHandle.BottomRight:
                newW = orig.Width + deltaX;
                newH = orig.Height + deltaY;
                break;
        }

        // Ensure minimum size
        if (newW < 1) { newW = 1; newX = orig.X + orig.Width - 1; }
        if (newH < 1) { newH = 1; newY = orig.Y + orig.Height - 1; }

        // Proportional resize
        if (proportional && orig.Width > 0 && orig.Height > 0)
        {
            var ratio = orig.Width / orig.Height;
            if (_activeHandle is ResizeHandle.TopLeft or ResizeHandle.TopRight or 
                ResizeHandle.BottomLeft or ResizeHandle.BottomRight)
            {
                // Corner handles: maintain aspect ratio
                var newRatio = newW / newH;
                if (newRatio > ratio)
                {
                    newW = newH * ratio;
                }
                else
                {
                    newH = newW / ratio;
                }
            }
        }

        // Center resize
        if (fromCenter)
        {
            var centerX = orig.X + orig.Width / 2;
            var centerY = orig.Y + orig.Height / 2;
            newX = centerX - newW / 2;
            newY = centerY - newH / 2;
        }

        // Apply scale to each element
        var scaleX = newW / orig.Width;
        var scaleY = newH / orig.Height;

        foreach (var elem in _selectedElements)
        {
            if (!_originalElementBounds.TryGetValue(elem, out var elemOrig)) continue;

            // Calculate new element position and size
            var relX = (elemOrig.X - orig.X) / orig.Width;
            var relY = (elemOrig.Y - orig.Y) / orig.Height;
            var relW = elemOrig.Width / orig.Width;
            var relH = elemOrig.Height / orig.Height;

            var newElemX = newX + relX * newW;
            var newElemY = newY + relY * newH;
            var newElemW = relW * newW;
            var newElemH = relH * newH;

            // Apply via transform (scale and translate)
            var tx = newElemX - elemOrig.X;
            var ty = newElemY - elemOrig.Y;
            var sx = newElemW / elemOrig.Width;
            var sy = newElemH / elemOrig.Height;

            elem.Transform = new Transform
            {
                ScaleX = sx,
                SkewY = 0,
                SkewX = 0,
                ScaleY = sy,
                TranslateX = tx + elemOrig.X * (1 - sx),
                TranslateY = ty + elemOrig.Y * (1 - sy)
            };
        }
    }

    private void ApplyRotation(ToolPoint point, KeyModifiers modifiers)
    {
        if (_selectedElements.Count == 0) return;

        var bounds = _originalBounds;
        var centerX = bounds.X + bounds.Width / 2;
        var centerY = bounds.Y + bounds.Height / 2;

        var currentAngle = Math.Atan2(point.Y - centerY, point.X - centerX);
        var deltaAngle = currentAngle - _rotationStartAngle;

        // Snap to 15° increments when Shift is held
        if (modifiers.HasFlag(KeyModifiers.Shift))
        {
            var snapAngle = Math.PI / 12; // 15 degrees
            deltaAngle = Math.Round(deltaAngle / snapAngle) * snapAngle;
        }

        _currentRotationAngle = deltaAngle;

        // Apply rotation transform to each element
        foreach (var elem in _selectedElements)
        {
            if (!_originalElementBounds.TryGetValue(elem, out var elemOrig)) continue;

            // Calculate element's center relative to selection center
            var elemCenterX = elemOrig.X + elemOrig.Width / 2;
            var elemCenterY = elemOrig.Y + elemOrig.Height / 2;

            // Rotate element center around selection center
            var cos = Math.Cos(deltaAngle);
            var sin = Math.Sin(deltaAngle);
            var dx = elemCenterX - centerX;
            var dy = elemCenterY - centerY;
            var newCenterX = centerX + dx * cos - dy * sin;
            var newCenterY = centerY + dx * sin + dy * cos;

            // Apply rotation transform
            var translateX = newCenterX - elemCenterX;
            var translateY = newCenterY - elemCenterY;

            elem.Transform = new Transform
            {
                ScaleX = cos,
                SkewY = sin,
                SkewX = -sin,
                ScaleY = cos,
                TranslateX = translateX,
                TranslateY = translateY
            };
        }
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        // Colors in ARGB format (0xAARRGGBB)
        const uint selectionColor = 0xFF89B4FA; // Blue (Catppuccin)
        const uint selectionFillColor = 0x1A89B4FA; // Blue with 10% opacity
        const uint marqueeColor = 0x4089B4FA; // Semi-transparent blue
        const uint handleFillColor = 0xFFFFFFFF; // White
        const uint handleBorderColor = 0xFF89B4FA; // Blue border
        const uint rotateHandleColor = 0xFFA6E3A1; // Green for rotate

        // Calculate drag offset
        var offsetX = 0.0;
        var offsetY = 0.0;
        var isMoving = _mode == SelectMode.Moving && IsDragging;
        if (isMoving)
        {
            var delta = GetDragDelta();
            offsetX = delta.DeltaX;
            offsetY = delta.DeltaY;
        }

        // Draw element previews while dragging (semi-transparent at new position)
        if (isMoving && (Math.Abs(offsetX) > 1 || Math.Abs(offsetY) > 1))
        {
            foreach (var element in _selectedElements)
            {
                context.DrawElementPreview(element, offsetX, offsetY, 0.6);
            }
        }

        // Draw aggregate bounding box for all selected elements
        if (_selectedElements.Count > 0)
        {
            var bounds = GetAggregateBounds();
            
            var x = bounds.X + offsetX;
            var y = bounds.Y + offsetY;
            var w = bounds.Width;
            var h = bounds.Height;

            // Draw semi-transparent fill
            context.DrawRect(x, y, w, h, selectionFillColor, 1f, true);
            
            // Draw dashed border (2px, blue)
            context.DrawDashedRect(x, y, w, h, selectionColor, 2f, 6f, 4f);

            // Draw resize handles (8 points)
            DrawHandle(context, x, y, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.TopLeft);
            DrawHandle(context, x + w / 2, y, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.TopCenter);
            DrawHandle(context, x + w, y, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.TopRight);
            DrawHandle(context, x, y + h / 2, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.MiddleLeft);
            DrawHandle(context, x + w, y + h / 2, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.MiddleRight);
            DrawHandle(context, x, y + h, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.BottomLeft);
            DrawHandle(context, x + w / 2, y + h, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.BottomCenter);
            DrawHandle(context, x + w, y + h, handleFillColor, handleBorderColor, _hoveredHandle == ResizeHandle.BottomRight);

            // Draw rotate handle (above top center)
            var rotateY = y - RotateHandleOffset;
            context.DrawLine(x + w / 2, y, x + w / 2, rotateY + HandleSize / 2, selectionColor, 1f);
            DrawHandle(context, x + w / 2, rotateY, handleFillColor, rotateHandleColor, _hoveredHandle == ResizeHandle.Rotate);
            
            // Draw rotation angle tooltip when rotating
            if (_mode == SelectMode.Rotating)
            {
                var angleDeg = _currentRotationAngle * 180 / Math.PI;
                var tooltipText = $"{angleDeg:F1}°";
                context.DrawText(tooltipText, x + w / 2 + 20, rotateY, 0xFFFFFFFF, 12f);
            }
        }

        // Draw marquee selection box
        if (_mode == SelectMode.MarqueeSelect && IsDragging)
        {
            var (mx, my, mw, mh) = GetDragBounds();
            context.DrawRect(mx, my, mw, mh, marqueeColor, 1f, true);
            context.DrawDashedRect(mx, my, mw, mh, selectionColor, 1f, 6f, 4f);

            // Highlight elements in marquee
            foreach (var element in _previewSelection)
            {
                var b = element.GetBoundingBox();
                context.DrawRect(b.X, b.Y, b.Width, b.Height, selectionColor, 1f);
            }
        }
    }

    private static void DrawHandle(IToolRenderContext context, double x, double y, uint fillColor, uint borderColor, bool isHovered)
    {
        var size = isHovered ? HandleSize + 2 : HandleSize;
        var half = size / 2;
        context.DrawRect(x - half, y - half, size, size, fillColor, 1f, true);
        context.DrawRect(x - half, y - half, size, size, borderColor, 1f, false);
    }

    /// <summary>
    /// Gets the aggregate bounding box for all selected elements.
    /// </summary>
    private (double X, double Y, double Width, double Height) GetAggregateBounds()
    {
        if (_selectedElements.Count == 0)
            return (0, 0, 0, 0);

        double minX = double.MaxValue, minY = double.MaxValue;
        double maxX = double.MinValue, maxY = double.MinValue;

        foreach (var element in _selectedElements)
        {
            var b = element.GetBoundingBox();
            minX = Math.Min(minX, b.X);
            minY = Math.Min(minY, b.Y);
            maxX = Math.Max(maxX, b.X + b.Width);
            maxY = Math.Max(maxY, b.Y + b.Height);
        }

        return (minX, minY, maxX - minX, maxY - minY);
    }

    /// <summary>
    /// Hit tests resize/rotate handles.
    /// </summary>
    private ResizeHandle HitTestHandle(double x, double y, (double X, double Y, double Width, double Height) bounds)
    {
        var bx = bounds.X;
        var by = bounds.Y;
        var bw = bounds.Width;
        var bh = bounds.Height;

        // Check rotate handle first (above top center)
        var rotateY = by - RotateHandleOffset;
        if (IsNearPoint(x, y, bx + bw / 2, rotateY))
            return ResizeHandle.Rotate;

        // Check corner handles
        if (IsNearPoint(x, y, bx, by)) return ResizeHandle.TopLeft;
        if (IsNearPoint(x, y, bx + bw, by)) return ResizeHandle.TopRight;
        if (IsNearPoint(x, y, bx, by + bh)) return ResizeHandle.BottomLeft;
        if (IsNearPoint(x, y, bx + bw, by + bh)) return ResizeHandle.BottomRight;

        // Check edge handles
        if (IsNearPoint(x, y, bx + bw / 2, by)) return ResizeHandle.TopCenter;
        if (IsNearPoint(x, y, bx + bw / 2, by + bh)) return ResizeHandle.BottomCenter;
        if (IsNearPoint(x, y, bx, by + bh / 2)) return ResizeHandle.MiddleLeft;
        if (IsNearPoint(x, y, bx + bw, by + bh / 2)) return ResizeHandle.MiddleRight;

        return ResizeHandle.None;
    }

    private static bool IsNearPoint(double x, double y, double px, double py)
    {
        var dx = x - px;
        var dy = y - py;
        return dx * dx + dy * dy <= HandleHitRadius * HandleHitRadius;
    }

    /// <summary>
    /// Performs hit testing to find element at the given point.
    /// </summary>
    private VectorElement? HitTest(ToolPoint point)
    {
        if (Document is null) return null;

        var logger = DebugLogger.Instance;
        logger.Log("Selection", $"HitTest at ({point.X:F1}, {point.Y:F1}) against {Document.Elements.Count} elements");

        // Test elements in reverse order (top to bottom)
        for (var i = Document.Elements.Count - 1; i >= 0; i--)
        {
            var element = Document.Elements[i];
            
            // Skip invisible or locked elements
            if (!element.IsVisible || element.IsLocked) continue;
            
            var bounds = element.GetBoundingBox();
            var hit = element.HitTest(point.X, point.Y);
            
            logger.LogHitTest(element.GetType().Name, point.X, point.Y, bounds, hit);
            
            if (hit)
            {
                logger.Info("Selection", $"Selected: {element.GetType().Name} '{element.Name}'");
                return element;
            }
        }
        
        logger.Log("Selection", "No element hit");
        return null;
    }

    /// <summary>
    /// Updates the marquee selection preview.
    /// </summary>
    private void UpdateMarqueeSelection()
    {
        if (Document is null) return;

        _previewSelection.Clear();
        var (x, y, w, h) = GetDragBounds();

        foreach (var element in Document.Elements)
        {
            // Skip invisible or locked elements
            if (!element.IsVisible || element.IsLocked) continue;
            
            var bounds = element.GetBoundingBox();
            
            // Check if element bounds intersect with marquee
            if (bounds.X < x + w && bounds.X + bounds.Width > x &&
                bounds.Y < y + h && bounds.Y + bounds.Height > y)
            {
                _previewSelection.Add(element);
            }
        }
    }

    /// <summary>
    /// Clears the current selection.
    /// </summary>
    public void ClearSelection()
    {
        _selectedElements.Clear();
        OnSelectionChanged();
    }

    /// <summary>
    /// Selects all elements in the document.
    /// </summary>
    public void SelectAll()
    {
        if (Document is null) return;

        _selectedElements.Clear();
        foreach (var elem in Document.Elements)
        {
            if (elem.IsVisible && !elem.IsLocked)
            {
                _selectedElements.Add(elem);
            }
        }
        OnSelectionChanged();
    }

    /// <summary>
    /// Inverts the current selection.
    /// </summary>
    public void InvertSelection()
    {
        if (Document is null) return;

        var currentlySelected = new HashSet<VectorElement>(_selectedElements);
        _selectedElements.Clear();
        
        foreach (var elem in Document.Elements)
        {
            if (elem.IsVisible && !elem.IsLocked && !currentlySelected.Contains(elem))
            {
                _selectedElements.Add(elem);
            }
        }
        OnSelectionChanged();
    }

    /// <summary>
    /// Deletes the selected elements.
    /// </summary>
    public void DeleteSelected()
    {
        if (Document is null || _selectedElements.Count == 0) return;

        var command = new DeleteElementCommand(Document, _selectedElements);
        History?.ExecuteCommand(command);
        _selectedElements.Clear();
        OnSelectionChanged();
    }

    /// <summary>
    /// Sets the selection to the specified elements.
    /// </summary>
    public void SetSelection(IEnumerable<VectorElement> elements)
    {
        _selectedElements.Clear();
        _selectedElements.AddRange(elements);
        OnSelectionChanged();
    }

    /// <summary>
    /// Gets the selection bounds for the current selection.
    /// </summary>
    public (double X, double Y, double Width, double Height)? GetSelectionBounds()
    {
        if (_selectedElements.Count == 0) return null;
        return GetAggregateBounds();
    }

    private void OnSelectionChanged()
    {
        SelectionChanged?.Invoke(this, _selectedElements);
    }
}
