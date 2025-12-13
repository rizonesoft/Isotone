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
    private readonly SvgParser _svgParser = new();

    #region Window Properties
    
    [ObservableProperty]
    private string _title = "Bezier";
    
    [ObservableProperty]
    private string _statusText = "Ready";
    
    [ObservableProperty]
    private int _zoomLevel = 100;
    
    [ObservableProperty]
    private string _documentSize = "800 x 600";

    [ObservableProperty]
    private VectorDocument? _document;

    [ObservableProperty]
    private string? _currentFilePath;
    
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
                Document = _svgParser.ParseFile(dialog.FileName);
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
            DocumentSize = $"{Document.Width:0} x {Document.Height:0}";
            Title = string.IsNullOrEmpty(CurrentFilePath) 
                ? "Bezier - Untitled" 
                : $"Bezier - {System.IO.Path.GetFileName(CurrentFilePath)}";
        }
    }
    
    [RelayCommand]
    private void Save()
    {
        StatusText = "Document saved";
    }
    
    [RelayCommand]
    private void SaveAs()
    {
        StatusText = "Save document as...";
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
        if (ZoomLevel < 800)
        {
            ZoomLevel = Math.Min(800, ZoomLevel + 25);
            StatusText = $"Zoom: {ZoomLevel}%";
        }
    }
    
    [RelayCommand]
    private void ZoomOut()
    {
        if (ZoomLevel > 10)
        {
            ZoomLevel = Math.Max(10, ZoomLevel - 25);
            StatusText = $"Zoom: {ZoomLevel}%";
        }
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
