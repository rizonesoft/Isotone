using System.ComponentModel;
using System.Text.Json;

namespace Bezier.Core.Services;

/// <summary>
/// Unit of measurement for document dimensions.
/// </summary>
public enum DocumentUnit
{
    Pixels,
    Millimeters,
    Centimeters,
    Inches,
    Points
}

/// <summary>
/// Color mode for the document.
/// </summary>
public enum ColorMode
{
    RGB,
    CMYK,
    Grayscale
}

/// <summary>
/// Category of document preset.
/// </summary>
public enum PresetCategory
{
    Icon,
    Web,
    Print,
    Social,
    Mobile,
    Custom
}

/// <summary>
/// Represents a document preset/template.
/// </summary>
public class DocumentPreset
{
    public string Id { get; init; } = Guid.NewGuid().ToString();
    public string Name { get; init; } = "Untitled";
    public PresetCategory Category { get; init; } = PresetCategory.Custom;
    public double Width { get; init; } = 800;
    public double Height { get; init; } = 600;
    public DocumentUnit Unit { get; init; } = DocumentUnit.Pixels;
    public ColorMode ColorMode { get; init; } = ColorMode.RGB;
    public string? Description { get; init; }
    public bool IsBuiltIn { get; init; }

    /// <summary>
    /// Gets the width in pixels.
    /// </summary>
    public double WidthInPixels => ConvertToPixels(Width, Unit);

    /// <summary>
    /// Gets the height in pixels.
    /// </summary>
    public double HeightInPixels => ConvertToPixels(Height, Unit);

    /// <summary>
    /// Converts a value to pixels based on unit.
    /// </summary>
    public static double ConvertToPixels(double value, DocumentUnit unit, double dpi = 96)
    {
        return unit switch
        {
            DocumentUnit.Pixels => value,
            DocumentUnit.Millimeters => value * dpi / 25.4,
            DocumentUnit.Centimeters => value * dpi / 2.54,
            DocumentUnit.Inches => value * dpi,
            DocumentUnit.Points => value * dpi / 72,
            _ => value
        };
    }

    /// <summary>
    /// Converts pixels to a specific unit.
    /// </summary>
    public static double ConvertFromPixels(double pixels, DocumentUnit unit, double dpi = 96)
    {
        return unit switch
        {
            DocumentUnit.Pixels => pixels,
            DocumentUnit.Millimeters => pixels * 25.4 / dpi,
            DocumentUnit.Centimeters => pixels * 2.54 / dpi,
            DocumentUnit.Inches => pixels / dpi,
            DocumentUnit.Points => pixels * 72 / dpi,
            _ => pixels
        };
    }
}

/// <summary>
/// Built-in document presets.
/// </summary>
public static class DocumentPresets
{
    // Icon presets
    public static DocumentPreset Icon16 => new() { Name = "Icon 16×16", Category = PresetCategory.Icon, Width = 16, Height = 16, IsBuiltIn = true };
    public static DocumentPreset Icon32 => new() { Name = "Icon 32×32", Category = PresetCategory.Icon, Width = 32, Height = 32, IsBuiltIn = true };
    public static DocumentPreset Icon48 => new() { Name = "Icon 48×48", Category = PresetCategory.Icon, Width = 48, Height = 48, IsBuiltIn = true };
    public static DocumentPreset Icon64 => new() { Name = "Icon 64×64", Category = PresetCategory.Icon, Width = 64, Height = 64, IsBuiltIn = true };
    public static DocumentPreset Icon128 => new() { Name = "Icon 128×128", Category = PresetCategory.Icon, Width = 128, Height = 128, IsBuiltIn = true };
    public static DocumentPreset Icon256 => new() { Name = "Icon 256×256", Category = PresetCategory.Icon, Width = 256, Height = 256, IsBuiltIn = true };
    public static DocumentPreset Icon512 => new() { Name = "Icon 512×512", Category = PresetCategory.Icon, Width = 512, Height = 512, IsBuiltIn = true };

    // Web presets
    public static DocumentPreset WebBanner => new() { Name = "Web Banner", Category = PresetCategory.Web, Width = 728, Height = 90, IsBuiltIn = true, Description = "Standard leaderboard" };
    public static DocumentPreset WebSquare => new() { Name = "Web Square", Category = PresetCategory.Web, Width = 300, Height = 250, IsBuiltIn = true, Description = "Medium rectangle" };
    public static DocumentPreset WebSkyscraper => new() { Name = "Skyscraper", Category = PresetCategory.Web, Width = 160, Height = 600, IsBuiltIn = true };
    public static DocumentPreset WebHero => new() { Name = "Hero Image", Category = PresetCategory.Web, Width = 1920, Height = 1080, IsBuiltIn = true, Description = "Full HD" };

