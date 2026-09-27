; Isotone Graphics Suite: shared Inno Setup definitions (Inno Setup 7.1 or newer).
;
; Each app script (Stilus.iss, Pinxit.iss, Albumen.iss) defines the app identity,
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
; Rizonesoft is a brand of Rizonetech (Pty) Ltd, the copyright holder. The publisher
; users see stays Rizonesoft. PublisherUrl is the one product page value (the per-app
; pages on rizonesoft.com are not decided yet); package.ps1 or CI may pass /DPublisherUrl=...
#define Publisher "Rizonesoft"
#ifndef PublisherUrl
  #define PublisherUrl "https://www.rizonesoft.com/"
#endif
#define Company "Rizonetech (Pty) Ltd"
#define Copyright "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd"
#define RepoUrl "https://github.com/rizonesoft/Isotone"

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
; Binaries are distributed only from rizonesoft.com (download.rizonesoft.com), never
; from GitHub releases, so updates point at the product page.
AppUpdatesURL={#PublisherUrl}
AppVersion={#AppVersion}
VersionInfoVersion={#AppFileVersion}
VersionInfoCompany={#Company}
AppCopyright={#Copyright}
VersionInfoCopyright={#Copyright}
; Per-user by default; the dialog offers an all-users install.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; 64-bit only: a 64-bit Setup (Inno 7 SetupArchitecture) installing in 64-bit mode.
; The .NET runtime ships inside the app (self-contained): no prerequisites.
SetupArchitecture=x64
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; Supported: Windows 11. Windows 10 (1809 or later) may install and run but is
; unsupported by .NET 11; the wizard says so on build < 22000 (see [Code]).
MinVersion=10.0.17763
; Inno 7: follow the system light or dark theme.
WizardStyle=modern dynamic
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

[Code]
// Windows 10 is not on the .NET 11 supported-OS list (only Windows 11 and the
// Windows 10 LTSC/IoT editions are), so on build < 22000 the wizard shows one
// non-blocking notice page. Silent installs (/SILENT, /VERYSILENT) never show
// wizard pages, so they skip it. Event attributes keep this composable with any
// InitializeWizard or ShouldSkipPage an including script adds.
var
  IsotoneWin10Page: TOutputMsgWizardPage;

function IsotoneIsWindows10: Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := (Version.Major = 10) and (Version.Build < 22000);
end;

<event('InitializeWizard')>
procedure IsotoneInitializeWizard;
begin
  IsotoneWin10Page := CreateOutputMsgPage(wpWelcome,
    'Windows 10 is not officially supported',
    '{#AppName} is built for Windows 11.',
    'Windows 10 is not officially supported by .NET 11, which {#AppName} is built on. ' +
    '{#AppName} may work, but it is untested on Windows 10.' + #13#10#13#10 +
    'Click Next to continue anyway, or Cancel to exit Setup.');
end;

<event('ShouldSkipPage')>
function IsotoneShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := (IsotoneWin10Page <> nil) and (PageID = IsotoneWin10Page.ID) and not IsotoneIsWindows10;
end;
