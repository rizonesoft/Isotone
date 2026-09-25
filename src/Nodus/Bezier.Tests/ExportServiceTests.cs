namespace Bezier.Tests;

using Bezier.Core.Services;

public class ExportServiceTests
{
    private readonly ExportService _service;
    private const string SimpleSvg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect x="10" y="10" width="80" height="80" fill="#FF0000"/></svg>""";

    public ExportServiceTests()
    {
        _service = new ExportService();
    }

    [Fact]
    public void GetFileExtension_Svg()
    {
        Assert.Equal(".svg", ExportService.GetFileExtension(ExportFormat.Svg));
        Assert.Equal(".svg", ExportService.GetFileExtension(ExportFormat.SvgOptimized));
        Assert.Equal(".svg", ExportService.GetFileExtension(ExportFormat.SvgMinified));
    }

    [Fact]
    public void GetFileExtension_Raster()
    {
        Assert.Equal(".png", ExportService.GetFileExtension(ExportFormat.Png));
        Assert.Equal(".jpg", ExportService.GetFileExtension(ExportFormat.Jpg));
        Assert.Equal(".webp", ExportService.GetFileExtension(ExportFormat.WebP));
    }

    [Fact]
    public void GetFileExtension_Code()
    {
        Assert.Equal(".xaml", ExportService.GetFileExtension(ExportFormat.Xaml));
        Assert.Equal(".tsx", ExportService.GetFileExtension(ExportFormat.ReactComponent));
        Assert.Equal(".vue", ExportService.GetFileExtension(ExportFormat.VueComponent));
        Assert.Equal(".css", ExportService.GetFileExtension(ExportFormat.CssClipPath));
    }

    [Fact]
    public void GetMimeType_Svg()
    {
        Assert.Equal("image/svg+xml", ExportService.GetMimeType(ExportFormat.Svg));
    }

    [Fact]
    public void GetMimeType_Raster()
    {
        Assert.Equal("image/png", ExportService.GetMimeType(ExportFormat.Png));
        Assert.Equal("image/jpeg", ExportService.GetMimeType(ExportFormat.Jpg));
        Assert.Equal("image/webp", ExportService.GetMimeType(ExportFormat.WebP));
    }

    [Fact]
    public void GetSaveFilter_ContainsAllFormats()
    {
        var filter = ExportService.GetSaveFilter();

        Assert.Contains("*.svg", filter);
        Assert.Contains("*.png", filter);
        Assert.Contains("*.jpg", filter);
        Assert.Contains("*.webp", filter);
        Assert.Contains("*.pdf", filter);
        Assert.Contains("*.xaml", filter);
        Assert.Contains("*.tsx", filter);
        Assert.Contains("*.vue", filter);
        Assert.Contains("*.css", filter);
        Assert.Contains("*.ico", filter);
    }

    [Fact]
    public void ExportSvg_ValidSvg_Succeeds()
    {
        var result = _service.ExportSvg(SimpleSvg);

        Assert.True(result.Success);
        Assert.NotNull(result.TextContent);
        Assert.Contains("<svg", result.TextContent);
        Assert.Equal(ExportFormat.Svg, result.Format);
    }

    [Fact]
    public void ExportSvg_InvalidSvg_Fails()
    {
        var result = _service.ExportSvg("<invalid>");

        Assert.False(result.Success);
        Assert.NotNull(result.ErrorMessage);
    }

    [Fact]
    public void ExportSvgOptimized_RemovesComments()
    {
        var svgWithComment = """<svg xmlns="http://www.w3.org/2000/svg"><!-- comment --><rect/></svg>""";

        var result = _service.ExportSvgOptimized(svgWithComment);

        Assert.True(result.Success);
        Assert.DoesNotContain("<!--", result.TextContent);
    }

    [Fact]
    public void ExportSvgOptimized_SetsCorrectFormat()
    {
        var result = _service.ExportSvgOptimized(SimpleSvg);

        Assert.Equal(ExportFormat.SvgOptimized, result.Format);
        Assert.Contains("optimized", result.SuggestedFileName);
    }

    [Fact]
    public void ExportSvgMinified_RemovesWhitespace()
    {
        var svgWithWhitespace = """
            <svg xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="10"/>
            </svg>
            """;

        var result = _service.ExportSvgMinified(svgWithWhitespace);

        Assert.True(result.Success);
        Assert.DoesNotContain("\n", result.TextContent);
    }

    [Fact]
    public void ExportSvgMinified_SetsCorrectFormat()
    {
        var result = _service.ExportSvgMinified(SimpleSvg);

        Assert.Equal(ExportFormat.SvgMinified, result.Format);
        Assert.Contains(".min.svg", result.SuggestedFileName);
    }

    [Fact]
    public void ExportXaml_CreatesValidXaml()
    {
        var result = _service.ExportXaml(SimpleSvg);

        Assert.True(result.Success);
        Assert.Contains("<DrawingImage", result.TextContent);
        Assert.Contains("<DrawingGroup>", result.TextContent);
        Assert.Equal(ExportFormat.Xaml, result.Format);
    }

    [Fact]
    public void ExportXaml_UsesComponentName()
    {
        var options = new CodeExportOptions { ComponentName = "MyIcon" };

        var result = _service.ExportXaml(SimpleSvg, options);

        Assert.Contains("MyIcon", result.TextContent);
        Assert.Contains("MyIcon.xaml", result.SuggestedFileName);
    }

    [Fact]
    public void ExportReactComponent_CreatesValidComponent()
    {
        var result = _service.ExportReactComponent(SimpleSvg);

        Assert.True(result.Success);
        Assert.Contains("import React", result.TextContent);
        Assert.Contains("export default", result.TextContent);
        Assert.Equal(ExportFormat.ReactComponent, result.Format);
    }

    [Fact]
    public void ExportReactComponent_UsesComponentName()
    {
        var options = new CodeExportOptions { ComponentName = "MyIcon" };

        var result = _service.ExportReactComponent(SimpleSvg, options);

        Assert.Contains("const MyIcon", result.TextContent);
        Assert.Contains("export default MyIcon", result.TextContent);
    }

    [Fact]
    public void ExportReactComponent_TypeScript_UsesTsx()
    {
        var options = new CodeExportOptions { UseTypeScript = true };

        var result = _service.ExportReactComponent(SimpleSvg, options);

        Assert.Contains(".tsx", result.SuggestedFileName);
    }

    [Fact]
    public void ExportVueComponent_CreatesValidComponent()
    {
        var result = _service.ExportVueComponent(SimpleSvg);

        Assert.True(result.Success);
        Assert.Contains("<template>", result.TextContent);
        Assert.Contains("<script>", result.TextContent);
        Assert.Contains("export default", result.TextContent);
        Assert.Equal(ExportFormat.VueComponent, result.Format);
    }

    [Fact]
    public void ExportVueComponent_UsesComponentName()
    {
        var options = new CodeExportOptions { ComponentName = "MyIcon" };

        var result = _service.ExportVueComponent(SimpleSvg, options);

        Assert.Contains("name: 'MyIcon'", result.TextContent);
    }

    [Fact]
    public void ExportCssClipPath_CreatesValidCss()
    {
        var svgWithPath = """<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0 L100 0 L100 100 Z"/></svg>""";

