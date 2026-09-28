using System.IO;
using System.Text.Json;
using System.Windows.Media;

namespace Gesso.UI.Services;

/// <summary>
/// Service for loading and caching vector icon geometries from icons.json.
/// </summary>
public sealed class IconService
{
    private static IconService? s_instance;
    public static IconService Instance => s_instance ??= new IconService();

    private Dictionary<string, string> _iconPaths = [];
    private readonly Dictionary<string, Geometry> _geometryCache = [];

    public void Initialize()
    {
        try
        {
            var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Resources", "icons.json");
            if (File.Exists(path))
            {
                var json = File.ReadAllText(path);
                _iconPaths = JsonSerializer.Deserialize<Dictionary<string, string>>(json) ?? [];
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Failed to load icons.json: {ex.Message}");
        }
    }

    public Geometry GetGeometry(string name)
    {
        if (string.IsNullOrEmpty(name))
            return Geometry.Empty;

        if (_geometryCache.TryGetValue(name, out var geometry))
            return geometry;

        if (_iconPaths.TryGetValue(name, out var pathData))
        {
            try
            {
                var geom = Geometry.Parse(pathData);
                geom.Freeze();
                _geometryCache[name] = geom;
                return geom;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to parse geometry for icon '{name}': {ex.Message}");
            }
        }

        return Geometry.Empty;
    }

    public void RegisterIcon(string name, string pathData)
    {
        if (!string.IsNullOrEmpty(name) && !string.IsNullOrEmpty(pathData))
        {
            _iconPaths[name] = pathData;
            _geometryCache.Remove(name);
        }
    }
}
