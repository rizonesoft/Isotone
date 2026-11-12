---
name: authoring-skills
description: Use when creating, moving, reviewing, or documenting project skills, skill references, Antigravity (.agents/skills) or Claude (.claude/skills) skill folders, or agent-scoped rules.
---

# Authoring Skills

Keep repository skills clean, self-contained, and aligned across Isotone's writer harnesses (`.agents/skills/` for Google Antigravity, `.claude/skills/` for Claude Code). Note that `codex` runs strictly as a read-only headless reviewer via `scripts/review-dispatch.py`, so Isotone does **not** carry a `.codex/` directory.

## Required Pattern

1. Place Antigravity skills in `.agents/skills/<skill-name>/SKILL.md` (loaded via `.agents/skills.json`) and Claude skills in `.claude/skills/<skill-name>/SKILL.md`.
2. Keep both `.agents/skills/` and `.claude/skills/` as real files and directories, never symlinks.
3. Name each skill directory in kebab-case for the capability (`process-todo-section`, `local-tool-safety`) and match `name:` in YAML frontmatter to the directory name.
4. Put detailed checklists in `references/` and templates in `todo-template.md` or `assets/` inside the owning skill folder.
5. Never place OpenAI/Codex `agents/openai.yaml` files inside `.agents/skills/` or `.claude/skills/`.
6. Follow Isotone's prose and validator rules in every `SKILL.md`:
   - Zero em dashes or en dashes (`--` only), and one line per Markdown paragraph and list item.
   - Never write bare short section citations (`§<N>`, `T<NN> §<N>`, or `file.md §<N>`), and ensure any literal `DNN TNN §N` reference resolves in `todo/` (`python scripts/todo-graph.py validate` checks both `.agents/skills/` and `.claude/skills/` under Rule 26; use `D<NN> T<NN> §<N>` for placeholders).

## Validation

```powershell
python scripts/todo-graph.py validate
python scripts/campaign_guard.py --self-test
```

Confirm both exit `0`, frontmatter `name` matches each folder name, no symlinks exist, and `AGENTS.md` / `.conclave/kits.json` stay in sync when managed skills change.
