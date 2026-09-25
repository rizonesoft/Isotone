; Imago: raster editor. Build with: pwsh scripts/package.ps1 -App Imago
#define AppName "Imago"
#define AppExeName "Imago.exe"
#define AppIdGuid "E356E958-05F9-4F97-8537-77FA5B529BF4"
; PLACEHOLDER: Imago has no .ico yet (src/Imago/src/Imago.UI/Assets/imago-icon.png
; is an empty file). common.iss falls back to the default Setup icon until it exists.
#define AppIcon AddBackslash(SourcePath) + "..\resources\icons\imago\imago.ico"

#include "common.iss"

[Tasks]
Name: "assoc_png"; Description: "Open .png files with {#AppName}"; GroupDescription: "File associations:"; Flags: unchecked
Name: "assoc_jpg"; Description: "Open .jpg and .jpeg files with {#AppName}"; GroupDescription: "File associations:"; Flags: unchecked
Name: "assoc_psd"; Description: "Open .psd files with {#AppName}"; GroupDescription: "File associations:"; Flags: unchecked

[Registry]
; One ProgID per format; entries are written only for ticked tasks.
Root: HKA; Subkey: "Software\Classes\Imago.png"; ValueType: string; ValueName: ""; ValueData: "PNG Image"; Flags: uninsdeletekey; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\Imago.png\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#AppExeName},0"; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\Imago.png\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}"" ""%1"""; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\.png\OpenWithProgids"; ValueType: string; ValueName: "Imago.png"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_png

Root: HKA; Subkey: "Software\Classes\Imago.jpg"; ValueType: string; ValueName: ""; ValueData: "JPEG Image"; Flags: uninsdeletekey; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\Imago.jpg\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#AppExeName},0"; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\Imago.jpg\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}"" ""%1"""; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\.jpg\OpenWithProgids"; ValueType: string; ValueName: "Imago.jpg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\.jpeg\OpenWithProgids"; ValueType: string; ValueName: "Imago.jpg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_jpg

Root: HKA; Subkey: "Software\Classes\Imago.psd"; ValueType: string; ValueName: ""; ValueData: "Photoshop Document"; Flags: uninsdeletekey; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\Imago.psd\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#AppExeName},0"; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\Imago.psd\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}"" ""%1"""; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\.psd\OpenWithProgids"; ValueType: string; ValueName: "Imago.psd"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_psd

Root: HKA; Subkey: "Software\Classes\Applications\{#AppExeName}\SupportedTypes"; ValueType: string; ValueName: ".png"; ValueData: ""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\Applications\{#AppExeName}\SupportedTypes"; ValueType: string; ValueName: ".jpg"; ValueData: ""
Root: HKA; Subkey: "Software\Classes\Applications\{#AppExeName}\SupportedTypes"; ValueType: string; ValueName: ".jpeg"; ValueData: ""
Root: HKA; Subkey: "Software\Classes\Applications\{#AppExeName}\SupportedTypes"; ValueType: string; ValueName: ".psd"; ValueData: ""
