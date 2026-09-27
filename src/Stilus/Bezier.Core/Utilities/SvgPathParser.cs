using System.Globalization;
using System.Text.RegularExpressions;

namespace Bezier.Core.Utilities;

/// <summary>
/// Parses SVG path data strings and extracts geometric information.
/// Supports M, L, H, V, C, S, Q, T, A, Z commands (both absolute and relative).
/// </summary>
public static partial class SvgPathParser
{
    /// <summary>
    /// Calculates the bounding box of an SVG path from its path data string.
    /// </summary>
    /// <param name="pathData">The SVG path data (d attribute value).</param>
    /// <returns>Bounding box as (X, Y, Width, Height).</returns>
    public static (double X, double Y, double Width, double Height) GetBoundingBox(string pathData)
    {
        if (string.IsNullOrWhiteSpace(pathData))
            return (0, 0, 0, 0);

        var points = ExtractAllPoints(pathData);
        
        if (points.Count == 0)
            return (0, 0, 0, 0);

        var minX = points.Min(p => p.X);
        var minY = points.Min(p => p.Y);
        var maxX = points.Max(p => p.X);
        var maxY = points.Max(p => p.Y);

        return (minX, minY, maxX - minX, maxY - minY);
    }

    /// <summary>
    /// Extracts all points from an SVG path for hit testing purposes.
    /// Includes control points for curves to ensure accurate bounds.
    /// </summary>
    public static List<(double X, double Y)> ExtractAllPoints(string pathData)
    {
        var points = new List<(double X, double Y)>();
        if (string.IsNullOrWhiteSpace(pathData))
            return points;

        double currentX = 0, currentY = 0;
        double startX = 0, startY = 0;
        double lastControlX = 0, lastControlY = 0;
        char lastCommand = '\0';

        var commands = ParseCommands(pathData);

        foreach (var (command, args) in commands)
        {
            var isRelative = char.IsLower(command);
            var cmd = char.ToUpperInvariant(command);

            switch (cmd)
            {
                case 'M': // Move to
                    ProcessMoveTo(args, isRelative, ref currentX, ref currentY, ref startX, ref startY, points);
                    break;

                case 'L': // Line to
                    ProcessLineTo(args, isRelative, ref currentX, ref currentY, points);
                    break;

                case 'H': // Horizontal line
                    ProcessHorizontalLine(args, isRelative, ref currentX, currentY, points);
                    break;

                case 'V': // Vertical line
                    ProcessVerticalLine(args, isRelative, currentX, ref currentY, points);
                    break;

                case 'C': // Cubic bezier
                    ProcessCubicBezier(args, isRelative, ref currentX, ref currentY, 
                        ref lastControlX, ref lastControlY, points);
                    break;

                case 'S': // Smooth cubic bezier
                    ProcessSmoothCubic(args, isRelative, ref currentX, ref currentY,
                        ref lastControlX, ref lastControlY, lastCommand, points);
                    break;

                case 'Q': // Quadratic bezier
                    ProcessQuadraticBezier(args, isRelative, ref currentX, ref currentY,
                        ref lastControlX, ref lastControlY, points);
                    break;

                case 'T': // Smooth quadratic bezier
                    ProcessSmoothQuadratic(args, isRelative, ref currentX, ref currentY,
                        ref lastControlX, ref lastControlY, lastCommand, points);
                    break;

                case 'A': // Arc
                    ProcessArc(args, isRelative, ref currentX, ref currentY, points);
                    break;

                case 'Z': // Close path
                    currentX = startX;
                    currentY = startY;
                    points.Add((currentX, currentY));
                    break;
            }

            lastCommand = cmd;
        }

        return points;
    }

    /// <summary>
    /// Tests if a point is inside or near the path.
    /// Uses bounding box test plus stroke tolerance.
    /// </summary>
    public static bool HitTest(string pathData, double x, double y, double tolerance = 5.0)
    {
        var bounds = GetBoundingBox(pathData);
        
        // Expand bounds by tolerance for stroke hit testing
        var expandedBounds = (
            X: bounds.X - tolerance,
            Y: bounds.Y - tolerance,
            Width: bounds.Width + tolerance * 2,
            Height: bounds.Height + tolerance * 2
        );

        return x >= expandedBounds.X && 
               x <= expandedBounds.X + expandedBounds.Width &&
               y >= expandedBounds.Y && 
               y <= expandedBounds.Y + expandedBounds.Height;
    }

