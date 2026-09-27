using Microsoft.Extensions.DependencyInjection;

namespace Bezier.Desktop;

/// <summary>
/// Extension methods for configuring services in the DI container.
/// </summary>
public static class ServiceCollectionExtensions
{
    /// <summary>
    /// Registers all Bezier application services.
    /// </summary>
    public static IServiceCollection AddBezierServices(this IServiceCollection services)
    {
        // Core services
        // services.AddSingleton<IHistoryManager, HistoryManager>();
        // services.AddSingleton<IToolManager, ToolManager>();
        
        // ViewModels
        services.AddTransient<ViewModels.MainWindowViewModel>();
        
        return services;
    }
}
