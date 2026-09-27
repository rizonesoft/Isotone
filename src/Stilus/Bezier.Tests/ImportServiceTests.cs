namespace Bezier.Tests;

using Bezier.Core.Services;

public class ImportServiceTests
{
    private readonly ImportService _service;

    public ImportServiceTests()
    {
        _service = new ImportService();
    }

    [Fact]
    public void DetectFormatByExtension_Svg()
    {
        var format = ImportService.DetectFormatByExtension("test.svg");
        Assert.Equal(ImportFormat.Svg, format);
    }

    [Fact]
    public void DetectFormatByExtension_Png()
    {
        var format = ImportService.DetectFormatByExtension("test.png");
        Assert.Equal(ImportFormat.Png, format);
    }

    [Fact]
    public void DetectFormatByExtension_Jpg()
    {
        var format = ImportService.DetectFormatByExtension("test.jpg");
        Assert.Equal(ImportFormat.Jpg, format);
    }

    [Fact]
    public void DetectFormatByExtension_Jpeg()
    {
        var format = ImportService.DetectFormatByExtension("test.jpeg");
        Assert.Equal(ImportFormat.Jpg, format);
    }

    [Fact]
    public void DetectFormatByExtension_Ai()
    {
        var format = ImportService.DetectFormatByExtension("test.ai");
        Assert.Equal(ImportFormat.Ai, format);
    }

    [Fact]
    public void DetectFormatByExtension_Eps()
    {
        var format = ImportService.DetectFormatByExtension("test.eps");
        Assert.Equal(ImportFormat.Eps, format);
    }

    [Fact]
    public void DetectFormatByExtension_Pdf()
    {
        var format = ImportService.DetectFormatByExtension("test.pdf");
        Assert.Equal(ImportFormat.Pdf, format);
    }

    [Fact]
    public void DetectFormatByExtension_Unknown()
    {
        var format = ImportService.DetectFormatByExtension("test.xyz");
        Assert.Equal(ImportFormat.Unknown, format);
    }

    [Fact]
    public void DetectFormatByExtension_CaseInsensitive()
    {
        var format = ImportService.DetectFormatByExtension("test.SVG");
        Assert.Equal(ImportFormat.Svg, format);
    }

    [Fact]
    public void DetectFormatByContent_Png()
    {
        var pngHeader = new byte[] { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A };
        var format = ImportService.DetectFormatByContent(pngHeader);
        Assert.Equal(ImportFormat.Png, format);
    }

    [Fact]
    public void DetectFormatByContent_Jpg()
    {
        var jpgHeader = new byte[] { 0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46 };
        var format = ImportService.DetectFormatByContent(jpgHeader);
        Assert.Equal(ImportFormat.Jpg, format);
    }

    [Fact]
    public void DetectFormatByContent_Gif()
    {
        var gifHeader = new byte[] { 0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0x00, 0x00 };
        var format = ImportService.DetectFormatByContent(gifHeader);
        Assert.Equal(ImportFormat.Gif, format);
    }

