namespace Bezier.Tests;

using Bezier.Core.Services;

public class MicroInteractionServiceTests
{
    private readonly MicroInteractionService _service;

    public MicroInteractionServiceTests()
    {
        _service = new MicroInteractionService();
    }

    [Fact]
    public void StartInteraction_CreatesState()
    {
        var config = MicroInteractionService.Defaults.ButtonPress;

        var state = _service.StartInteraction(config);

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.Press, state.Effect);
        Assert.True(_service.HasActiveInteractions);
    }

    [Fact]
    public void Press_CreatesInteraction()
    {
        var state = _service.Press();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.Press, state.Effect);
    }

    [Fact]
    public void Hover_CreatesInteraction()
    {
        var state = _service.Hover();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.Hover, state.Effect);
    }

    [Fact]
    public void Shake_CreatesInteraction()
    {
        var state = _service.Shake();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.Shake, state.Effect);
    }

    [Fact]
    public void Bounce_CreatesInteraction()
    {
        var state = _service.Bounce();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.Bounce, state.Effect);
    }

    [Fact]
    public void Pulse_CreatesInteraction()
    {
        var state = _service.Pulse();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.Pulse, state.Effect);
    }

    [Fact]
    public void SlideIn_CreatesInteraction()
    {
        var state = _service.SlideIn();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.SlideIn, state.Effect);
    }

    [Fact]
    public void FadeIn_CreatesInteraction()
    {
        var state = _service.FadeIn();

        Assert.NotNull(state);
        Assert.Equal(InteractionEffect.FadeIn, state.Effect);
    }

    [Fact]
    public void Cancel_RemovesInteraction()
    {
        var state = _service.Press();

        _service.Cancel(state);

        Assert.False(_service.HasActiveInteractions);
    }

    [Fact]
    public void CancelAll_RemovesAllInteractions()
    {
        _service.Press();
        _service.Hover();
        _service.Shake();

        _service.CancelAll();

        Assert.False(_service.HasActiveInteractions);
    }

    [Fact]
    public void CancelForTarget_RemovesTargetInteractions()
    {
        var target = new object();
        _service.Press(target);
        _service.Press();

        _service.CancelForTarget(target);

        Assert.True(_service.HasActiveInteractions); // Non-target still exists
    }

    [Fact]
    public void InteractionState_GetScale_Press_ReturnsValidValue()
    {
        var state = new InteractionState
        {
            Effect = InteractionEffect.Press,
            Progress = 0.5,
            Intensity = 1.0,
            Easing = EasingFunction.Linear
        };

        var scale = state.GetScale();

        Assert.InRange(scale, 0.9, 1.0);
    }

    [Fact]
    public void InteractionState_GetScale_Hover_ReturnsValidValue()
    {
        var state = new InteractionState
        {
            Effect = InteractionEffect.Hover,
            Progress = 1.0,
            Intensity = 1.0,
            Easing = EasingFunction.Linear
        };

        var scale = state.GetScale();

        Assert.InRange(scale, 1.0, 1.05);
    }

    [Fact]
    public void InteractionState_GetOpacity_FadeIn_ReturnsValidValue()
    {
        var state = new InteractionState
        {
            Effect = InteractionEffect.FadeIn,
            Progress = 0.5,
            Intensity = 1.0,
            Easing = EasingFunction.Linear
        };

        var opacity = state.GetOpacity();

        Assert.InRange(opacity, 0.4, 0.6);
    }

    [Fact]
    public void InteractionState_GetOffset_SlideIn_ReturnsValidValue()
    {
        var state = new InteractionState
        {
            Effect = InteractionEffect.SlideIn,
            Progress = 0.5,
            Intensity = 1.0,
            Easing = EasingFunction.Linear
        };

        var (x, y) = state.GetOffset();

        Assert.Equal(0, x);
        Assert.InRange(y, 5, 15);
    }

    [Fact]
    public void InteractionState_GetOffset_Shake_ReturnsValidValue()
    {
        var state = new InteractionState
        {
            Effect = InteractionEffect.Shake,
            Progress = 0.25,
            Intensity = 1.0,
            Easing = EasingFunction.Linear
        };

        var (x, y) = state.GetOffset();

        Assert.NotEqual(0, x); // Should oscillate
        Assert.Equal(0, y);
    }

    [Fact]
    public void Defaults_HaveValidConfigurations()
    {
        Assert.True(MicroInteractionService.Defaults.ButtonPress.Duration > 0);
        Assert.True(MicroInteractionService.Defaults.ButtonHover.Duration > 0);
        Assert.True(MicroInteractionService.Defaults.ToggleSwitch.Duration > 0);
        Assert.True(MicroInteractionService.Defaults.ErrorShake.Duration > 0);
        Assert.True(MicroInteractionService.Defaults.SuccessBounce.Duration > 0);
    }
}

public class ToastNotificationServiceTests
{
    private readonly ToastNotificationService _service;

    public ToastNotificationServiceTests()
    {
        _service = new ToastNotificationService();
    }

