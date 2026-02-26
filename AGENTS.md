# Viget Agent Skills

A public repository of skills for AI coding agents, based on the
[agentskills.io](https://agentskills.io/) standard. Skills work across Claude
Code, Cursor, Codex, GitHub Copilot, Gemini CLI, and more.

## Project Structure

```
skills/                  # Each skill is a directory
  <skill-name>/
    SKILL.md             # Required entry point
    references/          # Optional: supplementary docs loaded on demand
    scripts/             # Optional: executable code
    assets/              # Optional: templates, schemas, static files
docs/                    # User-facing guides
scratch/                 # Temporary files, not committed (gitignored)
```

## Conventions

- This is a **public repo**. Never commit proprietary or internal-only content.
- ALWAYS flag to users if you find content that might be sensitive to public sharing.
- Each skill directory name must match the `name` field in its SKILL.md
  frontmatter.
- Skill names are lowercase with hyphens only, max 64 characters.
- SKILL.md files must have YAML frontmatter with `name` and `description`.
- Keep SKILL.md under 500 lines. Move detailed content to `references/`.
- File references are one level deep — don't chain references to references.
- Descriptions should say **what** the skill does and **when** to trigger it,
  not how it works internally.
- No agent-specific tool names in SKILL.md bodies — use conditional language
  so skills work across agents.

## Adding a Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter and instructions.
2. Add `references/`, `scripts/`, or `assets/` subdirectories as needed.
3. Test with at least one agent before opening a PR.

See the README for full contributing guidelines and the frontmatter field
reference.
