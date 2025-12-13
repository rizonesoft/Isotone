using System.Xml.Linq;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

namespace Bezier.Core.Services;

/// <summary>
/// Basic SVG file parser that converts SVG XML to VectorDocument.
/// </summary>
public class SvgParser
{
    private static readonly XNamespace SvgNs = "http://www.w3.org/2000/svg";

    /// <summary>
    /// Parses an SVG file and returns a VectorDocument.
    /// </summary>
    public VectorDocument ParseFile(string filePath)
    {
        var content = File.ReadAllText(filePath);
        return ParseString(content);
    }

    /// <summary>
    /// Parses an SVG string and returns a VectorDocument.
    /// </summary>
    public VectorDocument ParseString(string svgContent)
    {
        var doc = XDocument.Parse(svgContent);
        var svg = doc.Root ?? throw new InvalidOperationException("Invalid SVG: no root element");

        var width = ParseDouble(svg.Attribute("width")?.Value, 800);
        var height = ParseDouble(svg.Attribute("height")?.Value, 600);

        var document = new VectorDocument
        {
            Width = width,
            Height = height,
            ViewBox = ParseViewBox(svg.Attribute("viewBox")?.Value, width, height),
            Title = svg.Element(SvgNs + "title")?.Value ?? "Untitled"
        };

        // Parse child elements
        foreach (var element in svg.Elements())
        {
            var vectorElement = ParseElement(element);
            if (vectorElement is not null)
            {
                document.Elements.Add(vectorElement);
            }
        }

        document.IsDirty = false;
        return document;
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

    private VectorElement? ParseElement(XElement element)
    {
        var localName = element.Name.LocalName.ToLowerInvariant();

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
            "g" => ParseGroup(element),
            _ => null // Skip unknown elements
        };
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

    private SvgGroup ParseGroup(XElement element)
    {
        var group = new SvgGroup();
        ApplyCommonAttributes(group, element);

        foreach (var child in element.Elements())
        {
            var childElement = ParseElement(child);
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
        element.Opacity = ParseDouble(xml.Attribute("opacity")?.Value, 1.0);

        // Parse fill
        var fillAttr = xml.Attribute("fill")?.Value;
        if (!string.IsNullOrEmpty(fillAttr) && fillAttr != "none")
        {
            element.Fill = ParseFill(fillAttr);
        }

        // Parse stroke
        var strokeAttr = xml.Attribute("stroke")?.Value;
        if (!string.IsNullOrEmpty(strokeAttr) && strokeAttr != "none")
        {
            element.Stroke = new Stroke
            {
                Fill = ParseFill(strokeAttr),
                Width = ParseDouble(xml.Attribute("stroke-width")?.Value, 1)
            };
        }

        // Parse transform (simplified - only handles basic transforms)
        var transformAttr = xml.Attribute("transform")?.Value;
        if (!string.IsNullOrEmpty(transformAttr))
        {
            element.Transform = ParseTransform(transformAttr);
        }
    }

    private SolidFill? ParseFill(string value)
    {
        if (string.IsNullOrEmpty(value) || value == "none")
            return null;

        // Parse hex color
        if (value.StartsWith('#'))
        {
            return ParseHexColor(value);
        }

        // Parse named colors (basic set)
        return value.ToLowerInvariant() switch
        {
            "black" => new SolidFill { Color = 0xFF000000 },
            "white" => new SolidFill { Color = 0xFFFFFFFF },
            "red" => new SolidFill { Color = 0xFFFF0000 },
            "green" => new SolidFill { Color = 0xFF00FF00 },
            "blue" => new SolidFill { Color = 0xFF0000FF },
            "yellow" => new SolidFill { Color = 0xFFFFFF00 },
            "cyan" => new SolidFill { Color = 0xFF00FFFF },
            "magenta" => new SolidFill { Color = 0xFFFF00FF },
            "gray" or "grey" => new SolidFill { Color = 0xFF808080 },
            "orange" => new SolidFill { Color = 0xFFFFA500 },
            "purple" => new SolidFill { Color = 0xFF800080 },
            _ => new SolidFill { Color = 0xFF000000 } // Default to black
        };
    }

    private SolidFill ParseHexColor(string hex)
    {
        hex = hex.TrimStart('#');
        uint color = 0xFF000000; // Default opaque black

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
            var r = Convert.ToByte(hex.Substring(0, 2), 16);
            var g = Convert.ToByte(hex.Substring(2, 2), 16);
            var b = Convert.ToByte(hex.Substring(4, 2), 16);
            color = 0xFF000000 | ((uint)r << 16) | ((uint)g << 8) | b;
        }
        else if (hex.Length == 8)
        {
            color = Convert.ToUInt32(hex, 16);
        }

        return new SolidFill { Color = color };
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
}
