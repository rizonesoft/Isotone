; Photon Graphics Suite: shared Inno Setup definitions.
;
; Each app script (Nodus.iss, Imago.iss, Lumen.iss) defines the app identity,
; then includes this file. scripts/package.ps1 passes the build inputs:
;   /DAppVersion=1.2.3[-pre]     SemVer shown to users (default 0.0.0-dev)
;   /DAppFileVersion=1.2.3.45    four-part Win32 version (default 0.0.0.0)
;   /DSourceDir=<publish dir>    self-contained publish output for the app
;   /DOutputDir=<dist dir>       where the Setup.exe is written
;
; Required defines from the including script:
;   AppName, AppExeName, AppIdGuid (no braces), AppIcon (path, may be absent)
; Optional: AppDescription, AppSourceDir (default artifacts\publish\<AppName>\win-x64)

#define RepoRoot AddBackslash(SourcePath) + ".."
#define Publisher "Rizonesoft"
#define PublisherUrl "https://www.rizonesoft.com"
#define RepoUrl "https://github.com/rizonesoft/Photon"

#ifndef AppVersion
  #define AppVersion "0.0.0-dev"
#endif
#ifndef AppFileVersion
  #define AppFileVersion "0.0.0.0"
#endif
#ifndef OutputDir
  #define OutputDir RepoRoot + "\artifacts\dist"
#endif
#ifndef Runtime
  #define Runtime "win-x64"
#endif

[Setup]
AppPublisher={#Publisher}
AppPublisherURL={#PublisherUrl}
AppSupportURL={#RepoUrl}/issues
AppUpdatesURL={#RepoUrl}/releases
AppVersion={#AppVersion}
VersionInfoVersion={#AppFileVersion}
VersionInfoCompany={#Publisher}
VersionInfoCopyright=Copyright (c) Rizonesoft
; Per-user by default; the dialog offers an all-users install.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; 64-bit only. The .NET runtime ships inside the app (self-contained): no prerequisites.
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.17763
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes
OutputDir={#OutputDir}
DisableProgramGroupPage=yes
DisableReadyPage=no
CloseApplications=yes
RestartApplications=no
Uninstallable=yes
UsePreviousAppDir=yes
UsePreviousTasks=yes
ShowLanguageDialog=no
#if FileExists(RepoRoot + "\LICENSE")
LicenseFile={#RepoRoot}\LICENSE
#endif

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

#ifndef SuiteInstaller
; ---------------------------------------------------------------------------
; Single-app installer body. Each app has its own AppId and its own install
; directory; nothing is shared between apps (or with the suite installer).
; ---------------------------------------------------------------------------
#ifndef AppSourceDir
  #define AppSourceDir RepoRoot + "\artifacts\publish\" + AppName + "\" + Runtime
#endif
#if !FileExists(AppSourceDir + "\" + AppExeName)
  #error AppSourceDir has no AppExeName. Run: pwsh scripts/publish.ps1 -App <App>
#endif

[Setup]
AppId={{{#AppIdGuid}}
AppName={#AppName}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
VersionInfoDescription={#AppName} Setup
VersionInfoProductName={#AppName}
VersionInfoProductVersion={#AppFileVersion}
OutputBaseFilename={#AppName}-{#AppVersion}-{#Runtime}-Setup
ChangesAssociations=yes
#if FileExists(AppIcon)
SetupIconFile={#AppIcon}
#else
  #pragma message "WARNING: icon " + AppIcon + " not found; using the Inno Setup default icon."
#endif

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#AppSourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
#endif
