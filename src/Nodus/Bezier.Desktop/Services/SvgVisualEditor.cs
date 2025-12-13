using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using System.Xml.Linq;
using SharpVectors.Converters;
using SharpVectors.Renderers.Wpf;

namespace Bezier.Desktop.Services;

/// <summary>
/// Enhanced SVG visual editor using SharpVectors for accurate rendering
/// with overlay selection handles for interactive editing
/// </summary>
public class SvgVisualEditor
{
    public record ElementInfo(string Id, Rect Bounds, XElement Source);
    
    private readonly List<ElementInfo> _elements = new();
    private readonly WpfDrawingSettings _settings;
    private DrawingGroup? _drawing;
    private XDocument? _document;
    private double _svgWidth = 400;
    private double _svgHeight = 400;
    
    public IReadOnlyList<ElementInfo> Elements => _elements;
    public double SvgWidth => _svgWidth;
    public double SvgHeight => _svgHeight;
    
    public SvgVisualEditor()
    {
        _settings = new WpfDrawingSettings
        {
            IncludeRuntime = true,
            TextAsGeometry = false
        };
    }
    
    /// <summary>
    /// Renders the SVG using SharpVectors and extracts element bounds for hit-testing
    /// </summary>
    public bool LoadSvg(string svgContent, out DrawingImage? image)
    {
        image = null;
        _elements.Clear();
        _document = null;
        
        if (string.IsNullOrWhiteSpace(svgContent)) return false;
        
        try
        {
            // Parse the SVG document
            _document = XDocument.Parse(svgContent);
            var root = _document.Root;
            if (root == null || root.Name.LocalName != "svg") return false;
            
            // Get dimensions
            ExtractDimensions(root);
            
            // Extract element bounds for hit-testing
            ExtractElementBounds(root);
            
            // Use SharpVectors to render
            var tempFile = System.IO.Path.Combine(System.IO.Path.GetTempPath(), $"bezier_visual_{Guid.NewGuid():N}.svg");
            System.IO.File.WriteAllText(tempFile, svgContent);
            
            try
            {
                var converter = new FileSvgReader(_settings);
                _drawing = converter.Read(tempFile);
                
                if (_drawing != null)
                {
                    image = new DrawingImage(_drawing);
                    return true;
                }
            }
            finally
            {
                Task.Delay(100).ContinueWith(_ => { try { System.IO.File.Delete(tempFile); } catch { } });
            }
        }
        catch
        {
            // Failed to parse
        }
        
        return false;
    }
    
    private void ExtractDimensions(XElement root)
    {
        var viewBox = root.Attribute("viewBox")?.Value;
        
        if (!string.IsNullOrEmpty(viewBox))
        {
            var parts = viewBox.Split(new[] { ' ', ',' }, StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length >= 4)
            {
                double.TryParse(parts[2], NumberStyles.Float, CultureInfo.InvariantCulture, out _svgWidth);
                double.TryParse(parts[3], NumberStyles.Float, CultureInfo.InvariantCulture, out _svgHeight);
            }
        }
        else
        {
            var w = root.Attribute("width")?.Value?.Replace("px", "").Replace("pt", "");
            var h = root.Attribute("height")?.Value?.Replace("px", "").Replace("pt", "");
            if (!string.IsNullOrEmpty(w)) double.TryParse(w, NumberStyles.Float, CultureInfo.InvariantCulture, out _svgWidth);
            if (!string.IsNullOrEmpty(h)) double.TryParse(h, NumberStyles.Float, CultureInfo.InvariantCulture, out _svgHeight);
        }
    }
    
