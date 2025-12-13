using System.Collections.ObjectModel;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG group element (container for other elements).
/// </summary>
public class SvgGroup : VectorElement
{
    /// <summary>Child elements in this group.</summary>
    public ObservableCollection<VectorElement> Children { get; } = [];

    /// <summary>
    /// Adds a child element to this group.
    /// </summary>
    public void Add(VectorElement element)
    {
        element.Parent = this;
        Children.Add(element);
    }

    /// <summary>
    /// Removes a child element from this group.
    /// </summary>
    public bool Remove(VectorElement element)
    {
        if (Children.Remove(element))
        {
            element.Parent = null;
            return true;
        }
        return false;
    }

    public override VectorElement Clone()
    {
        var clone = new SvgGroup
        {
            Id = Guid.NewGuid(),
            Name = Name,
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            Transform = Transform,
            Fill = Fill?.Clone(),
            Stroke = Stroke?.Clone()
        };

        foreach (var child in Children)
        {
            var childClone = child.Clone();
            childClone.Parent = clone;
            clone.Children.Add(childClone);
        }

        return clone;
    }

    protected override bool HitTestLocal(double x, double y)
    {
        // Hit test against children in reverse order (topmost first)
        // Note: Group transforms are already handled by base class
        for (int i = Children.Count - 1; i >= 0; i--)
        {
            if (Children[i].IsVisible && Children[i].HitTest(x, y))
                return true;
        }
        return false;
    }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        if (Children.Count == 0) return (0, 0, 0, 0);

        var firstBox = Children[0].GetBoundingBox();
        var minX = firstBox.X;
        var minY = firstBox.Y;
        var maxX = firstBox.X + firstBox.Width;
        var maxY = firstBox.Y + firstBox.Height;

        for (int i = 1; i < Children.Count; i++)
        {
            var box = Children[i].GetBoundingBox();
            minX = Math.Min(minX, box.X);
            minY = Math.Min(minY, box.Y);
            maxX = Math.Max(maxX, box.X + box.Width);
            maxY = Math.Max(maxY, box.Y + box.Height);
        }

        return (minX, minY, maxX - minX, maxY - minY);
    }

    public override string ToSvgString()
    {
        var childrenSvg = string.Join("\n  ", Children.Select(c => c.ToSvgString()));
        return $"<g{GetCommonSvgAttributes()}>\n  {childrenSvg}\n</g>";
    }
}
