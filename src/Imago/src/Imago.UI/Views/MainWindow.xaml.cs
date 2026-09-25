namespace Imago.UI.Views;

using System.Windows;
using Imago.UI.Controls;
using Imago.UI.ViewModels;

public partial class MainWindow : Window
{
    private readonly MainWindowViewModel _viewModel;

    public MainWindow(MainWindowViewModel viewModel)
    {
        _viewModel = viewModel;
        DataContext = _viewModel;

        InitializeComponent();

        // Wire up canvas events
        _viewModel.ImageLoadRequested += OnImageLoadRequested;
        CanvasContainer.CanvasMouseMove += OnCanvasMouseMove;
        CanvasContainer.ImageCanvas.ViewportChanged += OnViewportChanged;
    }

    private void OnImageLoadRequested(object? sender, string filePath)
    {
        CanvasContainer.LoadImage(filePath);
        CanvasContainer.ZoomToFit();
    }

    private void OnCanvasMouseMove(object? sender, CanvasMouseEventArgs e)
    {
        _viewModel.UpdateCursorPosition((int)e.DocumentX, (int)e.DocumentY);
    }

    private void OnViewportChanged(object? sender, EventArgs e)
    {
        _viewModel.ZoomLevel = CanvasContainer.ImageCanvas.Zoom;
    }
}
