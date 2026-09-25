using System.ComponentModel;
using System.Text.Json;

namespace Bezier.Core.Services;

/// <summary>
/// Modifier keys for shortcuts.
/// </summary>
[Flags]
public enum ModifierKeys
{
    None = 0,
    Ctrl = 1,
    Alt = 2,
    Shift = 4,
    Win = 8
}

/// <summary>
/// Represents a keyboard shortcut binding.
/// </summary>
public class KeyboardShortcut : INotifyPropertyChanged
{
    private string _key = string.Empty;
    private ModifierKeys _modifiers;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets or sets the command ID this shortcut is bound to.
    /// </summary>
    public string CommandId { get; init; } = string.Empty;

    /// <summary>
    /// Gets or sets the key (e.g., "A", "F1", "Delete").
    /// </summary>
    public string Key
    {
        get => _key;
        set { _key = value; OnPropertyChanged(nameof(Key)); OnPropertyChanged(nameof(DisplayText)); }
    }

    /// <summary>
    /// Gets or sets the modifier keys.
    /// </summary>
    public ModifierKeys Modifiers
    {
        get => _modifiers;
        set { _modifiers = value; OnPropertyChanged(nameof(Modifiers)); OnPropertyChanged(nameof(DisplayText)); }
    }

    /// <summary>
    /// Gets whether this is the default shortcut.
    /// </summary>
    public bool IsDefault { get; init; }

    /// <summary>
    /// Gets the display text for this shortcut.
    /// </summary>
    public string DisplayText
    {
        get
        {
            var parts = new List<string>();
            if (Modifiers.HasFlag(ModifierKeys.Ctrl)) parts.Add("Ctrl");
            if (Modifiers.HasFlag(ModifierKeys.Alt)) parts.Add("Alt");
            if (Modifiers.HasFlag(ModifierKeys.Shift)) parts.Add("Shift");
            if (Modifiers.HasFlag(ModifierKeys.Win)) parts.Add("Win");
            if (!string.IsNullOrEmpty(Key)) parts.Add(Key);
            return string.Join("+", parts);
        }
    }

    /// <summary>
    /// Checks if this shortcut matches the given key and modifiers.
    /// </summary>
    public bool Matches(string key, ModifierKeys modifiers)
    {
        return Key.Equals(key, StringComparison.OrdinalIgnoreCase) && Modifiers == modifiers;
    }

    /// <summary>
    /// Parses a shortcut string (e.g., "Ctrl+S").
    /// </summary>
    public static KeyboardShortcut Parse(string shortcutText, string commandId = "")
    {
        var shortcut = new KeyboardShortcut { CommandId = commandId };
        var parts = shortcutText.Split('+');

        foreach (var part in parts)
        {
            var trimmed = part.Trim();
            switch (trimmed.ToLowerInvariant())
            {
                case "ctrl":
                case "control":
                    shortcut.Modifiers |= ModifierKeys.Ctrl;
                    break;
                case "alt":
                    shortcut.Modifiers |= ModifierKeys.Alt;
                    break;
                case "shift":
                    shortcut.Modifiers |= ModifierKeys.Shift;
                    break;
                case "win":
                case "windows":
                case "meta":
                    shortcut.Modifiers |= ModifierKeys.Win;
                    break;
                default:
                    shortcut.Key = trimmed;
                    break;
            }
        }

        return shortcut;
    }
}

/// <summary>
/// Shortcut conflict information.
/// </summary>
public record ShortcutConflict(
    KeyboardShortcut Existing,
    KeyboardShortcut New,
    string ExistingCommandName,
    string NewCommandName
);

/// <summary>
/// Preset shortcut profile.
/// </summary>
public enum ShortcutProfile
{
    Default,
    Illustrator,
    Inkscape,
    Figma
}

/// <summary>
/// Service for managing keyboard shortcuts.
/// </summary>
public class ShortcutManager : INotifyPropertyChanged
{
    private readonly Dictionary<string, KeyboardShortcut> _shortcuts = [];
    private readonly Dictionary<string, KeyboardShortcut> _defaultShortcuts = [];
    private readonly Dictionary<string, string> _commandNames = [];
    private ShortcutProfile _currentProfile = ShortcutProfile.Default;

    public event PropertyChangedEventHandler? PropertyChanged;
    public event EventHandler<KeyboardShortcut>? ShortcutChanged;
    public event EventHandler<ShortcutConflict>? ConflictDetected;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets all registered shortcuts.
    /// </summary>
    public IReadOnlyDictionary<string, KeyboardShortcut> Shortcuts => _shortcuts;

