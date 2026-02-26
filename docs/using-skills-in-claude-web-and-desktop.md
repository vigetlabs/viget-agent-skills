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

## Skill Compatibility

Not all skills in this repo work with Claude Web & Desktop yet. Check the table
below or look at a skill's directory on GitHub to see if it's a single file or
multi-file.

| Type | Example | Web & Desktop support |
| ---- | ------- | --------------------- |
| Single-file (just `SKILL.md`) | — | Supported — download and upload directly |
| Multi-file (`SKILL.md` + `references/`, `scripts/`, etc.) | `viget-lore` | Coming soon |

## Uploading a Single-File Skill

If a skill is just a `SKILL.md` with no subdirectories:

1. Navigate to the skill's `SKILL.md` on GitHub
   (e.g. `skills/your-skill-name/SKILL.md`)
2. Click the **Raw** button (or the download icon)
3. Save the file (right-click > "Save As" if viewing raw)
4. In Claude, go to **Customize > Skills**, click **+**, select **Upload a skill**
5. Upload the `.md` file

## Multi-File Skills (Coming Soon)

Skills like [`viget-lore`](../skills/viget-lore/) include a `references/`
directory with supporting files that `SKILL.md` loads on demand. These need to
be uploaded as a `.zip` file.

GitHub doesn't natively support downloading a subdirectory as a zip, so we're
working on a tool to make this seamless. In the meantime, you can package a
multi-file skill manually:

### Manual download

1. Create a new folder on your computer named after the skill (e.g. `viget-lore`)
2. On GitHub, navigate into the skill's directory and download each file —
   click the file, then click the **Raw** button and save it (right-click >
   "Save As")
3. Recreate any subdirectories locally (e.g. `references/`) and download those
   files into them
4. Select the **folder itself** (not its contents) and compress it to a `.zip`
5. Upload the zip in **Customize > Skills**

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
