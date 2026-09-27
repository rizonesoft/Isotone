namespace Pinxit.UI.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;

public partial class WelcomeViewModel : ObservableObject
{
    [ObservableProperty]
    private string _welcomeMessage = "Welcome to Pinxit";

    [ObservableProperty]
    private string _version = "0.1.0";
}
