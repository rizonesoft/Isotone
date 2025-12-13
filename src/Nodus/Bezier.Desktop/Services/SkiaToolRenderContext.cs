namespace Bezier.Desktop.Services;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using SkiaSharp;

/// <summary>
/// Implementation of IToolRenderContext using SkiaSharp.
/// </summary>
public class SkiaToolRenderContext : IToolRenderContext
{
    private readonly SKCanvas _canvas;
    private readonly double _zoom;
    private readonly SkiaRenderer _renderer;

    public SkiaToolRenderContext(SKCanvas canvas, double zoom, SkiaRenderer? renderer = null)
    {
        _canvas = canvas;
        _zoom = zoom;
        _renderer = renderer ?? new SkiaRenderer();
    }

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
        
        // For small handles (fill=true), scale inversely with zoom to maintain screen size
        var drawWidth = (float)width;
        var drawHeight = (float)height;
        var drawX = (float)x;
        var drawY = (float)y;
        
        if (fill && width <= 20 && height <= 20)
        {
            // This is likely a handle - scale to maintain screen size
            drawWidth = (float)(width / _zoom);
            drawHeight = (float)(height / _zoom);
            // Adjust position to center the scaled handle
            drawX = (float)(x - (drawWidth - width) / 2);
            drawY = (float)(y - (drawHeight - height) / 2);
        }
        
        _canvas.DrawRect(drawX, drawY, drawWidth, drawHeight, paint);
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

    public void DrawElementPreview(object element, double offsetX, double offsetY, double opacity = 0.5)
    {
        if (element is not VectorElement vectorElement) return;

        _canvas.Save();
        
        // Apply offset translation
        _canvas.Translate((float)offsetX, (float)offsetY);
        
        // Apply opacity via save layer
        using var layerPaint = new SKPaint
        {
            Color = SKColors.White.WithAlpha((byte)(opacity * 255))
        };
        _canvas.SaveLayer(layerPaint);
        
        // Render the element
        _renderer.RenderElement(_canvas, vectorElement, outlineMode: false, pixelPreview: false);
        
        _canvas.Restore(); // Layer
        _canvas.Restore(); // Translation
    }
}
