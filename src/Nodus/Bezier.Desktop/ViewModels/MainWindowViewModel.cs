using CommunityToolkit.Mvvm.ComponentModel;

namespace Bezier.Desktop.ViewModels;

/// <summary>
/// ViewModel for the main Bezier editor window.
/// </summary>
public partial class MainWindowViewModel : ObservableObject
{
    [ObservableProperty]
    private string _title = "Bezier";
    
    [ObservableProperty]
    private string _statusText = "Ready";
    
    [ObservableProperty]
    private int _zoomLevel = 100;
    
    [ObservableProperty]
    private string _documentSize = "0 x 0";
    
    public MainWindowViewModel()
    {
    }
}
