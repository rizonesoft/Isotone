namespace Bezier.Core.Services;

/// <summary>
/// Type of micro-interaction effect.
/// </summary>
public enum InteractionEffect
{
    /// <summary>Scale down then up (press effect).</summary>
    Press,
    /// <summary>Scale up slightly (hover effect).</summary>
    Hover,
    /// <summary>Subtle glow effect.</summary>
    Glow,
    /// <summary>Ripple from click point.</summary>
    Ripple,
    /// <summary>Shake effect (error).</summary>
    Shake,
    /// <summary>Bounce effect (success).</summary>
    Bounce,
    /// <summary>Pulse effect (attention).</summary>
    Pulse,
    /// <summary>Slide in effect.</summary>
    SlideIn,
    /// <summary>Fade in effect.</summary>
    FadeIn
}

/// <summary>
/// Configuration for a micro-interaction.
/// </summary>
public record InteractionConfig(
    InteractionEffect Effect,
    double Duration = 200,
    EasingFunction Easing = EasingFunction.EaseOutCubic,
    double Intensity = 1.0
);

/// <summary>
/// State of an active interaction animation.
/// </summary>
public class InteractionState
{
    public Guid Id { get; } = Guid.NewGuid();
    public InteractionEffect Effect { get; init; }
    public double Progress { get; set; }
    public double Duration { get; init; }
    public EasingFunction Easing { get; init; }
    public double Intensity { get; init; }
    public DateTime StartTime { get; init; } = DateTime.UtcNow;
    public Action<InteractionState>? OnUpdate { get; init; }
    public Action? OnComplete { get; init; }
    public object? Target { get; init; }

    /// <summary>
    /// Gets the current scale value for scale-based effects.
    /// </summary>
    public double GetScale()
    {
        var t = AnimationService.ApplyEasing(Progress, Easing);
        return Effect switch
        {
            InteractionEffect.Press => 1.0 - (0.05 * Intensity * (1 - t)),
            InteractionEffect.Hover => 1.0 + (0.02 * Intensity * t),
            InteractionEffect.Bounce => 1.0 + (0.1 * Intensity * Math.Sin(t * Math.PI)),
            InteractionEffect.Pulse => 1.0 + (0.05 * Intensity * Math.Sin(t * Math.PI * 2)),
            _ => 1.0
        };
    }

    /// <summary>
    /// Gets the current opacity for fade effects.
    /// </summary>
    public double GetOpacity()
    {
        var t = AnimationService.ApplyEasing(Progress, Easing);
        return Effect switch
        {
            InteractionEffect.FadeIn => t,
            InteractionEffect.Glow => 0.3 * Intensity * (1 - Math.Abs(2 * t - 1)),
            _ => 1.0
        };
    }

    /// <summary>
    /// Gets the current offset for slide/shake effects.
    /// </summary>
    public (double X, double Y) GetOffset()
    {
        var t = AnimationService.ApplyEasing(Progress, Easing);
        return Effect switch
        {
            InteractionEffect.SlideIn => (0, 20 * (1 - t) * Intensity),
            InteractionEffect.Shake => (5 * Intensity * Math.Sin(t * Math.PI * 6) * (1 - t), 0),
            _ => (0, 0)
        };
    }
}

/// <summary>
/// Service for managing micro-interactions and UI feedback animations.
/// </summary>
public class MicroInteractionService
{
    private readonly List<InteractionState> _activeInteractions = [];
    private readonly AnimationService _animationService;
    private readonly object _lock = new();

    /// <summary>
    /// Default configurations for common interactions.
    /// </summary>
    public static class Defaults
    {
        public static readonly InteractionConfig ButtonPress = new(InteractionEffect.Press, 150, EasingFunction.EaseOutCubic);
        public static readonly InteractionConfig ButtonHover = new(InteractionEffect.Hover, 200, EasingFunction.EaseOutCubic);
        public static readonly InteractionConfig ToggleSwitch = new(InteractionEffect.Press, 200, EasingFunction.Spring);
        public static readonly InteractionConfig ErrorShake = new(InteractionEffect.Shake, 400, EasingFunction.EaseOutCubic);
        public static readonly InteractionConfig SuccessBounce = new(InteractionEffect.Bounce, 300, EasingFunction.EaseOutElastic);
        public static readonly InteractionConfig AttentionPulse = new(InteractionEffect.Pulse, 600, EasingFunction.Linear);
        public static readonly InteractionConfig PanelSlideIn = new(InteractionEffect.SlideIn, 250, EasingFunction.EaseOutCubic);
        public static readonly InteractionConfig PanelFadeIn = new(InteractionEffect.FadeIn, 200, EasingFunction.EaseOutCubic);
        public static readonly InteractionConfig SubtleGlow = new(InteractionEffect.Glow, 300, EasingFunction.EaseInOutCubic);
    }

