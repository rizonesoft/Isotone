namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class SelectionInfoTests
{
    [Fact]
    public void SelectionInfo_DefaultValues()
    {
        var info = new SelectionInfo();

        Assert.Equal(0, info.Count);
        Assert.Equal("Nothing", info.ElementType);
        Assert.False(info.HasSelection);
        Assert.Equal("Nothing selected", info.Summary);
    }

    [Fact]
    public void SelectionInfo_Clear_ResetsValues()
    {
        var info = new SelectionInfo { Count = 5, ElementType = "Rectangle" };

        info.Clear();

        Assert.Equal(0, info.Count);
        Assert.False(info.HasSelection);
    }

    [Fact]
    public void SelectionInfo_UpdateFromElement_SetsSingleSelection()
    {
        var info = new SelectionInfo();
        var element = new SvgRect { X = 10, Y = 20, Width = 100, Height = 50 };

        info.UpdateFromElement(element);

        Assert.Equal(1, info.Count);
        Assert.Equal("Rect", info.ElementType);
        Assert.Equal(10, info.X);
        Assert.Equal(20, info.Y);
        Assert.Equal(100, info.Width);
        Assert.Equal(50, info.Height);
    }

    [Fact]
    public void SelectionInfo_UpdateFromElements_SetsMultipleSelection()
    {
        var info = new SelectionInfo();
        var elements = new VectorElement[]
        {
            new SvgRect { X = 0, Y = 0, Width = 50, Height = 50 },
            new SvgRect { X = 100, Y = 100, Width = 50, Height = 50 }
        };

        info.UpdateFromElements(elements);

        Assert.Equal(2, info.Count);
        Assert.Equal("2 objects", info.Summary);
        Assert.Equal(0, info.X);
        Assert.Equal(0, info.Y);
        Assert.Equal(150, info.Width);
        Assert.Equal(150, info.Height);
    }

    [Fact]
    public void SelectionInfo_UpdateFromElements_Empty_Clears()
    {
        var info = new SelectionInfo { Count = 5 };

        info.UpdateFromElements([]);

        Assert.Equal(0, info.Count);
        Assert.False(info.HasSelection);
    }

    [Fact]
    public void SelectionInfo_PositionText_FormatsCorrectly()
    {
        var info = new SelectionInfo { X = 10, Y = 20 };

        Assert.Contains("X:", info.PositionText);
        Assert.Contains("Y:", info.PositionText);
    }

    [Fact]
    public void SelectionInfo_DimensionsText_FormatsCorrectly()
    {
        var info = new SelectionInfo { Width = 100, Height = 50 };

        Assert.Contains("W:", info.DimensionsText);
        Assert.Contains("H:", info.DimensionsText);
    }

    [Fact]
    public void SelectionInfo_RotationText_FormatsCorrectly()
    {
        var info = new SelectionInfo { Rotation = 45 };

        Assert.Contains("45", info.RotationText);
        Assert.Contains("°", info.RotationText);
    }

    [Fact]
    public void SelectionInfo_Summary_ShowsMixedForDifferentTypes()
    {
        var info = new SelectionInfo();
        var elements = new VectorElement[]
        {
            new SvgRect { X = 0, Y = 0, Width = 50, Height = 50 },
            new SvgEllipse { Cx = 100, Cy = 100, Rx = 25, Ry = 25 }
        };

        info.UpdateFromElements(elements);

        Assert.Equal("Mixed", info.ElementType);
    }
}

public class ElementTooltipTests
{
    [Fact]
    public void ElementTooltip_FromElement_CreatesCorrectTooltip()
    {
        var element = new SvgRect { Name = "MyRect", X = 0, Y = 0, Width = 100, Height = 50 };

        var tooltip = ElementTooltip.FromElement(element, 150, 200);

        Assert.Equal("Rect", tooltip.Type);
        Assert.Equal("MyRect", tooltip.Name);
        Assert.Equal("100 × 50", tooltip.Dimensions);
        Assert.Equal(165, tooltip.X);
        Assert.Equal(215, tooltip.Y);
        Assert.True(tooltip.IsVisible);
    }

