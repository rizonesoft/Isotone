using System.Globalization;
using System.Text.RegularExpressions;
using System.Xml.Linq;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

namespace Bezier.Core.Services;

/// <summary>
/// SVG importer that converts SVG XML to VectorDocument.
/// Handles basic SVG elements, styles, gradients, and transforms.
/// </summary>
public partial class SvgImporter
{
    private static readonly XNamespace SvgNs = "http://www.w3.org/2000/svg";
    private static readonly XNamespace XlinkNs = "http://www.w3.org/1999/xlink";
    private static readonly XNamespace InkscapeNs = "http://www.inkscape.org/namespaces/inkscape";
    private static readonly XNamespace SodipodiNs = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd";

    // Gradient definitions storage for reference resolution
    private readonly Dictionary<string, IFill> _gradientDefs = new();
    
    // CSS class styles storage
    private readonly Dictionary<string, Dictionary<string, string>> _cssStyles = new();

    /// <summary>
    /// Result of an SVG import operation.
    /// </summary>
    public record ImportResult(VectorDocument? Document, bool Success, string? ErrorMessage, List<string> Warnings);

    /// <summary>
    /// Parses an SVG file and returns a VectorDocument.
    /// </summary>
    public ImportResult ImportFile(string filePath)
    {
        try
        {
            if (!File.Exists(filePath))
                return new ImportResult(null, false, $"File not found: {filePath}", []);

            var content = File.ReadAllText(filePath);
            return ImportString(content);
        }
        catch (Exception ex)
        {
            return new ImportResult(null, false, $"Failed to read file: {ex.Message}", []);
        }
    }

    /// <summary>
    /// Parses an SVG string and returns a VectorDocument.
    /// </summary>
    public ImportResult ImportString(string svgContent)
    {
        var warnings = new List<string>();
        _gradientDefs.Clear();
        _cssStyles.Clear();

        try
        {
            if (string.IsNullOrWhiteSpace(svgContent))
                return new ImportResult(null, false, "SVG content is empty", warnings);

            var doc = XDocument.Parse(svgContent);
            var svg = doc.Root;
            
            if (svg is null)
                return new ImportResult(null, false, "Invalid SVG: no root element", warnings);

            // Handle both namespaced and non-namespaced SVG
            if (svg.Name.LocalName != "svg")
                return new ImportResult(null, false, "Invalid SVG: root element must be 'svg'", warnings);

            var width = ParseDouble(svg.Attribute("width")?.Value, 800);
            var height = ParseDouble(svg.Attribute("height")?.Value, 600);

            var document = new VectorDocument
            {
                Width = width,
                Height = height,
                ViewBox = ParseViewBox(svg.Attribute("viewBox")?.Value, width, height),
                Title = svg.Element(SvgNs + "title")?.Value ?? 
                        svg.Elements().FirstOrDefault(e => e.Name.LocalName == "title")?.Value ?? 
                        "Untitled",
                Description = svg.Element(SvgNs + "desc")?.Value ??
                              svg.Elements().FirstOrDefault(e => e.Name.LocalName == "desc")?.Value ??
                              string.Empty
            };

            // Parse CSS styles from <style> elements
            ParseStyleElements(svg, warnings);

            // Parse <defs> for gradients and patterns
            ParseDefs(svg, warnings);

            // Parse child elements
            foreach (var element in svg.Elements())
            {
                var localName = element.Name.LocalName.ToLowerInvariant();
                if (localName is "defs" or "style" or "title" or "desc" or "metadata")
                    continue;

                var vectorElement = ParseElement(element, warnings);
                if (vectorElement is not null)
                {
                    document.Elements.Add(vectorElement);
                }
            }

            document.IsDirty = false;
            return new ImportResult(document, true, null, warnings);
        }
        catch (System.Xml.XmlException ex)
        {
            return new ImportResult(null, false, $"Invalid XML: {ex.Message} at line {ex.LineNumber}", warnings);
        }
        catch (Exception ex)
        {
            return new ImportResult(null, false, $"Import failed: {ex.Message}", warnings);
        }
    }

