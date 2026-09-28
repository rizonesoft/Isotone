namespace Gesso.UI.Services;

using System.IO;
using System.IO.Pipes;
using System.Windows;
using Serilog;

/// <summary>
/// Manages single-instance application behavior using a named mutex and named pipes.
/// </summary>
public sealed class SingleInstanceManager : IDisposable
{
    private const string MutexName = "Gesso.SingleInstance.Mutex.{7E3B4A2C-1D5F-4E8A-9C6B-0F2E8D7A3B1C}";
    private const string PipeName = "Gesso.SingleInstance.Pipe.{7E3B4A2C-1D5F-4E8A-9C6B-0F2E8D7A3B1C}";

    private static readonly ILogger s_logger = Log.ForContext<SingleInstanceManager>();
    private static SingleInstanceManager? s_instance;

    private readonly Mutex _mutex;
    private readonly bool _isFirstInstance;
    private CancellationTokenSource? _pipeServerCts;
    private Task? _pipeServerTask;

    /// <summary>
    /// Gets whether this is the first (primary) instance.
    /// </summary>
    public bool IsFirstInstance => _isFirstInstance;

    /// <summary>
    /// Raised when another instance attempts to start.
    /// </summary>
    public event EventHandler<string[]>? SecondInstanceStarted;

    private SingleInstanceManager()
    {
        _mutex = new Mutex(true, MutexName, out _isFirstInstance);

        if (_isFirstInstance)
        {
            s_logger.Information("Single instance: This is the primary instance");
            StartPipeServer();
        }
        else
        {
            s_logger.Information("Single instance: Another instance is already running");
        }
    }

    /// <summary>
    /// Initializes the single instance manager.
    /// </summary>
    /// <returns>True if this is the first instance; false if another instance exists.</returns>
    public static bool Initialize()
    {
        s_instance = new SingleInstanceManager();
        return s_instance.IsFirstInstance;
    }

    /// <summary>
    /// Gets the current instance.
    /// </summary>
    public static SingleInstanceManager? Instance => s_instance;

    /// <summary>
    /// Notifies the existing instance and passes command-line arguments.
    /// </summary>
    public static void NotifyExistingInstance(string[] args)
    {
        try
        {
            using var client = new NamedPipeClientStream(".", PipeName, PipeDirection.Out);
            client.Connect(1000);

            using var writer = new StreamWriter(client);
            writer.WriteLine(string.Join("\0", args));
            writer.Flush();

            s_logger.Information("Single instance: Notified existing instance with {ArgCount} args", args.Length);
        }
        catch (Exception ex)
        {
            s_logger.Warning(ex, "Single instance: Failed to notify existing instance");
        }
    }

    /// <summary>
    /// Brings the main window to the foreground.
    /// </summary>
    public static void ActivateMainWindow()
    {
        Application.Current.Dispatcher.Invoke(() =>
        {
            var mainWindow = Application.Current.MainWindow;
            if (mainWindow is null) return;

            if (mainWindow.WindowState == WindowState.Minimized)
            {
                mainWindow.WindowState = WindowState.Normal;
            }

            mainWindow.Activate();
            mainWindow.Topmost = true;
            mainWindow.Topmost = false;
            mainWindow.Focus();

            s_logger.Debug("Single instance: Main window activated");
        });
    }

    private void StartPipeServer()
    {
        _pipeServerCts = new CancellationTokenSource();
        _pipeServerTask = Task.Run(async () => await RunPipeServerAsync(_pipeServerCts.Token));
    }

    private async Task RunPipeServerAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            try
            {
                await using var server = new NamedPipeServerStream(
                    PipeName,
                    PipeDirection.In,
                    1,
                    PipeTransmissionMode.Byte,
                    PipeOptions.Asynchronous);

                await server.WaitForConnectionAsync(ct);

                using var reader = new StreamReader(server);
                var message = await reader.ReadLineAsync(ct);

                if (!string.IsNullOrEmpty(message))
                {
                    var args = message.Split('\0', StringSplitOptions.RemoveEmptyEntries);
                    s_logger.Information("Single instance: Received activation from another instance with {ArgCount} args", args.Length);

                    SecondInstanceStarted?.Invoke(this, args);
                    ActivateMainWindow();
                }
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                s_logger.Warning(ex, "Single instance: Pipe server error");
                await Task.Delay(100, ct);
            }
        }
    }

    public void Dispose()
    {
        _pipeServerCts?.Cancel();

        try
        {
            _pipeServerTask?.Wait(1000);
        }
        catch { }

        _pipeServerCts?.Dispose();
        _mutex.Dispose();

        s_logger.Debug("Single instance: Manager disposed");
    }
}
