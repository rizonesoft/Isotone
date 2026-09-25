namespace Imago.UI.Controls;

using System.Windows;
using System.Windows.Controls;
using SkiaSharp;

/// <summary>
/// Container control that combines the image canvas with rulers.
/// </summary>
public partial class CanvasContainer : UserControl
{
    public static readonly DependencyProperty ShowRulersProperty =
        DependencyProperty.Register(nameof(ShowRulers), typeof(bool), typeof(CanvasContainer),
            new PropertyMetadata(true, OnShowRulersChanged));

    public static readonly DependencyProperty ZoomProperty =
        DependencyProperty.Register(nameof(Zoom), typeof(double), typeof(CanvasContainer),
            new PropertyMetadata(1.0));

    public bool ShowRulers
    {
        get => (bool)GetValue(ShowRulersProperty);
        set => SetValue(ShowRulersProperty, value);
    }

    public double Zoom
    {
        get => (double)GetValue(ZoomProperty);
        set => SetValue(ZoomProperty, value);
    }

    public ImageCanvas ImageCanvas => Canvas;

    public event EventHandler<CanvasMouseEventArgs>? CanvasMouseMove;
    public event EventHandler<CanvasMouseEventArgs>? CanvasMouseDown;
    public event EventHandler<CanvasMouseEventArgs>? CanvasMouseUp;

    public CanvasContainer()
    {
        InitializeComponent();

        Canvas.CanvasMouseMove += OnCanvasMouseMove;
        Canvas.CanvasMouseDown += (s, e) => CanvasMouseDown?.Invoke(this, e);
        Canvas.CanvasMouseUp += (s, e) => CanvasMouseUp?.Invoke(this, e);
        Canvas.ViewportChanged += OnViewportChanged;

        UpdateRulerVisibility();
    }

    public void LoadImage(string filePath)
    {
        Canvas.LoadImage(filePath);
        UpdateRulers();
    }

    public void LoadImage(SKBitmap bitmap)
    {
        Canvas.LoadImage(bitmap);
        UpdateRulers();
    }

    public void ZoomToFit() => Canvas.ZoomToFit();

    public void ZoomToActual() => Canvas.ZoomToActual();

    public void CenterDocument() => Canvas.CenterDocument();

    private void OnCanvasMouseMove(object? sender, CanvasMouseEventArgs e)
    {
        // Update ruler cursor positions
        HorizontalRuler.CursorPosition = e.DocumentX;
        VerticalRuler.CursorPosition = e.DocumentY;

        CanvasMouseMove?.Invoke(this, e);
    }

    private void OnViewportChanged(object? sender, EventArgs e)
    {
        UpdateRulers();
    }

    private void UpdateRulers()
    {
        HorizontalRuler.Zoom = Canvas.Zoom;
        HorizontalRuler.Offset = Canvas.PanX;
        HorizontalRuler.DocumentSize = Canvas.DocumentWidth;

        VerticalRuler.Zoom = Canvas.Zoom;
        VerticalRuler.Offset = Canvas.PanY;
        VerticalRuler.DocumentSize = Canvas.DocumentHeight;

        Zoom = Canvas.Zoom;
    }

    private void UpdateRulerVisibility()
    {
        var visibility = ShowRulers ? Visibility.Visible : Visibility.Collapsed;
        HorizontalRuler.Visibility = visibility;
        VerticalRuler.Visibility = visibility;
    }

    private static void OnShowRulersChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        (d as CanvasContainer)?.UpdateRulerVisibility();
    }
}
