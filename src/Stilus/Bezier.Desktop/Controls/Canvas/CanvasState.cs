namespace Bezier.Desktop.Controls.Canvas;

using SkiaSharp;

/// <summary>
/// Manages the view state of the canvas including pan, zoom, and coordinate transformations.
/// </summary>
public class CanvasState
{
    private double _zoom = 1.0;
    private SKPoint _panOffset = SKPoint.Empty;
    
    /// <summary>
    /// Minimum zoom level (10%).
    /// </summary>
    public const double MinZoom = 0.1;
    
    /// <summary>
    /// Maximum zoom level (6400%).
    /// </summary>
    public const double MaxZoom = 64.0;

    /// <summary>
    /// Current zoom level (1.0 = 100%).
    /// </summary>
    public double Zoom
    {
        get => _zoom;
        private set
        {
            var clamped = Math.Clamp(value, MinZoom, MaxZoom);
            if (Math.Abs(_zoom - clamped) > double.Epsilon)
            {
                _zoom = clamped;
                OnStateChanged();
            }
        }
    }

    /// <summary>
    /// Current pan offset in screen coordinates.
    /// </summary>
    public SKPoint PanOffset
    {
        get => _panOffset;
        private set
        {
            if (_panOffset != value)
            {
                _panOffset = value;
                OnStateChanged();
            }
        }
    }

    /// <summary>
    /// Event raised when state changes.
    /// </summary>
    public event EventHandler? StateChanged;

    /// <summary>
    /// Gets the current view transform matrix.
    /// </summary>
    public SKMatrix ViewMatrix => SKMatrix.CreateScaleTranslation(
        (float)_zoom, (float)_zoom,
        _panOffset.X, _panOffset.Y);

    /// <summary>
    /// Gets the inverse view transform matrix.
    /// </summary>
    public SKMatrix InverseViewMatrix
    {
        get
        {
            var matrix = ViewMatrix;
            matrix.TryInvert(out var inverse);
            return inverse;
        }
    }

    /// <summary>
    /// Sets the zoom level.
    /// </summary>
    public void SetZoom(double zoom)
    {
        Zoom = zoom;
    }

    /// <summary>
    /// Zooms in or out centered on a specific screen point.
    /// </summary>
    public void ZoomAtPoint(double factor, SKPoint screenPoint)
    {
        var newZoom = Math.Clamp(_zoom * factor, MinZoom, MaxZoom);
        if (Math.Abs(newZoom - _zoom) < double.Epsilon) return;

        // Convert screen point to document coordinates before zoom
        var docPoint = ScreenToDocument(screenPoint);
        
        // Apply new zoom
        _zoom = newZoom;
        
        // Calculate new pan offset to keep the document point under the cursor
        _panOffset = new SKPoint(
            screenPoint.X - (float)(docPoint.X * _zoom),
            screenPoint.Y - (float)(docPoint.Y * _zoom));
        
        OnStateChanged();
    }

    /// <summary>
    /// Pans the view by delta screen coordinates.
    /// </summary>
    public void Pan(float deltaX, float deltaY)
    {
        PanOffset = new SKPoint(_panOffset.X + deltaX, _panOffset.Y + deltaY);
    }

    /// <summary>
    /// Sets the absolute pan offset.
    /// </summary>
    public void SetPan(float x, float y)
    {
        PanOffset = new SKPoint(x, y);
    }

    /// <summary>
    /// Converts screen coordinates to document coordinates.
    /// </summary>
    public SKPoint ScreenToDocument(SKPoint screenPoint)
    {
        return new SKPoint(
            (screenPoint.X - _panOffset.X) / (float)_zoom,
            (screenPoint.Y - _panOffset.Y) / (float)_zoom);
    }

    /// <summary>
    /// Converts document coordinates to screen coordinates.
    /// </summary>
    public SKPoint DocumentToScreen(SKPoint documentPoint)
    {
        return new SKPoint(
            documentPoint.X * (float)_zoom + _panOffset.X,
            documentPoint.Y * (float)_zoom + _panOffset.Y);
    }

    /// <summary>
    /// Resets the view to default state.
    /// </summary>
    public void Reset()
    {
        _zoom = 1.0;
        _panOffset = SKPoint.Empty;
        OnStateChanged();
    }

    private void OnStateChanged()
    {
        StateChanged?.Invoke(this, EventArgs.Empty);
    }
}
