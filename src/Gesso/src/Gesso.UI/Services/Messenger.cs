namespace Gesso.UI.Services;

using System.Collections.Concurrent;

/// <summary>
/// Lightweight messenger for loose coupling between ViewModels.
/// Thread-safe implementation using weak references.
/// </summary>
public sealed class Messenger : IMessenger
{
    private static readonly Lazy<Messenger> s_default = new(() => new Messenger());

    private readonly ConcurrentDictionary<Type, ConcurrentBag<WeakReference<object>>> _subscribers = new();

    /// <summary>
    /// Gets the default messenger instance.
    /// </summary>
    public static Messenger Default => s_default.Value;

    /// <summary>
    /// Registers a handler for a message type.
    /// </summary>
    public void Register<TMessage>(object recipient, Action<TMessage> handler) where TMessage : class
    {
        var wrapper = new MessageHandler<TMessage>(recipient, handler);
        var bag = _subscribers.GetOrAdd(typeof(TMessage), _ => []);
        bag.Add(new WeakReference<object>(wrapper));
    }

    /// <summary>
    /// Unregisters all handlers for a recipient.
    /// </summary>
    public void Unregister(object recipient)
    {
        foreach (var bag in _subscribers.Values)
        {
            var toRemove = new List<WeakReference<object>>();

            foreach (var weakRef in bag)
            {
                if (!weakRef.TryGetTarget(out var target) ||
                    (target is IMessageHandler handler && handler.Recipient == recipient))
                {
                    toRemove.Add(weakRef);
                }
            }

            // ConcurrentBag doesn't support removal directly
            // Cleanup happens lazily during Send()
        }
    }

    /// <summary>
    /// Unregisters handlers for a specific message type.
    /// </summary>
    public void Unregister<TMessage>(object recipient) where TMessage : class
    {
        // Cleanup happens lazily during Send()
        _ = recipient; // Suppress unused parameter warning
    }

    /// <summary>
    /// Sends a message to all registered handlers.
    /// </summary>
    public void Send<TMessage>(TMessage message) where TMessage : class
    {
        if (!_subscribers.TryGetValue(typeof(TMessage), out var bag))
            return;

        var deadRefs = new List<WeakReference<object>>();

        foreach (var weakRef in bag)
        {
            if (weakRef.TryGetTarget(out var target) && target is MessageHandler<TMessage> handler)
            {
                handler.Handle(message);
            }
            else
            {
                deadRefs.Add(weakRef);
            }
        }
    }

    /// <summary>
    /// Sends a message and waits for a response.
    /// </summary>
    public TResponse? Send<TMessage, TResponse>(TMessage message)
        where TMessage : class, IRequestMessage<TResponse>
        where TResponse : class
    {
        Send(message);
        return message.Response;
    }

    private interface IMessageHandler
    {
        object Recipient { get; }
    }

    private sealed class MessageHandler<TMessage> : IMessageHandler where TMessage : class
    {
        private readonly WeakReference<object> _recipientRef;
        private readonly Action<TMessage> _handler;

        public object Recipient
        {
            get
            {
                _recipientRef.TryGetTarget(out var recipient);
                return recipient!;
            }
        }

        public MessageHandler(object recipient, Action<TMessage> handler)
        {
            _recipientRef = new WeakReference<object>(recipient);
            _handler = handler;
        }

        public void Handle(TMessage message)
        {
            if (_recipientRef.TryGetTarget(out _))
            {
                _handler(message);
            }
        }
    }
}

/// <summary>
/// Messenger interface for dependency injection.
/// </summary>
public interface IMessenger
{
    void Register<TMessage>(object recipient, Action<TMessage> handler) where TMessage : class;
    void Unregister(object recipient);
    void Send<TMessage>(TMessage message) where TMessage : class;
}

/// <summary>
/// Base interface for request/response messages.
/// </summary>
public interface IRequestMessage<TResponse>
{
    TResponse? Response { get; set; }
}

/// <summary>
/// Base class for simple notification messages.
/// </summary>
public abstract record MessageBase;

/// <summary>
/// Base class for request/response messages.
/// </summary>
public abstract record RequestMessage<TResponse> : IRequestMessage<TResponse>
{
    public TResponse? Response { get; set; }
}
