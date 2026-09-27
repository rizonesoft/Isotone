namespace Bezier.Tests;

using Bezier.Core.Services;

public class AnimationServiceTests
{
    private readonly AnimationService _service;

    public AnimationServiceTests()
    {
        _service = new AnimationService();
    }

    [Fact]
    public void Animate_CreatesAnimation()
    {
        var animation = _service.Animate(0, 100);

        Assert.NotNull(animation);
        Assert.Equal(0, animation.StartValue);
        Assert.Equal(100, animation.EndValue);
        Assert.True(_service.HasActiveAnimations);
    }

    [Fact]
    public void Animation_GetProgress_ReturnsZeroInitially()
    {
        var animation = _service.Animate(0, 100, 1000);

        var progress = animation.GetProgress();

        Assert.InRange(progress, 0, 0.1);
    }

    [Fact]
    public void Animation_GetCurrentValue_ReturnsStartInitially()
    {
        var animation = _service.Animate(0, 100, 1000);

        var value = animation.GetCurrentValue();

        Assert.InRange(value, 0, 10);
    }

    [Fact]
    public void Cancel_RemovesAnimation()
    {
        var animation = _service.Animate(0, 100);

        _service.Cancel(animation);

        Assert.False(_service.HasActiveAnimations);
    }

    [Fact]
    public void CancelAll_RemovesAllAnimations()
    {
        _service.Animate(0, 100);
        _service.Animate(0, 200);
        _service.Animate(0, 300);

        _service.CancelAll();

        Assert.False(_service.HasActiveAnimations);
    }

    [Theory]
    [InlineData(EasingFunction.Linear, 0.5, 0.5)]
    [InlineData(EasingFunction.Linear, 0, 0)]
    [InlineData(EasingFunction.Linear, 1, 1)]
    public void ApplyEasing_Linear_ReturnsCorrectValue(EasingFunction easing, double t, double expected)
    {
        var result = AnimationService.ApplyEasing(t, easing);

        Assert.Equal(expected, result, 0.001);
    }

    [Fact]
    public void ApplyEasing_EaseOutCubic_StartsSlowEndsFlat()
    {
        var start = AnimationService.ApplyEasing(0.1, EasingFunction.EaseOutCubic);
        var mid = AnimationService.ApplyEasing(0.5, EasingFunction.EaseOutCubic);
        var end = AnimationService.ApplyEasing(0.9, EasingFunction.EaseOutCubic);

        Assert.True(start > 0.1); // Faster at start
        Assert.True(mid > 0.5); // Still faster
        Assert.True(end > 0.9); // Slowing at end
    }

    [Fact]
    public void ApplyEasing_AllEasings_ReturnValidRange()
    {
        foreach (EasingFunction easing in Enum.GetValues<EasingFunction>())
        {
            var at0 = AnimationService.ApplyEasing(0, easing);
            var at1 = AnimationService.ApplyEasing(1, easing);

            Assert.InRange(at0, -0.5, 0.5); // Some back easings go negative
            Assert.InRange(at1, 0.5, 1.5); // Some elastic overshoots
        }
    }

    [Fact]
    public void LerpColor_InterpolatesCorrectly()
    {
        var black = 0xFF000000u;
        var white = 0xFFFFFFFFu;

        var mid = AnimationService.LerpColor(black, white, 0.5);

        var r = (byte)((mid >> 16) & 0xFF);
        var g = (byte)((mid >> 8) & 0xFF);
        var b = (byte)(mid & 0xFF);

        Assert.InRange(r, 125, 130);
        Assert.InRange(g, 125, 130);
        Assert.InRange(b, 125, 130);
    }

    [Fact]
    public void LerpColor_AtZero_ReturnsFromColor()
    {
        var from = 0xFFFF0000u;
        var to = 0xFF0000FFu;

        var result = AnimationService.LerpColor(from, to, 0);

        Assert.Equal(from, result);
    }

    [Fact]
    public void LerpColor_AtOne_ReturnsToColor()
    {
        var from = 0xFFFF0000u;
        var to = 0xFF0000FFu;

        var result = AnimationService.LerpColor(from, to, 1);

        Assert.Equal(to, result);
    }

    [Fact]
    public void Update_InvokesOnUpdateCallback()
    {
        var values = new List<double>();
        _service.Animate(0, 100, 10, onUpdate: v => values.Add(v));

        _service.Update();

        Assert.NotEmpty(values);
    }
}

