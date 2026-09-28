namespace Gesso.UI.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;

public partial class WelcomeViewModel : ObservableObject
{
    [ObservableProperty]
    private string _welcomeMessage = "Welcome to Gesso";

    [ObservableProperty]
    private string _version = "0.1.0";
}
