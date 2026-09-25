namespace Bezier.Core.Services;

/// <summary>
/// Category of a command.
/// </summary>
public enum CommandCategory
{
    File,
    Edit,
    View,
    Object,
    Path,
    Text,
    Layer,
    Tools,
    Window,
    Help,
    Recent,
    Settings
}

/// <summary>
/// Represents a command that can be executed from the palette.
/// </summary>
public class PaletteCommand
{
    /// <summary>
    /// Gets the unique identifier.
    /// </summary>
    public string Id { get; init; } = string.Empty;

    /// <summary>
    /// Gets the display name.
    /// </summary>
    public string Name { get; init; } = string.Empty;

    /// <summary>
    /// Gets the description.
    /// </summary>
    public string? Description { get; init; }

    /// <summary>
    /// Gets the category.
    /// </summary>
    public CommandCategory Category { get; init; } = CommandCategory.Edit;

    /// <summary>
    /// Gets the keyboard shortcut (e.g., "Ctrl+S").
    /// </summary>
    public string? Shortcut { get; init; }

    /// <summary>
    /// Gets the icon name/path.
    /// </summary>
    public string? Icon { get; init; }

    /// <summary>
    /// Gets the action to execute.
    /// </summary>
    public Action? Execute { get; init; }

    /// <summary>
    /// Gets whether this command is currently enabled.
    /// </summary>
    public Func<bool>? CanExecute { get; init; }

    /// <summary>
    /// Gets search keywords for matching.
    /// </summary>
    public string[] Keywords { get; init; } = [];

    /// <summary>
    /// Gets whether the command is enabled.
    /// </summary>
    public bool IsEnabled => CanExecute?.Invoke() ?? true;
}

/// <summary>
/// Result of a fuzzy search match.
/// </summary>
public class CommandSearchResult
{
    /// <summary>
    /// Gets the matched command.
    /// </summary>
    public PaletteCommand Command { get; init; } = null!;

    /// <summary>
    /// Gets the match score (higher is better).
    /// </summary>
    public int Score { get; init; }

    /// <summary>
    /// Gets the indices of matched characters in the name.
    /// </summary>
    public int[] MatchedIndices { get; init; } = [];
}

/// <summary>
/// Service for managing the command palette.
/// </summary>
public class CommandPaletteService
{
    private readonly List<PaletteCommand> _commands = [];
    private readonly List<string> _recentCommandIds = [];
    private const int MaxRecentCommands = 10;

    /// <summary>
    /// Gets all registered commands.
    /// </summary>
    public IReadOnlyList<PaletteCommand> Commands => _commands;

    /// <summary>
    /// Gets recent command IDs.
    /// </summary>
    public IReadOnlyList<string> RecentCommandIds => _recentCommandIds;

    /// <summary>
    /// Event raised when a command is executed.
    /// </summary>
    public event EventHandler<PaletteCommand>? CommandExecuted;

    /// <summary>
    /// Registers a command.
    /// </summary>
    public void RegisterCommand(PaletteCommand command)
    {
        if (_commands.All(c => c.Id != command.Id))
        {
            _commands.Add(command);
        }
    }

    /// <summary>
    /// Registers multiple commands.
    /// </summary>
    public void RegisterCommands(IEnumerable<PaletteCommand> commands)
    {
        foreach (var command in commands)
        {
            RegisterCommand(command);
        }
    }

    /// <summary>
    /// Unregisters a command.
    /// </summary>
    public bool UnregisterCommand(string commandId)
    {
        return _commands.RemoveAll(c => c.Id == commandId) > 0;
    }

    /// <summary>
    /// Gets a command by ID.
    /// </summary>
    public PaletteCommand? GetCommand(string commandId)
    {
        return _commands.FirstOrDefault(c => c.Id == commandId);
    }

    /// <summary>
    /// Gets commands by category.
    /// </summary>
    public IEnumerable<PaletteCommand> GetByCategory(CommandCategory category)
    {
        return _commands.Where(c => c.Category == category);
    }

