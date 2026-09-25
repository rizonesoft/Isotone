namespace Imago.UI.Services;

using System.Windows;

/// <summary>
/// Simple dialog service implementation using standard WPF MessageBox.
/// </summary>
public sealed class DialogService : IDialogService
{
    public Task ShowInfoAsync(string title, string message)
    {
        MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Information);
        return Task.CompletedTask;
    }

    public Task ShowWarningAsync(string title, string message)
    {
        MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Warning);
        return Task.CompletedTask;
    }

    public Task ShowErrorAsync(string title, string message)
    {
        MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Error);
        return Task.CompletedTask;
    }

    public Task<bool> ShowConfirmAsync(string title, string message)
    {
        var result = MessageBox.Show(message, title, MessageBoxButton.YesNo, MessageBoxImage.Question);
        return Task.FromResult(result == MessageBoxResult.Yes);
    }

    public Task<bool?> ShowConfirmWithCancelAsync(string title, string message)
    {
        var result = MessageBox.Show(message, title, MessageBoxButton.YesNoCancel, MessageBoxImage.Question);
        return Task.FromResult<bool?>(result switch
        {
            MessageBoxResult.Yes => true,
            MessageBoxResult.No => false,
            _ => null
        });
    }

    public Task<string?> ShowInputAsync(string title, string message, string defaultValue = "")
    {
        // Simple implementation - returns default or null based on confirmation
        var result = MessageBox.Show(message, title, MessageBoxButton.OKCancel, MessageBoxImage.Question);
        return Task.FromResult<string?>(result == MessageBoxResult.OK ? defaultValue : null);
    }

    public Task<TResult?> ShowDialogAsync<TResult>(object viewModel) where TResult : class
    {
        // Custom dialog implementation would go here
        return Task.FromResult<TResult?>(null);
    }
}
