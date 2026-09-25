namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;
using Bezier.Core.Tools;

public class ToolManagerTests
{
    private readonly ToolManager _manager = new();

    [Fact]
    public void RegisterTool_AddsTool()
    {
        var tool = new SelectTool();
        _manager.RegisterTool(tool);

        Assert.Single(_manager.Tools);
        Assert.Same(tool, _manager.Tools[0]);
    }

    [Fact]
    public void SetTool_ChangesActiveTool()
    {
        var selectTool = new SelectTool();
        var panTool = new PanTool();
        _manager.RegisterTool(selectTool);
        _manager.RegisterTool(panTool);

        _manager.SetTool(selectTool);
        Assert.Same(selectTool, _manager.ActiveTool);

        _manager.SetTool(panTool);
        Assert.Same(panTool, _manager.ActiveTool);
    }

    [Fact]
    public void SetTool_ByName_FindsCorrectTool()
    {
        var selectTool = new SelectTool();
        var panTool = new PanTool();
        _manager.RegisterTool(selectTool);
        _manager.RegisterTool(panTool);

        _manager.SetTool("Pan");
        Assert.Same(panTool, _manager.ActiveTool);
    }

    [Fact]
    public void SetTool_RaisesActiveToolChangedEvent()
    {
        var tool = new SelectTool();
        _manager.RegisterTool(tool);

        ITool? changedTool = null;
        _manager.ActiveToolChanged += (_, t) => changedTool = t;

        _manager.SetTool(tool);

        Assert.Same(tool, changedTool);
    }

    [Fact]
    public void SetTool_RaisesCursorChangedEvent()
    {
        var tool = new PanTool();
        _manager.RegisterTool(tool);

        ToolCursor? changedCursor = null;
        _manager.CursorChanged += (_, c) => changedCursor = c;

        _manager.SetTool(tool);

        Assert.Equal(ToolCursor.Hand, changedCursor);
    }

    [Fact]
    public void HandleShortcut_SwitchesToCorrectTool()
    {
        var selectTool = new SelectTool();
        var panTool = new PanTool();
        _manager.RegisterTool(selectTool);
        _manager.RegisterTool(panTool);

        var handled = _manager.HandleShortcut("H");

        Assert.True(handled);
        Assert.Same(panTool, _manager.ActiveTool);
    }

    [Fact]
    public void HandleShortcut_ReturnsFalse_WhenNoMatch()
    {
        var selectTool = new SelectTool();
        _manager.RegisterTool(selectTool);

        var handled = _manager.HandleShortcut("X");

        Assert.False(handled);
    }

    [Fact]
    public void PushTool_TemporarilySwitchesTool()
    {
        var selectTool = new SelectTool();
        var panTool = new PanTool();
        _manager.RegisterTool(selectTool);
        _manager.RegisterTool(panTool);

        _manager.SetTool(selectTool);
        _manager.PushTool(panTool);

        Assert.Same(panTool, _manager.ActiveTool);
    }

    [Fact]
    public void PopTool_ReturnsToPreviousTool()
    {
        var selectTool = new SelectTool();
        var panTool = new PanTool();
        _manager.RegisterTool(selectTool);
        _manager.RegisterTool(panTool);

        _manager.SetTool(selectTool);
        _manager.PushTool(panTool);
        _manager.PopTool();

        Assert.Same(selectTool, _manager.ActiveTool);
    }

    [Fact]
    public void GetTool_ReturnsToolByType()
    {
        var selectTool = new SelectTool();
        var panTool = new PanTool();
        _manager.RegisterTool(selectTool);
        _manager.RegisterTool(panTool);

        var found = _manager.GetTool<PanTool>();

        Assert.Same(panTool, found);
    }

    [Fact]
    public void SetContext_SetsContextOnAllTools()
    {
        var document = new VectorDocument();
        var history = new HistoryManager();
        var tool = new SelectTool();
        _manager.RegisterTool(tool);

        _manager.SetContext(document, history);

        // Tool should now have context (we can't directly verify, but it shouldn't throw)
        _manager.SetTool(tool);
        Assert.Same(tool, _manager.ActiveTool);
    }
}

public class SelectToolTests
{
    private readonly SelectTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;

    public SelectToolTests()
    {
        _tool = new SelectTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Select", _tool.Name);
        Assert.Equal("CursorClick", _tool.Icon);
        Assert.Equal("V", _tool.Shortcut);
        Assert.Equal(ToolCursor.Arrow, _tool.Cursor);
    }

