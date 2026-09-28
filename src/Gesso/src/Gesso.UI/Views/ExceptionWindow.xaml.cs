#pragma warning disable CA1305 // StringBuilder formatting for exception display

namespace Gesso.UI.Views;

using System.Text;
using System.Windows;
using System.Windows.Media;
using System.Windows.Threading;

/// <summary>
/// Exception display window for showing handled and unhandled exceptions.
/// </summary>
public partial class ExceptionWindow : Window
{
    private readonly string _fullExceptionText;

    public ExceptionWindow(Exception exception, string title, bool canContinue = true)
    {
        InitializeComponent();
        
        TitleText.Text = title;
        ExceptionTypeText.Text = exception.GetType().FullName;
        MessageText.Text = exception.Message;
        
        var sb = new StringBuilder();
        BuildStackTrace(sb, exception, 0);
        StackTraceText.Text = sb.ToString();
        
        _fullExceptionText = BuildFullExceptionText(exception, title);
        
        ContinueButton.Visibility = canContinue ? Visibility.Visible : Visibility.Collapsed;
        
        if (title.Contains("Unhandled", StringComparison.OrdinalIgnoreCase))
        {
            IconBackground.Color = Color.FromRgb(243, 139, 168);
        }
        else
        {
            IconBackground.Color = Color.FromRgb(249, 226, 175);
        }
    }

    private static void BuildStackTrace(StringBuilder sb, Exception ex, int level)
    {
        var indent = new string(' ', level * 2);
        
        if (level > 0)
        {
            sb.AppendLine();
            sb.AppendLine($"{indent}--- Inner Exception ({ex.GetType().Name}) ---");
            sb.AppendLine($"{indent}Message: {ex.Message}");
            sb.AppendLine();
        }
        
        if (!string.IsNullOrEmpty(ex.StackTrace))
        {
            foreach (var line in ex.StackTrace.Split('\n'))
            {
                sb.AppendLine($"{indent}{line.Trim()}");
            }
        }
        else
        {
            sb.AppendLine($"{indent}(No stack trace available)");
        }
        
        if (ex.InnerException is not null)
        {
            BuildStackTrace(sb, ex.InnerException, level + 1);
        }
    }

    private static string BuildFullExceptionText(Exception ex, string title)
    {
        var sb = new StringBuilder();
        sb.AppendLine("=".PadRight(60, '='));
        sb.AppendLine("GESSO EXCEPTION REPORT");
        sb.AppendLine($"Time: {DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}");
        sb.AppendLine($"Type: {title}");
        sb.AppendLine("=".PadRight(60, '='));
        sb.AppendLine();
        
        BuildFullExceptionDetails(sb, ex, 0);
        
        sb.AppendLine();
        sb.AppendLine("=".PadRight(60, '='));
        sb.AppendLine("System Information:");
        sb.AppendLine($"  OS: {Environment.OSVersion}");
        sb.AppendLine($"  .NET: {Environment.Version}");
        sb.AppendLine($"  64-bit OS: {Environment.Is64BitOperatingSystem}");
        sb.AppendLine($"  64-bit Process: {Environment.Is64BitProcess}");
        sb.AppendLine("=".PadRight(60, '='));
        
        return sb.ToString();
    }

    private static void BuildFullExceptionDetails(StringBuilder sb, Exception ex, int level)
    {
        var prefix = level > 0 ? $"[Inner Exception {level}] " : "";
        
        sb.AppendLine($"{prefix}Exception Type: {ex.GetType().FullName}");
        sb.AppendLine($"{prefix}Message: {ex.Message}");
        sb.AppendLine($"{prefix}Source: {ex.Source ?? "N/A"}");
        sb.AppendLine($"{prefix}Target Site: {ex.TargetSite?.ToString() ?? "N/A"}");
        sb.AppendLine();
        sb.AppendLine($"{prefix}Stack Trace:");
        
        if (!string.IsNullOrEmpty(ex.StackTrace))
        {
            foreach (var line in ex.StackTrace.Split('\n'))
            {
                sb.AppendLine($"  {line.Trim()}");
            }
        }
        else
        {
            sb.AppendLine("  (No stack trace available)");
        }
        
        if (ex.InnerException is not null)
        {
            sb.AppendLine();
            BuildFullExceptionDetails(sb, ex.InnerException, level + 1);
        }
    }

    private void Copy_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            Clipboard.SetText(_fullExceptionText);
            CopyButton.Content = "Copied!";
            
            var timer = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(2)
            };
            timer.Tick += (_, _) =>
            {
                CopyButton.Content = "Copy to Clipboard";
                timer.Stop();
            };
            timer.Start();
        }
        catch
        {
            CopyButton.Content = "Copy Failed";
        }
    }

    private void Continue_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = true;
        Close();
    }

    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = false;
        Application.Current.Shutdown(1);
    }

    /// <summary>
    /// Shows the exception window and returns whether the user chose to continue.
    /// </summary>
    public static bool Show(Exception exception, string title, bool canContinue = true)
    {
        var window = new ExceptionWindow(exception, title, canContinue);
        return window.ShowDialog() == true;
    }
}
