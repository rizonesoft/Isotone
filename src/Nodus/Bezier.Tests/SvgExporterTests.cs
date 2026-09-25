namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;
using Bezier.Core.Services;

public class SvgExporterTests
{
    private readonly SvgExporter _exporter = new();

    [Fact]
    public void Export_EmptyDocument_GeneratesValidSvg()
    {
        var document = new VectorDocument { Width = 800, Height = 600 };
        var svg = _exporter.Export(document);

        Assert.Contains("<?xml version=\"1.0\"", svg);
        Assert.Contains("<svg", svg);
        Assert.Contains("xmlns=\"http://www.w3.org/2000/svg\"", svg);
        Assert.Contains("width=\"800\"", svg);
        Assert.Contains("height=\"600\"", svg);
        Assert.Contains("</svg>", svg);
    }

    [Fact]
    public void Export_WithViewBox_IncludesViewBox()
    {
        var document = new VectorDocument
        {
            Width = 800,
            Height = 600,
            ViewBox = new ViewBox(10, 20, 400, 300)
        };
        var svg = _exporter.Export(document);

        Assert.Contains("viewBox=\"10 20 400 300\"", svg);
    }

    [Fact]
    public void Export_WithTitle_IncludesTitle()
    {
        var document = new VectorDocument { Title = "Test Document" };
        var svg = _exporter.Export(document);

        Assert.Contains("<title>Test Document</title>", svg);
    }

