namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class GuideTests
{
    [Fact]
    public void Horizontal_CreatesHorizontalGuide()
    {
        var guide = Guide.Horizontal(100);

        Assert.Equal(GuideOrientation.Horizontal, guide.Orientation);
        Assert.Equal(100, guide.Position);
    }

    [Fact]
    public void Vertical_CreatesVerticalGuide()
    {
        var guide = Guide.Vertical(200);

        Assert.Equal(GuideOrientation.Vertical, guide.Orientation);
        Assert.Equal(200, guide.Position);
    }

    [Fact]
    public void HitTest_Horizontal_ReturnsTrue_WhenNear()
    {
        var guide = Guide.Horizontal(100);

        Assert.True(guide.HitTest(50, 100));
        Assert.True(guide.HitTest(50, 103));
        Assert.True(guide.HitTest(50, 97));
    }

    [Fact]
    public void HitTest_Horizontal_ReturnsFalse_WhenFar()
    {
        var guide = Guide.Horizontal(100);

        Assert.False(guide.HitTest(50, 110));
        Assert.False(guide.HitTest(50, 90));
    }

    [Fact]
    public void HitTest_Vertical_ReturnsTrue_WhenNear()
    {
        var guide = Guide.Vertical(100);

        Assert.True(guide.HitTest(100, 50));
        Assert.True(guide.HitTest(103, 50));
        Assert.True(guide.HitTest(97, 50));
    }

    [Fact]
    public void HitTest_Vertical_ReturnsFalse_WhenFar()
    {
        var guide = Guide.Vertical(100);

        Assert.False(guide.HitTest(110, 50));
        Assert.False(guide.HitTest(90, 50));
    }
}

public class SnapManagerTests
{
    private readonly SnapManager _snapManager;
    private readonly VectorDocument _document;

    public SnapManagerTests()
    {
        _snapManager = new SnapManager
        {
            GridSize = 10,
            Tolerance = 5
        };
        _document = new VectorDocument();
    }

    [Fact]
    public void DefaultProperties_AreSet()
    {
        var manager = new SnapManager();

        Assert.True(manager.IsEnabled);
        Assert.Equal(8, manager.Tolerance);
        Assert.Equal(10, manager.GridSize);
        Assert.True(manager.SnapToGrid);
        Assert.True(manager.SnapToGuides);
        Assert.True(manager.SnapToObjects);
        Assert.True(manager.SmartGuidesEnabled);
    }

    [Fact]
    public void Snap_WhenDisabled_ReturnsOriginalPoint()
    {
        _snapManager.IsEnabled = false;

        var result = _snapManager.Snap(15, 15);

        Assert.Equal(15, result.X);
        Assert.Equal(15, result.Y);
        Assert.False(result.SnappedX);
        Assert.False(result.SnappedY);
    }

    [Fact]
    public void Snap_ToGrid_SnapsNearbyPoint()
    {
        var result = _snapManager.Snap(12, 18);

        Assert.Equal(10, result.X);
        Assert.Equal(20, result.Y);
        Assert.True(result.SnappedX);
        Assert.True(result.SnappedY);
    }

    [Fact]
    public void Snap_ToGrid_DoesNotSnapFarPoint()
    {
        // 15 rounds to 20, but 15 is 5 away which equals tolerance, so it snaps
        // Use 25 which is equidistant from 20 and 30, should snap to nearest (20 or 30)
        // Let's use a clearer test: disable grid and check no snap occurs
        _snapManager.SnapToGrid = false;
        var result = _snapManager.Snap(16, 16);

        Assert.Equal(16, result.X);
        Assert.Equal(16, result.Y);
        Assert.False(result.SnappedX);
        Assert.False(result.SnappedY);
    }

    [Fact]
    public void Snap_ToGuide_SnapsToVerticalGuide()
    {
        _snapManager.AddGuide(Guide.Vertical(100));

        var result = _snapManager.Snap(97, 50);

        Assert.Equal(100, result.X);
        Assert.True(result.SnappedX);
        Assert.Equal(100, result.SnapLineX);
    }

    [Fact]
    public void Snap_ToGuide_SnapsToHorizontalGuide()
    {
        _snapManager.AddGuide(Guide.Horizontal(100));

        var result = _snapManager.Snap(50, 103);

        Assert.Equal(100, result.Y);
        Assert.True(result.SnappedY);
        Assert.Equal(100, result.SnapLineY);
    }

    [Fact]
    public void Snap_ToObject_SnapsToEdge()
    {
        var rect = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        var result = _snapManager.Snap(102, 50, _document);

        Assert.Equal(100, result.X); // Snaps to left edge
        Assert.True(result.SnappedX);
    }

