namespace Pinxit.Scripting;

using Microsoft.CodeAnalysis.CSharp.Scripting;
using Microsoft.CodeAnalysis.Scripting;
using Serilog;

/// <summary>
/// Roslyn-based scripting engine for Pinxit automation.
/// </summary>
public sealed class ScriptEngine
{
    private readonly ILogger _logger = Log.ForContext<ScriptEngine>();
    private readonly ScriptOptions _scriptOptions;

    public ScriptEngine()
    {
        _scriptOptions = ScriptOptions.Default
            .AddReferences(typeof(object).Assembly)
            .AddImports("System", "System.Linq", "System.Collections.Generic");
    }

    public async Task<T> EvaluateAsync<T>(string code, CancellationToken cancellationToken = default)
    {
        _logger.Debug("Evaluating script: {Code}", code);

        try
        {
            var result = await CSharpScript.EvaluateAsync<T>(
                code,
                _scriptOptions,
                cancellationToken: cancellationToken);

            _logger.Debug("Script result: {Result}", result);
            return result;
        }
        catch (CompilationErrorException ex)
        {
            _logger.Error(ex, "Script compilation error");
            throw;
        }
    }

    public async Task RunAsync(string code, CancellationToken cancellationToken = default)
    {
        _logger.Debug("Running script: {Code}", code);

        try
        {
            await CSharpScript.RunAsync(
                code,
                _scriptOptions,
                cancellationToken: cancellationToken);

            _logger.Debug("Script completed successfully");
        }
        catch (CompilationErrorException ex)
        {
            _logger.Error(ex, "Script compilation error");
            throw;
        }
    }
}
