using System.ComponentModel;
using System.Text.RegularExpressions;

namespace Bezier.Core.Services;

/// <summary>
/// Export preset for quick configuration.
/// </summary>
public enum ExportPreset
{
    Custom,
    Web,
    Print,
    Social,
    Icon,
    HighQuality
}

/// <summary>
/// Model for export dialog configuration.
/// </summary>
public partial class ExportDialogModel : INotifyPropertyChanged
{
    private ExportFormat _format = ExportFormat.Png;
    private ExportPreset _preset = ExportPreset.Custom;
    private string _filename = "export";
    private string _filenameTemplate = "{name}";
    private string _outputFolder = string.Empty;
    private double _scale = 1.0;
    private int? _width;
    private int? _height;
    private bool _maintainAspectRatio = true;
    private int _quality = 90;
    private bool _transparent = true;
    private string? _backgroundColor;
    private bool _exportAllArtboards;
    private bool _useArtboardNames = true;
    private int _selectedArtboardIndex = -1;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets or sets the export format.
    /// </summary>
    public ExportFormat Format
    {
        get => _format;
        set
        {
            if (_format != value)
            {
                _format = value;
                OnPropertyChanged(nameof(Format));
                OnPropertyChanged(nameof(SupportsTransparency));
                OnPropertyChanged(nameof(SupportsQuality));
                OnPropertyChanged(nameof(FileExtension));
                OnPropertyChanged(nameof(IsRasterFormat));
                OnPropertyChanged(nameof(IsVectorFormat));
                UpdateFilenameExtension();
            }
        }
    }

    /// <summary>
    /// Gets or sets the export preset.
    /// </summary>
    public ExportPreset Preset
    {
        get => _preset;
        set
        {
            if (_preset != value)
            {
                _preset = value;
                ApplyPreset(value);
                OnPropertyChanged(nameof(Preset));
            }
        }
    }

    /// <summary>
    /// Gets or sets the base filename (without extension).
    /// </summary>
    public string Filename
    {
        get => _filename;
        set
        {
            _filename = SanitizeFilename(value);
            OnPropertyChanged(nameof(Filename));
            OnPropertyChanged(nameof(FullFilename));
        }
    }

    /// <summary>
    /// Gets or sets the filename template for batch export.
    /// </summary>
    public string FilenameTemplate
    {
        get => _filenameTemplate;
        set
        {
            _filenameTemplate = value;
            OnPropertyChanged(nameof(FilenameTemplate));
        }
    }

    /// <summary>
    /// Gets or sets the output folder.
    /// </summary>
    public string OutputFolder
    {
        get => _outputFolder;
        set
        {
            _outputFolder = value;
            OnPropertyChanged(nameof(OutputFolder));
            OnPropertyChanged(nameof(FullPath));
        }
    }

    /// <summary>
    /// Gets or sets the scale factor.
    /// </summary>
    public double Scale
    {
        get => _scale;
        set
        {
            _scale = Math.Max(0.1, Math.Min(10, value));
            OnPropertyChanged(nameof(Scale));
            OnPropertyChanged(nameof(ScalePercentage));
            if (_maintainAspectRatio)
            {
                UpdateDimensionsFromScale();
            }
        }
    }

    /// <summary>
    /// Gets or sets the output width.
    /// </summary>
    public int? Width
    {
        get => _width;
        set
        {
            _width = value;
            OnPropertyChanged(nameof(Width));
            if (_maintainAspectRatio && value.HasValue && OriginalWidth > 0)
            {
                var ratio = (double)value.Value / OriginalWidth;
                _height = (int)(OriginalHeight * ratio);
                _scale = ratio;
                OnPropertyChanged(nameof(Height));
                OnPropertyChanged(nameof(Scale));
                OnPropertyChanged(nameof(ScalePercentage));
            }
        }
    }

    /// <summary>
    /// Gets or sets the output height.
    /// </summary>
    public int? Height
    {
        get => _height;
        set
        {
            _height = value;
            OnPropertyChanged(nameof(Height));
            if (_maintainAspectRatio && value.HasValue && OriginalHeight > 0)
            {
                var ratio = (double)value.Value / OriginalHeight;
                _width = (int)(OriginalWidth * ratio);
                _scale = ratio;
                OnPropertyChanged(nameof(Width));
                OnPropertyChanged(nameof(Scale));
                OnPropertyChanged(nameof(ScalePercentage));
            }
        }
    }

    /// <summary>
    /// Gets or sets whether to maintain aspect ratio.
    /// </summary>
    public bool MaintainAspectRatio
    {
        get => _maintainAspectRatio;
        set
        {
            _maintainAspectRatio = value;
            OnPropertyChanged(nameof(MaintainAspectRatio));
        }
    }

