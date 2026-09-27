namespace Bezier.Tests;

using Bezier.Core.Services;

public class KeyboardShortcutTests
{
    [Fact]
    public void KeyboardShortcut_DefaultValues()
    {
        var shortcut = new KeyboardShortcut();

        Assert.Equal(string.Empty, shortcut.Key);
        Assert.Equal(ModifierKeys.None, shortcut.Modifiers);
        Assert.Equal(string.Empty, shortcut.CommandId);
    }

    [Fact]
    public void KeyboardShortcut_DisplayText_ShowsKeyOnly()
    {
        var shortcut = new KeyboardShortcut { Key = "A" };

        Assert.Equal("A", shortcut.DisplayText);
    }

    [Fact]
    public void KeyboardShortcut_DisplayText_ShowsModifiersAndKey()
    {
        var shortcut = new KeyboardShortcut
        {
            Key = "S",
            Modifiers = ModifierKeys.Ctrl
        };

        Assert.Equal("Ctrl+S", shortcut.DisplayText);
    }

    [Fact]
    public void KeyboardShortcut_DisplayText_ShowsMultipleModifiers()
    {
        var shortcut = new KeyboardShortcut
        {
            Key = "S",
            Modifiers = ModifierKeys.Ctrl | ModifierKeys.Shift
        };

        Assert.Equal("Ctrl+Shift+S", shortcut.DisplayText);
    }

    [Fact]
    public void KeyboardShortcut_DisplayText_ShowsAllModifiers()
    {
        var shortcut = new KeyboardShortcut
        {
            Key = "A",
            Modifiers = ModifierKeys.Ctrl | ModifierKeys.Alt | ModifierKeys.Shift | ModifierKeys.Win
        };

        Assert.Equal("Ctrl+Alt+Shift+Win+A", shortcut.DisplayText);
    }

    [Fact]
    public void KeyboardShortcut_Matches_ReturnsTrue_WhenEqual()
    {
        var shortcut = new KeyboardShortcut
        {
            Key = "S",
            Modifiers = ModifierKeys.Ctrl
        };

        Assert.True(shortcut.Matches("S", ModifierKeys.Ctrl));
        Assert.True(shortcut.Matches("s", ModifierKeys.Ctrl)); // Case insensitive
    }

    [Fact]
    public void KeyboardShortcut_Matches_ReturnsFalse_WhenDifferent()
    {
        var shortcut = new KeyboardShortcut
        {
            Key = "S",
            Modifiers = ModifierKeys.Ctrl
        };

        Assert.False(shortcut.Matches("A", ModifierKeys.Ctrl));
        Assert.False(shortcut.Matches("S", ModifierKeys.Alt));
        Assert.False(shortcut.Matches("S", ModifierKeys.None));
    }

    [Fact]
    public void KeyboardShortcut_Parse_SingleKey()
    {
        var shortcut = KeyboardShortcut.Parse("V");

        Assert.Equal("V", shortcut.Key);
        Assert.Equal(ModifierKeys.None, shortcut.Modifiers);
    }

    [Fact]
    public void KeyboardShortcut_Parse_CtrlKey()
    {
        var shortcut = KeyboardShortcut.Parse("Ctrl+S");

        Assert.Equal("S", shortcut.Key);
        Assert.Equal(ModifierKeys.Ctrl, shortcut.Modifiers);
    }

    [Fact]
    public void KeyboardShortcut_Parse_MultipleModifiers()
    {
        var shortcut = KeyboardShortcut.Parse("Ctrl+Shift+G");

        Assert.Equal("G", shortcut.Key);
        Assert.Equal(ModifierKeys.Ctrl | ModifierKeys.Shift, shortcut.Modifiers);
    }

    [Fact]
    public void KeyboardShortcut_Parse_ControlVariant()
    {
        var shortcut = KeyboardShortcut.Parse("Control+S");

        Assert.Equal(ModifierKeys.Ctrl, shortcut.Modifiers);
    }

    [Fact]
    public void KeyboardShortcut_Parse_SetsCommandId()
    {
        var shortcut = KeyboardShortcut.Parse("Ctrl+S", "file.save");

        Assert.Equal("file.save", shortcut.CommandId);
    }
}

public class ShortcutManagerTests
{
    private readonly ShortcutManager _manager;

    public ShortcutManagerTests()
    {
        _manager = new ShortcutManager();
    }

    [Fact]
    public void RegisterCommand_AddsToRegistry()
    {
        _manager.RegisterCommand("test.command", "Test Command", "Ctrl+T");

        var shortcut = _manager.GetShortcut("test.command");

        Assert.NotNull(shortcut);
        Assert.Equal("T", shortcut.Key);
        Assert.Equal(ModifierKeys.Ctrl, shortcut.Modifiers);
    }

