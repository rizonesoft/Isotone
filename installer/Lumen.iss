; Lumen: planned app, NOT YET SHIPPING (no code exists). This script is valid
; Inno Setup but refuses to compile unless /DLumenShipping is passed, so no
; release can ship an empty Lumen by accident. Remove the guard (and set
; Shipping = $true in scripts/apps.psd1) once Lumen has a publishable project.
#ifndef LumenShipping
  #error Lumen is not shipping yet. Pass /DLumenShipping once src/Lumen has a publishable app.
#endif

#define AppName "Lumen"
#define AppExeName "Lumen.exe"
#define AppIdGuid "EC44C380-F350-4C37-8CEC-1C2472CD25DA"
#define AppIcon AddBackslash(SourcePath) + "..\resources\icons\lumen\lumen.ico"

#include "common.iss"
