# Gesso main window, before record

The imported Gesso main window as it looked before `Isotone.UI` and the design system replaced it, captured by `D00 T03 §2`. A before record only: never a fidelity source (`docs/captures/README.md`, `standards/design-contract.md`).

- **Built from:** commit `b7ad3a5` (`dotnet build Isotone.slnx -c Debug`), run as `artifacts/bin/Gesso.UI/debug/Gesso.exe`. The next commit, `f7747ff`, changed documentation only.
- **Captured:** 2026-10-22, Windows 11 Pro build 26300, on a 3840 x 2160 display at 150 percent scaling.
- **Window:** sized to 1600 x 1000 DIPs and captured whole with `PrintWindow` (`PW_RENDERFULLCONTENT`), title bar and frame included.
- **Scaling:** the 150 percent captures are the app as it runs on this display. The display was not switched to 100 percent; instead the 100 percent captures launch the app DPI-unaware (the `DPIUNAWARE` compatibility layer), so WPF lays out and renders at 96 DPI, one pixel per DIP, exactly as on a 100 percent display, and `PrintWindow` returns that render before the desktop compositor scales it. `GetDpiForWindow` reported each window's DPI below.

| File | Pixels | Window DPI | State |
| ---- | ------ | ---------- | ----- |
| `empty-100.png` | 1600 x 1000 | 96 | no document |
| `empty-150.png` | 2400 x 1500 | 144 | no document |