    [Fact]
    public void DetectFormatByContent_Bmp()
    {
        var bmpHeader = new byte[] { 0x42, 0x4D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
        var format = ImportService.DetectFormatByContent(bmpHeader);
        Assert.Equal(ImportFormat.Bmp, format);
    }

    [Fact]
    public void DetectFormatByContent_Pdf()
    {
        var pdfHeader = new byte[] { 0x25, 0x50, 0x44, 0x46, 0x2D, 0x31, 0x2E, 0x34 }; // %PDF-1.4
        var format = ImportService.DetectFormatByContent(pdfHeader);
        Assert.Equal(ImportFormat.Pdf, format);
    }

    [Fact]
    public void DetectFormatByContent_Svg()
    {
        var svgContent = System.Text.Encoding.UTF8.GetBytes("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>");
        var format = ImportService.DetectFormatByContent(svgContent);
        Assert.Equal(ImportFormat.Svg, format);
    }

    [Fact]
    public void DetectFormatByContent_Unknown()
    {
        var unknownData = new byte[] { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07 };
        var format = ImportService.DetectFormatByContent(unknownData);
        Assert.Equal(ImportFormat.Unknown, format);
    }

    [Fact]
    public void GetFileFilter_ReturnsValidFilter()
    {
        var filter = ImportService.GetFileFilter();

        Assert.Contains("*.svg", filter);
        Assert.Contains("*.png", filter);
        Assert.Contains("*.jpg", filter);
        Assert.Contains("*.ai", filter);
        Assert.Contains("*.eps", filter);
        Assert.Contains("*.pdf", filter);
    }

    [Fact]
    public void ImportSvgContent_ValidSvg_Succeeds()
    {
        var svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\"></svg>";

        var result = _service.ImportSvgContent(svg);

        Assert.True(result.Success);
        Assert.NotNull(result.SvgContent);
        Assert.Equal(ImportFormat.Svg, result.DetectedFormat);
    }

    [Fact]
    public void ImportSvgContent_InvalidXml_Fails()
    {
        var invalidSvg = "<svg><rect></svg>";

        var result = _service.ImportSvgContent(invalidSvg);

        Assert.False(result.Success);
        Assert.NotNull(result.ErrorMessage);
    }

    [Fact]
    public void ImportSvgContent_NotSvgRoot_Fails()
    {
        var notSvg = "<html><body></body></html>";

        var result = _service.ImportSvgContent(notSvg);

        Assert.False(result.Success);
        Assert.Contains("root element", result.ErrorMessage);
    }

    [Fact]
    public void ImportSvgContent_WithOptions_PreservesIds()
    {
        var svg = "<svg xmlns=\"http://www.w3.org/2000/svg\"><rect id=\"test\"/></svg>";
        var options = new ImportOptions { PreserveIds = true };

        var result = _service.ImportSvgContent(svg, options);

        Assert.True(result.Success);
        Assert.Contains("id=\"test\"", result.SvgContent);
    }

    [Fact]
    public void ImportSvgContent_WithOptions_RemovesIds()
    {
        var svg = "<svg xmlns=\"http://www.w3.org/2000/svg\"><rect id=\"test\"/></svg>";
        var options = new ImportOptions { PreserveIds = false };

        var result = _service.ImportSvgContent(svg, options);

        Assert.True(result.Success);
        Assert.DoesNotContain("id=", result.SvgContent);
    }

    [Fact]
    public void ImportFromClipboard_WithSvg_Succeeds()
    {
        var clipboard = new ClipboardData
        {
            HasSvg = true,
            SvgContent = "<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>"
        };

        var result = _service.ImportFromClipboard(clipboard);

        Assert.True(result.Success);
    }

    [Fact]
    public void ImportFromClipboard_WithSvgText_Succeeds()
    {
        var clipboard = new ClipboardData
        {
            HasText = true,
            TextContent = "<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>"
        };

        var result = _service.ImportFromClipboard(clipboard);

        Assert.True(result.Success);
    }

    [Fact]
    public void ImportFromClipboard_Empty_Fails()
    {
        var clipboard = new ClipboardData();

        var result = _service.ImportFromClipboard(clipboard);

        Assert.False(result.Success);
        Assert.Equal(ImportFormat.Clipboard, result.DetectedFormat);
    }

    [Fact]
    public void ImportFile_NonExistent_Fails()
    {
        var result = _service.ImportFile("nonexistent.svg");

        Assert.False(result.Success);
        Assert.Contains("not found", result.ErrorMessage);
    }

    [Fact]
    public void IsRasterFormat_ReturnsCorrectly()
    {
        Assert.True(ImportService.IsRasterFormat(ImportFormat.Png));
        Assert.True(ImportService.IsRasterFormat(ImportFormat.Jpg));
        Assert.True(ImportService.IsRasterFormat(ImportFormat.Gif));
        Assert.True(ImportService.IsRasterFormat(ImportFormat.Bmp));
        Assert.True(ImportService.IsRasterFormat(ImportFormat.WebP));
        Assert.False(ImportService.IsRasterFormat(ImportFormat.Svg));
        Assert.False(ImportService.IsRasterFormat(ImportFormat.Pdf));
    }

    [Fact]
    public void IsVectorFormat_ReturnsCorrectly()
    {
        Assert.True(ImportService.IsVectorFormat(ImportFormat.Svg));
        Assert.True(ImportService.IsVectorFormat(ImportFormat.Ai));
        Assert.True(ImportService.IsVectorFormat(ImportFormat.Eps));
        Assert.True(ImportService.IsVectorFormat(ImportFormat.Pdf));
        Assert.False(ImportService.IsVectorFormat(ImportFormat.Png));
        Assert.False(ImportService.IsVectorFormat(ImportFormat.Jpg));
    }

    [Fact]
    public void CreateEmbeddedImageElement_CreatesValidElement()
    {
        var imageData = new byte[] { 0x01, 0x02, 0x03 };

        var element = ImportService.CreateEmbeddedImageElement(imageData, "png", 10, 20, 100, 50);

        Assert.Contains("<image", element);
        Assert.Contains("x=\"10\"", element);
        Assert.Contains("y=\"20\"", element);
        Assert.Contains("width=\"100\"", element);
        Assert.Contains("height=\"50\"", element);
        Assert.Contains("data:image/png;base64,", element);
    }
}

public class ImportResultTests
{
    [Fact]
    public void ImportResult_Succeeded_SetsProperties()
    {
        var result = ImportResult.Succeeded("<svg></svg>", ImportFormat.Svg, "/path/file.svg");

        Assert.True(result.Success);
        Assert.Equal("<svg></svg>", result.SvgContent);
        Assert.Equal(ImportFormat.Svg, result.DetectedFormat);
        Assert.Equal("/path/file.svg", result.SourcePath);
        Assert.Null(result.ErrorMessage);
    }

