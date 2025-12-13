using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using System.Xml.Linq;

namespace Bezier.Desktop.Services;

/// <summary>
/// Parses SVG and creates editable WPF shapes
/// </summary>
public class SvgCanvasRenderer
{
    public record SvgElement(UIElement Visual, XElement Source, string Id);
    
    private readonly List<SvgElement> _elements = new();
    
    public IReadOnlyList<SvgElement> Elements => _elements;
    
    public void RenderToCanvas(Canvas canvas, string svgContent)
    {
        canvas.Children.Clear();
        _elements.Clear();
        
        if (string.IsNullOrWhiteSpace(svgContent)) return;
        
        try
        {
            var doc = XDocument.Parse(svgContent);
            var root = doc.Root;
            if (root == null || root.Name.LocalName != "svg") return;
            
            // Get viewBox or width/height for canvas sizing
            var viewBox = root.Attribute("viewBox")?.Value;
            double width = 400, height = 400;
            
            if (!string.IsNullOrEmpty(viewBox))
            {
                var parts = viewBox.Split(new[] { ' ', ',' }, StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length >= 4)
                {
                    double.TryParse(parts[2], out width);
                    double.TryParse(parts[3], out height);
                }
            }
            else
            {
                var wAttr = root.Attribute("width")?.Value?.Replace("px", "");
                var hAttr = root.Attribute("height")?.Value?.Replace("px", "");
                if (!string.IsNullOrEmpty(wAttr)) double.TryParse(wAttr, out width);
                if (!string.IsNullOrEmpty(hAttr)) double.TryParse(hAttr, out height);
            }
            
            canvas.Width = width;
            canvas.Height = height;
            
            // Add a visible white/light background for the SVG canvas
            var bg = new Rectangle
            {
                Width = width,
                Height = height,
                Fill = new SolidColorBrush(Color.FromRgb(245, 245, 245)),
                Stroke = new SolidColorBrush(Color.FromRgb(200, 200, 200)),
                StrokeThickness = 1
            };
            canvas.Children.Add(bg);
            
            // Render all elements recursively (check all descendants)
            foreach (var element in root.DescendantsAndSelf())
            {
                RenderSingleElement(canvas, element);
            }
        }
        catch (Exception ex)
        {
            // Add error text to canvas
            var errorText = new TextBlock
            {
                Text = $"Error: {ex.Message}",
                Foreground = Brushes.Red,
                FontSize = 12
            };
            Canvas.SetLeft(errorText, 10);
            Canvas.SetTop(errorText, 10);
            canvas.Children.Add(errorText);
        }
    }
    
    private void RenderSingleElement(Canvas canvas, XElement element)
    {
        UIElement? visual = null;
        var localName = element.Name.LocalName;
        var id = element.Attribute("id")?.Value ?? $"element_{_elements.Count}";
        
        switch (localName)
        {
            case "rect":
                visual = CreateRect(element);
                break;
            case "circle":
                visual = CreateCircle(element);
                break;
            case "ellipse":
                visual = CreateEllipse(element);
                break;
            case "line":
                visual = CreateLine(element);
                break;
            case "path":
                visual = CreatePath(element);
                break;
            case "polygon":
            case "polyline":
                visual = CreatePolygon(element, localName == "polygon");
                break;
            case "text":
                visual = CreateText(element);
                break;
        }
        
        if (visual != null)
        {
            canvas.Children.Add(visual);
            _elements.Add(new SvgElement(visual, element, id));
        }
    }
    
    private static Shape? CreateRect(XElement el)
    {
        var rect = new Rectangle();
        
        if (TryGetDouble(el, "width", out var w)) rect.Width = w;
        if (TryGetDouble(el, "height", out var h)) rect.Height = h;
        if (TryGetDouble(el, "rx", out var rx)) rect.RadiusX = rx;
        if (TryGetDouble(el, "ry", out var ry)) rect.RadiusY = ry;
        
        ApplyCommonAttributes(rect, el);
        
        if (TryGetDouble(el, "x", out var x)) Canvas.SetLeft(rect, x);
        if (TryGetDouble(el, "y", out var y)) Canvas.SetTop(rect, y);
        
        return rect;
    }
    
    private static Shape? CreateCircle(XElement el)
    {
        var ellipse = new Ellipse();
        
        if (TryGetDouble(el, "r", out var r))
        {
            ellipse.Width = r * 2;
            ellipse.Height = r * 2;
        }
        
        ApplyCommonAttributes(ellipse, el);
        
        if (TryGetDouble(el, "cx", out var cx) && TryGetDouble(el, "r", out var r2))
            Canvas.SetLeft(ellipse, cx - r2);
        if (TryGetDouble(el, "cy", out var cy) && TryGetDouble(el, "r", out var r3))
            Canvas.SetTop(ellipse, cy - r3);
        
        return ellipse;
    }
    
