using System.ComponentModel;
using System.Text.Json;

namespace Bezier.Core.Services;

/// <summary>
/// Type of asset in the library.
/// </summary>
public enum AssetType
{
    Icon,
    Template,
    UserAsset,
    Shape,
    Pattern
}

/// <summary>
/// Category for organizing assets.
/// </summary>
public class AssetCategory
{
    public string Id { get; init; } = Guid.NewGuid().ToString();
    public string Name { get; init; } = string.Empty;
    public string? Icon { get; init; }
    public AssetType Type { get; init; }
    public int Order { get; init; }
    public bool IsBuiltIn { get; init; }
}

/// <summary>
/// Represents an asset in the library.
/// </summary>
public class Asset
{
    public string Id { get; init; } = Guid.NewGuid().ToString();
    public string Name { get; init; } = string.Empty;
    public string? Description { get; init; }
    public AssetType Type { get; init; }
    public string CategoryId { get; init; } = string.Empty;
    public string SvgContent { get; init; } = string.Empty;
    public string[]? Tags { get; init; }
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
    public DateTime? ModifiedAt { get; init; }
    public bool IsBuiltIn { get; init; }
    public bool IsFavorite { get; set; }
    public int UsageCount { get; set; }
    public string? ThumbnailPath { get; init; }
    public double Width { get; init; }
    public double Height { get; init; }
}

/// <summary>
/// Template with metadata.
/// </summary>
public class Template : Asset
{
    public string? Author { get; init; }
    public string? License { get; init; }
    public DocumentPreset? Preset { get; init; }
}

/// <summary>
/// User folder for organizing assets.
/// </summary>
public class AssetFolder
{
    public string Id { get; init; } = Guid.NewGuid().ToString();
    public string Name { get; init; } = string.Empty;
    public string? ParentId { get; init; }
    public string? Color { get; init; }
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
    public List<string> AssetIds { get; init; } = [];
}

/// <summary>
/// Search result for assets.
/// </summary>
public class AssetSearchResult
{
    public Asset Asset { get; init; } = null!;
    public double Score { get; init; }
    public string[] MatchedTerms { get; init; } = [];
}

/// <summary>
/// Service for managing asset libraries.
/// </summary>
public class AssetLibraryService : INotifyPropertyChanged
{
    private readonly List<AssetCategory> _categories = [];
    private readonly List<Asset> _assets = [];
    private readonly List<AssetFolder> _folders = [];
    private readonly List<string> _favorites = [];
    private readonly List<string> _recentlyUsed = [];
    private readonly string _userLibraryPath;

    public const int MaxRecentItems = 20;

    public event PropertyChangedEventHandler? PropertyChanged;
    public event EventHandler<Asset>? AssetAdded;
    public event EventHandler<Asset>? AssetRemoved;
    public event EventHandler<Asset>? AssetUsed;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    public AssetLibraryService()
    {
        var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        _userLibraryPath = Path.Combine(appData, "Bezier", "Library");
        Directory.CreateDirectory(_userLibraryPath);

        InitializeBuiltInAssets();
        LoadUserLibrary();
    }

    /// <summary>
    /// Gets all categories.
    /// </summary>
    public IReadOnlyList<AssetCategory> Categories => _categories;

    /// <summary>
    /// Gets all assets.
    /// </summary>
    public IReadOnlyList<Asset> Assets => _assets;

    /// <summary>
    /// Gets user folders.
    /// </summary>
    public IReadOnlyList<AssetFolder> Folders => _folders;

    /// <summary>
    /// Gets favorite asset IDs.
    /// </summary>
    public IReadOnlyList<string> Favorites => _favorites;

    /// <summary>
    /// Gets recently used asset IDs.
    /// </summary>
    public IReadOnlyList<string> RecentlyUsed => _recentlyUsed;

    /// <summary>
    /// Gets categories by type.
    /// </summary>
    public IEnumerable<AssetCategory> GetCategoriesByType(AssetType type)
    {
        return _categories.Where(c => c.Type == type).OrderBy(c => c.Order);
    }

