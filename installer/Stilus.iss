; Stilus: vector editor. Build with: pwsh scripts/package.ps1 -App Stilus
#define AppName "Stilus"
#define AppExeName "Bezier.Desktop.exe"
#define AppIdGuid "5EDC0A18-04A2-47C7-A124-96C9B85CBA2F"
#define AppIcon AddBackslash(SourcePath) + "..\resources\icons\stilus\stilus.ico"

#include "common.iss"

[Tasks]
Name: "assoc_svg"; Description: "Open .svg files with {#AppName}"; GroupDescription: "File associations:"; Flags: unchecked

[Registry]
; ProgID plus an OpenWithProgids entry, only when the user ticks the task.
; HKA follows the per-user or all-users choice made in the privileges dialog.
Root: HKA; Subkey: "Software\Classes\Stilus.svg"; ValueType: string; ValueName: ""; ValueData: "SVG Image"; Flags: uninsdeletekey; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\Stilus.svg\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#AppExeName},0"; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\Stilus.svg\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}"" ""%1"""; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\.svg\OpenWithProgids"; ValueType: string; ValueName: "Stilus.svg"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoc_svg
Root: HKA; Subkey: "Software\Classes\Applications\{#AppExeName}\SupportedTypes"; ValueType: string; ValueName: ".svg"; ValueData: ""; Flags: uninsdeletekey
