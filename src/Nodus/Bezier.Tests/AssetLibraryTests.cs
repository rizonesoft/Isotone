namespace Bezier.Tests;

using Bezier.Core.Services;

public class AssetLibraryServiceTests
{
    private readonly AssetLibraryService _service;

    public AssetLibraryServiceTests()
    {
        _service = new AssetLibraryService();
    }

    [Fact]
    public void AssetLibraryService_HasBuiltInCategories()
    {
        Assert.True(_service.Categories.Count > 0);
        Assert.Contains(_service.Categories, c => c.IsBuiltIn);
    }

    [Fact]
    public void AssetLibraryService_HasBuiltInAssets()
    {
        Assert.True(_service.Assets.Count > 0);
        Assert.Contains(_service.Assets, a => a.IsBuiltIn);
    }

    [Fact]
    public void GetCategoriesByType_ReturnsCorrectType()
    {
        var iconCategories = _service.GetCategoriesByType(AssetType.Icon).ToList();

        Assert.True(iconCategories.Count > 0);
        Assert.All(iconCategories, c => Assert.Equal(AssetType.Icon, c.Type));
    }

    [Fact]
    public void GetCategoriesByType_ReturnsOrderedByOrder()
    {
        var categories = _service.GetCategoriesByType(AssetType.Icon).ToList();

        for (var i = 1; i < categories.Count; i++)
        {
            Assert.True(categories[i].Order >= categories[i - 1].Order);
        }
    }

    [Fact]
    public void GetAssetsByCategory_ReturnsCorrectAssets()
    {
        var assets = _service.GetAssetsByCategory("icons-basic").ToList();

        Assert.True(assets.Count > 0);
        Assert.All(assets, a => Assert.Equal("icons-basic", a.CategoryId));
    }

    [Fact]
    public void GetAssetsByType_ReturnsCorrectType()
    {
        var icons = _service.GetAssetsByType(AssetType.Icon).ToList();

        Assert.True(icons.Count > 0);
        Assert.All(icons, a => Assert.Equal(AssetType.Icon, a.Type));
    }

    [Fact]
    public void GetAsset_ReturnsAssetById()
    {
        var asset = _service.GetAsset("builtin-circle");

        Assert.NotNull(asset);
        Assert.Equal("Circle", asset.Name);
    }

    [Fact]
    public void GetAsset_ReturnsNullForInvalidId()
    {
        var asset = _service.GetAsset("nonexistent");

        Assert.Null(asset);
    }

    [Fact]
    public void Search_FindsByName()
    {
        var results = _service.Search("circle").ToList();

        Assert.True(results.Count > 0);
        Assert.Contains(results, r => r.Asset.Name.Contains("Circle", StringComparison.OrdinalIgnoreCase));
    }

    [Fact]
    public void Search_FindsByTag()
    {
        var results = _service.Search("shape").ToList();

        Assert.True(results.Count > 0);
    }

    [Fact]
    public void Search_EmptyQuery_ReturnsEmpty()
    {
        var results = _service.Search("").ToList();

        Assert.Empty(results);
    }

    [Fact]
    public void Search_FiltersByType()
    {
        var results = _service.Search("icon", AssetType.Template).ToList();

        Assert.All(results, r => Assert.Equal(AssetType.Template, r.Asset.Type));
    }

    [Fact]
    public void Search_ReturnsScores()
    {
        var results = _service.Search("arrow").ToList();

        Assert.True(results.Count > 0);
        Assert.All(results, r => Assert.True(r.Score > 0));
    }

    [Fact]
    public void Search_OrdersByScore()
    {
        var results = _service.Search("arrow").ToList();

        for (var i = 1; i < results.Count; i++)
        {
            Assert.True(results[i].Score <= results[i - 1].Score);
        }
    }

    [Fact]
    public void AddUserAsset_AddsToAssets()
    {
        var initialCount = _service.Assets.Count;
        var svg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect/></svg>""";

        var asset = _service.AddUserAsset("Test Asset", svg);

        Assert.Equal(initialCount + 1, _service.Assets.Count);
        Assert.Equal("Test Asset", asset.Name);
        Assert.Equal(AssetType.UserAsset, asset.Type);
        Assert.False(asset.IsBuiltIn);
    }

    [Fact]
    public void AddUserAsset_ExtractsDimensions()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="150"><rect/></svg>""";

        var asset = _service.AddUserAsset("Test", svg);

        Assert.Equal(200, asset.Width);
        Assert.Equal(150, asset.Height);
    }

