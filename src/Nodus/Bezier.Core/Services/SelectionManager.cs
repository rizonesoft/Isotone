namespace Bezier.Core.Services;

using System.Collections.ObjectModel;
using System.Collections.Specialized;
using Bezier.Core.Models;

/// <summary>
/// Event arguments for selection change events.
/// </summary>
public class SelectionChangedEventArgs : EventArgs
{
    /// <summary>
    /// Gets the elements that were added to the selection.
    /// </summary>
    public IReadOnlyList<VectorElement> AddedElements { get; }

    /// <summary>
    /// Gets the elements that were removed from the selection.
    /// </summary>
    public IReadOnlyList<VectorElement> RemovedElements { get; }

    /// <summary>
    /// Gets all currently selected elements.
    /// </summary>
    public IReadOnlyList<VectorElement> CurrentSelection { get; }

    public SelectionChangedEventArgs(
        IEnumerable<VectorElement> added,
        IEnumerable<VectorElement> removed,
        IEnumerable<VectorElement> current)
    {
        AddedElements = added.ToList();
        RemovedElements = removed.ToList();
        CurrentSelection = current.ToList();
    }
}

/// <summary>
/// Manages the selection state for vector elements.
/// </summary>
public class SelectionManager
{
    private readonly ObservableCollection<VectorElement> _selectedElements = [];
    private VectorDocument? _document;
    private bool _isUpdating;

    /// <summary>
    /// Gets the observable collection of selected elements.
    /// </summary>
    public ObservableCollection<VectorElement> SelectedElements => _selectedElements;

    /// <summary>
    /// Gets whether any elements are selected.
    /// </summary>
    public bool HasSelection => _selectedElements.Count > 0;

    /// <summary>
    /// Gets the number of selected elements.
    /// </summary>
    public int SelectionCount => _selectedElements.Count;

    /// <summary>
    /// Gets the primary selected element (first in selection).
    /// </summary>
    public VectorElement? PrimarySelection => _selectedElements.FirstOrDefault();

    /// <summary>
    /// Event raised when the selection changes.
    /// </summary>
    public event EventHandler<SelectionChangedEventArgs>? SelectionChanged;

    /// <summary>
    /// Event raised when the selection bounds change.
    /// </summary>
    public event EventHandler<(double X, double Y, double Width, double Height)>? SelectionBoundsChanged;

    public SelectionManager()
    {
        _selectedElements.CollectionChanged += OnSelectedElementsChanged;
    }

    /// <summary>
    /// Sets the document context for selection operations.
    /// </summary>
    public void SetDocument(VectorDocument? document)
    {
        if (_document != document)
        {
            Clear();
            _document = document;
        }
    }

    /// <summary>
    /// Selects a single element, clearing any previous selection.
    /// </summary>
    public void Select(VectorElement element)
    {
        ArgumentNullException.ThrowIfNull(element);

        _isUpdating = true;
        var removed = _selectedElements.ToList();
        _selectedElements.Clear();
        _selectedElements.Add(element);
        _isUpdating = false;

        RaiseSelectionChanged([element], removed);
    }

    /// <summary>
    /// Selects multiple elements, clearing any previous selection.
    /// </summary>
    public void Select(IEnumerable<VectorElement> elements)
    {
        ArgumentNullException.ThrowIfNull(elements);

        _isUpdating = true;
        var removed = _selectedElements.ToList();
        var added = elements.ToList();
        _selectedElements.Clear();
        foreach (var element in added)
        {
            _selectedElements.Add(element);
        }
        _isUpdating = false;

        RaiseSelectionChanged(added, removed);
    }

    /// <summary>
    /// Adds an element to the current selection.
    /// </summary>
    public void AddToSelection(VectorElement element)
    {
        ArgumentNullException.ThrowIfNull(element);

        if (!_selectedElements.Contains(element))
        {
            _selectedElements.Add(element);
            RaiseSelectionChanged([element], []);
        }
    }

    /// <summary>
    /// Adds multiple elements to the current selection.
    /// </summary>
    public void AddToSelection(IEnumerable<VectorElement> elements)
    {
        ArgumentNullException.ThrowIfNull(elements);

        _isUpdating = true;
        var added = new List<VectorElement>();
        foreach (var element in elements)
        {
            if (!_selectedElements.Contains(element))
            {
                _selectedElements.Add(element);
                added.Add(element);
            }
        }
        _isUpdating = false;

        if (added.Count > 0)
        {
            RaiseSelectionChanged(added, []);
        }
    }

    /// <summary>
    /// Removes an element from the selection.
    /// </summary>
    public void RemoveFromSelection(VectorElement element)
    {
        ArgumentNullException.ThrowIfNull(element);

        if (_selectedElements.Remove(element))
        {
            RaiseSelectionChanged([], [element]);
        }
    }

    /// <summary>
    /// Toggles the selection state of an element.
    /// </summary>
    public void ToggleSelection(VectorElement element)
    {
        ArgumentNullException.ThrowIfNull(element);

        if (_selectedElements.Contains(element))
        {
            RemoveFromSelection(element);
        }
        else
        {
            AddToSelection(element);
        }
    }

    /// <summary>
    /// Clears the current selection.
    /// </summary>
    public void Clear()
    {
        if (_selectedElements.Count == 0) return;

        _isUpdating = true;
        var removed = _selectedElements.ToList();
        _selectedElements.Clear();
        _isUpdating = false;

        RaiseSelectionChanged([], removed);
    }

    /// <summary>
    /// Selects all elements in the document.
    /// </summary>
    public void SelectAll()
    {
        if (_document is null) return;

        Select(_document.Elements);
    }

