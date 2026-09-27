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
  Pinxit = @{
    Project   = 'src/Pinxit/src/Pinxit.UI/Pinxit.UI.csproj'
    Exe       = 'Pinxit.exe'
    TagPrefix = 'pinxit-v'
    Installer = 'installer/Pinxit.iss'
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
