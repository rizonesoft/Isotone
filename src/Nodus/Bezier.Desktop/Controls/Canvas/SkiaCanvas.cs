namespace Bezier.Desktop.Controls.Canvas;

using System.Windows;
using System.Windows.Input;
using Bezier.Core.Models;
using Bezier.Desktop.Services;
using SkiaSharp;
using SkiaSharp.Views.Desktop;
using SkiaSharp.Views.WPF;

/// <summary>
/// WPF control for rendering vector documents using SkiaSharp.
/// Provides pan, zoom, grid, rulers, and element rendering.
/// </summary>
public class SkiaCanvas : SKElement
{
    private VectorDocument? _document;
    private readonly SkiaRenderer _renderer;
    private readonly CanvasState _state;
    
    // Mouse interaction state
    private Point _lastMousePosition;
    private bool _isPanning;
    private bool _isSpaceDown;

    /// <summary>
    /// The vector document being rendered.
    /// </summary>
    public static readonly DependencyProperty DocumentProperty =
        DependencyProperty.Register(
            nameof(Document),
            typeof(VectorDocument),
            typeof(SkiaCanvas),
            new PropertyMetadata(null, OnDocumentChanged));

    /// <summary>
    /// Whether to show the grid.
    /// </summary>
    public static readonly DependencyProperty ShowGridProperty =
        DependencyProperty.Register(
            nameof(ShowGrid),
            typeof(bool),
            typeof(SkiaCanvas),
            new PropertyMetadata(true, OnRenderPropertyChanged));

    /// <summary>
    /// Whether to show rulers.
    /// </summary>
    public static readonly DependencyProperty ShowRulersProperty =
        DependencyProperty.Register(
            nameof(ShowRulers),
            typeof(bool),
            typeof(SkiaCanvas),
            new PropertyMetadata(true, OnRenderPropertyChanged));

    /// <summary>
    /// Whether to render in outline mode (wireframe).
    /// </summary>
    public static readonly DependencyProperty OutlineModeProperty =
        DependencyProperty.Register(
            nameof(OutlineMode),
            typeof(bool),
            typeof(SkiaCanvas),
            new PropertyMetadata(false, OnRenderPropertyChanged));

    /// <summary>
    /// Whether to show pixel preview at high zoom levels.
    /// </summary>
    public static readonly DependencyProperty PixelPreviewProperty =
        DependencyProperty.Register(
            nameof(PixelPreview),
            typeof(bool),
            typeof(SkiaCanvas),
            new PropertyMetadata(false, OnRenderPropertyChanged));

    /// <summary>
    /// Background type for the canvas.
    /// </summary>
    public static readonly DependencyProperty BackgroundTypeProperty =
        DependencyProperty.Register(
            nameof(BackgroundType),
            typeof(CanvasBackgroundType),
            typeof(SkiaCanvas),
            new PropertyMetadata(CanvasBackgroundType.Checkerboard, OnRenderPropertyChanged));

    /// <summary>
    /// Solid background color when BackgroundType is SolidColor.
    /// </summary>
    public static readonly DependencyProperty BackgroundColorProperty =
        DependencyProperty.Register(
            nameof(BackgroundColor),
            typeof(SKColor),
            typeof(SkiaCanvas),
            new PropertyMetadata(SKColors.White, OnRenderPropertyChanged));

    public VectorDocument? Document
    {
        get => (VectorDocument?)GetValue(DocumentProperty);
        set => SetValue(DocumentProperty, value);
    }

    public bool ShowGrid
    {
        get => (bool)GetValue(ShowGridProperty);
        set => SetValue(ShowGridProperty, value);
    }

    public bool ShowRulers
    {
        get => (bool)GetValue(ShowRulersProperty);
        set => SetValue(ShowRulersProperty, value);
    }

    public bool OutlineMode
    {
        get => (bool)GetValue(OutlineModeProperty);
        set => SetValue(OutlineModeProperty, value);
    }

    public bool PixelPreview
    {
        get => (bool)GetValue(PixelPreviewProperty);
        set => SetValue(PixelPreviewProperty, value);
    }

    public CanvasBackgroundType BackgroundType
    {
        get => (CanvasBackgroundType)GetValue(BackgroundTypeProperty);
        set => SetValue(BackgroundTypeProperty, value);
    }

    public SKColor BackgroundColor
    {
        get => (SKColor)GetValue(BackgroundColorProperty);
        set => SetValue(BackgroundColorProperty, value);
    }

