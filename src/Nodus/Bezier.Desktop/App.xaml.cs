using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Bezier.Desktop.Views;

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

        // Show splash screen on a separate thread
        SplashWindow.ShowOnSeparateThread();
        SplashWindow.SetStatusText("Initializing services...");

        // Configure services
        var services = new ServiceCollection();
        services.AddBezierServices();
        Services = services.BuildServiceProvider();

        SplashWindow.SetStatusText("Loading editor...");

        // Create and show main window
        var mainWindow = new MainWindowView();
        mainWindow.DataContext = Services.GetRequiredService<ViewModels.MainWindowViewModel>();
        
        // Close splash when main window is ready and bring to front
        mainWindow.Loaded += (_, _) =>
        {
            SplashWindow.CloseAndDispose();
            
            // Bring main window to front
            mainWindow.Activate();
            mainWindow.Topmost = true;
            mainWindow.Topmost = false;
            mainWindow.Focus();
        };
        
        mainWindow.Show();
    }
}