    // Print presets
    public static DocumentPreset PrintA4 => new() { Name = "A4", Category = PresetCategory.Print, Width = 210, Height = 297, Unit = DocumentUnit.Millimeters, IsBuiltIn = true };
    public static DocumentPreset PrintA3 => new() { Name = "A3", Category = PresetCategory.Print, Width = 297, Height = 420, Unit = DocumentUnit.Millimeters, IsBuiltIn = true };
    public static DocumentPreset PrintLetter => new() { Name = "Letter", Category = PresetCategory.Print, Width = 8.5, Height = 11, Unit = DocumentUnit.Inches, IsBuiltIn = true };
    public static DocumentPreset PrintLegal => new() { Name = "Legal", Category = PresetCategory.Print, Width = 8.5, Height = 14, Unit = DocumentUnit.Inches, IsBuiltIn = true };
    public static DocumentPreset PrintBusinessCard => new() { Name = "Business Card", Category = PresetCategory.Print, Width = 3.5, Height = 2, Unit = DocumentUnit.Inches, IsBuiltIn = true };

    // Social media presets
    public static DocumentPreset SocialFacebookPost => new() { Name = "Facebook Post", Category = PresetCategory.Social, Width = 1200, Height = 630, IsBuiltIn = true };
    public static DocumentPreset SocialInstagramSquare => new() { Name = "Instagram Square", Category = PresetCategory.Social, Width = 1080, Height = 1080, IsBuiltIn = true };
    public static DocumentPreset SocialInstagramStory => new() { Name = "Instagram Story", Category = PresetCategory.Social, Width = 1080, Height = 1920, IsBuiltIn = true };
    public static DocumentPreset SocialTwitterPost => new() { Name = "Twitter Post", Category = PresetCategory.Social, Width = 1200, Height = 675, IsBuiltIn = true };
    public static DocumentPreset SocialLinkedInBanner => new() { Name = "LinkedIn Banner", Category = PresetCategory.Social, Width = 1584, Height = 396, IsBuiltIn = true };
    public static DocumentPreset SocialYouTubeThumbnail => new() { Name = "YouTube Thumbnail", Category = PresetCategory.Social, Width = 1280, Height = 720, IsBuiltIn = true };

    // Mobile presets
    public static DocumentPreset MobileIPhoneApp => new() { Name = "iPhone App Icon", Category = PresetCategory.Mobile, Width = 1024, Height = 1024, IsBuiltIn = true };
    public static DocumentPreset MobileAndroidApp => new() { Name = "Android App Icon", Category = PresetCategory.Mobile, Width = 512, Height = 512, IsBuiltIn = true };
    public static DocumentPreset MobileSplash => new() { Name = "Mobile Splash", Category = PresetCategory.Mobile, Width = 1242, Height = 2688, IsBuiltIn = true };

    /// <summary>
    /// Gets all built-in presets.
    /// </summary>
    public static IEnumerable<DocumentPreset> All =>
    [
        Icon16, Icon32, Icon48, Icon64, Icon128, Icon256, Icon512,
        WebBanner, WebSquare, WebSkyscraper, WebHero,
        PrintA4, PrintA3, PrintLetter, PrintLegal, PrintBusinessCard,
        SocialFacebookPost, SocialInstagramSquare, SocialInstagramStory, SocialTwitterPost, SocialLinkedInBanner, SocialYouTubeThumbnail,
        MobileIPhoneApp, MobileAndroidApp, MobileSplash
    ];

    /// <summary>
    /// Gets presets by category.
    /// </summary>
    public static IEnumerable<DocumentPreset> GetByCategory(PresetCategory category)
    {
        return All.Where(p => p.Category == category);
    }
}

/// <summary>
/// Represents a recent file entry.
/// </summary>
public class RecentFile
{
    public string FilePath { get; init; } = string.Empty;
    public string FileName => Path.GetFileName(FilePath);
    public DateTime LastOpened { get; init; } = DateTime.UtcNow;
    public bool Exists => File.Exists(FilePath);
}

/// <summary>
/// Auto-save draft information.
/// </summary>
public class AutoSaveDraft
{
    public string DraftPath { get; init; } = string.Empty;
    public string? OriginalPath { get; init; }
    public DateTime SavedAt { get; init; } = DateTime.UtcNow;
    public string DocumentName { get; init; } = "Untitled";
}

/// <summary>
/// Service for managing file operations.
/// </summary>
public class FileOperationsService : INotifyPropertyChanged
{
    private readonly List<RecentFile> _recentFiles = [];
    private readonly List<DocumentPreset> _customPresets = [];
    private string? _currentFilePath;
    private bool _isDirty;
    private DateTime _lastAutoSave = DateTime.MinValue;
    private readonly string _draftsFolder;
    private readonly string _settingsPath;