    /// <summary>
    /// Current zoom level (1.0 = 100%).
    /// </summary>
    public double ZoomLevel => _state.Zoom;

    /// <summary>
    /// Current pan offset.
    /// </summary>
    public SKPoint PanOffset => _state.PanOffset;

    /// <summary>
    /// Event raised when zoom level changes.
    /// </summary>
    public event EventHandler<double>? ZoomChanged;

    /// <summary>
    /// Event raised when cursor position changes on the canvas.
    /// </summary>
    public event EventHandler<SKPoint>? CursorPositionChanged;

    public SkiaCanvas()
    {
        _state = new CanvasState();
        _renderer = new SkiaRenderer();
        
        Focusable = true;
        ClipToBounds = true;
        
        // Subscribe to state changes
        _state.StateChanged += (_, _) => InvalidateVisual();
    }

    protected override void OnPaintSurface(SKPaintSurfaceEventArgs e)
    {
        base.OnPaintSurface(e);
        
        var canvas = e.Surface.Canvas;
        var info = e.Info;
        
        canvas.Clear(SKColors.Transparent);
        
        // Render background (outside of artboard)
        RenderCanvasBackground(canvas, info);
        
        // Apply view transform (pan and zoom)
        canvas.Save();
        canvas.Translate(_state.PanOffset.X, _state.PanOffset.Y);
        canvas.Scale((float)_state.Zoom);
        
        // Render document artboard background
        if (_document is not null)
        {
            RenderArtboardBackground(canvas);
        }
        
        // Render grid if enabled
        if (ShowGrid && _document is not null)
        {
            _renderer.RenderGrid(canvas, _document, _state.Zoom);
        }
        
        // Render document elements
        if (_document is not null)
        {
            _renderer.RenderDocument(canvas, _document, OutlineMode, PixelPreview && _state.Zoom >= 8);
        }
        
        canvas.Restore();
        
        // Render rulers on top (not affected by pan/zoom transform)
        if (ShowRulers)
        {
            _renderer.RenderRulers(canvas, info, _state, _document);
        }
    }

    private void RenderCanvasBackground(SKCanvas canvas, SKImageInfo info)
    {
        using var paint = new SKPaint();
        
        switch (BackgroundType)
        {
            case CanvasBackgroundType.Checkerboard:
                _renderer.RenderCheckerboard(canvas, info);
                break;
                
            case CanvasBackgroundType.SolidColor:
                paint.Color = BackgroundColor;
                canvas.DrawRect(0, 0, info.Width, info.Height, paint);
                break;
                
            case CanvasBackgroundType.Transparent:
                // Already cleared to transparent
                break;
        }
    }

    private void RenderArtboardBackground(SKCanvas canvas)
    {
        if (_document is null) return;
        
        using var paint = new SKPaint
        {
            Color = SKColors.White,
            Style = SKPaintStyle.Fill
        };
        
        // Draw artboard (document) background
        canvas.DrawRect(0, 0, (float)_document.Width, (float)_document.Height, paint);
        
        // Draw artboard border
        using var borderPaint = new SKPaint
        {
            Color = new SKColor(180, 180, 180),
            Style = SKPaintStyle.Stroke,
            StrokeWidth = 1f / (float)_state.Zoom,
            IsAntialias = true
        };
        canvas.DrawRect(0, 0, (float)_document.Width, (float)_document.Height, borderPaint);
    }

    #region Mouse Handling

    protected override void OnMouseWheel(MouseWheelEventArgs e)
    {
        base.OnMouseWheel(e);
        
        var position = e.GetPosition(this);
        var skPoint = new SKPoint((float)position.X, (float)position.Y);
        
        // Zoom centered on cursor position
        var zoomFactor = e.Delta > 0 ? 1.1 : 0.9;
        _state.ZoomAtPoint(zoomFactor, skPoint);
        
        ZoomChanged?.Invoke(this, _state.Zoom);
        e.Handled = true;
    }

    protected override void OnMouseDown(MouseButtonEventArgs e)
    {
        base.OnMouseDown(e);
        
        Focus();
        _lastMousePosition = e.GetPosition(this);
        
        // Middle mouse button or space+left click for panning
        if (e.MiddleButton == MouseButtonState.Pressed || 
            (_isSpaceDown && e.LeftButton == MouseButtonState.Pressed))
        {
            _isPanning = true;
            CaptureMouse();
            Cursor = Cursors.Hand;
            e.Handled = true;
        }
    }

