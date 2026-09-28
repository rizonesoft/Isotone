namespace Gesso.UI.Services;

using Serilog;

public sealed class DocumentService : IDocumentService
{
    private readonly ILogger _logger = Log.ForContext<DocumentService>();

    public bool HasUnsavedChanges { get; private set; }

    public async Task<bool> NewDocumentAsync(int width, int height)
    {
        _logger.Information("Creating new document: {Width}x{Height}", width, height);
        await Task.Delay(10);
        HasUnsavedChanges = false;
        return true;
    }

    public async Task<bool> OpenDocumentAsync(string path)
    {
        _logger.Information("Opening document: {Path}", path);
        await Task.Delay(10);
        HasUnsavedChanges = false;
        return true;
    }

    public async Task<bool> SaveDocumentAsync(string path)
    {
        _logger.Information("Saving document: {Path}", path);
        await Task.Delay(10);
        HasUnsavedChanges = false;
        return true;
    }

    public async Task<bool> ExportAsync(string path, string format)
    {
        _logger.Information("Exporting document: {Path} as {Format}", path, format);
        await Task.Delay(10);
        return true;
    }

    public void CloseDocument()
    {
        _logger.Information("Closing document");
        HasUnsavedChanges = false;
    }
}
