using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using System.Xml;
using ICSharpCode.AvalonEdit.Highlighting;
using ICSharpCode.AvalonEdit.Highlighting.Xshd;
using Bezier.Desktop.Services;
using IOPath = System.IO.Path;
using IOFile = System.IO.File;

namespace Bezier.Desktop.Views;

public partial class MainWindowView : Window
{
    private SvgVisualEditor? _visualEditor;
    private double _zoomLevel = 1.0;
    
    // Drag state
    private SvgVisualEditor.ElementInfo? _selectedElement;
    private Point _dragStart;
    private bool _isDragging;
    private Rectangle? _selectionRect;

    public MainWindowView()
    {
        InitializeComponent();
        Loaded += MainWindowView_Loaded;
        CodeEditor.TextArea.Caret.PositionChanged += (s, e) => UpdateCursorPosition();
    }

    private void MainWindowView_Loaded(object sender, RoutedEventArgs e)
    {
        LoadCustomSyntaxHighlighting();
        UpdatePreview("");
    }

    private void LoadCustomSyntaxHighlighting()
    {
        try
        {
            var resourcePath = IOPath.Combine(AppDomain.CurrentDomain.BaseDirectory, "Resources", "VsCodeDarkXml.xshd");
            if (IOFile.Exists(resourcePath))
            {
                using var stream = IOFile.OpenRead(resourcePath);
                using var reader = new XmlTextReader(stream);
                CodeEditor.SyntaxHighlighting = HighlightingLoader.Load(reader, HighlightingManager.Instance);
            }
            else
            {
                CodeEditor.SyntaxHighlighting = HighlightingManager.Instance.GetDefinition("XML");
            }
        }
        catch
        {
            CodeEditor.SyntaxHighlighting = HighlightingManager.Instance.GetDefinition("XML");
        }
    }

    private void UpdateCursorPosition()
    {
        CursorPosition.Text = $"Ln {CodeEditor.TextArea.Caret.Line}, Col {CodeEditor.TextArea.Caret.Column}";
    }

    private void CodeEditor_TextChanged(object? sender, EventArgs e)
    {
        if (DataContext is ViewModels.MainViewModel vm)
        {
            vm.SourceCode = CodeEditor.Text;
            UpdatePreview(CodeEditor.Text);
        }
    }

    public void SetEditorText(string text)
    {
        CodeEditor.Text = text;
    }

