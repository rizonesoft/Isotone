namespace Bezier.Core.Services;

/// <summary>
/// Easing functions for animations.
/// </summary>
public enum EasingFunction
{
    Linear,
    EaseInQuad,
    EaseOutQuad,
    EaseInOutQuad,
    EaseInCubic,
    EaseOutCubic,
    EaseInOutCubic,
    EaseInExpo,
    EaseOutExpo,
    EaseInOutExpo,
    EaseInBack,
    EaseOutBack,
    EaseInOutBack,
    EaseInElastic,
    EaseOutElastic,
    Spring
}

/// <summary>
/// Represents an active animation.
/// </summary>
public class Animation
{
    /// <summary>
    /// Gets the unique identifier.
    /// </summary>
    public Guid Id { get; } = Guid.NewGuid();

    /// <summary>
    /// Gets or sets the start value.
    /// </summary>
    public double StartValue { get; init; }

    /// <summary>
    /// Gets or sets the end value.
    /// </summary>
    public double EndValue { get; init; }

    /// <summary>
    /// Gets or sets the duration in milliseconds.
    /// </summary>
    public double DurationMs { get; init; } = 300;

    /// <summary>
    /// Gets or sets the easing function.
    /// </summary>
    public EasingFunction Easing { get; init; } = EasingFunction.EaseOutCubic;

    /// <summary>
    /// Gets or sets the start time.
    /// </summary>
    public DateTime StartTime { get; init; } = DateTime.UtcNow;

    /// <summary>
    /// Gets or sets the callback for value updates.
    /// </summary>
    public Action<double>? OnUpdate { get; init; }

    /// <summary>
    /// Gets or sets the callback when animation completes.
    /// </summary>
    public Action? OnComplete { get; init; }

    /// <summary>
    /// Gets whether the animation is complete.
    /// </summary>
    public bool IsComplete => GetProgress() >= 1.0;

    /// <summary>
    /// Gets the current progress (0-1).
    /// </summary>
    public double GetProgress()
    {
        var elapsed = (DateTime.UtcNow - StartTime).TotalMilliseconds;
        return Math.Clamp(elapsed / DurationMs, 0, 1);
    }

    /// <summary>
    /// Gets the current animated value.
    /// </summary>
    public double GetCurrentValue()
    {
        var t = AnimationService.ApplyEasing(GetProgress(), Easing);
        return StartValue + (EndValue - StartValue) * t;
    }
}

/// <summary>
/// Service for managing UI animations.
/// </summary>
public class AnimationService
{
    private readonly List<Animation> _activeAnimations = [];
    private readonly object _lock = new();

    /// <summary>
    /// Gets whether any animations are active.
    /// </summary>
    public bool HasActiveAnimations
    {
        get
        {
            lock (_lock)
            {
                return _activeAnimations.Count > 0;
            }
        }
    }

    /// <summary>
    /// Event raised when animations need to be rendered.
    /// </summary>
    public event EventHandler? AnimationFrame;

    /// <summary>
    /// Starts a new animation.
    /// </summary>
    public Animation Animate(
        double from,
        double to,
        double durationMs = 300,
        EasingFunction easing = EasingFunction.EaseOutCubic,
        Action<double>? onUpdate = null,
        Action? onComplete = null)
    {
        var animation = new Animation
        {
            StartValue = from,
            EndValue = to,
            DurationMs = durationMs,
            Easing = easing,
            OnUpdate = onUpdate,
            OnComplete = onComplete
        };

        lock (_lock)
        {
            _activeAnimations.Add(animation);
        }

        return animation;
    }

    /// <summary>
    /// Updates all active animations.
    /// </summary>
    public void Update()
    {
        List<Animation> completed = [];

        lock (_lock)
        {
            foreach (var animation in _activeAnimations)
            {
                var value = animation.GetCurrentValue();
                animation.OnUpdate?.Invoke(value);

                if (animation.IsComplete)
                {
                    completed.Add(animation);
                }
            }

            foreach (var animation in completed)
            {
                _activeAnimations.Remove(animation);
                animation.OnComplete?.Invoke();
            }
        }

        if (HasActiveAnimations)
        {
            AnimationFrame?.Invoke(this, EventArgs.Empty);
        }
    }

