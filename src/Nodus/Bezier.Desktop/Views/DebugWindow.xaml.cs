using System.Collections.ObjectModel;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Bezier.Core.Models;
using Bezier.Core.Models.Fills;
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
    private readonly HashSet<string> _knownCategories = [];
    private string _filterText = string.Empty;
    private string _selectedCategory = string.Empty;
    private bool _isLoaded;
    private bool _liveUpdateEnabled = true;
    
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
        
        // Subscribe to debug info service for Coordinates tab
        DebugInfoService.Instance.InfoUpdated += OnDebugInfoUpdated;
        
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

    private void Tab_Checked(object sender, RoutedEventArgs e)
    {
        if (!_isLoaded) return;
        
        if (sender is RadioButton rb && rb.Tag is string tabName)
        {
            ConsolePanel.Visibility = tabName == "Console" ? Visibility.Visible : Visibility.Collapsed;
            CoordinatesPanel.Visibility = tabName == "Coordinates" ? Visibility.Visible : Visibility.Collapsed;
            ElementsPanel.Visibility = tabName == "Elements" ? Visibility.Visible : Visibility.Collapsed;
            PerformancePanel.Visibility = tabName == "Performance" ? Visibility.Visible : Visibility.Collapsed;
        }
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
            // Register category
            AddCategoryIfNew(entry.Category);
            
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
        
        // Unsubscribe from services
        DebugLogger.Instance.LogAdded -= OnLogAdded;
        DebugInfoService.Instance.InfoUpdated -= OnDebugInfoUpdated;
    }

    private void OnLogAdded(object? sender, LogEntry entry)
    {
        // Register category if new
        AddCategoryIfNew(entry.Category);
        
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

    private void CategoryFilter_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
    {
        if (!_isLoaded) return;
        
        if (CategoryFilterComboBox.SelectedItem is ComboBoxItem item && item.Tag is string category)
        {
            _selectedCategory = category;
            ApplyFilter();
        }
    }

    private void AddCategoryIfNew(string category)
    {
        if (_knownCategories.Add(category))
        {
            // Add new category to the dropdown
            Dispatcher.BeginInvoke(() =>
            {
                var item = new ComboBoxItem
                {
                    Content = category,
                    Tag = category,
                    Foreground = FindResource("TextBrush") as Brush,
                    Background = FindResource("Surface0Brush") as Brush,
                    FontSize = 11,
                    Padding = new Thickness(8, 4, 8, 4)
                };
                CategoryFilterComboBox.Items.Add(item);
            });
        }
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
        
        // Check category filter
        if (!string.IsNullOrEmpty(_selectedCategory))
        {
            if (!entry.Category.Equals(_selectedCategory, StringComparison.OrdinalIgnoreCase))
                return false;
        }
        
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
        
        // Update level counts
        var debugCount = _logEntries.Count(e => e.Level == "Debug");
        var infoCount = _logEntries.Count(e => e.Level == "Info");
        var warnCount = _logEntries.Count(e => e.Level == "Warning");
        var errorCount = _logEntries.Count(e => e.Level == "Error");
        
        if (DebugCountText is not null) DebugCountText.Text = $"D:{debugCount}";
        if (InfoCountText is not null) InfoCountText.Text = $"I:{infoCount}";
        if (WarnCountText is not null) WarnCountText.Text = $"W:{warnCount}";
        if (ErrorCountText is not null) ErrorCountText.Text = $"E:{errorCount}";
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

    #region Coordinates Tab

    private void OnDebugInfoUpdated(object? sender, DebugInfoUpdateEventArgs e)
    {
        if (!_liveUpdateEnabled) return;
        
        // Marshal to UI thread
        Dispatcher.BeginInvoke(() => UpdateCoordinatesDisplay(e.Snapshot));
    }

    private void UpdateCoordinatesDisplay(DebugInfoSnapshot snapshot)
    {
        // Mouse coordinates
        ScreenCoordsText.Text = $"{snapshot.ScreenX:F1}, {snapshot.ScreenY:F1}";
        DocumentCoordsText.Text = $"{snapshot.DocumentX:F1}, {snapshot.DocumentY:F1}";
        
        if (!string.IsNullOrEmpty(snapshot.ActiveArtboardName))
        {
            ArtboardCoordsText.Text = $"{snapshot.ArtboardX:F1}, {snapshot.ArtboardY:F1} [{snapshot.ActiveArtboardName}]";
        }
        else
        {
            ArtboardCoordsText.Text = "—";
        }
        
        // Canvas state
        ZoomLevelText.Text = $"{snapshot.ZoomLevel * 100:F0}%";
        PanOffsetText.Text = $"{snapshot.PanOffsetX:F1}, {snapshot.PanOffsetY:F1}";
        ViewportText.Text = $"{snapshot.ViewportWidth:F0} × {snapshot.ViewportHeight:F0}";
        
        // Selection
        if (snapshot.SelectionCount == 0)
        {
            NoSelectionGrid.Visibility = Visibility.Visible;
            SelectionInfoGrid.Visibility = Visibility.Collapsed;
            SelectionBoundsPanel.Visibility = Visibility.Collapsed;
        }
        else if (snapshot.SelectionCount == 1 && snapshot.PrimarySelection is not null)
        {
            NoSelectionGrid.Visibility = Visibility.Collapsed;
            SelectionInfoGrid.Visibility = Visibility.Visible;
            SelectionBoundsPanel.Visibility = Visibility.Collapsed;
            
            UpdateSingleElementDisplay(snapshot.PrimarySelection);
        }
        else
        {
            // Multi-selection
            NoSelectionGrid.Visibility = Visibility.Collapsed;
            SelectionInfoGrid.Visibility = Visibility.Collapsed;
            SelectionBoundsPanel.Visibility = Visibility.Visible;
            
            SelectionCountText.Text = snapshot.SelectionCount.ToString();
            
            if (snapshot.SelectionBounds is not null)
            {
                var b = snapshot.SelectionBounds.Value;
                SelectionPositionText.Text = $"{b.X:F1}, {b.Y:F1}";
                SelectionSizeText.Text = $"{b.Width:F1} × {b.Height:F1}";
            }
        }
    }

    private void UpdateSingleElementDisplay(VectorElement element)
    {
        ElementTypeText.Text = element.GetType().Name.Replace("Svg", "");
        ElementNameText.Text = string.IsNullOrEmpty(element.Name) ? "(unnamed)" : element.Name;
        
        var bounds = element.GetBoundingBox();
        ElementPositionText.Text = $"{bounds.X:F1}, {bounds.Y:F1}";
        ElementSizeText.Text = $"{bounds.Width:F1} × {bounds.Height:F1}";
        
        var t = element.Transform;
        var rotationDeg = Math.Atan2(t.SkewY, t.ScaleX) * 180.0 / Math.PI;
        ElementTransformText.Text = $"T({t.TranslateX:F1}, {t.TranslateY:F1}) S({t.ScaleX:F2}, {t.ScaleY:F2}) R({rotationDeg:F1}°)";
        
        ElementBoundsText.Text = $"({bounds.X:F1}, {bounds.Y:F1}) → ({bounds.X + bounds.Width:F1}, {bounds.Y + bounds.Height:F1})";
        
        // Fill info
        ElementFillText.Text = element.Fill switch
        {
            null => "None",
            NoneFill => "None",
            SolidFill solid => $"Solid #{solid.R:X2}{solid.G:X2}{solid.B:X2}",
            LinearGradientFill => "Linear Gradient",
            RadialGradientFill => "Radial Gradient",
            PatternFill => "Pattern",
            _ => element.Fill.GetType().Name
        };
        
        // Stroke info
        if (element.Stroke is not null && element.Stroke.Width > 0)
        {
            var stroke = element.Stroke;
            var strokeFillText = stroke.Fill switch
            {
                SolidFill solid => $"#{solid.R:X2}{solid.G:X2}{solid.B:X2}",
                _ => stroke.Fill?.GetType().Name ?? "None"
            };
            ElementStrokeText.Text = $"{stroke.Width}px {strokeFillText}";
        }
        else
        {
            ElementStrokeText.Text = "None";
        }
    }

    private void LiveUpdate_Changed(object sender, RoutedEventArgs e)
    {
        _liveUpdateEnabled = LiveUpdateCheckBox?.IsChecked == true;
    }

    private void CopyCoordinatesInfo_Click(object sender, RoutedEventArgs e)
    {
        var text = DebugInfoService.Instance.FormatAllInfo();
        Clipboard.SetText(text);
        DebugLogger.Instance.Info("DebugWindow", "Copied coordinates info to clipboard");
    }

    #endregion
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
            LogLevel.Debug => new SolidColorBrush(System.Windows.Media.Color.FromRgb(166, 173, 200)), // Subtext
            LogLevel.Info => new SolidColorBrush(System.Windows.Media.Color.FromRgb(137, 180, 250)),  // Blue
            LogLevel.Warning => new SolidColorBrush(System.Windows.Media.Color.FromRgb(249, 226, 175)), // Yellow
            LogLevel.Error => new SolidColorBrush(System.Windows.Media.Color.FromRgb(243, 139, 168)),  // Red
            _ => new SolidColorBrush(System.Windows.Media.Color.FromRgb(205, 214, 244)) // Text
        };
    }
}
