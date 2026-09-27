namespace Bezier.Tests;

using Bezier.Core.Services;

public class CommandPaletteServiceTests
{
    private readonly CommandPaletteService _service;

    public CommandPaletteServiceTests()
    {
        _service = new CommandPaletteService();
    }

    [Fact]
    public void RegisterCommand_AddsToCollection()
    {
        var command = new PaletteCommand { Id = "test.command", Name = "Test Command" };

        _service.RegisterCommand(command);

        Assert.Single(_service.Commands);
        Assert.Contains(command, _service.Commands);
    }

    [Fact]
    public void RegisterCommand_IgnoresDuplicateIds()
    {
        var command1 = new PaletteCommand { Id = "test.command", Name = "Test 1" };
        var command2 = new PaletteCommand { Id = "test.command", Name = "Test 2" };

        _service.RegisterCommand(command1);
        _service.RegisterCommand(command2);

        Assert.Single(_service.Commands);
        Assert.Equal("Test 1", _service.Commands[0].Name);
    }

    [Fact]
    public void RegisterCommands_AddsMultiple()
    {
        var commands = new[]
        {
            new PaletteCommand { Id = "cmd1", Name = "Command 1" },
            new PaletteCommand { Id = "cmd2", Name = "Command 2" },
        };

        _service.RegisterCommands(commands);

        Assert.Equal(2, _service.Commands.Count);
    }

    [Fact]
    public void UnregisterCommand_RemovesFromCollection()
    {
        var command = new PaletteCommand { Id = "test.command", Name = "Test" };
        _service.RegisterCommand(command);

        var removed = _service.UnregisterCommand("test.command");

        Assert.True(removed);
        Assert.Empty(_service.Commands);
    }

    [Fact]
    public void GetCommand_FindsById()
    {
        var command = new PaletteCommand { Id = "test.command", Name = "Test" };
        _service.RegisterCommand(command);

        var found = _service.GetCommand("test.command");

        Assert.Same(command, found);
    }

    [Fact]
    public void GetCommand_ReturnsNull_WhenNotFound()
    {
        var found = _service.GetCommand("nonexistent");

        Assert.Null(found);
    }