        var result = _service.ExportCssClipPath(svgWithPath, "my-clip");

        Assert.True(result.Success);
        Assert.Contains(".my-clip", result.TextContent);
        Assert.Contains("clip-path: path(", result.TextContent);
        Assert.Equal(ExportFormat.CssClipPath, result.Format);
    }

    [Fact]
    public void ExportCssClipPath_NoPath_ReturnsComment()
    {
        var result = _service.ExportCssClipPath(SimpleSvg, "my-clip");

        Assert.True(result.Success);
        Assert.Contains("No path found", result.TextContent);
    }

    [Fact]
    public void GetSvgDimensions_FromAttributes()
    {
        var (width, height) = ExportService.GetSvgDimensions(SimpleSvg);

        Assert.Equal(100, width);
        Assert.Equal(100, height);
    }

    [Fact]
    public void GetSvgDimensions_FromViewBox()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 150"></svg>""";

        var (width, height) = ExportService.GetSvgDimensions(svg);

        Assert.Equal(200, width);
        Assert.Equal(150, height);
    }

    [Fact]
    public void GetSvgDimensions_InvalidSvg_ReturnsDefault()
    {
        var (width, height) = ExportService.GetSvgDimensions("<invalid>");

        Assert.Equal(100, width);
        Assert.Equal(100, height);
    }

    [Fact]
    public void CalculateRasterDimensions_WithScale()
    {
        var options = new RasterExportOptions { Scale = 2.0 };

        var (width, height) = _service.CalculateRasterDimensions(SimpleSvg, options);

        Assert.Equal(200, width);
        Assert.Equal(200, height);
    }

    [Fact]
    public void CalculateRasterDimensions_WithFixedWidth()
    {
        var options = new RasterExportOptions { Width = 50 };

        var (width, height) = _service.CalculateRasterDimensions(SimpleSvg, options);

        Assert.Equal(50, width);
        Assert.Equal(50, height); // Maintains aspect ratio
    }

    [Fact]
    public void CalculateRasterDimensions_WithFixedHeight()
    {
        var options = new RasterExportOptions { Height = 200 };

        var (width, height) = _service.CalculateRasterDimensions(SimpleSvg, options);

        Assert.Equal(200, width); // Maintains aspect ratio
        Assert.Equal(200, height);
    }

    [Fact]
    public void CalculateRasterDimensions_WithBothDimensions()
    {
        var options = new RasterExportOptions { Width = 300, Height = 200 };

        var (width, height) = _service.CalculateRasterDimensions(SimpleSvg, options);

        Assert.Equal(300, width);
        Assert.Equal(200, height);
    }
}

