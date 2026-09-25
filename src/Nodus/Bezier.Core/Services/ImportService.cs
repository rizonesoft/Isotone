using System.Text;
using System.Xml;

namespace Bezier.Core.Services;

/// <summary>
/// Supported import formats.
/// </summary>
public enum ImportFormat
{
    Unknown,
    Svg,
    Ai,
    Eps,
    Pdf,
    Png,
    Jpg,
    Gif,
    Bmp,
    WebP,
    Clipboard
}

/// <summary>
/// Result of an import operation.
/// </summary>
public class ImportResult
{
    public bool Success { get; init; }
    public string? SvgContent { get; init; }
    public string? ErrorMessage { get; init; }
    public ImportFormat DetectedFormat { get; init; }
    public string? SourcePath { get; init; }
    public List<string> Warnings { get; init; } = [];

    public static ImportResult Succeeded(string svgContent, ImportFormat format, string? sourcePath = null)
    {
        return new ImportResult
        {
            Success = true,
            SvgContent = svgContent,
            DetectedFormat = format,
            SourcePath = sourcePath
        };
    }

    public static ImportResult Failed(string errorMessage, ImportFormat format = ImportFormat.Unknown)
    {
        return new ImportResult
        {
            Success = false,
            ErrorMessage = errorMessage,
            DetectedFormat = format
        };
    }
}

/// <summary>
/// Options for importing files.
/// </summary>
public class ImportOptions
{
    public bool PreserveIds { get; set; } = true;
    public bool PreserveStyles { get; set; } = true;
    public bool ConvertTextToPath { get; set; } = false;
    public bool EmbedImages { get; set; } = true;
    public double? MaxWidth { get; set; }
    public double? MaxHeight { get; set; }
    public string? DefaultUnit { get; set; } = "px";
}

/// <summary>
/// Clipboard data for paste operations.
/// </summary>
public class ClipboardData
{
    public bool HasSvg { get; init; }
    public bool HasImage { get; init; }
    public bool HasText { get; init; }
    public string? SvgContent { get; init; }
    public byte[]? ImageData { get; init; }
    public string? ImageFormat { get; init; }
    public string? TextContent { get; init; }
}

/// <summary>
/// Service for importing various file formats into SVG.
/// </summary>
public class ImportService
{
    private static readonly Dictionary<string, ImportFormat> ExtensionMap = new(StringComparer.OrdinalIgnoreCase)
    {
        [".svg"] = ImportFormat.Svg,
        [".ai"] = ImportFormat.Ai,
        [".eps"] = ImportFormat.Eps,
        [".pdf"] = ImportFormat.Pdf,
        [".png"] = ImportFormat.Png,
        [".jpg"] = ImportFormat.Jpg,
        [".jpeg"] = ImportFormat.Jpg,
        [".gif"] = ImportFormat.Gif,
        [".bmp"] = ImportFormat.Bmp,
        [".webp"] = ImportFormat.WebP
    };

    private static readonly Dictionary<string, string> MimeTypeMap = new(StringComparer.OrdinalIgnoreCase)
    {
        ["image/svg+xml"] = "svg",
        ["image/png"] = "png",
        ["image/jpeg"] = "jpg",
        ["image/gif"] = "gif",
        ["image/bmp"] = "bmp",
        ["image/webp"] = "webp"
    };

    /// <summary>
    /// Detects the format of a file by extension.
    /// </summary>
    public static ImportFormat DetectFormatByExtension(string filePath)
    {
        var ext = Path.GetExtension(filePath);
        return ExtensionMap.GetValueOrDefault(ext, ImportFormat.Unknown);
    }

    /// <summary>
    /// Detects the format by file content (magic bytes).
    /// </summary>
    public static ImportFormat DetectFormatByContent(byte[] data)
    {
        if (data.Length < 8) return ImportFormat.Unknown;

        // PNG: 89 50 4E 47 0D 0A 1A 0A
        if (data[0] == 0x89 && data[1] == 0x50 && data[2] == 0x4E && data[3] == 0x47)
            return ImportFormat.Png;

        // JPEG: FF D8 FF
        if (data[0] == 0xFF && data[1] == 0xD8 && data[2] == 0xFF)
            return ImportFormat.Jpg;

        // GIF: 47 49 46 38
        if (data[0] == 0x47 && data[1] == 0x49 && data[2] == 0x46 && data[3] == 0x38)
            return ImportFormat.Gif;

        // BMP: 42 4D
        if (data[0] == 0x42 && data[1] == 0x4D)
            return ImportFormat.Bmp;

        // WebP: 52 49 46 46 ... 57 45 42 50
        if (data[0] == 0x52 && data[1] == 0x49 && data[2] == 0x46 && data[3] == 0x46 &&
            data.Length > 11 && data[8] == 0x57 && data[9] == 0x45 && data[10] == 0x42 && data[11] == 0x50)
            return ImportFormat.WebP;

        // PDF: 25 50 44 46 (%PDF)
        if (data[0] == 0x25 && data[1] == 0x50 && data[2] == 0x44 && data[3] == 0x46)
            return ImportFormat.Pdf;

        // EPS: %!PS
        if (data[0] == 0x25 && data[1] == 0x21 && data[2] == 0x50 && data[3] == 0x53)
            return ImportFormat.Eps;

        // Try text-based formats
        var text = Encoding.UTF8.GetString(data, 0, Math.Min(1024, data.Length));
        if (text.Contains("<svg", StringComparison.OrdinalIgnoreCase))
            return ImportFormat.Svg;

        if (text.Contains("%AI") || text.Contains("%%Creator: Adobe Illustrator"))
            return ImportFormat.Ai;

        return ImportFormat.Unknown;
    }