    /// <summary>
    /// Gets or sets the quality (0-100) for lossy formats.
    /// </summary>
    public int Quality
    {
        get => _quality;
        set
        {
            _quality = Math.Max(0, Math.Min(100, value));
            OnPropertyChanged(nameof(Quality));
        }
    }

    /// <summary>
    /// Gets or sets whether to use transparent background.
    /// </summary>
    public bool Transparent
    {
        get => _transparent;
        set
        {
            _transparent = value;
            OnPropertyChanged(nameof(Transparent));
        }
    }

    /// <summary>
    /// Gets or sets the background color (when not transparent).
    /// </summary>
    public string? BackgroundColor
    {
        get => _backgroundColor;
        set
        {
            _backgroundColor = value;
            OnPropertyChanged(nameof(BackgroundColor));
        }
    }

    /// <summary>
    /// Gets or sets whether to export all artboards.
    /// </summary>
    public bool ExportAllArtboards
    {
        get => _exportAllArtboards;
        set
        {
            _exportAllArtboards = value;
            OnPropertyChanged(nameof(ExportAllArtboards));
        }
    }

    /// <summary>
    /// Gets or sets whether to use artboard names in filenames.
    /// </summary>
    public bool UseArtboardNames
    {
        get => _useArtboardNames;
        set
        {
            _useArtboardNames = value;
            OnPropertyChanged(nameof(UseArtboardNames));
        }
    }

    /// <summary>
    /// Gets or sets the selected artboard index (-1 for all).
    /// </summary>
    public int SelectedArtboardIndex
    {
        get => _selectedArtboardIndex;
        set
        {
            _selectedArtboardIndex = value;
            OnPropertyChanged(nameof(SelectedArtboardIndex));
        }
    }

    /// <summary>
    /// Gets or sets the original SVG width.
    /// </summary>
    public double OriginalWidth { get; set; } = 100;

    /// <summary>
    /// Gets or sets the original SVG height.
    /// </summary>
    public double OriginalHeight { get; set; } = 100;

    /// <summary>
    /// Gets the file extension for the current format.
    /// </summary>
    public string FileExtension => ExportService.GetFileExtension(Format);

    /// <summary>
    /// Gets the full filename with extension.
    /// </summary>
    public string FullFilename => $"{Filename}{FileExtension}";

    /// <summary>
    /// Gets the full output path.
    /// </summary>
    public string FullPath => string.IsNullOrEmpty(OutputFolder) 
        ? FullFilename 
        : Path.Combine(OutputFolder, FullFilename);

    /// <summary>
    /// Gets the scale as percentage.
    /// </summary>
    public string ScalePercentage => $"{Scale * 100:F0}%";

    /// <summary>
    /// Gets whether the format supports transparency.
    /// </summary>
    public bool SupportsTransparency => Format is ExportFormat.Png or ExportFormat.WebP or ExportFormat.Svg 
        or ExportFormat.SvgOptimized or ExportFormat.SvgMinified;

    /// <summary>
    /// Gets whether the format supports quality setting.
    /// </summary>
    public bool SupportsQuality => Format is ExportFormat.Jpg or ExportFormat.WebP;

    /// <summary>
    /// Gets whether the format is a raster format.
    /// </summary>
    public bool IsRasterFormat => Format is ExportFormat.Png or ExportFormat.Jpg or ExportFormat.WebP or ExportFormat.Ico;

    /// <summary>
    /// Gets whether the format is a vector format.
    /// </summary>
    public bool IsVectorFormat => Format is ExportFormat.Svg or ExportFormat.SvgOptimized or ExportFormat.SvgMinified 
        or ExportFormat.Pdf or ExportFormat.Xaml;

    /// <summary>
    /// Applies a preset configuration.
    /// </summary>
    public void ApplyPreset(ExportPreset preset)
    {
        switch (preset)
        {
            case ExportPreset.Web:
                Format = ExportFormat.Png;
                Scale = 1.0;
                Quality = 85;
                Transparent = true;
                break;

            case ExportPreset.Print:
                Format = ExportFormat.Pdf;
                Scale = 1.0;
                break;

            case ExportPreset.Social:
                Format = ExportFormat.Jpg;
                Scale = 1.0;
                Quality = 90;
                Transparent = false;
                BackgroundColor = "#FFFFFF";
                break;

            case ExportPreset.Icon:
                Format = ExportFormat.Png;
                Transparent = true;
                break;

            case ExportPreset.HighQuality:
                Format = ExportFormat.Png;
                Scale = 2.0;
                Quality = 100;
                Transparent = true;
                break;
        }
    }

    /// <summary>
    /// Updates the filename extension when format changes.
    /// </summary>
    private void UpdateFilenameExtension()
    {
        OnPropertyChanged(nameof(FullFilename));
        OnPropertyChanged(nameof(FullPath));
    }

