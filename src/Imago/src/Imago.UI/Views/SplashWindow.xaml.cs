namespace Imago.UI.Views;

using System.Diagnostics;
using System.Reflection;
using System.Windows;
using System.Windows.Threading;
using Imago.UI.Helpers;

/// <summary>
/// Splash window displayed during application startup.
/// Runs on a separate UI thread to keep animations smooth during blocking operations.
/// </summary>
public partial class SplashWindow : Window
{
    private const int MinDisplayTimeMs = 1500;

    private Thread? _splashThread;
    private Dispatcher? _splashDispatcher;
    private static SplashWindow? s_instance;
    private static readonly ManualResetEventSlim s_readyEvent = new(false);
    private static readonly Stopwatch s_displayTimer = new();

    public SplashWindow()
    {
        InitializeComponent();

        // Set version from assembly
        var version = Assembly.GetExecutingAssembly().GetName().Version;
        VersionText.Text = $"Version {version?.Major}.{version?.Minor}.{version?.Build}";

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
        s_readyEvent.Reset();
        s_displayTimer.Restart();

        var thread = new Thread(() =>
        {
            s_instance = new SplashWindow();
            s_instance._splashThread = Thread.CurrentThread;
            s_instance._splashDispatcher = Dispatcher.CurrentDispatcher;

            s_instance.Show();
            s_readyEvent.Set();

            Dispatcher.Run();
        });

        thread.SetApartmentState(ApartmentState.STA);
        thread.IsBackground = true;
        thread.Start();

        // Wait for splash to be ready
        s_readyEvent.Wait();
    }

    /// <summary>
    /// Updates the status text displayed on the splash screen.
    /// Thread-safe - can be called from any thread.
    /// </summary>
    public static void SetStatus(string status)
    {
        var instance = s_instance;
        instance?._splashDispatcher?.BeginInvoke(() =>
        {
            instance.StatusText.Text = status;
        });
    }

    /// <summary>
    /// Closes the splash screen and shuts down its dispatcher.
    /// Ensures splash is shown for at least MinDisplayTimeMs to avoid jarring quick flashes.
    /// </summary>
    public static void CloseAndDispose()
    {
        // Ensure minimum display time so splash doesn't flash on fast starts
        var elapsed = (int)s_displayTimer.ElapsedMilliseconds;
        if (elapsed < MinDisplayTimeMs)
        {
            Thread.Sleep(MinDisplayTimeMs - elapsed);
        }
        s_displayTimer.Stop();

        s_instance?._splashDispatcher?.BeginInvoke(() =>
        {
            s_instance?.Close();
            s_instance?._splashDispatcher?.InvokeShutdown();
            s_instance = null;
        });
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