    [Fact]
    public void GetByCategory_FiltersCorrectly()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "file.new", Name = "New", Category = CommandCategory.File });
        _service.RegisterCommand(new PaletteCommand { Id = "edit.undo", Name = "Undo", Category = CommandCategory.Edit });
        _service.RegisterCommand(new PaletteCommand { Id = "file.open", Name = "Open", Category = CommandCategory.File });

        var fileCommands = _service.GetByCategory(CommandCategory.File).ToList();

        Assert.Equal(2, fileCommands.Count);
        Assert.All(fileCommands, c => Assert.Equal(CommandCategory.File, c.Category));
    }

    [Fact]
    public void ExecuteCommand_CallsAction()
    {
        var executed = false;
        var command = new PaletteCommand
        {
            Id = "test.command",
            Name = "Test",
            Execute = () => executed = true
        };
        _service.RegisterCommand(command);

        var result = _service.ExecuteCommand("test.command");

        Assert.True(result);
        Assert.True(executed);
    }

    [Fact]
    public void ExecuteCommand_ReturnsFalse_WhenDisabled()
    {
        var command = new PaletteCommand
        {
            Id = "test.command",
            Name = "Test",
            CanExecute = () => false,
            Execute = () => { }
        };
        _service.RegisterCommand(command);

        var result = _service.ExecuteCommand("test.command");

        Assert.False(result);
    }

    [Fact]
    public void ExecuteCommand_AddsToRecent()
    {
        var command = new PaletteCommand { Id = "test.command", Name = "Test", Execute = () => { } };
        _service.RegisterCommand(command);

        _service.ExecuteCommand("test.command");

        Assert.Contains("test.command", _service.RecentCommandIds);
    }

    [Fact]
    public void ExecuteCommand_RaisesEvent()
    {
        var command = new PaletteCommand { Id = "test.command", Name = "Test", Execute = () => { } };
        _service.RegisterCommand(command);
        PaletteCommand? executedCommand = null;
        _service.CommandExecuted += (_, c) => executedCommand = c;

        _service.ExecuteCommand("test.command");

        Assert.Same(command, executedCommand);
    }

    [Fact]
    public void Search_ReturnsAllCommands_WhenQueryEmpty()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Command 1" });
        _service.RegisterCommand(new PaletteCommand { Id = "cmd2", Name = "Command 2" });

        var results = _service.Search("").ToList();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public void Search_FindsExactMatch()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Save" });
        _service.RegisterCommand(new PaletteCommand { Id = "cmd2", Name = "Save As" });

        var results = _service.Search("Save").ToList();

        Assert.True(results.Count > 0);
        Assert.Equal("Save", results[0].Command.Name);
    }

    [Fact]
    public void Search_FindsPartialMatch()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Save Document" });

        var results = _service.Search("doc").ToList();

        Assert.Single(results);
    }

    [Fact]
    public void Search_FindsFuzzyMatch()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Save Document" });

        var results = _service.Search("sv").ToList();

        Assert.Single(results);
    }

    [Fact]
    public void Search_FindsByKeywords()
    {
        _service.RegisterCommand(new PaletteCommand
        {
            Id = "cmd1",
            Name = "Export",
            Keywords = ["png", "jpg", "save"]
        });

        var results = _service.Search("png").ToList();

        Assert.Single(results);
    }

    [Fact]
    public void Search_ReturnsMatchedIndices()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Save" });

        var results = _service.Search("Save").ToList();

        Assert.True(results[0].MatchedIndices.Length > 0);
    }

    [Fact]
    public void Search_OrdersByScore()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Save" });
        _service.RegisterCommand(new PaletteCommand { Id = "cmd2", Name = "Save As" });
        _service.RegisterCommand(new PaletteCommand { Id = "cmd3", Name = "Save All" });

        var results = _service.Search("Save").ToList();

        Assert.Equal("Save", results[0].Command.Name); // Exact match first
    }

    [Fact]
    public void GetRecentCommands_ReturnsRecentFirst()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Command 1", Execute = () => { } });
        _service.RegisterCommand(new PaletteCommand { Id = "cmd2", Name = "Command 2", Execute = () => { } });

        _service.ExecuteCommand("cmd1");
        _service.ExecuteCommand("cmd2");

        var recent = _service.GetRecentCommands().ToList();

        Assert.Equal("cmd2", recent[0].Id);
        Assert.Equal("cmd1", recent[1].Id);
    }

    [Fact]
    public void ClearRecentCommands_ClearsHistory()
    {
        _service.RegisterCommand(new PaletteCommand { Id = "cmd1", Name = "Command 1", Execute = () => { } });
        _service.ExecuteCommand("cmd1");

        _service.ClearRecentCommands();

        Assert.Empty(_service.RecentCommandIds);
    }

    [Fact]
    public void CreateStandardCommands_ReturnsCommands()
    {
        var commands = CommandPaletteService.CreateStandardCommands().ToList();

        Assert.True(commands.Count > 0);
        Assert.Contains(commands, c => c.Id == "file.new");
        Assert.Contains(commands, c => c.Id == "edit.undo");
        Assert.Contains(commands, c => c.Id == "tool.select");
    }
}

public class FuzzyMatchTests
{
    [Theory]
    [InlineData("save", "Save", 1000)] // Exact match
    [InlineData("sav", "Save", 903)] // Starts with
    [InlineData("ave", "Save", 703)] // Contains
    public void FuzzyMatchString_ScoresCorrectly(string query, string target, int expectedScore)
    {
        var (score, _) = CommandPaletteService.FuzzyMatchString(query, target);

        Assert.Equal(expectedScore, score);
    }

