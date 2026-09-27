using System.Globalization;
using System.Text;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

namespace Bezier.Core.Services;

/// <summary>
/// Options for SVG export.
/// </summary>
public record SvgExportOptions
{
    /// <summary>Whether to minify the output (no formatting/whitespace).</summary>
    public bool Minify { get; init; }

    /// <summary>Whether to preserve element IDs in the output.</summary>
    public bool PreserveIds { get; init; } = true;

    /// <summary>Whether to include the XML declaration.</summary>
    public bool IncludeXmlDeclaration { get; init; } = true;

    /// <summary>Whether to include viewBox attribute.</summary>
    public bool IncludeViewBox { get; init; } = true;

    /// <summary>Number of decimal places for numeric values.</summary>
    public int DecimalPrecision { get; init; } = 3;

    /// <summary>Whether to use inline styles (style attribute) vs presentation attributes.</summary>
    public bool UseInlineStyles { get; init; }

    /// <summary>Default options for standard export.</summary>
    public static SvgExportOptions Default => new();

    /// <summary>Options optimized for minimal file size.</summary>
    public static SvgExportOptions Minified => new()
    {
        Minify = true,
        IncludeXmlDeclaration = false,
        DecimalPrecision = 2
    };
}

/// <summary>
/// Exports VectorDocument to SVG format.
/// </summary>
public class SvgExporter
{
    private SvgExportOptions _options = SvgExportOptions.Default;
    private StringBuilder _sb = new();
    private int _indentLevel;
    private int _gradientIdCounter;
    private readonly Dictionary<IFill, string> _gradientIds = new();