    [Fact]
    public void RegisterCommand_WithoutShortcut_RegistersCommand()
    {
        _manager.RegisterCommand("test.command", "Test Command");

        var shortcut = _manager.GetShortcut("test.command");

        Assert.Null(shortcut);
    }

    [Fact]
    public void SetShortcut_UpdatesShortcut()
    {
        _manager.RegisterCommand("test.command", "Test Command", "Ctrl+T");

        _manager.SetShortcut("test.command", "A", ModifierKeys.Ctrl | ModifierKeys.Shift);

        var shortcut = _manager.GetShortcut("test.command");
        Assert.Equal("A", shortcut?.Key);
        Assert.Equal(ModifierKeys.Ctrl | ModifierKeys.Shift, shortcut?.Modifiers);
    }

    [Fact]
    public void SetShortcut_FromString_Works()
    {
        _manager.RegisterCommand("test.command", "Test Command");

        _manager.SetShortcut("test.command", "Ctrl+Shift+A");

        var shortcut = _manager.GetShortcut("test.command");
        Assert.Equal("A", shortcut?.Key);
        Assert.Equal(ModifierKeys.Ctrl | ModifierKeys.Shift, shortcut?.Modifiers);
    }

    [Fact]
    public void SetShortcut_DetectsConflict()
    {
        _manager.RegisterCommand("cmd1", "Command 1", "Ctrl+S");
        _manager.RegisterCommand("cmd2", "Command 2");

        var conflict = _manager.SetShortcut("cmd2", "S", ModifierKeys.Ctrl);

        Assert.NotNull(conflict);
        Assert.Equal("cmd1", conflict.Existing.CommandId);
        Assert.Equal("cmd2", conflict.New.CommandId);
    }

    [Fact]
    public void SetShortcut_RaisesConflictEvent()
    {
        _manager.RegisterCommand("cmd1", "Command 1", "Ctrl+S");
        _manager.RegisterCommand("cmd2", "Command 2");
        ShortcutConflict? detectedConflict = null;
        _manager.ConflictDetected += (_, c) => detectedConflict = c;

        _manager.SetShortcut("cmd2", "S", ModifierKeys.Ctrl);

        Assert.NotNull(detectedConflict);
    }

    [Fact]
    public void RemoveShortcut_RemovesFromRegistry()
    {
        _manager.RegisterCommand("test.command", "Test Command", "Ctrl+T");

        _manager.RemoveShortcut("test.command");

        Assert.Null(_manager.GetShortcut("test.command"));
    }

    [Fact]
    public void ResetToDefault_RestoresDefaultShortcut()
    {
        _manager.RegisterCommand("test.command", "Test Command", "Ctrl+T");
        _manager.SetShortcut("test.command", "A", ModifierKeys.None);

        _manager.ResetToDefault("test.command");

        var shortcut = _manager.GetShortcut("test.command");
        Assert.Equal("T", shortcut?.Key);
        Assert.Equal(ModifierKeys.Ctrl, shortcut?.Modifiers);
    }

    [Fact]
    public void ResetAllToDefaults_RestoresAllShortcuts()
    {
        _manager.RegisterCommand("cmd1", "Command 1", "Ctrl+A");
        _manager.RegisterCommand("cmd2", "Command 2", "Ctrl+B");
        _manager.SetShortcut("cmd1", "X", ModifierKeys.None);
        _manager.SetShortcut("cmd2", "Y", ModifierKeys.None);

        _manager.ResetAllToDefaults();

        Assert.Equal("A", _manager.GetShortcut("cmd1")?.Key);
        Assert.Equal("B", _manager.GetShortcut("cmd2")?.Key);
    }

    [Fact]
    public void GetCommandForKey_ReturnsCommandId()
    {
        _manager.RegisterCommand("test.command", "Test Command", "Ctrl+T");

        var commandId = _manager.GetCommandForKey("T", ModifierKeys.Ctrl);

        Assert.Equal("test.command", commandId);
    }

    [Fact]
    public void GetCommandForKey_ReturnsNull_WhenNotFound()
    {
        var commandId = _manager.GetCommandForKey("X", ModifierKeys.Ctrl);

        Assert.Null(commandId);
    }

    [Fact]
    public void FindConflict_ReturnsConflict_WhenExists()
    {
        _manager.RegisterCommand("cmd1", "Command 1", "Ctrl+S");

        var conflict = _manager.FindConflict("cmd2", "S", ModifierKeys.Ctrl);

        Assert.NotNull(conflict);
        Assert.Equal("cmd1", conflict.Existing.CommandId);
    }

    [Fact]
    public void FindConflict_ReturnsNull_WhenNoConflict()
    {
        _manager.RegisterCommand("cmd1", "Command 1", "Ctrl+S");

        var conflict = _manager.FindConflict("cmd2", "A", ModifierKeys.Ctrl);

        Assert.Null(conflict);
    }

