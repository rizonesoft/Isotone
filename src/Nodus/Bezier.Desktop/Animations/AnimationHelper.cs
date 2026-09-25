using System.Windows;
using System.Windows.Media.Animation;

namespace Bezier.Desktop.Animations;

/// <summary>
/// Provides reusable animation helpers using native WPF Storyboards.
/// Replaces XamlFlair with modern, maintained approach.
/// </summary>
public static class AnimationHelper
{
    /// <summary>
    /// Standard animation duration for UI transitions.
    /// </summary>
    public static readonly Duration StandardDuration = new(TimeSpan.FromMilliseconds(200));
    
    /// <summary>
    /// Slow animation duration for complex transitions.
    /// </summary>
    public static readonly Duration SlowDuration = new(TimeSpan.FromMilliseconds(400));
    
    /// <summary>
    /// Fast animation duration for micro-interactions.
    /// </summary>
    public static readonly Duration FastDuration = new(TimeSpan.FromMilliseconds(100));
    
    /// <summary>
    /// Standard easing function for smooth animations.
    /// </summary>
    public static readonly IEasingFunction StandardEasing = new CubicEase { EasingMode = EasingMode.EaseOut };

    /// <summary>
    /// Fades an element in from 0 to 1 opacity.
    /// </summary>
    public static void FadeIn(UIElement element, Duration? duration = null)
    {
        var animation = new DoubleAnimation
        {
            From = 0,
            To = 1,
            Duration = duration ?? StandardDuration,
            EasingFunction = StandardEasing
        };
        element.BeginAnimation(UIElement.OpacityProperty, animation);
    }

    /// <summary>
    /// Fades an element out from current opacity to 0.
    /// </summary>
    public static void FadeOut(UIElement element, Duration? duration = null, Action? onCompleted = null)
    {
        var animation = new DoubleAnimation
        {
            To = 0,
            Duration = duration ?? StandardDuration,
            EasingFunction = StandardEasing
        };
        
        if (onCompleted != null)
        {
            animation.Completed += (s, e) => onCompleted();
        }
        
        element.BeginAnimation(UIElement.OpacityProperty, animation);
    }

    /// <summary>
    /// Slides an element in from the specified offset.
    /// </summary>
    public static void SlideIn(FrameworkElement element, double fromX = 0, double fromY = 20, Duration? duration = null)
    {
        element.RenderTransform = new System.Windows.Media.TranslateTransform(fromX, fromY);
        
        var storyboard = new Storyboard();
        
        var translateX = new DoubleAnimation
        {
            From = fromX,
            To = 0,
            Duration = duration ?? StandardDuration,
            EasingFunction = StandardEasing
        };
        Storyboard.SetTarget(translateX, element);
        Storyboard.SetTargetProperty(translateX, new PropertyPath("RenderTransform.X"));
        
        var translateY = new DoubleAnimation
        {
            From = fromY,
            To = 0,
            Duration = duration ?? StandardDuration,
            EasingFunction = StandardEasing
        };
        Storyboard.SetTarget(translateY, element);
        Storyboard.SetTargetProperty(translateY, new PropertyPath("RenderTransform.Y"));
        
        var fadeIn = new DoubleAnimation
        {
            From = 0,
            To = 1,
            Duration = duration ?? StandardDuration,
            EasingFunction = StandardEasing
        };
        Storyboard.SetTarget(fadeIn, element);
        Storyboard.SetTargetProperty(fadeIn, new PropertyPath(UIElement.OpacityProperty));
        
        storyboard.Children.Add(translateX);
        storyboard.Children.Add(translateY);
        storyboard.Children.Add(fadeIn);
        storyboard.Begin();
    }

    /// <summary>
    /// Scales an element for a "pop" effect (micro-interaction).
    /// </summary>
    public static void Pop(FrameworkElement element, double scaleTo = 0.95)
    {
        element.RenderTransformOrigin = new Point(0.5, 0.5);
        element.RenderTransform = new System.Windows.Media.ScaleTransform(1, 1);
        
        var scaleDown = new DoubleAnimation
        {
            To = scaleTo,
            Duration = FastDuration,
            EasingFunction = StandardEasing,
            AutoReverse = true
        };
        
        var storyboard = new Storyboard();
        Storyboard.SetTarget(scaleDown, element);
        Storyboard.SetTargetProperty(scaleDown, new PropertyPath("RenderTransform.ScaleX"));
        storyboard.Children.Add(scaleDown);
        
        var scaleDownY = scaleDown.Clone();
        Storyboard.SetTarget(scaleDownY, element);
        Storyboard.SetTargetProperty(scaleDownY, new PropertyPath("RenderTransform.ScaleY"));
        storyboard.Children.Add(scaleDownY);
        
        storyboard.Begin();
    }
}
