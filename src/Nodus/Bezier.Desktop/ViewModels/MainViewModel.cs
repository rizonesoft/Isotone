using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Win32;
using System.IO;
using System.Text;
using Bezier.Desktop.Services;

namespace Bezier.Desktop.ViewModels;

public partial class MainViewModel : ObservableObject
{
    private readonly ISvgOptimizerService _optimizer;

    [ObservableProperty]
    private string _sourceCode = "";

    [ObservableProperty]
    private string _originalSize = "0 KB";

    [ObservableProperty]
    private string _optimizedSize = "0 KB";

    [ObservableProperty]
    private string _savingsPercent = "0%";

    // Optimization Options
    [ObservableProperty]
    private bool _removeComments = true;

    [ObservableProperty]
    private bool _removeMetadata = true;

    [ObservableProperty]
    private bool _removeEditorData = true;

    [ObservableProperty]
    private bool _removeEmptyGroups = true;

    [ObservableProperty]
    private bool _collapseGroups = false;

    [ObservableProperty]
    private bool _roundNumbers = false;

    [ObservableProperty]
    private bool _minifyOutput = false;

    private string _originalContent = "";
    private long _originalBytes = 0;

    public MainViewModel()
    {
        _optimizer = new SvgOptimizerService();
    }

    [RelayCommand]
    private void OpenFile()
    {
        var dialog = new OpenFileDialog
        {
            Filter = "SVG Files (*.svg)|*.svg|All Files (*.*)|*.*",
            Title = "Open SVG File"
        };

        if (dialog.ShowDialog() == true)
        {
            try
            {
                _originalContent = File.ReadAllText(dialog.FileName);
                _originalBytes = new FileInfo(dialog.FileName).Length;
                
                SourceCode = _originalContent;
                UpdateStats(_originalContent);
                
                // Update the editor via the view
                if (App.Current.MainWindow is Views.MainWindowView view)
                {
                    view.SetEditorText(_originalContent);
                }
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Error opening file: {ex.Message}", "Error", 
                    System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Error);
            }
        }
    }

    [RelayCommand]
    private void SaveFile()
    {
        var dialog = new SaveFileDialog
        {
            Filter = "SVG Files (*.svg)|*.svg",
            Title = "Save Optimized SVG",
            FileName = "optimized.svg"
        };

        if (dialog.ShowDialog() == true)
        {
            try
            {
                File.WriteAllText(dialog.FileName, SourceCode, Encoding.UTF8);
                System.Windows.MessageBox.Show("File saved successfully!", "Success", 
                    System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show($"Error saving file: {ex.Message}", "Error", 
                    System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Error);
            }
        }
    }

    [RelayCommand]
    private void Optimize()
    {
        if (string.IsNullOrWhiteSpace(SourceCode))
        {
            System.Windows.MessageBox.Show("Please open an SVG file first.", "No Content", 
                System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Warning);
            return;
        }

        var options = new OptimizationOptions
        {
            RemoveComments = RemoveComments,
            RemoveMetadata = RemoveMetadata,
            RemoveEditorData = RemoveEditorData,
            RemoveEmptyGroups = RemoveEmptyGroups,
            CollapseGroups = CollapseGroups,
            RoundNumbers = RoundNumbers,
            Minify = MinifyOutput
        };

        var optimized = _optimizer.Optimize(SourceCode, options);
        SourceCode = optimized;
        
        // Update the editor
        if (App.Current.MainWindow is Views.MainWindowView view)
        {
            view.SetEditorText(optimized);
        }

        UpdateStats(optimized);
    }

    [RelayCommand]
    private void RefreshPreview()
    {
        // The preview updates automatically on text change
    }

    private void UpdateStats(string content)
    {
        var currentBytes = Encoding.UTF8.GetByteCount(content);
        
        OriginalSize = FormatBytes(_originalBytes > 0 ? _originalBytes : currentBytes);
        OptimizedSize = FormatBytes(currentBytes);
        
        if (_originalBytes > 0 && currentBytes < _originalBytes)
        {
            var savings = (1.0 - (double)currentBytes / _originalBytes) * 100;
            SavingsPercent = $"-{savings:F1}%";
        }
        else
        {
            SavingsPercent = "0%";
        }
    }

    private static string FormatBytes(long bytes)
    {
        if (bytes < 1024) return $"{bytes} B";
        if (bytes < 1024 * 1024) return $"{bytes / 1024.0:F1} KB";
        return $"{bytes / (1024.0 * 1024):F2} MB";
    }
}
