namespace Bezier.Desktop.Services;

using Bezier.Core.Interfaces;
using SkiaSharp;

/// <summary>
/// Implementation of IToolRenderContext using SkiaSharp.
/// </summary>
public class SkiaToolRenderContext(SKCanvas canvas, double zoom) : IToolRenderContext
{
    private readonly SKCanvas _canvas = canvas;
    private readonly double _zoom = zoom;

    public void DrawLine(double x1, double y1, double x2, double y2, uint color, float strokeWidth = 1f)
    {
        using var paint = new SKPaint
        {
            Color = new SKColor(color),
            Style = SKPaintStyle.Stroke,
            StrokeWidth = strokeWidth / (float)_zoom,
            IsAntialias = true
        };
        _canvas.DrawLine((float)x1, (float)y1, (float)x2, (float)y2, paint);
    }

    public void DrawRect(double x, double y, double width, double height, uint color, float strokeWidth = 1f, bool fill = false)
    {
        using var paint = new SKPaint
        {
            Color = new SKColor(color),
            Style = fill ? SKPaintStyle.Fill : SKPaintStyle.Stroke,
            StrokeWidth = strokeWidth / (float)_zoom,
            IsAntialias = true
        };
        _canvas.DrawRect((float)x, (float)y, (float)width, (float)height, paint);
    }

    public void DrawEllipse(double cx, double cy, double rx, double ry, uint color, float strokeWidth = 1f, bool fill = false)
    {
        using var paint = new SKPaint
        {
            Color = new SKColor(color),
            Style = fill ? SKPaintStyle.Fill : SKPaintStyle.Stroke,
            StrokeWidth = strokeWidth / (float)_zoom,
            IsAntialias = true
        };
        _canvas.DrawOval((float)cx, (float)cy, (float)rx, (float)ry, paint);
    }

    public void DrawPath(string pathData, uint color, float strokeWidth = 1f, bool fill = false)
    {
        var path = SKPath.ParseSvgPathData(pathData);
        if (path is null) return;

        using var paint = new SKPaint
        {
            Color = new SKColor(color),
            Style = fill ? SKPaintStyle.Fill : SKPaintStyle.Stroke,
            StrokeWidth = strokeWidth / (float)_zoom,
            IsAntialias = true
        };
        _canvas.DrawPath(path, paint);
    }

    public void DrawText(string text, double x, double y, uint color, float fontSize = 12f)
    {
        using var paint = new SKPaint
        {
            Color = new SKColor(color),
            IsAntialias = true
        };
        using var font = new SKFont(SKTypeface.Default, fontSize / (float)_zoom);
        _canvas.DrawText(text, (float)x, (float)y, font, paint);
    }
}
