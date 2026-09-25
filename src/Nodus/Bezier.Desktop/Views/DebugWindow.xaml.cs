using System.Collections.ObjectModel;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Bezier.Core.Models;
using Bezier.Core.Models.Fills;
using Bezier.Core.Services;
using Microsoft.Win32;
namespace Bezier.Desktop.Views;

/// <summary>
/// Developer Tools window for debugging and inspection.
/// </summary>
public partial class DebugWindow : Window
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
        
        // Subscribe to performance metrics for Performance tab
        PerformanceMetricsService.Instance.MetricsUpdated += OnPerformanceMetricsUpdated;
        
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
        PerformanceMetricsService.Instance.MetricsUpdated -= OnPerformanceMetricsUpdated;
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

    #region Elements Inspector Tab

    private VectorDocument? _currentDocument;
    private readonly ObservableCollection<ElementTreeItemViewModel> _elementTreeItems = [];
    private VectorElement? _hoveredElement;
    private bool _suppressTreeSelection;

    /// <summary>
    /// Sets the document to inspect.
    /// </summary>
    public void SetDocument(VectorDocument? document)
    {
        if (_currentDocument == document) return;
        
        // Unsubscribe from old document
        if (_currentDocument is not null)
        {
            _currentDocument.Elements.CollectionChanged -= OnDocumentElementsChanged;
        }
        
        _currentDocument = document;
        
        // Subscribe to new document
        if (_currentDocument is not null)
        {
            _currentDocument.Elements.CollectionChanged += OnDocumentElementsChanged;
        }
        
        RefreshElementTree();
    }

    private void OnDocumentElementsChanged(object? sender, System.Collections.Specialized.NotifyCollectionChangedEventArgs e)
    {
        Dispatcher.BeginInvoke(RefreshElementTree);
    }

    private void RefreshElementTree()
    {
        _elementTreeItems.Clear();
        
        if (_currentDocument is null || _currentDocument.Elements.Count == 0)
        {
            ElementTreeView.ItemsSource = null;
            NoElementsMessage.Visibility = Visibility.Visible;
            ElementCountText.Text = "0 elements";
            return;
        }
        
        NoElementsMessage.Visibility = Visibility.Collapsed;
        
        var totalCount = 0;
        foreach (var element in _currentDocument.Elements)
        {
            var item = CreateTreeItem(element, ref totalCount);
            _elementTreeItems.Add(item);
        }
        
        ElementTreeView.ItemsSource = _elementTreeItems;
        ElementCountText.Text = $"{totalCount} element{(totalCount == 1 ? "" : "s")}";
    }

    private static ElementTreeItemViewModel CreateTreeItem(VectorElement element, ref int count)
    {
        count++;
        var item = new ElementTreeItemViewModel(element);
        
        if (element is Bezier.Core.Models.Elements.SvgGroup group)
        {
            foreach (var child in group.Children)
            {
                item.Children.Add(CreateTreeItem(child, ref count));
            }
        }
        
        return item;
    }

    private void RefreshElements_Click(object sender, RoutedEventArgs e)
    {
        RefreshElementTree();
        DebugLogger.Instance.Log("DebugWindow", "Element tree refreshed");
    }

    private void ElementTree_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
    {
        if (_suppressTreeSelection) return;
        
        if (e.NewValue is ElementTreeItemViewModel item)
        {
            // Raise event to select in canvas
            ElementSelectedInTree?.Invoke(this, item.Element);
            DebugLogger.Instance.Log("DebugWindow", $"Selected element: {item.DisplayName}");
        }
    }

    private void TreeItem_MouseEnter(object sender, System.Windows.Input.MouseEventArgs e)
    {
        if (sender is System.Windows.Controls.TreeViewItem tvi && tvi.DataContext is ElementTreeItemViewModel item)
        {
            _hoveredElement = item.Element;
            ElementHovered?.Invoke(this, item.Element);
        }
    }

    private void TreeItem_MouseLeave(object sender, System.Windows.Input.MouseEventArgs e)
    {
        _hoveredElement = null;
        ElementHovered?.Invoke(this, null);
    }

    private void ToggleVisibility_Click(object sender, RoutedEventArgs e)
    {
        if (sender is System.Windows.Controls.Button btn && btn.Tag is ElementTreeItemViewModel item)
        {
            item.Element.IsVisible = !item.Element.IsVisible;
            item.NotifyVisibilityChanged();
            ElementVisibilityToggled?.Invoke(this, item.Element);
            DebugLogger.Instance.Log("DebugWindow", $"{item.DisplayName} visibility: {item.Element.IsVisible}");
        }
    }

    private void ToggleLock_Click(object sender, RoutedEventArgs e)
    {
        if (sender is System.Windows.Controls.Button btn && btn.Tag is ElementTreeItemViewModel item)
        {
            item.Element.IsLocked = !item.Element.IsLocked;
            item.NotifyLockChanged();
            ElementLockToggled?.Invoke(this, item.Element);
            DebugLogger.Instance.Log("DebugWindow", $"{item.DisplayName} locked: {item.Element.IsLocked}");
        }
    }

    private void ViewRawSvg_Click(object sender, RoutedEventArgs e)
    {
        if (_currentDocument is null)
        {
            System.Windows.MessageBox.Show("No document loaded.", "Raw SVG", System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Information);
            return;
        }
        
        var svgContent = GenerateSvgOutput();
        var dialog = new RawSvgDialog(svgContent) { Owner = this };
        dialog.ShowDialog();
    }

    private string GenerateSvgOutput()
    {
        if (_currentDocument is null) return string.Empty;
        
        var sb = new System.Text.StringBuilder();
        sb.AppendLine($"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{_currentDocument.Width}\" height=\"{_currentDocument.Height}\" viewBox=\"{_currentDocument.ViewBox}\">");
        
        if (!string.IsNullOrEmpty(_currentDocument.Title))
        {
            sb.AppendLine($"  <title>{_currentDocument.Title}</title>");
        }
        
        foreach (var element in _currentDocument.Elements)
        {
            var svgStr = element.ToSvgString();
            foreach (var line in svgStr.Split('\n'))
            {
                sb.AppendLine($"  {line}");
            }
        }
        
        sb.AppendLine("</svg>");
        return sb.ToString();
    }

    /// <summary>
    /// Selects an element in the tree view (called when canvas selection changes).
    /// </summary>
    public void SelectElementInTree(VectorElement? element)
    {
        if (element is null)
        {
            // Deselect
            return;
        }
        
        _suppressTreeSelection = true;
        try
        {
            var item = FindTreeItem(_elementTreeItems, element);
            if (item is not null)
            {
                // Expand parents and select
                SelectTreeViewItem(ElementTreeView, item);
            }
        }
        finally
        {
            _suppressTreeSelection = false;
        }
    }

    private static ElementTreeItemViewModel? FindTreeItem(IEnumerable<ElementTreeItemViewModel> items, VectorElement element)
    {
        foreach (var item in items)
        {
            if (item.Element == element)
                return item;
            
            var child = FindTreeItem(item.Children, element);
            if (child is not null)
                return child;
        }
        return null;
    }

    private static void SelectTreeViewItem(System.Windows.Controls.TreeView treeView, ElementTreeItemViewModel item)
    {
        // Find the TreeViewItem container and select it
        if (treeView.ItemContainerGenerator.ContainerFromItem(item) is System.Windows.Controls.TreeViewItem container)
        {
            container.IsSelected = true;
            container.BringIntoView();
        }
    }

    /// <summary>
    /// Event raised when an element is selected in the tree.
    /// </summary>
    public event EventHandler<VectorElement>? ElementSelectedInTree;

    /// <summary>
    /// Event raised when an element is hovered in the tree.
    /// </summary>
    public event EventHandler<VectorElement?>? ElementHovered;

    /// <summary>
    /// Event raised when element visibility is toggled.
    /// </summary>
    public event EventHandler<VectorElement>? ElementVisibilityToggled;

    /// <summary>
    /// Event raised when element lock state is toggled.
    /// </summary>
    public event EventHandler<VectorElement>? ElementLockToggled;

    #endregion

    #region Performance Tab

    private void OnPerformanceMetricsUpdated(object? sender, PerformanceSnapshot snapshot)
    {
        // Marshal to UI thread
        Dispatcher.BeginInvoke(() => UpdatePerformanceDisplay(snapshot));
    }

    private void UpdatePerformanceDisplay(PerformanceSnapshot s)
    {
        // Frame rate
        CurrentFpsText.Text = $"{s.Fps:F1}";
        AverageFpsText.Text = $"{s.AverageFps:F1}";
        MinFpsText.Text = $"{s.MinFps:F1}";
        MaxFpsText.Text = $"{s.MaxFps:F1}";
        TotalFramesText.Text = $"{s.TotalFrames:N0}";
        
        // Update FPS badge color based on performance
        FpsBadgeText.Text = $"{s.Fps:F0} FPS";
        FpsIndicator.Background = s.Fps switch
        {
            >= 55 => FindResource("GreenBrush") as Brush ?? Brushes.Green,
            >= 30 => FindResource("YellowBrush") as Brush ?? Brushes.Yellow,
            _ => FindResource("RedBrush") as Brush ?? Brushes.Red
        };
        
        // Render time
        LastRenderTimeText.Text = $"{s.LastRenderTimeMs:F2} ms";
        AverageRenderTimeText.Text = $"{s.AverageRenderTimeMs:F2} ms";
        MaxRenderTimeText.Text = $"{s.MaxRenderTimeMs:F2} ms";
        
        // Memory
        ProcessMemoryText.Text = PerformanceMetricsService.FormatBytes(s.MemoryUsedBytes);
        GcMemoryText.Text = PerformanceMetricsService.FormatBytes(s.GcMemoryBytes);
        
        // Document stats
        PerfElementCountText.Text = s.ElementCount.ToString();
        UndoStackText.Text = s.UndoStackSize.ToString();
        RedoStackText.Text = s.RedoStackSize.ToString();
    }

    private void ResetPerformance_Click(object sender, RoutedEventArgs e)
    {
        PerformanceMetricsService.Instance.Reset();
        DebugLogger.Instance.Info("DebugWindow", "Performance metrics reset");
    }

    private void CopyPerformanceInfo_Click(object sender, RoutedEventArgs e)
    {
        var text = PerformanceMetricsService.Instance.FormatAllInfo();
        Clipboard.SetText(text);
        DebugLogger.Instance.Info("DebugWindow", "Copied performance info to clipboard");
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

/// <summary>
/// ViewModel for elements in the Elements Inspector tree.
/// </summary>
public class ElementTreeItemViewModel : System.ComponentModel.INotifyPropertyChanged
{
    public VectorElement Element { get; }
    public ObservableCollection<ElementTreeItemViewModel> Children { get; } = [];
    
    public event System.ComponentModel.PropertyChangedEventHandler? PropertyChanged;

    public ElementTreeItemViewModel(VectorElement element)
    {
        Element = element;
    }

    public string TypeName => Element.GetType().Name.Replace("Svg", "");

    public string TypeIcon => Element switch
    {
        Bezier.Core.Models.Elements.SvgRect => "▢",
        Bezier.Core.Models.Elements.SvgEllipse => "○",
        Bezier.Core.Models.Elements.SvgCircle => "◯",
        Bezier.Core.Models.Elements.SvgLine => "╱",
        Bezier.Core.Models.Elements.SvgPath => "✒",
        Bezier.Core.Models.Elements.SvgPolygon => "⬠",
        Bezier.Core.Models.Elements.SvgPolyline => "⌇",
        Bezier.Core.Models.Elements.SvgText => "T",
        Bezier.Core.Models.Elements.SvgImage => "🖼",
        Bezier.Core.Models.Elements.SvgGroup => "📁",
        _ => "●"
    };

    public string DisplayName => string.IsNullOrEmpty(Element.Name) 
        ? $"{TypeName} ({Element.Id.ToString()[..8]})"
        : Element.Name;

    public string VisibilityIcon => Element.IsVisible ? "👁" : "👁‍🗨";
    public double VisibilityOpacity => Element.IsVisible ? 1.0 : 0.4;
    public string LockIcon => Element.IsLocked ? "🔒" : "🔓";

    public void NotifyVisibilityChanged()
    {
        PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(nameof(VisibilityIcon)));
        PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(nameof(VisibilityOpacity)));
    }

    public void NotifyLockChanged()
    {
        PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(nameof(LockIcon)));
    }
}