    /// <summary>
    /// Updates width/height from scale.
    /// </summary>
    private void UpdateDimensionsFromScale()
    {
        _width = (int)(OriginalWidth * _scale);
        _height = (int)(OriginalHeight * _scale);
        OnPropertyChanged(nameof(Width));
        OnPropertyChanged(nameof(Height));
    }

    /// <summary>
    /// Sanitizes a filename by removing invalid characters.
    /// </summary>
    private static string SanitizeFilename(string filename)
    {
        var invalid = Path.GetInvalidFileNameChars();
        return string.Concat(filename.Where(c => !invalid.Contains(c)));
    }

    /// <summary>
    /// Generates a filename from a template.
    /// </summary>
    public string GenerateFilename(string template, string documentName, string? artboardName = null, int? index = null)
    {
        var result = template;

        result = result.Replace("{name}", documentName);
        result = result.Replace("{artboard}", artboardName ?? "artboard");
        result = result.Replace("{index}", (index ?? 0).ToString());
        result = result.Replace("{date}", DateTime.Now.ToString("yyyy-MM-dd"));
        result = result.Replace("{time}", DateTime.Now.ToString("HHmmss"));
        result = result.Replace("{scale}", $"{Scale:F0}x");
        result = result.Replace("{width}", Width?.ToString() ?? "auto");
        result = result.Replace("{height}", Height?.ToString() ?? "auto");

        return SanitizeFilename(result);
    }

    /// <summary>
    /// Creates RasterExportOptions from the current configuration.
    /// </summary>
    public RasterExportOptions ToRasterOptions()
    {
        return new RasterExportOptions
        {
            Scale = Scale,
            Width = Width,
            Height = Height,
            Transparent = Transparent,
            BackgroundColor = BackgroundColor,
            JpegQuality = Quality,
            WebPQuality = Quality
        };
    }

    /// <summary>
    /// Creates SvgProcessingOptions from the current configuration.
    /// </summary>
    public SvgProcessingOptions ToSvgOptions()
    {
        return new SvgProcessingOptions
        {
            Minify = Format == ExportFormat.SvgMinified,
            PrettyPrint = Format != ExportFormat.SvgMinified
        };
    }

    /// <summary>
    /// Validates the export configuration.
    /// </summary>
    public (bool IsValid, string? ErrorMessage) Validate()
    {
        if (string.IsNullOrWhiteSpace(Filename))
            return (false, "Filename is required");

        if (IsRasterFormat && Width <= 0 && Height <= 0 && Scale <= 0)
            return (false, "Width, height, or scale must be specified for raster formats");

        if (SupportsQuality && (Quality < 0 || Quality > 100))
            return (false, "Quality must be between 0 and 100");

        return (true, null);
    }
}

/// <summary>
/// Batch export item.
/// </summary>
public class BatchExportItem
{
    public string Name { get; init; } = string.Empty;
    public string? ArtboardName { get; init; }
    public int Index { get; init; }
    public string SvgContent { get; init; } = string.Empty;
    public string OutputFilename { get; set; } = string.Empty;
    public bool IsSelected { get; set; } = true;
    public ExportResult? Result { get; set; }
}

/// <summary>
/// Service for managing export dialog operations.
/// </summary>
public class ExportDialogService
{
    private readonly ExportService _exportService;

    public ExportDialogService(ExportService? exportService = null)
    {
        _exportService = exportService ?? new ExportService();
    }

    /// <summary>
    /// Gets available export formats.
    /// </summary>
    public static IEnumerable<(ExportFormat Format, string Name, string Description)> AvailableFormats =>
    [
        (ExportFormat.Png, "PNG", "Portable Network Graphics - lossless with transparency"),
        (ExportFormat.Jpg, "JPEG", "Joint Photographic Experts Group - lossy compression"),
        (ExportFormat.WebP, "WebP", "Modern format with good compression and transparency"),
        (ExportFormat.Svg, "SVG", "Scalable Vector Graphics - standard"),
        (ExportFormat.SvgOptimized, "SVG (Optimized)", "Optimized SVG with reduced file size"),
        (ExportFormat.SvgMinified, "SVG (Minified)", "Minified SVG for production"),
        (ExportFormat.Pdf, "PDF", "Portable Document Format - vector"),
        (ExportFormat.Xaml, "XAML", "WPF DrawingImage resource"),
        (ExportFormat.ReactComponent, "React", "React/JSX component"),
        (ExportFormat.VueComponent, "Vue", "Vue single-file component"),
        (ExportFormat.CssClipPath, "CSS", "CSS clip-path"),
        (ExportFormat.Ico, "ICO", "Windows icon format")
    ];

