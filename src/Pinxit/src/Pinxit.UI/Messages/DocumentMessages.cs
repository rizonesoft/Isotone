namespace Pinxit.UI.Messages;

using Pinxit.UI.Services;

/// <summary>
/// Message sent when a document is opened.
/// </summary>
public sealed record DocumentOpenedMessage(string FilePath) : MessageBase;

/// <summary>
/// Message sent when a document is closed.
/// </summary>
public sealed record DocumentClosedMessage : MessageBase;

/// <summary>
/// Message sent when a document is saved.
/// </summary>
public sealed record DocumentSavedMessage(string FilePath) : MessageBase;

/// <summary>
/// Message sent when the active document changes.
/// </summary>
public sealed record ActiveDocumentChangedMessage(object? Document) : MessageBase;

/// <summary>
/// Message sent when document dirty state changes.
/// </summary>
public sealed record DocumentDirtyChangedMessage(bool IsDirty) : MessageBase;

/// <summary>
/// Message requesting to save the current document.
/// </summary>
public sealed record SaveDocumentRequestMessage : RequestMessage<bool>;

/// <summary>
/// Message requesting to close the current document.
/// </summary>
public sealed record CloseDocumentRequestMessage : RequestMessage<bool>;
