namespace Pinxit.UI.Services;

/// <summary>
/// Service for displaying dialogs and message boxes.
/// </summary>
public interface IDialogService
{
    /// <summary>
    /// Shows an information message dialog.
    /// </summary>
    Task ShowInfoAsync(string title, string message);

    /// <summary>
    /// Shows a warning message dialog.
    /// </summary>
    Task ShowWarningAsync(string title, string message);

    /// <summary>
    /// Shows an error message dialog.
    /// </summary>
    Task ShowErrorAsync(string title, string message);

    /// <summary>
    /// Shows a confirmation dialog with Yes/No options.
    /// </summary>
    Task<bool> ShowConfirmAsync(string title, string message);

    /// <summary>
    /// Shows a confirmation dialog with Yes/No/Cancel options.
    /// </summary>
    Task<bool?> ShowConfirmWithCancelAsync(string title, string message);

    /// <summary>
    /// Shows an input dialog for text entry.
    /// </summary>
    Task<string?> ShowInputAsync(string title, string message, string defaultValue = "");

    /// <summary>
    /// Shows a custom content dialog.
    /// </summary>
    Task<TResult?> ShowDialogAsync<TResult>(object viewModel) where TResult : class;
}
