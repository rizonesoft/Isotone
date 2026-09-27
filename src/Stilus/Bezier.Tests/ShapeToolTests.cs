namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Services;
using Bezier.Core.Tools;

public class RectangleToolTests
{
    private readonly RectangleTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;

    public RectangleToolTests()
    {
        _tool = new RectangleTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Rectangle", _tool.Name);
        Assert.Equal("Square", _tool.Icon);
        Assert.Equal("R", _tool.Shortcut);
        Assert.Equal(ToolCursor.Cross, _tool.Cursor);
    }

    [Fact]
    public void MouseDrag_CreatesRectangle()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        var rect = _document.Elements[0] as Bezier.Core.Models.Elements.SvgRect;
        Assert.NotNull(rect);
        Assert.Equal(10, rect.X);
        Assert.Equal(10, rect.Y);
        Assert.Equal(100, rect.Width);
        Assert.Equal(50, rect.Height);
    }

    [Fact]
    public void ShiftModifier_CreatesSquare()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.Shift);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.Shift);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.Shift);

        Assert.Single(_document.Elements);
        var rect = _document.Elements[0] as Bezier.Core.Models.Elements.SvgRect;
        Assert.NotNull(rect);
        Assert.Equal(rect.Width, rect.Height); // Square
    }

    [Fact]
    public void AltModifier_DrawsFromCenter()
    {
        _tool.OnMouseDown(new ToolPoint(50, 50), KeyModifiers.Alt);
        _tool.OnMouseMove(new ToolPoint(100, 75), KeyModifiers.Alt);
        _tool.OnMouseUp(new ToolPoint(100, 75), KeyModifiers.Alt);

        Assert.Single(_document.Elements);
        var rect = _document.Elements[0] as Bezier.Core.Models.Elements.SvgRect;
        Assert.NotNull(rect);
        // Center should be at (50, 50), dimensions doubled
        Assert.Equal(0, rect.X); // 50 - 50 = 0
        Assert.Equal(25, rect.Y); // 50 - 25 = 25
        Assert.Equal(100, rect.Width); // (100-50)*2 = 100
        Assert.Equal(50, rect.Height); // (75-50)*2 = 50
    }

    [Fact]
    public void SmallDrag_DoesNotCreateRectangle()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(10.5, 10.5), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(10.5, 10.5), KeyModifiers.None);

        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void DragUpLeft_CreatesValidRectangle()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(50, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(50, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        var rect = _document.Elements[0] as Bezier.Core.Models.Elements.SvgRect;
        Assert.NotNull(rect);
        Assert.Equal(50, rect.X);
        Assert.Equal(60, rect.Y);
        Assert.Equal(50, rect.Width);
        Assert.Equal(40, rect.Height);
    }

    [Fact]
    public void Creation_IsUndoable()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        
        _history.Undo();
        
        Assert.Empty(_document.Elements);
    }
}

public class EllipseToolTests
{
    private readonly EllipseTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;

    public EllipseToolTests()
    {
        _tool = new EllipseTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Ellipse", _tool.Name);
        Assert.Equal("Circle", _tool.Icon);
        Assert.Equal("E", _tool.Shortcut);
        Assert.Equal(ToolCursor.Cross, _tool.Cursor);
    }

    [Fact]
    public void MouseDrag_CreatesEllipse()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        var ellipse = _document.Elements[0] as Bezier.Core.Models.Elements.SvgEllipse;
        Assert.NotNull(ellipse);
        Assert.Equal(50, ellipse.Rx); // (110-10)/2 = 50
        Assert.Equal(25, ellipse.Ry); // (60-10)/2 = 25
    }

    [Fact]
    public void ShiftModifier_CreatesCircle()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.Shift);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.Shift);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.Shift);

        Assert.Single(_document.Elements);
        var ellipse = _document.Elements[0] as Bezier.Core.Models.Elements.SvgEllipse;
        Assert.NotNull(ellipse);
        Assert.Equal(ellipse.Rx, ellipse.Ry); // Circle
    }

    [Fact]
    public void SmallDrag_DoesNotCreateEllipse()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(10.5, 10.5), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(10.5, 10.5), KeyModifiers.None);

        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void Creation_IsUndoable()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        
        _history.Undo();
        
        Assert.Empty(_document.Elements);
    }
}

public class LineToolTests
{
    private readonly LineTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;

    public LineToolTests()
    {
        _tool = new LineTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Line", _tool.Name);
        Assert.Equal("LineHorizontal1", _tool.Icon);
        Assert.Equal("L", _tool.Shortcut);
        Assert.Equal(ToolCursor.Cross, _tool.Cursor);
    }

    [Fact]
    public void MouseDrag_CreatesLine()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        var line = _document.Elements[0] as Bezier.Core.Models.Elements.SvgLine;
        Assert.NotNull(line);
        Assert.Equal(10, line.X1);
        Assert.Equal(10, line.Y1);
        Assert.Equal(110, line.X2);
        Assert.Equal(60, line.Y2);
    }

    [Fact]
    public void ShiftModifier_SnapsTo45Degrees()
    {
        _tool.OnMouseDown(new ToolPoint(0, 0), KeyModifiers.Shift);
        _tool.OnMouseMove(new ToolPoint(100, 10), KeyModifiers.Shift); // Almost horizontal
        _tool.OnMouseUp(new ToolPoint(100, 10), KeyModifiers.Shift);

        Assert.Single(_document.Elements);
        var line = _document.Elements[0] as Bezier.Core.Models.Elements.SvgLine;
        Assert.NotNull(line);
        // Should snap to horizontal (0°)
        Assert.Equal(0, line.Y2, 5); // Y2 should be ~0
    }

    [Fact]
    public void ShiftModifier_SnapsToDiagonal()
    {
        _tool.OnMouseDown(new ToolPoint(0, 0), KeyModifiers.Shift);
        _tool.OnMouseMove(new ToolPoint(100, 95), KeyModifiers.Shift); // Almost 45°
        _tool.OnMouseUp(new ToolPoint(100, 95), KeyModifiers.Shift);

        Assert.Single(_document.Elements);
        var line = _document.Elements[0] as Bezier.Core.Models.Elements.SvgLine;
        Assert.NotNull(line);
        // Should snap to 45°, so X2 ≈ Y2
        Assert.Equal(line.X2, line.Y2, 5);
    }

    [Fact]
    public void SmallDrag_DoesNotCreateLine()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(10.5, 10.5), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(10.5, 10.5), KeyModifiers.None);

        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void Creation_IsUndoable()
    {
        _tool.OnMouseDown(new ToolPoint(10, 10), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(110, 60), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(110, 60), KeyModifiers.None);

        Assert.Single(_document.Elements);
        
        _history.Undo();
        
        Assert.Empty(_document.Elements);
    }
}
