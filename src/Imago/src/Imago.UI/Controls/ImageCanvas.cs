namespace Imago.UI.Controls;

using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using SkiaSharp;
using SkiaSharp.Views.Desktop;
using SkiaSharp.Views.WPF;

/// <summary>
/// SkiaSharp-based canvas control for rendering and interacting with images.
/// </summary>
public sealed class ImageCanvas : SKElement
{
    private SKBitmap? _documentBitmap;
    private float _zoom = 1.0f;
    private float _panX;
    private float _panY;
    private Point _lastMousePosition;
    private bool _isPanning;

    public static readonly DependencyProperty ZoomProperty =
        DependencyProperty.Register(nameof(Zoom), typeof(double), typeof(ImageCanvas),
            new PropertyMetadata(1.0, OnZoomChanged));

    public static readonly DependencyProperty PanXProperty =
        DependencyProperty.Register(nameof(PanX), typeof(double), typeof(ImageCanvas),
            new PropertyMetadata(0.0, OnPanChanged));

    public static readonly DependencyProperty PanYProperty =
        DependencyProperty.Register(nameof(PanY), typeof(double), typeof(ImageCanvas),
            new PropertyMetadata(0.0, OnPanChanged));

    public static readonly DependencyProperty ShowCheckerboardProperty =
        DependencyProperty.Register(nameof(ShowCheckerboard), typeof(bool), typeof(ImageCanvas),
            new PropertyMetadata(true, OnVisualPropertyChanged));

    public static readonly DependencyProperty DocumentWidthProperty =
        DependencyProperty.Register(nameof(DocumentWidth), typeof(int), typeof(ImageCanvas),
            new PropertyMetadata(0));

    public static readonly DependencyProperty DocumentHeightProperty =
        DependencyProperty.Register(nameof(DocumentHeight), typeof(int), typeof(ImageCanvas),
            new PropertyMetadata(0));

    public double Zoom
    {
        get => (double)GetValue(ZoomProperty);
        set => SetValue(ZoomProperty, Math.Clamp(value, 0.01, 64.0));
    }

    public double PanX
    {
        get => (double)GetValue(PanXProperty);
        set => SetValue(PanXProperty, value);
    }

    public double PanY
    {
        get => (double)GetValue(PanYProperty);
        set => SetValue(PanYProperty, value);
    }

    public bool ShowCheckerboard
    {
        get => (bool)GetValue(ShowCheckerboardProperty);
        set => SetValue(ShowCheckerboardProperty, value);
    }

    public int DocumentWidth
    {
        get => (int)GetValue(DocumentWidthProperty);
        private set => SetValue(DocumentWidthProperty, value);
    }

    public int DocumentHeight
    {
        get => (int)GetValue(DocumentHeightProperty);
        private set => SetValue(DocumentHeightProperty, value);
    }

    public event EventHandler<CanvasMouseEventArgs>? CanvasMouseMove;
    public event EventHandler<CanvasMouseEventArgs>? CanvasMouseDown;
    public event EventHandler<CanvasMouseEventArgs>? CanvasMouseUp;
    public event EventHandler? ViewportChanged;

    public ImageCanvas()
    {
        ClipToBounds = true;
        Focusable = true;

        MouseWheel += OnMouseWheel;
        MouseMove += OnMouseMove;
        MouseDown += OnMouseDown;
        MouseUp += OnMouseUp;
        MouseLeave += OnMouseLeave;
    }

    public void LoadImage(string filePath)
    {
        _documentBitmap?.Dispose();
        _documentBitmap = SKBitmap.Decode(filePath);

        if (_documentBitmap != null)
        {
            DocumentWidth = _documentBitmap.Width;
            DocumentHeight = _documentBitmap.Height;
            CenterDocument();
        }

        InvalidateVisual();
    }

