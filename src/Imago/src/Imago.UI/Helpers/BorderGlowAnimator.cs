namespace Imago.UI.Helpers;

using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;

/// <summary>
/// Animates a glowing effect that travels around a border.
/// Use with a RadialGradientBrush mask on a Shape element (Path, Rectangle, etc.).
/// </summary>
public class BorderGlowAnimator
{
    private readonly Shape _glowShape;
    private readonly RadialGradientBrush _glowMask;
    private PointAnimationUsingKeyFrames? _animation;
    private bool _isVisible;

    /// <summary>
    /// Gets whether the glow effect is currently visible.
    /// </summary>
    public bool IsVisible => _isVisible;

    /// <summary>
    /// Duration for one complete loop around the border.
    /// </summary>
    public TimeSpan Duration { get; set; } = TimeSpan.FromSeconds(6);

    /// <summary>
    /// Corner radius of the border.
    /// </summary>
    public double CornerRadius { get; set; } = 8;

    /// <summary>
    /// Number of keyframe steps for smooth animation.
    /// </summary>
    public int Steps { get; set; } = 300;

    /// <summary>
    /// Creates a new BorderGlowAnimator.
    /// </summary>
    /// <param name="glowShape">The Shape element to animate opacity on (Path, Rectangle, etc.).</param>
    /// <param name="glowMask">The RadialGradientBrush to animate position on.</param>
    public BorderGlowAnimator(Shape glowShape, RadialGradientBrush glowMask)
    {
        _glowShape = glowShape;
        _glowMask = glowMask;
    }

    /// <summary>
    /// Initializes and starts the animation (runs continuously but hidden).
    /// </summary>
    /// <param name="width">Width of the border area.</param>
    /// <param name="height">Height of the border area.</param>
    public void Initialize(double width, double height)
    {
        if (width <= 0 || height <= 0) return;

        // Stop any existing animation before reinitializing
        if (_animation != null)
        {
            _glowMask.BeginAnimation(RadialGradientBrush.CenterProperty, null);
            _glowMask.BeginAnimation(RadialGradientBrush.GradientOriginProperty, null);
        }

        double r = CornerRadius;

        // Calculate total path length
        double straightH = width - 2 * r;
        double straightV = height - 2 * r;
        double cornerLength = Math.PI * r / 2;
        double totalLength = 2 * straightH + 2 * straightV + 4 * cornerLength;

        _animation = new PointAnimationUsingKeyFrames
        {
            RepeatBehavior = RepeatBehavior.Forever,
            Duration = Duration
        };

        // Generate keyframes
        for (int i = 0; i <= Steps; i++)
        {
            double progress = (double)i / Steps;
            double currentDist = progress * totalLength;

            var pos = GetPointOnBorder(currentDist, width, height, r);
            _animation.KeyFrames.Add(new LinearPointKeyFrame(pos, KeyTime.FromPercent(progress)));
        }

        // Start the animation (runs continuously in background)
        _glowMask.BeginAnimation(RadialGradientBrush.CenterProperty, _animation);
        _glowMask.BeginAnimation(RadialGradientBrush.GradientOriginProperty, _animation);
    }

    /// <summary>
    /// Shows the glow effect (fades in).
    /// </summary>
    public void Show()
    {
        if (_animation == null || _isVisible) return;

        _isVisible = true;

        var fadeIn = new DoubleAnimation
        {
            To = 1,
            Duration = TimeSpan.FromMilliseconds(300),
            EasingFunction = new QuadraticEase { EasingMode = EasingMode.EaseOut }
        };
        _glowShape.BeginAnimation(UIElement.OpacityProperty, fadeIn);
    }

    /// <summary>
    /// Hides the glow effect (fades out).
    /// </summary>
    public void Hide()
    {
        if (!_isVisible) return;

        _isVisible = false;

        var fadeOut = new DoubleAnimation
        {
            To = 0,
            Duration = TimeSpan.FromMilliseconds(500),
            EasingFunction = new QuadraticEase { EasingMode = EasingMode.EaseIn }
        };
        _glowShape.BeginAnimation(UIElement.OpacityProperty, fadeOut);
    }

    /// <summary>
    /// Stops the animation completely.
    /// </summary>
    public void Stop()
    {
        _glowMask.BeginAnimation(RadialGradientBrush.CenterProperty, null);
        _glowMask.BeginAnimation(RadialGradientBrush.GradientOriginProperty, null);
        _glowShape.BeginAnimation(UIElement.OpacityProperty, null);
        _animation = null;
        _isVisible = false;
    }

    private Point GetPointOnBorder(double distance, double w, double h, double r)
    {
        double straightH = w - 2 * r;
        double straightV = h - 2 * r;
        double cornerLen = Math.PI * r / 2;

        // 1. Top Edge
        if (distance <= straightH)
            return new Point(r + distance, 0);
        distance -= straightH;

        // 2. Top-Right Corner
        if (distance <= cornerLen)
        {
            double angleRad = distance / r;
            double theta = -Math.PI / 2 + angleRad;
            double px = (w - r) + r * Math.Cos(theta);
            double py = r + r * Math.Sin(theta);
            return new Point(px, py);
        }
        distance -= cornerLen;

        // 3. Right Edge
        if (distance <= straightV)
            return new Point(w, r + distance);
        distance -= straightV;

        // 4. Bottom-Right Corner
        if (distance <= cornerLen)
        {
            double angleRad = distance / r;
            double theta = angleRad;
            double px = (w - r) + r * Math.Cos(theta);
            double py = (h - r) + r * Math.Sin(theta);
            return new Point(px, py);
        }
        distance -= cornerLen;

        // 5. Bottom Edge
        if (distance <= straightH)
            return new Point(w - r - distance, h);
        distance -= straightH;

        // 6. Bottom-Left Corner
        if (distance <= cornerLen)
        {
            double angleRad = distance / r;
            double theta = Math.PI / 2 + angleRad;
            double px = r + r * Math.Cos(theta);
            double py = (h - r) + r * Math.Sin(theta);
            return new Point(px, py);
        }
        distance -= cornerLen;

        // 7. Left Edge
        if (distance <= straightV)
            return new Point(0, h - r - distance);
        distance -= straightV;

        // 8. Top-Left Corner
        double finalAngleRad = distance / r;
        double finalTheta = Math.PI + finalAngleRad;
        double finalPx = r + r * Math.Cos(finalTheta);
        double finalPy = r + r * Math.Sin(finalTheta);
        return new Point(finalPx, finalPy);
    }
}
