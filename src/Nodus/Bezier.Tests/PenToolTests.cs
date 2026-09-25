namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Services;
using Bezier.Core.Tools;

public class ControlPointTests
{
    [Fact]
    public void CreateCorner_HasNoHandles()
    {
        var point = ControlPoint.CreateCorner(100, 100);

        Assert.Equal((100, 100), point.Position);
        Assert.Null(point.InHandle);
        Assert.Null(point.OutHandle);
        Assert.Equal(ControlPointType.Corner, point.Type);
    }

    [Fact]
    public void CreateSmooth_HasSymmetricHandles()
    {
        var point = ControlPoint.CreateSmooth(100, 100, 20, 10);

        Assert.Equal((100, 100), point.Position);
        Assert.Equal((-20, -10), point.InHandle);
        Assert.Equal((20, 10), point.OutHandle);
        Assert.Equal(ControlPointType.Smooth, point.Type);
    }

    [Fact]
    public void CreateSymmetric_HasEqualHandles()
    {
        var point = ControlPoint.CreateSymmetric(100, 100, 30, 0);

        Assert.Equal((30, 0), point.OutHandle);
        Assert.Equal((-30, 0), point.InHandle);
        Assert.Equal(ControlPointType.Symmetric, point.Type);
    }

    [Fact]
    public void InHandleAbsolute_ReturnsAbsolutePosition()
    {
        var point = ControlPoint.CreateSmooth(100, 100, 20, 10);

        Assert.Equal((80, 90), point.InHandleAbsolute);
    }

    [Fact]
    public void OutHandleAbsolute_ReturnsAbsolutePosition()
    {
        var point = ControlPoint.CreateSmooth(100, 100, 20, 10);

        Assert.Equal((120, 110), point.OutHandleAbsolute);
    }

    [Fact]
    public void SetOutHandle_Symmetric_MirrorsInHandle()
    {
        var point = ControlPoint.CreateSymmetric(100, 100, 10, 10);

        point.SetOutHandle(30, 20);

        Assert.Equal((30, 20), point.OutHandle);
        Assert.Equal((-30, -20), point.InHandle);
    }

    [Fact]
    public void SetOutHandle_Corner_DoesNotAffectInHandle()
    {
        var point = ControlPoint.CreateCorner(100, 100);
        point.InHandle = (10, 10);

        point.SetOutHandle(30, 20);

        Assert.Equal((30, 20), point.OutHandle);
        Assert.Equal((10, 10), point.InHandle); // Unchanged
    }

    [Fact]
    public void ConvertToCorner_ChangesType()
    {
        var point = ControlPoint.CreateSmooth(100, 100, 20, 10);

        point.ConvertToCorner();

        Assert.Equal(ControlPointType.Corner, point.Type);
    }

    [Fact]
    public void HitTestAnchor_ReturnsTrue_WhenNear()
    {
        var point = ControlPoint.CreateCorner(100, 100);

        Assert.True(point.HitTestAnchor(100, 100));
        Assert.True(point.HitTestAnchor(105, 105));
        Assert.True(point.HitTestAnchor(95, 95));
    }

    [Fact]
    public void HitTestAnchor_ReturnsFalse_WhenFar()
    {
        var point = ControlPoint.CreateCorner(100, 100);

        Assert.False(point.HitTestAnchor(120, 120));
    }

    [Fact]
    public void HitTestOutHandle_ReturnsTrue_WhenNear()
    {
        var point = ControlPoint.CreateSmooth(100, 100, 20, 0);

        // OutHandle is (20, 0) relative, so absolute is (120, 100)
        Assert.True(point.HitTestOutHandle(120, 100)); // At handle position
        Assert.True(point.HitTestOutHandle(122, 102)); // Near handle
    }

    [Fact]
    public void HitTestOutHandle_ReturnsFalse_WhenNoHandle()
    {
        var point = ControlPoint.CreateCorner(100, 100);

        Assert.False(point.HitTestOutHandle(100, 100));
    }

