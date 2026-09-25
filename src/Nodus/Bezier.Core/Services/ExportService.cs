using System.Text;
using System.Text.RegularExpressions;
using System.Xml;

namespace Bezier.Core.Services;

/// <summary>
/// Supported export formats.
/// </summary>
public enum ExportFormat
{
    Svg,
    SvgOptimized,
    SvgMinified,
    Png,
    Jpg,
    WebP,
    Pdf,
    Xaml,
    ReactComponent,
    VueComponent,
    CssClipPath,
    Ico
}

/// <summary>
/// Options for SVG processing/optimization during export.
/// </summary>
public class SvgProcessingOptions
{
    public bool RemoveComments { get; set; } = true;
    public bool RemoveMetadata { get; set; } = true;
    public bool RemoveEditorData { get; set; } = true;
    public bool RemoveEmptyGroups { get; set; } = true;
    public bool RemoveUnusedDefs { get; set; } = true;
    public bool CollapseGroups { get; set; } = false;
    public bool ConvertColorsToHex { get; set; } = true;
    public bool ShortenIds { get; set; } = false;
    public bool RemoveDefaultValues { get; set; } = true;
    public int DecimalPrecision { get; set; } = 2;
    public bool Minify { get; set; } = false;
    public bool PrettyPrint { get; set; } = true;
}

/// <summary>
/// Options for raster image export.
/// </summary>
public class RasterExportOptions
{
    public double Scale { get; set; } = 1.0;
    public int? Width { get; set; }
    public int? Height { get; set; }
    public int Dpi { get; set; } = 96;
    public bool Transparent { get; set; } = true;
    public string? BackgroundColor { get; set; }
    public int JpegQuality { get; set; } = 90;
    public int WebPQuality { get; set; } = 90;
}

/// <summary>
/// Options for ICO export.
/// </summary>
public class IcoExportOptions
{
    public int[] Sizes { get; set; } = [16, 32, 48, 64, 128, 256];
    public bool IncludePng { get; set; } = true;
}

/// <summary>
/// Options for code export.
/// </summary>
public class CodeExportOptions
{
    public string ComponentName { get; set; } = "SvgIcon";
    public bool UseTypeScript { get; set; } = false;
    public bool IncludeProps { get; set; } = true;
    public string IndentString { get; set; } = "  ";
}

/// <summary>
/// Result of an export operation.
/// </summary>
public class ExportResult
{
    public bool Success { get; init; }
    public byte[]? Data { get; init; }
    public string? TextContent { get; init; }
    public string? ErrorMessage { get; init; }
    public ExportFormat Format { get; init; }
    public string? SuggestedFileName { get; init; }
    public string? MimeType { get; init; }

    public static ExportResult Succeeded(byte[] data, ExportFormat format, string? fileName = null, string? mimeType = null)
    {
        return new ExportResult
        {
            Success = true,
            Data = data,
            Format = format,
            SuggestedFileName = fileName,
            MimeType = mimeType
        };
    }

    public static ExportResult Succeeded(string textContent, ExportFormat format, string? fileName = null, string? mimeType = null)
    {
        return new ExportResult
        {
            Success = true,
            TextContent = textContent,
            Data = Encoding.UTF8.GetBytes(textContent),
            Format = format,
            SuggestedFileName = fileName,
            MimeType = mimeType
        };
    }

    public static ExportResult Failed(string errorMessage, ExportFormat format)
    {
        return new ExportResult
        {
            Success = false,
            ErrorMessage = errorMessage,
            Format = format
        };
    }
}

/// <summary>
/// Service for exporting SVG to various formats.
/// </summary>
public partial class ExportService
{
    /// <summary>
    /// Gets the file extension for a format.
    /// </summary>
    public static string GetFileExtension(ExportFormat format)
    {
        return format switch
        {
            ExportFormat.Svg or ExportFormat.SvgOptimized or ExportFormat.SvgMinified => ".svg",
            ExportFormat.Png => ".png",
            ExportFormat.Jpg => ".jpg",
            ExportFormat.WebP => ".webp",
            ExportFormat.Pdf => ".pdf",
            ExportFormat.Xaml => ".xaml",
            ExportFormat.ReactComponent => ".tsx",
            ExportFormat.VueComponent => ".vue",
            ExportFormat.CssClipPath => ".css",
            ExportFormat.Ico => ".ico",
            _ => ".svg"
        };
    }

