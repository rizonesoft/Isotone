using System;
using System.Windows.Markup;
using System.Windows.Media;
using Bezier.Desktop.Services;

namespace Bezier.Desktop.Helpers;

[MarkupExtensionReturnType(typeof(Geometry))]
public class IconExtension : MarkupExtension
{
    [ConstructorArgument("icon")]
    public string? Icon { get; set; }

    public IconExtension() { }

    public IconExtension(string icon)
    {
        Icon = icon;
    }

    public override object ProvideValue(IServiceProvider serviceProvider)
    {
        if (string.IsNullOrEmpty(Icon))
            return Geometry.Empty;

        return IconService.Instance.GetGeometry(Icon);
    }
}
