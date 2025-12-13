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
        LogException(e.Exception, "UI Thread Exception");
        
        // Show exception window and let user decide to continue or exit
        ExceptionWindow.Show(e.Exception, "UI Thread Exception", canContinue: true);
    }

    private void OnUnhandledException(object sender, UnhandledExceptionEventArgs e)
    {
        if (e.ExceptionObject is Exception ex)
        {
            LogException(ex, "Unhandled Exception");
            
            // Cannot continue from AppDomain unhandled exceptions
            ExceptionWindow.Show(ex, "Unhandled Exception (Fatal)", canContinue: false);
        }
    }

    private void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
    {
        e.SetObserved();
        LogException(e.Exception, "Task Exception");
        
        // Show exception window
        ExceptionWindow.Show(e.Exception, "Async Task Exception", canContinue: true);
    }

    private static void LogException(Exception ex, string title)
    {
        try
        {
            Bezier.Core.Services.DebugLogger.Instance.Error("App", $"{title}: {ex.Message}", ex);
        }
        catch { }
    }

    /// <summary>
    /// Shows an exception to the user. Can be called from anywhere in the app for handled exceptions.
    /// </summary>
    public static void ShowException(Exception ex, string title = "Exception")
    {
        LogException(ex, title);
        ExceptionWindow.Show(ex, title, canContinue: true);
    }
}