    /// <summary>
    /// Gets assets by category.
    /// </summary>
    public IEnumerable<Asset> GetAssetsByCategory(string categoryId)
    {
        return _assets.Where(a => a.CategoryId == categoryId);
    }

    /// <summary>
    /// Gets assets by type.
    /// </summary>
    public IEnumerable<Asset> GetAssetsByType(AssetType type)
    {
        return _assets.Where(a => a.Type == type);
    }

    /// <summary>
    /// Gets favorite assets.
    /// </summary>
    public IEnumerable<Asset> GetFavorites()
    {
        return _assets.Where(a => _favorites.Contains(a.Id));
    }

    /// <summary>
    /// Gets recently used assets.
    /// </summary>
    public IEnumerable<Asset> GetRecentlyUsed()
    {
        return _recentlyUsed
            .Select(id => _assets.FirstOrDefault(a => a.Id == id))
            .Where(a => a != null)!;
    }

    /// <summary>
    /// Searches assets by query.
    /// </summary>
    public IEnumerable<AssetSearchResult> Search(string query, AssetType? type = null)
    {
        if (string.IsNullOrWhiteSpace(query))
            return [];

        var terms = query.ToLowerInvariant().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var results = new List<AssetSearchResult>();

        foreach (var asset in _assets)
        {
            if (type.HasValue && asset.Type != type.Value)
                continue;

            var (score, matchedTerms) = CalculateSearchScore(asset, terms);
            if (score > 0)
            {
                results.Add(new AssetSearchResult
                {
                    Asset = asset,
                    Score = score,
                    MatchedTerms = matchedTerms
                });
            }
        }

        return results.OrderByDescending(r => r.Score);
    }

    /// <summary>
    /// Gets an asset by ID.
    /// </summary>
    public Asset? GetAsset(string id)
    {
        return _assets.FirstOrDefault(a => a.Id == id);
    }

    /// <summary>
    /// Adds a user asset.
    /// </summary>
    public Asset AddUserAsset(string name, string svgContent, string? categoryId = null, string[]? tags = null)
    {
        var (width, height) = ExportService.GetSvgDimensions(svgContent);

        var asset = new Asset
        {
            Name = name,
            Type = AssetType.UserAsset,
            CategoryId = categoryId ?? "user-general",
            SvgContent = svgContent,
            Tags = tags,
            IsBuiltIn = false,
            Width = width,
            Height = height
        };

        _assets.Add(asset);
        SaveUserLibrary();
        AssetAdded?.Invoke(this, asset);
        OnPropertyChanged(nameof(Assets));

        return asset;
    }

    /// <summary>
    /// Removes a user asset.
    /// </summary>
    public bool RemoveAsset(string assetId)
    {
        var asset = _assets.FirstOrDefault(a => a.Id == assetId && !a.IsBuiltIn);
        if (asset == null) return false;

        _assets.Remove(asset);
        _favorites.Remove(assetId);
        _recentlyUsed.Remove(assetId);

        foreach (var folder in _folders)
        {
            folder.AssetIds.Remove(assetId);
        }

        SaveUserLibrary();
        AssetRemoved?.Invoke(this, asset);
        OnPropertyChanged(nameof(Assets));

        return true;
    }

    /// <summary>
    /// Toggles favorite status.
    /// </summary>
    public bool ToggleFavorite(string assetId)
    {
        var asset = _assets.FirstOrDefault(a => a.Id == assetId);
        if (asset == null) return false;

        if (_favorites.Contains(assetId))
        {
            _favorites.Remove(assetId);
            asset.IsFavorite = false;
        }
        else
        {
            _favorites.Add(assetId);
            asset.IsFavorite = true;
        }

        SaveUserLibrary();
        OnPropertyChanged(nameof(Favorites));
        return asset.IsFavorite;
    }