    private void ExtractElementBounds(XElement root)
    {
        foreach (var el in root.DescendantsAndSelf())
        {
            var localName = el.Name.LocalName;
            var id = el.Attribute("id")?.Value ?? $"el_{_elements.Count}";
            Rect? bounds = null;
            
            switch (localName)
            {
                case "rect":
                    bounds = GetRectBounds(el);
                    break;
                case "circle":
                    bounds = GetCircleBounds(el);
                    break;
                case "ellipse":
                    bounds = GetEllipseBounds(el);
                    break;
                case "line":
                    bounds = GetLineBounds(el);
                    break;
                case "path":
                case "polygon":
                case "polyline":
                    bounds = GetPathBounds(el);
                    break;
                case "text":
                    bounds = GetTextBounds(el);
                    break;
                case "image":
                    bounds = GetImageBounds(el);
                    break;
            }
            
            if (bounds.HasValue && bounds.Value.Width > 0 && bounds.Value.Height > 0)
            {
                _elements.Add(new ElementInfo(id, bounds.Value, el));
            }
        }
    }
    
    private static Rect? GetRectBounds(XElement el)
    {
        if (!TryGetDouble(el, "width", out var w) || !TryGetDouble(el, "height", out var h)) return null;
        TryGetDouble(el, "x", out var x);
        TryGetDouble(el, "y", out var y);
        return new Rect(x, y, w, h);
    }
    
    private static Rect? GetCircleBounds(XElement el)
    {
        if (!TryGetDouble(el, "r", out var r)) return null;
        TryGetDouble(el, "cx", out var cx);
        TryGetDouble(el, "cy", out var cy);
        return new Rect(cx - r, cy - r, r * 2, r * 2);
    }
    
    private static Rect? GetEllipseBounds(XElement el)
    {
        if (!TryGetDouble(el, "rx", out var rx) || !TryGetDouble(el, "ry", out var ry)) return null;
        TryGetDouble(el, "cx", out var cx);
        TryGetDouble(el, "cy", out var cy);
        return new Rect(cx - rx, cy - ry, rx * 2, ry * 2);
    }
    
    private static Rect? GetLineBounds(XElement el)
    {
        TryGetDouble(el, "x1", out var x1);
        TryGetDouble(el, "y1", out var y1);
        TryGetDouble(el, "x2", out var x2);
        TryGetDouble(el, "y2", out var y2);
        var minX = Math.Min(x1, x2);
        var minY = Math.Min(y1, y2);
        var w = Math.Abs(x2 - x1);
        var h = Math.Abs(y2 - y1);
        if (w < 1) w = 4; // Minimum for hit-testing
        if (h < 1) h = 4;
        return new Rect(minX, minY, w, h);
    }
    
    private static Rect? GetPathBounds(XElement el)
    {
        // Parse path data or points to get bounds
        var d = el.Attribute("d")?.Value;
        var points = el.Attribute("points")?.Value;
        
        if (!string.IsNullOrEmpty(d))
        {
            try
            {
                var geometry = Geometry.Parse(d);
                return geometry.Bounds;
            }
            catch { }
        }
        
        if (!string.IsNullOrEmpty(points))
        {
            var nums = points.Split(new[] { ' ', ',' }, StringSplitOptions.RemoveEmptyEntries);
            double minX = double.MaxValue, minY = double.MaxValue;
            double maxX = double.MinValue, maxY = double.MinValue;
            
            for (int i = 0; i < nums.Length - 1; i += 2)
            {
                if (double.TryParse(nums[i], NumberStyles.Float, CultureInfo.InvariantCulture, out var x) &&
                    double.TryParse(nums[i + 1], NumberStyles.Float, CultureInfo.InvariantCulture, out var y))
                {
                    minX = Math.Min(minX, x);
                    minY = Math.Min(minY, y);
                    maxX = Math.Max(maxX, x);
                    maxY = Math.Max(maxY, y);
                }
            }
            
            if (minX < double.MaxValue)
                return new Rect(minX, minY, maxX - minX, maxY - minY);
        }
        
        return null;
    }
    
    private static Rect? GetTextBounds(XElement el)
    {
        TryGetDouble(el, "x", out var x);
        TryGetDouble(el, "y", out var y);
        // Approximate text bounds
        var text = el.Value;
        var fontSize = 14.0;
        var fs = el.Attribute("font-size")?.Value?.Replace("px", "");
        if (!string.IsNullOrEmpty(fs)) double.TryParse(fs, NumberStyles.Float, CultureInfo.InvariantCulture, out fontSize);
        
        var width = text.Length * fontSize * 0.6;
        var height = fontSize * 1.2;
        return new Rect(x, y - height, width, height);
    }
    
