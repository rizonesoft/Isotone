# Reference Machine

Every performance goal in [`docs/specs/2026-10-22-native-stack-design.md`](../specs/2026-10-22-native-stack-design.md) ("Goals and how each is measured", "The reference environment") and every optimization record in [`docs/benchmarks/`](../benchmarks/README.md) (`standards/cpp.md`, "SIMD and performance", `D00 T04 §2`) is measured on the recorded reference machine below.

**Update rule:** Any change to the CPU, GPU, GPU driver version, RAM, storage, Windows build, display resolution, display scaling, display refresh rate, or power plan is recorded as a new dated heading (`## YYYY-MM-DD`) added above the previous entries. Existing entries are never edited in place, and every benchmark record in `docs/benchmarks/` cites the exact dated entry under which its measurements were taken.

## 2026-11-09

| Field | Value |
| ----- | ----- |
| **CPU** | `11th Gen Intel(R) Core(TM) i5-11600K @ 3.90GHz` (6 physical cores, 12 logical processors, 3,912 MHz base clock; L1d 6 x 48 KiB, L2 6 x 512 KiB = 3,072 KiB, L3 12,288 KiB; instruction sets: SSE2, SSE4.1, SSE4.2, AVX, AVX2, FMA, AVX-512) |
| **GPU** | `NVIDIA GeForce RTX 2060` (6 GiB GDDR6; WMI `AdapterRAM` 4,293,918,720 bytes) |
| **GPU driver version** | `32.0.16.1088` |
| **RAM** | `32 GiB` (`34,185,392,128` bytes: 4 x 8 GiB Corsair `CMG16GX4M2D3600C18` DDR4 configured at 2,133 MT/s) |
| **Storage** | `C:` (system and toolchain): `Corsair MP600 PRO XT` 1 TB NVMe SSD (`1,000,204,886,016` bytes, 930.4 GiB NTFS); `D:` (workspace `D:\GitHub\Isotone`): `Msft Virtual Disk` 1 TiB File-Backed Virtual SSD (`1,099,511,627,776` bytes, 1,024.0 GiB NTFS); `R:` (scratch): `Micron MTFDKCD512QFM-1BD1AABLA` 512 GB NVMe SSD (`512,110,190,592` bytes, 474.7 GiB NTFS) |
| **Windows build** | `Microsoft Windows 11 Business` 26H2, version `10.0.26300`, build `26300.9818` |
| **Display resolution** | `3840 x 2160` physical pixels (`2560 x 1440` logical DIPs) |
| **Display scaling** | `150%` (`144 DPI`) |
| **Display refresh rate** | `59 Hz` |
| **Power plan** | `Balanced` (`381b4222-f694-41f0-9685-ff5bb260df2e`) |