    /// <summary>
    /// Marks an asset as used.
    /// </summary>
    public void MarkAsUsed(string assetId)
    {
        var asset = _assets.FirstOrDefault(a => a.Id == assetId);
        if (asset == null) return;

        asset.UsageCount++;
        _recentlyUsed.Remove(assetId);
        _recentlyUsed.Insert(0, assetId);

        while (_recentlyUsed.Count > MaxRecentItems)
        {
            _recentlyUsed.RemoveAt(_recentlyUsed.Count - 1);
        }

        SaveUserLibrary();
        AssetUsed?.Invoke(this, asset);
        OnPropertyChanged(nameof(RecentlyUsed));
    }

    /// <summary>
    /// Creates a folder.
    /// </summary>
    public AssetFolder CreateFolder(string name, string? parentId = null, string? color = null)
    {
        var folder = new AssetFolder
        {
            Name = name,
            ParentId = parentId,
            Color = color
        };

        _folders.Add(folder);
        SaveUserLibrary();
        OnPropertyChanged(nameof(Folders));

        return folder;
    }

    /// <summary>
    /// Removes a folder.
    /// </summary>
    public bool RemoveFolder(string folderId)
    {
        var folder = _folders.FirstOrDefault(f => f.Id == folderId);
        if (folder == null) return false;

        _folders.Remove(folder);
        SaveUserLibrary();
        OnPropertyChanged(nameof(Folders));

        return true;
    }

    /// <summary>
    /// Adds an asset to a folder.
    /// </summary>
    public bool AddToFolder(string assetId, string folderId)
    {
        var folder = _folders.FirstOrDefault(f => f.Id == folderId);
        if (folder == null) return false;

        if (!folder.AssetIds.Contains(assetId))
        {
            folder.AssetIds.Add(assetId);
            SaveUserLibrary();
        }

        return true;
    }

    /// <summary>
    /// Removes an asset from a folder.
    /// </summary>
    public bool RemoveFromFolder(string assetId, string folderId)
    {
        var folder = _folders.FirstOrDefault(f => f.Id == folderId);
        if (folder == null) return false;

        var removed = folder.AssetIds.Remove(assetId);
        if (removed)
        {
            SaveUserLibrary();
        }

        return removed;
    }

    /// <summary>
    /// Gets assets in a folder.
    /// </summary>
    public IEnumerable<Asset> GetAssetsInFolder(string folderId)
    {
        var folder = _folders.FirstOrDefault(f => f.Id == folderId);
        if (folder == null) return [];

        return folder.AssetIds
            .Select(id => _assets.FirstOrDefault(a => a.Id == id))
            .Where(a => a != null)!;
    }

    /// <summary>
    /// Imports SVG files to user library.
    /// </summary>
    public List<Asset> ImportFiles(IEnumerable<string> filePaths, string? folderId = null)
    {
        var imported = new List<Asset>();

        foreach (var path in filePaths)
        {
            if (!File.Exists(path)) continue;

            try
            {
                var content = File.ReadAllText(path);
                var name = Path.GetFileNameWithoutExtension(path);
                var asset = AddUserAsset(name, content);

                if (folderId != null)
                {
                    AddToFolder(asset.Id, folderId);
                }

                imported.Add(asset);
            }
            catch
            {
                // Skip invalid files
            }
        }

        return imported;
    }

    private (double Score, string[] MatchedTerms) CalculateSearchScore(Asset asset, string[] terms)
    {
        var score = 0.0;
        var matched = new List<string>();

        var nameLower = asset.Name.ToLowerInvariant();
        var descLower = asset.Description?.ToLowerInvariant() ?? "";
        var tagsLower = asset.Tags?.Select(t => t.ToLowerInvariant()).ToArray() ?? [];

        foreach (var term in terms)
        {
            if (nameLower.Contains(term))
            {
                score += nameLower == term ? 10 : 5;
                matched.Add(term);
            }
            else if (descLower.Contains(term))
            {
                score += 2;
                matched.Add(term);
            }
            else if (tagsLower.Any(t => t.Contains(term)))
            {
                score += tagsLower.Any(t => t == term) ? 8 : 3;
                matched.Add(term);
            }
        }

        // Bonus for matching all terms
        if (matched.Count == terms.Length && terms.Length > 1)
        {
            score *= 1.5;
        }

        return (score, matched.Distinct().ToArray());
    }