    [Fact]
    public void Show_AddsToast()
    {
        var toast = _service.Show("Test message");

        Assert.Single(_service.Toasts);
        Assert.Equal("Test message", toast.Message);
    }

    [Fact]
    public void Show_SetsCorrectType()
    {
        var toast = _service.Show("Test", ToastType.Error);

        Assert.Equal(ToastType.Error, toast.Type);
    }

    [Fact]
    public void Info_CreatesInfoToast()
    {
        var toast = _service.Info("Info message");

        Assert.Equal(ToastType.Info, toast.Type);
        Assert.Equal("Information", toast.Title);
    }

    [Fact]
    public void Success_CreatesSuccessToast()
    {
        var toast = _service.Success("Success message");

        Assert.Equal(ToastType.Success, toast.Type);
        Assert.Equal("Success", toast.Title);
    }

    [Fact]
    public void Warning_CreatesWarningToast()
    {
        var toast = _service.Warning("Warning message");

        Assert.Equal(ToastType.Warning, toast.Type);
        Assert.Equal("Warning", toast.Title);
    }

    [Fact]
    public void Error_CreatesErrorToast()
    {
        var toast = _service.Error("Error message");

        Assert.Equal(ToastType.Error, toast.Type);
        Assert.Equal("Error", toast.Title);
    }

    [Fact]
    public void Show_WithCustomTitle_UsesTitle()
    {
        var toast = _service.Show("Message", title: "Custom Title");

        Assert.Equal("Custom Title", toast.Title);
    }

    [Fact]
    public void Show_WithActions_AddsActions()
    {
        var actionCalled = false;
        var toast = _service.Show("Message", actions: new ToastAction("Click", () => actionCalled = true));

        Assert.Single(toast.Actions);
        toast.Actions[0].OnClick();
        Assert.True(actionCalled);
    }

    [Fact]
    public void ShowWithAction_CreatesActionableToast()
    {
        var toast = _service.ShowWithAction("Message", "Undo", () => { });

        Assert.Single(toast.Actions);
        Assert.Equal("Undo", toast.Actions[0].Label);
    }

    [Fact]
    public void Dismiss_RemovesToast()
    {
        var toast = _service.Show("Test");

        _service.Dismiss(toast);

        // Toast is exiting
        Assert.True(toast.IsExiting);
    }

    [Fact]
    public void DismissById_RemovesToast()
    {
        var toast = _service.Show("Test");

        _service.Dismiss(toast.Id);

        Assert.True(toast.IsExiting);
    }

    [Fact]
    public void VisibleToasts_RespectsMaxVisible()
    {
        _service.MaxVisible = 2;

        _service.Show("Toast 1");
        _service.Show("Toast 2");
        _service.Show("Toast 3");

        Assert.Equal(2, _service.VisibleToasts.Count);
    }

    [Fact]
    public void Toast_RemainingMs_DecreasesOverTime()
    {
        var toast = new Toast { DurationMs = 1000 };

        Thread.Sleep(100);
        var remaining = toast.RemainingMs;

        Assert.True(remaining < 1000);
    }

    [Fact]
    public void Toast_ShouldDismiss_ReturnsTrue_WhenExpired()
    {
        var toast = new Toast { DurationMs = 1, AutoDismiss = true };

        Thread.Sleep(10);

        Assert.True(toast.ShouldDismiss);
    }

    [Fact]
    public void Toast_ShouldDismiss_ReturnsFalse_WhenNotAutoDismiss()
    {
        var toast = new Toast { DurationMs = 1, AutoDismiss = false };

        Thread.Sleep(10);

        Assert.False(toast.ShouldDismiss);
    }

    [Fact]
    public void ToastAdded_EventRaised()
    {
        Toast? addedToast = null;
        _service.ToastAdded += (_, e) => addedToast = e.Toast;

        var toast = _service.Show("Test");

        Assert.Same(toast, addedToast);
    }

    [Fact]
    public void DefaultDuration_IsUsed()
    {
        _service.DefaultDuration = 5000;

        var toast = _service.Show("Test");

        Assert.Equal(5000, toast.DurationMs);
    }

    [Fact]
    public void CustomDuration_OverridesDefault()
    {
        _service.DefaultDuration = 5000;

        var toast = _service.Show("Test", durationMs: 1000);

        Assert.Equal(1000, toast.DurationMs);
    }
}

public class InteractionConfigTests
{
    [Fact]
    public void InteractionConfig_HasDefaultValues()
    {
        var config = new InteractionConfig(InteractionEffect.Press);

        Assert.Equal(200, config.Duration);
        Assert.Equal(EasingFunction.EaseOutCubic, config.Easing);
        Assert.Equal(1.0, config.Intensity);
    }

    [Fact]
    public void InteractionConfig_AllowsCustomValues()
    {
        var config = new InteractionConfig(
            InteractionEffect.Shake,
            Duration: 500,
            Easing: EasingFunction.EaseInOutBack,
            Intensity: 2.0
        );

        Assert.Equal(500, config.Duration);
        Assert.Equal(EasingFunction.EaseInOutBack, config.Easing);
        Assert.Equal(2.0, config.Intensity);
    }
}