    [Fact]
    public void ElementTooltip_FromElement_UsesUnnamedForNullName()
    {
        var element = new SvgRect { Name = null };

        var tooltip = ElementTooltip.FromElement(element, 0, 0);

        Assert.Equal("Unnamed", tooltip.Name);
    }
}

public class CanvasHUDServiceTests
{
    private readonly CanvasHUDService _service;

    public CanvasHUDServiceTests()
    {
        _service = new CanvasHUDService();
    }

    [Fact]
    public void CanvasHUDService_DefaultValues()
    {
        Assert.True(_service.ShowContextualToolbar);
        Assert.True(_service.ShowSelectionInfo);
        Assert.True(_service.ShowZoomIndicator);
        Assert.True(_service.ShowRulerCursor);
        Assert.False(_service.ShowDistanceIndicators);
        Assert.Equal(1.0, _service.ZoomLevel);
    }

    [Fact]
    public void CanvasHUDService_ZoomText_FormatsCorrectly()
    {
        _service.ZoomLevel = 1.5;

        Assert.Equal("150%", _service.ZoomText);
    }

    [Fact]
    public void CanvasHUDService_CursorText_FormatsCorrectly()
    {
        _service.CursorPosition = (100, 200);

        Assert.Contains("100", _service.CursorText);
        Assert.Contains("200", _service.CursorText);
    }

    [Fact]
    public void CanvasHUDService_RegisterDefaultActions_AddsActions()
    {
        _service.RegisterDefaultActions();

        Assert.True(_service.QuickActions.Count > 0);
        Assert.Contains(_service.QuickActions, a => a.Id == "group");
        Assert.Contains(_service.QuickActions, a => a.Id == "ungroup");
        Assert.Contains(_service.QuickActions, a => a.Id == "delete");
    }

    [Fact]
    public void CanvasHUDService_UpdateSelection_UpdatesSelectionInfo()
    {
        var elements = new[] { new SvgRect { X = 10, Y = 20, Width = 100, Height = 50 } };

        _service.UpdateSelection(elements);

        Assert.Equal(1, _service.Selection.Count);
        Assert.NotNull(_service.SelectionBounds);
    }

    [Fact]
    public void CanvasHUDService_UpdateSelection_Empty_ClearsSelection()
    {
        _service.UpdateSelection([new SvgRect()]);
        _service.UpdateSelection([]);

        Assert.Equal(0, _service.Selection.Count);
        Assert.Null(_service.SelectionBounds);
    }

    [Fact]
    public void CanvasHUDService_ShowTooltip_SetsTooltip()
    {
        var element = new SvgRect { Name = "Test" };

        _service.ShowTooltip(element, 100, 100);

        Assert.NotNull(_service.Tooltip);
        Assert.Equal("Test", _service.Tooltip.Name);
    }

    [Fact]
    public void CanvasHUDService_HideTooltip_ClearsTooltip()
    {
        var element = new SvgRect { Name = "Test" };
        _service.ShowTooltip(element, 100, 100);

        _service.HideTooltip();

        Assert.Null(_service.Tooltip);
    }

    [Fact]
    public void CanvasHUDService_ToolbarPosition_CentersAboveSelection()
    {
        _service.SelectionBounds = (100, 200, 100, 50);

        var pos = _service.ToolbarPosition;

        Assert.Equal(150, pos.X); // Centered on selection
        Assert.Equal(160, pos.Y); // Above selection
    }

    [Fact]
    public void CanvasHUDService_CalculateToolbarPosition_StaysOnScreen()
    {
        _service.SelectionBounds = (0, 10, 50, 50);

        var pos = _service.CalculateToolbarPosition(800, 600, 200, 40);

        Assert.True(pos.X >= 10); // Left margin
        Assert.True(pos.Y >= 10); // Top margin
    }

