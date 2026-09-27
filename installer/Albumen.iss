; Albumen: planned app, NOT YET SHIPPING (no code exists). This script is valid
; Inno Setup but refuses to compile unless /DAlbumenShipping is passed, so no
; release can ship an empty Albumen by accident. Remove the guard (and set
; Shipping = $true in scripts/apps.psd1) once Albumen has a publishable project.
#ifndef AlbumenShipping
  #error Albumen is not shipping yet. Pass /DAlbumenShipping once src/Albumen has a publishable app.
#endif

#define AppName "Albumen"
#define AppExeName "Albumen.exe"
#define AppIdGuid "EC44C380-F350-4C37-8CEC-1C2472CD25DA"
#define AppIcon AddBackslash(SourcePath) + "..\resources\icons\albumen\albumen.ico"

#include "common.iss"
