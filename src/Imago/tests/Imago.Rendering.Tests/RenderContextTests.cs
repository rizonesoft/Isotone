namespace Imago.Rendering.Tests;

using FluentAssertions;
using Xunit;

public class RenderContextTests
{
    public class Constructor
    {
        [Fact]
        public void ShouldSetWidthAndHeight()
        {
            // Arrange & Act
            using var context = new RenderContext(1920, 1080);

            // Assert
            context.Width.Should().Be(1920);
            context.Height.Should().Be(1080);
        }

        [Fact]
        public void ShouldInitializeWithDefaultValues()
        {
            // Arrange & Act
            using var context = new RenderContext(800, 600);

            // Assert
            context.Zoom.Should().Be(1.0f);
            context.PanX.Should().Be(0f);
            context.PanY.Should().Be(0f);
        }
    }

    public class ScreenToCanvas
    {
        [Fact]
        public void ShouldConvertWithNoZoomOrPan()
        {
            // Arrange
            using var context = new RenderContext(800, 600);

            // Act
            var (x, y) = context.ScreenToCanvas(100, 200);

            // Assert
            x.Should().Be(100);
            y.Should().Be(200);
        }

        [Fact]
        public void ShouldAccountForZoom()
        {
            // Arrange
            using var context = new RenderContext(800, 600) { Zoom = 2.0f };

            // Act
            var (x, y) = context.ScreenToCanvas(200, 400);

            // Assert
            x.Should().Be(100);
            y.Should().Be(200);
        }

        [Fact]
        public void ShouldAccountForPan()
        {
            // Arrange
            using var context = new RenderContext(800, 600) { PanX = 50, PanY = 100 };

            // Act
            var (x, y) = context.ScreenToCanvas(150, 300);

            // Assert
            x.Should().Be(100);
            y.Should().Be(200);
        }
    }

    public class CanvasToScreen
    {
        [Fact]
        public void ShouldConvertWithNoZoomOrPan()
        {
            // Arrange
            using var context = new RenderContext(800, 600);

            // Act
            var (x, y) = context.CanvasToScreen(100, 200);

            // Assert
            x.Should().Be(100);
            y.Should().Be(200);
        }

        [Fact]
        public void ShouldAccountForZoom()
        {
            // Arrange
            using var context = new RenderContext(800, 600) { Zoom = 2.0f };

            // Act
            var (x, y) = context.CanvasToScreen(100, 200);

            // Assert
            x.Should().Be(200);
            y.Should().Be(400);
        }

        [Fact]
        public void ShouldBeInverseOfScreenToCanvas()
        {
            // Arrange
            using var context = new RenderContext(800, 600) { Zoom = 1.5f, PanX = 25, PanY = 50 };
            const float originalX = 100;
            const float originalY = 200;

            // Act
            var (screenX, screenY) = context.CanvasToScreen(originalX, originalY);
            var (canvasX, canvasY) = context.ScreenToCanvas(screenX, screenY);

            // Assert
            canvasX.Should().BeApproximately(originalX, 0.001f);
            canvasY.Should().BeApproximately(originalY, 0.001f);
        }
    }
}
