namespace Pinxit.Rendering.RenderGraph;

/// <summary>
/// Base class for render graph nodes.
/// </summary>
public abstract class RenderNode : IRenderNode
{
    private readonly List<IRenderNode> _inputs = new();

    public Guid Id { get; } = Guid.NewGuid();

    public abstract string Name { get; }

    public bool IsDirty { get; protected set; } = true;

    public IReadOnlyList<IRenderNode> Inputs => _inputs;

    protected RenderNode()
    {
    }

    public void AddInput(IRenderNode node)
    {
        ArgumentNullException.ThrowIfNull(node);
        _inputs.Add(node);
    }

    public void RemoveInput(IRenderNode node)
    {
        _inputs.Remove(node);
    }

    public void Invalidate()
    {
        IsDirty = true;
    }

    public abstract void Execute(RenderContext context);

    protected void MarkClean()
    {
        IsDirty = false;
    }
}