    /// <summary>
    /// Legacy method for compatibility - parses SVG file.
    /// </summary>
    public VectorDocument ParseFile(string filePath)
    {
        var result = ImportFile(filePath);
        return result.Document ?? throw new InvalidOperationException(result.ErrorMessage ?? "Import failed");
    }

    /// <summary>
    /// Legacy method for compatibility - parses SVG string.
    /// </summary>
    public VectorDocument ParseString(string svgContent)
    {
        var result = ImportString(svgContent);
        return result.Document ?? throw new InvalidOperationException(result.ErrorMessage ?? "Import failed");
    }

    private void ParseStyleElements(XElement svg, List<string> warnings)
    {
        var styleElements = svg.Descendants()
            .Where(e => e.Name.LocalName == "style");

        foreach (var style in styleElements)
        {
            try
            {
                ParseCssContent(style.Value);
            }
            catch
            {
                warnings.Add("Failed to parse some CSS styles");
            }
        }
    }

    private void ParseCssContent(string css)
    {
        // Simple CSS parser for class selectors
        var classMatches = CssClassRegex().Matches(css);
        foreach (Match match in classMatches)
        {
            var className = match.Groups[1].Value;
            var properties = match.Groups[2].Value;
            var propDict = new Dictionary<string, string>();

            var propMatches = CssPropertyRegex().Matches(properties);
            foreach (Match propMatch in propMatches)
            {
                var name = propMatch.Groups[1].Value.Trim();
                var value = propMatch.Groups[2].Value.Trim();
                propDict[name] = value;
            }

            _cssStyles[className] = propDict;
        }
    }

    private void ParseDefs(XElement svg, List<string> warnings)
    {
        var defs = svg.Descendants().Where(e => e.Name.LocalName == "defs");
        
        foreach (var def in defs)
        {
            foreach (var child in def.Elements())
            {
                var localName = child.Name.LocalName.ToLowerInvariant();
                var id = child.Attribute("id")?.Value;

                if (string.IsNullOrEmpty(id)) continue;

                try
                {
                    switch (localName)
                    {
                        case "lineargradient":
                            _gradientDefs[id] = ParseLinearGradient(child);
                            break;
                        case "radialgradient":
                            _gradientDefs[id] = ParseRadialGradient(child);
                            break;
                    }
                }
                catch
                {
                    warnings.Add($"Failed to parse gradient: {id}");
                }
            }
        }
    }

    private LinearGradientFill ParseLinearGradient(XElement element)
    {
        var gradient = new LinearGradientFill
        {
            StartX = ParseDouble(element.Attribute("x1")?.Value, 0) / 100.0,
            StartY = ParseDouble(element.Attribute("y1")?.Value, 0) / 100.0,
            EndX = ParseDouble(element.Attribute("x2")?.Value, 100) / 100.0,
            EndY = ParseDouble(element.Attribute("y2")?.Value, 0) / 100.0,
            SpreadMode = ParseSpreadMode(element.Attribute("spreadMethod")?.Value)
        };

        // Check for percentage vs absolute units
        var gradientUnits = element.Attribute("gradientUnits")?.Value;
        if (gradientUnits != "userSpaceOnUse")
        {
            // objectBoundingBox (default) - values are already 0-1
            gradient.StartX = ParseDouble(element.Attribute("x1")?.Value, 0);
            gradient.StartY = ParseDouble(element.Attribute("y1")?.Value, 0);
            gradient.EndX = ParseDouble(element.Attribute("x2")?.Value, 1);
            gradient.EndY = ParseDouble(element.Attribute("y2")?.Value, 0);
        }

        gradient.Stops = ParseGradientStops(element);
        return gradient;
    }

