using Bezier.Core.Models.Fills;

namespace Bezier.Core.Models.Elements;

/// <summary>
/// Represents an SVG gradient definition element.
/// Can be linear or radial, stored in defs and referenced by fills.
/// </summary>
public class SvgGradient : VectorElement
{
    private GradientType _type = GradientType.Linear;
    private double _x1;
    private double _y1;
    private double _x2 = 1;
    private double _y2;
    private double _cx = 0.5;
    private double _cy = 0.5;
    private double _r = 0.5;
    private double _fx = 0.5;
    private double _fy = 0.5;
    private string _gradientUnits = "objectBoundingBox";
    private string _spreadMethod = "pad";
    private List<GradientStop> _stops = [];

    /// <summary>Type of gradient (Linear or Radial).</summary>
    public GradientType Type
    {
        get => _type;
        set { if (_type == value) return; _type = value; OnPropertyChanged(nameof(Type)); }
    }

    // Linear gradient properties
    /// <summary>Start X (linear gradient).</summary>
    public double X1
    {
        get => _x1;
        set { if (Math.Abs(_x1 - value) < 0.0001) return; _x1 = value; OnPropertyChanged(nameof(X1)); }
    }

    /// <summary>Start Y (linear gradient).</summary>
    public double Y1
    {
        get => _y1;
        set { if (Math.Abs(_y1 - value) < 0.0001) return; _y1 = value; OnPropertyChanged(nameof(Y1)); }
    }

    /// <summary>End X (linear gradient).</summary>
    public double X2
    {
        get => _x2;
        set { if (Math.Abs(_x2 - value) < 0.0001) return; _x2 = value; OnPropertyChanged(nameof(X2)); }
    }

    /// <summary>End Y (linear gradient).</summary>
    public double Y2
    {
        get => _y2;
        set { if (Math.Abs(_y2 - value) < 0.0001) return; _y2 = value; OnPropertyChanged(nameof(Y2)); }
    }

    // Radial gradient properties
    /// <summary>Center X (radial gradient).</summary>
    public double CX
    {
        get => _cx;
        set { if (Math.Abs(_cx - value) < 0.0001) return; _cx = value; OnPropertyChanged(nameof(CX)); }
    }

    /// <summary>Center Y (radial gradient).</summary>
    public double CY
    {
        get => _cy;
        set { if (Math.Abs(_cy - value) < 0.0001) return; _cy = value; OnPropertyChanged(nameof(CY)); }
    }

    /// <summary>Radius (radial gradient).</summary>
    public double R
    {
        get => _r;
        set { if (Math.Abs(_r - value) < 0.0001) return; _r = Math.Max(0, value); OnPropertyChanged(nameof(R)); }
    }

    /// <summary>Focal point X (radial gradient).</summary>
    public double FX
    {
        get => _fx;
        set { if (Math.Abs(_fx - value) < 0.0001) return; _fx = value; OnPropertyChanged(nameof(FX)); }
    }

    /// <summary>Focal point Y (radial gradient).</summary>
    public double FY
    {
        get => _fy;
        set { if (Math.Abs(_fy - value) < 0.0001) return; _fy = value; OnPropertyChanged(nameof(FY)); }
    }

    /// <summary>Coordinate system ("objectBoundingBox" or "userSpaceOnUse").</summary>
    public string GradientUnits
    {
        get => _gradientUnits;
        set 
        { 
            var newValue = value is "objectBoundingBox" or "userSpaceOnUse" ? value : "objectBoundingBox";
            if (_gradientUnits == newValue) return; 
            _gradientUnits = newValue; 
            OnPropertyChanged(nameof(GradientUnits)); 
        }
    }

    /// <summary>Spread method ("pad", "reflect", or "repeat").</summary>
    public string SpreadMethod
    {
        get => _spreadMethod;
        set 
        { 
            var newValue = value is "pad" or "reflect" or "repeat" ? value : "pad";
            if (_spreadMethod == newValue) return; 
            _spreadMethod = newValue; 
            OnPropertyChanged(nameof(SpreadMethod)); 
        }
    }

    /// <summary>Color stops for this gradient.</summary>
    public List<GradientStop> Stops
    {
        get => _stops;
        set { _stops = value ?? []; OnPropertyChanged(nameof(Stops)); }
    }

    public override VectorElement Clone()
    {
        return new SvgGradient
        {
            Id = Guid.NewGuid(),
            Name = Name,
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            Transform = Transform,
            Type = Type,
            X1 = X1, Y1 = Y1, X2 = X2, Y2 = Y2,
            CX = CX, CY = CY, R = R, FX = FX, FY = FY,
            GradientUnits = GradientUnits,
            SpreadMethod = SpreadMethod,
            Stops = Stops.Select(s => new GradientStop(s.Offset, s.Color)).ToList()
        };
    }

    protected override bool HitTestLocal(double x, double y) => false; // Gradients are not directly hittable

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox() => (0, 0, 0, 0);

    public override string ToSvgString()
    {
        var stopsStr = string.Join("\n  ", Stops.Select(s => 
        {
            // Extract ARGB components from uint color
            var a = (byte)((s.Color >> 24) & 0xFF);
            var r = (byte)((s.Color >> 16) & 0xFF);
            var g = (byte)((s.Color >> 8) & 0xFF);
            var b = (byte)(s.Color & 0xFF);
            return $"<stop offset=\"{s.Offset * 100}%\" stop-color=\"rgba({r},{g},{b},{a / 255.0:F2})\"/>";
        }));

        if (Type == GradientType.Linear)
        {
            var attrs = new List<string>();
            if (X1 != 0) attrs.Add($"x1=\"{X1 * 100}%\"");
            if (Y1 != 0) attrs.Add($"y1=\"{Y1 * 100}%\"");
            if (X2 != 1) attrs.Add($"x2=\"{X2 * 100}%\"");
            if (Y2 != 0) attrs.Add($"y2=\"{Y2 * 100}%\"");
            if (GradientUnits != "objectBoundingBox") attrs.Add($"gradientUnits=\"{GradientUnits}\"");
            if (SpreadMethod != "pad") attrs.Add($"spreadMethod=\"{SpreadMethod}\"");
            var attrsStr = attrs.Count > 0 ? " " + string.Join(" ", attrs) : "";
            return $"<linearGradient{GetCommonSvgAttributes()}{attrsStr}>\n  {stopsStr}\n</linearGradient>";
        }
        else
        {
            var attrs = new List<string>();
            if (CX != 0.5) attrs.Add($"cx=\"{CX * 100}%\"");
            if (CY != 0.5) attrs.Add($"cy=\"{CY * 100}%\"");
            if (R != 0.5) attrs.Add($"r=\"{R * 100}%\"");
            if (Math.Abs(FX - CX) > 0.0001) attrs.Add($"fx=\"{FX * 100}%\"");
            if (Math.Abs(FY - CY) > 0.0001) attrs.Add($"fy=\"{FY * 100}%\"");
            if (GradientUnits != "objectBoundingBox") attrs.Add($"gradientUnits=\"{GradientUnits}\"");
            if (SpreadMethod != "pad") attrs.Add($"spreadMethod=\"{SpreadMethod}\"");
            var attrsStr = attrs.Count > 0 ? " " + string.Join(" ", attrs) : "";
            return $"<radialGradient{GetCommonSvgAttributes()}{attrsStr}>\n  {stopsStr}\n</radialGradient>";
        }
    }
}

/// <summary>Gradient type enumeration.</summary>
public enum GradientType
{
    Linear,
    Radial
}
