namespace Pinxit.UI.Views;

using System.Windows;
using Wpf.Ui;
using Wpf.Ui.Appearance;
using Wpf.Ui.Controls;
using Pinxit.UI.ViewModels;

public partial class MainWindow : FluentWindow
{
    private readonly MainWindowViewModel _viewModel;
    private readonly ISnackbarService _snackbarService;
    private readonly IContentDialogService _contentDialogService;

    public MainWindow(
        MainWindowViewModel viewModel,
        ISnackbarService snackbarService,
        IContentDialogService contentDialogService)
    {
        _viewModel = viewModel;
        _snackbarService = snackbarService;
        _contentDialogService = contentDialogService;

        DataContext = _viewModel;

        InitializeComponent();

        _snackbarService.SetSnackbarPresenter(SnackbarPresenter);
        _contentDialogService.SetDialogHost(RootContentDialog);

        Loaded += OnLoaded;
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        SystemThemeWatcher.Watch(this);

        ApplicationThemeManager.Apply(ApplicationTheme.Dark);
    }
}