    public void UpdatePreview(string svgContent)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(svgContent) || !svgContent.Contains("<svg"))
            {
                SvgPreview.Visibility = Visibility.Collapsed;
                PlaceholderText.Visibility = Visibility.Visible;
                if (StatusText != null) StatusText.Text = "Ready";
                return;
            }

            var tempFile = IOPath.Combine(IOPath.GetTempPath(), $"bezier_preview_{Guid.NewGuid():N}.svg");
            IOFile.WriteAllText(tempFile, svgContent);

            try
            {
                SvgPreview.Source = new Uri(tempFile);
                SvgPreview.Visibility = Visibility.Visible;
                PlaceholderText.Visibility = Visibility.Collapsed;
                if (StatusText != null) StatusText.Text = "Preview updated";
            }
            finally
            {
                Task.Delay(500).ContinueWith(_ => { try { IOFile.Delete(tempFile); } catch { } });
            }
        }
        catch (Exception ex)
        {
            if (StatusText != null) StatusText.Text = $"Preview error: {ex.Message}";
        }
    }

    #region View Mode Switching

    private void ViewMode_Changed(object sender, RoutedEventArgs e)
    {
        // Guard against event firing during XAML initialization
        if (CodeEditorPanel == null || VisualEditorPanel == null) return;
        
        if (CodeModeBtn.IsChecked == true)
        {
            CodeEditorPanel.Visibility = Visibility.Visible;
            VisualEditorPanel.Visibility = Visibility.Collapsed;
            if (PropertiesPanel != null) PropertiesPanel.Visibility = Visibility.Collapsed;
            if (StatusText != null) StatusText.Text = "Code editing mode";
        }
        else
        {
            CodeEditorPanel.Visibility = Visibility.Collapsed;
            VisualEditorPanel.Visibility = Visibility.Visible;
            RenderToVisualCanvas();
            if (StatusText != null) StatusText.Text = "Visual mode - Click to select, drag to move";
        }
    }

    private void RenderToVisualCanvas()
    {
        if (VisualSvgImage == null || VisualOverlay == null) return;
        if (string.IsNullOrWhiteSpace(CodeEditor?.Text)) return;
        
        try
        {
            _visualEditor ??= new SvgVisualEditor();
            
            if (_visualEditor.LoadSvg(CodeEditor.Text, out var image) && image != null)
            {
                VisualSvgImage.Source = image;
                VisualSvgImage.Width = _visualEditor.SvgWidth;
                VisualSvgImage.Height = _visualEditor.SvgHeight;
                
                VisualOverlay.Width = _visualEditor.SvgWidth;
                VisualOverlay.Height = _visualEditor.SvgHeight;
                VisualOverlay.Children.Clear();
                
                if (StatusText != null)
                    StatusText.Text = $"Visual mode: {_visualEditor.Elements.Count} elements";
            }
            else
            {
                if (StatusText != null)
                    StatusText.Text = "Could not render SVG in visual mode";
            }
        }
        catch (Exception ex)
        {
            if (StatusText != null)
                StatusText.Text = $"Render error: {ex.Message}";
        }
    }

    #endregion

    #region Visual Editor - Mouse Interaction

    private void VisualOverlay_MouseDown(object sender, MouseButtonEventArgs e)
    {
        if (_visualEditor == null || VisualOverlay == null) return;
        
        var pos = e.GetPosition(VisualOverlay);
        _selectedElement = _visualEditor.HitTest(pos);
        
        if (_selectedElement != null)
        {
            _dragStart = pos;
            _isDragging = true;
            VisualOverlay.CaptureMouse();
            
            ShowSelectionRect(_selectedElement.Bounds);
            UpdatePropertiesPanel();
            
            if (StatusText != null)
                StatusText.Text = $"Selected: {_selectedElement.Source.Name.LocalName} #{_selectedElement.Id}";
        }
        else
        {
            ClearSelection();
        }
        
        e.Handled = true;
    }

    private void VisualOverlay_MouseMove(object sender, MouseEventArgs e)
    {
        if (!_isDragging || _selectedElement == null || VisualOverlay == null) return;
        
        var pos = e.GetPosition(VisualOverlay);
        var dx = pos.X - _dragStart.X;
        var dy = pos.Y - _dragStart.Y;
        
        // Move the selection rectangle visually
        if (_selectionRect != null)
        {
            Canvas.SetLeft(_selectionRect, _selectedElement.Bounds.X + dx - 2);
            Canvas.SetTop(_selectionRect, _selectedElement.Bounds.Y + dy - 2);
        }
        
        // Update position display
        if (PosX != null && PosY != null)
        {
            PosX.Text = $"{_selectedElement.Bounds.X + dx:F1}";
            PosY.Text = $"{_selectedElement.Bounds.Y + dy:F1}";
        }
    }

    private void VisualOverlay_MouseUp(object sender, MouseButtonEventArgs e)
    {
        if (!_isDragging || _selectedElement == null || _visualEditor == null) return;
        
        VisualOverlay.ReleaseMouseCapture();
        
        var pos = e.GetPosition(VisualOverlay);
        var dx = pos.X - _dragStart.X;
        var dy = pos.Y - _dragStart.Y;
        
        // Only update if actually moved
        if (Math.Abs(dx) > 1 || Math.Abs(dy) > 1)
        {
            var newSvg = _visualEditor.MoveElement(_selectedElement, dx, dy);
            if (!string.IsNullOrEmpty(newSvg))
            {
                // Update the code editor
                CodeEditor.Text = newSvg;
                
                // Refresh the visual
                RenderToVisualCanvas();
                
                if (StatusText != null)
                    StatusText.Text = $"Moved {_selectedElement.Id} by ({dx:F0}, {dy:F0})";
            }
        }
        
        _isDragging = false;
    }

    private void ShowSelectionRect(Rect bounds)
    {
        ClearSelection();
        
        if (VisualOverlay == null) return;
        
        _selectionRect = new Rectangle
        {
            Width = bounds.Width + 4,
            Height = bounds.Height + 4,
            Stroke = new SolidColorBrush(Color.FromRgb(0, 120, 212)),
            StrokeThickness = 2,
            StrokeDashArray = new DoubleCollection { 4, 2 },
            Fill = new SolidColorBrush(Color.FromArgb(30, 0, 120, 212))
        };
        
        Canvas.SetLeft(_selectionRect, bounds.X - 2);
        Canvas.SetTop(_selectionRect, bounds.Y - 2);
        
        VisualOverlay.Children.Add(_selectionRect);
    }

    private void ClearSelection()
    {
        if (_selectionRect != null && VisualOverlay != null)
        {
            VisualOverlay.Children.Remove(_selectionRect);
            _selectionRect = null;
        }
        _selectedElement = null;
        if (PropertiesPanel != null) PropertiesPanel.Visibility = Visibility.Collapsed;
    }

    private void UpdatePropertiesPanel()
    {
        if (_selectedElement != null && PropertiesPanel != null)
        {
            PropertiesPanel.Visibility = Visibility.Visible;
            if (SelectedElementType != null)
                SelectedElementType.Text = _selectedElement.Source.Name.LocalName.ToUpper();
            if (SelectedElementId != null)
                SelectedElementId.Text = $"#{_selectedElement.Id}";
            if (PosX != null)
                PosX.Text = $"{_selectedElement.Bounds.X:F1}";
            if (PosY != null)
                PosY.Text = $"{_selectedElement.Bounds.Y:F1}";
        }
    }

    #endregion

    #region Zoom Controls

    private void ZoomIn_Click(object sender, RoutedEventArgs e)
    {
        _zoomLevel = Math.Min(_zoomLevel + 0.25, 4.0);
        ApplyZoom();
    }

    private void ZoomOut_Click(object sender, RoutedEventArgs e)
    {
        _zoomLevel = Math.Max(_zoomLevel - 0.25, 0.25);
        ApplyZoom();
    }

    private void ZoomFit_Click(object sender, RoutedEventArgs e)
    {
        _zoomLevel = 1.0;
        ApplyZoom();
    }

    private void ApplyZoom()
    {
        if (CanvasScale != null)
        {
            CanvasScale.ScaleX = _zoomLevel;
            CanvasScale.ScaleY = _zoomLevel;
        }
        if (ZoomLevel != null)
            ZoomLevel.Text = $"{(int)(_zoomLevel * 100)}%";
    }

    #endregion

    #region Code Editor Actions

    private void CopyCode_Click(object sender, RoutedEventArgs e)
    {
        Clipboard.SetText(string.IsNullOrEmpty(CodeEditor.SelectedText) ? CodeEditor.Text : CodeEditor.SelectedText);
        if (StatusText != null) StatusText.Text = "Copied to clipboard";
    }

    private void PasteCode_Click(object sender, RoutedEventArgs e)
    {
        if (Clipboard.ContainsText())
        {
            CodeEditor.Text = Clipboard.GetText();
            if (StatusText != null) StatusText.Text = "Pasted from clipboard";
        }
    }

    private void FormatCode_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var xml = System.Xml.Linq.XDocument.Parse(CodeEditor.Text);
            CodeEditor.Text = xml.ToString();
            if (StatusText != null) StatusText.Text = "Code formatted";
        }
        catch
        {
            if (StatusText != null) StatusText.Text = "Could not format - invalid XML";
        }
    }

    private void RefreshPreview_Click(object sender, RoutedEventArgs e)
    {
        UpdatePreview(CodeEditor.Text);
        if (VisualModeBtn?.IsChecked == true)
        {
            RenderToVisualCanvas();
        }
    }

    #endregion
}