    [Fact]
    public void MouseDown_OnElement_SelectsElement()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50, Name = "TestRect" };
        _document.Elements.Add(rect);

        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);

        Assert.Single(_tool.SelectedElements);
        Assert.Same(rect, _tool.SelectedElements[0]);
    }

    [Fact]
    public void MouseDown_OnEmpty_ClearsSelection()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        // Select the rect
        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(25, 25), KeyModifiers.None);

        // Click on empty space
        _tool.OnMouseDown(new ToolPoint(200, 200), KeyModifiers.None);

        Assert.Empty(_tool.SelectedElements);
    }

    [Fact]
    public void MouseDown_WithShift_AddsToSelection()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 30, Height = 30 };
        var rect2 = new SvgRect { X = 50, Y = 10, Width = 30, Height = 30 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        // Select first rect
        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(25, 25), KeyModifiers.None);

        // Shift+click second rect
        _tool.OnMouseDown(new ToolPoint(65, 25), KeyModifiers.Shift);

        Assert.Equal(2, _tool.SelectedElements.Count);
    }

    [Fact]
    public void MouseDown_WithCtrl_TogglesSelection()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        // Select the rect
        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(25, 25), KeyModifiers.None);
        Assert.Single(_tool.SelectedElements);

        // Ctrl+click to deselect
        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.Control);

        Assert.Empty(_tool.SelectedElements);
    }

    [Fact]
    public void ClearSelection_ClearsAllSelected()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        _tool.ClearSelection();

        Assert.Empty(_tool.SelectedElements);
    }

    [Fact]
    public void SelectAll_SelectsAllElements()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 30, Height = 30 };
        var rect2 = new SvgRect { X = 50, Y = 10, Width = 30, Height = 30 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        _tool.SelectAll();

        Assert.Equal(2, _tool.SelectedElements.Count);
    }

    [Fact]
    public void DeleteSelected_RemovesSelectedElements()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        _tool.DeleteSelected();

        Assert.Empty(_document.Elements);
        Assert.Empty(_tool.SelectedElements);
    }

    [Fact]
    public void KeyDown_Delete_DeletesSelection()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        var handled = _tool.OnKeyDown("Delete", KeyModifiers.None);

        Assert.True(handled);
        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void KeyDown_Escape_ClearsSelection()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);
        var handled = _tool.OnKeyDown("Escape", KeyModifiers.None);

        Assert.True(handled);
        Assert.Empty(_tool.SelectedElements);
    }

    [Fact]
    public void KeyDown_CtrlA_SelectsAll()
    {
        var rect1 = new SvgRect { X = 10, Y = 10, Width = 30, Height = 30 };
        var rect2 = new SvgRect { X = 50, Y = 10, Width = 30, Height = 30 };
        _document.Elements.Add(rect1);
        _document.Elements.Add(rect2);

        var handled = _tool.OnKeyDown("A", KeyModifiers.Control);

        Assert.True(handled);
        Assert.Equal(2, _tool.SelectedElements.Count);
    }

    [Fact]
    public void SelectionChanged_EventRaised()
    {
        var rect = new SvgRect { X = 10, Y = 10, Width = 50, Height = 50 };
        _document.Elements.Add(rect);

        var eventRaised = false;
        _tool.SelectionChanged += (_, _) => eventRaised = true;

        _tool.OnMouseDown(new ToolPoint(25, 25), KeyModifiers.None);

        Assert.True(eventRaised);
    }
}

public class PanToolTests
{
    [Fact]
    public void Properties_AreCorrect()
    {
        var tool = new PanTool();

        Assert.Equal("Pan", tool.Name);
        Assert.Equal("HandLeft", tool.Icon);
        Assert.Equal("H", tool.Shortcut);
        Assert.Equal(ToolCursor.Hand, tool.Cursor);
    }

    [Fact]
    public void MouseDrag_RaisesPanDeltaEvent()
    {
        var tool = new PanTool();
        (double DeltaX, double DeltaY)? delta = null;
        tool.PanDelta += (_, d) => delta = d;

        tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        tool.OnMouseMove(new ToolPoint(150, 120), KeyModifiers.None);

        Assert.NotNull(delta);
        Assert.Equal(50, delta.Value.DeltaX);
        Assert.Equal(20, delta.Value.DeltaY);
    }
}

public class ZoomToolTests
{
    [Fact]
    public void Properties_AreCorrect()
    {
        var tool = new ZoomTool();

        Assert.Equal("Zoom", tool.Name);
        Assert.Equal("ZoomIn", tool.Icon);
        Assert.Equal("Z", tool.Shortcut);
        Assert.Equal(ToolCursor.ZoomIn, tool.Cursor);
    }

    [Fact]
    public void Click_RaisesZoomRequestedEvent()
    {
        var tool = new ZoomTool();
        (double CenterX, double CenterY, double Factor)? zoom = null;
        tool.ZoomRequested += (_, z) => zoom = z;

        tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.NotNull(zoom);
        Assert.Equal(100, zoom.Value.CenterX);
        Assert.Equal(100, zoom.Value.CenterY);
        Assert.Equal(2.0, zoom.Value.Factor);
    }

    [Fact]
    public void AltClick_ZoomsOut()
    {
        var tool = new ZoomTool();
        (double CenterX, double CenterY, double Factor)? zoom = null;
        tool.ZoomRequested += (_, z) => zoom = z;

        tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.Alt);
        tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.Alt);

        Assert.NotNull(zoom);
        Assert.Equal(0.5, zoom.Value.Factor);
    }

    [Fact]
    public void DragArea_RaisesZoomToAreaEvent()
    {
        var tool = new ZoomTool();
        (double X, double Y, double Width, double Height)? area = null;
        tool.ZoomToAreaRequested += (_, a) => area = a;

        tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        tool.OnMouseMove(new ToolPoint(200, 150), KeyModifiers.None);
        tool.OnMouseUp(new ToolPoint(200, 150), KeyModifiers.None);

        Assert.NotNull(area);
        Assert.Equal(100, area.Value.X);
        Assert.Equal(100, area.Value.Y);
        Assert.Equal(100, area.Value.Width);
        Assert.Equal(50, area.Value.Height);
    }
}
