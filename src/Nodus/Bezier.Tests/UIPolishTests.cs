namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Services;

public class ToolOptionsTests
{
    [Fact]
    public void NumericToolOption_SetValue_ClampsToRange()
    {
        var option = new NumericToolOption
        {
            Id = "test",
            Name = "Test",
            Minimum = 0,
            Maximum = 100,
            Value = 50
        };

        option.SetValue(150);
        Assert.Equal(100, option.Value);

        option.SetValue(-50);
        Assert.Equal(0, option.Value);
    }

    [Fact]
    public void NumericToolOption_SetValue_RaisesEvent()
    {
        var option = new NumericToolOption
        {
            Id = "test",
            Name = "Test",
            Minimum = 0,
            Maximum = 100
        };

        double? changedValue = null;
        option.ValueChanged += (_, v) => changedValue = v;

        option.SetValue(75);

        Assert.Equal(75, changedValue);
    }

    [Fact]
    public void ToggleToolOption_SetChecked_RaisesEvent()
    {
        var option = new ToggleToolOption
        {
            Id = "test",
            Name = "Test"
        };

        bool? changedValue = null;
        option.CheckedChanged += (_, v) => changedValue = v;

        option.SetChecked(true);

        Assert.True(changedValue);
        Assert.True(option.IsChecked);
    }

    [Fact]
    public void DropdownToolOption_SetSelectedIndex_RaisesEvent()
    {
        var option = new DropdownToolOption
        {
            Id = "test",
            Name = "Test",
            Items = ["Option 1", "Option 2", "Option 3"]
        };

        int? changedIndex = null;
        option.SelectionChanged += (_, v) => changedIndex = v;

        option.SetSelectedIndex(1);

        Assert.Equal(1, changedIndex);
        Assert.Equal("Option 2", option.SelectedItem);
    }

    [Fact]
    public void DropdownToolOption_SetSelectedIndex_IgnoresInvalidIndex()
    {
        var option = new DropdownToolOption
        {
            Id = "test",
            Name = "Test",
            Items = ["Option 1", "Option 2"],
            SelectedIndex = 0
        };

        option.SetSelectedIndex(5);

        Assert.Equal(0, option.SelectedIndex);
    }

    [Fact]
    public void ColorToolOption_SetColor_RaisesEvent()
    {
        var option = new ColorToolOption
        {
            Id = "test",
            Name = "Test",
            Color = 0xFF000000
        };

        uint? changedColor = null;
        option.ColorChanged += (_, v) => changedColor = v;

        option.SetColor(0xFFFF0000);

        Assert.Equal(0xFFFF0000u, changedColor);
        Assert.Equal(0xFFFF0000u, option.Color);
    }
}

public class CanvasTooltipServiceTests
{
    private readonly CanvasTooltipService _service;

    public CanvasTooltipServiceTests()
    {
        _service = new CanvasTooltipService();
    }

    [Fact]
    public void ShowDimensions_CreatesTooltip()
    {
        _service.ShowDimensions(100, 100, 50, 30);

        Assert.NotNull(_service.ActiveTooltip);
        Assert.Equal(TooltipType.Dimensions, _service.ActiveTooltip!.Type);
        Assert.Contains("50", _service.ActiveTooltip.Text);
        Assert.Contains("30", _service.ActiveTooltip.Text);
    }

    [Fact]
    public void ShowAngle_CreatesTooltip()
    {
        _service.ShowAngle(100, 100, 45);

        Assert.NotNull(_service.ActiveTooltip);
        Assert.Equal(TooltipType.Angle, _service.ActiveTooltip!.Type);
        Assert.Contains("45", _service.ActiveTooltip.Text);
    }

    [Fact]
    public void ShowDistance_CreatesTooltip()
    {
        _service.ShowDistance(100, 100, 75);

        Assert.NotNull(_service.ActiveTooltip);
        Assert.Equal(TooltipType.Distance, _service.ActiveTooltip!.Type);
        Assert.Contains("75", _service.ActiveTooltip.Text);
        Assert.Contains("px", _service.ActiveTooltip.Text);
    }

    [Fact]
    public void ShowPosition_CreatesTooltip()
    {
        _service.ShowPosition(150, 200);

        Assert.NotNull(_service.ActiveTooltip);
        Assert.Equal(TooltipType.Position, _service.ActiveTooltip!.Type);
        Assert.Contains("150", _service.ActiveTooltip.Text);
        Assert.Contains("200", _service.ActiveTooltip.Text);
    }

    [Fact]
    public void Hide_ClearsTooltip()
    {
        _service.ShowDimensions(100, 100, 50, 30);
        Assert.NotNull(_service.ActiveTooltip);

        _service.Hide();

        Assert.Null(_service.ActiveTooltip);
    }