    private RadialGradientFill ParseRadialGradient(XElement element)
    {
        var gradient = new RadialGradientFill
        {
            CenterX = ParseDouble(element.Attribute("cx")?.Value, 0.5),
            CenterY = ParseDouble(element.Attribute("cy")?.Value, 0.5),
            RadiusX = ParseDouble(element.Attribute("r")?.Value, 0.5),
            RadiusY = ParseDouble(element.Attribute("r")?.Value, 0.5),
            FocalX = ParseDouble(element.Attribute("fx")?.Value, 
                     ParseDouble(element.Attribute("cx")?.Value, 0.5)),
            FocalY = ParseDouble(element.Attribute("fy")?.Value,
                     ParseDouble(element.Attribute("cy")?.Value, 0.5)),
            SpreadMode = ParseSpreadMode(element.Attribute("spreadMethod")?.Value)
        };

        gradient.Stops = ParseGradientStops(element);
        return gradient;
    }

    private List<GradientStop> ParseGradientStops(XElement gradient)
    {
        var stops = new List<GradientStop>();
        
        foreach (var stop in gradient.Elements().Where(e => e.Name.LocalName == "stop"))
        {
            var offset = ParseDouble(stop.Attribute("offset")?.Value?.TrimEnd('%'), 0);
            if (stop.Attribute("offset")?.Value?.EndsWith('%') == true)
                offset /= 100.0;

            var colorStr = stop.Attribute("stop-color")?.Value ?? 
                          GetStyleProperty(stop.Attribute("style")?.Value, "stop-color") ??
                          "#000000";
            var opacityStr = stop.Attribute("stop-opacity")?.Value ??
                            GetStyleProperty(stop.Attribute("style")?.Value, "stop-opacity") ??
                            "1";

            var color = ParseColorToUint(colorStr);
            var opacity = ParseDouble(opacityStr, 1.0);
            
            // Apply opacity to alpha channel
            var alpha = (byte)(((color >> 24) & 0xFF) * opacity);
            color = (color & 0x00FFFFFF) | ((uint)alpha << 24);

            stops.Add(new GradientStop(offset, color));
        }

        return stops;
    }

    private static GradientSpreadMode ParseSpreadMode(string? value) => value?.ToLowerInvariant() switch
    {
        "reflect" => GradientSpreadMode.Reflect,
        "repeat" => GradientSpreadMode.Repeat,
        _ => GradientSpreadMode.Pad
    };

    private static string? GetStyleProperty(string? style, string property)
    {
        if (string.IsNullOrEmpty(style)) return null;
        
        var props = style.Split(';', StringSplitOptions.RemoveEmptyEntries);
        foreach (var prop in props)
        {
            var parts = prop.Split(':', 2);
            if (parts.Length == 2 && parts[0].Trim().Equals(property, StringComparison.OrdinalIgnoreCase))
                return parts[1].Trim();
        }
        return null;
    }

    private static ViewBox ParseViewBox(string? value, double defaultWidth, double defaultHeight)
    {
        if (string.IsNullOrEmpty(value))
            return new ViewBox(0, 0, defaultWidth, defaultHeight);

        var parts = value.Split([' ', ','], StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length >= 4 &&
            double.TryParse(parts[0], System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out var minX) &&
            double.TryParse(parts[1], System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out var minY) &&
            double.TryParse(parts[2], System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out var w) &&
            double.TryParse(parts[3], System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out var h))
        {
            return new ViewBox(minX, minY, w, h);
        }

        return new ViewBox(0, 0, defaultWidth, defaultHeight);
    }

    private VectorElement? ParseElement(XElement element, List<string> warnings)
    {
        var localName = element.Name.LocalName.ToLowerInvariant();

        try
        {
            return localName switch
            {
                "rect" => ParseRect(element),
                "circle" => ParseCircle(element),
                "ellipse" => ParseEllipse(element),
                "line" => ParseLine(element),
                "polygon" => ParsePolygon(element),
                "polyline" => ParsePolyline(element),
                "path" => ParsePath(element),
                "text" => ParseText(element),
                "image" => ParseImage(element),
                "g" => ParseGroup(element, warnings),
                "use" => ParseUse(element, warnings),
                _ => null // Skip unknown elements
            };
        }
        catch (Exception ex)
        {
            var id = element.Attribute("id")?.Value ?? "unknown";
            warnings.Add($"Failed to parse {localName} element (id: {id}): {ex.Message}");
            return null;
        }
    }

