## Round 1: none

- Writer: claude
- Run: 2026-10-23T07:35:50Z
- Skipped: sol (exited 1)
- Lines: 1
- Digest: 0555d87060386853

No reviewer returned a review. This round is not an approval.

## Round 2: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T08:04:18Z
- Effort: xhigh
- Lines: 24
- Digest: 966f68c1bbf6a3f3

adversarial: needs-attention

1. P1 `todo/07-tinctura/TODO-01-tinctura-plan.md:54`: §6 depends only on §5, although it requires planning against the shipped 0.1.0. An in-memory probe marking the five planning sections complete made `resolve 'D07 T01 §6'` return 0 with no Tinctura implementation or release present. Capio and Folium have the same dependency. If foundation work parks, the campaign can advance and plan parity against a nonexistent baseline. §5 must wire §6 to the authored 0.1.0 release-candidate checkpoint.

consistency: needs-attention

2. P1 `todo/07-tinctura/TODO-01-tinctura-plan.md:78`: §2 requires a registered catalog with valid statuses and passing `validate`, but its implementation owners are authored only in §5 and §6. A representative `plan D07 T02 §1` produces `parity-ref-dead`; the grammar has no pending-owner status. Routing in-scope features to exclusions, backlog, or planning sections would misrepresent their ownership. Capio §2 and Folium §2 repeat this sequencing contradiction.
3. P2 `docs/design/app-icons.md:46`: The ladder renders 40 px from the simplified 32 px variant, which removes Gesso’s stroke. The recorded decision removes the stroke only below 40 px. Following the ladder therefore produces the wrong glyph at exactly 40 px, including the planned ICO frame, while the checks pass.

integration: needs-attention

4. P2 `scripts/check-all.ps1:101`: The new mandatory gate imports `resvg_py` and Pillow, but neither provisioning nor a committed requirements file supplies them. Their installation remains future work in `D00 T03 §3`. A fresh Python environment fails immediately with `ModuleNotFoundError: No module named 'resvg_py'`, so the documented toolchain cannot run the newly added gate.
5. P2 `scripts/generate-small-icons.py:68`: This generator now processes only Isotone, while `todo/00-workspace/TODO-03-repo-layout.md:141` still requires its future `--check` to protect the app variants against master changes. Its retained app extractors also fail against the Solid masters: calling `small('stilus', 16)` or `small('gesso', 16)` raises `AttributeError`; Albumen raises `ValueError`. The raster-export section must be rewired to the new app generator.

source-defect: needs-attention

6. P2 `scripts/build-app-icons.py:190`: `re.subn(..., count=1)` prevents the subsequent count check from detecting duplicate nested icons. In an in-memory probe, inserting the pre-Solid Gesso nested SVG immediately after the current nested SVG left the old icon overlaid on the new one, yet `--check` returned 0 with `app icons: 0 stale`. Require exactly one matching nested icon before replacement.

record: needs-attention

7. P2 `todo/supersession-2026-10.md:708`: The Phase column retains 63 old assignments after the renumbering. For example, `D02 T17 §11` at line 711 has Phase 41 beside a title saying Phase 47, and `D05 T01 §7` at line 770 still says Phase 45 instead of 51. Comparing the map with the candidate’s implementation-plan tables reproduces all 63 mismatches.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 1

Round 1 first returned no review (the reviewer was at capacity, recorded above as `none`); its retry after the 15-minute backoff is the round. Every finding was verified against the tree and is real.

1. P1, each new app's §6 could run before its 0.1.0 shipped: verified. §5 now adds the authored `<app>-v0.1.0` release section to §6's Depends On, with `resolve` exiting 4 naming it as its proof.
2. P1, the catalogs could not honestly be registered before their owners exist: verified. The parity grammar gains `to-author <DNN TNN §N>` (a planned app's feature whose owner a named planning section authors) and the FATAL `parity-to-author-stale` (the ref names a missing, moved, or stamped section), with `excluded: scope` for an operator's fence and the three planned apps in `other-app`; every catalog's Totals carries the new kind. §2 writes `to-author §6`, §3 moves Phase A rows to `to-author §5`, and §5 and §6 reroute them to `plan`. Self-test cases cover an open, a missing, a stamped, and a moved ref, and a mutant without the stamped case fails.
3. P2, 40 px rendered the simplified glyph: verified. 40 px now takes the master in the spec, the component page, the resources README, and the raster export's size table, so only sizes below 40 px drop the Gesso stroke.
4. P2, the new gate's packages were not provisioned: verified. `scripts/requirements-icons.txt` pins `resvg-py`, `Pillow`, and `fonttools`, and `tools/provision.ps1` gains a `pydeps` leg that verifies the pins and installs them on repair (a wrong pin reads FAULT, restored reads OK); the raster export section keeps the file.
5. P2, `generate-small-icons.py` kept dead app extractors and its planned `--check` still claimed the app variants: verified. It now writes only the suite icon, and `D00 T03 §3` scopes its `--check` to the suite icon beside `build-app-icons.py --check`, which guards every app icon.
6. P2, a duplicated nested icon passed the splash check: verified. The splash must hold exactly one nested master, counted before replacement; a probe with a duplicate now fails naming the count.
7. P2, the supersession map kept 63 old phase numbers: verified. All 63 rows moved by six; a cross-check of every map row against the plan's tables reports no mismatch.