    /// <summary>
    /// Exports a VectorDocument to an SVG string.
    /// </summary>
    public string Export(VectorDocument document, SvgExportOptions? options = null)
    {
        _options = options ?? SvgExportOptions.Default;
        _sb = new StringBuilder();
        _indentLevel = 0;
        _gradientIdCounter = 0;
        _gradientIds.Clear();

        // Collect gradients first
        CollectGradients(document);

        // XML declaration
        if (_options.IncludeXmlDeclaration)
        {
            AppendLine("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
        }

        // SVG root element
        var svgAttrs = new List<string>
        {
            "xmlns=\"http://www.w3.org/2000/svg\"",
            $"width=\"{FormatNumber(document.Width)}\"",
            $"height=\"{FormatNumber(document.Height)}\""
        };

        if (_options.IncludeViewBox)
        {
            var vb = document.ViewBox;
            svgAttrs.Add($"viewBox=\"{FormatNumber(vb.MinX)} {FormatNumber(vb.MinY)} {FormatNumber(vb.Width)} {FormatNumber(vb.Height)}\"");
        }

        AppendLine($"<svg {string.Join(" ", svgAttrs)}>");
        _indentLevel++;

        // Title and description
        if (!string.IsNullOrEmpty(document.Title) && document.Title != "Untitled")
        {
            AppendLine($"<title>{EscapeXml(document.Title)}</title>");
        }

        if (!string.IsNullOrEmpty(document.Description))
        {
            AppendLine($"<desc>{EscapeXml(document.Description)}</desc>");
        }

        // Defs section for gradients
        if (_gradientIds.Count > 0)
        {
            AppendLine("<defs>");
            _indentLevel++;
            ExportGradientDefs();
            _indentLevel--;
            AppendLine("</defs>");
        }

        // Export elements
        foreach (var element in document.Elements)
        {
            ExportElement(element);
        }

        _indentLevel--;
        AppendLine("</svg>");

        return _sb.ToString();
    }

    /// <summary>
    /// Exports a VectorDocument to an SVG file.
    /// </summary>
    public void ExportToFile(VectorDocument document, string filePath, SvgExportOptions? options = null)
    {
        var svg = Export(document, options);
        File.WriteAllText(filePath, svg, Encoding.UTF8);
    }

    private void CollectGradients(VectorDocument document)
    {
        foreach (var element in document.Elements)
        {
            CollectGradientsFromElement(element);
        }
    }

    private void CollectGradientsFromElement(VectorElement element)
    {
        RegisterGradient(element.Fill);
        RegisterGradient(element.Stroke?.Fill);

        if (element is SvgGroup group)
        {
            foreach (var child in group.Children)
            {
                CollectGradientsFromElement(child);
            }
        }
    }

    private void RegisterGradient(IFill? fill)
    {
        if (fill is LinearGradientFill or RadialGradientFill)
        {
            if (!_gradientIds.ContainsKey(fill))
            {
                _gradientIds[fill] = $"gradient{++_gradientIdCounter}";
            }
        }
    }

    private void ExportGradientDefs()
    {
        foreach (var (fill, id) in _gradientIds)
        {
            switch (fill)
            {
                case LinearGradientFill linear:
                    ExportLinearGradient(linear, id);
                    break;
                case RadialGradientFill radial:
                    ExportRadialGradient(radial, id);
                    break;
            }
        }
    }

    private void ExportLinearGradient(LinearGradientFill gradient, string id)
    {
        var attrs = new List<string>
        {
            $"id=\"{id}\"",
            $"x1=\"{FormatNumber(gradient.StartX * 100)}%\"",
            $"y1=\"{FormatNumber(gradient.StartY * 100)}%\"",
            $"x2=\"{FormatNumber(gradient.EndX * 100)}%\"",
            $"y2=\"{FormatNumber(gradient.EndY * 100)}%\""
        };

        if (gradient.SpreadMode != GradientSpreadMode.Pad)
        {
            attrs.Add($"spreadMethod=\"{gradient.SpreadMode.ToString().ToLowerInvariant()}\"");
        }

        AppendLine($"<linearGradient {string.Join(" ", attrs)}>");
        _indentLevel++;
        ExportGradientStops(gradient.Stops);
        _indentLevel--;
        AppendLine("</linearGradient>");
    }

    private void ExportRadialGradient(RadialGradientFill gradient, string id)
    {
        var attrs = new List<string>
        {
            $"id=\"{id}\"",
            $"cx=\"{FormatNumber(gradient.CenterX * 100)}%\"",
            $"cy=\"{FormatNumber(gradient.CenterY * 100)}%\"",
            $"r=\"{FormatNumber(gradient.RadiusX * 100)}%\""
        };

        // Add focal point if different from center
        if (Math.Abs(gradient.FocalX - gradient.CenterX) > 0.001 ||
            Math.Abs(gradient.FocalY - gradient.CenterY) > 0.001)
        {
            attrs.Add($"fx=\"{FormatNumber(gradient.FocalX * 100)}%\"");
            attrs.Add($"fy=\"{FormatNumber(gradient.FocalY * 100)}%\"");
        }

        if (gradient.SpreadMode != GradientSpreadMode.Pad)
        {
            attrs.Add($"spreadMethod=\"{gradient.SpreadMode.ToString().ToLowerInvariant()}\"");
        }

        AppendLine($"<radialGradient {string.Join(" ", attrs)}>");
        _indentLevel++;
        ExportGradientStops(gradient.Stops);
        _indentLevel--;
        AppendLine("</radialGradient>");
    }

    private void ExportGradientStops(List<GradientStop> stops)
    {
        foreach (var stop in stops)
        {
            var color = stop.Color;
            var alpha = (color >> 24) & 0xFF;
            var r = (color >> 16) & 0xFF;
            var g = (color >> 8) & 0xFF;
            var b = color & 0xFF;

            var attrs = new List<string>
            {
                $"offset=\"{FormatNumber(stop.Offset * 100)}%\"",
                $"stop-color=\"#{r:X2}{g:X2}{b:X2}\""
            };

            if (alpha < 255)
            {
                attrs.Add($"stop-opacity=\"{FormatNumber(alpha / 255.0)}\"");
            }

            AppendLine($"<stop {string.Join(" ", attrs)}/>");
        }
    }

    private void ExportElement(VectorElement element)
    {
        if (!element.IsVisible) return;

        switch (element)
        {
            case SvgRect rect:
                ExportRect(rect);
                break;
            case SvgCircle circle:
                ExportCircle(circle);
                break;
            case SvgEllipse ellipse:
                ExportEllipse(ellipse);
                break;
            case SvgLine line:
                ExportLine(line);
                break;
            case SvgPath path:
                ExportPath(path);
                break;
            case SvgPolygon polygon:
                ExportPolygon(polygon);
                break;
            case SvgPolyline polyline:
                ExportPolyline(polyline);
                break;
            case SvgText text:
                ExportText(text);
                break;
            case SvgImage image:
                ExportImage(image);
                break;
            case SvgGroup group:
                ExportGroup(group);
                break;
        }
    }

    private void ExportRect(SvgRect rect)
    {
        var attrs = new List<string>
        {
            $"x=\"{FormatNumber(rect.X)}\"",
            $"y=\"{FormatNumber(rect.Y)}\"",
            $"width=\"{FormatNumber(rect.Width)}\"",
            $"height=\"{FormatNumber(rect.Height)}\""
        };

        if (rect.Rx > 0) attrs.Add($"rx=\"{FormatNumber(rect.Rx)}\"");
        if (rect.Ry > 0) attrs.Add($"ry=\"{FormatNumber(rect.Ry)}\"");

        attrs.AddRange(GetCommonAttributes(rect));
        AppendLine($"<rect {string.Join(" ", attrs)}/>");
    }

    private void ExportCircle(SvgCircle circle)
    {
        var attrs = new List<string>
        {
            $"cx=\"{FormatNumber(circle.Cx)}\"",
            $"cy=\"{FormatNumber(circle.Cy)}\"",
            $"r=\"{FormatNumber(circle.R)}\""
        };

        attrs.AddRange(GetCommonAttributes(circle));
        AppendLine($"<circle {string.Join(" ", attrs)}/>");
    }

    private void ExportEllipse(SvgEllipse ellipse)
    {
        var attrs = new List<string>
        {
            $"cx=\"{FormatNumber(ellipse.Cx)}\"",
            $"cy=\"{FormatNumber(ellipse.Cy)}\"",
            $"rx=\"{FormatNumber(ellipse.Rx)}\"",
            $"ry=\"{FormatNumber(ellipse.Ry)}\""
        };

        attrs.AddRange(GetCommonAttributes(ellipse));
        AppendLine($"<ellipse {string.Join(" ", attrs)}/>");
    }

    private void ExportLine(SvgLine line)
    {
        var attrs = new List<string>
        {
            $"x1=\"{FormatNumber(line.X1)}\"",
            $"y1=\"{FormatNumber(line.Y1)}\"",
            $"x2=\"{FormatNumber(line.X2)}\"",
            $"y2=\"{FormatNumber(line.Y2)}\""
        };

        attrs.AddRange(GetCommonAttributes(line));
        AppendLine($"<line {string.Join(" ", attrs)}/>");
    }

    private void ExportPath(SvgPath path)
    {
        var attrs = new List<string> { $"d=\"{path.PathData}\"" };
        attrs.AddRange(GetCommonAttributes(path));
        AppendLine($"<path {string.Join(" ", attrs)}/>");
    }

    private void ExportPolygon(SvgPolygon polygon)
    {
        var points = string.Join(" ", polygon.Points.Select(p => $"{FormatNumber(p.X)},{FormatNumber(p.Y)}"));
        var attrs = new List<string> { $"points=\"{points}\"" };
        attrs.AddRange(GetCommonAttributes(polygon));
        AppendLine($"<polygon {string.Join(" ", attrs)}/>");
    }

    private void ExportPolyline(SvgPolyline polyline)
    {
        var points = string.Join(" ", polyline.Points.Select(p => $"{FormatNumber(p.X)},{FormatNumber(p.Y)}"));
        var attrs = new List<string> { $"points=\"{points}\"" };
        attrs.AddRange(GetCommonAttributes(polyline));
        AppendLine($"<polyline {string.Join(" ", attrs)}/>");
    }

    private void ExportText(SvgText text)
    {
        var attrs = new List<string>
        {
            $"x=\"{FormatNumber(text.X)}\"",
            $"y=\"{FormatNumber(text.Y)}\"",
            $"font-family=\"{text.FontFamily}\"",
            $"font-size=\"{FormatNumber(text.FontSize)}\""
        };

        if (text.FontWeight != 400)
            attrs.Add($"font-weight=\"{text.FontWeight}\"");
        if (text.Italic)
            attrs.Add("font-style=\"italic\"");
        if (text.TextAnchor != TextAnchor.Start)
            attrs.Add($"text-anchor=\"{text.TextAnchor.ToString().ToLowerInvariant()}\"");

        attrs.AddRange(GetCommonAttributes(text));
        AppendLine($"<text {string.Join(" ", attrs)}>{EscapeXml(text.Text)}</text>");
    }

    private void ExportImage(SvgImage image)
    {
        var attrs = new List<string>
        {
            $"x=\"{FormatNumber(image.X)}\"",
            $"y=\"{FormatNumber(image.Y)}\"",
            $"width=\"{FormatNumber(image.Width)}\"",
            $"height=\"{FormatNumber(image.Height)}\""
        };

        if (image.IsEmbedded && image.EmbeddedData is not null)
        {
            var base64 = Convert.ToBase64String(image.EmbeddedData);
            attrs.Add($"href=\"data:{image.MimeType};base64,{base64}\"");
        }
        else if (!string.IsNullOrEmpty(image.Href))
        {
            attrs.Add($"href=\"{EscapeXml(image.Href)}\"");
        }

        attrs.AddRange(GetCommonAttributes(image));
        AppendLine($"<image {string.Join(" ", attrs)}/>");
    }

    private void ExportGroup(SvgGroup group)
    {
        var attrs = GetCommonAttributes(group);

        if (group.Children.Count == 0 && attrs.Count == 0)
            return;

        var attrStr = attrs.Count > 0 ? " " + string.Join(" ", attrs) : "";
        AppendLine($"<g{attrStr}>");
        _indentLevel++;

        foreach (var child in group.Children)
        {
            ExportElement(child);
        }

        _indentLevel--;
        AppendLine("</g>");
    }

    private List<string> GetCommonAttributes(VectorElement element)
    {
        var attrs = new List<string>();

        // ID
        if (_options.PreserveIds && !string.IsNullOrEmpty(element.Name))
        {
            attrs.Add($"id=\"{EscapeXml(element.Name)}\"");
        }

        // Fill
        var fillStr = GetFillString(element.Fill);
        if (!string.IsNullOrEmpty(fillStr))
        {
            attrs.Add($"fill=\"{fillStr}\"");
        }
        else if (element.Fill is null && element is not SvgLine)
        {
            attrs.Add("fill=\"none\"");
        }

        // Stroke
        if (element.Stroke is { IsVisible: true })
        {
            var strokeFillStr = GetFillString(element.Stroke.Fill);
            if (!string.IsNullOrEmpty(strokeFillStr))
            {
                attrs.Add($"stroke=\"{strokeFillStr}\"");
            }

            if (Math.Abs(element.Stroke.Width - 1) > 0.001)
            {
                attrs.Add($"stroke-width=\"{FormatNumber(element.Stroke.Width)}\"");
            }

            if (element.Stroke.LineCap != LineCap.Butt)
            {
                attrs.Add($"stroke-linecap=\"{element.Stroke.LineCap.ToString().ToLowerInvariant()}\"");
            }

            if (element.Stroke.LineJoin != LineJoin.Miter)
            {
                attrs.Add($"stroke-linejoin=\"{element.Stroke.LineJoin.ToString().ToLowerInvariant()}\"");
            }

            if (element.Stroke.DashArray is { Length: > 0 })
            {
                attrs.Add($"stroke-dasharray=\"{string.Join(",", element.Stroke.DashArray.Select(FormatNumber))}\"");
            }

            if (Math.Abs(element.Stroke.DashOffset) > 0.001)
            {
                attrs.Add($"stroke-dashoffset=\"{FormatNumber(element.Stroke.DashOffset)}\"");
            }

            if (Math.Abs(element.Stroke.MiterLimit - 4) > 0.001)
            {
                attrs.Add($"stroke-miterlimit=\"{FormatNumber(element.Stroke.MiterLimit)}\"");
            }
        }

        // Opacity
        if (Math.Abs(element.Opacity - 1.0) > 0.001)
        {
            attrs.Add($"opacity=\"{FormatNumber(element.Opacity)}\"");
        }

        // Transform
        if (!element.Transform.IsIdentity)
        {
            attrs.Add($"transform=\"{element.Transform.ToSvgString()}\"");
        }

        return attrs;
    }

    private string? GetFillString(IFill? fill)
    {
        return fill switch
        {
            null => null,
            NoneFill => "none",
            SolidFill solid => FormatColor(solid.Color),
            LinearGradientFill linear when _gradientIds.TryGetValue(linear, out var id) => $"url(#{id})",
            RadialGradientFill radial when _gradientIds.TryGetValue(radial, out var id) => $"url(#{id})",
            _ => null
        };
    }

    private static string FormatColor(uint color)
    {
        var a = (color >> 24) & 0xFF;
        var r = (color >> 16) & 0xFF;
        var g = (color >> 8) & 0xFF;
        var b = color & 0xFF;

        if (a == 255)
        {
            return $"#{r:X2}{g:X2}{b:X2}";
        }
        else
        {
            return $"rgba({r},{g},{b},{a / 255.0:F2})";
        }
    }

    private string FormatNumber(double value)
    {
        // Remove unnecessary decimal places
        var formatted = value.ToString($"F{_options.DecimalPrecision}", CultureInfo.InvariantCulture);
        
        // Trim trailing zeros after decimal point
        if (formatted.Contains('.'))
        {
            formatted = formatted.TrimEnd('0').TrimEnd('.');
        }

        return formatted;
    }

    private void AppendLine(string line)
    {
        if (_options.Minify)
        {
            _sb.Append(line);
        }
        else
        {
            _sb.Append(new string(' ', _indentLevel * 2));
            _sb.AppendLine(line);
        }
    }

    private static string EscapeXml(string text)
    {
        return text
            .Replace("&", "&amp;")
            .Replace("<", "&lt;")
            .Replace(">", "&gt;")
            .Replace("\"", "&quot;")
            .Replace("'", "&apos;");
    }
}
