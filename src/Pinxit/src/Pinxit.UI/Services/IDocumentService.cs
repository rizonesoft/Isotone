namespace Pinxit.UI.Services;

public interface IDocumentService
{
    Task<bool> NewDocumentAsync(int width, int height);
    Task<bool> OpenDocumentAsync(string path);
    Task<bool> SaveDocumentAsync(string path);
    Task<bool> ExportAsync(string path, string format);
    void CloseDocument();
    bool HasUnsavedChanges { get; }
}
