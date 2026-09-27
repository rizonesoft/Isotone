namespace Bezier.Tests;

using Bezier.Core.Models;

public class ColorTests
{
    [Fact]
    public void Color_FromRgb_CreatesCorrectColor()
    {
        var color = Color.FromRgb(255, 128, 64);

        Assert.Equal(255, color.R);
        Assert.Equal(128, color.G);
        Assert.Equal(64, color.B);
        Assert.Equal(255, color.A);
    }

    [Fact]
    public void Color_FromArgb_CreatesCorrectColor()
    {
        var color = Color.FromArgb(0x80FF8040);

        Assert.Equal(255, color.R);
        Assert.Equal(128, color.G);
        Assert.Equal(64, color.B);
        Assert.Equal(128, color.A);
    }

    [Fact]
    public void Color_ToArgb_ReturnsCorrectValue()
    {
        var color = new Color(255, 128, 64, 128);

        Assert.Equal(0x80FF8040u, color.ToArgb());
    }

    [Fact]
    public void Color_FromHex_ParsesRRGGBB()
    {
        var color = Color.FromHex("#FF8040");

        Assert.Equal(255, color.R);
        Assert.Equal(128, color.G);
        Assert.Equal(64, color.B);
        Assert.Equal(255, color.A);
    }

    [Fact]
    public void Color_FromHex_ParsesRRGGBBAA()
    {
        var color = Color.FromHex("#FF804080");

        Assert.Equal(255, color.R);
        Assert.Equal(128, color.G);
        Assert.Equal(64, color.B);
        Assert.Equal(128, color.A);
    }

    [Fact]
    public void Color_FromHex_ParsesShortForm()
    {
        var color = Color.FromHex("#F84");

        Assert.Equal(255, color.R);
        Assert.Equal(136, color.G);
        Assert.Equal(68, color.B);
    }

    [Fact]
    public void Color_ToHex_ReturnsCorrectString()
    {
        var color = new Color(255, 128, 64, 255);

        Assert.Equal("#FF8040", color.ToHex());
    }

    [Fact]
    public void Color_ToHex_IncludesAlpha_WhenNotOpaque()
    {
        var color = new Color(255, 128, 64, 128);

        Assert.Equal("#FF804080", color.ToHex());
    }

    [Fact]
    public void Color_FromHsl_CreatesCorrectColor()
    {
        // Red: H=0, S=1, L=0.5
        var red = Color.FromHsl(0, 1, 0.5);
        Assert.Equal(255, red.R);
        Assert.Equal(0, red.G);
        Assert.Equal(0, red.B);

        // Green: H=120, S=1, L=0.5
        var green = Color.FromHsl(120, 1, 0.5);
        Assert.Equal(0, green.R);
        Assert.Equal(255, green.G);
        Assert.Equal(0, green.B);

        // Blue: H=240, S=1, L=0.5
        var blue = Color.FromHsl(240, 1, 0.5);
        Assert.Equal(0, blue.R);
        Assert.Equal(0, blue.G);
        Assert.Equal(255, blue.B);
    }

    [Fact]
    public void Color_ToHsl_ReturnsCorrectValues()
    {
        var red = Color.Red;
        var (h, s, l) = red.ToHsl();

        Assert.Equal(0, h, 1);
        Assert.Equal(1, s, 0.01);
        Assert.Equal(0.5, l, 0.01);
    }

    [Fact]
    public void Color_FromHsv_CreatesCorrectColor()
    {
        // Red: H=0, S=1, V=1
        var red = Color.FromHsv(0, 1, 1);
        Assert.Equal(255, red.R);
        Assert.Equal(0, red.G);
        Assert.Equal(0, red.B);
    }

    [Fact]
    public void Color_ToHsv_ReturnsCorrectValues()
    {
        var red = Color.Red;
        var (h, s, v) = red.ToHsv();

        Assert.Equal(0, h, 1);
        Assert.Equal(1, s, 0.01);
        Assert.Equal(1, v, 0.01);
    }

    [Fact]
    public void Color_Lerp_InterpolatesCorrectly()
    {
        var black = Color.Black;
        var white = Color.White;

        var mid = Color.Lerp(black, white, 0.5);

        Assert.Equal(127, mid.R);
        Assert.Equal(127, mid.G);
        Assert.Equal(127, mid.B);
    }

    [Fact]
    public void Color_WithAlpha_ReturnsNewColor()
    {
        var color = Color.Red;
        var transparent = color.WithAlpha(128);

        Assert.Equal(255, transparent.R);
        Assert.Equal(0, transparent.G);
        Assert.Equal(0, transparent.B);
        Assert.Equal(128, transparent.A);
    }

    [Fact]
    public void Color_Luminance_CalculatesCorrectly()
    {
        Assert.Equal(0, Color.Black.Luminance, 0.01);
        Assert.Equal(1, Color.White.Luminance, 0.01);
    }

    [Fact]
    public void Color_IsLight_ReturnsTrueForLightColors()
    {
        Assert.True(Color.White.IsLight);
        Assert.True(Color.Yellow.IsLight);
        Assert.False(Color.Black.IsLight);
        Assert.False(Color.Blue.IsLight);
    }

    [Fact]
    public void Color_ContrastColor_ReturnsBlackOrWhite()
    {
        Assert.Equal(Color.Black, Color.White.ContrastColor);
        Assert.Equal(Color.White, Color.Black.ContrastColor);
    }

    [Fact]
    public void Color_Equality_WorksCorrectly()
    {
        var color1 = new Color(255, 128, 64, 255);
        var color2 = new Color(255, 128, 64, 255);
        var color3 = new Color(255, 128, 64, 128);

        Assert.Equal(color1, color2);
        Assert.NotEqual(color1, color3);
        Assert.True(color1 == color2);
        Assert.True(color1 != color3);
    }
}

public class PropertyDescriptorTests
{
    [Fact]
    public void PropertyDescriptor_SetValue_RaisesEvent()
    {
        var property = new PropertyDescriptor
        {
            Id = "test",
            Name = "Test",
            Type = PropertyType.Number
        };

        object? receivedValue = null;
        property.ValueChanged += (_, v) => receivedValue = v;

        property.SetValue(42);

        Assert.Equal(42, receivedValue);
        Assert.Equal(42, property.Value);
    }

    [Fact]
    public void PropertyDescriptor_SetValue_DoesNotRaiseEvent_WhenSameValue()
    {
        var property = new PropertyDescriptor
        {
            Id = "test",
            Name = "Test",
            Type = PropertyType.Number,
            Value = 42
        };

        var eventRaised = false;
        property.ValueChanged += (_, _) => eventRaised = true;

        property.SetValue(42);

        Assert.False(eventRaised);
    }

    [Fact]
    public void PropertyGroup_DefaultsExpanded()
    {
        var group = new PropertyGroup { Name = "Test" };

        Assert.True(group.IsExpanded);
        Assert.Empty(group.Properties);
    }
}