    /// <summary>
    /// Gets or sets the current shortcut profile.
    /// </summary>
    public ShortcutProfile CurrentProfile
    {
        get => _currentProfile;
        set
        {
            if (_currentProfile != value)
            {
                _currentProfile = value;
                ApplyProfile(value);
                OnPropertyChanged(nameof(CurrentProfile));
            }
        }
    }

    /// <summary>
    /// Registers a command with its default shortcut.
    /// </summary>
    public void RegisterCommand(string commandId, string commandName, string? defaultShortcut = null)
    {
        _commandNames[commandId] = commandName;

        if (!string.IsNullOrEmpty(defaultShortcut))
        {
            var shortcut = KeyboardShortcut.Parse(defaultShortcut, commandId);
            var defaultShortcutCopy = new KeyboardShortcut
            {
                CommandId = shortcut.CommandId,
                Key = shortcut.Key,
                Modifiers = shortcut.Modifiers,
                IsDefault = true
            };
            _defaultShortcuts[commandId] = defaultShortcutCopy;
            _shortcuts[commandId] = shortcut;
        }
    }

    /// <summary>
    /// Sets a shortcut for a command.
    /// </summary>
    public ShortcutConflict? SetShortcut(string commandId, string key, ModifierKeys modifiers)
    {
        // Check for conflicts
        var conflict = FindConflict(commandId, key, modifiers);
        if (conflict != null)
        {
            ConflictDetected?.Invoke(this, conflict);
        }

        var shortcut = new KeyboardShortcut
        {
            CommandId = commandId,
            Key = key,
            Modifiers = modifiers
        };

        _shortcuts[commandId] = shortcut;
        ShortcutChanged?.Invoke(this, shortcut);
        return conflict;
    }

    /// <summary>
    /// Sets a shortcut from a string.
    /// </summary>
    public ShortcutConflict? SetShortcut(string commandId, string shortcutText)
    {
        var parsed = KeyboardShortcut.Parse(shortcutText, commandId);
        return SetShortcut(commandId, parsed.Key, parsed.Modifiers);
    }

    /// <summary>
    /// Removes a shortcut for a command.
    /// </summary>
    public void RemoveShortcut(string commandId)
    {
        if (_shortcuts.TryGetValue(commandId, out var shortcut))
        {
            _shortcuts.Remove(commandId);
            ShortcutChanged?.Invoke(this, shortcut);
        }
    }

    /// <summary>
    /// Resets a command to its default shortcut.
    /// </summary>
    public void ResetToDefault(string commandId)
    {
        if (_defaultShortcuts.TryGetValue(commandId, out var defaultShortcut))
        {
            _shortcuts[commandId] = defaultShortcut;
            ShortcutChanged?.Invoke(this, defaultShortcut);
        }
        else
        {
            RemoveShortcut(commandId);
        }
    }

    /// <summary>
    /// Resets all shortcuts to defaults.
    /// </summary>
    public void ResetAllToDefaults()
    {
        _shortcuts.Clear();
        foreach (var kvp in _defaultShortcuts)
        {
            _shortcuts[kvp.Key] = kvp.Value;
        }
        OnPropertyChanged(nameof(Shortcuts));
    }

    /// <summary>
    /// Gets the shortcut for a command.
    /// </summary>
    public KeyboardShortcut? GetShortcut(string commandId)
    {
        return _shortcuts.GetValueOrDefault(commandId);
    }

    /// <summary>
    /// Gets the command ID for a key press.
    /// </summary>
    public string? GetCommandForKey(string key, ModifierKeys modifiers)
    {
        foreach (var kvp in _shortcuts)
        {
            if (kvp.Value.Matches(key, modifiers))
                return kvp.Key;
        }
        return null;
    }

    /// <summary>
    /// Finds a conflicting shortcut.
    /// </summary>
    public ShortcutConflict? FindConflict(string commandId, string key, ModifierKeys modifiers)
    {
        foreach (var kvp in _shortcuts)
        {
            if (kvp.Key != commandId && kvp.Value.Matches(key, modifiers))
            {
                return new ShortcutConflict(
                    kvp.Value,
                    new KeyboardShortcut { CommandId = commandId, Key = key, Modifiers = modifiers },
                    _commandNames.GetValueOrDefault(kvp.Key, kvp.Key),
                    _commandNames.GetValueOrDefault(commandId, commandId)
                );
            }
        }
        return null;
    }

