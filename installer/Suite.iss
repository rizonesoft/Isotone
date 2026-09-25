; Rizonesoft Graphics Suite: one installer, one component per shipping app.
; Build with: pwsh scripts/package.ps1 -Suite
; Each app installs into its own folder under the suite directory. The suite has
; its own AppId and ProgIDs and never shares folders with the standalone installers.
#define SuiteInstaller
#define AppName "Rizonesoft Graphics Suite"
#define AppIdGuid "92E725F7-EB5D-430E-A701-49D9E896E11C"

#include "common.iss"

#ifndef PublishRoot
  #define PublishRoot RepoRoot + "\artifacts\publish"
#endif
#define NodusDir PublishRoot + "\Nodus\" + Runtime
#define ImagoDir PublishRoot + "\Imago\" + Runtime
#define LumenDir PublishRoot + "\Lumen\" + Runtime
#define NodusExe "Bezier.Desktop.exe"
#define ImagoExe "Imago.exe"
#define LumenExe "Lumen.exe"
#if !FileExists(NodusDir + "\" + NodusExe)
  #error Nodus is not published. Run: pwsh scripts/publish.ps1 -App Nodus
#endif
#if !FileExists(ImagoDir + "\" + ImagoExe)
  #error Imago is not published. Run: pwsh scripts/publish.ps1 -App Imago
#endif

[Setup]
AppId={{{#AppIdGuid}}
AppName={#AppName}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf}\Rizonesoft Graphics Suite
DefaultGroupName=Rizonesoft Graphics Suite
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\Nodus\{#NodusExe}
VersionInfoDescription={#AppName} Setup
VersionInfoProductName={#AppName}
VersionInfoProductVersion={#AppFileVersion}
OutputBaseFilename=Photon-{#AppVersion}-{#Runtime}-Setup
ChangesAssociations=yes
#if FileExists(RepoRoot + "\resources\icons\nodus\nodus.ico")
SetupIconFile={#RepoRoot}\resources\icons\nodus\nodus.ico
#endif

[Types]
Name: "full"; Description: "Full installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "nodus"; Description: "Nodus (vector editor)"; Types: full custom
Name: "imago"; Description: "Imago (raster editor)"; Types: full custom
#ifdef LumenShipping
Name: "lumen"; Description: "Lumen"; Types: full custom
#endif

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "assoc_svg"; Description: "Open .svg files with Nodus"; GroupDescription: "File associations:"; Components: nodus; Flags: unchecked
Name: "assoc_png"; Description: "Open .png files with Imago"; GroupDescription: "File associations:"; Components: imago; Flags: unchecked
Name: "assoc_jpg"; Description: "Open .jpg and .jpeg files with Imago"; GroupDescription: "File associations:"; Components: imago; Flags: unchecked
Name: "assoc_psd"; Description: "Open .psd files with Imago"; GroupDescription: "File associations:"; Components: imago; Flags: unchecked

[Files]
Source: "{#NodusDir}\*"; DestDir: "{app}\Nodus"; Components: nodus; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#ImagoDir}\*"; DestDir: "{app}\Imago"; Components: imago; Flags: ignoreversion recursesubdirs createallsubdirs
#ifdef LumenShipping
Source: "{#LumenDir}\*"; DestDir: "{app}\Lumen"; Components: lumen; Flags: ignoreversion recursesubdirs createallsubdirs
#endif

[Icons]
Name: "{group}\Nodus"; Filename: "{app}\Nodus\{#NodusExe}"; Components: nodus
Name: "{group}\Imago"; Filename: "{app}\Imago\{#ImagoExe}"; Components: imago
#ifdef LumenShipping
Name: "{group}\Lumen"; Filename: "{app}\Lumen\{#LumenExe}"; Components: lumen
#endif
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Nodus"; Filename: "{app}\Nodus\{#NodusExe}"; Components: nodus; Tasks: desktopicon
Name: "{autodesktop}\Imago"; Filename: "{app}\Imago\{#ImagoExe}"; Components: imago; Tasks: desktopicon

[Registry]
; Suite-specific ProgIDs (PhotonSuite.*) never collide with the standalone installers.
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Nodus.svg"; ValueType: string; ValueName: ""; ValueData: "SVG Image"; Flags: uninsdeletekey; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Nodus.svg\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Nodus\{#NodusExe},0"; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Nodus.svg\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Nodus\{#NodusExe}"" ""%1"""; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\.svg\OpenWithProgids"; ValueType: string; ValueName: "PhotonSuite.Nodus.svg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_svg

Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.png"; ValueType: string; ValueName: ""; ValueData: "PNG Image"; Flags: uninsdeletekey; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.png\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Imago\{#ImagoExe},0"; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.png\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Imago\{#ImagoExe}"" ""%1"""; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\.png\OpenWithProgids"; ValueType: string; ValueName: "PhotonSuite.Imago.png"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_png

Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.jpg"; ValueType: string; ValueName: ""; ValueData: "JPEG Image"; Flags: uninsdeletekey; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.jpg\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Imago\{#ImagoExe},0"; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.jpg\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Imago\{#ImagoExe}"" ""%1"""; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\.jpg\OpenWithProgids"; ValueType: string; ValueName: "PhotonSuite.Imago.jpg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\.jpeg\OpenWithProgids"; ValueType: string; ValueName: "PhotonSuite.Imago.jpg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_jpg

Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.psd"; ValueType: string; ValueName: ""; ValueData: "Photoshop Document"; Flags: uninsdeletekey; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.psd\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Imago\{#ImagoExe},0"; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\PhotonSuite.Imago.psd\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Imago\{#ImagoExe}"" ""%1"""; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\.psd\OpenWithProgids"; ValueType: string; ValueName: "PhotonSuite.Imago.psd"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_psd

[Run]
Filename: "{app}\Nodus\{#NodusExe}"; Description: "{cm:LaunchProgram,Nodus}"; Components: nodus; Flags: nowait postinstall skipifsilent unchecked
Filename: "{app}\Imago\{#ImagoExe}"; Description: "{cm:LaunchProgram,Imago}"; Components: imago; Flags: nowait postinstall skipifsilent unchecked