    /// <summary>
    /// Executes a command by ID.
    /// </summary>
    public bool ExecuteCommand(string commandId)
    {
        var command = GetCommand(commandId);
        if (command == null || !command.IsEnabled)
            return false;

        command.Execute?.Invoke();
        AddToRecent(commandId);
        CommandExecuted?.Invoke(this, command);
        return true;
    }

    /// <summary>
    /// Executes a command.
    /// </summary>
    public bool ExecuteCommand(PaletteCommand command)
    {
        if (!command.IsEnabled)
            return false;

        command.Execute?.Invoke();
        AddToRecent(command.Id);
        CommandExecuted?.Invoke(this, command);
        return true;
    }

    /// <summary>
    /// Searches commands using fuzzy matching.
    /// </summary>
    public IEnumerable<CommandSearchResult> Search(string query)
    {
        if (string.IsNullOrWhiteSpace(query))
        {
            // Return recent commands first, then all commands
            var recent = _recentCommandIds
                .Select(id => GetCommand(id))
                .Where(c => c != null)
                .Select(c => new CommandSearchResult { Command = c!, Score = 1000 });

            var others = _commands
                .Where(c => !_recentCommandIds.Contains(c.Id))
                .Select(c => new CommandSearchResult { Command = c, Score = 0 });

            return recent.Concat(others);
        }

        return _commands
            .Select(c => new { Command = c, Result = FuzzyMatch(query, c) })
            .Where(x => x.Result.Score > 0)
            .OrderByDescending(x => x.Result.Score)
            .ThenBy(x => x.Command.Name)
            .Select(x => new CommandSearchResult
            {
                Command = x.Command,
                Score = x.Result.Score,
                MatchedIndices = x.Result.MatchedIndices
            });
    }

    /// <summary>
    /// Gets recent commands.
    /// </summary>
    public IEnumerable<PaletteCommand> GetRecentCommands()
    {
        return _recentCommandIds
            .Select(id => GetCommand(id))
            .Where(c => c != null)
            .Cast<PaletteCommand>();
    }

    /// <summary>
    /// Clears recent command history.
    /// </summary>
    public void ClearRecentCommands()
    {
        _recentCommandIds.Clear();
    }

    private void AddToRecent(string commandId)
    {
        _recentCommandIds.Remove(commandId);
        _recentCommandIds.Insert(0, commandId);

        while (_recentCommandIds.Count > MaxRecentCommands)
        {
            _recentCommandIds.RemoveAt(_recentCommandIds.Count - 1);
        }
    }

    /// <summary>
    /// Performs fuzzy matching on a command.
    /// </summary>
    private static (int Score, int[] MatchedIndices) FuzzyMatch(string query, PaletteCommand command)
    {
        var bestResult = FuzzyMatchString(query, command.Name);

        // Also match against description
        if (command.Description != null)
        {
            var descResult = FuzzyMatchString(query, command.Description);
            if (descResult.Score > bestResult.Score)
            {
                bestResult = (descResult.Score / 2, []); // Lower weight for description matches
            }
        }

        // Also match against keywords
        foreach (var keyword in command.Keywords)
        {
            var keywordResult = FuzzyMatchString(query, keyword);
            if (keywordResult.Score > bestResult.Score)
            {
                bestResult = (keywordResult.Score, []);
            }
        }

        // Bonus for category match
        if (command.Category.ToString().Contains(query, StringComparison.OrdinalIgnoreCase))
        {
            bestResult = (bestResult.Score + 10, bestResult.MatchedIndices);
        }

        return bestResult;
    }

