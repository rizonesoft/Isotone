namespace Bezier.Tests;

using Bezier.Core.Services;

public class ExportDialogModelTests
{
    [Fact]
    public void ExportDialogModel_DefaultValues()
    {
        var model = new ExportDialogModel();

        Assert.Equal(ExportFormat.Png, model.Format);
        Assert.Equal(ExportPreset.Custom, model.Preset);
        Assert.Equal("export", model.Filename);
        Assert.Equal(1.0, model.Scale);
        Assert.True(model.MaintainAspectRatio);
        Assert.Equal(90, model.Quality);
        Assert.True(model.Transparent);
        Assert.False(model.ExportAllArtboards);
    }

    [Fact]
    public void ExportDialogModel_Format_UpdatesExtension()
    {
        var model = new ExportDialogModel { Format = ExportFormat.Png };

        Assert.Equal(".png", model.FileExtension);

        model.Format = ExportFormat.Jpg;
        Assert.Equal(".jpg", model.FileExtension);

        model.Format = ExportFormat.Svg;
        Assert.Equal(".svg", model.FileExtension);
    }

    [Fact]
    public void ExportDialogModel_FullFilename_IncludesExtension()
    {
        var model = new ExportDialogModel
        {
            Filename = "myfile",
            Format = ExportFormat.Png
        };

        Assert.Equal("myfile.png", model.FullFilename);
    }

    [Fact]
    public void ExportDialogModel_FullPath_CombinesFolderAndFilename()
    {
        var model = new ExportDialogModel
        {
            Filename = "myfile",
            Format = ExportFormat.Png,
            OutputFolder = @"C:\exports"
        };

        Assert.Contains("myfile.png", model.FullPath);
        Assert.Contains("exports", model.FullPath);
    }

    [Fact]
    public void ExportDialogModel_Scale_UpdatesDimensions()
    {
        var model = new ExportDialogModel
        {
            OriginalWidth = 100,
            OriginalHeight = 50,
            MaintainAspectRatio = true
        };

        model.Scale = 2.0;

        Assert.Equal(200, model.Width);
        Assert.Equal(100, model.Height);
    }

    [Fact]
    public void ExportDialogModel_Width_UpdatesScaleAndHeight()
    {
        var model = new ExportDialogModel
        {
            OriginalWidth = 100,
            OriginalHeight = 50,
            MaintainAspectRatio = true
        };

        model.Width = 200;

        Assert.Equal(2.0, model.Scale);
        Assert.Equal(100, model.Height);
    }

    [Fact]
    public void ExportDialogModel_Height_UpdatesScaleAndWidth()
    {
        var model = new ExportDialogModel
        {
            OriginalWidth = 100,
            OriginalHeight = 50,
            MaintainAspectRatio = true
        };

        model.Height = 100;

        Assert.Equal(2.0, model.Scale);
        Assert.Equal(200, model.Width);
    }

    [Fact]
    public void ExportDialogModel_ScalePercentage_FormatsCorrectly()
    {
        var model = new ExportDialogModel { Scale = 1.5 };

        Assert.Equal("150%", model.ScalePercentage);
    }

    [Fact]
    public void ExportDialogModel_SupportsTransparency_ByFormat()
    {
        var model = new ExportDialogModel();

        model.Format = ExportFormat.Png;
        Assert.True(model.SupportsTransparency);

        model.Format = ExportFormat.Jpg;
        Assert.False(model.SupportsTransparency);

        model.Format = ExportFormat.WebP;
        Assert.True(model.SupportsTransparency);
    }

    [Fact]
    public void ExportDialogModel_SupportsQuality_ByFormat()
    {
        var model = new ExportDialogModel();

        model.Format = ExportFormat.Png;
        Assert.False(model.SupportsQuality);

        model.Format = ExportFormat.Jpg;
        Assert.True(model.SupportsQuality);

        model.Format = ExportFormat.WebP;
        Assert.True(model.SupportsQuality);
    }

