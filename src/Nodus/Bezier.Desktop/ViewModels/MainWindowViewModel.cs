using CommunityToolkit.Mvvm.ComponentModel;

namespace Bezier.Desktop.ViewModels;

/// <summary>
/// Main window view model.
/// </summary>
public partial class MainWindowViewModel : ObservableObject
{
    [ObservableProperty]
    private string _title = "Bezier SVG Editor";

    [ObservableProperty]
    private string _statusText = "Ready";

    [ObservableProperty]
    private double _zoomLevel = 100.0;
}
