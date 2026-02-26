# Your Skills Repo Name

A collection of skills for AI coding agents. Works with Claude Code, Cursor,
Codex, GitHub Copilot, Gemini CLI, more! Based on the
[agentskills.io](https://agentskills.io/) standard.

## Install

### Any agent (recommended)

```bash
npx skills add your-org/your-skills-repo
```

The CLI auto-detects your installed agents and symlinks the skills into each
one's expected directory. Options:

```bash
# Install a single skill
npx skills add your-org/your-skills-repo --skill skill-name

# Install globally (available in all projects)
npx skills add your-org/your-skills-repo -g

# Target a specific agent
npx skills add your-org/your-skills-repo -a claude-code
```

### Claude Code

```
/install-plugin your-org/your-skills-repo
```

### Manual

Clone the repo and symlink the skills you want:

```bash
git clone https://github.com/your-org/your-skills-repo.git ~/.agent-skills/your-skills-repo

# Claude Code
ln -s ~/.agent-skills/your-skills-repo/skills/* ~/.claude/skills/

# Cursor
ln -s ~/.agent-skills/your-skills-repo/skills/* ~/.cursor/skills/

# Codex
ln -s ~/.agent-skills/your-skills-repo/skills/* ~/.codex/skills/
```

Symlinks keep your skills in sync with `git pull`.

---

## Contributing a Skill

### Quick start

1. Create a new directory under `skills/` with your skill name
2. Add a `SKILL.md` file with frontmatter and instructions
3. Open a PR

```
skills/
└── your-skill-name/
    ├── SKILL.md            # Required
    ├── scripts/            # Optional: executable code
    ├── references/         # Optional: supplementary docs
    └── assets/             # Optional: templates, schemas, etc.
```

### SKILL.md format

Every skill needs a `SKILL.md` with YAML frontmatter and a Markdown body:

```yaml
---
name: your-skill-name
description: >-
  What this skill does. Use when [specific trigger conditions]. Handles
  [keywords agents will match on].
---
```

The body contains the actual instructions the agent will follow. Write it as
clear, step-by-step guidance with examples and edge cases.

### Frontmatter fields

| Field           | Required | Notes                                                                 |
| --------------- | -------- | --------------------------------------------------------------------- |
| `name`          | Yes      | Lowercase, hyphens only, max 64 chars. Must match the directory name. |
| `description`   | Yes      | Max 1024 chars. Describe what it does and when to use it.             |
| `license`       | No       | License name or reference to a bundled file.                          |
| `compatibility` | No       | Environment requirements (e.g. "Requires docker").                    |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools. Experimental.             |
| `metadata`      | No       | Arbitrary key-value pairs (author, version, etc.).                    |

### Writing good descriptions

The `description` is the only thing agents read at startup to decide if your
skill is relevant. This makes it the most important field.

**Do:**

- Describe what the skill does and when to trigger it
- Include specific keywords agents will match on
- Start with a verb ("Extracts text from PDFs", "Runs database migrations")

**Don't:**

- Summarize the workflow. Agents will follow the summary instead of reading the
  full SKILL.md.
- Be vague ("Helps with files")

### Managing context budget

Skills use progressive disclosure to stay lightweight:

1. **Description** (~100 tokens) -- loaded at startup for all installed skills
2. **SKILL.md body** (<5000 tokens) -- loaded when the skill activates
3. **References/scripts** -- loaded only when the skill explicitly asks for them

Rules of thumb:

- Keep `SKILL.md` under 500 lines
- Move detailed reference material to `references/`
- Keep file references one level deep (don't chain references to references)
- Scripts run externally and cost zero context tokens

### Optional directories

**`scripts/`** -- Executable code the agent can run.

- Use `stderr` for human-readable output, `stdout` for structured JSON
- Include `set -e` for fail-fast
- Add cleanup traps for temporary resources
- Document dependencies at the top of the script

**`references/`** -- Supplementary docs loaded on demand.

- Keep each file focused on one topic
- Name files descriptively (`api-endpoints.md`, not `ref1.md`)
- Reference them from SKILL.md: `See [API docs](references/api-endpoints.md)`

**`assets/`** -- Static resources: templates, schemas, config files, images.

### Example skill

```
skills/
└── lint-fix/
    ├── SKILL.md
    └── references/
        └── eslint-rules.md
```

```yaml
# skills/lint-fix/SKILL.md
---
name: lint-fix
description: >-
  Runs linting and auto-fixes code style issues. Use when the user asks to
  lint, fix formatting, or clean up code style. Supports ESLint, Prettier,
  and Stylelint.
---

# Lint and Fix

## Process

1. Detect which linters are configured in the project (check for
   `.eslintrc*`, `.prettierrc*`, `.stylelintrc*`, `package.json` config)
2. Run the appropriate fix command
3. Report what changed

## Common edge cases

- If no linter config exists, ask the user before installing one
- If multiple linters conflict, prefer the project's existing config
- See [ESLint rule reference](references/eslint-rules.md) for rule-specific
  guidance
```

### Checklist before opening a PR

- [ ] Directory name matches the `name` field in frontmatter
- [ ] Description says what it does and when to trigger (not how it works)
- [ ] SKILL.md is under 500 lines
- [ ] No agent-specific tool names in the SKILL.md body (use conditional
      language instead)
- [ ] Scripts are self-contained with documented dependencies
- [ ] Tested with at least one agent
