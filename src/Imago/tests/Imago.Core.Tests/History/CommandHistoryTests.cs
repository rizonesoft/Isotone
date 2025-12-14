namespace Imago.Core.Tests.History;

using FluentAssertions;
using Imago.Core.History;
using Moq;
using Xunit;

public class CommandHistoryTests
{
    private static Mock<ICommand> CreateMockCommand(string name = "Test Command")
    {
        var mock = new Mock<ICommand>();
        mock.Setup(c => c.Name).Returns(name);
        mock.Setup(c => c.CanMergeWith(It.IsAny<ICommand>())).Returns(false);
        return mock;
    }

    public class Execute
    {
        [Fact]
        public void ShouldExecuteCommand()
        {
            // Arrange
            var history = new CommandHistory();
            var command = CreateMockCommand();

            // Act
            history.Execute(command.Object);

            // Assert
            command.Verify(c => c.Execute(), Times.Once);
        }

        [Fact]
        public void ShouldAddToUndoStack()
        {
            // Arrange
            var history = new CommandHistory();
            var command = CreateMockCommand();

            // Act
            history.Execute(command.Object);

            // Assert
            history.UndoStack.Should().HaveCount(1);
            history.CanUndo.Should().BeTrue();
        }

        [Fact]
        public void ShouldClearRedoStack()
        {
            // Arrange
            var history = new CommandHistory();
            var command1 = CreateMockCommand();
            var command2 = CreateMockCommand();

            history.Execute(command1.Object);
            history.Undo();

            // Act
            history.Execute(command2.Object);

            // Assert
            history.RedoStack.Should().BeEmpty();
            history.CanRedo.Should().BeFalse();
        }
    }

    public class Undo
    {
        [Fact]
        public void ShouldUndoLastCommand()
        {
            // Arrange
            var history = new CommandHistory();
            var command = CreateMockCommand();
            history.Execute(command.Object);

            // Act
            history.Undo();

            // Assert
            command.Verify(c => c.Undo(), Times.Once);
        }

        [Fact]
        public void ShouldMoveCommandToRedoStack()
        {
            // Arrange
            var history = new CommandHistory();
            var command = CreateMockCommand();
            history.Execute(command.Object);

            // Act
            history.Undo();

            // Assert
            history.UndoStack.Should().BeEmpty();
            history.RedoStack.Should().HaveCount(1);
            history.CanRedo.Should().BeTrue();
        }

        [Fact]
        public void ShouldDoNothingWhenStackIsEmpty()
        {
            // Arrange
            var history = new CommandHistory();

            // Act
            history.Undo();

            // Assert
            history.UndoStack.Should().BeEmpty();
        }
    }

    public class Redo
    {
        [Fact]
        public void ShouldReExecuteCommand()
        {
            // Arrange
            var history = new CommandHistory();
            var command = CreateMockCommand();
            history.Execute(command.Object);
            history.Undo();

            // Act
            history.Redo();

            // Assert
            command.Verify(c => c.Execute(), Times.Exactly(2));
        }

        [Fact]
        public void ShouldMoveCommandBackToUndoStack()
        {
            // Arrange
            var history = new CommandHistory();
            var command = CreateMockCommand();
            history.Execute(command.Object);
            history.Undo();

            // Act
            history.Redo();

            // Assert
            history.UndoStack.Should().HaveCount(1);
            history.RedoStack.Should().BeEmpty();
        }
    }

    public class Clear
    {
        [Fact]
        public void ShouldClearBothStacks()
        {
            // Arrange
            var history = new CommandHistory();
            history.Execute(CreateMockCommand().Object);
            history.Execute(CreateMockCommand().Object);
            history.Undo();

            // Act
            history.Clear();

            // Assert
            history.UndoStack.Should().BeEmpty();
            history.RedoStack.Should().BeEmpty();
            history.CanUndo.Should().BeFalse();
            history.CanRedo.Should().BeFalse();
        }
    }
}