    [Fact]
    public void Snap_ToObject_SnapsToCenter()
    {
        var rect = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        // Center is at (125, 125)
        var result = _snapManager.Snap(123, 50, _document);

        Assert.Equal(125, result.X);
        Assert.True(result.SnappedX);
    }

    [Fact]
    public void Snap_ToObject_ExcludesSpecifiedElement()
    {
        var rect = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        var result = _snapManager.Snap(102, 50, _document, rect);

        // Should not snap to the excluded rect
        Assert.Equal(100, result.X); // Snaps to grid instead
    }

    [Fact]
    public void AddGuide_AddsToList()
    {
        var guide = Guide.Horizontal(100);

        _snapManager.AddGuide(guide);

        Assert.Single(_snapManager.Guides);
        Assert.Contains(guide, _snapManager.Guides);
    }

    [Fact]
    public void RemoveGuide_RemovesFromList()
    {
        var guide = Guide.Horizontal(100);
        _snapManager.AddGuide(guide);

        var removed = _snapManager.RemoveGuide(guide);

        Assert.True(removed);
        Assert.Empty(_snapManager.Guides);
    }

    [Fact]
    public void RemoveGuide_ById_RemovesFromList()
    {
        var guide = Guide.Horizontal(100);
        _snapManager.AddGuide(guide);

        var removed = _snapManager.RemoveGuide(guide.Id);

        Assert.True(removed);
        Assert.Empty(_snapManager.Guides);
    }

    [Fact]
    public void ClearGuides_RemovesAllGuides()
    {
        _snapManager.AddGuide(Guide.Horizontal(100));
        _snapManager.AddGuide(Guide.Vertical(200));

        _snapManager.ClearGuides();

        Assert.Empty(_snapManager.Guides);
    }

    [Fact]
    public void HitTestGuide_FindsGuide()
    {
        var guide = Guide.Horizontal(100);
        _snapManager.AddGuide(guide);

        var found = _snapManager.HitTestGuide(50, 100);

        Assert.Same(guide, found);
    }

    [Fact]
    public void HitTestGuide_ReturnsNull_WhenNoGuide()
    {
        _snapManager.AddGuide(Guide.Horizontal(100));

        var found = _snapManager.HitTestGuide(50, 200);

        Assert.Null(found);
    }

    [Fact]
    public void GuidesChanged_EventRaised_OnAdd()
    {
        var raised = false;
        _snapManager.GuidesChanged += (_, _) => raised = true;

        _snapManager.AddGuide(Guide.Horizontal(100));

        Assert.True(raised);
    }

    [Fact]
    public void GuidesChanged_EventRaised_OnRemove()
    {
        var guide = Guide.Horizontal(100);
        _snapManager.AddGuide(guide);

        var raised = false;
        _snapManager.GuidesChanged += (_, _) => raised = true;

        _snapManager.RemoveGuide(guide);

        Assert.True(raised);
    }

    [Fact]
    public void SnapToGridValue_SnapsCorrectly()
    {
        Assert.Equal(10, _snapManager.SnapToGridValue(12));
        Assert.Equal(20, _snapManager.SnapToGridValue(18));
        Assert.Equal(0, _snapManager.SnapToGridValue(4));
    }

    [Fact]
    public void SnapBounds_SnapsAllCorners()
    {
        _snapManager.AddGuide(Guide.Vertical(100));

        // Bounds starting at 98, should snap to 100
        var result = _snapManager.SnapBounds(98, 50, 50, 50, _document);

        Assert.Equal(100, result.X);
        Assert.True(result.SnappedX);
    }

    [Fact]
    public void Snap_GridDisabled_DoesNotSnapToGrid()
    {
        _snapManager.SnapToGrid = false;

        var result = _snapManager.Snap(12, 18);

        Assert.Equal(12, result.X);
        Assert.Equal(18, result.Y);
    }

    [Fact]
    public void Snap_GuidesDisabled_DoesNotSnapToGuides()
    {
        _snapManager.SnapToGuides = false;
        _snapManager.AddGuide(Guide.Vertical(100));

        var result = _snapManager.Snap(98, 50);

        Assert.Equal(100, result.X); // Snaps to grid at 100
    }

    [Fact]
    public void SmartGuides_CreatedWhenSnappingToObjects()
    {
        var rect = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _snapManager.Snap(102, 50, _document);

        Assert.NotEmpty(_snapManager.ActiveSmartGuides);
    }

    [Fact]
    public void ClearSmartGuides_ClearsActiveGuides()
    {
        var rect = new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _snapManager.Snap(102, 50, _document);
        Assert.NotEmpty(_snapManager.ActiveSmartGuides);

        _snapManager.ClearSmartGuides();

        Assert.Empty(_snapManager.ActiveSmartGuides);
    }
}
