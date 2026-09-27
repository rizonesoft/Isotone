namespace Bezier.Desktop.Services;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;
using SkiaSharp;

/// <summary>
/// Converts domain fill models to SkiaSharp paint objects for rendering.
/// </summary>
public static class FillConverter
{
    /// <summary>
    /// Converts an <see cref="IFill"/> to an <see cref="SKPaint"/> for rendering.
    /// </summary>
    /// <param name="fill">The fill to convert.</param>
    /// <param name="bounds">The element bounds for gradient calculations.</param>
    /// <param name="document">The document containing definitions (for pattern lookup).</param>
    /// <param name="patternRenderer">Callback to render a pattern element to an SKPicture.</param>
    /// <returns>An SKPaint configured for the fill, or null for NoneFill.</returns>
    public static SKPaint? ToSkiaPaint(
        this IFill? fill, 
        SKRect bounds, 
        VectorDocument? document = null,
        Func<SvgPattern, SKPicture>? patternRenderer = null)
    {
        if (fill is null or NoneFill)
            return null;

        return fill switch
        {
            SolidFill solid => CreateSolidPaint(solid),
            LinearGradientFill linear => CreateLinearGradientPaint(linear, bounds),
            RadialGradientFill radial => CreateRadialGradientPaint(radial, bounds),
            PatternFill pattern => CreatePatternPaint(pattern, bounds, document, patternRenderer),
            _ => null
        };
    }

    /// <summary>
    /// Creates an SKPaint from a solid fill.
    /// </summary>
    private static SKPaint CreateSolidPaint(SolidFill solid)
    {
        return new SKPaint
        {
            Style = SKPaintStyle.Fill,
            Color = new SKColor(solid.Color),
            IsAntialias = true
        };
    }

    /// <summary>
    /// Creates an SKPaint from a linear gradient fill.
    /// </summary>
    private static SKPaint CreateLinearGradientPaint(LinearGradientFill gradient, SKRect bounds)
    {
        var startPoint = new SKPoint(
            bounds.Left + (float)(gradient.StartX * bounds.Width),
            bounds.Top + (float)(gradient.StartY * bounds.Height));

        var endPoint = new SKPoint(
            bounds.Left + (float)(gradient.EndX * bounds.Width),
            bounds.Top + (float)(gradient.EndY * bounds.Height));

        var (colors, positions) = ExtractGradientStops(gradient.Stops);
        var tileMode = ConvertSpreadMode(gradient.SpreadMode);

        var shader = SKShader.CreateLinearGradient(
            startPoint,
            endPoint,
            colors,
            positions,
            tileMode);

        return new SKPaint
        {
            Style = SKPaintStyle.Fill,
            Shader = shader,
            IsAntialias = true
        };
    }

    /// <summary>
    /// Creates an SKPaint from a radial gradient fill.
    /// </summary>
    private static SKPaint CreateRadialGradientPaint(RadialGradientFill gradient, SKRect bounds)
    {
        var center = new SKPoint(
            bounds.Left + (float)(gradient.CenterX * bounds.Width),
            bounds.Top + (float)(gradient.CenterY * bounds.Height));

        var radiusX = (float)(gradient.RadiusX * bounds.Width);
        var radiusY = (float)(gradient.RadiusY * bounds.Height);
        var radius = Math.Max(radiusX, radiusY);

        var (colors, positions) = ExtractGradientStops(gradient.Stops);
        var tileMode = ConvertSpreadMode(gradient.SpreadMode);

        SKShader shader;

        // Check if focal point differs from center (two-point radial gradient)
        var hasFocalPoint = Math.Abs(gradient.FocalX - gradient.CenterX) > 0.001 ||
                           Math.Abs(gradient.FocalY - gradient.CenterY) > 0.001;

        if (hasFocalPoint)
        {
            var focal = new SKPoint(
                bounds.Left + (float)(gradient.FocalX * bounds.Width),
                bounds.Top + (float)(gradient.FocalY * bounds.Height));

            shader = SKShader.CreateTwoPointConicalGradient(
                focal, 0,
                center, radius,
                colors,
                positions,
                tileMode);
        }
        else
        {
            shader = SKShader.CreateRadialGradient(
                center,
                radius,
                colors,
                positions,
                tileMode);
        }

        // Handle non-uniform radius with matrix transform
        if (Math.Abs(radiusX - radiusY) > 0.001 && radiusX > 0 && radiusY > 0)
        {
            var scaleX = radiusX / radius;
            var scaleY = radiusY / radius;
            var matrix = SKMatrix.CreateScale(scaleX, scaleY, center.X, center.Y);
            shader = shader.WithLocalMatrix(matrix);
        }

        return new SKPaint
        {
            Style = SKPaintStyle.Fill,
            Shader = shader,
            IsAntialias = true
        };
    }

