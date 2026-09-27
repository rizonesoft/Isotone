# Viewing the previews locally

Each `components/<Comp>/preview.html` is a fragment the artifact page renders as a card. The page injects three things the file does not load itself: `tokens.css` (every token in `tokens.json` as a CSS custom property, one block per brightness theme selected by `data-theme`), `components/bundle.css` (the shared component and `.pv` preview styles), and `components/bundle.js` (`window.Photon`, the icon catalog and the scrub helper).

Opened straight from disk, a preview therefore shows unstyled markup. To see the previews as designed, open `docs/design/index.html` (straight from disk works: it fetches nothing) or its published copy at https://rizonesoft.github.io/Photon/design/, which render every card with the Theme, Highlight and Density switches; the artifact page (https://claude.ai/artifact/2oBf2CQ5mQoLfMb6g1XwD6) renders the same cards.

`scripts/build-design-site.py` generates `index.html`, including a `tokens.css` with the artifact page's naming (the first theme on `:root, [data-theme="dark"]`, one `[data-theme="<id>"]` block per further theme, `--font-<family>`, and one class per type style), which it inlines into each preview frame with `bundle.css` and `bundle.js`. The page is committed and `--check` fails when it drifts from its sources; `tokens.css` itself is never stored as a file (see `SYNC.md`).

The `AppIcon` preview references the app icons as `/_blob/<id>` asset URLs, which resolve only on the artifact page; the generator maps each id through `design-system.json` to the same file in `resources/icons/<app>/` and inlines it.