    private VectorElement? ParseUse(XElement element, List<string> warnings)
    {
        // Handle <use> elements that reference other elements
        var href = element.Attribute("href")?.Value ?? 
                   element.Attribute(XlinkNs + "href")?.Value;

        if (string.IsNullOrEmpty(href) || !href.StartsWith('#'))
        {
            warnings.Add("Unsupported use element: only local references (#id) are supported");
            return null;
        }

        // For now, create a placeholder group - full implementation would clone the referenced element
        var group = new SvgGroup();
        ApplyCommonAttributes(group, element);
        
        // Apply x/y as transform
        var x = ParseDouble(element.Attribute("x")?.Value, 0);
        var y = ParseDouble(element.Attribute("y")?.Value, 0);
        if (x != 0 || y != 0)
        {
            group.Transform = Transform.CreateTranslation(x, y).Multiply(group.Transform);
        }

        warnings.Add($"Use element referencing '{href}' converted to empty group");
        return group;
    }

    private SvgRect ParseRect(XElement element)
    {
        var rect = new SvgRect
        {
            X = ParseDouble(element.Attribute("x")?.Value, 0),
            Y = ParseDouble(element.Attribute("y")?.Value, 0),
            Width = ParseDouble(element.Attribute("width")?.Value, 100),
            Height = ParseDouble(element.Attribute("height")?.Value, 100),
            Rx = ParseDouble(element.Attribute("rx")?.Value, 0),
            Ry = ParseDouble(element.Attribute("ry")?.Value, 0)
        };
        ApplyCommonAttributes(rect, element);
        return rect;
    }

    private SvgCircle ParseCircle(XElement element)
    {
        var circle = new SvgCircle
        {
            Cx = ParseDouble(element.Attribute("cx")?.Value, 0),
            Cy = ParseDouble(element.Attribute("cy")?.Value, 0),
            R = ParseDouble(element.Attribute("r")?.Value, 50)
        };
        ApplyCommonAttributes(circle, element);
        return circle;
    }

    private SvgEllipse ParseEllipse(XElement element)
    {
        var ellipse = new SvgEllipse
        {
            Cx = ParseDouble(element.Attribute("cx")?.Value, 0),
            Cy = ParseDouble(element.Attribute("cy")?.Value, 0),
            Rx = ParseDouble(element.Attribute("rx")?.Value, 50),
            Ry = ParseDouble(element.Attribute("ry")?.Value, 30)
        };
        ApplyCommonAttributes(ellipse, element);
        return ellipse;
    }

    private SvgLine ParseLine(XElement element)
    {
        var line = new SvgLine
        {
            X1 = ParseDouble(element.Attribute("x1")?.Value, 0),
            Y1 = ParseDouble(element.Attribute("y1")?.Value, 0),
            X2 = ParseDouble(element.Attribute("x2")?.Value, 100),
            Y2 = ParseDouble(element.Attribute("y2")?.Value, 100)
        };
        ApplyCommonAttributes(line, element);
        return line;
    }

    private SvgPolygon ParsePolygon(XElement element)
    {
        var polygon = new SvgPolygon();
        polygon.Points = ParsePoints(element.Attribute("points")?.Value);
        ApplyCommonAttributes(polygon, element);
        return polygon;
    }

    private SvgPolyline ParsePolyline(XElement element)
    {
        var polyline = new SvgPolyline();
        polyline.Points = ParsePoints(element.Attribute("points")?.Value);
        ApplyCommonAttributes(polyline, element);
        return polyline;
    }

    private SvgPath ParsePath(XElement element)
    {
        var path = new SvgPath
        {
            PathData = element.Attribute("d")?.Value ?? string.Empty
        };
        ApplyCommonAttributes(path, element);
        return path;
    }