    [Fact]
    public void ExportDialogModel_IsRasterFormat()
    {
        var model = new ExportDialogModel();

        model.Format = ExportFormat.Png;
        Assert.True(model.IsRasterFormat);

        model.Format = ExportFormat.Svg;
        Assert.False(model.IsRasterFormat);
    }

    [Fact]
    public void ExportDialogModel_IsVectorFormat()
    {
        var model = new ExportDialogModel();

        model.Format = ExportFormat.Svg;
        Assert.True(model.IsVectorFormat);

        model.Format = ExportFormat.Png;
        Assert.False(model.IsVectorFormat);
    }

    [Fact]
    public void ExportDialogModel_ApplyPreset_Web()
    {
        var model = new ExportDialogModel();

        model.Preset = ExportPreset.Web;

        Assert.Equal(ExportFormat.Png, model.Format);
        Assert.Equal(1.0, model.Scale);
        Assert.True(model.Transparent);
    }

    [Fact]
    public void ExportDialogModel_ApplyPreset_Print()
    {
        var model = new ExportDialogModel();

        model.Preset = ExportPreset.Print;

        Assert.Equal(ExportFormat.Pdf, model.Format);
    }

    [Fact]
    public void ExportDialogModel_ApplyPreset_Social()
    {
        var model = new ExportDialogModel();

        model.Preset = ExportPreset.Social;

        Assert.Equal(ExportFormat.Jpg, model.Format);
        Assert.False(model.Transparent);
        Assert.Equal("#FFFFFF", model.BackgroundColor);
    }

    [Fact]
    public void ExportDialogModel_ApplyPreset_HighQuality()
    {
        var model = new ExportDialogModel();

        model.Preset = ExportPreset.HighQuality;

        Assert.Equal(ExportFormat.Png, model.Format);
        Assert.Equal(2.0, model.Scale);
        Assert.Equal(100, model.Quality);
    }

    [Fact]
    public void ExportDialogModel_GenerateFilename_Basic()
    {
        var model = new ExportDialogModel();

        var filename = model.GenerateFilename("{name}", "document");

        Assert.Equal("document", filename);
    }

    [Fact]
    public void ExportDialogModel_GenerateFilename_WithArtboard()
    {
        var model = new ExportDialogModel();

        var filename = model.GenerateFilename("{name}-{artboard}", "doc", "page1");

        Assert.Equal("doc-page1", filename);
    }

    [Fact]
    public void ExportDialogModel_GenerateFilename_WithIndex()
    {
        var model = new ExportDialogModel();

        var filename = model.GenerateFilename("{name}-{index}", "doc", null, 5);

        Assert.Equal("doc-5", filename);
    }

    [Fact]
    public void ExportDialogModel_GenerateFilename_WithScale()
    {
        var model = new ExportDialogModel { Scale = 2.0 };

        var filename = model.GenerateFilename("{name}@{scale}", "icon");

        Assert.Equal("icon@2x", filename);
    }

    [Fact]
    public void ExportDialogModel_GenerateFilename_SanitizesInvalidChars()
    {
        var model = new ExportDialogModel();

        var filename = model.GenerateFilename("{name}", "file:with/invalid*chars");

        Assert.DoesNotContain(":", filename);
        Assert.DoesNotContain("/", filename);
        Assert.DoesNotContain("*", filename);
    }

    [Fact]
    public void ExportDialogModel_ToRasterOptions_MapsCorrectly()
    {
        var model = new ExportDialogModel
        {
            OriginalWidth = 100,
            OriginalHeight = 50,
            MaintainAspectRatio = false, // Disable to set dimensions independently
            Width = 200,
            Height = 100,
            Transparent = true,
            BackgroundColor = "#FF0000",
            Quality = 85
        };

        var options = model.ToRasterOptions();

        Assert.Equal(200, options.Width);
        Assert.Equal(100, options.Height);
        Assert.True(options.Transparent);
        Assert.Equal("#FF0000", options.BackgroundColor);
        Assert.Equal(85, options.JpegQuality);
        Assert.Equal(85, options.WebPQuality);
    }

