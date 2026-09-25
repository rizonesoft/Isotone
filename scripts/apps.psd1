# Suite app manifest: the one place scripts/*.ps1 and CI learn about each app.
# Shipping = $false means the app has no code yet; publish and package refuse it.
@{
  Nodus = @{
    Project   = 'src/Nodus/Bezier.Desktop/Bezier.Desktop.csproj'
    Exe       = 'Bezier.Desktop.exe'
    TagPrefix = 'nodus-v'
    Installer = 'installer/Nodus.iss'
    Shipping  = $true
  }
  Imago = @{
    Project   = 'src/Imago/src/Imago.UI/Imago.UI.csproj'
    Exe       = 'Imago.exe'
    TagPrefix = 'imago-v'
    Installer = 'installer/Imago.iss'
    Shipping  = $true
  }
  Lumen = @{
    Project   = 'src/Lumen/Lumen.UI/Lumen.UI.csproj'
    Exe       = 'Lumen.exe'
    TagPrefix = 'lumen-v'
    Installer = 'installer/Lumen.iss'
    Shipping  = $false
  }
}