    private SvgText ParseText(XElement element)
    {
        var text = new SvgText
        {
            X = ParseDouble(element.Attribute("x")?.Value, 0),
            Y = ParseDouble(element.Attribute("y")?.Value, 0),
            Text = element.Value,
            FontFamily = element.Attribute("font-family")?.Value ?? "Arial",
            FontSize = ParseDouble(element.Attribute("font-size")?.Value, 16),
            FontWeight = ParseInt(element.Attribute("font-weight")?.Value, 400)
        };
        ApplyCommonAttributes(text, element);
        return text;
    }

    private SvgImage ParseImage(XElement element)
    {
        var image = new SvgImage
        {
            X = ParseDouble(element.Attribute("x")?.Value, 0),
            Y = ParseDouble(element.Attribute("y")?.Value, 0),
            Width = ParseDouble(element.Attribute("width")?.Value, 100),
            Height = ParseDouble(element.Attribute("height")?.Value, 100),
            Href = element.Attribute("href")?.Value ?? element.Attribute(XNamespace.Get("http://www.w3.org/1999/xlink") + "href")?.Value
        };
        ApplyCommonAttributes(image, element);
        return image;
    }

    private SvgGroup ParseGroup(XElement element, List<string> warnings)
    {
        var group = new SvgGroup();
        ApplyCommonAttributes(group, element);

        // Check for Inkscape layer name
        var inkscapeLabel = element.Attribute(InkscapeNs + "label")?.Value;
        if (!string.IsNullOrEmpty(inkscapeLabel) && string.IsNullOrEmpty(group.Name))
        {
            group.Name = inkscapeLabel;
        }

        foreach (var child in element.Elements())
        {
            var childElement = ParseElement(child, warnings);
            if (childElement is not null)
            {
                group.Add(childElement);
            }
        }

        return group;
    }

    private void ApplyCommonAttributes(VectorElement element, XElement xml)
    {
        element.Name = xml.Attribute("id")?.Value ?? string.Empty;
        
        // Parse inline styles first, then override with attribute values
        var styleAttr = xml.Attribute("style")?.Value;
        var styleProps = ParseInlineStyle(styleAttr);

        // Apply CSS class styles
        var classAttr = xml.Attribute("class")?.Value;
        if (!string.IsNullOrEmpty(classAttr))
        {
            var classes = classAttr.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            foreach (var cls in classes)
            {
                if (_cssStyles.TryGetValue(cls, out var classProps))
                {
                    foreach (var prop in classProps)
                    {
                        styleProps.TryAdd(prop.Key, prop.Value);
                    }
                }
            }
        }

        // Opacity from attribute or style
        var opacityStr = xml.Attribute("opacity")?.Value ?? 
                        (styleProps.TryGetValue("opacity", out var op) ? op : null);
        element.Opacity = ParseDouble(opacityStr, 1.0);

        // Parse fill (attribute takes precedence over style)
        var fillAttr = xml.Attribute("fill")?.Value ?? 
                      (styleProps.TryGetValue("fill", out var f) ? f : null);
        if (!string.IsNullOrEmpty(fillAttr) && fillAttr != "none")
        {
            element.Fill = ParseFillReference(fillAttr);
        }

        // Parse stroke
        var strokeAttr = xml.Attribute("stroke")?.Value ??
                        (styleProps.TryGetValue("stroke", out var s) ? s : null);
        if (!string.IsNullOrEmpty(strokeAttr) && strokeAttr != "none")
        {
            var strokeWidthStr = xml.Attribute("stroke-width")?.Value ??
                                (styleProps.TryGetValue("stroke-width", out var sw) ? sw : "1");
            var strokeLinecap = xml.Attribute("stroke-linecap")?.Value ??
                               (styleProps.TryGetValue("stroke-linecap", out var slc) ? slc : null);
            var strokeLinejoin = xml.Attribute("stroke-linejoin")?.Value ??
                                (styleProps.TryGetValue("stroke-linejoin", out var slj) ? slj : null);
            var strokeDasharray = xml.Attribute("stroke-dasharray")?.Value ??
                                 (styleProps.TryGetValue("stroke-dasharray", out var sda) ? sda : null);
            var strokeDashoffset = xml.Attribute("stroke-dashoffset")?.Value ??
                                  (styleProps.TryGetValue("stroke-dashoffset", out var sdo) ? sdo : null);
            var strokeMiterlimit = xml.Attribute("stroke-miterlimit")?.Value ??
                                  (styleProps.TryGetValue("stroke-miterlimit", out var sml) ? sml : null);

            element.Stroke = new Stroke
            {
                Fill = ParseFillReference(strokeAttr),
                Width = ParseDouble(strokeWidthStr, 1),
                LineCap = ParseLineCap(strokeLinecap),
                LineJoin = ParseLineJoin(strokeLinejoin),
                DashArray = ParseDashArray(strokeDasharray),
                DashOffset = ParseDouble(strokeDashoffset, 0),
                MiterLimit = ParseDouble(strokeMiterlimit, 4)
            };
        }

        // Parse transform
        var transformAttr = xml.Attribute("transform")?.Value;
        if (!string.IsNullOrEmpty(transformAttr))
        {
            element.Transform = ParseTransform(transformAttr);
        }
    }

