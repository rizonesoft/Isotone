using System.Windows;
using Microsoft.Extensions.DependencyInjection;

namespace Bezier.Desktop;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    /// <summary>
    /// Gets the service provider for dependency injection.
    /// </summary>
    public static IServiceProvider Services { get; private set; } = null!;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // Configure services
        var services = new ServiceCollection();
        services.AddBezierServices();
        Services = services.BuildServiceProvider();

        // Create and show main window
        var mainWindow = new Views.MainWindowView();
        mainWindow.DataContext = Services.GetRequiredService<ViewModels.MainWindowViewModel>();
        mainWindow.Show();
    }
}
