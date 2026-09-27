namespace Bezier.Core.Services;

/// <summary>
/// Type of toast notification.
/// </summary>
public enum ToastType
{
    Info,
    Success,
    Warning,
    Error
}

/// <summary>
/// Action button for a toast notification.
/// </summary>
public record ToastAction(string Label, Action OnClick);

/// <summary>
/// Represents a toast notification.
/// </summary>
public class Toast
{
    public Guid Id { get; } = Guid.NewGuid();
    public string Title { get; init; } = string.Empty;
    public string Message { get; init; } = string.Empty;
    public ToastType Type { get; init; } = ToastType.Info;
    public int DurationMs { get; init; } = 4000;
    public bool AutoDismiss { get; init; } = true;
    public List<ToastAction> Actions { get; init; } = [];
    public DateTime CreatedAt { get; } = DateTime.UtcNow;
    public double Progress { get; set; }
    public bool IsVisible { get; set; } = true;
    public bool IsExiting { get; set; }

    /// <summary>
    /// Gets the remaining time before auto-dismiss.
    /// </summary>
    public int RemainingMs => Math.Max(0, DurationMs - (int)(DateTime.UtcNow - CreatedAt).TotalMilliseconds);

    /// <summary>
    /// Gets whether the toast should be dismissed.
    /// </summary>
    public bool ShouldDismiss => AutoDismiss && RemainingMs <= 0;
}

/// <summary>
/// Event args for toast events.
/// </summary>
public class ToastEventArgs : EventArgs
{
    public Toast Toast { get; }
    public ToastEventArgs(Toast toast) => Toast = toast;
}

/// <summary>
/// Service for managing toast notifications.
/// </summary>
public class ToastNotificationService
{
    private readonly List<Toast> _toasts = [];
    private readonly object _lock = new();

    /// <summary>
    /// Maximum number of visible toasts.
    /// </summary>
    public int MaxVisible { get; set; } = 5;

    /// <summary>
    /// Default duration for toasts in milliseconds.
    /// </summary>
    public int DefaultDuration { get; set; } = 4000;

    /// <summary>
    /// Gets all active toasts.
    /// </summary>
    public IReadOnlyList<Toast> Toasts
    {
        get
        {
            lock (_lock)
            {
                return _toasts.ToList();
            }
        }
    }

    /// <summary>
    /// Gets visible toasts (limited by MaxVisible).
    /// </summary>
    public IReadOnlyList<Toast> VisibleToasts
    {
        get
        {
            lock (_lock)
            {
                return _toasts.Where(t => t.IsVisible).Take(MaxVisible).ToList();
            }
        }
    }

    /// <summary>
    /// Event raised when a toast is added.
    /// </summary>
    public event EventHandler<ToastEventArgs>? ToastAdded;

    /// <summary>
    /// Event raised when a toast is removed.
    /// </summary>
    public event EventHandler<ToastEventArgs>? ToastRemoved;

    /// <summary>
    /// Event raised when toasts change.
    /// </summary>
    public event EventHandler? ToastsChanged;

    /// <summary>
    /// Shows a toast notification.
    /// </summary>
    public Toast Show(string message, ToastType type = ToastType.Info, string? title = null, int? durationMs = null, params ToastAction[] actions)
    {
        var toast = new Toast
        {
            Title = title ?? GetDefaultTitle(type),
            Message = message,
            Type = type,
            DurationMs = durationMs ?? DefaultDuration,
            Actions = [.. actions]
        };

        lock (_lock)
        {
            _toasts.Add(toast);
        }

        ToastAdded?.Invoke(this, new ToastEventArgs(toast));
        ToastsChanged?.Invoke(this, EventArgs.Empty);

        return toast;
    }

    /// <summary>
    /// Shows an info toast.
    /// </summary>
    public Toast Info(string message, string? title = null)
    {
        return Show(message, ToastType.Info, title);
    }

    /// <summary>
    /// Shows a success toast.
    /// </summary>
    public Toast Success(string message, string? title = null)
    {
        return Show(message, ToastType.Success, title);
    }

    /// <summary>
    /// Shows a warning toast.
    /// </summary>
    public Toast Warning(string message, string? title = null)
    {
        return Show(message, ToastType.Warning, title);
    }

    /// <summary>
    /// Shows an error toast.
    /// </summary>
    public Toast Error(string message, string? title = null)
    {
        return Show(message, ToastType.Error, title);
    }

    /// <summary>
    /// Shows a toast with an action button.
    /// </summary>
    public Toast ShowWithAction(string message, string actionLabel, Action onAction, ToastType type = ToastType.Info)
    {
        return Show(message, type, actions: new ToastAction(actionLabel, onAction));
    }

    /// <summary>
    /// Dismisses a toast.
    /// </summary>
    public void Dismiss(Toast toast)
    {
        lock (_lock)
        {
            toast.IsExiting = true;
        }

        // Allow exit animation time
        Task.Delay(200).ContinueWith(_ =>
        {
            lock (_lock)
            {
                _toasts.Remove(toast);
            }
            ToastRemoved?.Invoke(this, new ToastEventArgs(toast));
            ToastsChanged?.Invoke(this, EventArgs.Empty);
        });
    }

    /// <summary>
    /// Dismisses a toast by ID.
    /// </summary>
    public void Dismiss(Guid toastId)
    {
        lock (_lock)
        {
            var toast = _toasts.FirstOrDefault(t => t.Id == toastId);
            if (toast != null)
            {
                Dismiss(toast);
            }
        }
    }

    /// <summary>
    /// Dismisses all toasts.
    /// </summary>
    public void DismissAll()
    {
        List<Toast> toasts;
        lock (_lock)
        {
            toasts = [.. _toasts];
        }

        foreach (var toast in toasts)
        {
            Dismiss(toast);
        }
    }

    /// <summary>
    /// Updates toasts (call periodically to handle auto-dismiss).
    /// </summary>
    public void Update()
    {
        List<Toast> toDismiss;

        lock (_lock)
        {
            toDismiss = _toasts.Where(t => t.ShouldDismiss && !t.IsExiting).ToList();
        }

        foreach (var toast in toDismiss)
        {
            Dismiss(toast);
        }
    }

    private static string GetDefaultTitle(ToastType type) => type switch
    {
        ToastType.Info => "Information",
        ToastType.Success => "Success",
        ToastType.Warning => "Warning",
        ToastType.Error => "Error",
        _ => "Notification"
    };
}