    public void LoadImage(SKBitmap bitmap)
    {
        _documentBitmap?.Dispose();
        _documentBitmap = bitmap;

        if (_documentBitmap != null)
        {
            DocumentWidth = _documentBitmap.Width;
            DocumentHeight = _documentBitmap.Height;
            CenterDocument();
        }

        InvalidateVisual();
    }

    public void CenterDocument()
    {
        if (_documentBitmap == null) return;

        var canvasWidth = ActualWidth;
        var canvasHeight = ActualHeight;

        PanX = (canvasWidth - _documentBitmap.Width * Zoom) / 2;
        PanY = (canvasHeight - _documentBitmap.Height * Zoom) / 2;

        ViewportChanged?.Invoke(this, EventArgs.Empty);
    }

    public void ZoomToFit()
    {
        if (_documentBitmap == null) return;

        var canvasWidth = ActualWidth;
        var canvasHeight = ActualHeight;

        // If canvas hasn't been laid out yet, defer until after layout
        if (canvasWidth <= 0 || canvasHeight <= 0)
        {
            Dispatcher.BeginInvoke(ZoomToFit, System.Windows.Threading.DispatcherPriority.Loaded);
            return;
        }

        var zoomX = canvasWidth / _documentBitmap.Width;
        var zoomY = canvasHeight / _documentBitmap.Height;

        Zoom = Math.Min(zoomX, zoomY) * 0.9;
        CenterDocument();
    }

    public void ZoomToActual()
    {
        Zoom = 1.0;
        CenterDocument();
    }

    public (double X, double Y) ScreenToDocument(double screenX, double screenY)
    {
        var docX = (screenX - PanX) / Zoom;
        var docY = (screenY - PanY) / Zoom;
        return (docX, docY);
    }

    public (double X, double Y) DocumentToScreen(double docX, double docY)
    {
        var screenX = docX * Zoom + PanX;
        var screenY = docY * Zoom + PanY;
        return (screenX, screenY);
    }

    protected override void OnPaintSurface(SKPaintSurfaceEventArgs e)
    {
        var canvas = e.Surface.Canvas;
        var info = e.Info;

        canvas.Clear(SKColors.DimGray);

        if (_documentBitmap == null)
        {
            DrawNoDocumentMessage(canvas, info);
            return;
        }

        canvas.Save();
        canvas.Translate((float)PanX, (float)PanY);
        canvas.Scale((float)Zoom);

        // Draw checkerboard for transparency
        if (ShowCheckerboard)
        {
            DrawCheckerboard(canvas, _documentBitmap.Width, _documentBitmap.Height);
        }

        // Draw document
        canvas.DrawBitmap(_documentBitmap, 0, 0);

        // Draw document border
        using var borderPaint = new SKPaint
        {
            Style = SKPaintStyle.Stroke,
            Color = SKColors.Black,
            StrokeWidth = 1f / (float)Zoom,
            IsAntialias = false
        };
        canvas.DrawRect(0, 0, _documentBitmap.Width, _documentBitmap.Height, borderPaint);

        canvas.Restore();
    }

    private void DrawNoDocumentMessage(SKCanvas canvas, SKImageInfo info)
    {
        using var font = new SKFont(SKTypeface.Default, 16);
        using var paint = new SKPaint
        {
            Color = SKColors.Gray,
            IsAntialias = true
        };

        canvas.DrawText("No document open", info.Width / 2f, info.Height / 2f, SKTextAlign.Center, font, paint);
        canvas.DrawText("Use File > Open to load an image", info.Width / 2f, info.Height / 2f + 24, SKTextAlign.Center, font, paint);
    }

    private static void DrawCheckerboard(SKCanvas canvas, int width, int height)
    {
        const int checkSize = 8;
        using var lightPaint = new SKPaint { Color = new SKColor(255, 255, 255) };
        using var darkPaint = new SKPaint { Color = new SKColor(204, 204, 204) };

        for (int y = 0; y < height; y += checkSize)
        {
            for (int x = 0; x < width; x += checkSize)
            {
                var paint = ((x / checkSize) + (y / checkSize)) % 2 == 0 ? lightPaint : darkPaint;
                var w = Math.Min(checkSize, width - x);
                var h = Math.Min(checkSize, height - y);
                canvas.DrawRect(x, y, w, h, paint);
            }
        }
    }

