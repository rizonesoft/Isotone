namespace Bezier.Tests;

using Bezier.Core.Services;

public class DocumentPresetTests
{
    [Fact]
    public void DocumentPreset_DefaultValues()
    {
        var preset = new DocumentPreset();

        Assert.Equal(800, preset.Width);
        Assert.Equal(600, preset.Height);
        Assert.Equal(DocumentUnit.Pixels, preset.Unit);
        Assert.Equal(ColorMode.RGB, preset.ColorMode);
        Assert.Equal(PresetCategory.Custom, preset.Category);
        Assert.False(preset.IsBuiltIn);
    }

    [Fact]
    public void DocumentPreset_WidthInPixels_ReturnsCorrectValue()
    {
        var preset = new DocumentPreset { Width = 100, Unit = DocumentUnit.Pixels };

        Assert.Equal(100, preset.WidthInPixels);
    }

    [Fact]
    public void DocumentPreset_ConvertToPixels_Millimeters()
    {
        // 25.4mm = 1 inch = 96 pixels at 96 DPI
        var pixels = DocumentPreset.ConvertToPixels(25.4, DocumentUnit.Millimeters, 96);

        Assert.Equal(96, pixels, 1);
    }

    [Fact]
    public void DocumentPreset_ConvertToPixels_Inches()
    {
        var pixels = DocumentPreset.ConvertToPixels(1, DocumentUnit.Inches, 96);

        Assert.Equal(96, pixels);
    }

    [Fact]
    public void DocumentPreset_ConvertToPixels_Points()
    {
        // 72 points = 1 inch = 96 pixels at 96 DPI
        var pixels = DocumentPreset.ConvertToPixels(72, DocumentUnit.Points, 96);

        Assert.Equal(96, pixels);
    }

    [Fact]
    public void DocumentPreset_ConvertFromPixels_Millimeters()
    {
        var mm = DocumentPreset.ConvertFromPixels(96, DocumentUnit.Millimeters, 96);

        Assert.Equal(25.4, mm, 1);
    }

    [Fact]
    public void DocumentPreset_ConvertFromPixels_Inches()
    {
        var inches = DocumentPreset.ConvertFromPixels(96, DocumentUnit.Inches, 96);

        Assert.Equal(1, inches);
    }
}

public class DocumentPresetsTests
{
    [Fact]
    public void DocumentPresets_All_ReturnsPresets()
    {
        var presets = DocumentPresets.All.ToList();

        Assert.True(presets.Count > 0);
    }

    [Fact]
    public void DocumentPresets_All_ContainsIconPresets()
    {
        var presets = DocumentPresets.All.ToList();

        Assert.Contains(presets, p => p.Category == PresetCategory.Icon);
    }

    [Fact]
    public void DocumentPresets_All_ContainsWebPresets()
    {
        var presets = DocumentPresets.All.ToList();

        Assert.Contains(presets, p => p.Category == PresetCategory.Web);
    }

    [Fact]
    public void DocumentPresets_All_ContainsPrintPresets()
    {
        var presets = DocumentPresets.All.ToList();

        Assert.Contains(presets, p => p.Category == PresetCategory.Print);
    }

    [Fact]
    public void DocumentPresets_All_ContainsSocialPresets()
    {
        var presets = DocumentPresets.All.ToList();

        Assert.Contains(presets, p => p.Category == PresetCategory.Social);
    }

    [Fact]
    public void DocumentPresets_All_ContainsMobilePresets()
    {
        var presets = DocumentPresets.All.ToList();

        Assert.Contains(presets, p => p.Category == PresetCategory.Mobile);
    }

    [Fact]
    public void DocumentPresets_GetByCategory_FiltersCorrectly()
    {
        var icons = DocumentPresets.GetByCategory(PresetCategory.Icon).ToList();

        Assert.All(icons, p => Assert.Equal(PresetCategory.Icon, p.Category));
    }

    [Fact]
    public void DocumentPresets_Icon16_HasCorrectDimensions()
    {
        var preset = DocumentPresets.Icon16;

        Assert.Equal(16, preset.Width);
        Assert.Equal(16, preset.Height);
        Assert.True(preset.IsBuiltIn);
    }

    [Fact]
    public void DocumentPresets_PrintA4_HasCorrectDimensions()
    {
        var preset = DocumentPresets.PrintA4;

        Assert.Equal(210, preset.Width);
        Assert.Equal(297, preset.Height);
        Assert.Equal(DocumentUnit.Millimeters, preset.Unit);
    }

    [Fact]
    public void DocumentPresets_SocialInstagramSquare_HasCorrectDimensions()
    {
        var preset = DocumentPresets.SocialInstagramSquare;

        Assert.Equal(1080, preset.Width);
        Assert.Equal(1080, preset.Height);
    }
}

