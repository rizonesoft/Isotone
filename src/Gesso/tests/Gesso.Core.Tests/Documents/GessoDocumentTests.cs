namespace Gesso.Core.Tests.Documents;

using AwesomeAssertions;
using Gesso.Core.Documents;
using Gesso.Core.Layers;
using Xunit;

public class GessoDocumentTests
{
    public class Constructor
    {
        [Fact]
        public void ShouldSetWidthAndHeight()
        {
            // Arrange & Act
            var document = new GessoDocument(1920, 1080);

            // Assert
            document.Width.Should().Be(1920);
            document.Height.Should().Be(1080);
        }

        [Fact]
        public void ShouldInitializeWithDefaultValues()
        {
            // Arrange & Act
            var document = new GessoDocument(800, 600);

            // Assert
            document.Name.Should().Be("Untitled");
            document.BitDepth.Should().Be(8);
            document.ColorSpace.Should().Be(ColorSpace.SRGB);
            document.Resolution.Should().Be(72.0);
            document.IsDirty.Should().BeFalse();
            document.Layers.Should().BeEmpty();
        }
    }

    public class AddLayer
    {
        [Fact]
        public void ShouldAddLayerToCollection()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            var layer = new RasterLayer(100, 100, "Test Layer");

            // Act
            document.AddLayer(layer);

            // Assert
            document.Layers.Should().Contain(layer);
            document.Layers.Should().HaveCount(1);
        }

        [Fact]
        public void ShouldSetActiveLayerWhenFirstLayerAdded()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            var layer = new RasterLayer(100, 100);

            // Act
            document.AddLayer(layer);

            // Assert
            document.ActiveLayer.Should().Be(layer);
        }

        [Fact]
        public void ShouldMarkDocumentAsDirty()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            var layer = new RasterLayer(100, 100);

            // Act
            document.AddLayer(layer);

            // Assert
            document.IsDirty.Should().BeTrue();
        }

        [Fact]
        public void ShouldThrowWhenLayerIsNull()
        {
            // Arrange
            var document = new GessoDocument(100, 100);

            // Act & Assert
            var action = () => document.AddLayer(null!);
            action.Should().Throw<ArgumentNullException>();
        }
    }

    public class RemoveLayer
    {
        [Fact]
        public void ShouldRemoveLayerFromCollection()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            var layer = new RasterLayer(100, 100);
            document.AddLayer(layer);

            // Act
            document.RemoveLayer(layer);

            // Assert
            document.Layers.Should().NotContain(layer);
            document.Layers.Should().BeEmpty();
        }

        [Fact]
        public void ShouldClearActiveLayerWhenRemoved()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            var layer = new RasterLayer(100, 100);
            document.AddLayer(layer);

            // Act
            document.RemoveLayer(layer);

            // Assert
            document.ActiveLayer.Should().BeNull();
        }
    }

    public class MoveLayer
    {
        [Fact]
        public void ShouldReorderLayers()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            var layer1 = new RasterLayer(100, 100, "Layer 1");
            var layer2 = new RasterLayer(100, 100, "Layer 2");
            var layer3 = new RasterLayer(100, 100, "Layer 3");
            document.AddLayer(layer1);
            document.AddLayer(layer2);
            document.AddLayer(layer3);

            // Act
            document.MoveLayer(0, 2);

            // Assert
            document.Layers[0].Should().Be(layer2);
            document.Layers[1].Should().Be(layer3);
            document.Layers[2].Should().Be(layer1);
        }

        [Fact]
        public void ShouldThrowWhenFromIndexOutOfRange()
        {
            // Arrange
            var document = new GessoDocument(100, 100);
            document.AddLayer(new RasterLayer(100, 100));

            // Act & Assert
            var action = () => document.MoveLayer(-1, 0);
            action.Should().Throw<ArgumentOutOfRangeException>();
        }
    }
}
