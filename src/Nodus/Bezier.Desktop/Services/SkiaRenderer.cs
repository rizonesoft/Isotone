namespace Bezier.Desktop.Services;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Desktop.Controls.Canvas;
using SkiaSharp;

/// <summary>
/// Renders vector documents and canvas elements using SkiaSharp.
/// </summary>
public class SkiaRenderer
{
    private const float RulerSize = 24f;
    private const int CheckerSize = 8;
    
    // Cached paints for performance
    private readonly SKPaint _gridMinorPaint;
    private readonly SKPaint _gridMajorPaint;
    private readonly SKPaint _rulerPaint;
    private readonly SKPaint _rulerTextPaint;
    private readonly SKPaint _rulerTickPaint;

    public SkiaRenderer()
    {
        _gridMinorPaint = new SKPaint
        {
            Color = new SKColor(200, 200, 200, 80),
            StrokeWidth = 1,
            IsAntialias = false,
            Style = SKPaintStyle.Stroke
        };
        
        _gridMajorPaint = new SKPaint
        {
            Color = new SKColor(150, 150, 150, 120),
            StrokeWidth = 1,
            IsAntialias = false,
            Style = SKPaintStyle.Stroke
        };
        
        _rulerPaint = new SKPaint
        {
            Color = new SKColor(45, 45, 50),
            Style = SKPaintStyle.Fill
        };
        
        _rulerTextPaint = new SKPaint
        {
            Color = new SKColor(180, 180, 180),
            TextSize = 10,
            IsAntialias = true,
            Typeface = SKTypeface.FromFamilyName("Segoe UI", SKFontStyle.Normal)
        };
        
        _rulerTickPaint = new SKPaint
        {
            Color = new SKColor(100, 100, 100),
            StrokeWidth = 1,
            IsAntialias = false
        };
    }

    /// <summary>
    /// Renders the entire vector document.
    /// </summary>
    public void RenderDocument(SKCanvas canvas, VectorDocument document, bool outlineMode, bool pixelPreview)
    {
        foreach (var element in document.Elements)
        {
            if (element.IsVisible)
            {
                RenderElement(canvas, element, outlineMode, pixelPreview);
            }
        }
    }

    /// <summary>
    /// Renders a single vector element.
    /// </summary>
    public void RenderElement(SKCanvas canvas, VectorElement element, bool outlineMode, bool pixelPreview)
    {
        canvas.Save();
        
        // Apply element transform
        if (!element.Transform.IsIdentity)
        {
            var matrix = new SKMatrix(
                (float)element.Transform.ScaleX,
                (float)element.Transform.SkewX,
                (float)element.Transform.TranslateX,
                (float)element.Transform.SkewY,
                (float)element.Transform.ScaleY,
                (float)element.Transform.TranslateY,
                0, 0, 1);
            canvas.Concat(ref matrix);
        }
        
        // Apply element opacity
        if (element.Opacity < 1.0)
        {
            canvas.SaveLayer(new SKPaint { Color = SKColors.White.WithAlpha((byte)(element.Opacity * 255)) });
        }

        switch (element)
        {
            case SvgRect rect:
                RenderRect(canvas, rect, outlineMode);
                break;
            case SvgCircle circle:
                RenderCircle(canvas, circle, outlineMode);
                break;
            case SvgEllipse ellipse:
                RenderEllipse(canvas, ellipse, outlineMode);
                break;
            case SvgLine line:
                RenderLine(canvas, line, outlineMode);
                break;
            case SvgPath path:
                RenderPath(canvas, path, outlineMode);
                break;
            case SvgPolygon polygon:
                RenderPolygon(canvas, polygon, outlineMode);
                break;
            case SvgPolyline polyline:
                RenderPolyline(canvas, polyline, outlineMode);
                break;
            case SvgText text:
                RenderText(canvas, text, outlineMode);
                break;
            case SvgGroup group:
                RenderGroup(canvas, group, outlineMode, pixelPreview);
                break;
        }

        if (element.Opacity < 1.0)
        {
            canvas.Restore();
        }
        
        canvas.Restore();
    }

