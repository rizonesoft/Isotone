namespace Imago.UI.Services;

public interface ISettingsService
{
    T GetValue<T>(string key, T defaultValue);
    void SetValue<T>(string key, T value);
    Task SaveAsync();
    Task LoadAsync();
}
