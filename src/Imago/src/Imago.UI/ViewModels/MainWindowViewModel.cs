namespace Imago.UI.ViewModels;

using System.Diagnostics;
using System.Windows;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Imago.UI.Services;

public partial class MainWindowViewModel : ObservableObject
{
    private readonly IDocumentService _documentService;
    private readonly ILogger _logger = Log.ForContext<MainWindowViewModel>();
    private readonly Stopwatch _memoryUpdateTimer = Stopwatch.StartNew();

    public event EventHandler<string>? ImageLoadRequested;

    [ObservableProperty]
    private string _documentTitle = "Untitled";

    [ObservableProperty]
    private bool _isDocumentDirty;

    [ObservableProperty]
    private bool _hasDocument;

    [ObservableProperty]
    private string _statusMessage = "Ready";

    [ObservableProperty]
    private string _cursorPosition = "X: 0, Y: 0";

    [ObservableProperty]
    private string _documentSize = "No document";

    [ObservableProperty]
    private long _memoryUsage;

    [ObservableProperty]
    private double _zoomLevel = 1.0;

    [ObservableProperty]
    private bool _showRulers = true;

    [ObservableProperty]
    private bool _showGrid;

    [ObservableProperty]
    private bool _showGuides = true;

    [ObservableProperty]
    private bool _showLayersPanel = true;

    [ObservableProperty]
    private bool _showPropertiesPanel = true;

    [ObservableProperty]
    private bool _showHistoryPanel;

    [ObservableProperty]
    private bool _showNavigatorPanel;

    [ObservableProperty]
    private bool _showColorPanel = true;

    public MainWindowViewModel(IDocumentService documentService)
    {
        _documentService = documentService;
        UpdateMemoryUsage();
        _logger.Information("MainWindowViewModel initialized");
    }

    private void UpdateMemoryUsage()
    {
        if (_memoryUpdateTimer.ElapsedMilliseconds > 1000)
        {
            MemoryUsage = GC.GetTotalMemory(false) / (1024 * 1024);
            _memoryUpdateTimer.Restart();
        }
    }

    public void UpdateCursorPosition(int x, int y)
    {
        CursorPosition = $"X: {x}, Y: {y}";
    }

    [RelayCommand]
    private void NewDocument()
    {
        _logger.Information("Creating new document");
        StatusMessage = "Creating new document...";
        HasDocument = true;
        DocumentTitle = "Untitled-1";
        DocumentSize = "1920 x 1080 px";
        StatusMessage = "New document created";
    }

    [RelayCommand]
    private async Task OpenDocumentAsync()
    {
        _logger.Information("Opening document dialog");

        var dialog = new Microsoft.Win32.OpenFileDialog
        {
            Title = "Open Image",
            Filter = "Image Files|*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.tif;*.webp|All Files|*.*",
            InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyPictures)
        };

