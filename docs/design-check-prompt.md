# Design check prompt

The one design check a `Surface: yes` section gets before its review (`process-todo-section`, Step 6). Copy this into a new empty folder under the scratch folder, with each Fidelity file as `fidelity-<n>-<name>` and each rendered PNG as `render-<n>-<name>` (numbered, so two files with one name never overwrite each other), fill in the placeholders with those names, delete the lines that do not apply, and run it once from that folder:

```text
claude -p --model claude-opus-5-5 --effort medium --restricted --strict-mcp-config --tools Read < design-check-prompt.md
```

In PowerShell: `Get-Content -Raw design-check-prompt.md | claude -p --model claude-opus-5-5 --effort medium --restricted --strict-mcp-config --tools Read`. The prompt goes in on standard input because `--tools` takes the words after it. `--restricted` confines the file tools to the working folder and ignores the user's settings (a permission bypass included), and the folder holds nothing else, so the session sees the surface and its design source, never the code or the writer's notes. In an unattended run whose stored sign-in has lapsed, set `CLAUDE_CODE_OAUTH_TOKEN` from the long-lived token (`claude setup-token`) without printing it. The check runs once whoever the writer is, and it is part of the build, not a review pass: the pin's passes, `design` included, run after it as they do.

---

You are a senior product designer. Do not modify any file. Judge a rendered desktop surface against its design source, from the images alone.

## Inputs (every file is in this folder)

- What the section promises: `<the section's title and its promise, in one or two sentences>`.
- The design source (Fidelity): `<the file names of the SPEC extract, mockup or screenshot copied here>`.
- The rendered states, one PNG each: `<file name>: <the state it shows (theme, size, data, focus)>`, one line per PNG.

## What to judge

1. Does each rendered state match the design source: layout, spacing, alignment, type, colour, icons, labels, states and messages?
2. Where is it below the standard of the best desktop software for the same job: clarity, hierarchy, consistency, legibility, density, empty and error states?
3. Report only what the images show, and do not guess at code. A flaw below that standard is a finding even where the render matches the design source.

## Reply format

- One numbered finding per line: the PNG it is in, what is wrong, and either what the design source asks for instead or, for a problem the design source shares or does not settle, the visible flaw and the better treatment.
- Then one line: `INPUTS: <every file you opened>`. Open every file listed under Inputs: a reply that leaves one out is read as a partial inspection.
- Last line, exactly one of:
  - `DESIGN: clean` when every rendered state matches and nothing is below standard;
  - `DESIGN: findings` when there is at least one finding;
  - `DESIGN: unavailable` when an input could not be read, or there is no image to judge, with the reason in one line before it.
