namespace Imago.UI.Services;

using System.IO;
using System.Text.Json;
using Serilog;

public sealed class SettingsService : ISettingsService
{
    private static readonly JsonSerializerOptions s_jsonOptions = new() { WriteIndented = true };
    private readonly ILogger _logger = Log.ForContext<SettingsService>();
    private readonly string _settingsPath;
    private Dictionary<string, JsonElement> _settings = new();

    public SettingsService()
    {
        var appDataPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "Imago");

        Directory.CreateDirectory(appDataPath);
        _settingsPath = Path.Combine(appDataPath, "settings.json");
    }

    public T GetValue<T>(string key, T defaultValue)
    {
        if (_settings.TryGetValue(key, out var element))
        {
            try
            {
                return element.Deserialize<T>() ?? defaultValue;
            }
            catch (JsonException ex)
            {
                _logger.Warning(ex, "Failed to deserialize setting: {Key}", key);
            }
        }

        return defaultValue;
    }

    public void SetValue<T>(string key, T value)
    {
        var json = JsonSerializer.SerializeToElement(value);
        _settings[key] = json;
    }

    public async Task SaveAsync()
    {
        try
        {
            var json = JsonSerializer.Serialize(_settings, s_jsonOptions);

            await File.WriteAllTextAsync(_settingsPath, json);
            _logger.Information("Settings saved to {Path}", _settingsPath);
        }
        catch (Exception ex)
        {
            _logger.Error(ex, "Failed to save settings");
        }
    }

    public async Task LoadAsync()
    {
        try
        {
            if (File.Exists(_settingsPath))
            {
                var json = await File.ReadAllTextAsync(_settingsPath);
                _settings = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(json) ?? new();
                _logger.Information("Settings loaded from {Path}", _settingsPath);
            }
        }
        catch (Exception ex)
        {
            _logger.Error(ex, "Failed to load settings");
            _settings = new();
        }
    }
}