    /// <summary>
    /// Cancels an animation.
    /// </summary>
    public void Cancel(Animation animation)
    {
        lock (_lock)
        {
            _activeAnimations.Remove(animation);
        }
    }

    /// <summary>
    /// Cancels all animations.
    /// </summary>
    public void CancelAll()
    {
        lock (_lock)
        {
            _activeAnimations.Clear();
        }
    }

    /// <summary>
    /// Applies an easing function to a progress value.
    /// </summary>
    public static double ApplyEasing(double t, EasingFunction easing)
    {
        return easing switch
        {
            EasingFunction.Linear => t,
            EasingFunction.EaseInQuad => t * t,
            EasingFunction.EaseOutQuad => t * (2 - t),
            EasingFunction.EaseInOutQuad => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
            EasingFunction.EaseInCubic => t * t * t,
            EasingFunction.EaseOutCubic => 1 - Math.Pow(1 - t, 3),
            EasingFunction.EaseInOutCubic => t < 0.5 ? 4 * t * t * t : 1 - Math.Pow(-2 * t + 2, 3) / 2,
            EasingFunction.EaseInExpo => t == 0 ? 0 : Math.Pow(2, 10 * t - 10),
            EasingFunction.EaseOutExpo => t == 1 ? 1 : 1 - Math.Pow(2, -10 * t),
            EasingFunction.EaseInOutExpo => t == 0 ? 0 : t == 1 ? 1 : t < 0.5
                ? Math.Pow(2, 20 * t - 10) / 2
                : (2 - Math.Pow(2, -20 * t + 10)) / 2,
            EasingFunction.EaseInBack => 2.70158 * t * t * t - 1.70158 * t * t,
            EasingFunction.EaseOutBack => 1 + 2.70158 * Math.Pow(t - 1, 3) + 1.70158 * Math.Pow(t - 1, 2),
            EasingFunction.EaseInOutBack => t < 0.5
                ? Math.Pow(2 * t, 2) * ((2.5949095 + 1) * 2 * t - 2.5949095) / 2
                : (Math.Pow(2 * t - 2, 2) * ((2.5949095 + 1) * (t * 2 - 2) + 2.5949095) + 2) / 2,
            EasingFunction.EaseInElastic => t == 0 ? 0 : t == 1 ? 1
                : -Math.Pow(2, 10 * t - 10) * Math.Sin((t * 10 - 10.75) * (2 * Math.PI / 3)),
            EasingFunction.EaseOutElastic => t == 0 ? 0 : t == 1 ? 1
                : Math.Pow(2, -10 * t) * Math.Sin((t * 10 - 0.75) * (2 * Math.PI / 3)) + 1,
            EasingFunction.Spring => 1 - Math.Cos(t * 4.5 * Math.PI) * Math.Exp(-t * 6),
            _ => t
        };
    }

    /// <summary>
    /// Interpolates between two colors.
    /// </summary>
    public static uint LerpColor(uint from, uint to, double t)
    {
        var fromA = (byte)((from >> 24) & 0xFF);
        var fromR = (byte)((from >> 16) & 0xFF);
        var fromG = (byte)((from >> 8) & 0xFF);
        var fromB = (byte)(from & 0xFF);

        var toA = (byte)((to >> 24) & 0xFF);
        var toR = (byte)((to >> 16) & 0xFF);
        var toG = (byte)((to >> 8) & 0xFF);
        var toB = (byte)(to & 0xFF);

        var a = (byte)(fromA + (toA - fromA) * t);
        var r = (byte)(fromR + (toR - fromR) * t);
        var g = (byte)(fromG + (toG - fromG) * t);
        var b = (byte)(fromB + (toB - fromB) * t);

        return (uint)((a << 24) | (r << 16) | (g << 8) | b);
    }
}
