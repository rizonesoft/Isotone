namespace Gesso.UI.Services;

public interface INavigationService
{
    void Navigate(Type viewType);
    void GoBack();
    bool CanGoBack { get; }
}