    [Fact]
    public void FuzzyMatchString_ReturnsZero_WhenNoMatch()
    {
        var (score, indices) = CommandPaletteService.FuzzyMatchString("xyz", "Save");

        Assert.Equal(0, score);
        Assert.Empty(indices);
    }

    [Fact]
    public void FuzzyMatchString_MatchesCamelCase()
    {
        var (score, indices) = CommandPaletteService.FuzzyMatchString("sd", "SaveDocument");

        Assert.True(score > 0);
        Assert.Contains(0, indices); // S
        Assert.Contains(4, indices); // D
    }

    [Fact]
    public void FuzzyMatchString_ReturnsMatchedIndices()
    {
        var (_, indices) = CommandPaletteService.FuzzyMatchString("save", "Save");

        Assert.Equal(4, indices.Length);
        Assert.Equal([0, 1, 2, 3], indices);
    }

    [Fact]
    public void FuzzyMatchString_HandlesEmptyStrings()
    {
        var (score1, _) = CommandPaletteService.FuzzyMatchString("", "Save");
        var (score2, _) = CommandPaletteService.FuzzyMatchString("save", "");

        Assert.Equal(0, score1);
        Assert.Equal(0, score2);
    }

    [Fact]
    public void FuzzyMatchString_BonusForWordBoundary()
    {
        // Test that matching at word start gets bonus
        var (scoreAtStart, _) = CommandPaletteService.FuzzyMatchString("s", "Save");
        var (scoreInMiddle, _) = CommandPaletteService.FuzzyMatchString("a", "Save");

        // 's' is at start (word boundary), 'a' is in middle
        Assert.True(scoreAtStart > scoreInMiddle);
    }

    [Fact]
    public void FuzzyMatchString_BonusForConsecutiveMatches()
    {
        var (consecutiveScore, _) = CommandPaletteService.FuzzyMatchString("sav", "Save");
        var (spreadScore, _) = CommandPaletteService.FuzzyMatchString("sve", "Save");

        Assert.True(consecutiveScore > spreadScore);
    }
}

public class PaletteCommandTests
{
    [Fact]
    public void PaletteCommand_DefaultValues()
    {
        var command = new PaletteCommand();

        Assert.Equal(string.Empty, command.Id);
        Assert.Equal(string.Empty, command.Name);
        Assert.Equal(CommandCategory.Edit, command.Category);
        Assert.True(command.IsEnabled);
        Assert.Empty(command.Keywords);
    }

    [Fact]
    public void PaletteCommand_IsEnabled_UsesCanExecute()
    {
        var enabled = true;
        var command = new PaletteCommand
        {
            Id = "test",
            Name = "Test",
            CanExecute = () => enabled
        };

        Assert.True(command.IsEnabled);

        enabled = false;
        Assert.False(command.IsEnabled);
    }

    [Fact]
    public void PaletteCommand_SupportsShortcut()
    {
        var command = new PaletteCommand
        {
            Id = "file.save",
            Name = "Save",
            Shortcut = "Ctrl+S"
        };

        Assert.Equal("Ctrl+S", command.Shortcut);
    }

    [Fact]
    public void PaletteCommand_SupportsKeywords()
    {
        var command = new PaletteCommand
        {
            Id = "file.export",
            Name = "Export",
            Keywords = ["png", "jpg", "svg"]
        };

        Assert.Equal(3, command.Keywords.Length);
    }
}

public class CommandSearchResultTests
{
    [Fact]
    public void CommandSearchResult_ContainsMatchInfo()
    {
        var result = new CommandSearchResult
        {
            Command = new PaletteCommand { Id = "test", Name = "Test" },
            Score = 100,
            MatchedIndices = [0, 1, 2, 3]
        };

        Assert.Equal(100, result.Score);
        Assert.Equal(4, result.MatchedIndices.Length);
    }
}