    private void RenderRect(SKCanvas canvas, SvgRect rect, bool outlineMode)
    {
        var skRect = SKRect.Create((float)rect.X, (float)rect.Y, (float)rect.Width, (float)rect.Height);
        var bounds = skRect;
        
        if (!outlineMode && rect.Fill is not null)
        {
            using var fillPaint = rect.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                if (rect.Rx > 0 || rect.Ry > 0)
                    canvas.DrawRoundRect(skRect, (float)rect.Rx, (float)rect.Ry, fillPaint);
                else
                    canvas.DrawRect(skRect, fillPaint);
            }
        }
        
        if (rect.Stroke is not null)
        {
            using var strokePaint = rect.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                if (rect.Rx > 0 || rect.Ry > 0)
                    canvas.DrawRoundRect(skRect, (float)rect.Rx, (float)rect.Ry, strokePaint);
                else
                    canvas.DrawRect(skRect, strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true
            };
            if (rect.Rx > 0 || rect.Ry > 0)
                canvas.DrawRoundRect(skRect, (float)rect.Rx, (float)rect.Ry, outlinePaint);
            else
                canvas.DrawRect(skRect, outlinePaint);
        }
    }

    private void RenderCircle(SKCanvas canvas, SvgCircle circle, bool outlineMode)
    {
        var bounds = SKRect.Create(
            (float)(circle.Cx - circle.R),
            (float)(circle.Cy - circle.R),
            (float)(circle.R * 2),
            (float)(circle.R * 2));
        
        if (!outlineMode && circle.Fill is not null)
        {
            using var fillPaint = circle.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                canvas.DrawCircle((float)circle.Cx, (float)circle.Cy, (float)circle.R, fillPaint);
            }
        }
        
        if (circle.Stroke is not null)
        {
            using var strokePaint = circle.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                canvas.DrawCircle((float)circle.Cx, (float)circle.Cy, (float)circle.R, strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true
            };
            canvas.DrawCircle((float)circle.Cx, (float)circle.Cy, (float)circle.R, outlinePaint);
        }
    }

    private void RenderEllipse(SKCanvas canvas, SvgEllipse ellipse, bool outlineMode)
    {
        var bounds = SKRect.Create(
            (float)(ellipse.Cx - ellipse.Rx),
            (float)(ellipse.Cy - ellipse.Ry),
            (float)(ellipse.Rx * 2),
            (float)(ellipse.Ry * 2));
        
        if (!outlineMode && ellipse.Fill is not null)
        {
            using var fillPaint = ellipse.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                canvas.DrawOval(bounds, fillPaint);
            }
        }
        
        if (ellipse.Stroke is not null)
        {
            using var strokePaint = ellipse.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                canvas.DrawOval(bounds, strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true
            };
            canvas.DrawOval(bounds, outlinePaint);
        }
    }

    private void RenderLine(SKCanvas canvas, SvgLine line, bool outlineMode)
    {
        var bounds = SKRect.Create(
            (float)Math.Min(line.X1, line.X2),
            (float)Math.Min(line.Y1, line.Y2),
            (float)Math.Abs(line.X2 - line.X1),
            (float)Math.Abs(line.Y2 - line.Y1));
        
        if (line.Stroke is not null)
        {
            using var strokePaint = line.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                canvas.DrawLine(
                    (float)line.X1, (float)line.Y1,
                    (float)line.X2, (float)line.Y2,
                    strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true
            };
            canvas.DrawLine(
                (float)line.X1, (float)line.Y1,
                (float)line.X2, (float)line.Y2,
                outlinePaint);
        }
    }

    private void RenderPath(SKCanvas canvas, SvgPath path, bool outlineMode)
    {
        if (string.IsNullOrWhiteSpace(path.PathData)) return;
        
        try
        {
            var skPath = SKPath.ParseSvgPathData(path.PathData);
            if (skPath is null) return;
            
            var bounds = skPath.Bounds;
            
            if (!outlineMode && path.Fill is not null)
            {
                using var fillPaint = path.Fill.ToSkiaPaint(bounds);
                if (fillPaint is not null)
                {
                    canvas.DrawPath(skPath, fillPaint);
                }
            }
            
            if (path.Stroke is not null)
            {
                using var strokePaint = path.Stroke.ToSkiaPaint(bounds);
                if (strokePaint is not null)
                {
                    if (outlineMode)
                    {
                        strokePaint.Color = SKColors.Black;
                        strokePaint.StrokeWidth = 1;
                    }
                    canvas.DrawPath(skPath, strokePaint);
                }
            }
            else if (outlineMode)
            {
                using var outlinePaint = new SKPaint
                {
                    Style = SKPaintStyle.Stroke,
                    Color = SKColors.Black,
                    StrokeWidth = 1,
                    IsAntialias = true
                };
                canvas.DrawPath(skPath, outlinePaint);
            }
            
            skPath.Dispose();
        }
        catch
        {
            // Invalid path data, skip rendering
        }
    }

    private void RenderPolygon(SKCanvas canvas, SvgPolygon polygon, bool outlineMode)
    {
        if (polygon.Points.Count < 2) return;
        
        using var skPath = new SKPath();
        skPath.MoveTo((float)polygon.Points[0].X, (float)polygon.Points[0].Y);
        
        for (int i = 1; i < polygon.Points.Count; i++)
        {
            skPath.LineTo((float)polygon.Points[i].X, (float)polygon.Points[i].Y);
        }
        skPath.Close();
        
        var bounds = skPath.Bounds;
        
        if (!outlineMode && polygon.Fill is not null)
        {
            using var fillPaint = polygon.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                canvas.DrawPath(skPath, fillPaint);
            }
        }
        
        if (polygon.Stroke is not null)
        {
            using var strokePaint = polygon.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                canvas.DrawPath(skPath, strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true
            };
            canvas.DrawPath(skPath, outlinePaint);
        }
    }

    private void RenderPolyline(SKCanvas canvas, SvgPolyline polyline, bool outlineMode)
    {
        if (polyline.Points.Count < 2) return;
        
        using var skPath = new SKPath();
        skPath.MoveTo((float)polyline.Points[0].X, (float)polyline.Points[0].Y);
        
        for (int i = 1; i < polyline.Points.Count; i++)
        {
            skPath.LineTo((float)polyline.Points[i].X, (float)polyline.Points[i].Y);
        }
        
        var bounds = skPath.Bounds;
        
        if (!outlineMode && polyline.Fill is not null)
        {
            using var fillPaint = polyline.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                canvas.DrawPath(skPath, fillPaint);
            }
        }
        
        if (polyline.Stroke is not null)
        {
            using var strokePaint = polyline.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                canvas.DrawPath(skPath, strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true
            };
            canvas.DrawPath(skPath, outlinePaint);
        }
    }

    private void RenderText(SKCanvas canvas, SvgText text, bool outlineMode)
    {
        using var paint = new SKPaint
        {
            TextSize = (float)text.FontSize,
            Typeface = SKTypeface.FromFamilyName(
                text.FontFamily,
                text.FontWeight,
                (int)SKFontStyleWidth.Normal,
                text.Italic ? SKFontStyleSlant.Italic : SKFontStyleSlant.Upright),
            IsAntialias = true
        };
        
        // Measure text for bounds
        var textBounds = new SKRect();
        paint.MeasureText(text.Text, ref textBounds);
        
        var x = (float)text.X;
        var y = (float)text.Y;
        
        // Adjust for text anchor
        x = text.TextAnchor switch
        {
            TextAnchor.Middle => x - textBounds.Width / 2,
            TextAnchor.End => x - textBounds.Width,
            _ => x
        };
        
        var bounds = SKRect.Create(x, y - textBounds.Height, textBounds.Width, textBounds.Height);
        
        if (!outlineMode && text.Fill is not null)
        {
            using var fillPaint = text.Fill.ToSkiaPaint(bounds);
            if (fillPaint is not null)
            {
                fillPaint.TextSize = paint.TextSize;
                fillPaint.Typeface = paint.Typeface;
                fillPaint.IsAntialias = true;
                fillPaint.Style = SKPaintStyle.Fill;
                canvas.DrawText(text.Text, (float)text.X, (float)text.Y, fillPaint);
            }
        }
        
        if (text.Stroke is not null)
        {
            using var strokePaint = text.Stroke.ToSkiaPaint(bounds);
            if (strokePaint is not null)
            {
                strokePaint.TextSize = paint.TextSize;
                strokePaint.Typeface = paint.Typeface;
                strokePaint.IsAntialias = true;
                if (outlineMode)
                {
                    strokePaint.Color = SKColors.Black;
                    strokePaint.StrokeWidth = 1;
                }
                canvas.DrawText(text.Text, (float)text.X, (float)text.Y, strokePaint);
            }
        }
        else if (outlineMode)
        {
            using var outlinePaint = new SKPaint
            {
                Style = SKPaintStyle.Stroke,
                Color = SKColors.Black,
                StrokeWidth = 1,
                IsAntialias = true,
                TextSize = paint.TextSize,
                Typeface = paint.Typeface
            };
            canvas.DrawText(text.Text, (float)text.X, (float)text.Y, outlinePaint);
        }
    }

    private void RenderGroup(SKCanvas canvas, SvgGroup group, bool outlineMode, bool pixelPreview)
    {
        foreach (var child in group.Children)
        {
            if (child.IsVisible)
            {
                RenderElement(canvas, child, outlineMode, pixelPreview);
            }
        }
    }

    /// <summary>
    /// Renders an adaptive grid that adjusts based on zoom level.
    /// </summary>
    public void RenderGrid(SKCanvas canvas, VectorDocument document, double zoom)
    {
        // Calculate adaptive grid spacing based on zoom
        var baseSpacing = 10.0;
        var majorInterval = 10;
        
        // Adjust grid visibility based on zoom
        while (baseSpacing * zoom < 10)
        {
            baseSpacing *= 2;
            majorInterval = 5;
        }
        while (baseSpacing * zoom > 50)
        {
            baseSpacing /= 2;
            majorInterval = 10;
        }
        
        var spacing = (float)baseSpacing;
        var majorSpacing = spacing * majorInterval;
        
        // Calculate grid bounds
        var startX = 0f;
        var startY = 0f;
        var endX = (float)document.Width;
        var endY = (float)document.Height;
        
        // Fade grid lines based on zoom
        var minorAlpha = (byte)Math.Clamp((zoom - 0.3) * 100, 0, 80);
        var majorAlpha = (byte)Math.Clamp((zoom - 0.2) * 150, 0, 120);
        
        _gridMinorPaint.Color = new SKColor(200, 200, 200, minorAlpha);
        _gridMajorPaint.Color = new SKColor(150, 150, 150, majorAlpha);
        
        // Adjust stroke width for zoom
        _gridMinorPaint.StrokeWidth = 1f / (float)zoom;
        _gridMajorPaint.StrokeWidth = 1f / (float)zoom;
        
        // Draw minor vertical lines
        for (var x = startX; x <= endX; x += spacing)
        {
            if (Math.Abs(x % majorSpacing) > 0.01)
            {
                canvas.DrawLine(x, startY, x, endY, _gridMinorPaint);
            }
        }
        
        // Draw minor horizontal lines
        for (var y = startY; y <= endY; y += spacing)
        {
            if (Math.Abs(y % majorSpacing) > 0.01)
            {
                canvas.DrawLine(startX, y, endX, y, _gridMinorPaint);
            }
        }
        
        // Draw major vertical lines
        for (var x = startX; x <= endX; x += majorSpacing)
        {
            canvas.DrawLine(x, startY, x, endY, _gridMajorPaint);
        }
        
        // Draw major horizontal lines
        for (var y = startY; y <= endY; y += majorSpacing)
        {
            canvas.DrawLine(startX, y, endX, y, _gridMajorPaint);
        }
        
        // Draw origin indicator
        using var originPaint = new SKPaint
        {
            Color = new SKColor(100, 150, 200, 150),
            StrokeWidth = 2f / (float)zoom,
            IsAntialias = true
        };
        canvas.DrawLine(-10f / (float)zoom, 0, 10f / (float)zoom, 0, originPaint);
        canvas.DrawLine(0, -10f / (float)zoom, 0, 10f / (float)zoom, originPaint);
    }

    /// <summary>
    /// Renders rulers along the top and left edges.
    /// </summary>
    public void RenderRulers(SKCanvas canvas, SKImageInfo info, CanvasState state, VectorDocument? document, SKPoint cursorScreenPosition = default)
    {
        // Draw ruler backgrounds
        canvas.DrawRect(0, 0, info.Width, RulerSize, _rulerPaint);
        canvas.DrawRect(0, 0, RulerSize, info.Height, _rulerPaint);
        
        // Draw corner square
        using var cornerPaint = new SKPaint { Color = new SKColor(35, 35, 40) };
        canvas.DrawRect(0, 0, RulerSize, RulerSize, cornerPaint);
        
        // Calculate tick spacing based on zoom
        var zoom = state.Zoom;
        var tickSpacing = CalculateRulerTickSpacing(zoom);
        var majorInterval = tickSpacing >= 100 ? 5 : 10;
        
        // Horizontal ruler
        RenderHorizontalRuler(canvas, info.Width, state, tickSpacing, majorInterval);
        
        // Vertical ruler
        RenderVerticalRuler(canvas, info.Height, state, tickSpacing, majorInterval);
        
        // Draw cursor position indicators
        if (cursorScreenPosition.X > RulerSize && cursorScreenPosition.Y > RulerSize)
        {
            RenderCursorIndicators(canvas, cursorScreenPosition, state);
        }
    }

    private void RenderCursorIndicators(SKCanvas canvas, SKPoint cursorScreenPosition, CanvasState state)
    {
        using var indicatorPaint = new SKPaint
        {
            Color = new SKColor(255, 107, 53), // Orange accent color
            Style = SKPaintStyle.Fill,
            IsAntialias = true
        };
        
        using var linePaint = new SKPaint
        {
            Color = new SKColor(255, 107, 53, 100),
            StrokeWidth = 1,
            IsAntialias = true
        };
        
        // Horizontal ruler indicator (triangle pointing down)
        var hx = cursorScreenPosition.X;
        if (hx > RulerSize)
        {
            var trianglePath = new SKPath();
            trianglePath.MoveTo(hx - 4, RulerSize - 8);
            trianglePath.LineTo(hx + 4, RulerSize - 8);
            trianglePath.LineTo(hx, RulerSize - 2);
            trianglePath.Close();
            canvas.DrawPath(trianglePath, indicatorPaint);
            
            // Draw vertical guide line
            canvas.DrawLine(hx, RulerSize, hx, cursorScreenPosition.Y, linePaint);
        }
        
        // Vertical ruler indicator (triangle pointing right)
        var vy = cursorScreenPosition.Y;
        if (vy > RulerSize)
        {
            var trianglePath = new SKPath();
            trianglePath.MoveTo(RulerSize - 8, vy - 4);
            trianglePath.LineTo(RulerSize - 8, vy + 4);
            trianglePath.LineTo(RulerSize - 2, vy);
            trianglePath.Close();
            canvas.DrawPath(trianglePath, indicatorPaint);
            
            // Draw horizontal guide line
            canvas.DrawLine(RulerSize, vy, cursorScreenPosition.X, vy, linePaint);
        }
    }

    private void RenderHorizontalRuler(SKCanvas canvas, int width, CanvasState state, float tickSpacing, int majorInterval)
    {
        var startDoc = state.ScreenToDocument(new SKPoint(RulerSize, 0));
        var endDoc = state.ScreenToDocument(new SKPoint(width, 0));
        
        var startX = (float)(Math.Floor(startDoc.X / tickSpacing) * tickSpacing);
        var endX = (float)(Math.Ceiling(endDoc.X / tickSpacing) * tickSpacing);
        
        for (var docX = startX; docX <= endX; docX += tickSpacing)
        {
            var screenX = state.DocumentToScreen(new SKPoint(docX, 0)).X;
            if (screenX < RulerSize) continue;
            
            var tickIndex = (int)Math.Round(docX / tickSpacing);
            var isMajor = tickIndex % majorInterval == 0;
            var tickHeight = isMajor ? RulerSize * 0.6f : RulerSize * 0.3f;
            
            canvas.DrawLine(screenX, RulerSize - tickHeight, screenX, RulerSize, _rulerTickPaint);
            
            if (isMajor)
            {
                var label = docX.ToString("0");
                canvas.DrawText(label, screenX + 2, RulerSize - tickHeight - 2, _rulerTextPaint);
            }
        }
    }

    private void RenderVerticalRuler(SKCanvas canvas, int height, CanvasState state, float tickSpacing, int majorInterval)
    {
        var startDoc = state.ScreenToDocument(new SKPoint(0, RulerSize));
        var endDoc = state.ScreenToDocument(new SKPoint(0, height));
        
        var startY = (float)(Math.Floor(startDoc.Y / tickSpacing) * tickSpacing);
        var endY = (float)(Math.Ceiling(endDoc.Y / tickSpacing) * tickSpacing);
        
        canvas.Save();
        
        for (var docY = startY; docY <= endY; docY += tickSpacing)
        {
            var screenY = state.DocumentToScreen(new SKPoint(0, docY)).Y;
            if (screenY < RulerSize) continue;
            
            var tickIndex = (int)Math.Round(docY / tickSpacing);
            var isMajor = tickIndex % majorInterval == 0;
            var tickWidth = isMajor ? RulerSize * 0.6f : RulerSize * 0.3f;
            
            canvas.DrawLine(RulerSize - tickWidth, screenY, RulerSize, screenY, _rulerTickPaint);
            
            if (isMajor)
            {
                var label = docY.ToString("0");
                canvas.Save();
                canvas.Translate(RulerSize - tickWidth - 2, screenY + 2);
                canvas.RotateDegrees(-90);
                canvas.DrawText(label, 0, 0, _rulerTextPaint);
                canvas.Restore();
            }
        }
        
        canvas.Restore();
    }

    private static float CalculateRulerTickSpacing(double zoom)
    {
        // Target tick spacing in screen pixels
        const float targetScreenSpacing = 50f;
        var docSpacing = (float)(targetScreenSpacing / zoom);
        
        // Round to nice numbers
        float[] niceNumbers = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000];
        
        foreach (var nice in niceNumbers)
        {
            if (docSpacing <= nice)
                return nice;
        }
        
        return 1000;
    }

    /// <summary>
    /// Renders a checkerboard pattern for transparency indication.
    /// </summary>
    public void RenderCheckerboard(SKCanvas canvas, SKImageInfo info)
    {
        var color1 = new SKColor(204, 204, 204);
        var color2 = new SKColor(255, 255, 255);
        
        using var paint1 = new SKPaint { Color = color1 };
        using var paint2 = new SKPaint { Color = color2 };
        
        for (var y = 0; y < info.Height; y += CheckerSize)
        {
            for (var x = 0; x < info.Width; x += CheckerSize)
            {
                var isLight = ((x / CheckerSize) + (y / CheckerSize)) % 2 == 0;
                canvas.DrawRect(x, y, CheckerSize, CheckerSize, isLight ? paint1 : paint2);
            }
        }
    }
}
