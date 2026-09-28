namespace Gesso.Core.Tests.Layers;

using AwesomeAssertions;
using Gesso.Core.Layers;
using Xunit;

public class RasterLayerTests
{
    public class Constructor
    {
        [Fact]
        public void ShouldSetWidthAndHeight()
        {
            // Arrange & Act
            var layer = new RasterLayer(1920, 1080);

            // Assert
            layer.Width.Should().Be(1920);
            layer.Height.Should().Be(1080);
        }

        [Fact]
        public void ShouldSetDefaultName()
        {
            // Arrange & Act
            var layer = new RasterLayer(100, 100);

            // Assert
            layer.Name.Should().Be("Layer");
        }

        [Fact]
        public void ShouldSetCustomName()
        {
            // Arrange & Act
            var layer = new RasterLayer(100, 100, "Background");

            // Assert
            layer.Name.Should().Be("Background");
        }

        [Fact]
        public void ShouldInitializeWithDefaultValues()
        {
            // Arrange & Act
            var layer = new RasterLayer(100, 100);

            // Assert
            layer.IsVisible.Should().BeTrue();
            layer.IsLocked.Should().BeFalse();
            layer.Opacity.Should().Be(1.0);
            layer.BlendMode.Should().Be(BlendMode.Normal);
            layer.LayerType.Should().Be(LayerType.Raster);
        }

        [Fact]
        public void ShouldGenerateUniqueId()
        {
            // Arrange & Act
            var layer1 = new RasterLayer(100, 100);
            var layer2 = new RasterLayer(100, 100);

            // Assert
            layer1.Id.Should().NotBe(layer2.Id);
        }
    }

    public class Clone
    {
        [Fact]
        public void ShouldCreateDeepCopy()
        {
            // Arrange
            var original = new RasterLayer(1920, 1080, "Original")
            {
                Opacity = 0.5,
                BlendMode = BlendMode.Multiply,
                IsVisible = false
            };

            // Act
            var clone = (RasterLayer)original.Clone();

            // Assert
            clone.Should().NotBeSameAs(original);
            clone.Id.Should().NotBe(original.Id);
            clone.Name.Should().Be("Original Copy");
            clone.Width.Should().Be(1920);
            clone.Height.Should().Be(1080);
            clone.Opacity.Should().Be(0.5);
            clone.BlendMode.Should().Be(BlendMode.Multiply);
            clone.IsVisible.Should().BeFalse();
        }
    }
}
