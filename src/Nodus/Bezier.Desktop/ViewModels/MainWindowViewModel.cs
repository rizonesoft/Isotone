using System.Windows;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Win32;
using Bezier.Core.Models;
using Bezier.Core.Services;

namespace Bezier.Desktop.ViewModels;

/// <summary>
/// ViewModel for the main Bezier editor window.
/// Contains all menu commands and view state properties.
/// </summary>
public partial class MainWindowViewModel : ObservableObject
{
    private readonly SvgImporter _svgImporter = new();
    private readonly SvgExporter _svgExporter = new();

    #region Window Properties
    
    [ObservableProperty]
    private string _title = "Bezier";
    
    [ObservableProperty]
    private string _statusText = "Ready";
    
    [ObservableProperty]
    private int _zoomLevel = 100;
    
    [ObservableProperty]
    private string _documentSize = "800 × 600";

    [ObservableProperty]
    private VectorDocument? _document;

    [ObservableProperty]
    private string? _currentFilePath;

    #endregion

    #region Status Bar Properties

    [ObservableProperty]
    private double _cursorX;

    [ObservableProperty]
    private double _cursorY;

    [ObservableProperty]
    private string _cursorPosition = "0, 0";

    [ObservableProperty]
    private int _elementCount;

    [ObservableProperty]
    private int _selectedCount;

    [ObservableProperty]
    private string _selectionInfo = "No selection";

    [ObservableProperty]
    private bool _isLoading;

    [ObservableProperty]
    private double _loadingProgress;

    [ObservableProperty]
    private string? _errorMessage;

    [ObservableProperty]
    private bool _showError;

    /// <summary>
    /// Available zoom levels for the dropdown.
    /// </summary>
    public int[] ZoomLevels { get; } = [25, 50, 75, 100, 125, 150, 200, 300, 400, 600, 800];

    /// <summary>
    /// Updates cursor position display.
    /// </summary>
    public void UpdateCursorPosition(double x, double y)
    {
        CursorX = Math.Round(x, 1);
        CursorY = Math.Round(y, 1);
        CursorPosition = $"{CursorX:0.#}, {CursorY:0.#}";
    }

    /// <summary>
    /// Updates selection information display.
    /// </summary>
    public void UpdateSelectionInfo(int count, double? width = null, double? height = null)
    {
        SelectedCount = count;
        if (count == 0)
        {
            SelectionInfo = "No selection";
        }
        else if (count == 1 && width.HasValue && height.HasValue)
        {
            SelectionInfo = $"1 object ({width:0.#} × {height:0.#})";
        }
        else
        {
            SelectionInfo = $"{count} objects";
        }
    }

    /// <summary>
    /// Shows an error toast message.
    /// </summary>
    public void ShowErrorToast(string message)
    {
        ErrorMessage = message;
        ShowError = true;
        
        // Auto-dismiss after 5 seconds
        Task.Delay(5000).ContinueWith(_ => 
        {
            Application.Current.Dispatcher.Invoke(() => ShowError = false);
        });
    }

    /// <summary>
    /// Dismisses the error toast.
    /// </summary>
    [RelayCommand]
    private void DismissError()
    {
        ShowError = false;
    }

    #endregion
    
    #region View State Properties
    
    [ObservableProperty]
    private bool _showGrid = true;
    
    [ObservableProperty]
    private bool _showRulers = true;
    
    [ObservableProperty]
    private bool _showGuides = true;
    
    [ObservableProperty]
    private bool _outlineMode = false;
    
    [ObservableProperty]
    private bool _showToolsPanel = true;
    
    [ObservableProperty]
    private bool _showPropertiesPanel = true;
    
    [ObservableProperty]
    private bool _showLayersPanel = true;
    
    [ObservableProperty]
    private bool _showCodePanel = false;
    
    [ObservableProperty]
    private bool _snapEnabled = true;
    
    #endregion
    
    #region File Commands
    
    [RelayCommand]
    private void New()
    {
        Document = new VectorDocument();
        CurrentFilePath = null;
        UpdateDocumentInfo();
        StatusText = "New document created";
    }
    
