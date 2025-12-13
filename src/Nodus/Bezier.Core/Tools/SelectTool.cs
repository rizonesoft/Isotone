namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Selection mode for the select tool.
/// </summary>
public enum SelectMode
{
    None,
    Selecting,
    Moving,
    MarqueeSelect
}

/// <summary>
/// Tool for selecting and manipulating elements.
/// </summary>
public class SelectTool : ToolBase
{
    private SelectMode _mode = SelectMode.None;
    private readonly List<VectorElement> _selectedElements = [];
    private readonly List<VectorElement> _previewSelection = [];
    private MoveCommand? _moveCommand;

    /// <inheritdoc/>
    public override string Name => "Select";

    /// <inheritdoc/>
    public override string Icon => "CursorClick";

    /// <inheritdoc/>
    public override ToolCursor Cursor => _mode == SelectMode.Moving ? ToolCursor.Move : ToolCursor.Arrow;

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

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        _mode = SelectMode.None;
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

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
        }

        _mode = SelectMode.None;
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

        return false;
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        // Colors in ARGB format (0xAARRGGBB)
        const uint selectionColor = 0xFFFF6B35; // Orange accent
        const uint marqueeColor = 0x40FF6B35; // Semi-transparent orange
        const uint handleColor = 0xFFFFFFFF; // White
        const uint handleBorderColor = 0xFFFF6B35; // Orange border

        // Draw selection handles for selected elements
        foreach (var element in _selectedElements)
        {
            var bounds = element.GetBoundingBox();
            
            // Apply current drag offset if moving
            var offsetX = 0.0;
            var offsetY = 0.0;
            if (_mode == SelectMode.Moving && IsDragging)
            {
                var delta = GetDragDelta();
                offsetX = delta.DeltaX;
                offsetY = delta.DeltaY;
            }

            var x = bounds.X + offsetX;
            var y = bounds.Y + offsetY;
            var w = bounds.Width;
            var h = bounds.Height;

            // Draw bounding box
            context.DrawRect(x, y, w, h, selectionColor, 1.5f);

            // Draw corner and edge handles
            const double handleSize = 8;
            var halfHandle = handleSize / 2;

            // Helper to draw a handle (white fill with orange border)
            void DrawHandle(double hx, double hy)
            {
                context.DrawRect(hx - halfHandle, hy - halfHandle, handleSize, handleSize, handleColor, 1f, true);
                context.DrawRect(hx - halfHandle, hy - halfHandle, handleSize, handleSize, handleBorderColor, 1f, false);
            }

            // Corner handles
            DrawHandle(x, y);           // Top-left
            DrawHandle(x + w, y);       // Top-right
            DrawHandle(x, y + h);       // Bottom-left
            DrawHandle(x + w, y + h);   // Bottom-right

            // Edge handles
            DrawHandle(x + w / 2, y);       // Top
            DrawHandle(x + w / 2, y + h);   // Bottom
            DrawHandle(x, y + h / 2);       // Left
            DrawHandle(x + w, y + h / 2);   // Right
        }

        // Draw marquee selection box
        if (_mode == SelectMode.MarqueeSelect && IsDragging)
        {
            var (x, y, w, h) = GetDragBounds();
            context.DrawRect(x, y, w, h, marqueeColor, 1f, true);
            context.DrawRect(x, y, w, h, selectionColor, 1f, false);

            // Highlight elements in marquee
            foreach (var element in _previewSelection)
            {
                var bounds = element.GetBoundingBox();
                context.DrawRect(bounds.X, bounds.Y, bounds.Width, bounds.Height, selectionColor, 1f);
            }
        }
    }

    /// <summary>
    /// Performs hit testing to find element at the given point.
    /// </summary>
    private VectorElement? HitTest(ToolPoint point)
    {
        if (Document is null) return null;

        // Test elements in reverse order (top to bottom)
        for (var i = Document.Elements.Count - 1; i >= 0; i--)
        {
            var element = Document.Elements[i];
            if (element.HitTest(point.X, point.Y))
            {
                return element;
            }
        }
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
        _selectedElements.AddRange(Document.Elements);
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

    private void OnSelectionChanged()
    {
        SelectionChanged?.Invoke(this, _selectedElements);
    }
}
