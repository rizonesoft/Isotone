namespace Bezier.Desktop.Services;

using Bezier.Core.Models;
using SkiaSharp;

/// <summary>
/// Converts domain stroke models to SkiaSharp paint objects for rendering.
/// </summary>
public static class StrokeConverter
{
    /// <summary>
    /// Converts a <see cref="Stroke"/> to an <see cref="SKPaint"/> for rendering.
    /// </summary>
    /// <param name="stroke">The stroke to convert.</param>
    /// <param name="bounds">The element bounds for gradient fill calculations.</param>
    /// <returns>An SKPaint configured for the stroke, or null if stroke is not visible.</returns>
    public static SKPaint? ToSkiaPaint(this Stroke? stroke, SKRect bounds)
    {
        if (stroke is null || !stroke.IsVisible)
            return null;

        var paint = new SKPaint
        {
            Style = SKPaintStyle.Stroke,
            StrokeWidth = (float)stroke.Width,
            IsAntialias = true,
            StrokeCap = ConvertLineCap(stroke.LineCap),
            StrokeJoin = ConvertLineJoin(stroke.LineJoin),
            StrokeMiter = (float)stroke.MiterLimit
        };

        // Apply stroke fill (color/gradient)
        if (stroke.Fill is not null)
        {
            var fillPaint = stroke.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                paint.Color = fillPaint.Color;
                paint.Shader = fillPaint.Shader;
                fillPaint.Dispose();
            }
        }

        // Apply opacity
        if (stroke.Opacity < 1.0)
        {
            var color = paint.Color;
            paint.Color = color.WithAlpha((byte)(color.Alpha * stroke.Opacity));
        }

        // Apply dash pattern
        if (stroke.DashArray is { Length: > 0 })
        {
            var dashArray = stroke.DashArray.Select(d => (float)d).ToArray();
            paint.PathEffect = SKPathEffect.CreateDash(dashArray, (float)stroke.DashOffset);
        }

        return paint;
    }

    /// <summary>
    /// Converts domain LineCap to SkiaSharp SKStrokeCap.
    /// </summary>
    private static SKStrokeCap ConvertLineCap(LineCap cap) => cap switch
    {
        LineCap.Butt => SKStrokeCap.Butt,
        LineCap.Round => SKStrokeCap.Round,
        LineCap.Square => SKStrokeCap.Square,
        _ => SKStrokeCap.Butt
    };

    /// <summary>
    /// Converts domain LineJoin to SkiaSharp SKStrokeJoin.
    /// </summary>
    private static SKStrokeJoin ConvertLineJoin(LineJoin join) => join switch
    {
        LineJoin.Miter => SKStrokeJoin.Miter,
        LineJoin.Round => SKStrokeJoin.Round,
        LineJoin.Bevel => SKStrokeJoin.Bevel,
        _ => SKStrokeJoin.Miter
    };
}