    private void OnMouseWheel(object sender, MouseWheelEventArgs e)
    {
        var pos = e.GetPosition(this);
        var (docX, docY) = ScreenToDocument(pos.X, pos.Y);

        var zoomFactor = e.Delta > 0 ? 1.1 : 1 / 1.1;
        var newZoom = Math.Clamp(Zoom * zoomFactor, 0.01, 64.0);

        // Zoom toward mouse position
        PanX = pos.X - docX * newZoom;
        PanY = pos.Y - docY * newZoom;
        Zoom = newZoom;

        ViewportChanged?.Invoke(this, EventArgs.Empty);
        InvalidateVisual();
    }

    private void OnMouseMove(object sender, MouseEventArgs e)
    {
        var pos = e.GetPosition(this);

        if (_isPanning)
        {
            var dx = pos.X - _lastMousePosition.X;
            var dy = pos.Y - _lastMousePosition.Y;
            PanX += dx;
            PanY += dy;
            ViewportChanged?.Invoke(this, EventArgs.Empty);
            InvalidateVisual();
        }

        _lastMousePosition = pos;

        var (docX, docY) = ScreenToDocument(pos.X, pos.Y);
        CanvasMouseMove?.Invoke(this, new CanvasMouseEventArgs(docX, docY, e));
    }

    private void OnMouseDown(object sender, MouseButtonEventArgs e)
    {
        var pos = e.GetPosition(this);
        _lastMousePosition = pos;

        if (e.MiddleButton == MouseButtonState.Pressed ||
            (e.LeftButton == MouseButtonState.Pressed && Keyboard.IsKeyDown(Key.Space)))
        {
            _isPanning = true;
            Cursor = Cursors.Hand;
            CaptureMouse();
            return;
        }

        var (docX, docY) = ScreenToDocument(pos.X, pos.Y);
        CanvasMouseDown?.Invoke(this, new CanvasMouseEventArgs(docX, docY, e));
    }

    private void OnMouseUp(object sender, MouseButtonEventArgs e)
    {
        if (_isPanning)
        {
            _isPanning = false;
            Cursor = Cursors.Arrow;
            ReleaseMouseCapture();
            return;
        }

        var pos = e.GetPosition(this);
        var (docX, docY) = ScreenToDocument(pos.X, pos.Y);
        CanvasMouseUp?.Invoke(this, new CanvasMouseEventArgs(docX, docY, e));
    }

    private void OnMouseLeave(object sender, MouseEventArgs e)
    {
        if (_isPanning)
        {
            _isPanning = false;
            Cursor = Cursors.Arrow;
            ReleaseMouseCapture();
        }
    }

    private static void OnZoomChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is ImageCanvas canvas)
        {
            canvas._zoom = (float)(double)e.NewValue;
            canvas.ViewportChanged?.Invoke(canvas, EventArgs.Empty);
            canvas.InvalidateVisual();
        }
    }

    private static void OnPanChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is ImageCanvas canvas)
        {
            canvas._panX = (float)canvas.PanX;
            canvas._panY = (float)canvas.PanY;
            canvas.InvalidateVisual();
        }
    }

    private static void OnVisualPropertyChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        (d as ImageCanvas)?.InvalidateVisual();
    }
}

/// <summary>
/// Event args for canvas mouse events with document coordinates.
/// </summary>
public sealed class CanvasMouseEventArgs : EventArgs
{
    public double DocumentX { get; }
    public double DocumentY { get; }
    public MouseEventArgs MouseEventArgs { get; }

    public CanvasMouseEventArgs(double documentX, double documentY, MouseEventArgs mouseEventArgs)
    {
        DocumentX = documentX;
        DocumentY = documentY;
        MouseEventArgs = mouseEventArgs;
    }
}