    /// <summary>
    /// Gets all shortcuts grouped by category.
    /// </summary>
    public Dictionary<string, List<(string CommandId, string CommandName, KeyboardShortcut? Shortcut)>> GetGroupedShortcuts()
    {
        var groups = new Dictionary<string, List<(string, string, KeyboardShortcut?)>>();

        foreach (var kvp in _commandNames)
        {
            var category = GetCategory(kvp.Key);
            if (!groups.ContainsKey(category))
                groups[category] = [];

            groups[category].Add((kvp.Key, kvp.Value, _shortcuts.GetValueOrDefault(kvp.Key)));
        }

        return groups;
    }

    /// <summary>
    /// Searches shortcuts.
    /// </summary>
    public IEnumerable<(string CommandId, string CommandName, KeyboardShortcut? Shortcut)> Search(string query)
    {
        query = query.ToLowerInvariant();
        return _commandNames
            .Where(kvp =>
                kvp.Key.Contains(query, StringComparison.OrdinalIgnoreCase) ||
                kvp.Value.Contains(query, StringComparison.OrdinalIgnoreCase) ||
                (_shortcuts.TryGetValue(kvp.Key, out var s) && s.DisplayText.Contains(query, StringComparison.OrdinalIgnoreCase)))
            .Select(kvp => (kvp.Key, kvp.Value, _shortcuts.GetValueOrDefault(kvp.Key)));
    }

    /// <summary>
    /// Applies a shortcut profile.
    /// </summary>
    public void ApplyProfile(ShortcutProfile profile)
    {
        var profileShortcuts = profile switch
        {
            ShortcutProfile.Illustrator => GetIllustratorProfile(),
            ShortcutProfile.Inkscape => GetInkscapeProfile(),
            ShortcutProfile.Figma => GetFigmaProfile(),
            _ => _defaultShortcuts
        };

        _shortcuts.Clear();
        foreach (var kvp in profileShortcuts)
        {
            _shortcuts[kvp.Key] = kvp.Value;
        }

        OnPropertyChanged(nameof(Shortcuts));
    }

    /// <summary>
    /// Exports shortcuts to JSON.
    /// </summary>
    public string ExportToJson()
    {
        var exportData = _shortcuts.ToDictionary(
            kvp => kvp.Key,
            kvp => kvp.Value.DisplayText
        );
        return JsonSerializer.Serialize(exportData, new JsonSerializerOptions { WriteIndented = true });
    }

    /// <summary>
    /// Imports shortcuts from JSON.
    /// </summary>
    public void ImportFromJson(string json)
    {
        var importData = JsonSerializer.Deserialize<Dictionary<string, string>>(json);
        if (importData == null) return;

        foreach (var kvp in importData)
        {
            if (_commandNames.ContainsKey(kvp.Key))
            {
                SetShortcut(kvp.Key, kvp.Value);
            }
        }
    }

    private static string GetCategory(string commandId)
    {
        var dotIndex = commandId.IndexOf('.');
        return dotIndex > 0 ? commandId[..dotIndex] : "General";
    }

