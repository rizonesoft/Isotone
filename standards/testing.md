# Testing Standards

How the suite proves its work. The five proofs a TODO checkpoint may cite are defined in [`todo/README.md`](../todo/README.md); the gate card sections run is [`.claude/skills/process-todo-section/gates.md`](../.claude/skills/process-todo-section/gates.md). Where this file and the gate card disagree, this file wins and the card is corrected in the same commit.

## Test projects

- xUnit, one test project per production assembly or app `Core`, under `tests/` once the layout restructure lands (`tests/Photon.Nodus.Tests`, `tests/Photon.Imago.Core.Tests`, and so on). Today they sit inside each app folder.
- Every test runs through `dotnet test Photon.slnx`. A test that needs something the CI runner lacks (a display, a GPU, a network) is marked with a trait (`[Trait("Requires", "display")]`) and skipped with a reason, never left to fail.
- Assertions: plain xUnit `Assert`, or the assertion library the recorded decision in `docs/dev/decisions.md` names. One assertion library in the whole suite.

## Naming and shape

- Test classes are `<TypeUnderTest>Tests`; tests are `Method_Scenario_Expected` (`Save_ReadOnlyTarget_RefusesAndKeepsDocumentDirty`).
- Arrange, act, assert, one behavior per test. A test that asserts nothing or only that no exception was thrown is not a test.
- No shared mutable state between tests. A test that touches the file system works in its own temporary folder; one that touches settings or app data points the service at that folder. Nothing writes under the real `%LOCALAPPDATA%`.

## Fixtures and fidelity

- Fixtures live under `tests/fixtures/<app>/<format>/`, committed, small, and licensed for redistribution (the source and license are recorded in a `README.md` beside them).
- A format reader or writer owes a round trip: open the fixture, save, reopen, and compare against the original or a golden, element by element for vector documents and pixel by pixel within a stated tolerance for raster and RAW output. Goldens produced by a reference implementation record its name and version beside them.
- Fidelity tests carry `[Trait("Category", "Fidelity")]` so `dotnet test Photon.slnx --filter "Category=Fidelity"` runs them all.
- Large corpora (RAW sample sets) are not committed: a script downloads a pinned list with SHA-256 checks into `build/fixtures/`, and at least one small fixture per format is committed so the proof runs on every clone.

## Failure paths

Every reader, writer, and user-document path is tested on its failure too: a truncated or corrupt file, a read-only target, a locked file, a full disk (simulated), an unsupported mode. The test asserts the message and that nothing was damaged.

## Surfaces

Until a UI test suite exists, a surface is proven by the launch smoke in the gate card: build, launch, drive the changed surface, quote the Serilog error count, and commit a capture under `docs/captures/<app>/`. A unit test on the view model behind the surface is owed as well.

## The quarantine

`tests/Photon.runsettings` holds a `TestCaseFilter` that excludes known-failing legacy tests. It is debt: each entry is listed in `docs/dev/build.md`, owned by a TODO section, and removed in the change that fixes its test. Adding an entry needs a TODO section that owns its removal.

## Coverage

Coverage is measured (`coverlet.collector`) and reported, not gated by a percentage. A section that adds logic adds the tests that pin it; review refuses logic without them.
