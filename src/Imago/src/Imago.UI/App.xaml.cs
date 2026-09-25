namespace Imago.UI;

using System.IO;
using System.Windows;
using System.Windows.Threading;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Serilog;
using Serilog.Events;
using Imago.UI.Services;
using Imago.UI.ViewModels;
using Imago.UI.Views;

public partial class App : Application
{
    private static readonly IHost s_host = CreateHostBuilder().Build();

    public static IServiceProvider Services => s_host.Services;

    public static T GetService<T>() where T : class =>
        Services.GetRequiredService<T>();

    private static IHostBuilder CreateHostBuilder() =>
        Host.CreateDefaultBuilder()
            .UseSerilog((context, services, configuration) =>
            {
                var logsPath = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "Imago",
                    "logs");

                Directory.CreateDirectory(logsPath);

                configuration
                    .MinimumLevel.Information()
                    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
                    .MinimumLevel.Override("System", LogEventLevel.Warning)
                    .Enrich.FromLogContext()
                    .WriteTo.Debug(
                        outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}",
                        formatProvider: System.Globalization.CultureInfo.InvariantCulture)
                    .WriteTo.File(
                        path: Path.Combine(logsPath, "imago-.log"),
                        rollingInterval: RollingInterval.Day,
                        retainedFileCountLimit: 7,
                        fileSizeLimitBytes: 10 * 1024 * 1024,
                        formatProvider: System.Globalization.CultureInfo.InvariantCulture,
                        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] [{ThreadId}] {SourceContext} - {Message:lj}{NewLine}{Exception}");
            })
            .ConfigureServices((context, services) =>
            {
                // Application Services
                services.AddSingleton<Services.INavigationService, Services.NavigationService>();
                services.AddSingleton<IDocumentService, DocumentService>();
                services.AddSingleton<ISettingsService, SettingsService>();

                // ViewModels
                services.AddSingleton<MainWindowViewModel>();
                services.AddTransient<WelcomeViewModel>();

                // Views
                services.AddSingleton<MainWindow>();
            });

    protected override async void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // Single instance check
        if (!SingleInstanceManager.Initialize())
        {
            SingleInstanceManager.NotifyExistingInstance(e.Args);
            Shutdown();
            return;
        }

        // Set up global exception handlers
        DispatcherUnhandledException += OnDispatcherUnhandledException;
        AppDomain.CurrentDomain.UnhandledException += OnUnhandledException;
        TaskScheduler.UnobservedTaskException += OnUnobservedTaskException;

        // Show splash screen on separate thread
        SplashWindow.ShowOnSeparateThread();

        Log.Information("Imago starting up...");
        Log.Information("Version: {Version}", GetType().Assembly.GetName().Version);
        Log.Information("Runtime: {Runtime}", Environment.Version);

        try
        {
            SplashWindow.SetStatus("Initializing services...");
            await s_host.StartAsync();

            // Apply custom theme overrides (must be after theme is loaded)
            ApplyCustomTheme();

            SplashWindow.SetStatus("Loading icons...");
            Imago.UI.Services.IconService.Instance.Initialize();

            SplashWindow.SetStatus("Preparing workspace...");
            var mainWindow = GetService<MainWindow>();
            MainWindow = mainWindow;

            SplashWindow.CloseAndDispose();
            mainWindow.Show();
        }
        catch (Exception ex)
        {
            SplashWindow.CloseAndDispose();
            LogException(ex, "Startup Exception");
            ExceptionWindow.Show(ex, "Startup Exception (Fatal)", canContinue: false);
        }
    }

    /// <summary>
    /// Applies custom theme overrides by adding our ResourceDictionary after WPF UI's theme.
    /// Resources added later to MergedDictionaries take precedence.
    /// </summary>
    private void ApplyCustomTheme()
    {
        try
        {
            var themeOverride = new ResourceDictionary
            {
                Source = new Uri("pack://application:,,,/Imago.UI;component/Themes/WpfUiOverrides.xaml", UriKind.Absolute)
            };
            
            Application.Current.Resources.MergedDictionaries.Add(themeOverride);
            Log.Information("Custom theme overrides applied successfully");
        }
        catch (Exception ex)
        {
            Log.Warning(ex, "Failed to apply custom theme overrides");
        }
    }

    private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        e.Handled = true;
        LogException(e.Exception, "UI Thread Exception");
        ExceptionWindow.Show(e.Exception, "UI Thread Exception", canContinue: true);
    }

    private void OnUnhandledException(object sender, UnhandledExceptionEventArgs e)
    {
        if (e.ExceptionObject is Exception ex)
        {
            LogException(ex, "Unhandled Exception");
            ExceptionWindow.Show(ex, "Unhandled Exception (Fatal)", canContinue: false);
        }
    }

    private void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
    {
        e.SetObserved();
        LogException(e.Exception, "Task Exception");
        ExceptionWindow.Show(e.Exception, "Async Task Exception", canContinue: true);
    }

    private static void LogException(Exception ex, string title)
    {
        try
        {
            Log.Error(ex, "{Title}: {Message}", title, ex.Message);
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

    private async void OnExit(object sender, ExitEventArgs e)
    {
        Log.Information("Imago shutting down...");

        SingleInstanceManager.Instance?.Dispose();

        await s_host.StopAsync();
        s_host.Dispose();

        await Log.CloseAndFlushAsync();
    }
}