    protected override void OnMouseMove(MouseEventArgs e)
    {
        base.OnMouseMove(e);
        
        var position = e.GetPosition(this);
        
        // Report cursor position in document coordinates
        var docPoint = _state.ScreenToDocument(new SKPoint((float)position.X, (float)position.Y));
        CursorPositionChanged?.Invoke(this, docPoint);
        
        if (_isPanning)
        {
            var delta = position - _lastMousePosition;
            _state.Pan((float)delta.X, (float)delta.Y);
            _lastMousePosition = position;
            e.Handled = true;
        }
        else
        {
            _lastMousePosition = position;
        }
    }

    protected override void OnMouseUp(MouseButtonEventArgs e)
    {
        base.OnMouseUp(e);
        
        if (_isPanning)
        {
            _isPanning = false;
            ReleaseMouseCapture();
            Cursor = _isSpaceDown ? Cursors.Hand : Cursors.Arrow;
            e.Handled = true;
        }
    }

    protected override void OnKeyDown(KeyEventArgs e)
    {
        base.OnKeyDown(e);
        
        if (e.Key == Key.Space && !_isSpaceDown)
        {
            _isSpaceDown = true;
            Cursor = Cursors.Hand;
            e.Handled = true;
        }
    }

    protected override void OnKeyUp(KeyEventArgs e)
    {
        base.OnKeyUp(e);
        
        if (e.Key == Key.Space)
        {
            _isSpaceDown = false;
            if (!_isPanning)
            {
                Cursor = Cursors.Arrow;
            }
            e.Handled = true;
        }
    }

    protected override void OnLostFocus(RoutedEventArgs e)
    {
        base.OnLostFocus(e);
        _isSpaceDown = false;
        _isPanning = false;
        Cursor = Cursors.Arrow;
    }

    #endregion

    #region Public Methods

    /// <summary>
    /// Sets the zoom level.
    /// </summary>
    public void SetZoom(double zoom)
    {
        _state.SetZoom(zoom);
        ZoomChanged?.Invoke(this, _state.Zoom);
    }

    /// <summary>
    /// Fits the document to the viewport.
    /// </summary>
    public void FitToWindow()
    {
        if (_document is null || ActualWidth <= 0 || ActualHeight <= 0) return;
        
        var rulerOffset = ShowRulers ? 24f : 0f;
        var availableWidth = (float)ActualWidth - rulerOffset;
        var availableHeight = (float)ActualHeight - rulerOffset;
        
        var scaleX = availableWidth / (float)_document.Width;
        var scaleY = availableHeight / (float)_document.Height;
        var scale = Math.Min(scaleX, scaleY) * 0.9; // 90% to add margin
        
        _state.SetZoom(scale);
        
        // Center the document
        var docWidth = (float)_document.Width * (float)scale;
        var docHeight = (float)_document.Height * (float)scale;
        var offsetX = rulerOffset + (availableWidth - docWidth) / 2;
        var offsetY = rulerOffset + (availableHeight - docHeight) / 2;
        
        _state.SetPan(offsetX, offsetY);
        ZoomChanged?.Invoke(this, _state.Zoom);
    }

    /// <summary>
    /// Resets zoom to 100% and centers the document.
    /// </summary>
    public void ResetView()
    {
        _state.SetZoom(1.0);
        
        if (_document is not null && ActualWidth > 0 && ActualHeight > 0)
        {
            var rulerOffset = ShowRulers ? 24f : 0f;
            var offsetX = rulerOffset + ((float)ActualWidth - rulerOffset - (float)_document.Width) / 2;
            var offsetY = rulerOffset + ((float)ActualHeight - rulerOffset - (float)_document.Height) / 2;
            _state.SetPan(offsetX, offsetY);
        }
        
        ZoomChanged?.Invoke(this, _state.Zoom);
    }

    /// <summary>
    /// Forces a redraw of the canvas.
    /// </summary>
    public void Redraw() => InvalidateVisual();

    #endregion

    private static void OnDocumentChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is SkiaCanvas canvas)
        {
            canvas._document = e.NewValue as VectorDocument;
            canvas.FitToWindow();
            canvas.InvalidateVisual();
        }
    }

    private static void OnRenderPropertyChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is SkiaCanvas canvas)
        {
            canvas.InvalidateVisual();
        }
    }
}

/// <summary>
/// Background type options for the canvas.
/// </summary>
public enum CanvasBackgroundType
{
    /// <summary>Checkerboard pattern (transparency indicator).</summary>
    Checkerboard,
    /// <summary>Solid color background.</summary>
    SolidColor,
    /// <summary>Transparent background.</summary>
    Transparent
}