    private static List<(char Command, double[] Args)> ParseCommands(string pathData)
    {
        var result = new List<(char Command, double[] Args)>();
        var matches = PathCommandRegex().Matches(pathData);

        foreach (Match match in matches)
        {
            var command = match.Groups[1].Value[0];
            var argsStr = match.Groups[2].Value;
            var args = ParseNumbers(argsStr);
            
            // Handle implicit commands (multiple coordinate pairs for same command)
            var argCount = GetExpectedArgCount(command);
            if (argCount > 0 && args.Length > argCount)
            {
                // Split into multiple commands
                for (int i = 0; i < args.Length; i += argCount)
                {
                    var chunk = args.Skip(i).Take(argCount).ToArray();
                    if (chunk.Length == argCount)
                    {
                        // After first M, subsequent coordinates are treated as L
                        var effectiveCommand = (i > 0 && char.ToUpper(command) == 'M') 
                            ? (char.IsUpper(command) ? 'L' : 'l')
                            : command;
                        result.Add((effectiveCommand, chunk));
                    }
                }
            }
            else
            {
                result.Add((command, args));
            }
        }

        return result;
    }

    private static int GetExpectedArgCount(char command) => char.ToUpperInvariant(command) switch
    {
        'M' or 'L' or 'T' => 2,
        'H' or 'V' => 1,
        'C' => 6,
        'S' or 'Q' => 4,
        'A' => 7,
        'Z' => 0,
        _ => 0
    };

    private static double[] ParseNumbers(string str)
    {
        if (string.IsNullOrWhiteSpace(str))
            return [];

        var matches = NumberRegex().Matches(str);
        var result = new double[matches.Count];
        
        for (int i = 0; i < matches.Count; i++)
        {
            if (double.TryParse(matches[i].Value, NumberStyles.Float, CultureInfo.InvariantCulture, out var value))
                result[i] = value;
        }

        return result;
    }

    private static void ProcessMoveTo(double[] args, bool isRelative, 
        ref double currentX, ref double currentY, ref double startX, ref double startY,
        List<(double X, double Y)> points)
    {
        if (args.Length < 2) return;

        if (isRelative)
        {
            currentX += args[0];
            currentY += args[1];
        }
        else
        {
            currentX = args[0];
            currentY = args[1];
        }

        startX = currentX;
        startY = currentY;
        points.Add((currentX, currentY));
    }

    private static void ProcessLineTo(double[] args, bool isRelative,
        ref double currentX, ref double currentY, List<(double X, double Y)> points)
    {
        if (args.Length < 2) return;

        if (isRelative)
        {
            currentX += args[0];
            currentY += args[1];
        }
        else
        {
            currentX = args[0];
            currentY = args[1];
        }

        points.Add((currentX, currentY));
    }

    private static void ProcessHorizontalLine(double[] args, bool isRelative,
        ref double currentX, double currentY, List<(double X, double Y)> points)
    {
        if (args.Length < 1) return;

        currentX = isRelative ? currentX + args[0] : args[0];
        points.Add((currentX, currentY));
    }

    private static void ProcessVerticalLine(double[] args, bool isRelative,
        double currentX, ref double currentY, List<(double X, double Y)> points)
    {
        if (args.Length < 1) return;

        currentY = isRelative ? currentY + args[0] : args[0];
        points.Add((currentX, currentY));
    }

    private static void ProcessCubicBezier(double[] args, bool isRelative,
        ref double currentX, ref double currentY, ref double lastControlX, ref double lastControlY,
        List<(double X, double Y)> points)
    {
        if (args.Length < 6) return;

        double x1, y1, x2, y2, x, y;

        if (isRelative)
        {
            x1 = currentX + args[0];
            y1 = currentY + args[1];
            x2 = currentX + args[2];
            y2 = currentY + args[3];
            x = currentX + args[4];
            y = currentY + args[5];
        }
        else
        {
            x1 = args[0];
            y1 = args[1];
            x2 = args[2];
            y2 = args[3];
            x = args[4];
            y = args[5];
        }

        // Add control points and end point for accurate bounds
        points.Add((x1, y1));
        points.Add((x2, y2));
        points.Add((x, y));

        // Sample bezier curve for better bounds approximation
        SampleCubicBezier(currentX, currentY, x1, y1, x2, y2, x, y, points);

        lastControlX = x2;
        lastControlY = y2;
        currentX = x;
        currentY = y;
    }

    private static void ProcessSmoothCubic(double[] args, bool isRelative,
        ref double currentX, ref double currentY, ref double lastControlX, ref double lastControlY,
        char lastCommand, List<(double X, double Y)> points)
    {
        if (args.Length < 4) return;

        // First control point is reflection of last control point
        double x1, y1;
        if (lastCommand == 'C' || lastCommand == 'S')
        {
            x1 = 2 * currentX - lastControlX;
            y1 = 2 * currentY - lastControlY;
        }
        else
        {
            x1 = currentX;
            y1 = currentY;
        }

        double x2, y2, x, y;
        if (isRelative)
        {
            x2 = currentX + args[0];
            y2 = currentY + args[1];
            x = currentX + args[2];
            y = currentY + args[3];
        }
        else
        {
            x2 = args[0];
            y2 = args[1];
            x = args[2];
            y = args[3];
        }

        points.Add((x1, y1));
        points.Add((x2, y2));
        points.Add((x, y));

        SampleCubicBezier(currentX, currentY, x1, y1, x2, y2, x, y, points);

        lastControlX = x2;
        lastControlY = y2;
        currentX = x;
        currentY = y;
    }