    [Fact]
    public void ImportResult_Failed_SetsProperties()
    {
        var result = ImportResult.Failed("Test error", ImportFormat.Png);

        Assert.False(result.Success);
        Assert.Equal("Test error", result.ErrorMessage);
        Assert.Equal(ImportFormat.Png, result.DetectedFormat);
        Assert.Null(result.SvgContent);
    }

    [Fact]
    public void ImportResult_Warnings_DefaultsToEmptyList()
    {
        var result = new ImportResult();

        Assert.NotNull(result.Warnings);
        Assert.Empty(result.Warnings);
    }
}

public class ImportOptionsTests
{
    [Fact]
    public void ImportOptions_DefaultValues()
    {
        var options = new ImportOptions();

        Assert.True(options.PreserveIds);
        Assert.True(options.PreserveStyles);
        Assert.False(options.ConvertTextToPath);
        Assert.True(options.EmbedImages);
        Assert.Null(options.MaxWidth);
        Assert.Null(options.MaxHeight);
        Assert.Equal("px", options.DefaultUnit);
    }
}

public class ClipboardDataTests
{
    [Fact]
    public void ClipboardData_DefaultValues()
    {
        var data = new ClipboardData();

        Assert.False(data.HasSvg);
        Assert.False(data.HasImage);
        Assert.False(data.HasText);
        Assert.Null(data.SvgContent);
        Assert.Null(data.ImageData);
        Assert.Null(data.ImageFormat);
        Assert.Null(data.TextContent);
    }

    [Fact]
    public void ClipboardData_CanSetAllProperties()
    {
        var imageData = new byte[] { 0x01, 0x02 };
        var data = new ClipboardData
        {
            HasSvg = true,
            HasImage = true,
            HasText = true,
            SvgContent = "<svg></svg>",
            ImageData = imageData,
            ImageFormat = "png",
            TextContent = "text"
        };

        Assert.True(data.HasSvg);
        Assert.True(data.HasImage);
        Assert.True(data.HasText);
        Assert.Equal("<svg></svg>", data.SvgContent);
        Assert.Equal(imageData, data.ImageData);
        Assert.Equal("png", data.ImageFormat);
        Assert.Equal("text", data.TextContent);
    }
}

public class ImportFormatTests
{
    [Fact]
    public void ImportFormat_HasExpectedValues()
    {
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Unknown));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Svg));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Ai));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Eps));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Pdf));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Png));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Jpg));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Gif));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Bmp));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.WebP));
        Assert.True(Enum.IsDefined(typeof(ImportFormat), ImportFormat.Clipboard));
    }
}
