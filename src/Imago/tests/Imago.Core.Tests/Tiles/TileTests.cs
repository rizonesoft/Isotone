namespace Imago.Core.Tests.Tiles;

using AwesomeAssertions;
using Imago.Core.Tiles;
using Xunit;

public class TileTests
{
    public class Constructor
    {
        [Fact]
        public void ShouldSetCoordinate()
        {
            // Arrange
            var coordinate = new TileCoordinate(5, 10);

            // Act
            using var tile = new Tile(coordinate);

            // Assert
            tile.Coordinate.Should().Be(coordinate);
        }

        [Fact]
        public void ShouldInitializeAsEmpty()
        {
            // Arrange & Act
            using var tile = new Tile(new TileCoordinate(0, 0));

            // Assert
            tile.IsEmpty.Should().BeTrue();
            tile.IsDirty.Should().BeFalse();
        }
    }

    public class GetData
    {
        [Fact]
        public void ShouldReturnCorrectSize()
        {
            // Arrange
            using var tile = new Tile(new TileCoordinate(0, 0));

            // Act
            var data = tile.GetData();

            // Assert
            data.Length.Should().Be(Tile.TileDataSize);
        }

        [Fact]
        public void ShouldReturnZeroInitializedData()
        {
            // Arrange
            using var tile = new Tile(new TileCoordinate(0, 0));

            // Act
            var data = tile.GetReadOnlyData();

            // Assert
            data.ToArray().Should().OnlyContain(b => b == 0);
        }
    }

    public class MarkDirty
    {
        [Fact]
        public void ShouldSetIsDirtyToTrue()
        {
            // Arrange
            using var tile = new Tile(new TileCoordinate(0, 0));

            // Act
            tile.MarkDirty();

            // Assert
            tile.IsDirty.Should().BeTrue();
        }

        [Fact]
        public void ShouldSetIsEmptyToFalse()
        {
            // Arrange
            using var tile = new Tile(new TileCoordinate(0, 0));

            // Act
            tile.MarkDirty();

            // Assert
            tile.IsEmpty.Should().BeFalse();
        }
    }

    public class Clear
    {
        [Fact]
        public void ShouldZeroOutData()
        {
            // Arrange
            using var tile = new Tile(new TileCoordinate(0, 0));
            var data = tile.GetData();
            data[0] = 255;
            data[1] = 128;

            // Act
            tile.Clear();

            // Assert
            tile.GetReadOnlyData().ToArray().Should().OnlyContain(b => b == 0);
        }

        [Fact]
        public void ShouldMarkAsEmpty()
        {
            // Arrange
            using var tile = new Tile(new TileCoordinate(0, 0));
            tile.MarkDirty();

            // Act
            tile.Clear();

            // Assert
            tile.IsEmpty.Should().BeTrue();
        }
    }
}
