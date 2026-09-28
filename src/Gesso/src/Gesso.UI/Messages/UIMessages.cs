namespace Gesso.UI.Messages;

using Gesso.UI.Services;

/// <summary>
/// Message sent when the status bar text should change.
/// </summary>
public sealed record StatusBarMessage(string Message, StatusBarMessageType Type = StatusBarMessageType.Info) : MessageBase;

/// <summary>
/// Status bar message types.
/// </summary>
public enum StatusBarMessageType
{
    Info,
    Success,
    Warning,
    Error,
    Progress
}

/// <summary>
/// Message sent when a progress operation starts.
/// </summary>
public sealed record ProgressStartedMessage(string OperationName, bool IsIndeterminate = false) : MessageBase;

/// <summary>
/// Message sent when progress updates.
/// </summary>
public sealed record ProgressUpdatedMessage(double Progress, string? StatusText = null) : MessageBase;

/// <summary>
/// Message sent when a progress operation completes.
/// </summary>
public sealed record ProgressCompletedMessage(bool Success, string? Message = null) : MessageBase;

/// <summary>
/// Message sent when a tool is selected.
/// </summary>
public sealed record ToolSelectedMessage(string ToolName) : MessageBase;

/// <summary>
/// Message sent when zoom level changes.
/// </summary>
public sealed record ZoomChangedMessage(double ZoomLevel) : MessageBase;

/// <summary>
/// Message sent when cursor position changes.
/// </summary>
public sealed record CursorPositionMessage(int X, int Y) : MessageBase;

/// <summary>
/// Message requesting the application to exit.
/// </summary>
public sealed record ExitApplicationMessage : MessageBase;
