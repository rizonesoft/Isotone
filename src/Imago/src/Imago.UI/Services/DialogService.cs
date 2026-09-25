namespace Imago.UI.Services;

using System.Windows;
using Wpf.Ui;
using Wpf.Ui.Controls;

/// <summary>
/// WPF-UI based dialog service implementation.
/// </summary>
public sealed class DialogService : IDialogService
{
    private readonly IContentDialogService _contentDialogService;

    public DialogService(IContentDialogService contentDialogService)
    {
        _contentDialogService = contentDialogService;
    }

    public async Task ShowInfoAsync(string title, string message)
    {
        await ShowMessageAsync(title, message, "OK", null, null);
    }

    public async Task ShowWarningAsync(string title, string message)
    {
        await ShowMessageAsync(title, message, "OK", null, null);
    }

    public async Task ShowErrorAsync(string title, string message)
    {
        await ShowMessageAsync(title, message, "OK", null, null);
    }

    public async Task<bool> ShowConfirmAsync(string title, string message)
    {
        var result = await ShowMessageAsync(title, message, "Yes", "No", null);
        return result == ContentDialogResult.Primary;
    }

    public async Task<bool?> ShowConfirmWithCancelAsync(string title, string message)
    {
        var result = await ShowMessageAsync(title, message, "Yes", "No", "Cancel");
        return result switch
        {
            ContentDialogResult.Primary => true,
            ContentDialogResult.Secondary => false,
            _ => null
        };
    }

    public async Task<string?> ShowInputAsync(string title, string message, string defaultValue = "")
    {
        // For now, use a simple message box approach
        // In a full implementation, this would show a custom input dialog
        var result = await ShowConfirmAsync(title, message);
        return result ? defaultValue : null;
    }

    public Task<TResult?> ShowDialogAsync<TResult>(object viewModel) where TResult : class
    {
        // Custom dialog implementation would go here
        // This is a placeholder for the pattern
        return Task.FromResult<TResult?>(null);
    }

    private async Task<ContentDialogResult> ShowMessageAsync(
        string title,
        string message,
        string primaryButton,
        string? secondaryButton,
        string? closeButton)
    {
        var dialog = new ContentDialog
        {
            Title = title,
            Content = message,
            PrimaryButtonText = primaryButton,
            SecondaryButtonText = secondaryButton ?? string.Empty,
            CloseButtonText = closeButton ?? string.Empty,
            DefaultButton = ContentDialogButton.Primary
        };

        return await _contentDialogService.ShowAsync(dialog, CancellationToken.None);
    }
}
