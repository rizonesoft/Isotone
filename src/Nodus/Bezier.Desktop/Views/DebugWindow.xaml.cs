using System.Collections.ObjectModel;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Bezier.Core.Services;
using Microsoft.Win32;
using Wpf.Ui.Controls;

namespace Bezier.Desktop.Views;

/// <summary>
/// Developer Tools window for debugging and inspection.
/// </summary>
public partial class DebugWindow : FluentWindow
{
    private readonly ObservableCollection<LogEntryViewModel> _logEntries = [];
    private readonly ObservableCollection<LogEntryViewModel> _filteredEntries = [];
    private string _filterText = string.Empty;
    private bool _isLoaded;
    
    // Singleton instance
    private static DebugWindow? _instance;
    private static readonly object _lock = new();
    
    // Window state persistence
    private static double _savedLeft = double.NaN;
    private static double _savedTop = double.NaN;
    private static double _savedWidth = 600;
    private static double _savedHeight = 400;
    private static bool _savedAlwaysOnTop;
    private static bool _isInitialized;

    private DebugWindow()
    {
        InitializeComponent();
        
        LogListBox.ItemsSource = _filteredEntries;
        
        // Subscribe to debug logger
        DebugLogger.Instance.LogAdded += OnLogAdded;
        
        _isLoaded = true;
    }

    /// <summary>
    /// Gets or creates the singleton instance of the debug window.
    /// </summary>
    public static DebugWindow Instance
    {
        get
        {
            lock (_lock)
            {
                if (_instance is null || !_instance.IsLoaded)
                {
                    _instance = new DebugWindow();
                }
                return _instance;
            }
        }
    }

    /// <summary>
    /// Shows the singleton debug window, bringing it to front if already open.
    /// </summary>
    public static void ShowInstance()
    {
        var window = Instance;
        if (window.IsVisible)
        {
            window.Activate();
            if (window.WindowState == WindowState.Minimized)
                window.WindowState = WindowState.Normal;
        }
        else
        {
            window.Show();
        }
    }

    private void TitleBar_MouseLeftButtonDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
    {
        if (e.ClickCount == 2)
        {
            WindowState = WindowState == WindowState.Maximized ? WindowState.Normal : WindowState.Maximized;
        }
        else
        {
            DragMove();
        }
    }

    private void Close_Click(object sender, RoutedEventArgs e)
    {
        Hide();
    }

    private void Window_Loaded(object sender, RoutedEventArgs e)
    {
        // Restore window position and state
        if (_isInitialized)
        {
            if (!double.IsNaN(_savedLeft) && !double.IsNaN(_savedTop))
            {
                Left = _savedLeft;
                Top = _savedTop;
            }
            Width = _savedWidth;
            Height = _savedHeight;
            Topmost = _savedAlwaysOnTop;
            AlwaysOnTopCheckBox.IsChecked = _savedAlwaysOnTop;
        }
        else
        {
            // First time - position near bottom right of primary screen
            var workArea = SystemParameters.WorkArea;
            Left = workArea.Right - Width - 20;
            Top = workArea.Bottom - Height - 60;
            _isInitialized = true;
        }
        
        // Load existing logs (must be done after UI is initialized)
        foreach (var entry in DebugLogger.Instance.Entries)
        {
            var vm = new LogEntryViewModel(entry);
            _logEntries.Add(vm);
            if (PassesFilter(vm))
                _filteredEntries.Add(vm);
        }
        
        UpdateStatus();
        DebugLogger.Instance.Info("DebugWindow", "Developer Tools opened");
    }

    private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
    {
        // Save window position and state
        _savedLeft = Left;
        _savedTop = Top;
        _savedWidth = Width;
        _savedHeight = Height;
        _savedAlwaysOnTop = Topmost;
        
        // Unsubscribe from logger
        DebugLogger.Instance.LogAdded -= OnLogAdded;
    }

    private void OnLogAdded(object? sender, LogEntry entry)
    {
        // Marshal to UI thread
        Dispatcher.BeginInvoke(() =>
        {
            var vm = new LogEntryViewModel(entry);
            _logEntries.Add(vm);
            
            if (PassesFilter(vm))
            {
                _filteredEntries.Add(vm);
                
                // Auto-scroll if enabled
                if (AutoScrollCheckBox.IsChecked == true && _filteredEntries.Count > 0)
                {
                    LogListBox.ScrollIntoView(_filteredEntries[^1]);
                }
            }
            
            UpdateStatus();
        });
    }

    private void AlwaysOnTop_Changed(object sender, RoutedEventArgs e)
    {
        Topmost = AlwaysOnTopCheckBox.IsChecked == true;
    }