    /// <summary>
    /// Checks if an element is currently selected.
    /// </summary>
    public bool IsSelected(VectorElement element)
    {
        return _selectedElements.Contains(element);
    }

    /// <summary>
    /// Gets the aggregate bounding box for all selected elements.
    /// </summary>
    public (double X, double Y, double Width, double Height)? GetSelectionBounds()
    {
        if (_selectedElements.Count == 0) return null;

        double minX = double.MaxValue;
        double minY = double.MaxValue;
        double maxX = double.MinValue;
        double maxY = double.MinValue;

        foreach (var element in _selectedElements)
        {
            var bounds = element.GetBoundingBox();
            
            // Apply element transform
            var transformedX = bounds.X + element.Transform.TranslateX;
            var transformedY = bounds.Y + element.Transform.TranslateY;
            var transformedRight = transformedX + bounds.Width * element.Transform.ScaleX;
            var transformedBottom = transformedY + bounds.Height * element.Transform.ScaleY;

            minX = Math.Min(minX, transformedX);
            minY = Math.Min(minY, transformedY);
            maxX = Math.Max(maxX, transformedRight);
            maxY = Math.Max(maxY, transformedBottom);
        }

        return (minX, minY, maxX - minX, maxY - minY);
    }

    /// <summary>
    /// Gets the center point of the selection bounds.
    /// </summary>
    public (double X, double Y)? GetSelectionCenter()
    {
        var bounds = GetSelectionBounds();
        if (bounds is null) return null;

        var (x, y, w, h) = bounds.Value;
        return (x + w / 2, y + h / 2);
    }

    /// <summary>
    /// Handles selection after grouping elements.
    /// Selects the new group and removes individual elements from selection.
    /// </summary>
    public void OnElementsGrouped(VectorElement group, IEnumerable<VectorElement> groupedElements)
    {
        _isUpdating = true;
        var removed = new List<VectorElement>();
        foreach (var element in groupedElements)
        {
            if (_selectedElements.Remove(element))
            {
                removed.Add(element);
            }
        }
        _selectedElements.Add(group);
        _isUpdating = false;

        RaiseSelectionChanged([group], removed);
    }

    /// <summary>
    /// Handles selection after ungrouping elements.
    /// Selects the ungrouped children and removes the group from selection.
    /// </summary>
    public void OnElementsUngrouped(VectorElement group, IEnumerable<VectorElement> children)
    {
        _isUpdating = true;
        var added = children.ToList();
        _selectedElements.Remove(group);
        foreach (var child in added)
        {
            if (!_selectedElements.Contains(child))
            {
                _selectedElements.Add(child);
            }
        }
        _isUpdating = false;

        RaiseSelectionChanged(added, [group]);
    }

    /// <summary>
    /// Updates selection when elements are deleted.
    /// </summary>
    public void OnElementsDeleted(IEnumerable<VectorElement> deletedElements)
    {
        _isUpdating = true;
        var removed = new List<VectorElement>();
        foreach (var element in deletedElements)
        {
            if (_selectedElements.Remove(element))
            {
                removed.Add(element);
            }
        }
        _isUpdating = false;

        if (removed.Count > 0)
        {
            RaiseSelectionChanged([], removed);
        }
    }

    /// <summary>
    /// Selects elements within a rectangular area.
    /// </summary>
    public void SelectInRect(double x, double y, double width, double height, bool addToSelection = false)
    {
        if (_document is null) return;

        var elementsInRect = new List<VectorElement>();
        var right = x + width;
        var bottom = y + height;

        foreach (var element in _document.Elements)
        {
            var bounds = element.GetBoundingBox();
            var transformedX = bounds.X + element.Transform.TranslateX;
            var transformedY = bounds.Y + element.Transform.TranslateY;
            var transformedRight = transformedX + bounds.Width;
            var transformedBottom = transformedY + bounds.Height;

            // Check intersection
            if (transformedX < right && transformedRight > x &&
                transformedY < bottom && transformedBottom > y)
            {
                elementsInRect.Add(element);
            }
        }

        if (addToSelection)
        {
            AddToSelection(elementsInRect);
        }
        else
        {
            Select(elementsInRect);
        }
    }

    /// <summary>
    /// Performs hit testing and selects the topmost element at the given point.
    /// </summary>
    public VectorElement? HitTestAndSelect(double x, double y, bool addToSelection = false, bool toggleSelection = false)
    {
        if (_document is null) return null;

        // Test elements in reverse order (top to bottom)
        for (var i = _document.Elements.Count - 1; i >= 0; i--)
        {
            var element = _document.Elements[i];
            if (element.HitTest(x, y))
            {
                if (toggleSelection)
                {
                    ToggleSelection(element);
                }
                else if (addToSelection)
                {
                    AddToSelection(element);
                }
                else
                {
                    Select(element);
                }
                return element;
            }
        }

        // Clicked on empty space
        if (!addToSelection && !toggleSelection)
        {
            Clear();
        }
        return null;
    }

    private void OnSelectedElementsChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (_isUpdating) return;

        var added = e.NewItems?.Cast<VectorElement>().ToList() ?? [];
        var removed = e.OldItems?.Cast<VectorElement>().ToList() ?? [];

        RaiseSelectionChanged(added, removed);
    }

    private void RaiseSelectionChanged(IEnumerable<VectorElement> added, IEnumerable<VectorElement> removed)
    {
        SelectionChanged?.Invoke(this, new SelectionChangedEventArgs(added, removed, _selectedElements));

        var bounds = GetSelectionBounds();
        if (bounds is not null)
        {
            SelectionBoundsChanged?.Invoke(this, bounds.Value);
        }
    }
}
