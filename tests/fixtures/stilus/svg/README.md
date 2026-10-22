# Stilus SVG fixtures

Two SVG files carried over from the Bezier repository, the origin of Stilus, where they sat beside the projects in `src/Stilus/`. `D00 T03 §1` moved them here so they read as test inputs, not build inputs.

| File | Origin | License |
| ---- | ------ | ------- |
| `test.svg` | Bezier repository, `test.svg` at its root (imported into `src/Stilus/test.svg`) | GPL-3.0, this repository's license (the Bezier repository was the operator's own, under the same license) |
| `bezier-sample.svg` | Bezier repository, `bezier-sample.svg` at its root (imported into `src/Stilus/bezier-sample.svg`); an export from Adobe Illustrator 30.0, per its generator comment, so it exercises a real Illustrator document's markup (a `<style>` block and class-based fills) | GPL-3.0, as above |

A format reader or writer that uses one of these for its round-trip proof says so in its section and records the fixture's expected elements beside it (`standards/testing.md`, Fixtures and fidelity).