    private void Clear_Click(object sender, RoutedEventArgs e)
    {
        DebugLogger.Instance.Clear();
        _logEntries.Clear();
        _filteredEntries.Clear();
        UpdateStatus();
    }

    private void Filter_TextChanged(object sender, TextChangedEventArgs e)
    {
        if (!_isLoaded) return;
        _filterText = FilterTextBox.Text ?? string.Empty;
        ApplyFilter();
    }

    private void LogLevel_Changed(object sender, RoutedEventArgs e)
    {
        if (!_isLoaded) return;
        ApplyFilter();
    }

    private void ApplyFilter()
    {
        _filteredEntries.Clear();
        
        foreach (var entry in _logEntries)
        {
            if (PassesFilter(entry))
            {
                _filteredEntries.Add(entry);
            }
        }
        
        UpdateStatus();
    }

    private bool PassesFilter(LogEntryViewModel entry)
    {
        // Check log level filter
        var showLevel = entry.Level switch
        {
            "Debug" => ShowDebugCheckBox?.IsChecked == true,
            "Info" => ShowInfoCheckBox?.IsChecked == true,
            "Warning" => ShowWarningCheckBox?.IsChecked == true,
            "Error" => ShowErrorCheckBox?.IsChecked == true,
            _ => true
        };
        
        if (!showLevel) return false;
        
        // Check text filter
        if (!string.IsNullOrEmpty(_filterText))
        {
            return entry.Category.Contains(_filterText, StringComparison.OrdinalIgnoreCase) ||
                   entry.Message.Contains(_filterText, StringComparison.OrdinalIgnoreCase);
        }
        
        return true;
    }

    private void UpdateStatus()
    {
        if (StatusText is null) return;
        StatusText.Text = $"{_filteredEntries.Count} of {_logEntries.Count} entries";
    }

    private void CopySelected_Click(object sender, RoutedEventArgs e)
    {
        var selected = LogListBox.SelectedItems.Cast<LogEntryViewModel>();
        var text = string.Join(Environment.NewLine, selected.Select(FormatLogEntry));
        
        if (!string.IsNullOrEmpty(text))
        {
            Clipboard.SetText(text);
            DebugLogger.Instance.Info("DebugWindow", $"Copied {LogListBox.SelectedItems.Count} entries to clipboard");
        }
    }

    private void CopyAll_Click(object sender, RoutedEventArgs e)
    {
        var text = string.Join(Environment.NewLine, _filteredEntries.Select(FormatLogEntry));
        
        if (!string.IsNullOrEmpty(text))
        {
            Clipboard.SetText(text);
            DebugLogger.Instance.Info("DebugWindow", $"Copied {_filteredEntries.Count} entries to clipboard");
        }
    }

    private void ExportToFile_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new SaveFileDialog
        {
            Filter = "Log Files (*.log)|*.log|Text Files (*.txt)|*.txt|All Files (*.*)|*.*",
            DefaultExt = ".log",
            FileName = $"bezier-debug-{DateTime.Now:yyyyMMdd-HHmmss}.log"
        };
        
        if (dialog.ShowDialog() == true)
        {
            var text = string.Join(Environment.NewLine, _filteredEntries.Select(FormatLogEntry));
            File.WriteAllText(dialog.FileName, text);
            DebugLogger.Instance.Info("DebugWindow", $"Exported {_filteredEntries.Count} entries to {dialog.FileName}");
        }
    }

    private static string FormatLogEntry(LogEntryViewModel entry)
    {
        return $"[{entry.Timestamp:yyyy-MM-dd HH:mm:ss.fff}] [{entry.Level}] [{entry.Category}] {entry.Message}";
    }
}

/// <summary>
/// ViewModel wrapper for log entries with UI-friendly properties.
/// </summary>
public class LogEntryViewModel
{
    public DateTime Timestamp { get; }
    public string Level { get; }
    public string Category { get; }
    public string Message { get; }
    public Brush LevelBrush { get; }

    public LogEntryViewModel(LogEntry entry)
    {
        Timestamp = entry.Timestamp;
        Level = entry.Level.ToString();
        Category = entry.Category;
        Message = entry.Message;
        
        LevelBrush = entry.Level switch
        {
            LogLevel.Debug => new SolidColorBrush(Color.FromRgb(166, 173, 200)), // Subtext
            LogLevel.Info => new SolidColorBrush(Color.FromRgb(137, 180, 250)),  // Blue
            LogLevel.Warning => new SolidColorBrush(Color.FromRgb(249, 226, 175)), // Yellow
            LogLevel.Error => new SolidColorBrush(Color.FromRgb(243, 139, 168)),  // Red
            _ => new SolidColorBrush(Color.FromRgb(205, 214, 244)) // Text
        };
    }
}
