namespace Gesso.Plugins;

/// <summary>
/// Base interface for all Gesso plugins.
/// </summary>
public interface IPlugin
{
    /// <summary>
    /// Gets the unique identifier for this plugin.
    /// </summary>
    Guid Id { get; }

    /// <summary>
    /// Gets the display name of the plugin.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets the plugin version.
    /// </summary>
    Version Version { get; }

    /// <summary>
    /// Gets the plugin author.
    /// </summary>
    string Author { get; }

    /// <summary>
    /// Gets a description of the plugin.
    /// </summary>
    string Description { get; }

    /// <summary>
    /// Called when the plugin is loaded.
    /// </summary>
    void Initialize();

    /// <summary>
    /// Called when the plugin is unloaded.
    /// </summary>
    void Shutdown();
}