    private static Rect? GetImageBounds(XElement el)
    {
        if (!TryGetDouble(el, "width", out var w) || !TryGetDouble(el, "height", out var h)) return null;
        TryGetDouble(el, "x", out var x);
        TryGetDouble(el, "y", out var y);
        return new Rect(x, y, w, h);
    }
    
    /// <summary>
    /// Find element at the given point
    /// </summary>
    public ElementInfo? HitTest(Point point)
    {
        // Search in reverse order (topmost first)
        for (int i = _elements.Count - 1; i >= 0; i--)
        {
            if (_elements[i].Bounds.Contains(point))
                return _elements[i];
        }
        return null;
    }
    
    /// <summary>
    /// Move an element by updating its position attributes
    /// </summary>
    public string? MoveElement(ElementInfo element, double dx, double dy)
    {
        if (_document == null) return null;
        
        var el = element.Source;
        var localName = el.Name.LocalName;
        
        switch (localName)
        {
            case "rect":
            case "text":
            case "image":
                UpdateAttr(el, "x", dx);
                UpdateAttr(el, "y", dy);
                break;
            case "circle":
            case "ellipse":
                UpdateAttr(el, "cx", dx);
                UpdateAttr(el, "cy", dy);
                break;
            case "line":
                UpdateAttr(el, "x1", dx);
                UpdateAttr(el, "y1", dy);
                UpdateAttr(el, "x2", dx);
                UpdateAttr(el, "y2", dy);
                break;
            case "path":
                // Translate path data
                TranslatePath(el, dx, dy);
                break;
            case "polygon":
            case "polyline":
                TranslatePoints(el, dx, dy);
                break;
        }
        
        return _document.Root?.ToString();
    }
    
    private static void UpdateAttr(XElement el, string attr, double delta)
    {
        var val = el.Attribute(attr)?.Value?.Replace("px", "");
        if (double.TryParse(val, NumberStyles.Float, CultureInfo.InvariantCulture, out var v))
        {
            el.SetAttributeValue(attr, (v + delta).ToString("F2", CultureInfo.InvariantCulture));
        }
    }
    
    private static void TranslatePath(XElement el, double dx, double dy)
    {
        var d = el.Attribute("d")?.Value;
        if (string.IsNullOrEmpty(d)) return;
        
        // Simple approach: wrap in a group with transform or add to existing transform
        var transform = el.Attribute("transform")?.Value ?? "";
        el.SetAttributeValue("transform", $"{transform} translate({dx:F2},{dy:F2})".Trim());
    }
    
    private static void TranslatePoints(XElement el, double dx, double dy)
    {
        var points = el.Attribute("points")?.Value;
        if (string.IsNullOrEmpty(points)) return;
        
        var nums = points.Split(new[] { ' ', ',' }, StringSplitOptions.RemoveEmptyEntries);
        var newPoints = new List<string>();
        
        for (int i = 0; i < nums.Length - 1; i += 2)
        {
            if (double.TryParse(nums[i], NumberStyles.Float, CultureInfo.InvariantCulture, out var x) &&
                double.TryParse(nums[i + 1], NumberStyles.Float, CultureInfo.InvariantCulture, out var y))
            {
                newPoints.Add($"{(x + dx):F2},{(y + dy):F2}");
            }
        }
        
        el.SetAttributeValue("points", string.Join(" ", newPoints));
    }
    
    private static bool TryGetDouble(XElement el, string attr, out double value)
    {
        value = 0;
        var str = el.Attribute(attr)?.Value?.Replace("px", "").Replace("pt", "");
        return !string.IsNullOrEmpty(str) && double.TryParse(str, NumberStyles.Float, CultureInfo.InvariantCulture, out value);
    }
}
