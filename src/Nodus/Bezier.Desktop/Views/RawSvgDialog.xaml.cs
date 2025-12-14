using System.IO;
using System.Windows;
using Bezier.Core.Services;
using Microsoft.Win32;
using Wpf.Ui.Controls;

namespace Bezier.Desktop.Views;

/// <summary>
/// Dialog for viewing and exporting raw SVG output.
/// </summary>
public partial class RawSvgDialog : FluentWindow
{
    private readonly string _svgContent;

    public RawSvgDialog(string svgContent)
    {
        _svgContent = svgContent;
        InitializeComponent();
        SvgTextBox.Text = svgContent;
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
        Close();
    }

    private void CopyToClipboard_Click(object sender, RoutedEventArgs e)
    {
        Clipboard.SetText(_svgContent);
        DebugLogger.Instance.Info("RawSvgDialog", "SVG content copied to clipboard");
    }

    private void SaveToFile_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new SaveFileDialog
        {
            Filter = "SVG Files (*.svg)|*.svg|All Files (*.*)|*.*",
            DefaultExt = ".svg",
            FileName = $"export-{DateTime.Now:yyyyMMdd-HHmmss}.svg"
        };

        if (dialog.ShowDialog() == true)
        {
            File.WriteAllText(dialog.FileName, _svgContent);
            DebugLogger.Instance.Info("RawSvgDialog", $"SVG saved to {dialog.FileName}");
        }
    }
}




