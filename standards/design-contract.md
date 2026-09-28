# Design Contract

Binding for every user-facing surface of Stilus, Gesso, Albumen, and `Isotone.UI`. It turns the Isotone Interface design system in [`docs/design/`](../docs/design/README.md) into a contract a section can be built, reviewed, and gated against: what "faithful to the design" means, how it is measured, how it is enforced, and what a deviation costs. [`ui.md`](ui.md) summarizes the design; this file says how the code is held to it. Where the two disagree, `docs/design/` wins, then this file, then `ui.md`, and the loser is corrected in the same commit.

Operator decisions of 2026-09-27 behind it: pixel perfect means "Exact tokens + ±1 DIP geometry + approved goldens"; legacy code is handled by "Record existing violations, fail new ones"; golden sign-off is "Review panel only", with no operator step.

## 1. Design first

- `docs/design/` is the source. `tokens.json` holds every value, `components/<Comp>/README.md` and its `preview.html` specify each control, `shell-layout.md` specifies the window anatomy and its regions, and `app-icons.md` the app icons. The WPF code implements them 1:1.
- A change to how something looks goes to `docs/design/` first, in its own commit or at the head of the section's range, with the design page regenerated (`python scripts/build-design-site.py`, `docs/design/EDITING.md`). Code then follows the new spec. Code never leads the design, and a surface is never "tuned" in XAML to a value the spec does not name.
- A surface that has no spec yet gets one before it is built: the section names it as `new surface: docs/design/<path>.md` on its `**Design:**` line and carries the checklist item that adds that README (and its preview card) to `docs/design/` before any XAML is written. A spec two apps need is one shared spec with no app prefix (for example `CurveEditor`, `GradientEditor`, `AssistantPanel`); the earliest section writes it and later sections extend it.
- The captures of the imported apps under `docs/captures/<app>/` (`D00 T03 §2`) are a "before" record of the legacy surfaces. They are never a fidelity source: a surface is compared with the design, not with what Bezier or the old Gesso looked like.

## 2. What fidelity means

A surface is faithful when all of these hold, in every theme and density its spec covers:

- **Exact tokens.** Every color, size, radius, spacing, font family, type style, shadow, duration, easing, and icon comes from `tokens.json` or the icon catalog through the generated `Isotone.UI` dictionaries, by its token key. Colors are consumed through `DynamicResource`; sizes may use `StaticResource`. No literal color, size, radius, spacing, font, or duration appears in a surface where a token names the value, and a resolved value equals the token's value for that theme exactly.
- **Geometry within 1 DIP.** Every measured position and size (control heights, paddings, gaps, radii, icon boxes, hairlines, focus ring offsets) is within ±1 device-independent pixel of the spec at 100, 150, and 200 percent display scaling. Hairlines stay one device pixel (`SnapsToDevicePixels`, `UseLayoutRounding`).
- **Every state.** Every state the component spec lists (rest, hover, pressed, keyboard focus, disabled, checked, indeterminate, error, open, selected, inactive, and the rest) is implemented and drawn as specified. A state the spec lists and the template lacks is a missing feature, not a detail.
- **Every theme and density.** Darkest, Dark, Medium Gray, and Light; the Blue and Isotone orange Highlight colors plus the Windows accent option; Compact and Comfortable. High contrast follows the mapping table in `docs/design/README.md`.
- **Type as specified.** Text uses the spec's type style (`caption`, `body`, `body-strong`, `section-header`, `title`, `dialog-title`, `display`, `mono`, `mono-body`), including weight, line height, capitals, and the density swap.
- **Approved goldens match.** The surface's renders match its approved golden PNGs (section 3) within the stated tolerance.

## 3. Goldens

- A golden is an approved PNG of one control or surface in one state, theme, Highlight, and density at one scale, committed under `docs/captures/golden/<area>/<Comp>/<state>-<theme>-<density>-<highlight>@<scale>.png` (for example `isotone-ui/Button/hover-dark-compact-blue@1.5x.png`), where `<area>` is `isotone-ui`, `stilus`, `gesso`, or `albumen` and `<Comp>` is the component folder name under `docs/design/components/` (or the shell-layout region for a whole surface). Beside them, `card-<theme>-<density>@1x.png` lays every state out in the order of the component's preview card, so review can set it beside the design reference render.
- The first WPF render of a control or surface is produced by the visual test harness (`tests/Isotone.UI.VisualTests`, `D01 T01 §9`) into `build/wpf-renders/`. The review panel compares it with the design reference render of the same spec (`python scripts/render-design-reference.py`, which writes `build/design-reference/<Comp>/<theme>-<density>.png` and the side-by-side `build/design-reference/report.html`) under the checks of section 2.
- Only `review-todo-section` approves a golden, after the `design-fidelity` lens passes: it runs the harness's `--approve` path, which copies the reviewed renders into `docs/captures/golden/`, and records the approval in the stamp's `Design:` verification line. `process-todo-section` never approves a golden, and no other path writes that folder.
- Once approved, CI pixel-diffs every render against its golden with a small anti-alias tolerance: a per-channel difference of at most 2 of 255 counts as equal, and at most 0.1 percent of the pixels (never more than 16) may differ beyond it. The harness states both numbers in one place and prints the differing count and the largest difference on a failure.
- Updating a golden needs a design change first (the spec or a token changed, and the golden follows it in the same range) or a review-approved reason recorded in the stamp. A golden is never re-approved to make a failing diff pass.