    public MicroInteractionService(AnimationService? animationService = null)
    {
        _animationService = animationService ?? new AnimationService();
    }

    /// <summary>
    /// Gets whether any interactions are active.
    /// </summary>
    public bool HasActiveInteractions
    {
        get
        {
            lock (_lock)
            {
                return _activeInteractions.Count > 0;
            }
        }
    }

    /// <summary>
    /// Event raised when interactions need to be rendered.
    /// </summary>
    public event EventHandler? InteractionFrame;

    /// <summary>
    /// Starts a micro-interaction.
    /// </summary>
    public InteractionState StartInteraction(
        InteractionConfig config,
        object? target = null,
        Action<InteractionState>? onUpdate = null,
        Action? onComplete = null)
    {
        var state = new InteractionState
        {
            Effect = config.Effect,
            Duration = config.Duration,
            Easing = config.Easing,
            Intensity = config.Intensity,
            Target = target,
            OnUpdate = onUpdate,
            OnComplete = onComplete
        };

        lock (_lock)
        {
            _activeInteractions.Add(state);
        }

        return state;
    }

    /// <summary>
    /// Starts a button press interaction.
    /// </summary>
    public InteractionState Press(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.ButtonPress, target, onUpdate);
    }

    /// <summary>
    /// Starts a hover interaction.
    /// </summary>
    public InteractionState Hover(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.ButtonHover, target, onUpdate);
    }

    /// <summary>
    /// Starts an error shake interaction.
    /// </summary>
    public InteractionState Shake(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.ErrorShake, target, onUpdate);
    }

    /// <summary>
    /// Starts a success bounce interaction.
    /// </summary>
    public InteractionState Bounce(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.SuccessBounce, target, onUpdate);
    }

    /// <summary>
    /// Starts an attention pulse interaction.
    /// </summary>
    public InteractionState Pulse(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.AttentionPulse, target, onUpdate);
    }

    /// <summary>
    /// Starts a panel slide-in interaction.
    /// </summary>
    public InteractionState SlideIn(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.PanelSlideIn, target, onUpdate);
    }

    /// <summary>
    /// Starts a fade-in interaction.
    /// </summary>
    public InteractionState FadeIn(object? target = null, Action<InteractionState>? onUpdate = null)
    {
        return StartInteraction(Defaults.PanelFadeIn, target, onUpdate);
    }

    /// <summary>
    /// Updates all active interactions.
    /// </summary>
    public void Update()
    {
        List<InteractionState> completed = [];

        lock (_lock)
        {
            foreach (var state in _activeInteractions)
            {
                var elapsed = (DateTime.UtcNow - state.StartTime).TotalMilliseconds;
                state.Progress = Math.Clamp(elapsed / state.Duration, 0, 1);
                state.OnUpdate?.Invoke(state);

                if (state.Progress >= 1.0)
                {
                    completed.Add(state);
                }
            }

            foreach (var state in completed)
            {
                _activeInteractions.Remove(state);
                state.OnComplete?.Invoke();
            }
        }

        if (HasActiveInteractions)
        {
            InteractionFrame?.Invoke(this, EventArgs.Empty);
        }
    }

    /// <summary>
    /// Cancels an interaction.
    /// </summary>
    public void Cancel(InteractionState state)
    {
        lock (_lock)
        {
            _activeInteractions.Remove(state);
        }
    }

    /// <summary>
    /// Cancels all interactions for a target.
    /// </summary>
    public void CancelForTarget(object target)
    {
        lock (_lock)
        {
            _activeInteractions.RemoveAll(s => s.Target == target);
        }
    }

    /// <summary>
    /// Cancels all active interactions.
    /// </summary>
    public void CancelAll()
    {
        lock (_lock)
        {
            _activeInteractions.Clear();
        }
    }
}
