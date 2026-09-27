namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class SelectionManagerTests
{
    private readonly SelectionManager _manager = new();
    private readonly VectorDocument _document = new();

    public SelectionManagerTests()
    {
        _manager.SetDocument(_document);
    }

    [Fact]
    public void Select_SingleElement_SelectsElement()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _manager.Select(rect);

        Assert.Single(_manager.SelectedElements);
        Assert.Same(rect, _manager.SelectedElements[0]);
        Assert.True(_manager.HasSelection);
        Assert.Equal(1, _manager.SelectionCount);
    }

    [Fact]
    public void Select_SingleElement_ClearsPreviousSelection()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select(rect1);
        _manager.Select(rect2);

        Assert.Single(_manager.SelectedElements);
        Assert.Same(rect2, _manager.SelectedElements[0]);
    }

    [Fact]
    public void Select_MultipleElements_SelectsAll()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);

        Assert.Equal(2, _manager.SelectionCount);
        Assert.Contains(rect1, _manager.SelectedElements);
        Assert.Contains(rect2, _manager.SelectedElements);
    }

    [Fact]
    public void AddToSelection_AddsElement()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select(rect1);
        _manager.AddToSelection(rect2);

        Assert.Equal(2, _manager.SelectionCount);
    }

    [Fact]
    public void AddToSelection_DoesNotDuplicate()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _manager.Select(rect);
        _manager.AddToSelection(rect);

        Assert.Single(_manager.SelectedElements);
    }

    [Fact]
    public void RemoveFromSelection_RemovesElement()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);
        _manager.RemoveFromSelection(rect1);

        Assert.Single(_manager.SelectedElements);
        Assert.Same(rect2, _manager.SelectedElements[0]);
    }

    [Fact]
    public void ToggleSelection_AddsWhenNotSelected()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _manager.ToggleSelection(rect);

        Assert.Single(_manager.SelectedElements);
        Assert.True(_manager.IsSelected(rect));
    }

    [Fact]
    public void ToggleSelection_RemovesWhenSelected()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _manager.Select(rect);
        _manager.ToggleSelection(rect);

        Assert.Empty(_manager.SelectedElements);
        Assert.False(_manager.IsSelected(rect));
    }

    [Fact]
    public void Clear_RemovesAllSelection()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);
        _manager.Clear();

        Assert.Empty(_manager.SelectedElements);
        Assert.False(_manager.HasSelection);
    }

    [Fact]
    public void SelectAll_SelectsAllDocumentElements()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        var rect3 = new SvgRect { X = 200, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);
        _document.Elements.Add(rect3);

        _manager.SelectAll();

        Assert.Equal(3, _manager.SelectionCount);
    }

    [Fact]
    public void IsSelected_ReturnsTrueForSelectedElement()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _manager.Select(rect);

        Assert.True(_manager.IsSelected(rect));
    }

    [Fact]
    public void IsSelected_ReturnsFalseForUnselectedElement()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select(rect1);

        Assert.False(_manager.IsSelected(rect2));
    }

    [Fact]
    public void PrimarySelection_ReturnsFirstSelectedElement()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);

        Assert.Same(rect1, _manager.PrimarySelection);
    }

    [Fact]
    public void GetSelectionBounds_SingleElement_ReturnsElementBounds()
    {
        var rect = new SvgRect { X = 10, Y = 20, Width = 50, Height = 30 };
        _document.Elements.Add(rect);

        _manager.Select(rect);
        var bounds = _manager.GetSelectionBounds();

        Assert.NotNull(bounds);
        Assert.Equal(10, bounds.Value.X);
        Assert.Equal(20, bounds.Value.Y);
        Assert.Equal(50, bounds.Value.Width);
        Assert.Equal(30, bounds.Value.Height);
    }

    [Fact]
    public void GetSelectionBounds_MultipleElements_ReturnsAggregateBounds()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);
        var bounds = _manager.GetSelectionBounds();

        Assert.NotNull(bounds);
        Assert.Equal(10, bounds.Value.X);
        Assert.Equal(10, bounds.Value.Y);
        Assert.Equal(140, bounds.Value.Width); // 100 + 50 - 10
        Assert.Equal(140, bounds.Value.Height); // 100 + 50 - 10
    }

    [Fact]
    public void GetSelectionBounds_NoSelection_ReturnsNull()
    {
        var bounds = _manager.GetSelectionBounds();
        Assert.Null(bounds);
    }

    [Fact]
    public void GetSelectionCenter_ReturnsCenter()
    {
        var rect = new SvgRect { X = 0, Y = 0, Width = 100, Height = 100 };
        _document.Elements.Add(rect);

        _manager.Select(rect);
        var center = _manager.GetSelectionCenter();

        Assert.NotNull(center);
        Assert.Equal(50, center.Value.X);
        Assert.Equal(50, center.Value.Y);
    }

    [Fact]
    public void SelectionChanged_EventRaised()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        SelectionChangedEventArgs? eventArgs = null;
        _manager.SelectionChanged += (_, e) => eventArgs = e;

        _manager.Select(rect);

        Assert.NotNull(eventArgs);
        Assert.Single(eventArgs.AddedElements);
        Assert.Same(rect, eventArgs.AddedElements[0]);
        Assert.Empty(eventArgs.RemovedElements);
    }

    [Fact]
    public void SelectionChanged_EventIncludesRemovedElements()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select(rect1);

        SelectionChangedEventArgs? eventArgs = null;
        _manager.SelectionChanged += (_, e) => eventArgs = e;

        _manager.Select(rect2);

        Assert.NotNull(eventArgs);
        Assert.Single(eventArgs.AddedElements);
        Assert.Single(eventArgs.RemovedElements);
        Assert.Same(rect1, eventArgs.RemovedElements[0]);
    }

    [Fact]
    public void OnElementsGrouped_SelectsGroupAndRemovesChildren()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        var group = new SvgGroup();
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);
        _manager.OnElementsGrouped(group, [rect1, rect2]);

        Assert.Single(_manager.SelectedElements);
        Assert.Same(group, _manager.SelectedElements[0]);
    }

    [Fact]
    public void OnElementsUngrouped_SelectsChildrenAndRemovesGroup()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        var group = new SvgGroup();
        group.Children.Add(rect1);
        group.Children.Add(rect2);
        _document.Elements.Add(group);

        _manager.Select(group);
        _manager.OnElementsUngrouped(group, [rect1, rect2]);

        Assert.Equal(2, _manager.SelectionCount);
        Assert.Contains(rect1, _manager.SelectedElements);
        Assert.Contains(rect2, _manager.SelectedElements);
        Assert.DoesNotContain(group, _manager.SelectedElements);
    }

    [Fact]
    public void OnElementsDeleted_RemovesFromSelection()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select([rect1, rect2]);
        _manager.OnElementsDeleted([rect1]);

        Assert.Single(_manager.SelectedElements);
        Assert.Same(rect2, _manager.SelectedElements[0]);
    }

    [Fact]
    public void SelectInRect_SelectsElementsInRectangle()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 200, Y = 200, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.SelectInRect(0, 0, 100, 100);

        Assert.Single(_manager.SelectedElements);
        Assert.Same(rect1, _manager.SelectedElements[0]);
    }

    [Fact]
    public void SelectInRect_WithAddToSelection_AddsToExisting()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 200, Y = 200, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select(rect1);
        _manager.SelectInRect(150, 150, 150, 150, addToSelection: true);

        Assert.Equal(2, _manager.SelectionCount);
    }

    [Fact]
    public void HitTestAndSelect_SelectsTopmostElement()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 20, Y = 20, Width = 50, Height = 50 }; // Overlaps rect1
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        var hit = _manager.HitTestAndSelect(30, 30);

        Assert.Same(rect2, hit); // rect2 is on top (added last)
        Assert.Single(_manager.SelectedElements);
        Assert.Same(rect2, _manager.SelectedElements[0]);
    }

    [Fact]
    public void HitTestAndSelect_OnEmpty_ClearsSelection()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _manager.Select(rect);
        var hit = _manager.HitTestAndSelect(200, 200);

        Assert.Null(hit);
        Assert.Empty(_manager.SelectedElements);
    }

    [Fact]
    public void HitTestAndSelect_WithAddToSelection_KeepsExisting()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        var rect2 = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _manager.Select(rect1);
        _manager.HitTestAndSelect(125, 125, addToSelection: true);

        Assert.Equal(2, _manager.SelectionCount);
    }

    [Fact]
    public void SetDocument_ClearsSelection()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);
        _manager.Select(rect);

        var newDocument = new VectorDocument();
        _manager.SetDocument(newDocument);

        Assert.Empty(_manager.SelectedElements);
    }
}