public class PresetServiceTests
{
    [Fact]
    public void StrokeWidths_ContainsExpectedPresets()
    {
        Assert.True(PresetService.StrokeWidths.Length > 0);
        Assert.Contains(PresetService.StrokeWidths, p => p.Name == "Normal");
        Assert.Contains(PresetService.StrokeWidths, p => p.Name == "Thick");
    }

    [Fact]
    public void Opacities_ContainsExpectedPresets()
    {
        Assert.True(PresetService.Opacities.Length > 0);
        Assert.Contains(PresetService.Opacities, p => p.Value == 0);
        Assert.Contains(PresetService.Opacities, p => p.Value == 1);
    }

    [Fact]
    public void CornerRadii_ContainsExpectedPresets()
    {
        Assert.True(PresetService.CornerRadii.Length > 0);
        Assert.Contains(PresetService.CornerRadii, p => p.Name == "None");
        Assert.Contains(PresetService.CornerRadii, p => p.Name == "Pill");
    }

    [Fact]
    public void DashPatterns_ContainsExpectedPresets()
    {
        Assert.True(PresetService.DashPatterns.Length > 0);
        Assert.Contains(PresetService.DashPatterns, p => p.Name == "Solid");
        Assert.Contains(PresetService.DashPatterns, p => p.Name == "Dashed");
    }

    [Fact]
    public void Colors_ContainsExpectedPresets()
    {
        Assert.True(PresetService.Colors.Length > 0);
        Assert.Contains(PresetService.Colors, p => p.Name == "Black");
        Assert.Contains(PresetService.Colors, p => p.Name == "White");
    }

    [Fact]
    public void Colors_ContainsCatppuccinPresets()
    {
        var catppuccin = PresetService.GetByCategory(PresetService.Colors, "Catppuccin").ToList();

        Assert.True(catppuccin.Count > 0);
        Assert.Contains(catppuccin, p => p.Name == "Blue");
    }

    [Fact]
    public void FontSizes_ContainsExpectedPresets()
    {
        Assert.True(PresetService.FontSizes.Length > 0);
        Assert.Contains(PresetService.FontSizes, p => p.Name == "Normal");
    }

    [Fact]
    public void RotationAngles_ContainsExpectedPresets()
    {
        Assert.True(PresetService.RotationAngles.Length > 0);
        Assert.Contains(PresetService.RotationAngles, p => p.Value == 0);
        Assert.Contains(PresetService.RotationAngles, p => p.Value == 90);
        Assert.Contains(PresetService.RotationAngles, p => p.Value == 180);
    }

    [Fact]
    public void GetByCategory_FiltersCorrectly()
    {
        var grayscale = PresetService.GetByCategory(PresetService.Colors, "Grayscale").ToList();

        Assert.True(grayscale.Count > 0);
        Assert.All(grayscale, p => Assert.Equal("Grayscale", p.Category));
    }

    [Fact]
    public void GetCategories_ReturnsUniqueCategories()
    {
        var categories = PresetService.GetCategories(PresetService.Colors).ToList();

        Assert.True(categories.Count > 0);
        Assert.Contains("Grayscale", categories);
        Assert.Contains("Primary", categories);
        Assert.Contains("Catppuccin", categories);
    }

    [Fact]
    public void FindByName_FindsPreset()
    {
        var preset = PresetService.FindByName(PresetService.StrokeWidths, "Normal");

        Assert.NotNull(preset);
        Assert.Equal(2, preset.Value);
    }

    [Fact]
    public void FindByName_ReturnsNull_WhenNotFound()
    {
        var preset = PresetService.FindByName(PresetService.StrokeWidths, "NonExistent");

        Assert.Null(preset);
    }

    [Fact]
    public void FindClosest_FindsNearestPreset()
    {
        var preset = PresetService.FindClosest(PresetService.StrokeWidths, 2.1, 0.5);

        Assert.NotNull(preset);
        Assert.Equal("Normal", preset.Name);
    }

    [Fact]
    public void FindClosest_ReturnsNull_WhenOutsideTolerance()
    {
        var preset = PresetService.FindClosest(PresetService.StrokeWidths, 100, 0.1);

        Assert.Null(preset);
    }
}