    private static Dictionary<string, string> ParseInlineStyle(string? style)
    {
        var result = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        if (string.IsNullOrEmpty(style)) return result;

        var props = style.Split(';', StringSplitOptions.RemoveEmptyEntries);
        foreach (var prop in props)
        {
            var parts = prop.Split(':', 2);
            if (parts.Length == 2)
            {
                result[parts[0].Trim()] = parts[1].Trim();
            }
        }
        return result;
    }

    private IFill? ParseFillReference(string value)
    {
        if (string.IsNullOrEmpty(value) || value == "none")
            return null;

        // Check for url() reference to gradient
        if (value.StartsWith("url("))
        {
            var match = UrlRefRegex().Match(value);
            if (match.Success)
            {
                var id = match.Groups[1].Value;
                if (_gradientDefs.TryGetValue(id, out var gradient))
                    return gradient.Clone();
            }
            return null; // Unknown reference
        }

        return ParseFill(value);
    }

    private static LineCap ParseLineCap(string? value) => value?.ToLowerInvariant() switch
    {
        "round" => LineCap.Round,
        "square" => LineCap.Square,
        _ => LineCap.Butt
    };

    private static LineJoin ParseLineJoin(string? value) => value?.ToLowerInvariant() switch
    {
        "round" => LineJoin.Round,
        "bevel" => LineJoin.Bevel,
        _ => LineJoin.Miter
    };

    private static double[]? ParseDashArray(string? value)
    {
        if (string.IsNullOrEmpty(value) || value == "none")
            return null;

        var parts = value.Split([',', ' '], StringSplitOptions.RemoveEmptyEntries);
        var result = new List<double>();
        foreach (var part in parts)
        {
            if (double.TryParse(part.Trim(), NumberStyles.Float, CultureInfo.InvariantCulture, out var d))
                result.Add(d);
        }
        return result.Count > 0 ? result.ToArray() : null;
    }

    private static SolidFill? ParseFill(string value)
    {
        if (string.IsNullOrEmpty(value) || value == "none")
            return null;

        return new SolidFill { Color = ParseColorToUint(value) };
    }

