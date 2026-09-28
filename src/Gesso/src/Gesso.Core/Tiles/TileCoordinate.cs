namespace Gesso.Core.Tiles;

/// <summary>
/// Represents the coordinate of a tile in tile space.
/// </summary>
public readonly record struct TileCoordinate(int X, int Y)
{
    /// <summary>
    /// Converts pixel coordinates to tile coordinates.
    /// </summary>
    public static TileCoordinate FromPixel(int pixelX, int pixelY)
    {
        return new TileCoordinate(
            pixelX / Tile.TileSize,
            pixelY / Tile.TileSize);
    }

    /// <summary>
    /// Gets the pixel coordinates of the top-left corner of this tile.
    /// </summary>
    public (int X, int Y) ToPixel()
    {
        return (X * Tile.TileSize, Y * Tile.TileSize);
    }

    /// <summary>
    /// Gets the bounds of this tile in pixel coordinates.
    /// </summary>
    public (int Left, int Top, int Right, int Bottom) GetPixelBounds()
    {
        var (left, top) = ToPixel();
        return (left, top, left + Tile.TileSize, top + Tile.TileSize);
    }

    public override string ToString() => $"Tile({X}, {Y})";
}
