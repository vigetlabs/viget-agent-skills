---
date: 2026-03-01
topic: github-pages-skill-publisher
---

# GitHub Pages Skill Publisher

## What We're Building

A GitHub Action that automatically packages every skill as a zip file and deploys them to GitHub Pages on every push to `main`. The site serves as both a download hub and a browsable directory — users can read about a skill and grab its zip in one place.

Every skill gets published as a zip (regardless of whether it's single-file or multi-file), along with a human-readable `index.html` page. A root `index.html` ties everything together with links and download buttons for each skill.

## Why This Approach

Currently the `docs/using-skills-in-claude-web-and-desktop.md` guide has "Coming soon" language for multi-file skill downloads. This action closes that gap with zero manual steps — a maintainer merges a new skill and it's immediately available for download.

Publishing everything as a zip (including single-file skills) keeps the download story uniform: users always download a zip, regardless of skill complexity.

## Key Decisions

- **Trigger:** Push to `main` — simplest, always up to date, no path filtering needed.
- **All skills as zips:** Single-file and multi-file skills are both packaged as zips. Consistent UX for users; no conditional download logic needed.
- **Zip structure:** Each zip contains a named folder (e.g. `viget-lore/`) at its root, matching Claude's upload requirement. Built by running `zip -r <skill>.zip <skill>/` from inside `skills/`.
- **Per-skill index.html:** Generated from `README.md` if present, else from `SKILL.md`. YAML frontmatter stripped before rendering. Includes a download button for the zip.
- **Root index.html:** Lists all valid skills (those with a `SKILL.md`), each with a link to the skill's page and a direct download link.
- **Styling:** Light inline CSS — clean typography, max-width, basic colors. No external CDN dependencies.
- **Invalid skills skipped:** Any skill directory without a `SKILL.md` (e.g. `viget-brand-guidelines` currently) is excluded from the build.

## URL Structure

```
https://vigetlabs.github.io/viget-agent-skills/
├── index.html                          ← root listing
└── skills/
    └── viget-lore/
        ├── index.html                  ← skill page
        └── viget-lore.zip             ← download
```

## Implied Follow-On

Once live, `docs/using-skills-in-claude-web-and-desktop.md` should be updated to replace the "Coming soon" language with direct download URLs pointing to the Pages site.

## Open Questions

_(none — resolved during brainstorm)_

## Resolved Questions

- **Should single-file skills be zipped?** Yes — uniform format for all skills.
- **Should there be an index.json?** Replaced by index.html; not needed separately.
- **HTML source priority?** README.md if present, SKILL.md as fallback.
- **Trigger scope?** Push to main (not path-filtered).
- **Styling approach?** Light inline CSS, no CDN dependencies.

## Next Steps

→ `/workflows:plan` for implementation details
