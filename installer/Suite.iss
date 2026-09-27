; Isotone Graphics Suite: one installer, one component per shipping app.
; Build with: pwsh scripts/package.ps1 -Suite
; Each app installs into its own folder under the suite directory. The suite has
; its own AppId and ProgIDs and never shares folders with the standalone installers.
#define SuiteInstaller
#define AppName "Isotone Graphics Suite"
#define AppIdGuid "92E725F7-EB5D-430E-A701-49D9E896E11C"

#include "common.iss"

#ifndef PublishRoot
  #define PublishRoot RepoRoot + "\artifacts\publish"
#endif
#define StilusDir PublishRoot + "\Stilus\" + Runtime
#define PinxitDir PublishRoot + "\Pinxit\" + Runtime
#define AlbumenDir PublishRoot + "\Albumen\" + Runtime
#define StilusExe "Bezier.Desktop.exe"
#define PinxitExe "Pinxit.exe"
#define AlbumenExe "Albumen.exe"
#if !FileExists(StilusDir + "\" + StilusExe)
  #error Stilus is not published. Run: pwsh scripts/publish.ps1 -App Stilus
#endif
#if !FileExists(PinxitDir + "\" + PinxitExe)
  #error Pinxit is not published. Run: pwsh scripts/publish.ps1 -App Pinxit
#endif

[Setup]
AppId={{{#AppIdGuid}}
AppName={#AppName}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf}\Isotone Graphics Suite
DefaultGroupName=Isotone Graphics Suite
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\Stilus\{#StilusExe}
VersionInfoDescription={#AppName} Setup
VersionInfoProductName={#AppName}
VersionInfoProductVersion={#AppFileVersion}
OutputBaseFilename=Isotone-{#AppVersion}-{#Runtime}-Setup
ChangesAssociations=yes
#if FileExists(RepoRoot + "\resources\icons\stilus\stilus.ico")
SetupIconFile={#RepoRoot}\resources\icons\stilus\stilus.ico
#endif

[Types]
Name: "full"; Description: "Full installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "stilus"; Description: "Stilus (vector editor)"; Types: full custom
Name: "pinxit"; Description: "Pinxit (raster editor)"; Types: full custom
#ifdef AlbumenShipping
Name: "albumen"; Description: "Albumen"; Types: full custom
#endif

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "assoc_svg"; Description: "Open .svg files with Stilus"; GroupDescription: "File associations:"; Components: stilus; Flags: unchecked
Name: "assoc_png"; Description: "Open .png files with Pinxit"; GroupDescription: "File associations:"; Components: pinxit; Flags: unchecked
Name: "assoc_jpg"; Description: "Open .jpg and .jpeg files with Pinxit"; GroupDescription: "File associations:"; Components: pinxit; Flags: unchecked
Name: "assoc_psd"; Description: "Open .psd files with Pinxit"; GroupDescription: "File associations:"; Components: pinxit; Flags: unchecked

[Files]
Source: "{#StilusDir}\*"; DestDir: "{app}\Stilus"; Components: stilus; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#PinxitDir}\*"; DestDir: "{app}\Pinxit"; Components: pinxit; Flags: ignoreversion recursesubdirs createallsubdirs
#ifdef AlbumenShipping
Source: "{#AlbumenDir}\*"; DestDir: "{app}\Albumen"; Components: albumen; Flags: ignoreversion recursesubdirs createallsubdirs
#endif

[Icons]
Name: "{group}\Stilus"; Filename: "{app}\Stilus\{#StilusExe}"; Components: stilus
Name: "{group}\Pinxit"; Filename: "{app}\Pinxit\{#PinxitExe}"; Components: pinxit
#ifdef AlbumenShipping
Name: "{group}\Albumen"; Filename: "{app}\Albumen\{#AlbumenExe}"; Components: albumen
#endif
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Stilus"; Filename: "{app}\Stilus\{#StilusExe}"; Components: stilus; Tasks: desktopicon
Name: "{autodesktop}\Pinxit"; Filename: "{app}\Pinxit\{#PinxitExe}"; Components: pinxit; Tasks: desktopicon

[Registry]
; Suite-specific ProgIDs (IsotoneSuite.*) never collide with the standalone installers.
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Stilus.svg"; ValueType: string; ValueName: ""; ValueData: "SVG Image"; Flags: uninsdeletekey; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Stilus.svg\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Stilus\{#StilusExe},0"; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Stilus.svg\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Stilus\{#StilusExe}"" ""%1"""; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\.svg\OpenWithProgids"; ValueType: string; ValueName: "IsotoneSuite.Stilus.svg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_svg

Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.png"; ValueType: string; ValueName: ""; ValueData: "PNG Image"; Flags: uninsdeletekey; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.png\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Pinxit\{#PinxitExe},0"; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.png\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Pinxit\{#PinxitExe}"" ""%1"""; Tasks: assoc_png
Root: HKA; Subkey: "Software\Classes\.png\OpenWithProgids"; ValueType: string; ValueName: "IsotoneSuite.Pinxit.png"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_png

Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.jpg"; ValueType: string; ValueName: ""; ValueData: "JPEG Image"; Flags: uninsdeletekey; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.jpg\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Pinxit\{#PinxitExe},0"; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.jpg\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Pinxit\{#PinxitExe}"" ""%1"""; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\.jpg\OpenWithProgids"; ValueType: string; ValueName: "IsotoneSuite.Pinxit.jpg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_jpg
Root: HKA; Subkey: "Software\Classes\.jpeg\OpenWithProgids"; ValueType: string; ValueName: "IsotoneSuite.Pinxit.jpg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_jpg

Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.psd"; ValueType: string; ValueName: ""; ValueData: "Photoshop Document"; Flags: uninsdeletekey; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.psd\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Pinxit\{#PinxitExe},0"; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\IsotoneSuite.Pinxit.psd\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Pinxit\{#PinxitExe}"" ""%1"""; Tasks: assoc_psd
Root: HKA; Subkey: "Software\Classes\.psd\OpenWithProgids"; ValueType: string; ValueName: "IsotoneSuite.Pinxit.psd"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_psd

[Run]
Filename: "{app}\Stilus\{#StilusExe}"; Description: "{cm:LaunchProgram,Stilus}"; Components: stilus; Flags: nowait postinstall skipifsilent unchecked
Filename: "{app}\Pinxit\{#PinxitExe}"; Description: "{cm:LaunchProgram,Pinxit}"; Components: pinxit; Flags: nowait postinstall skipifsilent unchecked
