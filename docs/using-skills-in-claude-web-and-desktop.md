# Using Skills in Claude Web & Desktop

Skills from this repo can be uploaded to the Claude web and desktop apps via
**Customize > Skills > Upload a skill**. This guide covers how to find, download,
and upload them.

## How Claude's Upload Works

The upload dialog accepts two formats:

| Format | When to use |
| ------ | ----------- |
| **`.md`** | Single-file skills (a standalone SKILL.md with YAML frontmatter) |
| **`.zip`** | Multi-file skills (SKILL.md + references, scripts, or assets) |

All skills in this repo are published as ready-to-download `.zip` files on our
[GitHub Pages skill directory](https://vigetlabs.github.io/viget-agent-skills/).

## Downloading a Skill

1. Go to the [skill directory](https://vigetlabs.github.io/viget-agent-skills/)
2. Find the skill you want and click **Download .zip**
3. In Claude, go to **Customize > Skills**, click **+**, select **Upload a skill**
4. Upload the `.zip` file

You can also download a skill's zip directly:

```
https://vigetlabs.github.io/viget-agent-skills/skills/<skill-name>/<skill-name>.zip
```

For example:
```
https://vigetlabs.github.io/viget-agent-skills/skills/viget-lore/viget-lore.zip
```

## Verifying It Works

After uploading:

1. Your skill should appear under **My skills** in **Customize > Skills**
2. Toggle it on if it isn't already enabled
3. Start a new conversation and try a prompt that should trigger the skill
4. Check Claude's thinking (if visible) to confirm the skill loaded

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| Upload rejected | Check that `.md` files have valid YAML frontmatter with `name` and `description` fields |
| Skill doesn't trigger | The `description` field is what Claude uses to decide relevance — make sure it matches your prompt |
| Zip rejected | Ensure the zip contains a folder (not loose files) with a `SKILL.md` at its root |
| References not loading | Confirm the file paths in `SKILL.md` match the actual filenames in the zip |

<details>
<summary>Manual packaging (advanced)</summary>

If you need to package a skill manually (e.g. for a local fork):

### Command line

```bash
# Clone the repo (or pull if you already have it)
git clone https://github.com/vigetlabs/viget-agent-skills.git
cd viget-agent-skills/skills

# Zip the skill folder
zip -r viget-lore.zip viget-lore/

# Upload viget-lore.zip to Claude
```

### Zip structure requirements

Claude expects the zip to contain a **folder** with `SKILL.md` inside it —
not loose files at the zip root.

**Correct:**
```
viget-lore.zip
└── viget-lore/
    ├── SKILL.md
    └── references/
        ├── founding-and-origins.md
        └── ...
```

**Incorrect:**
```
viget-lore.zip
├── SKILL.md          <-- files directly in zip root
└── references/
```

</details>
