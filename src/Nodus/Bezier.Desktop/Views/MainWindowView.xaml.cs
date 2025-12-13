using Bezier.Desktop.ViewModels;
using SkiaSharp;
using Wpf.Ui.Controls;

namespace Bezier.Desktop.Views;

/// <summary>
/// Main application window with Mica backdrop and docking layout.
/// </summary>
public partial class MainWindowView : FluentWindow
{
    public MainWindowView()
    {
        InitializeComponent();
        Loaded += OnLoaded;
    }

    private void OnLoaded(object sender, System.Windows.RoutedEventArgs e)
    {
        // Create a new blank document on startup
        if (DataContext is MainWindowViewModel viewModel && viewModel.Document is null)
        {
            viewModel.NewCommand.Execute(null);
        }
    }

    private void MainCanvas_CursorPositionChanged(object? sender, SKPoint e)
    {
        if (DataContext is MainWindowViewModel viewModel)
        {
            viewModel.UpdateCursorPosition(e.X, e.Y);
        }
    }

    private void MainCanvas_ZoomChanged(object? sender, double e)
    {
        if (DataContext is MainWindowViewModel viewModel)
        {
            viewModel.ZoomLevel = (int)Math.Round(e * 100);
        }
    }
}
