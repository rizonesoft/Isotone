# Captures

Captures of the apps' rendered surfaces. Two kinds live here, and they are never confused:

- **Before records** (`stilus/`, `gesso/`): how the imported apps looked before `isotone::ui` and the design system replaced their surfaces. A reviewer uses them to see what a section changed. They are never a fidelity source: no section is built or reviewed to match them.
- **Goldens** (`golden/`): the review-approved renders of every control and surface, per state, theme, Highlight, density, and scale, which `standards/design-contract.md` makes the regression reference. Only `review-todo-section` writes them, through the visual harness's approve path. The design in `docs/design/` is the fidelity source both answer to.

The apps the before records show were removed from `main` by `D00 T06 §3`, when the suite went native, and are preserved at the `csharp-final` Git tag, which also holds these captures unchanged. To find the code that drew a surface, list what the tag holds with `git ls-tree -r --name-only csharp-final src/` and read a file with `git show csharp-final:<path>`; each surface folder's `README.md` names the window source for its captures.

## Layout

- One folder per app, then one per surface: `docs/captures/<app>/<surface>/`, for example `stilus/main-window/`.
- File names are `<state>-<scale>.png`: `empty-100.png` is the surface with no document at 100 percent display scaling, `sample-100.png` the same surface with a sample document open, `empty-150.png` the empty surface at 150 percent.
- Each surface folder carries a `README.md` recording the commit the captured app was built from, the capture date, the Windows build, the display scaling, and how the capture was taken.