    /// <summary>
    /// Gets available presets.
    /// </summary>
    public static IEnumerable<(ExportPreset Preset, string Name, string Description)> AvailablePresets =>
    [
        (ExportPreset.Custom, "Custom", "Configure all options manually"),
        (ExportPreset.Web, "Web", "PNG optimized for web use"),
        (ExportPreset.Print, "Print", "High-quality PDF for printing"),
        (ExportPreset.Social, "Social Media", "JPEG with white background"),
        (ExportPreset.Icon, "Icon", "PNG with transparency for icons"),
        (ExportPreset.HighQuality, "High Quality", "2x PNG with maximum quality")
    ];

    /// <summary>
    /// Gets common scale options.
    /// </summary>
    public static IEnumerable<(double Scale, string Label)> ScaleOptions =>
    [
        (0.5, "0.5x (50%)"),
        (1.0, "1x (100%)"),
        (1.5, "1.5x (150%)"),
        (2.0, "2x (200%)"),
        (3.0, "3x (300%)"),
        (4.0, "4x (400%)")
    ];

    /// <summary>
    /// Gets template variables.
    /// </summary>
    public static IEnumerable<(string Variable, string Description)> TemplateVariables =>
    [
        ("{name}", "Document name"),
        ("{artboard}", "Artboard name"),
        ("{index}", "Export index"),
        ("{date}", "Current date (YYYY-MM-DD)"),
        ("{time}", "Current time (HHMMSS)"),
        ("{scale}", "Scale factor"),
        ("{width}", "Output width"),
        ("{height}", "Output height")
    ];

    /// <summary>
    /// Creates a default export dialog model.
    /// </summary>
    public ExportDialogModel CreateDefaultModel(double svgWidth, double svgHeight, string? documentName = null)
    {
        return new ExportDialogModel
        {
            OriginalWidth = svgWidth,
            OriginalHeight = svgHeight,
            Filename = documentName ?? "export",
            Width = (int)svgWidth,
            Height = (int)svgHeight
        };
    }

    /// <summary>
    /// Prepares batch export items from artboards.
    /// </summary>
    public List<BatchExportItem> PrepareBatchExport(
        ExportDialogModel model,
        string documentName,
        IEnumerable<(string Name, string SvgContent)> artboards)
    {
        var items = new List<BatchExportItem>();
        var index = 0;

        foreach (var (name, content) in artboards)
        {
            var filename = model.GenerateFilename(
                model.FilenameTemplate,
                documentName,
                name,
                index
            );

            items.Add(new BatchExportItem
            {
                Name = name,
                ArtboardName = name,
                Index = index,
                SvgContent = content,
                OutputFilename = $"{filename}{model.FileExtension}"
            });

            index++;
        }

        return items;
    }

    /// <summary>
    /// Exports using the dialog model configuration.
    /// </summary>
    public ExportResult Export(ExportDialogModel model, string svgContent)
    {
        return model.Format switch
        {
            ExportFormat.Svg => _exportService.ExportSvg(svgContent, model.ToSvgOptions()),
            ExportFormat.SvgOptimized => _exportService.ExportSvgOptimized(svgContent),
            ExportFormat.SvgMinified => _exportService.ExportSvgMinified(svgContent),
            ExportFormat.Xaml => _exportService.ExportXaml(svgContent),
            ExportFormat.ReactComponent => _exportService.ExportReactComponent(svgContent),
            ExportFormat.VueComponent => _exportService.ExportVueComponent(svgContent),
            ExportFormat.CssClipPath => _exportService.ExportCssClipPath(svgContent),
            // Raster formats need SkiaSharp in Desktop layer
            _ => ExportResult.Failed($"Format {model.Format} requires desktop rendering", model.Format)
        };
    }

    /// <summary>
    /// Gets estimated file size for preview.
    /// </summary>
    public string EstimateFileSize(ExportDialogModel model)
    {
        // Rough estimates based on format and dimensions
        var pixelCount = (model.Width ?? model.OriginalWidth) * (model.Height ?? model.OriginalHeight);

        var bytes = model.Format switch
        {
            ExportFormat.Png => (long)(pixelCount * 4 * 0.5), // Approximate PNG compression
            ExportFormat.Jpg => (long)(pixelCount * 3 * (model.Quality / 100.0) * 0.3),
            ExportFormat.WebP => (long)(pixelCount * 3 * (model.Quality / 100.0) * 0.2),
            ExportFormat.Svg or ExportFormat.SvgOptimized or ExportFormat.SvgMinified => 5000, // Varies widely
            _ => 10000
        };

        return FormatFileSize(bytes);
    }

    private static string FormatFileSize(long bytes)
    {
        return bytes switch
        {
            < 1024 => $"{bytes} B",
            < 1024 * 1024 => $"{bytes / 1024.0:F1} KB",
            _ => $"{bytes / (1024.0 * 1024.0):F1} MB"
        };
    }
}