    /// <summary>
    /// Gets the MIME type for a format.
    /// </summary>
    public static string GetMimeType(ExportFormat format)
    {
        return format switch
        {
            ExportFormat.Svg or ExportFormat.SvgOptimized or ExportFormat.SvgMinified => "image/svg+xml",
            ExportFormat.Png => "image/png",
            ExportFormat.Jpg => "image/jpeg",
            ExportFormat.WebP => "image/webp",
            ExportFormat.Pdf => "application/pdf",
            ExportFormat.Xaml => "application/xaml+xml",
            ExportFormat.ReactComponent or ExportFormat.VueComponent => "text/javascript",
            ExportFormat.CssClipPath => "text/css",
            ExportFormat.Ico => "image/x-icon",
            _ => "application/octet-stream"
        };
    }

    /// <summary>
    /// Gets the file filter for save dialog.
    /// </summary>
    public static string GetSaveFilter()
    {
        return "SVG|*.svg|" +
               "PNG|*.png|" +
               "JPEG|*.jpg|" +
               "WebP|*.webp|" +
               "PDF|*.pdf|" +
               "XAML|*.xaml|" +
               "React Component|*.tsx|" +
               "Vue Component|*.vue|" +
               "CSS|*.css|" +
               "ICO|*.ico";
    }