    private static uint ParseColorToUint(string value)
    {
        if (string.IsNullOrEmpty(value))
            return 0xFF000000;

        // Parse hex color
        if (value.StartsWith('#'))
        {
            return ParseHexColorToUint(value);
        }

        // Parse rgb() or rgba()
        if (value.StartsWith("rgb"))
        {
            return ParseRgbColor(value);
        }

        // Parse named colors (extended set)
        return value.ToLowerInvariant() switch
        {
            "black" => 0xFF000000,
            "white" => 0xFFFFFFFF,
            "red" => 0xFFFF0000,
            "green" => 0xFF008000,
            "lime" => 0xFF00FF00,
            "blue" => 0xFF0000FF,
            "yellow" => 0xFFFFFF00,
            "cyan" or "aqua" => 0xFF00FFFF,
            "magenta" or "fuchsia" => 0xFFFF00FF,
            "gray" or "grey" => 0xFF808080,
            "silver" => 0xFFC0C0C0,
            "maroon" => 0xFF800000,
            "olive" => 0xFF808000,
            "navy" => 0xFF000080,
            "teal" => 0xFF008080,
            "purple" => 0xFF800080,
            "orange" => 0xFFFFA500,
            "pink" => 0xFFFFC0CB,
            "brown" => 0xFFA52A2A,
            "coral" => 0xFFFF7F50,
            "crimson" => 0xFFDC143C,
            "darkblue" => 0xFF00008B,
            "darkgreen" => 0xFF006400,
            "darkred" => 0xFF8B0000,
            "gold" => 0xFFFFD700,
            "indigo" => 0xFF4B0082,
            "ivory" => 0xFFFFFFF0,
            "khaki" => 0xFFF0E68C,
            "lavender" => 0xFFE6E6FA,
            "lightblue" => 0xFFADD8E6,
            "lightgray" or "lightgrey" => 0xFFD3D3D3,
            "lightgreen" => 0xFF90EE90,
            "linen" => 0xFFFAF0E6,
            "mintcream" => 0xFFF5FFFA,
            "mistyrose" => 0xFFFFE4E1,
            "moccasin" => 0xFFFFE4B5,
            "oldlace" => 0xFFFDF5E6,
            "orangered" => 0xFFFF4500,
            "orchid" => 0xFFDA70D6,
            "plum" => 0xFFDDA0DD,
            "salmon" => 0xFFFA8072,
            "seagreen" => 0xFF2E8B57,
            "sienna" => 0xFFA0522D,
            "skyblue" => 0xFF87CEEB,
            "slategray" or "slategrey" => 0xFF708090,
            "snow" => 0xFFFFFAFA,
            "tan" => 0xFFD2B48C,
            "thistle" => 0xFFD8BFD8,
            "tomato" => 0xFFFF6347,
            "turquoise" => 0xFF40E0D0,
            "violet" => 0xFFEE82EE,
            "wheat" => 0xFFF5DEB3,
            "transparent" => 0x00000000,
            _ => 0xFF000000 // Default to black
        };
    }

    private static uint ParseRgbColor(string value)
    {
        var match = RgbColorRegex().Match(value);
        if (match.Success)
        {
            var r = byte.Parse(match.Groups[1].Value);
            var g = byte.Parse(match.Groups[2].Value);
            var b = byte.Parse(match.Groups[3].Value);
            var a = match.Groups.Count > 4 && match.Groups[4].Success
                ? (byte)(double.Parse(match.Groups[4].Value, CultureInfo.InvariantCulture) * 255)
                : (byte)255;
            return ((uint)a << 24) | ((uint)r << 16) | ((uint)g << 8) | b;
        }
        return 0xFF000000;
    }

    private static uint ParseHexColorToUint(string hex)
    {
        hex = hex.TrimStart('#');
        uint color = 0xFF000000; // Default opaque black

        try
        {
            if (hex.Length == 3)
            {
                // Short form: #RGB -> #RRGGBB
                var r = Convert.ToByte(new string(hex[0], 2), 16);
                var g = Convert.ToByte(new string(hex[1], 2), 16);
                var b = Convert.ToByte(new string(hex[2], 2), 16);
                color = 0xFF000000 | ((uint)r << 16) | ((uint)g << 8) | b;
            }
            else if (hex.Length == 6)
            {
                var r = Convert.ToByte(hex[..2], 16);
                var g = Convert.ToByte(hex[2..4], 16);
                var b = Convert.ToByte(hex[4..6], 16);
                color = 0xFF000000 | ((uint)r << 16) | ((uint)g << 8) | b;
            }
            else if (hex.Length == 8)
            {
                color = Convert.ToUInt32(hex, 16);
            }
        }
        catch
        {
            // Return default black on parse error
        }

        return color;
    }