    /// <summary>
    /// Gets supported file filter for open dialogs.
    /// </summary>
    public static string GetFileFilter()
    {
        return "All Supported|*.svg;*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp;*.ai;*.eps;*.pdf|" +
               "SVG Files|*.svg|" +
               "Image Files|*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp|" +
               "Adobe Illustrator|*.ai|" +
               "EPS Files|*.eps|" +
               "PDF Files|*.pdf|" +
               "All Files|*.*";
    }

    /// <summary>
    /// Imports a file.
    /// </summary>
    public ImportResult ImportFile(string filePath, ImportOptions? options = null)
    {
        options ??= new ImportOptions();

        if (!File.Exists(filePath))
            return ImportResult.Failed($"File not found: {filePath}");

        var format = DetectFormatByExtension(filePath);
        if (format == ImportFormat.Unknown)
        {
            var data = File.ReadAllBytes(filePath);
            format = DetectFormatByContent(data);
        }

        return format switch
        {
            ImportFormat.Svg => ImportSvg(filePath, options),
            ImportFormat.Png or ImportFormat.Jpg or ImportFormat.Gif or ImportFormat.Bmp or ImportFormat.WebP
                => ImportRasterImage(filePath, format, options),
            ImportFormat.Ai => ImportAdobeIllustrator(filePath, options),
            ImportFormat.Eps => ImportEps(filePath, options),
            ImportFormat.Pdf => ImportPdf(filePath, options),
            _ => ImportResult.Failed($"Unsupported format: {format}", format)
        };
    }

    /// <summary>
    /// Imports SVG content from a string.
    /// </summary>
    public ImportResult ImportSvgContent(string svgContent, ImportOptions? options = null)
    {
        options ??= new ImportOptions();

        try
        {
            // Validate SVG
            var doc = new XmlDocument();
            doc.LoadXml(svgContent);

            var root = doc.DocumentElement;
            if (root?.Name.ToLowerInvariant() != "svg")
                return ImportResult.Failed("Invalid SVG: root element must be <svg>");

            // Process options
            if (!options.PreserveIds)
            {
                RemoveIds(doc);
            }

            return ImportResult.Succeeded(doc.OuterXml, ImportFormat.Svg);
        }
        catch (XmlException ex)
        {
            return ImportResult.Failed($"Invalid SVG XML: {ex.Message}", ImportFormat.Svg);
        }
    }

    /// <summary>
    /// Imports from clipboard data.
    /// </summary>
    public ImportResult ImportFromClipboard(ClipboardData clipboard, ImportOptions? options = null)
    {
        options ??= new ImportOptions();

        if (clipboard.HasSvg && !string.IsNullOrEmpty(clipboard.SvgContent))
        {
            return ImportSvgContent(clipboard.SvgContent, options);
        }

        if (clipboard.HasImage && clipboard.ImageData != null)
        {
            return ImportRasterImageFromBytes(clipboard.ImageData, clipboard.ImageFormat ?? "png", options);
        }

        if (clipboard.HasText && !string.IsNullOrEmpty(clipboard.TextContent))
        {
            // Try to parse as SVG
            if (clipboard.TextContent.Contains("<svg", StringComparison.OrdinalIgnoreCase))
            {
                return ImportSvgContent(clipboard.TextContent, options);
            }
        }

        return ImportResult.Failed("No compatible content in clipboard", ImportFormat.Clipboard);
    }