public class RecentFileTests
{
    [Fact]
    public void RecentFile_FileName_ExtractsFromPath()
    {
        var recent = new RecentFile { FilePath = @"C:\Documents\test.svg" };

        Assert.Equal("test.svg", recent.FileName);
    }

    [Fact]
    public void RecentFile_DefaultLastOpened_IsSet()
    {
        var before = DateTime.UtcNow;
        var recent = new RecentFile { FilePath = "test.svg" };
        var after = DateTime.UtcNow;

        Assert.InRange(recent.LastOpened, before, after);
    }
}

public class FileOperationsServiceTests
{
    private readonly FileOperationsService _service;

    public FileOperationsServiceTests()
    {
        _service = new FileOperationsService();
    }

    [Fact]
    public void FileOperationsService_DefaultValues()
    {
        Assert.Null(_service.CurrentFilePath);
        Assert.Equal("Untitled", _service.CurrentFileName);
        Assert.False(_service.HasFile);
        Assert.False(_service.IsDirty);
    }

    [Fact]
    public void FileOperationsService_Title_ShowsUntitled()
    {
        Assert.Contains("Untitled", _service.Title);
        Assert.Contains("Bezier", _service.Title);
    }

    [Fact]
    public void FileOperationsService_Title_ShowsDirtyIndicator()
    {
        _service.IsDirty = true;

        Assert.Contains("*", _service.Title);
    }

    [Fact]
    public void FileOperationsService_CurrentFilePath_UpdatesFileName()
    {
        _service.CurrentFilePath = @"C:\test\document.svg";

        Assert.Equal("document.svg", _service.CurrentFileName);
        Assert.True(_service.HasFile);
    }

    [Fact]
    public void FileOperationsService_AddToRecentFiles_AddsFile()
    {
        _service.ClearRecentFiles();
        _service.AddToRecentFiles(@"C:\test.svg");

        Assert.Single(_service.RecentFiles);
        Assert.Equal(@"C:\test.svg", _service.RecentFiles[0].FilePath);
    }

    [Fact]
    public void FileOperationsService_AddToRecentFiles_MovesToTop()
    {
        _service.ClearRecentFiles();
        _service.AddToRecentFiles(@"C:\first.svg");
        _service.AddToRecentFiles(@"C:\second.svg");
        _service.AddToRecentFiles(@"C:\first.svg");

        Assert.Equal(2, _service.RecentFiles.Count);
        Assert.Equal(@"C:\first.svg", _service.RecentFiles[0].FilePath);
    }

    [Fact]
    public void FileOperationsService_AddToRecentFiles_LimitsTo10()
    {
        _service.ClearRecentFiles();
        for (var i = 0; i < 15; i++)
        {
            _service.AddToRecentFiles($@"C:\file{i}.svg");
        }

        Assert.Equal(FileOperationsService.MaxRecentFiles, _service.RecentFiles.Count);
    }

    [Fact]
    public void FileOperationsService_ClearRecentFiles_ClearsList()
    {
        _service.AddToRecentFiles(@"C:\test.svg");

        _service.ClearRecentFiles();

        Assert.Empty(_service.RecentFiles);
    }

    [Fact]
    public void FileOperationsService_RemoveFromRecentFiles_RemovesFile()
    {
        _service.ClearRecentFiles();
        _service.AddToRecentFiles(@"C:\test.svg");

        _service.RemoveFromRecentFiles(@"C:\test.svg");

        Assert.Empty(_service.RecentFiles);
    }

    [Fact]
    public void FileOperationsService_AddCustomPreset_AddsToList()
    {
        var preset = new DocumentPreset { Name = "Custom", Width = 500, Height = 500 };

        _service.AddCustomPreset(preset);

        Assert.Contains(preset, _service.CustomPresets);
        Assert.Contains(preset, _service.AllPresets);
    }

    [Fact]
    public void FileOperationsService_RemoveCustomPreset_RemovesFromList()
    {
        var preset = new DocumentPreset { Name = "Custom" };
        _service.AddCustomPreset(preset);

        var removed = _service.RemoveCustomPreset(preset.Id);

        Assert.True(removed);
        Assert.DoesNotContain(preset, _service.CustomPresets);
    }

    [Fact]
    public void FileOperationsService_CreateNewDocument_ReturnsSvg()
    {
        var preset = DocumentPresets.Icon64;

        var svg = _service.CreateNewDocument(preset);

        Assert.Contains("<svg", svg);
        Assert.Contains("width=\"64\"", svg);
        Assert.Contains("height=\"64\"", svg);
    }

