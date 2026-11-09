# Suite app manifest: the one place scripts/*.ps1 and CI learn about each app.
# Shipping = $false means the app has no native shipping binary yet; D00 T07 §5 re-plans release packaging.
@{
  Stilus = @{
    Name      = 'Stilus'
    Slug      = 'stilus'
    Exe       = 'Stilus.exe'
    TagPrefix = 'stilus-v'
    Installer = 'installer/Stilus.iss'
    Shipping  = $false
  }
  Gesso = @{
    Name      = 'Gesso'
    Slug      = 'gesso'
    Exe       = 'Gesso.exe'
    TagPrefix = 'gesso-v'
    Installer = 'installer/Gesso.iss'
    Shipping  = $false
  }
  Albumen = @{
    Name      = 'Albumen'
    Slug      = 'albumen'
    Exe       = 'Albumen.exe'
    TagPrefix = 'albumen-v'
    Installer = 'installer/Albumen.iss'
    Shipping  = $false
  }
}
