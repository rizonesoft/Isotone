namespace Gesso.UI.Services;

using Microsoft.Win32;

/// <summary>
/// Windows file dialog service implementation.
/// </summary>
public sealed class FileDialogService : IFileDialogService
{
    public string? ShowOpenFileDialog(string title, string filter, string? initialDirectory = null)
    {
        var dialog = new OpenFileDialog
        {
            Title = title,
            Filter = filter,
            InitialDirectory = initialDirectory ?? Environment.GetFolderPath(Environment.SpecialFolder.MyPictures),
            CheckFileExists = true,
            CheckPathExists = true
        };

        return dialog.ShowDialog() == true ? dialog.FileName : null;
    }

    public string[]? ShowOpenFilesDialog(string title, string filter, string? initialDirectory = null)
    {
        var dialog = new OpenFileDialog
        {
            Title = title,
            Filter = filter,
            InitialDirectory = initialDirectory ?? Environment.GetFolderPath(Environment.SpecialFolder.MyPictures),
            CheckFileExists = true,
            CheckPathExists = true,
            Multiselect = true
        };

        return dialog.ShowDialog() == true ? dialog.FileNames : null;
    }

    public string? ShowSaveFileDialog(string title, string filter, string? defaultFileName = null, string? initialDirectory = null)
    {
        var dialog = new SaveFileDialog
        {
            Title = title,
            Filter = filter,
            FileName = defaultFileName ?? string.Empty,
            InitialDirectory = initialDirectory ?? Environment.GetFolderPath(Environment.SpecialFolder.MyPictures),
            OverwritePrompt = true,
            AddExtension = true
        };

        return dialog.ShowDialog() == true ? dialog.FileName : null;
    }

    public string? ShowFolderDialog(string title, string? initialDirectory = null)
    {
        var dialog = new OpenFolderDialog
        {
            Title = title,
            InitialDirectory = initialDirectory ?? Environment.GetFolderPath(Environment.SpecialFolder.MyPictures)
        };

        return dialog.ShowDialog() == true ? dialog.FolderName : null;
    }
}