    [Fact]
    public void ExportDialogModel_ToSvgOptions_Standard()
    {
        var model = new ExportDialogModel { Format = ExportFormat.Svg };

        var options = model.ToSvgOptions();

        Assert.False(options.Minify);
        Assert.True(options.PrettyPrint);
    }

    [Fact]
    public void ExportDialogModel_ToSvgOptions_Minified()
    {
        var model = new ExportDialogModel { Format = ExportFormat.SvgMinified };

        var options = model.ToSvgOptions();

        Assert.True(options.Minify);
        Assert.False(options.PrettyPrint);
    }

    [Fact]
    public void ExportDialogModel_Validate_EmptyFilename_Fails()
    {
        var model = new ExportDialogModel { Filename = "" };

        var (isValid, error) = model.Validate();

        Assert.False(isValid);
        Assert.Contains("Filename", error);
    }

    [Fact]
    public void ExportDialogModel_Validate_ValidConfig_Succeeds()
    {
        var model = new ExportDialogModel
        {
            Filename = "test",
            Scale = 1.0,
            Quality = 90
        };

        var (isValid, _) = model.Validate();

        Assert.True(isValid);
    }

    [Fact]
    public void ExportDialogModel_Quality_ClampedTo100()
    {
        var model = new ExportDialogModel();

        model.Quality = 150;

        Assert.Equal(100, model.Quality);
    }

    [Fact]
    public void ExportDialogModel_Quality_ClampedTo0()
    {
        var model = new ExportDialogModel();

        model.Quality = -10;

        Assert.Equal(0, model.Quality);
    }

    [Fact]
    public void ExportDialogModel_Scale_ClampedToMin()
    {
        var model = new ExportDialogModel();

        model.Scale = 0.01;

        Assert.Equal(0.1, model.Scale);
    }

    [Fact]
    public void ExportDialogModel_Scale_ClampedToMax()
    {
        var model = new ExportDialogModel();

        model.Scale = 20;

        Assert.Equal(10, model.Scale);
    }
}

public class BatchExportItemTests
{
    [Fact]
    public void BatchExportItem_DefaultValues()
    {
        var item = new BatchExportItem();

        Assert.Equal(string.Empty, item.Name);
        Assert.Null(item.ArtboardName);
        Assert.Equal(0, item.Index);
        Assert.True(item.IsSelected);
        Assert.Null(item.Result);
    }

    [Fact]
    public void BatchExportItem_CanSetAllProperties()
    {
        var item = new BatchExportItem
        {
            Name = "Test",
            ArtboardName = "Page1",
            Index = 5,
            SvgContent = "<svg></svg>",
            OutputFilename = "test.png",
            IsSelected = false
        };

        Assert.Equal("Test", item.Name);
        Assert.Equal("Page1", item.ArtboardName);
        Assert.Equal(5, item.Index);
        Assert.Equal("<svg></svg>", item.SvgContent);
        Assert.Equal("test.png", item.OutputFilename);
        Assert.False(item.IsSelected);
    }
}

public class ExportDialogServiceTests
{
    private readonly ExportDialogService _service;

    public ExportDialogServiceTests()
    {
        _service = new ExportDialogService();
    }

    [Fact]
    public void AvailableFormats_ContainsAllMainFormats()
    {
        var formats = ExportDialogService.AvailableFormats.ToList();

        Assert.Contains(formats, f => f.Format == ExportFormat.Png);
        Assert.Contains(formats, f => f.Format == ExportFormat.Jpg);
        Assert.Contains(formats, f => f.Format == ExportFormat.Svg);
        Assert.Contains(formats, f => f.Format == ExportFormat.Pdf);
    }

