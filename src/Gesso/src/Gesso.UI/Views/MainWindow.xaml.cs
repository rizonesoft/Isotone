namespace Gesso.UI.Views;

using System.Windows;
using Wpf.Ui;
using Wpf.Ui.Appearance;
using Wpf.Ui.Controls;
using Gesso.UI.ViewModels;

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
        // WORKAROUND: WPF-UI 4.3 marks SetDialogHost(ContentPresenter) obsolete, and its replacement needs a WPF-UI
        // ContentDialogHost, which the design contract forbids adding. D03 T01 §3 removes the WPF-UI dialog service,
        // and this call and its pragma with it; until then CS0618 is excused on this line alone.
#pragma warning disable CS0618
        _contentDialogService.SetDialogHost(RootContentDialog);
#pragma warning restore CS0618

        Loaded += OnLoaded;
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        SystemThemeWatcher.Watch(this);

        ApplicationThemeManager.Apply(ApplicationTheme.Dark);
    }
}
