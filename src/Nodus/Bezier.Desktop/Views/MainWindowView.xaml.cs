using System.Windows;
using Bezier.Core.Services;
using Bezier.Desktop.ViewModels;
using SkiaSharp;
using Wpf.Ui.Controls;

namespace Bezier.Desktop.Views;

/// <summary>
/// Main application window with Mica backdrop and docking layout.
/// </summary>
public partial class MainWindowView : FluentWindow
{
    private SKPoint _lastScreenPosition;
    
    public MainWindowView()
    {
        InitializeComponent();
        Loaded += OnLoaded;
        SizeChanged += OnSizeChanged;
        Closed += OnClosed;
    }
    
    private void OnClosed(object? sender, EventArgs e)
    {
        // Explicitly shutdown the application when the main window closes.
        // This ensures all windows (including hidden ones like DebugWindow) are closed.
        Application.Current.Shutdown();
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        // Create a new blank document on startup
        if (DataContext is MainWindowViewModel viewModel && viewModel.Document is null)
        {
            viewModel.NewCommand.Execute(null);
        }
        
        // Update initial viewport size
        UpdateCanvasState();
    }
    
    private void OnSizeChanged(object sender, SizeChangedEventArgs e)
    {
        UpdateCanvasState();
    }

    private void MainCanvas_CursorPositionChanged(object? sender, SKPoint e)
    {
        if (DataContext is MainWindowViewModel viewModel)
        {
            viewModel.UpdateCursorPosition(e.X, e.Y);
            
            // Publish to DebugInfoService
            DebugInfoService.Instance.UpdateMousePosition(
                screenX: _lastScreenPosition.X,
                screenY: _lastScreenPosition.Y,
                documentX: e.X,
                documentY: e.Y
            );
        }
    }

    private void MainCanvas_ZoomChanged(object? sender, double e)
    {
        if (DataContext is MainWindowViewModel viewModel)
        {
            viewModel.ZoomLevel = (int)Math.Round(e * 100);
            UpdateCanvasState();
        }
    }
    
    private void UpdateCanvasState()
    {
        // Get canvas dimensions and state from the MainCanvas if available
        // For now, use window dimensions as an approximation
        var viewportWidth = ActualWidth > 0 ? ActualWidth : 800;
        var viewportHeight = ActualHeight > 0 ? ActualHeight : 600;
        
        if (DataContext is MainWindowViewModel viewModel)
        {
            var zoom = viewModel.ZoomLevel / 100.0;
            
            DebugInfoService.Instance.UpdateCanvasState(
                zoom: zoom,
                panX: 0,  // Will be updated from canvas if needed
                panY: 0,
                viewportWidth: viewportWidth,
                viewportHeight: viewportHeight
            );
        }
    }
    
    protected override void OnPreviewMouseMove(System.Windows.Input.MouseEventArgs e)
    {
        base.OnPreviewMouseMove(e);
        var pos = e.GetPosition(this);
        _lastScreenPosition = new SKPoint((float)pos.X, (float)pos.Y);
    }
}