    [Fact]
    public void Export_Rect_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            X = 10,
            Y = 20,
            Width = 100,
            Height = 50,
            Rx = 5,
            Ry = 3,
            Fill = SolidFill.Red
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<rect", svg);
        Assert.Contains("x=\"10\"", svg);
        Assert.Contains("y=\"20\"", svg);
        Assert.Contains("width=\"100\"", svg);
        Assert.Contains("height=\"50\"", svg);
        Assert.Contains("rx=\"5\"", svg);
        Assert.Contains("ry=\"3\"", svg);
    }

    [Fact]
    public void Export_Circle_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgCircle
        {
            Cx = 50,
            Cy = 60,
            R = 25,
            Fill = SolidFill.Blue
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<circle", svg);
        Assert.Contains("cx=\"50\"", svg);
        Assert.Contains("cy=\"60\"", svg);
        Assert.Contains("r=\"25\"", svg);
    }

    [Fact]
    public void Export_Ellipse_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgEllipse
        {
            Cx = 100,
            Cy = 80,
            Rx = 40,
            Ry = 20
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<ellipse", svg);
        Assert.Contains("cx=\"100\"", svg);
        Assert.Contains("cy=\"80\"", svg);
        Assert.Contains("rx=\"40\"", svg);
        Assert.Contains("ry=\"20\"", svg);
    }

    [Fact]
    public void Export_Line_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgLine
        {
            X1 = 10,
            Y1 = 20,
            X2 = 100,
            Y2 = 200,
            Stroke = new Stroke { Fill = SolidFill.Black, Width = 2 }
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<line", svg);
        Assert.Contains("x1=\"10\"", svg);
        Assert.Contains("y1=\"20\"", svg);
        Assert.Contains("x2=\"100\"", svg);
        Assert.Contains("y2=\"200\"", svg);
    }

    [Fact]
    public void Export_Path_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgPath
        {
            PathData = "M10 10 L100 100 Z",
            Fill = SolidFill.Green
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<path", svg);
        Assert.Contains("d=\"M10 10 L100 100 Z\"", svg);
    }

    [Fact]
    public void Export_Polygon_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        var polygon = new SvgPolygon { Fill = SolidFill.Red };
        polygon.Points = [(10, 10), (100, 10), (50, 100)];
        document.Elements.Add(polygon);

        var svg = _exporter.Export(document);

        Assert.Contains("<polygon", svg);
        Assert.Contains("points=\"10,10 100,10 50,100\"", svg);
    }

    [Fact]
    public void Export_Text_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgText
        {
            X = 10,
            Y = 50,
            Text = "Hello World",
            FontFamily = "Arial",
            FontSize = 24,
            Fill = SolidFill.Black
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<text", svg);
        Assert.Contains("x=\"10\"", svg);
        Assert.Contains("y=\"50\"", svg);
        Assert.Contains("font-family=\"Arial\"", svg);
        Assert.Contains("font-size=\"24\"", svg);
        Assert.Contains(">Hello World</text>", svg);
    }

    [Fact]
    public void Export_Group_GeneratesCorrectElement()
    {
        var document = new VectorDocument();
        var group = new SvgGroup { Name = "testGroup" };
        group.Add(new SvgRect { Width = 100, Height = 100 });
        document.Elements.Add(group);

        var svg = _exporter.Export(document);

        Assert.Contains("<g", svg);
        Assert.Contains("id=\"testGroup\"", svg);
        Assert.Contains("</g>", svg);
    }

    [Fact]
    public void Export_SolidFill_GeneratesHexColor()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Fill = SolidFill.FromRgb(255, 128, 64)
        });

        var svg = _exporter.Export(document);

        Assert.Contains("fill=\"#FF8040\"", svg);
    }

    [Fact]
    public void Export_NoFill_GeneratesFillNone()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Fill = null
        });

        var svg = _exporter.Export(document);

        Assert.Contains("fill=\"none\"", svg);
    }

    [Fact]
    public void Export_Stroke_GeneratesStrokeAttributes()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Stroke = new Stroke
            {
                Fill = SolidFill.Red,
                Width = 3,
                LineCap = LineCap.Round,
                LineJoin = LineJoin.Bevel,
                DashArray = [5, 3],
                DashOffset = 2
            }
        });

        var svg = _exporter.Export(document);

        Assert.Contains("stroke=\"#FF0000\"", svg);
        Assert.Contains("stroke-width=\"3\"", svg);
        Assert.Contains("stroke-linecap=\"round\"", svg);
        Assert.Contains("stroke-linejoin=\"bevel\"", svg);
        Assert.Contains("stroke-dasharray=\"5,3\"", svg);
        Assert.Contains("stroke-dashoffset=\"2\"", svg);
    }

    [Fact]
    public void Export_Opacity_GeneratesOpacityAttribute()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Opacity = 0.5
        });

        var svg = _exporter.Export(document);

        Assert.Contains("opacity=\"0.5\"", svg);
    }

    [Fact]
    public void Export_Transform_GeneratesTransformAttribute()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Transform = Transform.CreateTranslation(50, 100)
        });

        var svg = _exporter.Export(document);

        Assert.Contains("transform=\"", svg);
    }

    [Fact]
    public void Export_LinearGradient_GeneratesDefsAndUrl()
    {
        var document = new VectorDocument();
        var gradient = LinearGradientFill.Create(0xFFFF0000, 0xFF0000FF);
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Fill = gradient
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<defs>", svg);
        Assert.Contains("<linearGradient", svg);
        Assert.Contains("</linearGradient>", svg);
        Assert.Contains("fill=\"url(#gradient1)\"", svg);
        Assert.Contains("<stop", svg);
    }

    [Fact]
    public void Export_RadialGradient_GeneratesDefsAndUrl()
    {
        var document = new VectorDocument();
        var gradient = RadialGradientFill.Create(0xFFFFFFFF, 0xFF000000);
        document.Elements.Add(new SvgRect
        {
            Width = 100,
            Height = 100,
            Fill = gradient
        });

        var svg = _exporter.Export(document);

        Assert.Contains("<defs>", svg);
        Assert.Contains("<radialGradient", svg);
        Assert.Contains("</radialGradient>", svg);
        Assert.Contains("fill=\"url(#gradient1)\"", svg);
    }

    [Fact]
    public void Export_Minified_NoWhitespace()
    {
        var document = new VectorDocument { Width = 100, Height = 100 };
        document.Elements.Add(new SvgRect { Width = 50, Height = 50 });

        var svg = _exporter.Export(document, SvgExportOptions.Minified);

        Assert.DoesNotContain("\n", svg);
        Assert.DoesNotContain("  ", svg);
    }

    [Fact]
    public void Export_WithoutXmlDeclaration_NoDeclaration()
    {
        var document = new VectorDocument();
        var options = new SvgExportOptions { IncludeXmlDeclaration = false };
        var svg = _exporter.Export(document, options);

        Assert.DoesNotContain("<?xml", svg);
        Assert.StartsWith("<svg", svg);
    }

    [Fact]
    public void Export_WithoutIds_NoIdAttributes()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect { Name = "myRect", Width = 100, Height = 100 });

        var options = new SvgExportOptions { PreserveIds = false };
        var svg = _exporter.Export(document, options);

        Assert.DoesNotContain("id=\"myRect\"", svg);
    }

    [Fact]
    public void Export_InvisibleElement_NotIncluded()
    {
        var document = new VectorDocument();
        document.Elements.Add(new SvgRect
        {
            Name = "visibleRect",
            Width = 100,
            Height = 100,
            IsVisible = true
        });
        document.Elements.Add(new SvgRect
        {
            Name = "invisibleRect",
            Width = 50,
            Height = 50,
            IsVisible = false
        });

        var svg = _exporter.Export(document);

        Assert.Contains("visibleRect", svg);
        Assert.DoesNotContain("invisibleRect", svg);
    }

    [Fact]
    public void Export_XmlEscapes_SpecialCharacters()
    {
        var document = new VectorDocument { Title = "Test & <Special> \"Characters\"" };
        var svg = _exporter.Export(document);

        Assert.Contains("&amp;", svg);
        Assert.Contains("&lt;", svg);
        Assert.Contains("&gt;", svg);
        Assert.Contains("&quot;", svg);
    }

    [Fact]
    public void RoundTrip_ImportExport_PreservesStructure()
    {
        var importer = new SvgImporter();
        
        // Create a document
        var original = new VectorDocument { Width = 400, Height = 300, Title = "Test" };
        original.Elements.Add(new SvgRect { X = 10, Y = 20, Width = 100, Height = 50, Fill = SolidFill.Red });
        original.Elements.Add(new SvgCircle { Cx = 200, Cy = 150, R = 50, Fill = SolidFill.Blue });

        // Export
        var svg = _exporter.Export(original);

        // Import
        var result = importer.ImportString(svg);

        Assert.True(result.Success);
        Assert.Equal(2, result.Document!.Elements.Count);
        Assert.IsType<SvgRect>(result.Document.Elements[0]);
        Assert.IsType<SvgCircle>(result.Document.Elements[1]);
    }
}
