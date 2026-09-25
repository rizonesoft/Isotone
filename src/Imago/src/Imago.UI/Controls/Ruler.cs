namespace Imago.UI.Controls;

using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

/// <summary>
/// Ruler control for displaying measurements alongside the canvas.
/// </summary>
public class Ruler : Control
{
    private const double MinorTickHeight = 4;
    private const double MajorTickHeight = 8;

    public static readonly DependencyProperty OrientationProperty =
        DependencyProperty.Register(nameof(Orientation), typeof(Orientation), typeof(Ruler),
            new FrameworkPropertyMetadata(Orientation.Horizontal, FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty ZoomProperty =
        DependencyProperty.Register(nameof(Zoom), typeof(double), typeof(Ruler),
            new FrameworkPropertyMetadata(1.0, FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty OffsetProperty =
        DependencyProperty.Register(nameof(Offset), typeof(double), typeof(Ruler),
            new FrameworkPropertyMetadata(0.0, FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty DocumentSizeProperty =
        DependencyProperty.Register(nameof(DocumentSize), typeof(double), typeof(Ruler),
            new FrameworkPropertyMetadata(0.0, FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty CursorPositionProperty =
        DependencyProperty.Register(nameof(CursorPosition), typeof(double), typeof(Ruler),
            new FrameworkPropertyMetadata(-1.0, FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty RulerBackgroundProperty =
        DependencyProperty.Register(nameof(RulerBackground), typeof(Brush), typeof(Ruler),
            new FrameworkPropertyMetadata(new SolidColorBrush(Color.FromRgb(45, 45, 48)), FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty RulerForegroundProperty =
        DependencyProperty.Register(nameof(RulerForeground), typeof(Brush), typeof(Ruler),
            new FrameworkPropertyMetadata(Brushes.LightGray, FrameworkPropertyMetadataOptions.AffectsRender));

    public static readonly DependencyProperty CursorMarkerBrushProperty =
        DependencyProperty.Register(nameof(CursorMarkerBrush), typeof(Brush), typeof(Ruler),
            new FrameworkPropertyMetadata(Brushes.Red, FrameworkPropertyMetadataOptions.AffectsRender));

    public Orientation Orientation
    {
        get => (Orientation)GetValue(OrientationProperty);
        set => SetValue(OrientationProperty, value);
    }

    public double Zoom
    {
        get => (double)GetValue(ZoomProperty);
        set => SetValue(ZoomProperty, value);
    }

    public double Offset
    {
        get => (double)GetValue(OffsetProperty);
        set => SetValue(OffsetProperty, value);
    }

    public double DocumentSize
    {
        get => (double)GetValue(DocumentSizeProperty);
        set => SetValue(DocumentSizeProperty, value);
    }

    public double CursorPosition
    {
        get => (double)GetValue(CursorPositionProperty);
        set => SetValue(CursorPositionProperty, value);
    }

    public Brush RulerBackground
    {
        get => (Brush)GetValue(RulerBackgroundProperty);
        set => SetValue(RulerBackgroundProperty, value);
    }

    public Brush RulerForeground
    {
        get => (Brush)GetValue(RulerForegroundProperty);
        set => SetValue(RulerForegroundProperty, value);
    }

    public Brush CursorMarkerBrush
    {
        get => (Brush)GetValue(CursorMarkerBrushProperty);
        set => SetValue(CursorMarkerBrushProperty, value);
    }

    static Ruler()
    {
        DefaultStyleKeyProperty.OverrideMetadata(typeof(Ruler), new FrameworkPropertyMetadata(typeof(Ruler)));
    }

    protected override void OnRender(DrawingContext drawingContext)
    {
        base.OnRender(drawingContext);

        var size = new Size(ActualWidth, ActualHeight);
        if (size.Width <= 0 || size.Height <= 0) return;

        // Background
        drawingContext.DrawRectangle(RulerBackground, null, new Rect(size));

        var pen = new Pen(RulerForeground, 1);
        pen.Freeze();

        var typeface = new Typeface("Segoe UI");
        var fontSize = 9.0;

        // Calculate tick spacing based on zoom
        var baseSpacing = GetOptimalTickSpacing(Zoom);
        var majorSpacing = baseSpacing * 10;

        if (Orientation == Orientation.Horizontal)
        {
            DrawHorizontalRuler(drawingContext, pen, typeface, fontSize, size, baseSpacing, majorSpacing);
        }
        else
        {
            DrawVerticalRuler(drawingContext, pen, typeface, fontSize, size, baseSpacing, majorSpacing);
        }

        // Draw cursor marker
        if (CursorPosition >= 0)
        {
            DrawCursorMarker(drawingContext, size);
        }
    }

    private void DrawHorizontalRuler(DrawingContext dc, Pen pen, Typeface typeface, double fontSize, Size size, double baseSpacing, double majorSpacing)
    {
        var startPixel = -Offset;
        var endPixel = size.Width - Offset;

        var startDoc = startPixel / Zoom;
        var endDoc = endPixel / Zoom;

        var firstTick = Math.Floor(startDoc / baseSpacing) * baseSpacing;

        for (var docPos = firstTick; docPos <= endDoc; docPos += baseSpacing)
        {
            var screenX = docPos * Zoom + Offset;
            if (screenX < 0 || screenX > size.Width) continue;

            var isMajor = Math.Abs(docPos % majorSpacing) < 0.001;
            var tickHeight = isMajor ? MajorTickHeight : MinorTickHeight;

            dc.DrawLine(pen, new Point(screenX, size.Height - tickHeight), new Point(screenX, size.Height));

            if (isMajor && docPos >= 0 && docPos <= DocumentSize)
            {
                var text = new FormattedText(
                    ((int)docPos).ToString(CultureInfo.InvariantCulture),
                    CultureInfo.CurrentCulture,
                    FlowDirection.LeftToRight,
                    typeface,
                    fontSize,
                    RulerForeground,
                    VisualTreeHelper.GetDpi(this).PixelsPerDip);

                dc.DrawText(text, new Point(screenX + 2, 1));
            }
        }

        // Bottom border
        dc.DrawLine(pen, new Point(0, size.Height - 0.5), new Point(size.Width, size.Height - 0.5));
    }

    private void DrawVerticalRuler(DrawingContext dc, Pen pen, Typeface typeface, double fontSize, Size size, double baseSpacing, double majorSpacing)
    {
        var startPixel = -Offset;
        var endPixel = size.Height - Offset;

        var startDoc = startPixel / Zoom;
        var endDoc = endPixel / Zoom;

        var firstTick = Math.Floor(startDoc / baseSpacing) * baseSpacing;

        for (var docPos = firstTick; docPos <= endDoc; docPos += baseSpacing)
        {
            var screenY = docPos * Zoom + Offset;
            if (screenY < 0 || screenY > size.Height) continue;

            var isMajor = Math.Abs(docPos % majorSpacing) < 0.001;
            var tickWidth = isMajor ? MajorTickHeight : MinorTickHeight;

            dc.DrawLine(pen, new Point(size.Width - tickWidth, screenY), new Point(size.Width, screenY));

            if (isMajor && docPos >= 0 && docPos <= DocumentSize)
            {
                var text = new FormattedText(
                    ((int)docPos).ToString(CultureInfo.InvariantCulture),
                    CultureInfo.CurrentCulture,
                    FlowDirection.LeftToRight,
                    typeface,
                    fontSize,
                    RulerForeground,
                    VisualTreeHelper.GetDpi(this).PixelsPerDip);

                // Draw rotated text inside the ruler
                var textX = 2;
                var textY = screenY + 2;
                dc.PushTransform(new RotateTransform(-90, textX, textY));
                dc.DrawText(text, new Point(textX, textY));
                dc.Pop();
            }
        }

        // Right border
        dc.DrawLine(pen, new Point(size.Width - 0.5, 0), new Point(size.Width - 0.5, size.Height));
    }

    private void DrawCursorMarker(DrawingContext dc, Size size)
    {
        var screenPos = CursorPosition * Zoom + Offset;
        var markerPen = new Pen(CursorMarkerBrush, 1);
        markerPen.Freeze();

        if (Orientation == Orientation.Horizontal)
        {
            if (screenPos >= 0 && screenPos <= size.Width)
            {
                dc.DrawLine(markerPen, new Point(screenPos, 0), new Point(screenPos, size.Height));
            }
        }
        else
        {
            if (screenPos >= 0 && screenPos <= size.Height)
            {
                dc.DrawLine(markerPen, new Point(0, screenPos), new Point(size.Width, screenPos));
            }
        }
    }

    private static double GetOptimalTickSpacing(double zoom)
    {
        var pixelsPerUnit = zoom;

        double[] spacings = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000];

        foreach (var spacing in spacings)
        {
            if (spacing * pixelsPerUnit >= 5)
                return spacing;
        }

        return 1000;
    }
}