    [RelayCommand]
    private void Open()
    {
        var dialog = new OpenFileDialog
        {
            Title = "Open SVG File",
            Filter = "SVG Files (*.svg)|*.svg|All Files (*.*)|*.*",
            DefaultExt = ".svg"
        };

        if (dialog.ShowDialog() == true)
        {
            try
            {
                Document = _svgImporter.ParseFile(dialog.FileName);
                CurrentFilePath = dialog.FileName;
                UpdateDocumentInfo();
                StatusText = $"Opened: {System.IO.Path.GetFileName(dialog.FileName)} ({Document.Elements.Count} elements)";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error opening file: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusText = "Error opening file";
            }
        }
    }

    private void UpdateDocumentInfo()
    {
        if (Document is not null)
        {
            DocumentSize = $"{Document.Width:0} × {Document.Height:0}";
            ElementCount = Document.Elements.Count;
            Title = string.IsNullOrEmpty(CurrentFilePath) 
                ? "Bezier - Untitled" 
                : $"Bezier - {System.IO.Path.GetFileName(CurrentFilePath)}";
        }
        else
        {
            DocumentSize = "—";
            ElementCount = 0;
        }
    }
    
    [RelayCommand]
    private void Save()
    {
        if (Document is null) return;

        if (string.IsNullOrEmpty(CurrentFilePath))
        {
            SaveAs();
            return;
        }

        try
        {
            _svgExporter.ExportToFile(Document, CurrentFilePath);
            Document.IsDirty = false;
            StatusText = $"Saved: {System.IO.Path.GetFileName(CurrentFilePath)}";
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Error saving file: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            StatusText = "Error saving file";
        }
    }
    
    [RelayCommand]
    private void SaveAs()
    {
        if (Document is null) return;

        var dialog = new SaveFileDialog
        {
            Title = "Save SVG File",
            Filter = "SVG Files (*.svg)|*.svg|All Files (*.*)|*.*",
            DefaultExt = ".svg",
            FileName = string.IsNullOrEmpty(CurrentFilePath) 
                ? "untitled.svg" 
                : System.IO.Path.GetFileName(CurrentFilePath)
        };

        if (dialog.ShowDialog() == true)
        {
            try
            {
                _svgExporter.ExportToFile(Document, dialog.FileName);
                CurrentFilePath = dialog.FileName;
                Document.IsDirty = false;
                UpdateDocumentInfo();
                StatusText = $"Saved: {System.IO.Path.GetFileName(dialog.FileName)}";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error saving file: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusText = "Error saving file";
            }
        }
    }
    
    [RelayCommand]
    private void ExportPng()
    {
        StatusText = "Export as PNG...";
    }
    
    [RelayCommand]
    private void ExportJpeg()
    {
        StatusText = "Export as JPEG...";
    }
    
    [RelayCommand]
    private void ExportPdf()
    {
        StatusText = "Export as PDF...";
    }
    
    [RelayCommand]
    private void ExportXaml()
    {
        StatusText = "Export as XAML...";
    }
    
    [RelayCommand]
    private void Close()
    {
        StatusText = "Document closed";
    }
    
    [RelayCommand]
    private void Exit()
    {
        Application.Current.Shutdown();
    }
    
    #endregion
    
    #region Edit Commands
    
    [RelayCommand]
    private void Undo()
    {
        StatusText = "Undo";
    }
    
    [RelayCommand]
    private void Redo()
    {
        StatusText = "Redo";
    }
    
    [RelayCommand]
    private void Cut()
    {
        StatusText = "Cut";
    }
    
    [RelayCommand]
    private void Copy()
    {
        StatusText = "Copy";
    }
    
    [RelayCommand]
    private void Paste()
    {
        StatusText = "Paste";
    }
    
    [RelayCommand]
    private void Duplicate()
    {
        StatusText = "Duplicate";
    }
    
    [RelayCommand]
    private void Delete()
    {
        StatusText = "Delete";
    }
    
    [RelayCommand]
    private void SelectAll()
    {
        StatusText = "Select All";
    }
    
    [RelayCommand]
    private void Preferences()
    {
        StatusText = "Opening preferences...";
    }
    
    #endregion
    
    #region View Commands
    
    [RelayCommand]
    private void ZoomIn()
    {
        // Find next zoom level
        var nextZoom = ZoomLevels.FirstOrDefault(z => z > ZoomLevel);
        if (nextZoom > 0)
        {
            ZoomLevel = nextZoom;
            StatusText = $"Zoom: {ZoomLevel}%";
        }
    }
    