    /// <summary>
    /// Imports an SVG file.
    /// </summary>
    private ImportResult ImportSvg(string filePath, ImportOptions options)
    {
        try
        {
            var content = File.ReadAllText(filePath);
            var result = ImportSvgContent(content, options);
            if (result.Success)
            {
                return ImportResult.Succeeded(result.SvgContent!, ImportFormat.Svg, filePath);
            }
            return result;
        }
        catch (Exception ex)
        {
            return ImportResult.Failed($"Failed to read SVG: {ex.Message}", ImportFormat.Svg);
        }
    }

    /// <summary>
    /// Imports a raster image as embedded SVG image.
    /// </summary>
    private ImportResult ImportRasterImage(string filePath, ImportFormat format, ImportOptions options)
    {
        try
        {
            var data = File.ReadAllBytes(filePath);
            return ImportRasterImageFromBytes(data, GetMimeType(format), options, filePath);
        }
        catch (Exception ex)
        {
            return ImportResult.Failed($"Failed to read image: {ex.Message}", format);
        }
    }

    /// <summary>
    /// Imports a raster image from bytes.
    /// </summary>
    private ImportResult ImportRasterImageFromBytes(byte[] data, string mimeType, ImportOptions options, string? sourcePath = null)
    {
        try
        {
            var (width, height) = GetImageDimensions(data);

            // Apply max dimensions if specified
            var displayWidth = width;
            var displayHeight = height;

            if (options.MaxWidth.HasValue && displayWidth > options.MaxWidth.Value)
            {
                var scale = options.MaxWidth.Value / displayWidth;
                displayWidth = options.MaxWidth.Value;
                displayHeight *= scale;
            }

            if (options.MaxHeight.HasValue && displayHeight > options.MaxHeight.Value)
            {
                var scale = options.MaxHeight.Value / displayHeight;
                displayHeight = options.MaxHeight.Value;
                displayWidth *= scale;
            }

            var base64 = Convert.ToBase64String(data);
            var dataUri = $"data:image/{mimeType};base64,{base64}";

            var svg = $"""
                <svg xmlns="http://www.w3.org/2000/svg" 
                     xmlns:xlink="http://www.w3.org/1999/xlink"
                     width="{displayWidth}" height="{displayHeight}"
                     viewBox="0 0 {displayWidth} {displayHeight}">
                  <image x="0" y="0" width="{displayWidth}" height="{displayHeight}"
                         xlink:href="{dataUri}"/>
                </svg>
                """;

            var format = mimeType switch
            {
                "png" => ImportFormat.Png,
                "jpg" or "jpeg" => ImportFormat.Jpg,
                "gif" => ImportFormat.Gif,
                "bmp" => ImportFormat.Bmp,
                "webp" => ImportFormat.WebP,
                _ => ImportFormat.Png
            };

            return ImportResult.Succeeded(svg, format, sourcePath);
        }
        catch (Exception ex)
        {
            return ImportResult.Failed($"Failed to process image: {ex.Message}");
        }
    }

    /// <summary>
    /// Imports Adobe Illustrator file (basic support - extracts embedded SVG if present).
    /// </summary>
    private ImportResult ImportAdobeIllustrator(string filePath, ImportOptions options)
    {
        try
        {
            var content = File.ReadAllText(filePath);

            // AI files may contain embedded SVG
            var svgStart = content.IndexOf("<svg", StringComparison.OrdinalIgnoreCase);
            if (svgStart >= 0)
            {
                var svgEnd = content.IndexOf("</svg>", svgStart, StringComparison.OrdinalIgnoreCase);
                if (svgEnd > svgStart)
                {
                    var svgContent = content.Substring(svgStart, svgEnd - svgStart + 6);
                    var result = ImportSvgContent(svgContent, options);
                    if (result.Success)
                    {
                        return new ImportResult
                        {
                            Success = true,
                            SvgContent = result.SvgContent,
                            DetectedFormat = ImportFormat.Ai,
                            SourcePath = filePath,
                            Warnings = ["AI file imported with basic support - some features may not be preserved"]
                        };
                    }
                }
            }

            return ImportResult.Failed("Could not extract SVG content from AI file. Full AI support requires Adobe Illustrator.", ImportFormat.Ai);
        }
        catch (Exception ex)
        {
            return ImportResult.Failed($"Failed to read AI file: {ex.Message}", ImportFormat.Ai);
        }
    }