    public const int MaxRecentFiles = 10;
    public const int AutoSaveIntervalMinutes = 2;

    public event PropertyChangedEventHandler? PropertyChanged;
    public event EventHandler<AutoSaveDraft>? DraftRecovered;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    public FileOperationsService()
    {
        var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        var bezierFolder = Path.Combine(appData, "Bezier");
        _draftsFolder = Path.Combine(bezierFolder, "Drafts");
        _settingsPath = Path.Combine(bezierFolder, "recent-files.json");

        Directory.CreateDirectory(_draftsFolder);
        LoadRecentFiles();
    }

    /// <summary>
    /// Gets the current file path.
    /// </summary>
    public string? CurrentFilePath
    {
        get => _currentFilePath;
        set
        {
            _currentFilePath = value;
            OnPropertyChanged(nameof(CurrentFilePath));
            OnPropertyChanged(nameof(CurrentFileName));
            OnPropertyChanged(nameof(HasFile));
        }
    }

    /// <summary>
    /// Gets the current file name.
    /// </summary>
    public string CurrentFileName => _currentFilePath != null ? Path.GetFileName(_currentFilePath) : "Untitled";

    /// <summary>
    /// Gets whether a file is currently open.
    /// </summary>
    public bool HasFile => !string.IsNullOrEmpty(_currentFilePath);

    /// <summary>
    /// Gets or sets whether the document has unsaved changes.
    /// </summary>
    public bool IsDirty
    {
        get => _isDirty;
        set { _isDirty = value; OnPropertyChanged(nameof(IsDirty)); OnPropertyChanged(nameof(Title)); }
    }

    /// <summary>
    /// Gets the window title.
    /// </summary>
    public string Title => $"{CurrentFileName}{(_isDirty ? " *" : "")} - Bezier";

    /// <summary>
    /// Gets the recent files.
    /// </summary>
    public IReadOnlyList<RecentFile> RecentFiles => _recentFiles;

    /// <summary>
    /// Gets all document presets (built-in + custom).
    /// </summary>
    public IEnumerable<DocumentPreset> AllPresets => DocumentPresets.All.Concat(_customPresets);

    /// <summary>
    /// Gets custom presets.
    /// </summary>
    public IReadOnlyList<DocumentPreset> CustomPresets => _customPresets;

    /// <summary>
    /// Adds a file to recent files.
    /// </summary>
    public void AddToRecentFiles(string filePath)
    {
        _recentFiles.RemoveAll(f => f.FilePath.Equals(filePath, StringComparison.OrdinalIgnoreCase));
        _recentFiles.Insert(0, new RecentFile { FilePath = filePath, LastOpened = DateTime.UtcNow });

        while (_recentFiles.Count > MaxRecentFiles)
        {
            _recentFiles.RemoveAt(_recentFiles.Count - 1);
        }

        SaveRecentFiles();
        OnPropertyChanged(nameof(RecentFiles));
    }

    /// <summary>
    /// Clears recent files.
    /// </summary>
    public void ClearRecentFiles()
    {
        _recentFiles.Clear();
        SaveRecentFiles();
        OnPropertyChanged(nameof(RecentFiles));
    }

    /// <summary>
    /// Removes a specific file from recent files.
    /// </summary>
    public void RemoveFromRecentFiles(string filePath)
    {
        _recentFiles.RemoveAll(f => f.FilePath.Equals(filePath, StringComparison.OrdinalIgnoreCase));
        SaveRecentFiles();
        OnPropertyChanged(nameof(RecentFiles));
    }

    /// <summary>
    /// Adds a custom preset.
    /// </summary>
    public void AddCustomPreset(DocumentPreset preset)
    {
        _customPresets.Add(preset);
        OnPropertyChanged(nameof(CustomPresets));
        OnPropertyChanged(nameof(AllPresets));
    }

    /// <summary>
    /// Removes a custom preset.
    /// </summary>
    public bool RemoveCustomPreset(string presetId)
    {
        var removed = _customPresets.RemoveAll(p => p.Id == presetId) > 0;
        if (removed)
        {
            OnPropertyChanged(nameof(CustomPresets));
            OnPropertyChanged(nameof(AllPresets));
        }
        return removed;
    }

    /// <summary>
    /// Creates a new document from a preset.
    /// </summary>
    public string CreateNewDocument(DocumentPreset preset)
    {
        CurrentFilePath = null;
        IsDirty = false;

        return $"""
            <svg xmlns="http://www.w3.org/2000/svg" 
                 width="{preset.WidthInPixels}" 
                 height="{preset.HeightInPixels}"
                 viewBox="0 0 {preset.WidthInPixels} {preset.HeightInPixels}">
            </svg>
            """;
    }