        if (dialog.ShowDialog() == true)
        {
            StatusMessage = "Loading image...";
            var filePath = dialog.FileName;

            try
            {
                await Task.Run(() =>
                {
                    // Validate file exists
                    if (!System.IO.File.Exists(filePath))
                        throw new System.IO.FileNotFoundException("File not found", filePath);
                });

                DocumentTitle = System.IO.Path.GetFileName(filePath);
                HasDocument = true;

                // Get image dimensions
                using var stream = System.IO.File.OpenRead(filePath);
                using var bitmap = SkiaSharp.SKBitmap.Decode(stream);
                if (bitmap != null)
                {
                    DocumentSize = $"{bitmap.Width} x {bitmap.Height} px";
                }

                ImageLoadRequested?.Invoke(this, filePath);
                StatusMessage = $"Loaded: {DocumentTitle}";
                _logger.Information("Opened document: {FilePath}", filePath);
            }
            catch (Exception ex)
            {
                _logger.Error(ex, "Failed to open document: {FilePath}", filePath);
                StatusMessage = $"Error: {ex.Message}";
                HasDocument = false;
            }
        }
        else
        {
            StatusMessage = "Ready";
        }
    }

    [RelayCommand]
    private void SaveDocument()
    {
        if (!HasDocument)
        {
            return;
        }

        _logger.Information("Saving document: {DocumentTitle}", DocumentTitle);
        StatusMessage = "Saving...";
        IsDocumentDirty = false;
        StatusMessage = "Document saved";
    }

    [RelayCommand]
    private void SaveAs()
    {
        if (!HasDocument)
        {
            return;
        }

        _logger.Information("Save As dialog for: {DocumentTitle}", DocumentTitle);
    }

    [RelayCommand]
    private void Export()
    {
        if (!HasDocument)
        {
            return;
        }

        _logger.Information("Export dialog for: {DocumentTitle}", DocumentTitle);
    }

    [RelayCommand]
    private void Exit()
    {
        _logger.Information("Exiting application");
        Application.Current.Shutdown();
    }

    [RelayCommand]
    private void Undo()
    {
        _logger.Debug("Undo requested");
        StatusMessage = "Undo";
    }

    [RelayCommand]
    private void Redo()
    {
        _logger.Debug("Redo requested");
        StatusMessage = "Redo";
    }

    [RelayCommand]
    private void Cut()
    {
        _logger.Debug("Cut requested");
    }

    [RelayCommand]
    private void Copy()
    {
        _logger.Debug("Copy requested");
    }

    [RelayCommand]
    private void Paste()
    {
        _logger.Debug("Paste requested");
    }

    [RelayCommand]
    private void Preferences()
    {
        _logger.Information("Opening preferences dialog");
    }

    [RelayCommand]
    private void ImageSize()
    {
        _logger.Information("Opening image size dialog");
    }

    [RelayCommand]
    private void CanvasSize()
    {
        _logger.Information("Opening canvas size dialog");
    }

    [RelayCommand]
    private void RotateClockwise()
    {
        _logger.Debug("Rotate clockwise requested");
    }

    [RelayCommand]
    private void RotateCounterClockwise()
    {
        _logger.Debug("Rotate counter-clockwise requested");
    }

    [RelayCommand]
    private void Rotate180()
    {
        _logger.Debug("Rotate 180 requested");
    }

    [RelayCommand]
    private void FlipHorizontal()
    {
        _logger.Debug("Flip horizontal requested");
    }

    [RelayCommand]
    private void FlipVertical()
    {
        _logger.Debug("Flip vertical requested");
    }

    [RelayCommand]
    private void NewLayer()
    {
        _logger.Information("Creating new layer");
        StatusMessage = "New layer created";
    }

    [RelayCommand]
    private void DuplicateLayer()
    {
        _logger.Debug("Duplicate layer requested");
    }

    [RelayCommand]
    private void DeleteLayer()
    {
        _logger.Debug("Delete layer requested");
    }

    [RelayCommand]
    private void MergeDown()
    {
        _logger.Debug("Merge down requested");
    }

    [RelayCommand]
    private void FlattenImage()
    {
        _logger.Debug("Flatten image requested");
    }

    [RelayCommand]
    private void GaussianBlur()
    {
        _logger.Information("Opening Gaussian Blur dialog");
    }

    [RelayCommand]
    private void MotionBlur()
    {
        _logger.Information("Opening Motion Blur dialog");
    }

    [RelayCommand]
    private void SurfaceBlur()
    {
        _logger.Information("Opening Surface Blur dialog");
    }

    [RelayCommand]
    private void UnsharpMask()
    {
        _logger.Information("Opening Unsharp Mask dialog");
    }

    [RelayCommand]
    private void SmartSharpen()
    {
        _logger.Information("Opening Smart Sharpen dialog");
    }

    [RelayCommand]
    private void AddNoise()
    {
        _logger.Information("Opening Add Noise dialog");
    }

    [RelayCommand]
    private void ReduceNoise()
    {
        _logger.Information("Opening Reduce Noise dialog");
    }

    [RelayCommand]
    private void ZoomIn()
    {
        ZoomLevel = Math.Min(ZoomLevel * 1.25, 32.0);
        _logger.Debug("Zoom in: {ZoomLevel:P0}", ZoomLevel);
    }

    [RelayCommand]
    private void ZoomOut()
    {
        ZoomLevel = Math.Max(ZoomLevel / 1.25, 0.01);
        _logger.Debug("Zoom out: {ZoomLevel:P0}", ZoomLevel);
    }

    [RelayCommand]
    private void FitToWindow()
    {
        ZoomLevel = 1.0;
        _logger.Debug("Fit to window");
    }

    [RelayCommand]
    private void ActualSize()
    {
        ZoomLevel = 1.0;
        _logger.Debug("Actual size (100%)");
    }

    [RelayCommand]
    private void ResetWorkspace()
    {
        ShowLayersPanel = true;
        ShowPropertiesPanel = true;
        ShowHistoryPanel = false;
        ShowNavigatorPanel = false;
        ShowColorPanel = true;
        _logger.Information("Workspace reset to default");
    }

    [RelayCommand]
    private void Documentation()
    {
        _logger.Information("Opening documentation");
        Process.Start(new ProcessStartInfo
        {
            FileName = "https://github.com/yourusername/Imago/wiki",
            UseShellExecute = true
        });
    }

    [RelayCommand]
    private void KeyboardShortcuts()
    {
        _logger.Information("Opening keyboard shortcuts dialog");
    }

    [RelayCommand]
    private void About()
    {
        _logger.Information("Opening about dialog");
    }
}