    [Fact]
    public void GetGroupedShortcuts_GroupsByCategory()
    {
        _manager.RegisterCommand("file.new", "New", "Ctrl+N");
        _manager.RegisterCommand("file.save", "Save", "Ctrl+S");
        _manager.RegisterCommand("edit.undo", "Undo", "Ctrl+Z");

        var groups = _manager.GetGroupedShortcuts();

        Assert.Contains("file", groups.Keys);
        Assert.Contains("edit", groups.Keys);
        Assert.Equal(2, groups["file"].Count);
        Assert.Single(groups["edit"]);
    }

    [Fact]
    public void Search_FindsByCommandName()
    {
        _manager.RegisterCommand("file.save", "Save Document", "Ctrl+S");

        var results = _manager.Search("save").ToList();

        Assert.Single(results);
        Assert.Equal("file.save", results[0].CommandId);
    }

    [Fact]
    public void Search_FindsByShortcutText()
    {
        _manager.RegisterCommand("file.save", "Save", "Ctrl+S");

        var results = _manager.Search("ctrl").ToList();

        Assert.Single(results);
    }

    [Fact]
    public void ApplyProfile_ChangesShortcuts()
    {
        _manager.RegisterCommand("tool.rectangle", "Rectangle", "R");

        _manager.ApplyProfile(ShortcutProfile.Illustrator);

        var shortcut = _manager.GetShortcut("tool.rectangle");
        Assert.Equal("M", shortcut?.Key); // Illustrator uses M for rectangle
    }

    [Fact]
    public void CurrentProfile_AppliesProfileOnSet()
    {
        _manager.RegisterCommand("tool.ellipse", "Ellipse", "E");

        _manager.CurrentProfile = ShortcutProfile.Figma;

        var shortcut = _manager.GetShortcut("tool.ellipse");
        Assert.Equal("O", shortcut?.Key); // Figma uses O for ellipse
    }

    [Fact]
    public void ExportToJson_CreatesValidJson()
    {
        _manager.RegisterCommand("file.save", "Save", "Ctrl+S");

        var json = _manager.ExportToJson();

        Assert.Contains("file.save", json);
        // JSON may escape + as \u002B
        Assert.True(json.Contains("Ctrl+S") || json.Contains("Ctrl\\u002BS"));
    }

    [Fact]
    public void ImportFromJson_RestoresShortcuts()
    {
        _manager.RegisterCommand("file.save", "Save");
        var json = """{"file.save": "Ctrl+Shift+S"}""";

        _manager.ImportFromJson(json);

        var shortcut = _manager.GetShortcut("file.save");
        Assert.Equal("S", shortcut?.Key);
        Assert.Equal(ModifierKeys.Ctrl | ModifierKeys.Shift, shortcut?.Modifiers);
    }

    [Fact]
    public void ShortcutChanged_EventRaised()
    {
        _manager.RegisterCommand("test.command", "Test");
        KeyboardShortcut? changedShortcut = null;
        _manager.ShortcutChanged += (_, s) => changedShortcut = s;

        _manager.SetShortcut("test.command", "A", ModifierKeys.Ctrl);

        Assert.NotNull(changedShortcut);
        Assert.Equal("A", changedShortcut.Key);
    }

    [Fact]
    public void CreateWithDefaults_RegistersStandardShortcuts()
    {
        var manager = ShortcutManager.CreateWithDefaults();

        Assert.NotNull(manager.GetShortcut("file.save"));
        Assert.NotNull(manager.GetShortcut("edit.undo"));
        Assert.NotNull(manager.GetShortcut("tool.select"));
    }
}

public class ShortcutConflictTests
{
    [Fact]
    public void ShortcutConflict_ContainsAllInfo()
    {
        var existing = new KeyboardShortcut { CommandId = "cmd1", Key = "S", Modifiers = ModifierKeys.Ctrl };
        var newShortcut = new KeyboardShortcut { CommandId = "cmd2", Key = "S", Modifiers = ModifierKeys.Ctrl };

        var conflict = new ShortcutConflict(existing, newShortcut, "Command 1", "Command 2");

        Assert.Equal("cmd1", conflict.Existing.CommandId);
        Assert.Equal("cmd2", conflict.New.CommandId);
        Assert.Equal("Command 1", conflict.ExistingCommandName);
        Assert.Equal("Command 2", conflict.NewCommandName);
    }
}

public class ShortcutProfileTests
{
    [Theory]
    [InlineData(ShortcutProfile.Default)]
    [InlineData(ShortcutProfile.Illustrator)]
    [InlineData(ShortcutProfile.Inkscape)]
    [InlineData(ShortcutProfile.Figma)]
    public void AllProfiles_AreValid(ShortcutProfile profile)
    {
        var manager = ShortcutManager.CreateWithDefaults();

        manager.ApplyProfile(profile);

        // Should not throw and should have shortcuts
        Assert.True(manager.Shortcuts.Count > 0);
    }
}