    [RelayCommand]
    private void ZoomOut()
    {
        // Find previous zoom level
        var prevZoom = ZoomLevels.LastOrDefault(z => z < ZoomLevel);
        if (prevZoom > 0)
        {
            ZoomLevel = prevZoom;
            StatusText = $"Zoom: {ZoomLevel}%";
        }
    }

    [RelayCommand]
    private void SetZoom(int zoom)
    {
        ZoomLevel = Math.Clamp(zoom, 10, 800);
        StatusText = $"Zoom: {ZoomLevel}%";
    }
    
    [RelayCommand]
    private void FitToWindow()
    {
        ZoomLevel = 100;
        StatusText = "Fit to window";
    }
    
    [RelayCommand]
    private void ActualSize()
    {
        ZoomLevel = 100;
        StatusText = "Actual size (100%)";
    }
    
    #endregion
    
    #region Object Commands
    
    [RelayCommand]
    private void Group()
    {
        StatusText = "Group objects";
    }
    
    [RelayCommand]
    private void Ungroup()
    {
        StatusText = "Ungroup objects";
    }
    
    [RelayCommand]
    private void BringToFront()
    {
        StatusText = "Bring to front";
    }
    
    [RelayCommand]
    private void BringForward()
    {
        StatusText = "Bring forward";
    }
    
    [RelayCommand]
    private void SendBackward()
    {
        StatusText = "Send backward";
    }
    
    [RelayCommand]
    private void SendToBack()
    {
        StatusText = "Send to back";
    }
    
    [RelayCommand]
    private void AlignLeft()
    {
        StatusText = "Align left";
    }
    
    [RelayCommand]
    private void AlignCenter()
    {
        StatusText = "Align center";
    }
    
    [RelayCommand]
    private void AlignRight()
    {
        StatusText = "Align right";
    }
    
    [RelayCommand]
    private void AlignTop()
    {
        StatusText = "Align top";
    }
    
    [RelayCommand]
    private void AlignMiddle()
    {
        StatusText = "Align middle";
    }
    
    [RelayCommand]
    private void AlignBottom()
    {
        StatusText = "Align bottom";
    }
    
    [RelayCommand]
    private void DistributeHorizontally()
    {
        StatusText = "Distribute horizontally";
    }
    
    [RelayCommand]
    private void DistributeVertically()
    {
        StatusText = "Distribute vertically";
    }
    
    [RelayCommand]
    private void Rotate90Cw()
    {
        StatusText = "Rotate 90° clockwise";
    }
    
    [RelayCommand]
    private void Rotate90Ccw()
    {
        StatusText = "Rotate 90° counter-clockwise";
    }
    
    [RelayCommand]
    private void Rotate180()
    {
        StatusText = "Rotate 180°";
    }
    
    [RelayCommand]
    private void FlipHorizontal()
    {
        StatusText = "Flip horizontal";
    }
    
    [RelayCommand]
    private void FlipVertical()
    {
        StatusText = "Flip vertical";
    }
    
    #endregion
    
    #region Path Commands
    
    [RelayCommand]
    private void Union()
    {
        StatusText = "Union paths";
    }
    
    [RelayCommand]
    private void Subtract()
    {
        StatusText = "Subtract paths";
    }
    
    [RelayCommand]
    private void Intersect()
    {
        StatusText = "Intersect paths";
    }
    
    [RelayCommand]
    private void Exclude()
    {
        StatusText = "Exclude paths";
    }
    
    [RelayCommand]
    private void Simplify()
    {
        StatusText = "Simplify path";
    }
    
    [RelayCommand]
    private void StrokeToPath()
    {
        StatusText = "Convert stroke to path";
    }
    
    [RelayCommand]
    private void TextToPath()
    {
        StatusText = "Convert text to path";
    }
    
    #endregion
    
    #region Help Commands
    
    [RelayCommand]
    private void Documentation()
    {
        StatusText = "Opening documentation...";
        // TODO: Open docs URL in browser
    }
    
    [RelayCommand]
    private void KeyboardShortcuts()
    {
        StatusText = "Keyboard shortcuts";
        // TODO: Show keyboard shortcuts dialog
    }
    
    [RelayCommand]
    private void CheckUpdates()
    {
        StatusText = "Checking for updates...";
    }
    
    [RelayCommand]
    private void About()
    {
        StatusText = "About Bezier";
        // TODO: Show about dialog
    }
    
    #endregion
}