    /// <summary>
    /// Performs fuzzy string matching.
    /// </summary>
    public static (int Score, int[] MatchedIndices) FuzzyMatchString(string query, string target)
    {
        if (string.IsNullOrEmpty(query) || string.IsNullOrEmpty(target))
            return (0, []);

        query = query.ToLowerInvariant();
        var targetLower = target.ToLowerInvariant();

        // Exact match gets highest score
        if (targetLower == query)
            return (1000, Enumerable.Range(0, target.Length).ToArray());

        // Starts with gets high score
        if (targetLower.StartsWith(query))
            return (900 + query.Length, Enumerable.Range(0, query.Length).ToArray());

        // Contains gets medium score
        var containsIndex = targetLower.IndexOf(query);
        if (containsIndex >= 0)
            return (700 + query.Length, Enumerable.Range(containsIndex, query.Length).ToArray());

        // Fuzzy match - characters must appear in order
        var matchedIndices = new List<int>();
        var queryIndex = 0;
        var score = 0;
        var consecutiveBonus = 0;
        var lastMatchIndex = -1;

        for (var i = 0; i < target.Length && queryIndex < query.Length; i++)
        {
            if (char.ToLowerInvariant(target[i]) == query[queryIndex])
            {
                matchedIndices.Add(i);

                // Base score for match
                score += 10;

                // Bonus for consecutive matches
                if (lastMatchIndex == i - 1)
                {
                    consecutiveBonus++;
                    score += consecutiveBonus * 5;
                }
                else
                {
                    consecutiveBonus = 0;
                }

                // Bonus for matching at word boundaries
                if (i == 0 || !char.IsLetterOrDigit(target[i - 1]))
                {
                    score += 20;
                }

                // Bonus for matching uppercase (camelCase/PascalCase)
                if (char.IsUpper(target[i]))
                {
                    score += 10;
                }

                lastMatchIndex = i;
                queryIndex++;
            }
        }

        // Only return score if all query characters were matched
        if (queryIndex == query.Length)
        {
            // Penalty for unmatched characters at start
            score -= matchedIndices[0] * 2;

            // Penalty for spread out matches
            var spread = matchedIndices[^1] - matchedIndices[0] - query.Length + 1;
            score -= spread;

            return (Math.Max(1, score), [.. matchedIndices]);
        }

        return (0, []);
    }