    private void InitializeBuiltInAssets()
    {
        // Icon categories
        _categories.AddRange([
            new AssetCategory { Id = "icons-basic", Name = "Basic Shapes", Type = AssetType.Icon, Order = 1, IsBuiltIn = true },
            new AssetCategory { Id = "icons-arrows", Name = "Arrows", Type = AssetType.Icon, Order = 2, IsBuiltIn = true },
            new AssetCategory { Id = "icons-ui", Name = "UI Elements", Type = AssetType.Icon, Order = 3, IsBuiltIn = true },
            new AssetCategory { Id = "icons-social", Name = "Social Media", Type = AssetType.Icon, Order = 4, IsBuiltIn = true },
            new AssetCategory { Id = "icons-file", Name = "Files & Folders", Type = AssetType.Icon, Order = 5, IsBuiltIn = true },
            new AssetCategory { Id = "icons-media", Name = "Media", Type = AssetType.Icon, Order = 6, IsBuiltIn = true }
        ]);

        // Template categories
        _categories.AddRange([
            new AssetCategory { Id = "templates-logos", Name = "Logos", Type = AssetType.Template, Order = 1, IsBuiltIn = true },
            new AssetCategory { Id = "templates-icons", Name = "Icon Sets", Type = AssetType.Template, Order = 2, IsBuiltIn = true },
            new AssetCategory { Id = "templates-social", Name = "Social Media", Type = AssetType.Template, Order = 3, IsBuiltIn = true },
            new AssetCategory { Id = "templates-web", Name = "Web Graphics", Type = AssetType.Template, Order = 4, IsBuiltIn = true }
        ]);

        // User category
        _categories.Add(new AssetCategory { Id = "user-general", Name = "My Assets", Type = AssetType.UserAsset, Order = 1, IsBuiltIn = false });

        // Built-in icons (basic shapes)
        _assets.AddRange([
            CreateBuiltInIcon("circle", "Circle", "icons-basic", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["shape", "round"]),
            CreateBuiltInIcon("square", "Square", "icons-basic", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["shape", "rectangle"]),
            CreateBuiltInIcon("triangle", "Triangle", "icons-basic", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><polygon points="12,2 22,22 2,22" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["shape"]),
            CreateBuiltInIcon("star", "Star", "icons-basic", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><polygon points="12,2 15,9 22,9 17,14 19,22 12,18 5,22 7,14 2,9 9,9" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["shape", "favorite"]),
            CreateBuiltInIcon("heart", "Heart", "icons-basic", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["love", "like"]),
            
            CreateBuiltInIcon("arrow-right", "Arrow Right", "icons-arrows", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M5 12h14m-7-7l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["direction", "next"]),
            CreateBuiltInIcon("arrow-left", "Arrow Left", "icons-arrows", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M19 12H5m7-7l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["direction", "back"]),
            CreateBuiltInIcon("arrow-up", "Arrow Up", "icons-arrows", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 19V5m-7 7l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["direction"]),
            CreateBuiltInIcon("arrow-down", "Arrow Down", "icons-arrows", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 5v14m-7-7l7 7 7-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["direction"]),
            
            CreateBuiltInIcon("check", "Checkmark", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["done", "success", "tick"]),
            CreateBuiltInIcon("x", "Close", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["close", "remove", "delete"]),
            CreateBuiltInIcon("plus", "Plus", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 5v14m-7-7h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["add", "new"]),
            CreateBuiltInIcon("minus", "Minus", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M5 12h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["remove", "subtract"]),
            CreateBuiltInIcon("menu", "Menu", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M3 12h18M3 6h18M3 18h18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""", ["hamburger", "navigation"]),
            CreateBuiltInIcon("search", "Search", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M21 21l-4.35-4.35" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""", ["find", "magnifier"]),
            CreateBuiltInIcon("settings", "Settings", "icons-ui", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["gear", "preferences"]),
            
            CreateBuiltInIcon("file", "File", "icons-file", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9l-7-7z" fill="none" stroke="currentColor" stroke-width="2"/><polyline points="13 2 13 9 20 9" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["document"]),
            CreateBuiltInIcon("folder", "Folder", "icons-file", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2v11z" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["directory"]),
            CreateBuiltInIcon("download", "Download", "icons-file", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-5l5 5 5-5m-5 5V3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["save"]),
            CreateBuiltInIcon("upload", "Upload", "icons-file", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m14-7l-5-5-5 5m5-5v12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""", ["export"]),
            
            CreateBuiltInIcon("play", "Play", "icons-media", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>""", ["start", "video"]),
            CreateBuiltInIcon("pause", "Pause", "icons-media", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16" fill="none" stroke="currentColor" stroke-width="2"/><rect x="14" y="4" width="4" height="16" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["stop"]),
            CreateBuiltInIcon("image", "Image", "icons-media", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/><polyline points="21 15 16 10 5 21" fill="none" stroke="currentColor" stroke-width="2"/></svg>""", ["photo", "picture"])
        ]);

        // Built-in templates
        _assets.AddRange([
            new Template
            {
                Id = "template-app-icon",
                Name = "App Icon",
                Description = "Basic app icon template",
                Type = AssetType.Template,
                CategoryId = "templates-icons",
                SvgContent = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" rx="64" fill="#4F46E5"/><circle cx="256" cy="256" r="128" fill="white"/></svg>""",
                Tags = ["app", "icon", "mobile"],
                IsBuiltIn = true,
                Width = 512,
                Height = 512,
                Preset = DocumentPresets.MobileIPhoneApp
            },
            new Template
            {
                Id = "template-social-post",
                Name = "Social Post",
                Description = "Instagram square post template",
                Type = AssetType.Template,
                CategoryId = "templates-social",
                SvgContent = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"><rect width="1080" height="1080" fill="#1a1a2e"/><text x="540" y="540" text-anchor="middle" fill="white" font-size="72">Your Text Here</text></svg>""",
                Tags = ["social", "instagram", "post"],
                IsBuiltIn = true,
                Width = 1080,
                Height = 1080,
                Preset = DocumentPresets.SocialInstagramSquare
            }
        ]);
    }

    private static Asset CreateBuiltInIcon(string id, string name, string categoryId, string svgContent, string[] tags)
    {
        return new Asset
        {
            Id = $"builtin-{id}",
            Name = name,
            Type = AssetType.Icon,
            CategoryId = categoryId,
            SvgContent = svgContent,
            Tags = tags,
            IsBuiltIn = true,
            Width = 24,
            Height = 24
        };
    }

    private void LoadUserLibrary()
    {
        var libraryFile = Path.Combine(_userLibraryPath, "library.json");
        if (!File.Exists(libraryFile)) return;

        try
        {
            var json = File.ReadAllText(libraryFile);
            var data = JsonSerializer.Deserialize<UserLibraryData>(json);
            if (data != null)
            {
                _assets.AddRange(data.Assets);
                _folders.AddRange(data.Folders);
                _favorites.AddRange(data.Favorites);
                _recentlyUsed.AddRange(data.RecentlyUsed);
            }
        }
        catch
        {
            // Ignore load errors
        }
    }

    private void SaveUserLibrary()
    {
        try
        {
            var data = new UserLibraryData
            {
                Assets = _assets.Where(a => !a.IsBuiltIn).ToList(),
                Folders = _folders.ToList(),
                Favorites = _favorites.ToList(),
                RecentlyUsed = _recentlyUsed.ToList()
            };

            var json = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
            var libraryFile = Path.Combine(_userLibraryPath, "library.json");
            File.WriteAllText(libraryFile, json);
        }
        catch
        {
            // Ignore save errors
        }
    }

    private class UserLibraryData
    {
        public List<Asset> Assets { get; set; } = [];
        public List<AssetFolder> Folders { get; set; } = [];
        public List<string> Favorites { get; set; } = [];
        public List<string> RecentlyUsed { get; set; } = [];
    }
}
