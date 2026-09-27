namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Fills;
using Bezier.Desktop.Services;
using SkiaSharp;

public class StrokeConverterTests
{
    private static readonly SKRect TestBounds = new(0, 0, 100, 100);

    [Fact]
    public void ToSkiaPaint_NullStroke_ReturnsNull()
    {
        Stroke? stroke = null;
        var paint = stroke.ToSkiaPaint(TestBounds);
        Assert.Null(paint);
    }

    [Fact]
    public void ToSkiaPaint_StrokeWithNullFill_ReturnsNull()
    {
        var stroke = new Stroke { Fill = null, Width = 2 };
        var paint = stroke.ToSkiaPaint(TestBounds);
        Assert.Null(paint);
    }

    [Fact]
    public void ToSkiaPaint_StrokeWithZeroWidth_ReturnsNull()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Width = 0 };
        var paint = stroke.ToSkiaPaint(TestBounds);
        Assert.Null(paint);
    }

    [Fact]
    public void ToSkiaPaint_StrokeWithZeroOpacity_ReturnsNull()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Width = 2, Opacity = 0 };
        var paint = stroke.ToSkiaPaint(TestBounds);
        Assert.Null(paint);
    }

    [Fact]
    public void ToSkiaPaint_ValidStroke_ReturnsStrokePaint()
    {
        var stroke = new Stroke { Fill = SolidFill.Red, Width = 3 };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(SKPaintStyle.Stroke, paint.Style);
        Assert.Equal(3, paint.StrokeWidth);
    }

    [Fact]
    public void ToSkiaPaint_StrokeColor_IsCorrect()
    {
        var stroke = new Stroke { Fill = SolidFill.FromRgb(255, 128, 64) };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(255, paint.Color.Red);
        Assert.Equal(128, paint.Color.Green);
        Assert.Equal(64, paint.Color.Blue);
    }

    [Fact]
    public void ToSkiaPaint_StrokeOpacity_AppliedToAlpha()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Opacity = 0.5 };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(127, (int)paint.Color.Alpha);
    }

    [Theory]
    [InlineData(LineCap.Butt, SKStrokeCap.Butt)]
    [InlineData(LineCap.Round, SKStrokeCap.Round)]
    [InlineData(LineCap.Square, SKStrokeCap.Square)]
    public void ToSkiaPaint_LineCap_ConvertedCorrectly(LineCap input, SKStrokeCap expected)
    {
        var stroke = new Stroke { Fill = SolidFill.Black, LineCap = input };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(expected, paint.StrokeCap);
    }

    [Theory]
    [InlineData(LineJoin.Miter, SKStrokeJoin.Miter)]
    [InlineData(LineJoin.Round, SKStrokeJoin.Round)]
    [InlineData(LineJoin.Bevel, SKStrokeJoin.Bevel)]
    public void ToSkiaPaint_LineJoin_ConvertedCorrectly(LineJoin input, SKStrokeJoin expected)
    {
        var stroke = new Stroke { Fill = SolidFill.Black, LineJoin = input };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(expected, paint.StrokeJoin);
    }

    [Fact]
    public void ToSkiaPaint_MiterLimit_Applied()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, MiterLimit = 8 };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Equal(8, paint.StrokeMiter);
    }

    [Fact]
    public void ToSkiaPaint_DashArray_CreatesPathEffect()
    {
        var stroke = new Stroke
        {
            Fill = SolidFill.Black,
            DashArray = [5, 3, 2, 3]
        };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.PathEffect);
    }

    [Fact]
    public void ToSkiaPaint_DashArrayWithOffset_CreatesPathEffect()
    {
        var stroke = new Stroke
        {
            Fill = SolidFill.Black,
            DashArray = [10, 5],
            DashOffset = 3
        };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.PathEffect);
    }

    [Fact]
    public void ToSkiaPaint_EmptyDashArray_NoPathEffect()
    {
        var stroke = new Stroke
        {
            Fill = SolidFill.Black,
            DashArray = []
        };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.Null(paint.PathEffect);
    }

    [Fact]
    public void ToSkiaPaint_GradientFill_CreatesShader()
    {
        var stroke = new Stroke
        {
            Fill = LinearGradientFill.Create(0xFFFF0000, 0xFF0000FF),
            Width = 4
        };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.NotNull(paint.Shader);
        Assert.Equal(SKPaintStyle.Stroke, paint.Style);
    }

    [Fact]
    public void ToSkiaPaint_IsAntialiasEnabled()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Width = 2 };
        using var paint = stroke.ToSkiaPaint(TestBounds);

        Assert.NotNull(paint);
        Assert.True(paint.IsAntialias);
    }

    [Fact]
    public void Stroke_Clone_CreatesDeepCopy()
    {
        var original = new Stroke
        {
            Fill = SolidFill.Red,
            Width = 5,
            Opacity = 0.8,
            LineCap = LineCap.Round,
            LineJoin = LineJoin.Bevel,
            MiterLimit = 6,
            DashArray = [4, 2],
            DashOffset = 1
        };

        var clone = original.Clone();

        Assert.NotSame(original, clone);
        Assert.NotSame(original.Fill, clone.Fill);
        Assert.NotSame(original.DashArray, clone.DashArray);
        Assert.Equal(original.Width, clone.Width);
        Assert.Equal(original.Opacity, clone.Opacity);
        Assert.Equal(original.LineCap, clone.LineCap);
        Assert.Equal(original.LineJoin, clone.LineJoin);
        Assert.Equal(original.MiterLimit, clone.MiterLimit);
        Assert.Equal(original.DashOffset, clone.DashOffset);
    }

    [Fact]
    public void Stroke_IsVisible_TrueForValidStroke()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Width = 1, Opacity = 1 };
        Assert.True(stroke.IsVisible);
    }

    [Fact]
    public void Stroke_IsVisible_FalseForNullFill()
    {
        var stroke = new Stroke { Fill = null, Width = 1, Opacity = 1 };
        Assert.False(stroke.IsVisible);
    }

    [Fact]
    public void Stroke_IsVisible_FalseForZeroWidth()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Width = 0, Opacity = 1 };
        Assert.False(stroke.IsVisible);
    }

    [Fact]
    public void Stroke_IsVisible_FalseForZeroOpacity()
    {
        var stroke = new Stroke { Fill = SolidFill.Black, Width = 1, Opacity = 0 };
        Assert.False(stroke.IsVisible);
    }
}