## 4. Deviations

- There is no deviation from the design without a line in the section, directly under its `**Design:**` line:
- `**Design deviation:** opened YYYY-MM-DD -- spec: <design ref, e.g. docs/design/components/Button/README.md#states> -- reason: <why the code cannot match now> -- follow-up: DNN TNN §N (fix design|fix code)`
- The follow-up section either changes the design (the spec was wrong or impractical) or fixes the code; it names the deviation in its own checklist. A deviation is open until the follow-up's row is `[x]`.
- `python scripts/todo-graph.py validate` parses every deviation: a malformed line, a dead spec ref, or a follow-up that names no section is FATAL, and `python scripts/todo-graph.py query design` counts them, open and closed.
- A deviation must be closed before its app's release: an open deviation in a Stilus, Gesso, or Albumen file (an `Isotone.UI` deviation counts for all three) while that app's release section (the one that pushes its tag) is stamped on or after the day the deviation opened is FATAL (`design-deviation-open-at-release`). `review-todo-section` refuses a stamp while the section's own deviations are unexplained.

## 5. Enforcement

| Gate | What it enforces | Where it runs |
| --- | --- | --- |
| `**Design:**` line | Every section whose Fidelity line names a surface carries one; its refs resolve to files and GitHub-style heading anchors under `docs/design/` or `standards/ui.md` (`design-missing`, `design-malformed`, `design-dead-ref`). The gaps of 2026-09-27 are listed in `todo/.design-baseline`, which only shrinks (`design-baseline-stale`, `design-baseline-grown`). | `python scripts/todo-graph.py validate`: the commit hook, `scripts/check-all.ps1`, the `plan-gates` workflow |
| design-lint | No literal color or size, no `StaticResource` color, no non-token color key, no literal font family, no WPF-UI or FluentIcons, no emoji glyph, no system backdrop in the UI sources (`scripts/design-lint.py`, rules in its docstring). The violations of 2026-09-27 are recorded in `docs/design/.lint-baseline.json`: they pass, new ones fail, and a fixed one fails as stale until the baseline shrinks. | The commit hook (staged tree), `scripts/check-all.ps1`, the `build` workflow |
| Token drift | The `Isotone.UI` theme dictionaries equal what `tokens.json` generates (`python scripts/generate-theme.py --check`, `D01 T01 §3`); the design page equals its sources (`python scripts/build-design-site.py --check`). | `scripts/check-all.ps1`, CI |
| Visual regression | Every control and chrome surface renders within tolerance of its approved goldens in every state, theme, Highlight, density, and scale it has goldens for (`tests/Isotone.UI.VisualTests`, `D01 T01 §9`). | `dotnet test Isotone.slnx`, CI |
| Review lens | `design-fidelity` in `review-todo-section`: tokens exact, geometry within 1 DIP measured from the renders, every spec state and theme present, the WPF render compared side by side with the design reference render, goldens approved only after it passes. | Every surface section's review |

Adding to either baseline is not a way to pass: `todo/.design-baseline` refuses any ref HEAD does not list, and `docs/design/.lint-baseline.json` grows only through `--update-baseline --allow-add --reason "<text>"`, whose reason must be one the review approved and quoted in the stamp.

## 6. Definition of done for a UI section

A section that builds or changes a surface is done only when:

1. Its `**Design:**` line names every spec it implements and validates; it is out of `todo/.design-baseline`.
2. Any spec it needed was added to `docs/design/` first, with the design page regenerated.
3. It uses token keys only (colors through `DynamicResource`); `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` reports 0 new violations, and every violation it removed left the baseline in the same range.
4. Every state, theme, Highlight, and density the spec lists is implemented, and the visual harness renders each of them into `build/wpf-renders/`.
5. The review's `design-fidelity` lens passed against the design reference renders, the goldens it approved are committed under `docs/captures/golden/`, and the visual tests pass against them.
6. It has no open `**Design deviation:**` without a follow-up section, and none at all if the section is an app release.
7. The user guide under `docs/user/` describes the surface as built, in the same range.