    /// <summary>
    /// Creates an SKPaint from a pattern fill.
    /// </summary>
    /// <remarks>
    /// Pattern fills require the pattern content to be rendered separately.
    /// This method creates a placeholder paint. Full pattern support requires
    /// pattern definition lookup from the document's defs section.
    /// </remarks>
    private static SKPaint CreatePatternPaint(
        PatternFill pattern, 
        SKRect bounds, 
        VectorDocument? document,
        Func<SvgPattern, SKPicture>? patternRenderer)
    {
        // Try to find the pattern definition
        SvgPattern? patternDef = null;
        
        if (document is not null && !string.IsNullOrEmpty(pattern.PatternId))
        {
            // Look in Defs
            patternDef = document.Defs.OfType<SvgPattern>()
                .FirstOrDefault(p => p.Name == pattern.PatternId || p.Id.ToString() == pattern.PatternId);
                
            // Also look in Elements (though less common for definitions)
            if (patternDef is null)
            {
                patternDef = document.Elements.OfType<SvgPattern>()
                    .FirstOrDefault(p => p.Name == pattern.PatternId || p.Id.ToString() == pattern.PatternId);
            }
        }

        if (patternDef is not null && patternRenderer is not null)
        {
            var picture = patternRenderer(patternDef);
            
            var tileMode = SKShaderTileMode.Repeat;
            var matrix = SKMatrix.Identity;
            
            // Apply Pattern transform (x, y) if needed
            // PatternUnits logic can be complex, simplifying for now
            
            var shader = SKShader.CreatePicture(
                picture, 
                SKShaderTileMode.Repeat, 
                SKShaderTileMode.Repeat, 
                matrix, 
                SKRect.Create((float)patternDef.X, (float)patternDef.Y, (float)patternDef.Width, (float)patternDef.Height));
                
             return new SKPaint
            {
                Style = SKPaintStyle.Fill,
                Shader = shader,
                IsAntialias = true
            };
        }

        // Fallback to placeholder if pattern not found or renderer not provided
        var tileWidth = (int)Math.Max(pattern.Width, 1);
        var tileHeight = (int)Math.Max(pattern.Height, 1);

        using var tileBitmap = new SKBitmap(tileWidth, tileHeight);
        using var tileCanvas = new SKCanvas(tileBitmap);

        // Draw a simple checkered placeholder pattern
        var color1 = new SKColor(200, 200, 200);
        var color2 = new SKColor(150, 150, 150);

        using var paint1 = new SKPaint { Color = color1 };
        using var paint2 = new SKPaint { Color = color2 };

        var halfWidth = tileWidth / 2;
        var halfHeight = tileHeight / 2;

        tileCanvas.DrawRect(0, 0, halfWidth, halfHeight, paint1);
        tileCanvas.DrawRect(halfWidth, 0, halfWidth, halfHeight, paint2);
        tileCanvas.DrawRect(0, halfHeight, halfWidth, halfHeight, paint2);
        tileCanvas.DrawRect(halfWidth, halfHeight, halfWidth, halfHeight, paint1);

        var fallbackShader = SKShader.CreateBitmap(
            tileBitmap,
            SKShaderTileMode.Repeat,
            SKShaderTileMode.Repeat);

        // Apply offset if specified
        if (pattern.X != 0 || pattern.Y != 0)
        {
            var fallbackMatrix = SKMatrix.CreateTranslation((float)pattern.X, (float)pattern.Y);
            fallbackShader = fallbackShader.WithLocalMatrix(fallbackMatrix);
        }

        return new SKPaint
        {
            Style = SKPaintStyle.Fill,
            Shader = fallbackShader,
            IsAntialias = true
        };
    }

    /// <summary>
    /// Extracts colors and positions from gradient stops.
    /// </summary>
    private static (SKColor[] colors, float[] positions) ExtractGradientStops(List<GradientStop> stops)
    {
        if (stops.Count == 0)
        {
            // Default to transparent-to-transparent if no stops
            return ([SKColors.Transparent, SKColors.Transparent], [0f, 1f]);
        }

        // Sort stops by offset
        var sortedStops = stops.OrderBy(s => s.Offset).ToList();

        var colors = new SKColor[sortedStops.Count];
        var positions = new float[sortedStops.Count];

        for (int i = 0; i < sortedStops.Count; i++)
        {
            colors[i] = new SKColor(sortedStops[i].Color);
            positions[i] = (float)sortedStops[i].Offset;
        }

        return (colors, positions);
    }

    /// <summary>
    /// Converts gradient spread mode to SkiaSharp tile mode.
    /// </summary>
    private static SKShaderTileMode ConvertSpreadMode(GradientSpreadMode mode) => mode switch
    {
        GradientSpreadMode.Pad => SKShaderTileMode.Clamp,
        GradientSpreadMode.Reflect => SKShaderTileMode.Mirror,
        GradientSpreadMode.Repeat => SKShaderTileMode.Repeat,
        _ => SKShaderTileMode.Clamp
    };
}