    /// <summary>
    /// Imports EPS file (basic support).
    /// </summary>
    private ImportResult ImportEps(string filePath, ImportOptions options)
    {
        try
        {
            var content = File.ReadAllText(filePath);

            // Some EPS files contain embedded SVG or can be parsed
            var svgStart = content.IndexOf("<svg", StringComparison.OrdinalIgnoreCase);
            if (svgStart >= 0)
            {
                var svgEnd = content.IndexOf("</svg>", svgStart, StringComparison.OrdinalIgnoreCase);
                if (svgEnd > svgStart)
                {
                    var svgContent = content.Substring(svgStart, svgEnd - svgStart + 6);
                    var result = ImportSvgContent(svgContent, options);
                    if (result.Success)
                    {
                        return new ImportResult
                        {
                            Success = true,
                            SvgContent = result.SvgContent,
                            DetectedFormat = ImportFormat.Eps,
                            SourcePath = filePath,
                            Warnings = ["EPS file imported with basic support - some features may not be preserved"]
                        };
                    }
                }
            }

            return ImportResult.Failed("Could not extract vector content from EPS file. Full EPS support requires additional libraries.", ImportFormat.Eps);
        }
        catch (Exception ex)
        {
            return ImportResult.Failed($"Failed to read EPS file: {ex.Message}", ImportFormat.Eps);
        }
    }

    /// <summary>
    /// Imports PDF file (basic support).
    /// </summary>
    private ImportResult ImportPdf(string filePath, ImportOptions options)
    {
        // PDF vector extraction requires a dedicated library like PdfSharp or iText
        return ImportResult.Failed("PDF import requires additional libraries. Please convert to SVG first.", ImportFormat.Pdf);
    }

    /// <summary>
    /// Gets image dimensions from bytes.
    /// </summary>
    private static (double Width, double Height) GetImageDimensions(byte[] data)
    {
        // PNG
        if (data.Length > 24 && data[0] == 0x89 && data[1] == 0x50)
        {
            var width = (data[16] << 24) | (data[17] << 16) | (data[18] << 8) | data[19];
            var height = (data[20] << 24) | (data[21] << 16) | (data[22] << 8) | data[23];
            return (width, height);
        }

        // JPEG
        if (data.Length > 2 && data[0] == 0xFF && data[1] == 0xD8)
        {
            var i = 2;
            while (i < data.Length - 9)
            {
                if (data[i] != 0xFF) { i++; continue; }
                var marker = data[i + 1];
                if (marker >= 0xC0 && marker <= 0xC3)
                {
                    var height = (data[i + 5] << 8) | data[i + 6];
                    var width = (data[i + 7] << 8) | data[i + 8];
                    return (width, height);
                }
                var length = (data[i + 2] << 8) | data[i + 3];
                i += length + 2;
            }
        }

        // GIF
        if (data.Length > 10 && data[0] == 0x47 && data[1] == 0x49)
        {
            var width = data[6] | (data[7] << 8);
            var height = data[8] | (data[9] << 8);
            return (width, height);
        }

        // BMP
        if (data.Length > 26 && data[0] == 0x42 && data[1] == 0x4D)
        {
            var width = data[18] | (data[19] << 8) | (data[20] << 16) | (data[21] << 24);
            var height = data[22] | (data[23] << 8) | (data[24] << 16) | (data[25] << 24);
            return (width, Math.Abs(height));
        }

        // Default fallback
        return (100, 100);
    }

    /// <summary>
    /// Gets MIME type for format.
    /// </summary>
    private static string GetMimeType(ImportFormat format)
    {
        return format switch
        {
            ImportFormat.Png => "png",
            ImportFormat.Jpg => "jpeg",
            ImportFormat.Gif => "gif",
            ImportFormat.Bmp => "bmp",
            ImportFormat.WebP => "webp",
            _ => "png"
        };
    }

    /// <summary>
    /// Removes all id attributes from an XML document.
    /// </summary>
    private static void RemoveIds(XmlDocument doc)
    {
        var nodes = doc.SelectNodes("//*[@id]");
        if (nodes != null)
        {
            foreach (XmlElement node in nodes)
            {
                node.RemoveAttribute("id");
            }
        }
    }

    /// <summary>
    /// Creates an SVG element for embedding an image.
    /// </summary>
    public static string CreateEmbeddedImageElement(byte[] imageData, string mimeType, double x, double y, double width, double height)
    {
        var base64 = Convert.ToBase64String(imageData);
        return $"""<image x="{x}" y="{y}" width="{width}" height="{height}" xlink:href="data:image/{mimeType};base64,{base64}"/>""";
    }

    /// <summary>
    /// Checks if a format is a raster image format.
    /// </summary>
    public static bool IsRasterFormat(ImportFormat format)
    {
        return format is ImportFormat.Png or ImportFormat.Jpg or ImportFormat.Gif or ImportFormat.Bmp or ImportFormat.WebP;
    }

    /// <summary>
    /// Checks if a format is a vector format.
    /// </summary>
    public static bool IsVectorFormat(ImportFormat format)
    {
        return format is ImportFormat.Svg or ImportFormat.Ai or ImportFormat.Eps or ImportFormat.Pdf;
    }
}
