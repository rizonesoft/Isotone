namespace Imago.Rendering.Shaders;

/// <summary>
/// Interface for GPU pixel shaders.
/// </summary>
public interface IPixelShader
{
    /// <summary>
    /// Gets the name of the shader.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets whether the shader is currently compiled and ready.
    /// </summary>
    bool IsCompiled { get; }

    /// <summary>
    /// Compiles the shader if not already compiled.
    /// </summary>
    void Compile();

    /// <summary>
    /// Disposes of shader resources.
    /// </summary>
    void Dispose();
}
