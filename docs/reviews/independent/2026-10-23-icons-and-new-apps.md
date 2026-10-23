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

## Round 3: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T08:27:07Z
- Effort: xhigh
- Lines: 18
- Digest: 94b1473371d407eb

adversarial: needs-attention

1. P1 `todo/07-tinctura/TODO-01-tinctura-plan.md:137`: The checkpoint falsely claims `validate` refuses parity features deferred without the operator’s words. An in-memory probe routed IP-0001 to a new backlog entry with `why deferred: cheaper to skip it`, updated the totals, and received zero parity or budget findings. The checks establish that the entry exists, not that the operator approved deferral. Capio §6 and Folium §6 repeat this unenforced acceptance claim.

consistency: needs-attention

2. P2 `todo/07-tinctura/TODO-01-tinctura-plan.md:92`: §3 requires two phase-specific `to-author` counts in the Totals table, but its schema permits one aggregate `to-author` row, containing Features and Source rows. Adding a second row produces `parity-totals-drift`; qualifying its label with the authoring reference produces a malformed Totals row. Capio line 92 and Folium line 91 repeat this contradiction. The phase split needs a separately defined representation and check.

integration: needs-attention

3. P1 `scripts/todo-graph.py:6007`: The release and design gates still recognize only the original three apps and the suite. In-memory release sections containing `Push the tag tinctura-v0.1.0`, `capio-v0.1.0`, or `folium-v0.1.0` return no entries from `release_sections()`, bypassing mandatory backlog checks. Their valid `reviewed:` records are also rejected by the tag grammar at line 5150, and domains 07 to 09 are absent from `DESIGN_DOMAIN_APPS`. The new planning sections schedule parity registration but never assign this release-gate integration.

source-defect: approve

record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 2

Every finding was verified and is real; source-defect and record approved.

1. P1, each §6 checkpoint claimed `validate` refuses a deferral without the operator's words: verified, it does not. The checkpoints now name the real guards: the completion review, and the release's backlog review (`release-backlog-unreviewed`), which refuses the `<app>-v1.0.0` stamp until every backlog entry for the app is promoted or quotes the operator; §6's Done-when keeps deferral to the operator's own words and has an unattended run plan the row instead.
2. P2, §3 asked for two phase-specific `to-author` rows the Totals schema does not allow: verified. The proof is now a count of rows reading `to-author <ref> §5` and `§6` against the section design's two phase totals, with the Totals table's one `to-author` row equal to their sum.
3. P1, the release and design gates knew only the first three apps: verified. `RELEASE_APPS` now names Tinctura, Capio, and Folium and drives `RELEASE_TAG_PATTERN` and `RELEASE_ITEM_RE`, so their release sections meet the backlog gate and their `reviewed:` records parse; `DESIGN_DOMAIN_APPS` maps domains 07 to 09 and the shared core to every app; self-test cases cover each new app. Each plan's §5 now extends every remaining app list in the tooling (`release-manifest.ps1`, `build-design-site.py`, and any other the named `git grep` prints), and `todo/README.md` lists the new status forms.

## Round 4: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T08:51:08Z
- Effort: xhigh
- Lines: 20
- Digest: d64a34a1b2c4de08

adversarial: needs-attention

1. P1 `todo/07-tinctura/TODO-01-tinctura-plan.md:121`: §5 gates §6 on the published `tinctura-v0.1.0`, contradicting native-replan requirement 6, which forbids later phases depending on publication. An in-memory split with the release candidate complete and publication awaiting operator credentials makes `resolve 'D07 T01 §6'` return 4; depending on the release candidate returns 0. Capio and Folium repeat this conflict. Gate parity planning on the completed release candidate and adjust the “shipped” wording.

consistency: needs-attention

2. P3 `docs/design/components/AppIcon/preview.html:56`: The published construction caption still specifies tile `rx 48`, while the updated spec and generated masters use `rx 52`. Regenerating the design page preserves this contradiction because the caption remains in its source.

integration: needs-attention

3. P2 `tools/provision.ps1:177`: The new package verification and installation functions recognize only `python`, although the existing Python leg and `check-all.ps1` support `python3`. A mock exposing the interpreter only as `python3` returns Python-leg `OK=True` and package-leg `OK=False`, with “no python to check”; repair also selects only `python`. Reuse the interpreter selection across these functions.

source-defect: needs-attention

4. P2 `scripts/build-app-icons.py:249`: The duplicate-splash check counts only SVGs matching one exact opening tag. In an in-memory probe, inserting the pre-Solid Gesso nested icon with an added `class="old-icon"` attribute leaves two nested icons, yet `main(['build-app-icons.py', '--check'])` returns 0 and prints `app icons: 0 stale`. Count nested icons structurally so harmless attribute differences cannot hide an overlaid stale glyph.

record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 3

Every finding was verified and is real; record approved.

1. P1, each §6 waited on the published 0.1.0, which requirement 6 forbids: verified. §5 now adds the 0.1.0 release-candidate section (built, tested, packaged, signing-ready) to §6's Depends On, never the publication section that may wait on the operator's credentials; the §6 wording and the three Phase 42, 44, and 46 paragraphs say "the completed 0.1.0 release candidate".
2. P3, the AppIcon preview's caption still said `rx 48`: verified. It says `rx 52`, and the design page is regenerated.
3. P2, the `pydeps` leg and its repair looked only for `python`: verified. `tools/provision.ps1` has one `Get-Python3` that tries `python` then `python3`, and the python leg, the pydeps check, and its repair all use it.
4. P2, a nested icon with different attributes escaped the splash count: verified. The check counts every nested `<svg` element (the card is the root) and requires exactly one, the master at x 56, y 92; a probe adding a second icon with `class="old-icon"` now fails naming the count.

## Round 5: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T08:59:23Z
- Effort: xhigh
- Lines: 14
- Digest: 511363d7e4153929

adversarial: approve

consistency: approve

integration: approve

source-defect: needs-attention

1. P2 `scripts/build-app-icons.py:253`: The splash guard counts literal `<svg` tags, missing namespace-prefixed SVG elements. In an in-memory probe, appending the pre-Solid Gesso icon inside `<s:svg xmlns:s="http://www.w3.org/2000/svg">` at the splash’s icon coordinates produced two nested SVG elements and changed 14,513 rendered pixels, yet `main(['build-app-icons.py', '--check'])` returned 0 with `app icons: 0 stale`. Count SVG elements structurally by their namespace and local name.

record: approve

HIGHEST: P2
OVERALL: needs-attention

## Response to round 4

Four lenses approved; the one finding was verified and is real.

1. P2, a namespace-prefixed nested SVG escaped the splash count: verified. `scripts/build-app-icons.py` now parses the splash with `xml.etree.ElementTree` and counts every element whose expanded name is `{http://www.w3.org/2000/svg}svg`, whatever its prefix, below the root card; probes adding a second icon as `<s:svg xmlns:s=...>` and as `<svg class="old">` both fail naming two nested elements, and the committed splashes pass.
