namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Models.Fills;
using Bezier.Desktop.Services;
using SkiaSharp;

public class FillConverterTests
{
    private static readonly SKRect TestBounds = new(0, 0, 100, 100);

    [Fact]
    public void ToSkiaPaint_NullFill_ReturnsNull()
    {
        IFill? fill = null;
        var paint = fill.ToSkiaPaint(TestBounds);
        Assert.Null(paint);
    }

    [Fact]
    public void ToSkiaPaint_NoneFill_ReturnsNull()
    {
        var fill = NoneFill.Instance;
        var paint = fill.ToSkiaPaint(TestBounds);
        Assert.Null(paint);
    }

    [Fact]
    public void ToSkiaPaint_SolidFill_ReturnsCorrectColor()
    {
        var fill = SolidFill.FromRgb(255, 0, 0);
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(SKPaintStyle.Fill, paint.Style);
        Assert.Equal(255, paint.Color.Red);
        Assert.Equal(0, paint.Color.Green);
        Assert.Equal(0, paint.Color.Blue);
        Assert.Equal(255, paint.Color.Alpha);
    }

    [Fact]
    public void ToSkiaPaint_SolidFill_WithAlpha_ReturnsCorrectAlpha()
    {
        var fill = SolidFill.FromRgb(0, 255, 0, 128);
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(128, paint.Color.Alpha);
    }

    [Fact]
    public void ToSkiaPaint_SolidFill_FromHex_ReturnsCorrectColor()
    {
        var fill = SolidFill.FromHex("#FF5500");
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(255, paint.Color.Red);
        Assert.Equal(85, paint.Color.Green);
        Assert.Equal(0, paint.Color.Blue);
    }

    [Fact]
    public void ToSkiaPaint_LinearGradient_CreatesShader()
    {
        var fill = LinearGradientFill.Create(0xFFFF0000, 0xFF0000FF);
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
        Assert.Equal(SKPaintStyle.Fill, paint.Style);
    }

    [Fact]
    public void ToSkiaPaint_LinearGradient_WithMultipleStops_CreatesShader()
    {
        var fill = new LinearGradientFill
        {
            StartX = 0, StartY = 0,
            EndX = 1, EndY = 1,
            Stops =
            [
                new GradientStop(0, 0xFFFF0000),
                new GradientStop(0.5, 0xFF00FF00),
                new GradientStop(1, 0xFF0000FF)
            ]
        };
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
    }

    [Fact]
    public void ToSkiaPaint_LinearGradient_ReflectMode_CreatesShader()
    {
        var fill = new LinearGradientFill
        {
            StartX = 0, StartY = 0.5,
            EndX = 1, EndY = 0.5,
            SpreadMode = GradientSpreadMode.Reflect,
            Stops =
            [
                new GradientStop(0, 0xFFFFFFFF),
                new GradientStop(1, 0xFF000000)
            ]
        };
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
    }

    [Fact]
    public void ToSkiaPaint_RadialGradient_CreatesShader()
    {
        var fill = RadialGradientFill.Create(0xFFFFFFFF, 0xFF000000);
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
        Assert.Equal(SKPaintStyle.Fill, paint.Style);
    }

    [Fact]
    public void ToSkiaPaint_RadialGradient_WithFocalPoint_CreatesShader()
    {
        var fill = new RadialGradientFill
        {
            CenterX = 0.5, CenterY = 0.5,
            RadiusX = 0.5, RadiusY = 0.5,
            FocalX = 0.3, FocalY = 0.3,
            Stops =
            [
                new GradientStop(0, 0xFFFFFFFF),
                new GradientStop(1, 0xFF000000)
            ]
        };
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
    }

    [Fact]
    public void ToSkiaPaint_RadialGradient_NonUniformRadius_CreatesShader()
    {
        var fill = new RadialGradientFill
        {
            CenterX = 0.5, CenterY = 0.5,
            RadiusX = 0.5, RadiusY = 0.25,
            Stops =
            [
                new GradientStop(0, 0xFFFF0000),
                new GradientStop(1, 0xFF0000FF)
            ]
        };
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
    }

    [Fact]
    public void ToSkiaPaint_PatternFill_CreatesShader()
    {
        var fill = new PatternFill
        {
            PatternId = "test-pattern",
            Width = 10,
            Height = 10
        };
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
        Assert.Equal(SKPaintStyle.Fill, paint.Style);
    }

    [Fact]
    public void ToSkiaPaint_PatternFill_WithOffset_CreatesShader()
    {
        var fill = new PatternFill
        {
            PatternId = "test-pattern",
            Width = 20,
            Height = 20,
            X = 5,
            Y = 5
        };
        using var paint = fill.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
    }

    [Fact]
    public void ToSkiaPaint_AllFillTypes_HaveAntialiasEnabled()
    {
        var fills = new IFill[]
        {
            SolidFill.Black,
            LinearGradientFill.Create(0xFFFF0000, 0xFF0000FF),
            RadialGradientFill.Create(0xFFFFFFFF, 0xFF000000),
            new PatternFill { Width = 10, Height = 10 }
        };

        foreach (var fill in fills)
        {
            using var paint = fill.ToSkiaPaint(TestBounds);
            Assert.NotNull(paint);
            Assert.True(paint.IsAntialias);
        }
    }

    [Fact]
    public void GradientStop_ClampsOffset()
    {
        var stop1 = new GradientStop(-0.5, 0xFFFFFFFF);
        var stop2 = new GradientStop(1.5, 0xFF000000);

        Assert.Equal(0, stop1.Offset);
        Assert.Equal(1, stop2.Offset);
    }

    [Fact]
    public void GradientStop_FromRgba_CreatesCorrectColor()
    {
        var stop = GradientStop.FromRgba(0.5, 255, 128, 64, 200);

        Assert.Equal(0.5, stop.Offset);
        Assert.Equal(0xC8FF8040u, stop.Color);
    }
}