    private Dictionary<string, KeyboardShortcut> GetIllustratorProfile()
    {
        var profile = new Dictionary<string, KeyboardShortcut>();
        foreach (var kvp in _defaultShortcuts) profile[kvp.Key] = kvp.Value;

        // Illustrator-specific overrides
        SetProfileShortcut(profile, "tool.select", "V", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.pen", "P", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.rectangle", "M", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.ellipse", "L", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.line", "\\", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.text", "T", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.zoom", "Z", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.pan", "H", ModifierKeys.None);
        SetProfileShortcut(profile, "view.zoomIn", "=", ModifierKeys.Ctrl);
        SetProfileShortcut(profile, "view.zoomOut", "-", ModifierKeys.Ctrl);

        return profile;
    }

    private Dictionary<string, KeyboardShortcut> GetInkscapeProfile()
    {
        var profile = new Dictionary<string, KeyboardShortcut>();
        foreach (var kvp in _defaultShortcuts) profile[kvp.Key] = kvp.Value;

        // Inkscape-specific overrides
        SetProfileShortcut(profile, "tool.select", "S", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.pen", "B", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.pencil", "P", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.rectangle", "R", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.ellipse", "E", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.text", "T", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.zoom", "Z", ModifierKeys.None);
        SetProfileShortcut(profile, "object.group", "G", ModifierKeys.Ctrl);
        SetProfileShortcut(profile, "object.ungroup", "G", ModifierKeys.Ctrl | ModifierKeys.Shift);

        return profile;
    }

    private Dictionary<string, KeyboardShortcut> GetFigmaProfile()
    {
        var profile = new Dictionary<string, KeyboardShortcut>();
        foreach (var kvp in _defaultShortcuts) profile[kvp.Key] = kvp.Value;

        // Figma-specific overrides
        SetProfileShortcut(profile, "tool.select", "V", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.pen", "P", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.rectangle", "R", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.ellipse", "O", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.line", "L", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.text", "T", ModifierKeys.None);
        SetProfileShortcut(profile, "tool.pan", "H", ModifierKeys.None);
        SetProfileShortcut(profile, "object.group", "G", ModifierKeys.Ctrl);
        SetProfileShortcut(profile, "object.duplicate", "D", ModifierKeys.Ctrl);
        SetProfileShortcut(profile, "view.zoomFit", "1", ModifierKeys.Shift);

        return profile;
    }

    private static void SetProfileShortcut(Dictionary<string, KeyboardShortcut> profile, string commandId, string key, ModifierKeys modifiers)
    {
        profile[commandId] = new KeyboardShortcut
        {
            CommandId = commandId,
            Key = key,
            Modifiers = modifiers
        };
    }

    /// <summary>
    /// Creates a manager with standard shortcuts registered.
    /// </summary>
    public static ShortcutManager CreateWithDefaults()
    {
        var manager = new ShortcutManager();

        // File
        manager.RegisterCommand("file.new", "New Document", "Ctrl+N");
        manager.RegisterCommand("file.open", "Open...", "Ctrl+O");
        manager.RegisterCommand("file.save", "Save", "Ctrl+S");
        manager.RegisterCommand("file.saveAs", "Save As...", "Ctrl+Shift+S");
        manager.RegisterCommand("file.export", "Export...", "Ctrl+E");
        manager.RegisterCommand("file.close", "Close", "Ctrl+W");

        // Edit
        manager.RegisterCommand("edit.undo", "Undo", "Ctrl+Z");
        manager.RegisterCommand("edit.redo", "Redo", "Ctrl+Y");
        manager.RegisterCommand("edit.cut", "Cut", "Ctrl+X");
        manager.RegisterCommand("edit.copy", "Copy", "Ctrl+C");
        manager.RegisterCommand("edit.paste", "Paste", "Ctrl+V");
        manager.RegisterCommand("edit.delete", "Delete", "Delete");
        manager.RegisterCommand("edit.selectAll", "Select All", "Ctrl+A");
        manager.RegisterCommand("edit.deselectAll", "Deselect All", "Escape");

        // View
        manager.RegisterCommand("view.zoomIn", "Zoom In", "Ctrl++");
        manager.RegisterCommand("view.zoomOut", "Zoom Out", "Ctrl+-");
        manager.RegisterCommand("view.zoomFit", "Zoom to Fit", "Ctrl+0");
        manager.RegisterCommand("view.zoom100", "Zoom to 100%", "Ctrl+1");
        manager.RegisterCommand("view.toggleGrid", "Toggle Grid", "Ctrl+'");
        manager.RegisterCommand("view.toggleRulers", "Toggle Rulers", "Ctrl+R");

        // Object
        manager.RegisterCommand("object.group", "Group", "Ctrl+G");
        manager.RegisterCommand("object.ungroup", "Ungroup", "Ctrl+Shift+G");
        manager.RegisterCommand("object.bringToFront", "Bring to Front", "Ctrl+Shift+]");
        manager.RegisterCommand("object.sendToBack", "Send to Back", "Ctrl+Shift+[");
        manager.RegisterCommand("object.duplicate", "Duplicate", "Ctrl+D");
        manager.RegisterCommand("object.lock", "Lock", "Ctrl+L");

        // Tools
        manager.RegisterCommand("tool.select", "Selection Tool", "V");
        manager.RegisterCommand("tool.pen", "Pen Tool", "P");
        manager.RegisterCommand("tool.pencil", "Pencil Tool", "N");
        manager.RegisterCommand("tool.rectangle", "Rectangle Tool", "R");
        manager.RegisterCommand("tool.ellipse", "Ellipse Tool", "E");
        manager.RegisterCommand("tool.line", "Line Tool", "L");
        manager.RegisterCommand("tool.text", "Text Tool", "T");
        manager.RegisterCommand("tool.zoom", "Zoom Tool", "Z");
        manager.RegisterCommand("tool.pan", "Pan Tool", "H");

        return manager;
    }
}
