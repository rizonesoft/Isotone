namespace Imago.UI.Services;

/// <summary>
/// Service for file open/save dialogs.
/// </summary>
public interface IFileDialogService
{
    /// <summary>
    /// Shows an open file dialog.
    /// </summary>
    string? ShowOpenFileDialog(string title, string filter, string? initialDirectory = null);

    /// <summary>
    /// Shows an open file dialog for multiple files.
    /// </summary>
    string[]? ShowOpenFilesDialog(string title, string filter, string? initialDirectory = null);

    /// <summary>
    /// Shows a save file dialog.
    /// </summary>
    string? ShowSaveFileDialog(string title, string filter, string? defaultFileName = null, string? initialDirectory = null);

    /// <summary>
    /// Shows a folder browser dialog.
    /// </summary>
    string? ShowFolderDialog(string title, string? initialDirectory = null);
}

/// <summary>
/// Common file filter definitions.
/// </summary>
public static class FileFilters
{
    public const string AllImages = "Image Files|*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.tif;*.webp|All Files|*.*";
    public const string PngFiles = "PNG Files|*.png|All Files|*.*";
    public const string JpegFiles = "JPEG Files|*.jpg;*.jpeg|All Files|*.*";
    public const string ImagoFiles = "Imago Files|*.imago|All Files|*.*";
    public const string AllFiles = "All Files|*.*";

    public const string ExportFormats = "PNG|*.png|JPEG|*.jpg|BMP|*.bmp|TIFF|*.tiff|WebP|*.webp";
}