    [Fact]
    public void FileOperationsService_CreateNewDocument_CustomSize()
    {
        var svg = _service.CreateNewDocument(800, 600);

        Assert.Contains("width=\"800\"", svg);
        Assert.Contains("height=\"600\"", svg);
    }

    [Fact]
    public void FileOperationsService_CreateNewDocument_WithUnits()
    {
        var svg = _service.CreateNewDocument(1, 1, DocumentUnit.Inches);

        Assert.Contains("width=\"96\"", svg); // 1 inch = 96 pixels
        Assert.Contains("height=\"96\"", svg);
    }

    [Fact]
    public void FileOperationsService_CreateNewDocument_ResetsState()
    {
        _service.CurrentFilePath = @"C:\existing.svg";
        _service.IsDirty = true;

        _service.CreateNewDocument(DocumentPresets.Icon64);

        Assert.Null(_service.CurrentFilePath);
        Assert.False(_service.IsDirty);
    }

    [Fact]
    public void FileOperationsService_MarkFileOpened_SetsPath()
    {
        _service.MarkFileOpened(@"C:\test.svg");

        Assert.Equal(@"C:\test.svg", _service.CurrentFilePath);
        Assert.False(_service.IsDirty);
    }

    [Fact]
    public void FileOperationsService_MarkFileOpened_AddsToRecent()
    {
        _service.ClearRecentFiles();

        _service.MarkFileOpened(@"C:\test.svg");

        Assert.Single(_service.RecentFiles);
    }

    [Fact]
    public void FileOperationsService_MarkFileSaved_ClearsDirty()
    {
        _service.IsDirty = true;

        _service.MarkFileSaved(@"C:\test.svg");

        Assert.False(_service.IsDirty);
        Assert.Equal(@"C:\test.svg", _service.CurrentFilePath);
    }

    [Fact]
    public void FileOperationsService_ShouldAutoSave_ReturnsFalse_WhenNotDirty()
    {
        _service.IsDirty = false;

        Assert.False(_service.ShouldAutoSave());
    }

    [Fact]
    public void FileOperationsService_AllPresets_IncludesBuiltIn()
    {
        var allPresets = _service.AllPresets.ToList();

        Assert.Contains(allPresets, p => p.IsBuiltIn);
    }

    [Fact]
    public void FileOperationsService_DraftsFolder_IsSet()
    {
        Assert.NotNull(_service.DraftsFolder);
        Assert.Contains("Drafts", _service.DraftsFolder);
    }
}

public class AutoSaveDraftTests
{
    [Fact]
    public void AutoSaveDraft_DefaultValues()
    {
        var draft = new AutoSaveDraft();

        Assert.Equal(string.Empty, draft.DraftPath);
        Assert.Null(draft.OriginalPath);
        Assert.Equal("Untitled", draft.DocumentName);
    }

    [Fact]
    public void AutoSaveDraft_SavedAt_IsSet()
    {
        var before = DateTime.UtcNow;
        var draft = new AutoSaveDraft();
        var after = DateTime.UtcNow;

        Assert.InRange(draft.SavedAt, before, after);
    }
}

public class DocumentUnitTests
{
    [Theory]
    [InlineData(DocumentUnit.Pixels)]
    [InlineData(DocumentUnit.Millimeters)]
    [InlineData(DocumentUnit.Centimeters)]
    [InlineData(DocumentUnit.Inches)]
    [InlineData(DocumentUnit.Points)]
    public void DocumentUnit_AllValues_ConvertRoundTrip(DocumentUnit unit)
    {
        var original = 100.0;
        var pixels = DocumentPreset.ConvertToPixels(original, unit);
        var converted = DocumentPreset.ConvertFromPixels(pixels, unit);

        Assert.Equal(original, converted, 5);
    }
}

public class ColorModeTests
{
    [Fact]
    public void ColorMode_HasExpectedValues()
    {
        Assert.Equal(0, (int)ColorMode.RGB);
        Assert.Equal(1, (int)ColorMode.CMYK);
        Assert.Equal(2, (int)ColorMode.Grayscale);
    }
}

public class PresetCategoryTests
{
    [Fact]
    public void PresetCategory_HasExpectedValues()
    {
        Assert.True(Enum.IsDefined(typeof(PresetCategory), PresetCategory.Icon));
        Assert.True(Enum.IsDefined(typeof(PresetCategory), PresetCategory.Web));
        Assert.True(Enum.IsDefined(typeof(PresetCategory), PresetCategory.Print));
        Assert.True(Enum.IsDefined(typeof(PresetCategory), PresetCategory.Social));
        Assert.True(Enum.IsDefined(typeof(PresetCategory), PresetCategory.Mobile));
        Assert.True(Enum.IsDefined(typeof(PresetCategory), PresetCategory.Custom));
    }
}
