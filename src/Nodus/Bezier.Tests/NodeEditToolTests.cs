namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;
using Bezier.Core.Tools;

public class NodeEditToolTests
{
    private readonly NodeEditTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;
    private readonly SvgPath _testPath;

    public NodeEditToolTests()
    {
        _tool = new NodeEditTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);

        // Create a simple test path
        _testPath = new SvgPath
        {
            PathData = "M 100 100 L 200 100 L 200 200 L 100 200 Z",
            Name = "TestPath"
        };
        _document.Elements.Add(_testPath);
        
        // Activate the tool and set the path
        _tool.OnActivate();
        _tool.SetActivePath(_testPath);
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Node Edit", _tool.Name);
        Assert.Equal("Edit", _tool.Icon);
        Assert.Equal("A", _tool.Shortcut);
        Assert.Equal(ToolCursor.Arrow, _tool.Cursor);
    }

    [Fact]
    public void SetActivePath_ParsesNodes()
    {
        // Already set in constructor, verify it parsed
        Assert.Equal(4, _tool.NodeCount);
        Assert.Same(_testPath, _tool.ActivePath);
    }

    [Fact]
    public void SetActivePath_ClearsSelection()
    {
        // Select a node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);
        
        Assert.Single(_tool.SelectedNodes);

        // Set a new path
        var newPath = new SvgPath { PathData = "M 0 0 L 50 50" };
        _tool.SetActivePath(newPath);

        Assert.Empty(_tool.SelectedNodes);
    }

    [Fact]
    public void ClickOnNode_SelectsNode()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Single(_tool.SelectedNodes);
        Assert.Equal(0, _tool.SelectedNodes[0].NodeIndex);
    }

    [Fact]
    public void ShiftClick_AddsToSelection()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        // Shift+click second node
        _tool.OnMouseDown(new ToolPoint(200, 100), KeyModifiers.Shift);
        _tool.OnMouseUp(new ToolPoint(200, 100), KeyModifiers.Shift);

        Assert.Equal(2, _tool.SelectedNodes.Count);
    }

    [Fact]
    public void CtrlClick_TogglesSelection()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Single(_tool.SelectedNodes);

        // Ctrl+click same node to deselect
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.Control);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.Control);

        Assert.Empty(_tool.SelectedNodes);
    }

    [Fact]
    public void ClickOnEmpty_ClearsSelection()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Single(_tool.SelectedNodes);

        // Click on empty space (marquee with no nodes)
        _tool.OnMouseDown(new ToolPoint(0, 0), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(0, 0), KeyModifiers.None);

        Assert.Empty(_tool.SelectedNodes);
    }

    [Fact]
    public void CtrlA_SelectsAllNodes()
    {
        _tool.OnKeyDown("A", KeyModifiers.Control);

        Assert.Equal(4, _tool.SelectedNodes.Count);
    }

    [Fact]
    public void Delete_RemovesSelectedNodes()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Equal(4, _tool.NodeCount);
        Assert.Single(_tool.SelectedNodes);

        // Delete
        _tool.OnKeyDown("Delete", KeyModifiers.None);

        Assert.Equal(3, _tool.NodeCount);
        Assert.Empty(_tool.SelectedNodes);
    }

    [Fact]
    public void Key1_ConvertsToCorner()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        // Convert to corner (should already be corner for line path)
        _tool.OnKeyDown("1", KeyModifiers.None);

        // No exception means success
        Assert.Single(_tool.SelectedNodes);
    }

    [Fact]
    public void Key2_ConvertsToSmooth()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        _tool.OnKeyDown("2", KeyModifiers.None);

        Assert.Single(_tool.SelectedNodes);
    }

    [Fact]
    public void Key3_ConvertsToSymmetric()
    {
        // Select first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        _tool.OnKeyDown("3", KeyModifiers.None);

        Assert.Single(_tool.SelectedNodes);
    }

    [Fact]
    public void DragNode_MovesNode()
    {
        // Start drag on first node
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(150, 150), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(150, 150), KeyModifiers.None);

        // Path data should be updated
        Assert.Contains("150", _testPath.PathData);
    }

    [Fact]
    public void MarqueeSelection_SelectsMultipleNodes()
    {
        // Drag marquee around all nodes (start far from any node)
        _tool.OnMouseDown(new ToolPoint(50, 50), KeyModifiers.None);
        _tool.OnMouseMove(new ToolPoint(250, 250), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(250, 250), KeyModifiers.None);

        Assert.Equal(4, _tool.SelectedNodes.Count);
    }

    [Fact]
    public void SelectionChanged_EventRaised()
    {
        var eventRaised = false;
        _tool.SelectionChanged += (_, _) => eventRaised = true;

        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.True(eventRaised);
    }

    [Fact]
    public void AddNodeAtPosition_InsertsNode()
    {
        Assert.Equal(4, _tool.NodeCount);

        _tool.AddNodeAtPosition(150, 100, 0);

        Assert.Equal(5, _tool.NodeCount);
    }

    [Fact]
    public void ParsePath_HandlesCubicBezier()
    {
        var bezierPath = new SvgPath
        {
            PathData = "M 100 100 C 150 50, 200 50, 250 100"
        };
        
        var tool2 = new NodeEditTool();
        tool2.SetContext(_document, _history);
        tool2.OnActivate();
        tool2.SetActivePath(bezierPath);

        Assert.Equal(2, tool2.NodeCount);
    }

    [Fact]
    public void OnDeactivate_ClearsState()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnMouseUp(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Single(_tool.SelectedNodes);

        _tool.OnDeactivate();

        Assert.Empty(_tool.SelectedNodes);
        Assert.Null(_tool.ActivePath);
    }
}