    [Fact]
    public void TooltipChanged_EventRaised()
    {
        CanvasTooltip? received = null;
        _service.TooltipChanged += (_, t) => received = t;

        _service.ShowDimensions(100, 100, 50, 30);

        Assert.NotNull(received);
    }

    [Fact]
    public void WhenDisabled_DoesNotShowTooltip()
    {
        _service.IsEnabled = false;

        _service.ShowDimensions(100, 100, 50, 30);

        Assert.Null(_service.ActiveTooltip);
    }

    [Fact]
    public void CalculateAngle_ReturnsCorrectAngle()
    {
        var angle = CanvasTooltipService.CalculateAngle(0, 0, 1, 0);
        Assert.Equal(0, angle, 0.001);

        angle = CanvasTooltipService.CalculateAngle(0, 0, 0, 1);
        Assert.Equal(90, angle, 0.001);

        angle = CanvasTooltipService.CalculateAngle(0, 0, -1, 0);
        Assert.Equal(180, angle, 0.001);
    }

    [Fact]
    public void CalculateDistance_ReturnsCorrectDistance()
    {
        var distance = CanvasTooltipService.CalculateDistance(0, 0, 3, 4);
        Assert.Equal(5, distance, 0.001);

        distance = CanvasTooltipService.CalculateDistance(0, 0, 10, 0);
        Assert.Equal(10, distance, 0.001);
    }
}

public class VisualFeedbackServiceTests
{
    private readonly VisualFeedbackService _service;

    public VisualFeedbackServiceTests()
    {
        _service = new VisualFeedbackService();
    }

    [Fact]
    public void ShowSnapLine_AddsIndicator()
    {
        _service.ShowSnapLine(0, 0, 100, 100);

        Assert.Single(_service.ActiveIndicators);
        Assert.Equal(FeedbackType.SnapLine, _service.ActiveIndicators[0].Type);
    }

    [Fact]
    public void ShowVerticalSnapLine_AddsVerticalLine()
    {
        _service.ShowVerticalSnapLine(50, 0, 100);

        Assert.Single(_service.ActiveIndicators);
        var indicator = _service.ActiveIndicators[0];
        Assert.Equal(50, indicator.X1);
        Assert.Equal(50, indicator.X2);
    }

    [Fact]
    public void ShowHorizontalSnapLine_AddsHorizontalLine()
    {
        _service.ShowHorizontalSnapLine(50, 0, 100);

        Assert.Single(_service.ActiveIndicators);
        var indicator = _service.ActiveIndicators[0];
        Assert.Equal(50, indicator.Y1);
        Assert.Equal(50, indicator.Y2);
    }

    [Fact]
    public void ShowAlignmentGuide_AddsIndicator()
    {
        _service.ShowAlignmentGuide(0, 0, 100, 100);

        Assert.Single(_service.ActiveIndicators);
        Assert.Equal(FeedbackType.AlignmentGuide, _service.ActiveIndicators[0].Type);
    }

    [Fact]
    public void ShowSelectionHighlight_AddsIndicator()
    {
        _service.ShowSelectionHighlight(10, 10, 50, 50);

        Assert.Single(_service.ActiveIndicators);
        Assert.Equal(FeedbackType.SelectionHighlight, _service.ActiveIndicators[0].Type);
    }

    [Fact]
    public void Clear_RemovesAllIndicators()
    {
        _service.ShowSnapLine(0, 0, 100, 100);
        _service.ShowAlignmentGuide(0, 0, 50, 50);

        _service.Clear();

        Assert.Empty(_service.ActiveIndicators);
    }

    [Fact]
    public void ClearByType_RemovesOnlyThatType()
    {
        _service.ShowSnapLine(0, 0, 100, 100);
        _service.ShowAlignmentGuide(0, 0, 50, 50);

        _service.Clear(FeedbackType.SnapLine);

        Assert.Single(_service.ActiveIndicators);
        Assert.Equal(FeedbackType.AlignmentGuide, _service.ActiveIndicators[0].Type);
    }

    [Fact]
    public void IndicatorsChanged_EventRaised()
    {
        var raised = false;
        _service.IndicatorsChanged += (_, _) => raised = true;

        _service.ShowSnapLine(0, 0, 100, 100);

        Assert.True(raised);
    }

    [Fact]
    public void WhenDisabled_DoesNotAddIndicator()
    {
        _service.IsEnabled = false;

        _service.ShowSnapLine(0, 0, 100, 100);

        Assert.Empty(_service.ActiveIndicators);
    }

    [Fact]
    public void GetIndicatorOpacity_ReturnsValueBetweenZeroAndOne()
    {
        _service.ShowSnapLine(0, 0, 100, 100);
        var indicator = _service.ActiveIndicators[0];

        var opacity = _service.GetIndicatorOpacity(indicator);

        Assert.InRange(opacity, 0, 1);
    }
}
