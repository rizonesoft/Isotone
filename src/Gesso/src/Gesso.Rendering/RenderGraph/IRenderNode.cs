namespace Gesso.Rendering.RenderGraph;

/// <summary>
/// Represents a node in the render graph pipeline.
/// </summary>
public interface IRenderNode
{
    /// <summary>
    /// Gets the unique identifier for this node.
    /// </summary>
    Guid Id { get; }

    /// <summary>
    /// Gets the name of this node for debugging.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets whether this node needs to be re-rendered.
    /// </summary>
    bool IsDirty { get; }

    /// <summary>
    /// Gets the input nodes that this node depends on.
    /// </summary>
    IReadOnlyList<IRenderNode> Inputs { get; }

    /// <summary>
    /// Invalidates this node, marking it for re-rendering.
    /// </summary>
    void Invalidate();

    /// <summary>
    /// Executes this node's rendering operation.
    /// </summary>
    void Execute(RenderContext context);
}