    /// <summary>
    /// Exports SVG to standard format.
    /// </summary>
    public ExportResult ExportSvg(string svgContent, SvgProcessingOptions? options = null)
    {
        options ??= new SvgProcessingOptions();

        try
        {
            var processed = ProcessSvg(svgContent, options);
            return ExportResult.Succeeded(processed, ExportFormat.Svg, "export.svg", "image/svg+xml");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"SVG export failed: {ex.Message}", ExportFormat.Svg);
        }
    }

    /// <summary>
    /// Exports SVG in optimized format (SVGO-style).
    /// </summary>
    public ExportResult ExportSvgOptimized(string svgContent)
    {
        var options = new SvgProcessingOptions
        {
            RemoveComments = true,
            RemoveMetadata = true,
            RemoveEditorData = true,
            RemoveEmptyGroups = true,
            RemoveUnusedDefs = true,
            CollapseGroups = true,
            ConvertColorsToHex = true,
            ShortenIds = true,
            RemoveDefaultValues = true,
            DecimalPrecision = 2,
            Minify = false,
            PrettyPrint = true
        };

        try
        {
            var processed = ProcessSvg(svgContent, options);
            return ExportResult.Succeeded(processed, ExportFormat.SvgOptimized, "export-optimized.svg", "image/svg+xml");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"SVG optimization failed: {ex.Message}", ExportFormat.SvgOptimized);
        }
    }

    /// <summary>
    /// Exports SVG in minified format.
    /// </summary>
    public ExportResult ExportSvgMinified(string svgContent)
    {
        var options = new SvgProcessingOptions
        {
            RemoveComments = true,
            RemoveMetadata = true,
            RemoveEditorData = true,
            RemoveEmptyGroups = true,
            RemoveUnusedDefs = true,
            CollapseGroups = true,
            ConvertColorsToHex = true,
            ShortenIds = true,
            RemoveDefaultValues = true,
            DecimalPrecision = 1,
            Minify = true,
            PrettyPrint = false
        };

        try
        {
            var processed = ProcessSvg(svgContent, options);
            return ExportResult.Succeeded(processed, ExportFormat.SvgMinified, "export.min.svg", "image/svg+xml");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"SVG minification failed: {ex.Message}", ExportFormat.SvgMinified);
        }
    }

    /// <summary>
    /// Exports SVG as XAML (WPF DrawingImage).
    /// </summary>
    public ExportResult ExportXaml(string svgContent, CodeExportOptions? options = null)
    {
        options ??= new CodeExportOptions();

        try
        {
            var xaml = ConvertToXaml(svgContent, options);
            return ExportResult.Succeeded(xaml, ExportFormat.Xaml, $"{options.ComponentName}.xaml", "application/xaml+xml");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"XAML export failed: {ex.Message}", ExportFormat.Xaml);
        }
    }

    /// <summary>
    /// Exports SVG as React component.
    /// </summary>
    public ExportResult ExportReactComponent(string svgContent, CodeExportOptions? options = null)
    {
        options ??= new CodeExportOptions();

        try
        {
            var component = ConvertToReactComponent(svgContent, options);
            var ext = options.UseTypeScript ? ".tsx" : ".jsx";
            return ExportResult.Succeeded(component, ExportFormat.ReactComponent, $"{options.ComponentName}{ext}", "text/javascript");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"React export failed: {ex.Message}", ExportFormat.ReactComponent);
        }
    }

    /// <summary>
    /// Exports SVG as Vue component.
    /// </summary>
    public ExportResult ExportVueComponent(string svgContent, CodeExportOptions? options = null)
    {
        options ??= new CodeExportOptions();

        try
        {
            var component = ConvertToVueComponent(svgContent, options);
            return ExportResult.Succeeded(component, ExportFormat.VueComponent, $"{options.ComponentName}.vue", "text/javascript");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"Vue export failed: {ex.Message}", ExportFormat.VueComponent);
        }
    }

    /// <summary>
    /// Exports SVG path as CSS clip-path.
    /// </summary>
    public ExportResult ExportCssClipPath(string svgContent, string? className = null)
    {
        try
        {
            var css = ConvertToCssClipPath(svgContent, className ?? "clip-shape");
            return ExportResult.Succeeded(css, ExportFormat.CssClipPath, "clip-path.css", "text/css");
        }
        catch (Exception ex)
        {
            return ExportResult.Failed($"CSS export failed: {ex.Message}", ExportFormat.CssClipPath);
        }
    }

    /// <summary>
    /// Gets raster export data info (dimensions, etc.) - actual rendering requires SkiaSharp in Desktop.
    /// </summary>
    public (int Width, int Height) CalculateRasterDimensions(string svgContent, RasterExportOptions options)
    {
        var (svgWidth, svgHeight) = GetSvgDimensions(svgContent);

        if (options.Width.HasValue && options.Height.HasValue)
        {
            return (options.Width.Value, options.Height.Value);
        }

        if (options.Width.HasValue)
        {
            var ratio = options.Width.Value / svgWidth;
            return (options.Width.Value, (int)(svgHeight * ratio));
        }

        if (options.Height.HasValue)
        {
            var ratio = options.Height.Value / svgHeight;
            return ((int)(svgWidth * ratio), options.Height.Value);
        }

        return ((int)(svgWidth * options.Scale), (int)(svgHeight * options.Scale));
    }

    /// <summary>
    /// Gets SVG dimensions from content.
    /// </summary>
    public static (double Width, double Height) GetSvgDimensions(string svgContent)
    {
        try
        {
            var doc = new XmlDocument();
            doc.LoadXml(svgContent);
            var root = doc.DocumentElement;

            if (root == null) return (100, 100);

            var widthAttr = root.GetAttribute("width");
            var heightAttr = root.GetAttribute("height");
            var viewBox = root.GetAttribute("viewBox");

            if (!string.IsNullOrEmpty(viewBox))
            {
                var parts = viewBox.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length >= 4)
                {
                    if (double.TryParse(parts[2], out var vbWidth) && double.TryParse(parts[3], out var vbHeight))
                    {
                        if (string.IsNullOrEmpty(widthAttr)) return (vbWidth, vbHeight);
                    }
                }
            }

            var width = ParseDimension(widthAttr, 100);
            var height = ParseDimension(heightAttr, 100);

            return (width, height);
        }
        catch
        {
            return (100, 100);
        }
    }

    private static double ParseDimension(string value, double defaultValue)
    {
        if (string.IsNullOrEmpty(value)) return defaultValue;

        // Remove units
        var numericPart = DimensionRegex().Replace(value, "");
        return double.TryParse(numericPart, out var result) ? result : defaultValue;
    }

    private string ProcessSvg(string svgContent, SvgProcessingOptions options)
    {
        var doc = new XmlDocument();
        doc.PreserveWhitespace = !options.Minify;
        doc.LoadXml(svgContent);

        if (options.RemoveComments)
        {
            RemoveComments(doc);
        }

        if (options.RemoveMetadata)
        {
            RemoveElements(doc, ["metadata", "title", "desc"]);
        }

        if (options.RemoveEditorData)
        {
            RemoveEditorAttributes(doc);
        }

        if (options.RemoveEmptyGroups)
        {
            RemoveEmptyGroups(doc);
        }

        if (options.RemoveDefaultValues)
        {
            RemoveDefaultAttributes(doc);
        }

        if (options.ConvertColorsToHex)
        {
            ConvertColorsToHex(doc);
        }

        if (options.DecimalPrecision < 6)
        {
            RoundNumbers(doc, options.DecimalPrecision);
        }

        var settings = new XmlWriterSettings
        {
            Indent = options.PrettyPrint && !options.Minify,
            IndentChars = "  ",
            NewLineChars = options.Minify ? "" : "\n",
            OmitXmlDeclaration = true
        };

        var sb = new StringBuilder();
        using (var writer = XmlWriter.Create(sb, settings))
        {
            doc.Save(writer);
        }

        var result = sb.ToString();

        if (options.Minify)
        {
            result = MinifyRegex().Replace(result, "><");
            result = result.Trim();
        }

        return result;
    }

    private static void RemoveComments(XmlDocument doc)
    {
        var comments = doc.SelectNodes("//comment()");
        if (comments != null)
        {
            foreach (XmlComment comment in comments)
            {
                comment.ParentNode?.RemoveChild(comment);
            }
        }
    }

    private static void RemoveElements(XmlDocument doc, string[] elementNames)
    {
        foreach (var name in elementNames)
        {
            var nodes = doc.GetElementsByTagName(name);
            for (var i = nodes.Count - 1; i >= 0; i--)
            {
                nodes[i]?.ParentNode?.RemoveChild(nodes[i]!);
            }
        }
    }

    private static void RemoveEditorAttributes(XmlDocument doc)
    {
        var nodes = doc.SelectNodes("//*");
        if (nodes == null) return;

        var editorPrefixes = new[] { "inkscape:", "sodipodi:", "sketch:", "ai:" };
        foreach (XmlElement node in nodes)
        {
            var attrsToRemove = new List<string>();
            foreach (XmlAttribute attr in node.Attributes)
            {
                if (editorPrefixes.Any(p => attr.Name.StartsWith(p, StringComparison.OrdinalIgnoreCase)))
                {
                    attrsToRemove.Add(attr.Name);
                }
            }
            foreach (var name in attrsToRemove)
            {
                node.RemoveAttribute(name);
            }
        }
    }

    private static void RemoveEmptyGroups(XmlDocument doc)
    {
        bool removed;
        do
        {
            removed = false;
            var groups = doc.GetElementsByTagName("g");
            for (var i = groups.Count - 1; i >= 0; i--)
            {
                var g = groups[i];
                if (g?.ChildNodes.Count == 0)
                {
                    g.ParentNode?.RemoveChild(g);
                    removed = true;
                }
            }
        } while (removed);
    }

    private static void RemoveDefaultAttributes(XmlDocument doc)
    {
        var defaults = new Dictionary<string, string>
        {
            ["fill-opacity"] = "1",
            ["stroke-opacity"] = "1",
            ["opacity"] = "1",
            ["stroke-width"] = "1",
            ["stroke-linecap"] = "butt",
            ["stroke-linejoin"] = "miter",
            ["stroke-dashoffset"] = "0",
            ["fill-rule"] = "nonzero"
        };

        var nodes = doc.SelectNodes("//*");
        if (nodes == null) return;

        foreach (XmlElement node in nodes)
        {
            foreach (var kvp in defaults)
            {
                if (node.GetAttribute(kvp.Key) == kvp.Value)
                {
                    node.RemoveAttribute(kvp.Key);
                }
            }
        }
    }

    private static void ConvertColorsToHex(XmlDocument doc)
    {
        var colorAttrs = new[] { "fill", "stroke", "stop-color", "flood-color", "lighting-color" };
        var nodes = doc.SelectNodes("//*");
        if (nodes == null) return;

        foreach (XmlElement node in nodes)
        {
            foreach (var attr in colorAttrs)
            {
                var value = node.GetAttribute(attr);
                if (!string.IsNullOrEmpty(value))
                {
                    var hex = ConvertColorToHex(value);
                    if (hex != value)
                    {
                        node.SetAttribute(attr, hex);
                    }
                }
            }
        }
    }

    private static string ConvertColorToHex(string color)
    {
        if (color.StartsWith('#')) return color;

        var match = RgbColorRegex().Match(color);
        if (match.Success)
        {
            var r = int.Parse(match.Groups[1].Value);
            var g = int.Parse(match.Groups[2].Value);
            var b = int.Parse(match.Groups[3].Value);
            return $"#{r:X2}{g:X2}{b:X2}";
        }

        return color;
    }

    private static void RoundNumbers(XmlDocument doc, int precision)
    {
        var numericAttrs = new[] { "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "width", "height" };
        var nodes = doc.SelectNodes("//*");
        if (nodes == null) return;

        foreach (XmlElement node in nodes)
        {
            foreach (var attr in numericAttrs)
            {
                var value = node.GetAttribute(attr);
                if (!string.IsNullOrEmpty(value) && double.TryParse(value, out var num))
                {
                    node.SetAttribute(attr, Math.Round(num, precision).ToString());
                }
            }
        }
    }

    private string ConvertToXaml(string svgContent, CodeExportOptions options)
    {
        var indent = options.IndentString;
        var doc = new XmlDocument();
        doc.LoadXml(svgContent);
        var root = doc.DocumentElement!;

        var (width, height) = GetSvgDimensions(svgContent);

        var sb = new StringBuilder();
        sb.AppendLine($"<DrawingImage x:Key=\"{options.ComponentName}\">");
        sb.AppendLine($"{indent}<DrawingImage.Drawing>");
        sb.AppendLine($"{indent}{indent}<DrawingGroup>");

        ConvertSvgElementToXaml(root, sb, indent + indent + indent);

        sb.AppendLine($"{indent}{indent}</DrawingGroup>");
        sb.AppendLine($"{indent}</DrawingImage.Drawing>");
        sb.AppendLine("</DrawingImage>");

        return sb.ToString();
    }

    private void ConvertSvgElementToXaml(XmlElement element, StringBuilder sb, string indent)
    {
        foreach (XmlNode child in element.ChildNodes)
        {
            if (child is not XmlElement el) continue;

            switch (el.Name.ToLowerInvariant())
            {
                case "rect":
                    var x = el.GetAttribute("x") ?? "0";
                    var y = el.GetAttribute("y") ?? "0";
                    var w = el.GetAttribute("width") ?? "0";
                    var h = el.GetAttribute("height") ?? "0";
                    var fill = el.GetAttribute("fill") ?? "#000000";
                    sb.AppendLine($"{indent}<GeometryDrawing Brush=\"{fill}\">");
                    sb.AppendLine($"{indent}  <GeometryDrawing.Geometry>");
                    sb.AppendLine($"{indent}    <RectangleGeometry Rect=\"{x},{y},{w},{h}\"/>");
                    sb.AppendLine($"{indent}  </GeometryDrawing.Geometry>");
                    sb.AppendLine($"{indent}</GeometryDrawing>");
                    break;

                case "circle":
                    var cx = el.GetAttribute("cx") ?? "0";
                    var cy = el.GetAttribute("cy") ?? "0";
                    var r = el.GetAttribute("r") ?? "0";
                    var cfill = el.GetAttribute("fill") ?? "#000000";
                    sb.AppendLine($"{indent}<GeometryDrawing Brush=\"{cfill}\">");
                    sb.AppendLine($"{indent}  <GeometryDrawing.Geometry>");
                    sb.AppendLine($"{indent}    <EllipseGeometry Center=\"{cx},{cy}\" RadiusX=\"{r}\" RadiusY=\"{r}\"/>");
                    sb.AppendLine($"{indent}  </GeometryDrawing.Geometry>");
                    sb.AppendLine($"{indent}</GeometryDrawing>");
                    break;

                case "path":
                    var d = el.GetAttribute("d");
                    var pfill = el.GetAttribute("fill") ?? "#000000";
                    if (!string.IsNullOrEmpty(d))
                    {
                        sb.AppendLine($"{indent}<GeometryDrawing Brush=\"{pfill}\" Geometry=\"{d}\"/>");
                    }
                    break;

                case "g":
                    sb.AppendLine($"{indent}<DrawingGroup>");
                    ConvertSvgElementToXaml(el, sb, indent + "  ");
                    sb.AppendLine($"{indent}</DrawingGroup>");
                    break;
            }
        }
    }

    private string ConvertToReactComponent(string svgContent, CodeExportOptions options)
    {
        var doc = new XmlDocument();
        doc.LoadXml(svgContent);
        var root = doc.DocumentElement!;

        var propsType = options.UseTypeScript ? ": React.SVGProps<SVGSVGElement>" : "";
        var propsParam = options.IncludeProps ? $"props{propsType}" : "";

        var sb = new StringBuilder();
        sb.AppendLine("import React from 'react';");
        sb.AppendLine();
        sb.AppendLine($"const {options.ComponentName} = ({propsParam}) => (");

        // Convert SVG to JSX
        var jsx = ConvertSvgToJsx(root, options.IndentString);
        sb.Append(jsx);

        sb.AppendLine(");");
        sb.AppendLine();
        sb.AppendLine($"export default {options.ComponentName};");

        return sb.ToString();
    }

    private string ConvertSvgToJsx(XmlElement element, string indent)
    {
        var sb = new StringBuilder();
        sb.Append($"{indent}<{element.Name}");

        foreach (XmlAttribute attr in element.Attributes)
        {
            var name = ConvertAttributeToJsx(attr.Name);
            sb.Append($" {name}=\"{attr.Value}\"");
        }

        sb.Append(" {...props}");

        if (element.ChildNodes.Count == 0)
        {
            sb.AppendLine(" />");
        }
        else
        {
            sb.AppendLine(">");
            foreach (XmlNode child in element.ChildNodes)
            {
                if (child is XmlElement el)
                {
                    sb.Append(ConvertChildToJsx(el, indent + "  "));
                }
            }
            sb.AppendLine($"{indent}</{element.Name}>");
        }

        return sb.ToString();
    }

    private string ConvertChildToJsx(XmlElement element, string indent)
    {
        var sb = new StringBuilder();
        sb.Append($"{indent}<{element.Name}");

        foreach (XmlAttribute attr in element.Attributes)
        {
            var name = ConvertAttributeToJsx(attr.Name);
            sb.Append($" {name}=\"{attr.Value}\"");
        }

        if (element.ChildNodes.Count == 0)
        {
            sb.AppendLine(" />");
        }
        else
        {
            sb.AppendLine(">");
            foreach (XmlNode child in element.ChildNodes)
            {
                if (child is XmlElement el)
                {
                    sb.Append(ConvertChildToJsx(el, indent + "  "));
                }
            }
            sb.AppendLine($"{indent}</{element.Name}>");
        }

        return sb.ToString();
    }

    private static string ConvertAttributeToJsx(string name)
    {
        return name switch
        {
            "class" => "className",
            "for" => "htmlFor",
            "clip-path" => "clipPath",
            "fill-rule" => "fillRule",
            "stroke-width" => "strokeWidth",
            "stroke-linecap" => "strokeLinecap",
            "stroke-linejoin" => "strokeLinejoin",
            "stroke-dasharray" => "strokeDasharray",
            "stroke-dashoffset" => "strokeDashoffset",
            "font-size" => "fontSize",
            "font-family" => "fontFamily",
            "text-anchor" => "textAnchor",
            _ => name.Contains('-') ? ToCamelCase(name) : name
        };
    }

    private static string ToCamelCase(string name)
    {
        var parts = name.Split('-');
        return parts[0] + string.Concat(parts.Skip(1).Select(p => char.ToUpper(p[0]) + p[1..]));
    }

    private string ConvertToVueComponent(string svgContent, CodeExportOptions options)
    {
        var doc = new XmlDocument();
        doc.LoadXml(svgContent);

        var sb = new StringBuilder();
        sb.AppendLine("<template>");
        sb.AppendLine($"  {svgContent.Trim()}");
        sb.AppendLine("</template>");
        sb.AppendLine();
        sb.AppendLine("<script>");
        sb.AppendLine("export default {");
        sb.AppendLine($"  name: '{options.ComponentName}'");
        sb.AppendLine("}");
        sb.AppendLine("</script>");

        return sb.ToString();
    }

    private string ConvertToCssClipPath(string svgContent, string className)
    {
        var doc = new XmlDocument();
        doc.LoadXml(svgContent);

        // Find path element
        var path = doc.GetElementsByTagName("path");
        if (path.Count == 0)
        {
            return $"/* No path found in SVG */\n.{className} {{\n  /* clip-path: path('...'); */\n}}";
        }

        var d = (path[0] as XmlElement)?.GetAttribute("d");
        if (string.IsNullOrEmpty(d))
        {
            return $"/* Path has no 'd' attribute */\n.{className} {{\n  /* clip-path: path('...'); */\n}}";
        }

        var sb = new StringBuilder();
        sb.AppendLine($".{className} {{");
        sb.AppendLine($"  clip-path: path('{d}');");
        sb.AppendLine("}");

        return sb.ToString();
    }

    [GeneratedRegex(@"[a-z%]+$", RegexOptions.IgnoreCase)]
    private static partial Regex DimensionRegex();

    [GeneratedRegex(@">\s+<")]
    private static partial Regex MinifyRegex();

    [GeneratedRegex(@"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")]
    private static partial Regex RgbColorRegex();
}