    [Fact]
    public void Clone_CreatesIndependentCopy()
    {
        var original = ControlPoint.CreateSmooth(100, 100, 20, 10);
        var clone = original.Clone();

        clone.Position = (200, 200);

        Assert.Equal((100, 100), original.Position);
        Assert.Equal((200, 200), clone.Position);
    }
}

public class PenToolTests
{
    private readonly PenTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;

    public PenToolTests()
    {
        _tool = new PenTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Pen", _tool.Name);
        Assert.Equal("Pen", _tool.Icon);
        Assert.Equal("P", _tool.Shortcut);
        Assert.Equal(ToolCursor.Cross, _tool.Cursor);
    }

    [Fact]
    public void Click_CreatesCornerPoint()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Equal(1, _tool.PointCount);
    }

    [Fact]
    public void ClickDrag_CreatesSmoothPoint()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(150, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(150, 100), KeyModifiers.None);

        Assert.Equal(1, _tool.PointCount);
    }

    [Fact]
    public void MultipleClicks_CreatesMultiplePoints()
    {
        // First point
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        // Second point
        _tool.OnMouseDown(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(200, 100), KeyModifiers.None);

        // Third point
        _tool.OnMouseDown(new ToolPoint(200, 200), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(200, 200), KeyModifiers.None);

        Assert.Equal(3, _tool.PointCount);
    }

    [Fact]
    public void Enter_FinishesOpenPath()
    {
        // Create two points
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseDown(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(200, 100), KeyModifiers.None);

        // Finish with Enter
        _tool.OnKeyDown("Enter", KeyModifiers.None);

        Assert.Single(_document.Elements);
        Assert.Equal(0, _tool.PointCount);
    }

    [Fact]
    public void Escape_CancelsPath()
    {
        // Create a point
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        // Cancel with Escape
        _tool.OnKeyDown("Escape", KeyModifiers.None);

        Assert.Empty(_document.Elements);
        Assert.Equal(0, _tool.PointCount);
    }

    [Fact]
    public void Backspace_DeletesLastPoint()
    {
        // Create two points
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseDown(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(200, 100), KeyModifiers.None);

        // Delete last point
        _tool.OnKeyDown("Backspace", KeyModifiers.None);

        Assert.Equal(1, _tool.PointCount);
    }

    [Fact]
    public void ClickOnFirstPoint_ClosesPath()
    {
        // Create three points
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseDown(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnMouseDown(new ToolPoint(150, 200), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(150, 200), KeyModifiers.None);

        // Click near first point to close
        _tool.OnMouseDown(new ToolPoint(102, 102), KeyModifiers.None);

        Assert.Single(_document.Elements);
        var path = _document.Elements[0] as Bezier.Core.Models.Elements.SvgPath;
        Assert.NotNull(path);
        Assert.Contains("Z", path.PathData); // Path is closed
    }

    [Fact]
    public void FinishedPath_IsUndoable()
    {
        // Create two points and finish
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseDown(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(200, 100), KeyModifiers.None);
        _tool.OnKeyDown("Enter", KeyModifiers.None);

        Assert.Single(_document.Elements);

        _history.Undo();

        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void SinglePoint_DoesNotCreatePath()
    {
        // Create one point and try to finish
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("Enter", KeyModifiers.None);

        // Should not create path with single point
        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void AltDrag_CreatesCornerWithHandle()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.Alt);
        _tool.OnMouseMove(new ToolPoint(150, 100), KeyModifiers.Alt);
        _tool.OnMouseUp(new ToolPoint(150, 100), KeyModifiers.Alt);

        Assert.Equal(1, _tool.PointCount);
    }

    [Fact]
    public void IsDrawingPath_TrueWhileDrawing()
    {
        Assert.False(_tool.IsDrawingPath);

        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.True(_tool.IsDrawingPath);
    }
}
