using System.Diagnostics;
using System.Windows;
using System.Windows.Media;
using System.Windows.Threading;
using Bezier.Desktop.Helpers;

namespace Bezier.Desktop.Views;

/// <summary>
/// Splash window displayed during application startup.
/// Runs on a separate UI thread to keep animations smooth during blocking operations.
/// </summary>
public partial class SplashWindow : Window
{
    private const int MinDisplayTimeMs = 1500; // Minimum time splash is shown
    
    private Thread? _splashThread;
    private Dispatcher? _splashDispatcher;
    private static SplashWindow? _instance;
    private static readonly ManualResetEventSlim _readyEvent = new(false);
    private static readonly Stopwatch _displayTimer = new();

    public SplashWindow()
    {
        InitializeComponent();
        
        Loaded += (s, e) =>
        {
            StartBorderGlowAnimation();
        };
    }

    /// <summary>
    /// Shows the splash screen on a separate UI thread so animations run smoothly
    /// while the main thread initializes.
    /// </summary>
    public static void ShowOnSeparateThread()
    {
        _readyEvent.Reset();
        _displayTimer.Restart();
        
        var thread = new Thread(() =>
        {
            _instance = new SplashWindow();
            _instance._splashThread = Thread.CurrentThread;
            _instance._splashDispatcher = Dispatcher.CurrentDispatcher;
            
            _instance.Show();
            _readyEvent.Set();
            
            Dispatcher.Run();
        });
        
        thread.SetApartmentState(ApartmentState.STA);
        thread.IsBackground = true;
        thread.Start();
        
        // Wait for splash to be ready
        _readyEvent.Wait();
    }

    /// <summary>
    /// Updates the status text displayed on the splash screen.
    /// Thread-safe - can be called from any thread.
    /// </summary>
    /// <param name="status">The status message to display.</param>
    public static void SetStatusText(string status)
    {
        _instance?._splashDispatcher?.BeginInvoke(() =>
        {
            if (_instance != null)
                _instance.StatusText.Text = status;
        });
    }

    /// <summary>
    /// Closes the splash screen and shuts down its dispatcher.
    /// Ensures splash is shown for at least MinDisplayTimeMs to avoid jarring quick flashes.
    /// </summary>
    public static void CloseAndDispose()
    {
        // Ensure minimum display time so splash doesn't flash on fast starts
        var elapsed = (int)_displayTimer.ElapsedMilliseconds;
        if (elapsed < MinDisplayTimeMs)
        {
            Thread.Sleep(MinDisplayTimeMs - elapsed);
        }
        _displayTimer.Stop();
        
        _instance?._splashDispatcher?.BeginInvoke(() =>
        {
            _instance?.Close();
            _instance?._splashDispatcher?.InvokeShutdown();
            _instance = null;
        });
    }

    /// <summary>
    /// Updates the status text displayed on the splash screen.
    /// </summary>
    /// <param name="status">The status message to display.</param>
    public void SetStatus(string status)
    {
        Dispatcher.Invoke(() => StatusText.Text = status);
    }

    /// <summary>
    /// Starts the border glow animation that follows the border edges.
    /// </summary>
    private void StartBorderGlowAnimation()
    {
        // Canvas size is 404x304 (window 420x320 minus margin 8 on each side)
        var animator = new BorderGlowAnimator(GlowPath, GlowMask)
        {
            CornerRadius = 12,
            Duration = TimeSpan.FromSeconds(4),
            Steps = 200
        };
        animator.Initialize(404, 304);
    }
}
