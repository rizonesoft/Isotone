---
trigger: always_on
---
# Design Contract Rule

## Contract
- Authoritative UI contract: `standards/design-contract.md`, `standards/ui.md`, and `docs/design/README.md` (`docs/design/EDITING.md` governs changes).

## Tokens and icons
- Token source: `docs/design/tokens.json` (generated via `scripts/generate-ui-tokens.py` into `native/ui/`).
- App and UI icon sources live in `docs/design/app-icons.md` and `docs/design/components/Icons/README.md` (built via `scripts/build-app-icons.py` and `scripts/export-icons.py`).

## Never
- Never add raw `#RRGGBB` or `0xRRGGBB`, hardcoded `rgb()` or `ColorF`, or literal spacing, radius, or font size where a token in `docs/design/tokens.json` exists.
- Never add an inline unmanaged SVG, an emoji as an icon, or an unapproved backdrop.
- Never bypass `isotone::ui` shared controls or hand-edit generated token tables.

## Static lint
- Run `python scripts/design-lint.py` (`docs/design/.lint-baseline.json`, enforced by `tools/githooks/pre-commit`).

## Rendered check
- No built-app offscreen render command is active yet (`scripts/render-design-reference.py` renders reference previews); each surface section must build or name its own rendered check.
- Planned built-app WARP offscreen renderer and gate: `D01 T25 §1` and `D01 T25 §2` in `todo/01-core/TODO-25-foundation-goldens.md`.