    [Fact]
    public void CanvasHUDService_CalculateToolbarPosition_MovesBelow_WhenNoSpaceAbove()
    {
        _service.SelectionBounds = (100, 5, 100, 50); // Very close to top

        var pos = _service.CalculateToolbarPosition(800, 600, 200, 40);

        Assert.True(pos.Y > 5); // Should be below selection
    }

    [Fact]
    public void CanvasHUDService_HUDChanged_EventRaised()
    {
        var raised = false;
        _service.HUDChanged += (_, _) => raised = true;

        _service.UpdateSelection([new SvgRect()]);

        Assert.True(raised);
    }
}

public class DistanceIndicatorTests
{
    [Fact]
    public void DistanceIndicator_LabelPosition_ReturnsCenter()
    {
        var indicator = new DistanceIndicator
        {
            StartX = 0,
            StartY = 50,
            EndX = 100,
            EndY = 50
        };

        var pos = indicator.LabelPosition;

        Assert.Equal(50, pos.X);
        Assert.Equal(50, pos.Y);
    }

    [Fact]
    public void DistanceIndicator_DistanceText_FormatsCorrectly()
    {
        var indicator = new DistanceIndicator { Distance = 123.456 };

        Assert.Equal("123", indicator.DistanceText);
    }
}

public class HUDActionTests
{
    [Fact]
    public void HUDAction_CreatesCorrectly()
    {
        var action = new HUDAction("test", "Test Action", "icon", "Tooltip");

        Assert.Equal("test", action.Id);
        Assert.Equal("Test Action", action.Name);
        Assert.Equal("icon", action.Icon);
        Assert.Equal("Tooltip", action.Tooltip);
    }

    [Fact]
    public void HUDAction_Execute_CallsAction()
    {
        var executed = false;
        var action = new HUDAction("test", "Test", Execute: () => executed = true);

        action.Execute?.Invoke();

        Assert.True(executed);
    }

    [Fact]
    public void HUDAction_CanExecute_ReturnsValue()
    {
        var canExecute = true;
        var action = new HUDAction("test", "Test", CanExecute: () => canExecute);

        Assert.True(action.CanExecute?.Invoke() ?? false);

        canExecute = false;
        Assert.False(action.CanExecute?.Invoke() ?? true);
    }
}

public class DistanceCalculationTests
{
    private readonly CanvasHUDService _service;

    public DistanceCalculationTests()
    {
        _service = new CanvasHUDService();
    }

    [Fact]
    public void CalculateDistances_ReturnsEmpty_WhenNoSelection()
    {
        var elements = new[] { new SvgRect { X = 0, Y = 0, Width = 50, Height = 50 } };

        var distances = _service.CalculateDistances(elements, []).ToList();

        Assert.Empty(distances);
    }

    [Fact]
    public void CalculateDistances_ReturnsEmpty_WhenDistanceIndicatorsDisabled()
    {
        _service.ShowDistanceIndicators = false;
        _service.SelectionBounds = (0, 0, 50, 50);
        var selected = new[] { new SvgRect { X = 0, Y = 0, Width = 50, Height = 50 } };
        var others = new[] { new SvgRect { X = 100, Y = 0, Width = 50, Height = 50 } };

        var distances = _service.CalculateDistances(others, selected).ToList();

        Assert.Empty(distances);
    }

    [Fact]
    public void CalculateDistances_FindsHorizontalDistance()
    {
        _service.ShowDistanceIndicators = true;
        _service.SelectionBounds = (0, 0, 50, 50);
        var selected = new[] { new SvgRect { X = 0, Y = 0, Width = 50, Height = 50 } };
        var others = new[] { new SvgRect { X = 100, Y = 0, Width = 50, Height = 50 } };

        var distances = _service.CalculateDistances(others, selected).ToList();

        Assert.Contains(distances, d => d.IsHorizontal && d.Distance == 50);
    }
}
