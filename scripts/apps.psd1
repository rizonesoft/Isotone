# Suite app manifest: the one place scripts/*.ps1 and CI learn about each app.
# Shipping = $false means the app has no code yet; publish and package refuse it.
@{
  Stilus = @{
    Project   = 'src/Stilus/Bezier.Desktop/Bezier.Desktop.csproj'
    Exe       = 'Bezier.Desktop.exe'
    TagPrefix = 'stilus-v'
    Installer = 'installer/Stilus.iss'
    Shipping  = $true
  }
  Gesso = @{
    Project   = 'src/Gesso/src/Gesso.UI/Gesso.UI.csproj'
    Exe       = 'Gesso.exe'
    TagPrefix = 'gesso-v'
    Installer = 'installer/Gesso.iss'
    Shipping  = $true
  }
  Albumen = @{
    Project   = 'src/Albumen/Albumen.UI/Albumen.UI.csproj'
    Exe       = 'Albumen.exe'
    TagPrefix = 'albumen-v'
    Installer = 'installer/Albumen.iss'
    Shipping  = $false
  }
}