    private static Shape? CreateEllipse(XElement el)
    {
        var ellipse = new Ellipse();
        
        if (TryGetDouble(el, "rx", out var rx)) ellipse.Width = rx * 2;
        if (TryGetDouble(el, "ry", out var ry)) ellipse.Height = ry * 2;
        
        ApplyCommonAttributes(ellipse, el);
        
        if (TryGetDouble(el, "cx", out var cx) && TryGetDouble(el, "rx", out var rx2))
            Canvas.SetLeft(ellipse, cx - rx2);
        if (TryGetDouble(el, "cy", out var cy) && TryGetDouble(el, "ry", out var ry2))
            Canvas.SetTop(ellipse, cy - ry2);
        
        return ellipse;
    }
    
    private static Shape? CreateLine(XElement el)
    {
        var line = new Line();
        
        if (TryGetDouble(el, "x1", out var x1)) line.X1 = x1;
        if (TryGetDouble(el, "y1", out var y1)) line.Y1 = y1;
        if (TryGetDouble(el, "x2", out var x2)) line.X2 = x2;
        if (TryGetDouble(el, "y2", out var y2)) line.Y2 = y2;
        
        ApplyCommonAttributes(line, el);
        
        return line;
    }
    
    private static Shape? CreatePath(XElement el)
    {
        var pathData = el.Attribute("d")?.Value;
        if (string.IsNullOrEmpty(pathData)) return null;
        
        try
        {
            var path = new Path
            {
                Data = Geometry.Parse(pathData)
            };
            ApplyCommonAttributes(path, el);
            return path;
        }
        catch
        {
            return null;
        }
    }
    
    private static Shape? CreatePolygon(XElement el, bool closed)
    {
        var pointsStr = el.Attribute("points")?.Value;
        if (string.IsNullOrEmpty(pointsStr)) return null;
        
        var points = new PointCollection();
        var parts = pointsStr.Split(new[] { ' ', ',' }, StringSplitOptions.RemoveEmptyEntries);
        
        for (int i = 0; i < parts.Length - 1; i += 2)
        {
            if (double.TryParse(parts[i], out var x) && double.TryParse(parts[i + 1], out var y))
            {
                points.Add(new Point(x, y));
            }
        }
        
        if (closed)
        {
            var polygon = new Polygon { Points = points };
            ApplyCommonAttributes(polygon, el);
            return polygon;
        }
        else
        {
            var polyline = new Polyline { Points = points };
            ApplyCommonAttributes(polyline, el);
            return polyline;
        }
    }
    
    private static FrameworkElement? CreateText(XElement el)
    {
        var text = new TextBlock
        {
            Text = el.Value,
            FontSize = 14
        };
        
        var fill = el.Attribute("fill")?.Value;
        if (!string.IsNullOrEmpty(fill) && fill != "none")
        {
            try { text.Foreground = new BrushConverter().ConvertFromString(fill) as Brush ?? Brushes.Black; }
            catch { text.Foreground = Brushes.Black; }
        }
        
        var fontSize = el.Attribute("font-size")?.Value?.Replace("px", "");
        if (!string.IsNullOrEmpty(fontSize) && double.TryParse(fontSize, out var fs))
            text.FontSize = fs;
        
        if (TryGetDouble(el, "x", out var x)) Canvas.SetLeft(text, x);
        if (TryGetDouble(el, "y", out var y)) Canvas.SetTop(text, y - text.FontSize);
        
        return text;
    }
    
    private static void ApplyCommonAttributes(Shape shape, XElement el)
    {
        var fill = el.Attribute("fill")?.Value;
        if (!string.IsNullOrEmpty(fill) && fill != "none")
        {
            try { shape.Fill = new BrushConverter().ConvertFromString(fill) as Brush; }
            catch { }
        }
        
        var stroke = el.Attribute("stroke")?.Value;
        if (!string.IsNullOrEmpty(stroke) && stroke != "none")
        {
            try { shape.Stroke = new BrushConverter().ConvertFromString(stroke) as Brush; }
            catch { }
        }
        
        var strokeWidth = el.Attribute("stroke-width")?.Value;
        if (!string.IsNullOrEmpty(strokeWidth) && double.TryParse(strokeWidth, out var sw))
            shape.StrokeThickness = sw;
        
        var opacity = el.Attribute("opacity")?.Value;
        if (!string.IsNullOrEmpty(opacity) && double.TryParse(opacity, out var op))
            shape.Opacity = op;
    }
    
    private static bool TryGetDouble(XElement el, string attr, out double value)
    {
        value = 0;
        var str = el.Attribute(attr)?.Value?.Replace("px", "");
        return !string.IsNullOrEmpty(str) && double.TryParse(str, out value);
    }
}