    /// <summary>
    /// Creates standard editor commands.
    /// </summary>
    public static IEnumerable<PaletteCommand> CreateStandardCommands()
    {
        return
        [
            // File commands
            new PaletteCommand { Id = "file.new", Name = "New Document", Category = CommandCategory.File, Shortcut = "Ctrl+N", Keywords = ["create", "blank"] },
            new PaletteCommand { Id = "file.open", Name = "Open...", Category = CommandCategory.File, Shortcut = "Ctrl+O", Keywords = ["load", "import"] },
            new PaletteCommand { Id = "file.save", Name = "Save", Category = CommandCategory.File, Shortcut = "Ctrl+S" },
            new PaletteCommand { Id = "file.saveAs", Name = "Save As...", Category = CommandCategory.File, Shortcut = "Ctrl+Shift+S" },
            new PaletteCommand { Id = "file.export", Name = "Export...", Category = CommandCategory.File, Shortcut = "Ctrl+E", Keywords = ["png", "svg", "jpg"] },
            new PaletteCommand { Id = "file.close", Name = "Close", Category = CommandCategory.File, Shortcut = "Ctrl+W" },

            // Edit commands
            new PaletteCommand { Id = "edit.undo", Name = "Undo", Category = CommandCategory.Edit, Shortcut = "Ctrl+Z" },
            new PaletteCommand { Id = "edit.redo", Name = "Redo", Category = CommandCategory.Edit, Shortcut = "Ctrl+Y", Keywords = ["repeat"] },
            new PaletteCommand { Id = "edit.cut", Name = "Cut", Category = CommandCategory.Edit, Shortcut = "Ctrl+X" },
            new PaletteCommand { Id = "edit.copy", Name = "Copy", Category = CommandCategory.Edit, Shortcut = "Ctrl+C", Keywords = ["duplicate"] },
            new PaletteCommand { Id = "edit.paste", Name = "Paste", Category = CommandCategory.Edit, Shortcut = "Ctrl+V" },
            new PaletteCommand { Id = "edit.delete", Name = "Delete", Category = CommandCategory.Edit, Shortcut = "Delete", Keywords = ["remove"] },
            new PaletteCommand { Id = "edit.selectAll", Name = "Select All", Category = CommandCategory.Edit, Shortcut = "Ctrl+A" },
            new PaletteCommand { Id = "edit.deselectAll", Name = "Deselect All", Category = CommandCategory.Edit, Shortcut = "Ctrl+D" },

            // View commands
            new PaletteCommand { Id = "view.zoomIn", Name = "Zoom In", Category = CommandCategory.View, Shortcut = "Ctrl++", Keywords = ["magnify", "enlarge"] },
            new PaletteCommand { Id = "view.zoomOut", Name = "Zoom Out", Category = CommandCategory.View, Shortcut = "Ctrl+-", Keywords = ["shrink"] },
            new PaletteCommand { Id = "view.zoomFit", Name = "Zoom to Fit", Category = CommandCategory.View, Shortcut = "Ctrl+0", Keywords = ["fit", "all"] },
            new PaletteCommand { Id = "view.zoomSelection", Name = "Zoom to Selection", Category = CommandCategory.View, Shortcut = "Ctrl+1" },
            new PaletteCommand { Id = "view.zoom100", Name = "Zoom to 100%", Category = CommandCategory.View, Shortcut = "Ctrl+2", Keywords = ["actual", "real"] },
            new PaletteCommand { Id = "view.toggleGrid", Name = "Toggle Grid", Category = CommandCategory.View, Shortcut = "Ctrl+'", Keywords = ["show", "hide"] },
            new PaletteCommand { Id = "view.toggleRulers", Name = "Toggle Rulers", Category = CommandCategory.View, Shortcut = "Ctrl+R" },
            new PaletteCommand { Id = "view.toggleGuides", Name = "Toggle Guides", Category = CommandCategory.View },

            // Object commands
            new PaletteCommand { Id = "object.group", Name = "Group", Category = CommandCategory.Object, Shortcut = "Ctrl+G", Keywords = ["combine"] },
            new PaletteCommand { Id = "object.ungroup", Name = "Ungroup", Category = CommandCategory.Object, Shortcut = "Ctrl+Shift+G", Keywords = ["separate"] },
            new PaletteCommand { Id = "object.bringToFront", Name = "Bring to Front", Category = CommandCategory.Object, Shortcut = "Ctrl+Shift+]", Keywords = ["top", "forward"] },
            new PaletteCommand { Id = "object.sendToBack", Name = "Send to Back", Category = CommandCategory.Object, Shortcut = "Ctrl+Shift+[", Keywords = ["bottom", "behind"] },
            new PaletteCommand { Id = "object.bringForward", Name = "Bring Forward", Category = CommandCategory.Object, Shortcut = "Ctrl+]" },
            new PaletteCommand { Id = "object.sendBackward", Name = "Send Backward", Category = CommandCategory.Object, Shortcut = "Ctrl+[" },
            new PaletteCommand { Id = "object.duplicate", Name = "Duplicate", Category = CommandCategory.Object, Shortcut = "Ctrl+D", Keywords = ["copy", "clone"] },
            new PaletteCommand { Id = "object.lock", Name = "Lock", Category = CommandCategory.Object, Shortcut = "Ctrl+L" },
            new PaletteCommand { Id = "object.unlock", Name = "Unlock All", Category = CommandCategory.Object, Shortcut = "Ctrl+Shift+L" },
            new PaletteCommand { Id = "object.hide", Name = "Hide", Category = CommandCategory.Object, Shortcut = "Ctrl+H" },
            new PaletteCommand { Id = "object.showAll", Name = "Show All", Category = CommandCategory.Object, Shortcut = "Ctrl+Shift+H" },

            // Path commands
            new PaletteCommand { Id = "path.union", Name = "Union", Category = CommandCategory.Path, Keywords = ["boolean", "combine", "add"] },
            new PaletteCommand { Id = "path.subtract", Name = "Subtract", Category = CommandCategory.Path, Keywords = ["boolean", "minus", "cut"] },
            new PaletteCommand { Id = "path.intersect", Name = "Intersect", Category = CommandCategory.Path, Keywords = ["boolean", "common"] },
            new PaletteCommand { Id = "path.exclude", Name = "Exclude", Category = CommandCategory.Path, Keywords = ["boolean", "xor"] },
            new PaletteCommand { Id = "path.simplify", Name = "Simplify Path", Category = CommandCategory.Path, Keywords = ["reduce", "nodes"] },
            new PaletteCommand { Id = "path.outline", Name = "Outline Stroke", Category = CommandCategory.Path, Keywords = ["expand"] },
            new PaletteCommand { Id = "path.reverse", Name = "Reverse Path", Category = CommandCategory.Path, Keywords = ["direction"] },

            // Align commands
            new PaletteCommand { Id = "align.left", Name = "Align Left", Category = CommandCategory.Object, Keywords = ["alignment"] },
            new PaletteCommand { Id = "align.center", Name = "Align Center", Category = CommandCategory.Object, Keywords = ["alignment", "horizontal"] },
            new PaletteCommand { Id = "align.right", Name = "Align Right", Category = CommandCategory.Object, Keywords = ["alignment"] },
            new PaletteCommand { Id = "align.top", Name = "Align Top", Category = CommandCategory.Object, Keywords = ["alignment"] },
            new PaletteCommand { Id = "align.middle", Name = "Align Middle", Category = CommandCategory.Object, Keywords = ["alignment", "vertical"] },
            new PaletteCommand { Id = "align.bottom", Name = "Align Bottom", Category = CommandCategory.Object, Keywords = ["alignment"] },

            // Tools
            new PaletteCommand { Id = "tool.select", Name = "Selection Tool", Category = CommandCategory.Tools, Shortcut = "V", Keywords = ["pointer", "move"] },
            new PaletteCommand { Id = "tool.pen", Name = "Pen Tool", Category = CommandCategory.Tools, Shortcut = "P", Keywords = ["path", "draw", "bezier"] },
            new PaletteCommand { Id = "tool.pencil", Name = "Pencil Tool", Category = CommandCategory.Tools, Shortcut = "N", Keywords = ["freehand", "draw"] },
            new PaletteCommand { Id = "tool.rectangle", Name = "Rectangle Tool", Category = CommandCategory.Tools, Shortcut = "R", Keywords = ["shape", "square"] },
            new PaletteCommand { Id = "tool.ellipse", Name = "Ellipse Tool", Category = CommandCategory.Tools, Shortcut = "E", Keywords = ["shape", "circle", "oval"] },
            new PaletteCommand { Id = "tool.line", Name = "Line Tool", Category = CommandCategory.Tools, Shortcut = "L", Keywords = ["shape"] },
            new PaletteCommand { Id = "tool.text", Name = "Text Tool", Category = CommandCategory.Tools, Shortcut = "T", Keywords = ["type", "font"] },
            new PaletteCommand { Id = "tool.zoom", Name = "Zoom Tool", Category = CommandCategory.Tools, Shortcut = "Z", Keywords = ["magnify"] },
            new PaletteCommand { Id = "tool.pan", Name = "Pan Tool", Category = CommandCategory.Tools, Shortcut = "H", Keywords = ["hand", "move"] },

            // Window
            new PaletteCommand { Id = "window.layers", Name = "Layers Panel", Category = CommandCategory.Window, Keywords = ["show", "panel"] },
            new PaletteCommand { Id = "window.properties", Name = "Properties Panel", Category = CommandCategory.Window, Keywords = ["show", "panel"] },
            new PaletteCommand { Id = "window.symbols", Name = "Symbols Panel", Category = CommandCategory.Window, Keywords = ["show", "panel", "library"] },

            // Help
            new PaletteCommand { Id = "help.about", Name = "About", Category = CommandCategory.Help },
            new PaletteCommand { Id = "help.shortcuts", Name = "Keyboard Shortcuts", Category = CommandCategory.Help, Keywords = ["keys", "hotkeys"] },
            new PaletteCommand { Id = "help.docs", Name = "Documentation", Category = CommandCategory.Help, Keywords = ["manual", "guide"] },

            // Settings
            new PaletteCommand { Id = "settings.preferences", Name = "Preferences", Category = CommandCategory.Settings, Shortcut = "Ctrl+,", Keywords = ["options", "config"] },
            new PaletteCommand { Id = "settings.theme", Name = "Change Theme", Category = CommandCategory.Settings, Keywords = ["dark", "light", "color"] },
        ];
    }
}