public class ExportResultTests
{
    [Fact]
    public void ExportResult_Succeeded_WithData()
    {
        var data = new byte[] { 0x01, 0x02, 0x03 };

        var result = ExportResult.Succeeded(data, ExportFormat.Png, "test.png", "image/png");

        Assert.True(result.Success);
        Assert.Equal(data, result.Data);
        Assert.Equal(ExportFormat.Png, result.Format);
        Assert.Equal("test.png", result.SuggestedFileName);
        Assert.Equal("image/png", result.MimeType);
    }

    [Fact]
    public void ExportResult_Succeeded_WithText()
    {
        var result = ExportResult.Succeeded("<svg></svg>", ExportFormat.Svg, "test.svg");

        Assert.True(result.Success);
        Assert.Equal("<svg></svg>", result.TextContent);
        Assert.NotNull(result.Data);
    }

    [Fact]
    public void ExportResult_Failed()
    {
        var result = ExportResult.Failed("Test error", ExportFormat.Png);

        Assert.False(result.Success);
        Assert.Equal("Test error", result.ErrorMessage);
        Assert.Equal(ExportFormat.Png, result.Format);
    }
}

public class SvgProcessingOptionsTests
{
    [Fact]
    public void SvgProcessingOptions_DefaultValues()
    {
        var options = new SvgProcessingOptions();

        Assert.True(options.RemoveComments);
        Assert.True(options.RemoveMetadata);
        Assert.True(options.RemoveEditorData);
        Assert.True(options.RemoveEmptyGroups);
        Assert.True(options.RemoveUnusedDefs);
        Assert.False(options.CollapseGroups);
        Assert.True(options.ConvertColorsToHex);
        Assert.False(options.ShortenIds);
        Assert.True(options.RemoveDefaultValues);
        Assert.Equal(2, options.DecimalPrecision);
        Assert.False(options.Minify);
        Assert.True(options.PrettyPrint);
    }
}

public class RasterExportOptionsTests
{
    [Fact]
    public void RasterExportOptions_DefaultValues()
    {
        var options = new RasterExportOptions();

        Assert.Equal(1.0, options.Scale);
        Assert.Null(options.Width);
        Assert.Null(options.Height);
        Assert.Equal(96, options.Dpi);
        Assert.True(options.Transparent);
        Assert.Null(options.BackgroundColor);
        Assert.Equal(90, options.JpegQuality);
        Assert.Equal(90, options.WebPQuality);
    }
}

public class IcoExportOptionsTests
{
    [Fact]
    public void IcoExportOptions_DefaultSizes()
    {
        var options = new IcoExportOptions();

        Assert.Contains(16, options.Sizes);
        Assert.Contains(32, options.Sizes);
        Assert.Contains(48, options.Sizes);
        Assert.Contains(64, options.Sizes);
        Assert.Contains(128, options.Sizes);
        Assert.Contains(256, options.Sizes);
        Assert.True(options.IncludePng);
    }
}

public class CodeExportOptionsTests
{
    [Fact]
    public void CodeExportOptions_DefaultValues()
    {
        var options = new CodeExportOptions();

        Assert.Equal("SvgIcon", options.ComponentName);
        Assert.False(options.UseTypeScript);
        Assert.True(options.IncludeProps);
        Assert.Equal("  ", options.IndentString);
    }
}

public class ExportFormatTests
{
    [Fact]
    public void ExportFormat_HasExpectedValues()
    {
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.Svg));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.SvgOptimized));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.SvgMinified));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.Png));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.Jpg));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.WebP));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.Pdf));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.Xaml));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.ReactComponent));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.VueComponent));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.CssClipPath));
        Assert.True(Enum.IsDefined(typeof(ExportFormat), ExportFormat.Ico));
    }
}
