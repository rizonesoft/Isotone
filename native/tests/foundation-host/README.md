# The foundation test host

`foundation-host.exe` is the one window every native foundation proves itself in (`D01 T15 §1`). A foundation does not get a sample app of its own: it adds a scenario here, the scenario drives the real `isotone::ui` window, and the run leaves a report a test reads. The host is a development tool: it is never installed with an app.

The window is an `isotone::ui::Window` with a placeholder menu bar (File, Edit, View, Help, two commands each) and two placeholder panels filled with design token colors. The menu is a Win32 menu and the panels are filled with GDI until the renderer and the Isotone title bar replace them (`D01 T15 §2` and `§3`). Each menu command writes one log line and does nothing else.

## Running it

```powershell
foundation-host --scenario <name> --data-root <folder> --report <path>
foundation-host --data-root <folder>
```

| Switch | Meaning |
| --- | --- |
| `--scenario <name>` | The scenario to run. Without it the host is interactive: the window on screen until you close it. |
| `--data-root <folder>` | Required. Where the host keeps its log and settings, under `Rizonesoft\FoundationHost\`, through `isotone::core`. A run never writes your real app-data folder. |
| `--report <path>` | Where the report is written. Without it no report is written. |
| `--fail-window` | Test switch: the window's creation fails as if `CreateWindowExW` had refused. |

| Exit code | Meaning |
| --- | --- |
| 0 | The scenario passed. |
| 1 | The scenario failed, or the host could not start it (a data root it cannot keep its log and settings under, a window that cannot be created); each failure is one sentence on standard error and in the report. |
| 2 | The run could not start or could not report: an unknown switch or scenario, a missing `--data-root`, a report that cannot be written. The sentence on standard error names the problem. |
| 77 | There is no display session (the process's window station is not the visible one), so the scenario could not run. CTest reports the entry as skipped. A window that cannot be created on a working display is exit 1, never 77. |

## The scenarios

| Scenario | What it proves |
| --- | --- |
| `smoke` | The window exists at the size asked for with per-monitor DPI awareness v2; the menu bar holds its four menus and eight commands, and each command, invoked through the window's own message path, writes its log line; both panels, rendered through `WM_PRINTCLIENT`, have their token colors. The window stays hidden. |
| `lifecycle` | The window is shown, paints, is resized and lays its panels out and paints again, is closed, and is destroyed with its message loop ended. It is shown quietly: fully transparent, not activated, with no taskbar button, so nothing appears on the desktop. |

## The report

One JSON object, written atomically through `isotone::core::AtomicFile`:

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | number | `1`. It changes when a field's meaning changes. |
| `scenario` | string | The scenario that ran (`interactive` for a run without one). |
| `result` | string | `pass`, `fail`, or `no-display`. It decides the exit code: 0, 1, or 77. |
| `failures` | array of strings | One sentence for each thing that was wrong. Empty exactly when `result` is `pass`. |
| `measurements` | object | What the scenario measured. Each scenario owns its keys, listed below. |
| `build_id` | string | The build that ran: the commit's first 12 hex digits, with `-dirty` when the tree had changes. |

`smoke` measures `dpi`, `scale_percent`, `dpi_awareness` (`per-monitor-v2`, `per-monitor`, `system`, `unaware`, or `unknown`), `client_width_px`, `client_height_px`, `client_width_dip`, `client_height_dip`, `layouts`, `menus` (an array of `label` and `commands`), and `panels` (for `left` and `right`: the rectangle in pixels, the `expected` token color, and the `painted` color).

`lifecycle` measures `paints`, `layouts`, `resized_client_width_px`, `resized_client_height_px`, `loop_exit_code`, and `destroyed`. It resizes the window smaller, never larger: Windows holds a window to the size of the desktop, and a test desktop can be little larger than the window.

## In CTest

Each entry runs the host through `run_host.cmake`, which checks the exit code, the sentence on the console, and the report field by field against that exit code:

| Entry | Expects |
| --- | --- |
| `foundation.smoke` | Exit 0 and a passing report with the measurements above; a settings file and a log under the data root. |
| `foundation.lifecycle` | Exit 0 and a passing report, or exit 77 with `no-display`. |
| `foundation.unknown-scenario` | Exit 2, the scenario named on the console, no report. |
| `foundation.unwritable-report` | Exit 2 and "the report could not be written". |
| `foundation.missing-data-root` | Exit 2, `--data-root` named, and nothing written. |
| `foundation.unusable-data-root` | Exit 1 and a failing report: a data root the log and settings cannot be kept under is reported like any other failure. |
| `foundation.window-failure` | Exit 1 and a failing report whose failure names `CreateWindowExW`. |

`foundation_host_tests` holds the unit tests of the rules that need no window: which exit code a missing window gets, and how the switches are read.

## Adding a scenario

1. Write `Report run_<name>(Context& context)` in `host.cpp`. Create a `HostWindow`, drive it, put what you measured in `report.measurements`, and call `report.fail("<one sentence>")` for each thing that is wrong. A scenario that needs the window on screen shows it quietly (`HostWindow{context, true, ...}`) and returns `no-display` when `display_session()` is `Absent`.
2. Add it to `kScenarios` (kept in alphabetical order) and to the unknown-scenario sentence.
3. Add its case to `run_host.cmake` with the fields it must report, and its name to the `foreach` in `CMakeLists.txt`, so CTest runs it as `foundation.<name>`.
4. List it in the tables above with its measurements.

A measurement a later section depends on is part of the schema: renaming or removing one raises `schema_version`.
