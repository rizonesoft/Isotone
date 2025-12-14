namespace Imago.UI.Services;

using Serilog;

public sealed class NavigationService : INavigationService
{
    private readonly ILogger _logger = Log.ForContext<NavigationService>();
    private readonly Stack<Type> _navigationStack = new();

    public bool CanGoBack => _navigationStack.Count > 1;

    public void Navigate(Type viewType)
    {
        _logger.Debug("Navigating to {ViewType}", viewType.Name);
        _navigationStack.Push(viewType);
    }

    public void GoBack()
    {
        if (CanGoBack)
        {
            _navigationStack.Pop();
            var previousView = _navigationStack.Peek();
            _logger.Debug("Navigating back to {ViewType}", previousView.Name);
        }
    }
}