    private static void ProcessQuadraticBezier(double[] args, bool isRelative,
        ref double currentX, ref double currentY, ref double lastControlX, ref double lastControlY,
        List<(double X, double Y)> points)
    {
        if (args.Length < 4) return;

        double x1, y1, x, y;

        if (isRelative)
        {
            x1 = currentX + args[0];
            y1 = currentY + args[1];
            x = currentX + args[2];
            y = currentY + args[3];
        }
        else
        {
            x1 = args[0];
            y1 = args[1];
            x = args[2];
            y = args[3];
        }

        points.Add((x1, y1));
        points.Add((x, y));

        SampleQuadraticBezier(currentX, currentY, x1, y1, x, y, points);

        lastControlX = x1;
        lastControlY = y1;
        currentX = x;
        currentY = y;
    }

    private static void ProcessSmoothQuadratic(double[] args, bool isRelative,
        ref double currentX, ref double currentY, ref double lastControlX, ref double lastControlY,
        char lastCommand, List<(double X, double Y)> points)
    {
        if (args.Length < 2) return;

        // Control point is reflection of last control point
        double x1, y1;
        if (lastCommand == 'Q' || lastCommand == 'T')
        {
            x1 = 2 * currentX - lastControlX;
            y1 = 2 * currentY - lastControlY;
        }
        else
        {
            x1 = currentX;
            y1 = currentY;
        }

        double x, y;
        if (isRelative)
        {
            x = currentX + args[0];
            y = currentY + args[1];
        }
        else
        {
            x = args[0];
            y = args[1];
        }

        points.Add((x1, y1));
        points.Add((x, y));

        SampleQuadraticBezier(currentX, currentY, x1, y1, x, y, points);

        lastControlX = x1;
        lastControlY = y1;
        currentX = x;
        currentY = y;
    }

    private static void ProcessArc(double[] args, bool isRelative,
        ref double currentX, ref double currentY, List<(double X, double Y)> points)
    {
        if (args.Length < 7) return;

        var rx = args[0];
        var ry = args[1];
        // args[2] is x-axis-rotation
        // args[3] is large-arc-flag
        // args[4] is sweep-flag
        double x, y;

        if (isRelative)
        {
            x = currentX + args[5];
            y = currentY + args[6];
        }
        else
        {
            x = args[5];
            y = args[6];
        }

        // For bounds approximation, add corners of the arc's bounding box
        var arcMinX = Math.Min(currentX, x) - rx;
        var arcMinY = Math.Min(currentY, y) - ry;
        var arcMaxX = Math.Max(currentX, x) + rx;
        var arcMaxY = Math.Max(currentY, y) + ry;

        points.Add((arcMinX, arcMinY));
        points.Add((arcMaxX, arcMaxY));
        points.Add((x, y));

        currentX = x;
        currentY = y;
    }

    private static void SampleCubicBezier(double x0, double y0, double x1, double y1,
        double x2, double y2, double x3, double y3, List<(double X, double Y)> points)
    {
        // Sample curve at intervals to catch extrema
        const int samples = 8;
        for (int i = 1; i < samples; i++)
        {
            var t = i / (double)samples;
            var mt = 1 - t;
            var mt2 = mt * mt;
            var mt3 = mt2 * mt;
            var t2 = t * t;
            var t3 = t2 * t;

            var x = mt3 * x0 + 3 * mt2 * t * x1 + 3 * mt * t2 * x2 + t3 * x3;
            var y = mt3 * y0 + 3 * mt2 * t * y1 + 3 * mt * t2 * y2 + t3 * y3;

            points.Add((x, y));
        }
    }

    private static void SampleQuadraticBezier(double x0, double y0, double x1, double y1,
        double x2, double y2, List<(double X, double Y)> points)
    {
        // Sample curve at intervals
        const int samples = 6;
        for (int i = 1; i < samples; i++)
        {
            var t = i / (double)samples;
            var mt = 1 - t;
            var mt2 = mt * mt;
            var t2 = t * t;

            var x = mt2 * x0 + 2 * mt * t * x1 + t2 * x2;
            var y = mt2 * y0 + 2 * mt * t * y1 + t2 * y2;

            points.Add((x, y));
        }
    }

    [GeneratedRegex(@"([MmZzLlHhVvCcSsQqTtAa])([^MmZzLlHhVvCcSsQqTtAa]*)", RegexOptions.Compiled)]
    private static partial Regex PathCommandRegex();

    [GeneratedRegex(@"-?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?", RegexOptions.Compiled)]
    private static partial Regex NumberRegex();
}
