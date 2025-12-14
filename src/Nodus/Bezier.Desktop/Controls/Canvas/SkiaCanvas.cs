namespace Bezier.Desktop.Controls.Canvas;

using System.Diagnostics;
using System.Windows;
using System.Windows.Input;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Services;
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
    private SKPoint _currentCursorDocPosition;
    private SKPoint _currentCursorScreenPosition;
    
    // Animation state for smooth zoom
    private System.Windows.Threading.DispatcherTimer? _zoomAnimationTimer;
    private double _targetZoom;
    private double _zoomAnimationStartValue;
    private DateTime _zoomAnimationStartTime;
    private SKPoint _zoomCenter;
    private const double ZoomAnimationDurationMs = 150;
    
    // Performance tracking
    private readonly Stopwatch _renderStopwatch = new();

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
    /// ToolManager for handling tool input.
    /// </summary>
    public static readonly DependencyProperty ToolManagerProperty =
        DependencyProperty.Register(
            nameof(ToolManager),
            typeof(ToolManager),
            typeof(SkiaCanvas),
            new PropertyMetadata(null, OnToolManagerChanged));

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

    public ToolManager? ToolManager
    {
        get => (ToolManager?)GetValue(ToolManagerProperty);
        set => SetValue(ToolManagerProperty, value);
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
        
        // Use device-independent pixels so coordinates match WPF mouse events
        IgnorePixelScaling = true;
        
        Focusable = true;
        ClipToBounds = true;
        
        // Subscribe to state changes
        _state.StateChanged += (_, _) => InvalidateVisual();
    }

    protected override void OnPaintSurface(SKPaintSurfaceEventArgs e)
    {
        _renderStopwatch.Restart();
        
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
        
        // Render tool overlays (selection handles, guides, etc.) while still in document coordinates
        if (ToolManager?.ActiveTool is not null)
        {
            canvas.Save();
            canvas.Translate(_state.PanOffset.X, _state.PanOffset.Y);
            canvas.Scale((float)_state.Zoom);
            
            var renderContext = new SkiaToolRenderContext(canvas, _state.Zoom, _renderer);
            ToolManager.RenderOverlay(renderContext);
            
            canvas.Restore();
        }
        
        // Render rulers on top (not affected by pan/zoom transform)
        if (ShowRulers)
        {
            _renderer.RenderRulers(canvas, info, _state, _document, _currentCursorScreenPosition);
        }
        
        // Record render time for performance monitoring
        _renderStopwatch.Stop();
        PerformanceMetricsService.Instance.RecordRenderTime(_renderStopwatch.Elapsed.TotalMilliseconds);
        
        // Update element count
        if (_document is not null)
        {
            PerformanceMetricsService.Instance.UpdateElementCount(_document.Elements.Count);
        }
    }

    private void RenderCanvasBackground(SKCanvas canvas, SKImageInfo info)
    {
        using var paint = new SKPaint();
        
        switch (BackgroundType)
        {
            case CanvasBackgroundType.Checkerboard:
                // Illustrator-style: dark gray canvas, white artboard
                paint.Color = new SKColor(45, 45, 50); // Dark gray matching Catppuccin Crust
                canvas.DrawRect(0, 0, info.Width, info.Height, paint);
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
        _zoomCenter = new SKPoint((float)position.X, (float)position.Y);
        
        // Calculate target zoom with smooth animation
        var zoomFactor = e.Delta > 0 ? 1.25 : 0.8;
        var newTargetZoom = (_zoomAnimationTimer?.IsEnabled == true ? _targetZoom : _state.Zoom) * zoomFactor;
        newTargetZoom = Math.Clamp(newTargetZoom, CanvasState.MinZoom, CanvasState.MaxZoom);
        
        StartZoomAnimation(newTargetZoom);
        e.Handled = true;
    }

    private void StartZoomAnimation(double targetZoom)
    {
        _targetZoom = targetZoom;
        _zoomAnimationStartValue = _state.Zoom;
        _zoomAnimationStartTime = DateTime.Now;
        
        if (_zoomAnimationTimer is null)
        {
            _zoomAnimationTimer = new System.Windows.Threading.DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(16) // ~60fps
            };
            _zoomAnimationTimer.Tick += OnZoomAnimationTick;
        }
        
        _zoomAnimationTimer.Start();
    }

    private void OnZoomAnimationTick(object? sender, EventArgs e)
    {
        var elapsed = (DateTime.Now - _zoomAnimationStartTime).TotalMilliseconds;
        var progress = Math.Min(elapsed / ZoomAnimationDurationMs, 1.0);
        
        // Ease-out cubic for smooth deceleration
        var easedProgress = 1 - Math.Pow(1 - progress, 3);
        
        var currentZoom = _zoomAnimationStartValue + (_targetZoom - _zoomAnimationStartValue) * easedProgress;
        
        // Calculate zoom factor relative to current zoom
        var zoomFactor = currentZoom / _state.Zoom;
        _state.ZoomAtPoint(zoomFactor, _zoomCenter);
        
        ZoomChanged?.Invoke(this, _state.Zoom);
        
        if (progress >= 1.0)
        {
            _zoomAnimationTimer?.Stop();
        }
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
            return;
        }
        
        // Forward to ToolManager for tool handling
        if (e.LeftButton == MouseButtonState.Pressed && ToolManager is not null)
        {
            var screenPos = new SKPoint((float)_lastMousePosition.X, (float)_lastMousePosition.Y);
            var docPos = _state.ScreenToDocument(screenPos);
            System.Diagnostics.Debug.WriteLine($"[SelectDebug] WPF pos: {_lastMousePosition}, Doc pos: ({docPos.X:F1}, {docPos.Y:F1}), PanOffset: {_state.PanOffset}, Zoom: {_state.Zoom:F2}");
            
            var modifiers = GetKeyModifiers();
            if (ToolManager.OnMouseDown(new ToolPoint(docPos.X, docPos.Y), modifiers))
            {
                CaptureMouse();
                e.Handled = true;
            }
        }
    }

    protected override void OnMouseMove(MouseEventArgs e)
    {
        base.OnMouseMove(e);
        
        var position = e.GetPosition(this);
        _currentCursorScreenPosition = new SKPoint((float)position.X, (float)position.Y);
        
        // Report cursor position in document coordinates
        _currentCursorDocPosition = _state.ScreenToDocument(_currentCursorScreenPosition);
        CursorPositionChanged?.Invoke(this, _currentCursorDocPosition);
        
        // Invalidate to update cursor indicators on rulers
        if (ShowRulers)
        {
            InvalidateVisual();
        }
        
        if (_isPanning)
        {
            var delta = position - _lastMousePosition;
            _state.Pan((float)delta.X, (float)delta.Y);
            _lastMousePosition = position;
            e.Handled = true;
        }
        else if (e.LeftButton == MouseButtonState.Pressed && ToolManager is not null)
        {
            var modifiers = GetKeyModifiers();
            ToolManager.OnMouseMove(new ToolPoint(_currentCursorDocPosition.X, _currentCursorDocPosition.Y), modifiers);
            _lastMousePosition = position;
            UpdateToolCursor();
        }
        else
        {
            _lastMousePosition = position;
            // Update cursor on hover (for resize handles, etc.)
            if (ToolManager is not null)
            {
                var modifiers = GetKeyModifiers();
                ToolManager.OnMouseMove(new ToolPoint(_currentCursorDocPosition.X, _currentCursorDocPosition.Y), modifiers);
                UpdateToolCursor();
            }
        }
    }
    
    private void UpdateToolCursor()
    {
        if (_isPanning || _isSpaceDown) return;
        
        var toolCursor = ToolManager?.ActiveTool?.Cursor ?? ToolCursor.Arrow;
        Cursor = toolCursor switch
        {
            ToolCursor.Arrow => Cursors.Arrow,
            ToolCursor.Cross => Cursors.Cross,
            ToolCursor.Hand => Cursors.Hand,
            ToolCursor.Move => Cursors.SizeAll,
            ToolCursor.SizeNWSE => Cursors.SizeNWSE,
            ToolCursor.SizeNESW => Cursors.SizeNESW,
            ToolCursor.SizeWE => Cursors.SizeWE,
            ToolCursor.SizeNS => Cursors.SizeNS,
            ToolCursor.Rotate => Cursors.Hand, // WPF doesn't have rotate cursor, using hand as fallback
            ToolCursor.Text => Cursors.IBeam,
            ToolCursor.Pen => Cursors.Pen,
            ToolCursor.Eyedropper => Cursors.Cross,
            ToolCursor.ZoomIn => Cursors.Arrow,
            ToolCursor.ZoomOut => Cursors.Arrow,
            ToolCursor.None => Cursors.None,
            _ => Cursors.Arrow
        };
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
            return;
        }
        
        // Forward to ToolManager
        if (ToolManager is not null)
        {
            var position = e.GetPosition(this);
            var screenPos = new SKPoint((float)position.X, (float)position.Y);
            var docPos = _state.ScreenToDocument(screenPos);
            var modifiers = GetKeyModifiers();
            ToolManager.OnMouseUp(new ToolPoint(docPos.X, docPos.Y), modifiers);
            ReleaseMouseCapture();
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

    private static void OnToolManagerChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is SkiaCanvas canvas)
        {
            // Subscribe to redraw requests from the tool manager
            if (e.OldValue is ToolManager oldManager)
            {
                oldManager.RedrawRequested -= canvas.OnToolManagerRedrawRequested;
            }
            if (e.NewValue is ToolManager newManager)
            {
                newManager.RedrawRequested += canvas.OnToolManagerRedrawRequested;
            }
        }
    }

    private void OnToolManagerRedrawRequested(object? sender, EventArgs e)
    {
        InvalidateVisual();
    }

    private static KeyModifiers GetKeyModifiers()
    {
        var modifiers = KeyModifiers.None;
        if (Keyboard.IsKeyDown(Key.LeftShift) || Keyboard.IsKeyDown(Key.RightShift))
            modifiers |= KeyModifiers.Shift;
        if (Keyboard.IsKeyDown(Key.LeftCtrl) || Keyboard.IsKeyDown(Key.RightCtrl))
            modifiers |= KeyModifiers.Control;
        if (Keyboard.IsKeyDown(Key.LeftAlt) || Keyboard.IsKeyDown(Key.RightAlt))
            modifiers |= KeyModifiers.Alt;
        return modifiers;
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