    [Fact]
    public void AvailablePresets_ContainsAllPresets()
    {
        var presets = ExportDialogService.AvailablePresets.ToList();

        Assert.Contains(presets, p => p.Preset == ExportPreset.Custom);
        Assert.Contains(presets, p => p.Preset == ExportPreset.Web);
        Assert.Contains(presets, p => p.Preset == ExportPreset.Print);
        Assert.Contains(presets, p => p.Preset == ExportPreset.Social);
    }

    [Fact]
    public void ScaleOptions_ContainsCommonScales()
    {
        var scales = ExportDialogService.ScaleOptions.ToList();

        Assert.Contains(scales, s => s.Scale == 1.0);
        Assert.Contains(scales, s => s.Scale == 2.0);
        Assert.Contains(scales, s => s.Scale == 3.0);
    }

    [Fact]
    public void TemplateVariables_ContainsCommonVariables()
    {
        var variables = ExportDialogService.TemplateVariables.ToList();

        Assert.Contains(variables, v => v.Variable == "{name}");
        Assert.Contains(variables, v => v.Variable == "{artboard}");
        Assert.Contains(variables, v => v.Variable == "{index}");
    }

    [Fact]
    public void CreateDefaultModel_SetsCorrectDimensions()
    {
        var model = _service.CreateDefaultModel(200, 100, "test");

        Assert.Equal(200, model.OriginalWidth);
        Assert.Equal(100, model.OriginalHeight);
        Assert.Equal(200, model.Width);
        Assert.Equal(100, model.Height);
        Assert.Equal("test", model.Filename);
    }

    [Fact]
    public void PrepareBatchExport_CreatesCorrectItems()
    {
        var model = new ExportDialogModel
        {
            FilenameTemplate = "{name}-{artboard}",
            Format = ExportFormat.Png
        };

        var artboards = new[]
        {
            ("Page1", "<svg></svg>"),
            ("Page2", "<svg></svg>")
        };

        var items = _service.PrepareBatchExport(model, "doc", artboards);

        Assert.Equal(2, items.Count);
        Assert.Equal("doc-Page1.png", items[0].OutputFilename);
        Assert.Equal("doc-Page2.png", items[1].OutputFilename);
    }

    [Fact]
    public void Export_SvgFormat_Succeeds()
    {
        var model = new ExportDialogModel { Format = ExportFormat.Svg };
        var svg = "<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>";

        var result = _service.Export(model, svg);

        Assert.True(result.Success);
    }

    [Fact]
    public void Export_SvgOptimized_Succeeds()
    {
        var model = new ExportDialogModel { Format = ExportFormat.SvgOptimized };
        var svg = "<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>";

        var result = _service.Export(model, svg);

        Assert.True(result.Success);
    }

    [Fact]
    public void EstimateFileSize_ReturnsFormattedSize()
    {
        var model = new ExportDialogModel
        {
            Format = ExportFormat.Png,
            Width = 100,
            Height = 100
        };

        var size = _service.EstimateFileSize(model);

        Assert.NotEmpty(size);
        Assert.True(size.Contains("B") || size.Contains("KB") || size.Contains("MB"));
    }
}

public class ExportPresetTests
{
    [Fact]
    public void ExportPreset_HasExpectedValues()
    {
        Assert.True(Enum.IsDefined(typeof(ExportPreset), ExportPreset.Custom));
        Assert.True(Enum.IsDefined(typeof(ExportPreset), ExportPreset.Web));
        Assert.True(Enum.IsDefined(typeof(ExportPreset), ExportPreset.Print));
        Assert.True(Enum.IsDefined(typeof(ExportPreset), ExportPreset.Social));
        Assert.True(Enum.IsDefined(typeof(ExportPreset), ExportPreset.Icon));
        Assert.True(Enum.IsDefined(typeof(ExportPreset), ExportPreset.HighQuality));
    }
}