    [Fact]
    public void AddUserAsset_RaisesEvent()
    {
        Asset? addedAsset = null;
        _service.AssetAdded += (_, a) => addedAsset = a;
        var svg = """<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>""";

        _service.AddUserAsset("Test", svg);

        Assert.NotNull(addedAsset);
    }

    [Fact]
    public void RemoveAsset_RemovesUserAsset()
    {
        var svg = """<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>""";
        var asset = _service.AddUserAsset("To Remove", svg);

        var removed = _service.RemoveAsset(asset.Id);

        Assert.True(removed);
        Assert.Null(_service.GetAsset(asset.Id));
    }

    [Fact]
    public void RemoveAsset_CannotRemoveBuiltIn()
    {
        var removed = _service.RemoveAsset("builtin-circle");

        Assert.False(removed);
        Assert.NotNull(_service.GetAsset("builtin-circle"));
    }

    [Fact]
    public void ToggleFavorite_AddsFavorite()
    {
        var isFavorite = _service.ToggleFavorite("builtin-circle");

        Assert.True(isFavorite);
        Assert.Contains("builtin-circle", _service.Favorites);
    }

    [Fact]
    public void ToggleFavorite_RemovesFavorite()
    {
        _service.ToggleFavorite("builtin-circle"); // Add
        var isFavorite = _service.ToggleFavorite("builtin-circle"); // Remove

        Assert.False(isFavorite);
        Assert.DoesNotContain("builtin-circle", _service.Favorites);
    }

    [Fact]
    public void GetFavorites_ReturnsFavoriteAssets()
    {
        // Ensure asset exists
        var asset = _service.GetAsset("builtin-star");
        Assert.NotNull(asset);
        
        // Ensure it's a favorite (toggle until true)
        if (!_service.Favorites.Contains("builtin-star"))
        {
            _service.ToggleFavorite("builtin-star");
        }
        Assert.Contains("builtin-star", _service.Favorites);

        var favorites = _service.GetFavorites().ToList();

        Assert.NotEmpty(favorites);
        Assert.Contains(favorites, a => a.Id == "builtin-star");
    }

    [Fact]
    public void MarkAsUsed_AddsToRecentlyUsed()
    {
        _service.MarkAsUsed("builtin-circle");

        Assert.Contains("builtin-circle", _service.RecentlyUsed);
    }

    [Fact]
    public void MarkAsUsed_MovesToTop()
    {
        _service.MarkAsUsed("builtin-square");
        _service.MarkAsUsed("builtin-circle");
        _service.MarkAsUsed("builtin-square");

        Assert.Equal("builtin-square", _service.RecentlyUsed[0]);
    }

    [Fact]
    public void MarkAsUsed_IncrementsUsageCount()
    {
        var asset = _service.GetAsset("builtin-circle")!;
        var initialCount = asset.UsageCount;

        _service.MarkAsUsed("builtin-circle");

        Assert.Equal(initialCount + 1, asset.UsageCount);
    }

    [Fact]
    public void GetRecentlyUsed_ReturnsRecentAssets()
    {
        _service.MarkAsUsed("builtin-circle");

        var recent = _service.GetRecentlyUsed().ToList();

        Assert.Contains(recent, a => a.Id == "builtin-circle");
    }

    [Fact]
    public void CreateFolder_CreatesFolder()
    {
        var folder = _service.CreateFolder("Test Folder");

        Assert.NotNull(folder);
        Assert.Equal("Test Folder", folder.Name);
        Assert.Contains(folder, _service.Folders);
    }

    [Fact]
    public void CreateFolder_WithParent()
    {
        var parent = _service.CreateFolder("Parent");
        var child = _service.CreateFolder("Child", parent.Id);

        Assert.Equal(parent.Id, child.ParentId);
    }

    [Fact]
    public void CreateFolder_WithColor()
    {
        var folder = _service.CreateFolder("Colored", null, "#FF0000");

        Assert.Equal("#FF0000", folder.Color);
    }

    [Fact]
    public void RemoveFolder_RemovesFolder()
    {
        var folder = _service.CreateFolder("To Remove");

        var removed = _service.RemoveFolder(folder.Id);

        Assert.True(removed);
        Assert.DoesNotContain(folder, _service.Folders);
    }

    [Fact]
    public void AddToFolder_AddsAssetToFolder()
    {
        var folder = _service.CreateFolder("Test");

        var added = _service.AddToFolder("builtin-circle", folder.Id);

        Assert.True(added);
        Assert.Contains("builtin-circle", folder.AssetIds);
    }

