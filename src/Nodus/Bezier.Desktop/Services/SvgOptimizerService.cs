using System.Text.RegularExpressions;
using System.Xml.Linq;

namespace Bezier.Desktop.Services;

public class OptimizationOptions
{
    public bool RemoveComments { get; set; } = true;
    public bool RemoveMetadata { get; set; } = true;
    public bool RemoveEditorData { get; set; } = true;
    public bool RemoveEmptyGroups { get; set; } = true;
    public bool CollapseGroups { get; set; } = false;
    public bool RoundNumbers { get; set; } = false;
    public bool Minify { get; set; } = false;
}

public interface ISvgOptimizerService
{
    string Optimize(string svgContent, OptimizationOptions? options = null);
}

public partial class SvgOptimizerService : ISvgOptimizerService
{
    private static readonly string[] EditorNamespaces = 
    [
        "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        "http://www.inkscape.org/namespaces/inkscape",
        "http://ns.adobe.com/AdobeIllustrator/10.0/",
        "http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/",
        "http://www.bohemiancoding.com/sketch/ns"
    ];

    private static readonly string[] MetadataElements = ["title", "desc", "metadata"];

    public string Optimize(string svgContent, OptimizationOptions? options = null)
    {
        options ??= new OptimizationOptions();
        
        if (string.IsNullOrWhiteSpace(svgContent))
            return svgContent;

        try
        {
            var content = svgContent;

            // Remove comments first (before XML parsing to handle malformed comments)
            if (options.RemoveComments)
            {
                content = RemoveXmlComments(content);
            }

            // Parse XML
            var doc = XDocument.Parse(content, LoadOptions.PreserveWhitespace);
            
            if (doc.Root == null)
                return content;

            // Remove editor-specific namespaces and attributes
            if (options.RemoveEditorData)
            {
                RemoveEditorNamespacesAndAttributes(doc.Root);
            }

            // Remove metadata elements
            if (options.RemoveMetadata)
            {
                RemoveMetadataElements(doc.Root);
            }

            // Remove empty groups
            if (options.RemoveEmptyGroups)
            {
                RemoveEmptyGroupsRecursive(doc.Root);
            }

            // Collapse single-child groups
            if (options.CollapseGroups)
            {
                CollapseSingleChildGroups(doc.Root);
            }

            // Round numeric values
            if (options.RoundNumbers)
            {
                RoundNumericAttributes(doc.Root);
            }

            // Convert back to string
            var result = options.Minify 
                ? doc.ToString(SaveOptions.DisableFormatting) 
                : doc.ToString(SaveOptions.None);

            // Clean up empty namespace declarations
            result = CleanupEmptyNamespaces(result);

            return result;
        }
        catch (Exception)
        {
            // If XML parsing fails, return original content
            return svgContent;
        }
    }

    private static string RemoveXmlComments(string content)
    {
        return CommentRegex().Replace(content, "");
    }

    private static void RemoveEditorNamespacesAndAttributes(XElement element)
    {
        // Remove attributes from editor namespaces
        var attributesToRemove = element.Attributes()
            .Where(a => a.Name.Namespace != XNamespace.None && 
                        EditorNamespaces.Contains(a.Name.NamespaceName))
            .ToList();

        foreach (var attr in attributesToRemove)
        {
            attr.Remove();
        }

        // Remove namespace declarations for editor namespaces
        var nsDeclarations = element.Attributes()
            .Where(a => a.IsNamespaceDeclaration && 
                        EditorNamespaces.Contains(a.Value))
            .ToList();

        foreach (var ns in nsDeclarations)
        {
            ns.Remove();
        }

        // Recurse into child elements
        foreach (var child in element.Elements().ToList())
        {
            RemoveEditorNamespacesAndAttributes(child);
        }
    }

    private static void RemoveMetadataElements(XElement element)
    {
        var svgNs = element.GetDefaultNamespace();
        
        foreach (var metaName in MetadataElements)
        {
            var metaElements = element.Descendants(svgNs + metaName).ToList();
            foreach (var meta in metaElements)
            {
                meta.Remove();
            }
            
            // Also check without namespace
            var metaElementsNoNs = element.Descendants(metaName).ToList();
            foreach (var meta in metaElementsNoNs)
            {
                meta.Remove();
            }
        }
    }

    private static void RemoveEmptyGroupsRecursive(XElement element)
    {
        var svgNs = element.GetDefaultNamespace();
        
        // Process children first (bottom-up)
        foreach (var child in element.Elements().ToList())
        {
            RemoveEmptyGroupsRecursive(child);
        }

        // Check if this is an empty group
        if ((element.Name.LocalName == "g" || element.Name == svgNs + "g") && 
            !element.HasElements && 
            string.IsNullOrWhiteSpace(element.Value))
        {
            element.Remove();
        }
    }

    private static void CollapseSingleChildGroups(XElement element)
    {
        var svgNs = element.GetDefaultNamespace();
        
        foreach (var child in element.Elements().ToList())
        {
            CollapseSingleChildGroups(child);
        }

        // If this is a group with exactly one child element and no important attributes
        if ((element.Name.LocalName == "g" || element.Name == svgNs + "g") &&
            element.Elements().Count() == 1)
        {
            var hasSignificantAttributes = element.Attributes()
                .Any(a => !a.IsNamespaceDeclaration && 
                          a.Name.LocalName != "id");

            if (!hasSignificantAttributes)
            {
                var onlyChild = element.Elements().First();
                element.ReplaceWith(onlyChild);
            }
        }
    }

    private static void RoundNumericAttributes(XElement element)
    {
        var numericAttributes = new[] { "x", "y", "width", "height", "cx", "cy", "r", "rx", "ry", 
            "x1", "y1", "x2", "y2", "stroke-width", "font-size", "opacity" };

        foreach (var attr in element.Attributes().ToList())
        {
            if (numericAttributes.Contains(attr.Name.LocalName))
            {
                if (double.TryParse(attr.Value, out var value))
                {
                    attr.Value = Math.Round(value, 2).ToString();
                }
            }
        }

        // Round values in d attribute (path data)
        var dAttr = element.Attribute("d");
        if (dAttr != null)
        {
            dAttr.Value = RoundPathData(dAttr.Value);
        }

        foreach (var child in element.Elements())
        {
            RoundNumericAttributes(child);
        }
    }

    private static string RoundPathData(string pathData)
    {
        return NumberInPathRegex().Replace(pathData, match =>
        {
            if (double.TryParse(match.Value, out var value))
            {
                return Math.Round(value, 2).ToString();
            }
            return match.Value;
        });
    }

    private static string CleanupEmptyNamespaces(string content)
    {
        // Remove empty xmlns declarations
        content = EmptyXmlnsRegex().Replace(content, "");
        return content;
    }

    [GeneratedRegex(@"<!--[\s\S]*?-->", RegexOptions.Compiled)]
    private static partial Regex CommentRegex();

    [GeneratedRegex(@"-?\d+\.?\d*", RegexOptions.Compiled)]
    private static partial Regex NumberInPathRegex();

    [GeneratedRegex(@"\s+xmlns:\w+\s*=\s*""\s*""", RegexOptions.Compiled)]
    private static partial Regex EmptyXmlnsRegex();
}
