using System.Windows;
using System.Windows.Threading;
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
        
        // Set up global exception handlers
        DispatcherUnhandledException += OnDispatcherUnhandledException;
        AppDomain.CurrentDomain.UnhandledException += OnUnhandledException;
        TaskScheduler.UnobservedTaskException += OnUnobservedTaskException;

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

    private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        e.Handled = true;
        ShowExceptionDialog(e.Exception, "UI Thread Exception");
    }

    private void OnUnhandledException(object sender, UnhandledExceptionEventArgs e)
    {
        if (e.ExceptionObject is Exception ex)
        {
            ShowExceptionDialog(ex, "Unhandled Exception");
        }
    }

    private void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
    {
        e.SetObserved();
        ShowExceptionDialog(e.Exception, "Task Exception");
    }

    private static void ShowExceptionDialog(Exception ex, string title)
    {
        var message = $"""
            {title}

            Type: {ex.GetType().Name}
            Message: {ex.Message}

            Stack Trace:
            {ex.StackTrace}

            Inner Exception:
            {ex.InnerException?.Message ?? "None"}
            """;

        // Log to debug logger if available
        try
        {
            Bezier.Core.Services.DebugLogger.Instance.Error("App", $"{title}: {ex.Message}", ex);
        }
        catch { }

        // Show dialog
        MessageBox.Show(
            message,
            $"Bezier - {title}",
            MessageBoxButton.OK,
            MessageBoxImage.Error);
    }
}