    private Transform ParseTransform(string transformStr)
    {
        // Basic transform parsing - handles translate and matrix
        if (transformStr.StartsWith("translate("))
        {
            var values = ParseNumbers(transformStr.Substring(10).TrimEnd(')'));
            if (values.Count >= 2)
                return Transform.CreateTranslation(values[0], values[1]);
            if (values.Count == 1)
                return Transform.CreateTranslation(values[0], 0);
        }
        else if (transformStr.StartsWith("matrix("))
        {
            var values = ParseNumbers(transformStr.Substring(7).TrimEnd(')'));
            if (values.Count >= 6)
            {
                return new Transform
                {
                    ScaleX = values[0],
                    SkewY = values[1],
                    SkewX = values[2],
                    ScaleY = values[3],
                    TranslateX = values[4],
                    TranslateY = values[5]
                };
            }
        }
        else if (transformStr.StartsWith("rotate("))
        {
            var values = ParseNumbers(transformStr.Substring(7).TrimEnd(')'));
            if (values.Count >= 1)
                return Transform.CreateRotation(values[0]);
        }
        else if (transformStr.StartsWith("scale("))
        {
            var values = ParseNumbers(transformStr.Substring(6).TrimEnd(')'));
            if (values.Count >= 2)
                return Transform.CreateScale(values[0], values[1]);
            if (values.Count == 1)
                return Transform.CreateScale(values[0], values[0]);
        }

        return Transform.Identity;
    }

    private List<(double X, double Y)> ParsePoints(string? pointsStr)
    {
        var result = new List<(double X, double Y)>();
        if (string.IsNullOrEmpty(pointsStr)) return result;

        var numbers = ParseNumbers(pointsStr);
        for (int i = 0; i + 1 < numbers.Count; i += 2)
        {
            result.Add((numbers[i], numbers[i + 1]));
        }

        return result;
    }

    private List<double> ParseNumbers(string str)
    {
        var result = new List<double>();
        var parts = str.Split([',', ' ', '\t', '\n', '\r'], StringSplitOptions.RemoveEmptyEntries);
        foreach (var part in parts)
        {
            if (double.TryParse(part, System.Globalization.NumberStyles.Float, 
                System.Globalization.CultureInfo.InvariantCulture, out var value))
            {
                result.Add(value);
            }
        }
        return result;
    }

    private static double ParseDouble(string? value, double defaultValue)
    {
        if (string.IsNullOrEmpty(value)) return defaultValue;
        
        // Remove units (px, pt, em, etc.)
        var numericPart = value.TrimEnd(['p', 'x', 't', 'e', 'm', '%']);
        
        if (double.TryParse(numericPart, System.Globalization.NumberStyles.Float,
            System.Globalization.CultureInfo.InvariantCulture, out var result))
        {
            return result;
        }
        return defaultValue;
    }

    private static int ParseInt(string? value, int defaultValue)
    {
        if (string.IsNullOrEmpty(value)) return defaultValue;
        if (int.TryParse(value, out var result))
            return result;
        return defaultValue;
    }

    [GeneratedRegex(@"\.([\w-]+)\s*\{([^}]*)\}", RegexOptions.Compiled)]
    private static partial Regex CssClassRegex();

    [GeneratedRegex(@"([\w-]+)\s*:\s*([^;]+)", RegexOptions.Compiled)]
    private static partial Regex CssPropertyRegex();

    [GeneratedRegex(@"url\(#([^)]+)\)", RegexOptions.Compiled)]
    private static partial Regex UrlRefRegex();

    [GeneratedRegex(@"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)", RegexOptions.Compiled)]
    private static partial Regex RgbColorRegex();
}