    [Fact]
    public void RemoveFromFolder_RemovesAssetFromFolder()
    {
        var folder = _service.CreateFolder("Test");
        _service.AddToFolder("builtin-circle", folder.Id);

        var removed = _service.RemoveFromFolder("builtin-circle", folder.Id);

        Assert.True(removed);
        Assert.DoesNotContain("builtin-circle", folder.AssetIds);
    }

    [Fact]
    public void GetAssetsInFolder_ReturnsCorrectAssets()
    {
        var folder = _service.CreateFolder("Test");
        _service.AddToFolder("builtin-circle", folder.Id);
        _service.AddToFolder("builtin-square", folder.Id);

        var assets = _service.GetAssetsInFolder(folder.Id).ToList();

        Assert.Equal(2, assets.Count);
        Assert.Contains(assets, a => a.Id == "builtin-circle");
        Assert.Contains(assets, a => a.Id == "builtin-square");
    }
}

public class AssetTests
{
    [Fact]
    public void Asset_DefaultValues()
    {
        var asset = new Asset();

        Assert.NotEmpty(asset.Id);
        Assert.Equal(string.Empty, asset.Name);
        Assert.Equal(AssetType.Icon, asset.Type);
        Assert.False(asset.IsBuiltIn);
        Assert.False(asset.IsFavorite);
        Assert.Equal(0, asset.UsageCount);
    }

    [Fact]
    public void Asset_CanSetAllProperties()
    {
        var asset = new Asset
        {
            Name = "Test",
            Description = "Description",
            Type = AssetType.Template,
            CategoryId = "cat1",
            SvgContent = "<svg></svg>",
            Tags = ["tag1", "tag2"],
            IsBuiltIn = true,
            Width = 100,
            Height = 50
        };

        Assert.Equal("Test", asset.Name);
        Assert.Equal("Description", asset.Description);
        Assert.Equal(AssetType.Template, asset.Type);
        Assert.Equal("cat1", asset.CategoryId);
        Assert.Equal("<svg></svg>", asset.SvgContent);
        Assert.Equal(2, asset.Tags!.Length);
        Assert.True(asset.IsBuiltIn);
        Assert.Equal(100, asset.Width);
        Assert.Equal(50, asset.Height);
    }
}

public class AssetCategoryTests
{
    [Fact]
    public void AssetCategory_DefaultValues()
    {
        var category = new AssetCategory();

        Assert.NotEmpty(category.Id);
        Assert.Equal(string.Empty, category.Name);
        Assert.Equal(AssetType.Icon, category.Type);
        Assert.Equal(0, category.Order);
        Assert.False(category.IsBuiltIn);
    }
}

public class AssetFolderTests
{
    [Fact]
    public void AssetFolder_DefaultValues()
    {
        var folder = new AssetFolder();

        Assert.NotEmpty(folder.Id);
        Assert.Equal(string.Empty, folder.Name);
        Assert.Null(folder.ParentId);
        Assert.Null(folder.Color);
        Assert.Empty(folder.AssetIds);
    }
}

public class AssetSearchResultTests
{
    [Fact]
    public void AssetSearchResult_CanSetAllProperties()
    {
        var asset = new Asset { Name = "Test" };
        var result = new AssetSearchResult
        {
            Asset = asset,
            Score = 10.5,
            MatchedTerms = ["term1", "term2"]
        };

        Assert.Equal(asset, result.Asset);
        Assert.Equal(10.5, result.Score);
        Assert.Equal(2, result.MatchedTerms.Length);
    }
}

public class TemplateTests
{
    [Fact]
    public void Template_ExtendsAsset()
    {
        var template = new Template
        {
            Name = "Test Template",
            Author = "Test Author",
            License = "MIT"
        };

        Assert.Equal("Test Template", template.Name);
        Assert.Equal("Test Author", template.Author);
        Assert.Equal("MIT", template.License);
    }

    [Fact]
    public void Template_CanHavePreset()
    {
        var template = new Template
        {
            Preset = DocumentPresets.Icon64
        };

        Assert.NotNull(template.Preset);
        Assert.Equal(64, template.Preset.Width);
    }
}

public class AssetTypeTests
{
    [Fact]
    public void AssetType_HasExpectedValues()
    {
        Assert.True(Enum.IsDefined(typeof(AssetType), AssetType.Icon));
        Assert.True(Enum.IsDefined(typeof(AssetType), AssetType.Template));
        Assert.True(Enum.IsDefined(typeof(AssetType), AssetType.UserAsset));
        Assert.True(Enum.IsDefined(typeof(AssetType), AssetType.Shape));
        Assert.True(Enum.IsDefined(typeof(AssetType), AssetType.Pattern));
    }
}
