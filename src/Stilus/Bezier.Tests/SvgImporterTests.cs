namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;
using Bezier.Core.Services;

public class SvgImporterTests
{
    private readonly SvgImporter _importer = new();

    [Fact]
    public void ImportString_ValidSvg_ReturnsSuccess()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>""";
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        Assert.NotNull(result.Document);
        Assert.Equal(100, result.Document.Width);
        Assert.Equal(100, result.Document.Height);
    }

    [Fact]
    public void ImportString_EmptyString_ReturnsError()
    {
        var result = _importer.ImportString("");

        Assert.False(result.Success);
        Assert.Null(result.Document);
        Assert.NotNull(result.ErrorMessage);
    }

    [Fact]
    public void ImportString_InvalidXml_ReturnsError()
    {
        var result = _importer.ImportString("<svg><unclosed>");

        Assert.False(result.Success);
        Assert.Contains("Invalid XML", result.ErrorMessage);
    }

    [Fact]
    public void ImportString_NonSvgRoot_ReturnsError()
    {
        var result = _importer.ImportString("<div></div>");

        Assert.False(result.Success);
        Assert.Contains("root element must be 'svg'", result.ErrorMessage);
    }

    [Fact]
    public void ImportString_ParsesViewBox()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 20 300 400"></svg>""";
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        Assert.Equal(10, result.Document!.ViewBox.MinX);
        Assert.Equal(20, result.Document.ViewBox.MinY);
        Assert.Equal(300, result.Document.ViewBox.Width);
        Assert.Equal(400, result.Document.ViewBox.Height);
    }

    [Fact]
    public void ImportString_ParsesTitle()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg"><title>Test Title</title></svg>""";
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        Assert.Equal("Test Title", result.Document!.Title);
    }

    [Fact]
    public void ImportString_ParsesRect()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="20" width="100" height="50" rx="5" ry="3"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        Assert.Single(result.Document!.Elements);
        var rect = Assert.IsType<SvgRect>(result.Document.Elements[0]);
        Assert.Equal(10, rect.X);
        Assert.Equal(20, rect.Y);
        Assert.Equal(100, rect.Width);
        Assert.Equal(50, rect.Height);
        Assert.Equal(5, rect.Rx);
        Assert.Equal(3, rect.Ry);
    }

    [Fact]
    public void ImportString_ParsesCircle()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="60" r="25"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var circle = Assert.IsType<SvgCircle>(result.Document!.Elements[0]);
        Assert.Equal(50, circle.Cx);
        Assert.Equal(60, circle.Cy);
        Assert.Equal(25, circle.R);
    }

    [Fact]
    public void ImportString_ParsesEllipse()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <ellipse cx="100" cy="80" rx="40" ry="20"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var ellipse = Assert.IsType<SvgEllipse>(result.Document!.Elements[0]);
        Assert.Equal(100, ellipse.Cx);
        Assert.Equal(80, ellipse.Cy);
        Assert.Equal(40, ellipse.Rx);
        Assert.Equal(20, ellipse.Ry);
    }

    [Fact]
    public void ImportString_ParsesLine()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <line x1="10" y1="20" x2="100" y2="200"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var line = Assert.IsType<SvgLine>(result.Document!.Elements[0]);
        Assert.Equal(10, line.X1);
        Assert.Equal(20, line.Y1);
        Assert.Equal(100, line.X2);
        Assert.Equal(200, line.Y2);
    }

    [Fact]
    public void ImportString_ParsesPath()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <path d="M10 10 L100 100 Z"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var path = Assert.IsType<SvgPath>(result.Document!.Elements[0]);
        Assert.Equal("M10 10 L100 100 Z", path.PathData);
    }

    [Fact]
    public void ImportString_ParsesPolygon()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <polygon points="10,10 100,10 50,100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var polygon = Assert.IsType<SvgPolygon>(result.Document!.Elements[0]);
        Assert.Equal(3, polygon.Points.Count);
        Assert.Equal((10, 10), polygon.Points[0]);
        Assert.Equal((100, 10), polygon.Points[1]);
        Assert.Equal((50, 100), polygon.Points[2]);
    }

    [Fact]
    public void ImportString_ParsesText()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <text x="10" y="50" font-family="Arial" font-size="24">Hello World</text>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var text = Assert.IsType<SvgText>(result.Document!.Elements[0]);
        Assert.Equal(10, text.X);
        Assert.Equal(50, text.Y);
        Assert.Equal("Arial", text.FontFamily);
        Assert.Equal(24, text.FontSize);
        Assert.Equal("Hello World", text.Text);
    }

    [Fact]
    public void ImportString_ParsesGroup()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <g id="group1">
                    <rect x="0" y="0" width="10" height="10"/>
                    <circle cx="50" cy="50" r="20"/>
                </g>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var group = Assert.IsType<SvgGroup>(result.Document!.Elements[0]);
        Assert.Equal("group1", group.Name);
        Assert.Equal(2, group.Children.Count);
        Assert.IsType<SvgRect>(group.Children[0]);
        Assert.IsType<SvgCircle>(group.Children[1]);
    }

    [Fact]
    public void ImportString_ParsesSolidFill()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect fill="#FF0000" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        var fill = Assert.IsType<SolidFill>(rect.Fill);
        Assert.Equal(0xFFFF0000u, fill.Color);
    }

    [Fact]
    public void ImportString_ParsesNamedColor()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect fill="blue" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        var fill = Assert.IsType<SolidFill>(rect.Fill);
        Assert.Equal(0xFF0000FFu, fill.Color);
    }

    [Fact]
    public void ImportString_ParsesStroke()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect stroke="#00FF00" stroke-width="3" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        Assert.NotNull(rect.Stroke);
        Assert.Equal(3, rect.Stroke.Width);
        var strokeFill = Assert.IsType<SolidFill>(rect.Stroke.Fill);
        Assert.Equal(0xFF00FF00u, strokeFill.Color);
    }

    [Fact]
    public void ImportString_ParsesOpacity()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect opacity="0.5" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        Assert.Equal(0.5, rect.Opacity);
    }

    [Fact]
    public void ImportString_ParsesTranslateTransform()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect transform="translate(50, 100)" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        Assert.Equal(50, rect.Transform.TranslateX);
        Assert.Equal(100, rect.Transform.TranslateY);
    }

    [Fact]
    public void ImportString_ParsesLinearGradient()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="grad1" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stop-color="#FF0000"/>
                        <stop offset="100%" stop-color="#0000FF"/>
                    </linearGradient>
                </defs>
                <rect fill="url(#grad1)" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        var gradient = Assert.IsType<LinearGradientFill>(rect.Fill);
        Assert.Equal(2, gradient.Stops.Count);
    }

    [Fact]
    public void ImportString_ParsesInlineStyle()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect style="fill:#FF0000;stroke:#00FF00;stroke-width:2" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        var fill = Assert.IsType<SolidFill>(rect.Fill);
        Assert.Equal(0xFFFF0000u, fill.Color);
        Assert.NotNull(rect.Stroke);
        Assert.Equal(2, rect.Stroke.Width);
    }

    [Fact]
    public void ImportString_PreservesElementId()
    {
        var svg = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect id="myRect" width="100" height="100"/>
            </svg>
            """;
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        var rect = Assert.IsType<SvgRect>(result.Document!.Elements[0]);
        Assert.Equal("myRect", rect.Name);
    }

    [Fact]
    public void ParseString_LegacyMethod_Works()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="150"></svg>""";
        var document = _importer.ParseString(svg);

        Assert.NotNull(document);
        Assert.Equal(200, document.Width);
        Assert.Equal(150, document.Height);
    }

    [Fact]
    public void ImportString_NonNamespacedSvg_Works()
    {
        var svg = """<svg width="100" height="100"><rect width="50" height="50"/></svg>""";
        var result = _importer.ImportString(svg);

        Assert.True(result.Success);
        Assert.Single(result.Document!.Elements);
    }
}