    /// <summary>
    /// Creates a new document with custom dimensions.
    /// </summary>
    public string CreateNewDocument(double width, double height, DocumentUnit unit = DocumentUnit.Pixels)
    {
        var widthPx = DocumentPreset.ConvertToPixels(width, unit);
        var heightPx = DocumentPreset.ConvertToPixels(height, unit);

        CurrentFilePath = null;
        IsDirty = false;

        return $"""
            <svg xmlns="http://www.w3.org/2000/svg" 
                 width="{widthPx}" 
                 height="{heightPx}"
                 viewBox="0 0 {widthPx} {heightPx}">
            </svg>
            """;
    }

    /// <summary>
    /// Marks document as opened from a file.
    /// </summary>
    public void MarkFileOpened(string filePath)
    {
        CurrentFilePath = filePath;
        IsDirty = false;
        AddToRecentFiles(filePath);
    }

    /// <summary>
    /// Marks document as saved.
    /// </summary>
    public void MarkFileSaved(string filePath)
    {
        CurrentFilePath = filePath;
        IsDirty = false;
        AddToRecentFiles(filePath);
        DeleteAutoSaveDraft();
    }

    /// <summary>
    /// Checks if auto-save should run.
    /// </summary>
    public bool ShouldAutoSave()
    {
        if (!_isDirty) return false;
        var elapsed = DateTime.UtcNow - _lastAutoSave;
        return elapsed.TotalMinutes >= AutoSaveIntervalMinutes;
    }

    /// <summary>
    /// Creates an auto-save draft.
    /// </summary>
    public string CreateAutoSaveDraft(string content)
    {
        var draftName = $"draft_{DateTime.UtcNow:yyyyMMdd_HHmmss}.svg";
        var draftPath = Path.Combine(_draftsFolder, draftName);

        File.WriteAllText(draftPath, content);
        _lastAutoSave = DateTime.UtcNow;

        // Save draft metadata
        var metaPath = Path.Combine(_draftsFolder, "draft-meta.json");
        var meta = new AutoSaveDraft
        {
            DraftPath = draftPath,
            OriginalPath = _currentFilePath,
            SavedAt = DateTime.UtcNow,
            DocumentName = CurrentFileName
        };
        File.WriteAllText(metaPath, JsonSerializer.Serialize(meta));

        return draftPath;
    }

    /// <summary>
    /// Deletes the current auto-save draft.
    /// </summary>
    public void DeleteAutoSaveDraft()
    {
        var metaPath = Path.Combine(_draftsFolder, "draft-meta.json");
        if (File.Exists(metaPath))
        {
            try
            {
                var meta = JsonSerializer.Deserialize<AutoSaveDraft>(File.ReadAllText(metaPath));
                if (meta != null && File.Exists(meta.DraftPath))
                {
                    File.Delete(meta.DraftPath);
                }
                File.Delete(metaPath);
            }
            catch { /* Ignore cleanup errors */ }
        }
    }

    /// <summary>
    /// Checks for recovery files on startup.
    /// </summary>
    public AutoSaveDraft? CheckForRecovery()
    {
        var metaPath = Path.Combine(_draftsFolder, "draft-meta.json");
        if (!File.Exists(metaPath)) return null;

        try
        {
            var meta = JsonSerializer.Deserialize<AutoSaveDraft>(File.ReadAllText(metaPath));
            if (meta != null && File.Exists(meta.DraftPath))
            {
                return meta;
            }
        }
        catch { /* Ignore read errors */ }

        return null;
    }

    /// <summary>
    /// Recovers content from a draft.
    /// </summary>
    public string? RecoverFromDraft(AutoSaveDraft draft)
    {
        if (!File.Exists(draft.DraftPath)) return null;

        var content = File.ReadAllText(draft.DraftPath);
        CurrentFilePath = draft.OriginalPath;
        IsDirty = true;
        DraftRecovered?.Invoke(this, draft);

        return content;
    }

    /// <summary>
    /// Gets the drafts folder path.
    /// </summary>
    public string DraftsFolder => _draftsFolder;

    private void LoadRecentFiles()
    {
        if (!File.Exists(_settingsPath)) return;

        try
        {
            var json = File.ReadAllText(_settingsPath);
            var paths = JsonSerializer.Deserialize<List<string>>(json);
            if (paths != null)
            {
                _recentFiles.Clear();
                foreach (var path in paths.Take(MaxRecentFiles))
                {
                    _recentFiles.Add(new RecentFile { FilePath = path });
                }
            }
        }
        catch { /* Ignore load errors */ }
    }

    private void SaveRecentFiles()
    {
        try
        {
            Directory.CreateDirectory(Path.GetDirectoryName(_settingsPath)!);
            var paths = _recentFiles.Select(f => f.FilePath).ToList();
            File.WriteAllText(_settingsPath, JsonSerializer.Serialize(paths));
        }
        catch { /* Ignore save errors */ }
    }
}
