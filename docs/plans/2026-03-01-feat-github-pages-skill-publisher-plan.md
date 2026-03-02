---
title: "feat: GitHub Pages Skill Publisher"
type: feat
status: completed
date: 2026-03-01
---

# feat: GitHub Pages Skill Publisher

## Enhancement Summary

**Deepened on:** 2026-03-01
**Research agents used:** architecture-strategist, security-sentinel, performance-oracle, kieran-python-reviewer, code-simplicity-reviewer, deployment-verification-agent, best-practices-researcher, framework-docs-researcher

### Key Improvements Over Initial Plan

1. **Script moved to `.github/scripts/`** — keeps CI infra separate from skill content; `scripts/` inside a skill is a convention for agent-accessible scripts
2. **`python-frontmatter` replaces regex parsing** — the `viget-lore` description is already a `>-` multi-line block scalar; regex silently truncates it
3. **Per-job permission scoping** — build job only needs `contents: read`; deploy job gets `pages: write` + `id-token: write`
4. **`zipfile` stdlib replaces `zip` subprocess** — removes external binary dependency, enables path validation, better portability
5. **`NamedTuple` replaces `dict`** — typed contract for skill metadata instead of arbitrary key convention
6. **`actions/setup-python` with pip cache** — saves 8-15s per run at negligible implementation cost
7. **Add `_site/` to `.gitignore`** — prevents accidental commit of binary zip build artifacts
8. **SHA-pinned actions + Dependabot** — supply chain hardening for the deployment workflow

### New Considerations Discovered

- `"fenced_code"` and `"tables"` are the correct extension IDs (not `"fenced-code"` or `"fenced_code_blocks"`)
- `md.reset()` is the correct reuse pattern for `markdown.Markdown` instances
- `md.convert()` returns an HTML fragment with no trailing newline (safe to embed directly)
- `actions/upload-pages-artifact@v3` is the current version (v1/v2 used deprecated artifact internals)
- HTML injection risk: `python-markdown` passes raw `<script>` tags through unchanged; add `bleach` sanitization
- Skill directory names should be validated against the naming convention before processing

---

## Overview

Add a GitHub Action that automatically packages every skill as a `.zip` file and deploys a browsable, downloadable skill directory to GitHub Pages on every push to `main`. This closes the "Coming soon" gap in the multi-file skill installation docs and makes every skill a one-click download.

## Problem Statement / Motivation

The current `docs/using-skills-in-claude-web-and-desktop.md` guide tells users to manually zip skills for Claude Web & Desktop upload. For multi-file skills like `viget-lore`, this requires cloning the repo and running a shell command — a high-friction install path. A GitHub Pages site removes that friction entirely with permanent, shareable download URLs.

## Proposed Solution

A two-step GitHub Action:

1. **Build job** — a Python script traverses `skills/`, zips every valid skill, generates per-skill and root HTML pages, writes everything to `_site/`
2. **Deploy job** — uploads `_site/` to GitHub Pages via the standard `upload-pages-artifact` + `deploy-pages` action chain

A browsable site is published at `https://vigetlabs.github.io/viget-agent-skills/` with direct download links for every skill.

## Technical Considerations

### Script Location

The build script lives at **`.github/scripts/build-site.py`**, not `scripts/build-site.py`. The `scripts/` directory inside a skill folder is a convention for agent-accessible executable content (per `CLAUDE.md`). A repo-level build script belongs under `.github/` alongside all CI/CD concerns.

### Zip Structure

Claude requires the zip root to contain a named folder — not loose files. The build script uses Python's `zipfile` stdlib module (no external `zip` binary) to write zips with the correct structure:

```python
import zipfile

def zip_skill(skill_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_dir.rglob("*"):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(skill_dir.parent))
```

This produces zips where the root entry is `<skill-name>/`, matching Claude's upload requirement documented in `docs/using-skills-in-claude-web-and-desktop.md:72-85`.

**Research insight:** Using `zipfile` eliminates the external `zip` binary dependency, enables path validation before adding files, and avoids subprocess fork overhead.

### Markdown → HTML

The build script uses the **Python `markdown` library** with `fenced_code` and `tables` extensions. One instance is created per process and reused with `.reset()` between conversions:

```python
import markdown

_md = markdown.Markdown(
    extensions=["fenced_code", "tables"],
    output_format="html",
)

def to_html(source: str) -> str:
    html = _md.convert(source.strip())
    _md.reset()
    return html
```

**Research insights:**
- `"fenced_code"` and `"tables"` are the exact correct extension IDs. `"fenced-code"`, `"fenced_code_blocks"`, `"table"` all raise `ModuleNotFoundError`.
- `md.convert()` returns an HTML **fragment** (no `<!DOCTYPE>`, no `<html>`) with no trailing newline — safe to embed directly into a template.
- `md.reset()` is the correct documented reuse pattern; it clears all state accumulated during conversion.
- `output_format="html"` (not `"xhtml"`) produces `<br>` not `<br />`.
- An empty string input returns `''` — no error.

### YAML Frontmatter

**`python-frontmatter` replaces regex parsing.** The `viget-lore` SKILL.md already uses a `>-` multi-line block scalar for its `description` field. A regex like `re.search(r'^description:\s*(.+)$', ...)` captures only the literal `>-` marker, not the folded content — silently truncating the description on the published site.

```python
import frontmatter  # python-frontmatter library

def load_skill_md(path: Path) -> tuple[str, str, str]:
    """Returns (name, description, body) from a SKILL.md."""
    post = frontmatter.load(path)
    return (
        post.get("name", path.parent.name),
        post.get("description", ""),
        post.content,  # body with frontmatter already stripped
    )
```

`python-frontmatter` handles `>-` block scalars, quoted strings, colons in values, and all other YAML edge cases correctly. It also strips the frontmatter and returns `.content` in one call — eliminating `strip_frontmatter` as a separate function.

### Skill Metadata Type

Use a `NamedTuple` instead of a raw `dict` — typed contract, no key name guessing:

```python
from typing import NamedTuple

class SkillMeta(NamedTuple):
    name: str
    description: str
    skill_dir: Path
```

### HTML Sanitization

The `python-markdown` library passes raw HTML through unchanged by default. A SKILL.md containing `<script>...</script>` survives the build and executes in visitor browsers (stored XSS). Sanitize the HTML fragment before writing:

```python
import bleach

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS | {
    "p", "pre", "code", "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li", "table", "thead", "tbody", "tr", "th", "td",
    "blockquote", "hr", "img",
}
ALLOWED_ATTRS = {**bleach.sanitizer.ALLOWED_ATTRIBUTES, "img": ["src", "alt"]}

clean_body = bleach.clean(html_body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
```

### Skill Name Validation

Validate skill directory names against the naming convention (per `CLAUDE.md`: lowercase, hyphens only, max 64 characters) before processing. This catches typos, enforces convention, and prevents zip path traversal:

```python
import re

_VALID_NAME = re.compile(r'^[a-z][a-z0-9-]{0,63}$')

def is_valid_skill_name(name: str) -> bool:
    return bool(_VALID_NAME.match(name))
```

### Concurrency

A `concurrency` group prevents overlapping deployments on rapid pushes. Uses `cancel-in-progress: false` (not `true`) to avoid leaving the Pages site in a broken mid-deployment state.

## Implementation

### Files to Create

#### `.github/workflows/publish-skills.yml`

Two jobs with per-job permission scoping. SHA-pinned actions with inline version comments.

```yaml
name: Publish Skills to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

# Deny all at workflow level; grant minimum per job
permissions: {}

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@<SHA>  # v4
      - uses: actions/configure-pages@<SHA>  # v5
      - uses: actions/setup-python@<SHA>  # v5
        with:
          python-version: "3.12"
          cache: "pip"
          cache-dependency-path: ".github/requirements.txt"
      - name: Install dependencies
        run: pip install -r .github/requirements.txt
      - name: Build site
        run: python3 .github/scripts/build-site.py
      - uses: actions/upload-pages-artifact@<SHA>  # v3
        with:
          path: ./_site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@<SHA>  # v4
```

**Research insight:** SHA-pinned actions prevent supply chain attacks where a tag is force-pushed with malicious code. During implementation, replace each `<SHA>` with the current commit SHA for that tag. Dependabot (below) keeps SHAs current automatically.

**Research insight:** Per-job permissions follow the principle of least privilege. The build job's pip install step runs only with `contents: read` — not `pages: write` or `id-token: write`. If a compromised package ran malicious code in the build step under the original workflow, it would have had access to the Pages deployment token.

**Research insight:** `actions/setup-python` with `cache: "pip"` saves 8-15 seconds per run by caching pip wheels. The cache key is automatically derived from the hash of `cache-dependency-path`.

#### `.github/requirements.txt`

Pinned dependency versions for reproducible builds:

```
markdown==3.7
python-frontmatter==1.1.0
bleach==6.2.0
```

#### `.github/scripts/build-site.py`

Python 3.12 script. Key design decisions informed by research:

1. Cleans `_site/` with `shutil.rmtree` + `mkdir` (correct at current skill count; incremental builds not worth the complexity until 30+ skills)
2. Validates skill directory names against `CLAUDE.md` naming convention
3. Skips any directory without a `SKILL.md` (logs warning with `logging.warning`)
4. For each valid skill:
   - Loads frontmatter with `python-frontmatter` (handles multi-line block scalars)
   - Validates `name` and `description` fields exist
   - Creates zip with `zipfile` stdlib module
   - Determines HTML source: `README.md` if present, else `SKILL.md` body (already stripped by `python-frontmatter`)
   - Converts with `markdown.Markdown` instance (reused, `reset()` between files)
   - Sanitizes with `bleach`
   - Wraps in full HTML document with inline CSS and download button
   - Writes to `_site/skills/<name>/index.html`
5. Generates `_site/index.html` with alphabetical skill listing (name, description, skill page link, download button)

**Key functions:**
- `load_skill_md(path)` → `tuple[str, str, str]` — uses `python-frontmatter` to return `(name, description, body)`
- `zip_skill(skill_dir, zip_path)` → `None` — uses `zipfile.ZipFile` to write correct zip structure
- `to_html(source)` → `str` — converts + `reset()` + sanitizes with `bleach`
- `wrap_html(title, body, download_url)` → `str` — full document with module-level `CSS` constant
- `build_skill(skill_dir)` → `SkillMeta | None` — orchestrates zip + HTML for one skill
- `main()` — cleans `_site/`, iterates skills, calls `build_root_index`

**Inline CSS** lives as a module-level `CSS` constant (not embedded in `wrap_html`) so it can be read and edited without navigating into the function body. Includes: system font, max-width 800px, download button, table styles, pre/code styles.

**Logging:** uses `logging.warning` (not `print`) so output level is controllable and warnings go to stderr by default.

#### `.github/dependabot.yml`

Keeps action SHA pins current automatically:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "pip"
    directory: "/.github"
    schedule:
      interval: "weekly"
```

#### Add `_site/` to `.gitignore`

The build output directory contains binary zip files. If accidentally committed, it bloats the repository. Add before implementation PR is opened.

```
# existing .gitignore entries
**/scratch

# add:
_site/
```

### File to Update

#### `docs/using-skills-in-claude-web-and-desktop.md`

Replace the "Coming soon" section for multi-file skills with direct download instructions pointing to the Pages URLs:

```
https://vigetlabs.github.io/viget-agent-skills/skills/<skill-name>/<skill-name>.zip
```

Remove or collapse the "Manual download" and "Command line" fallback instructions into a `<details>` block for advanced users.

## Acceptance Criteria

- [ ] Pushing to `main` triggers the workflow and deploys to GitHub Pages
- [ ] `https://vigetlabs.github.io/viget-agent-skills/` serves a root `index.html` listing all valid skills alphabetically with name, description, link, and download button
- [ ] Each skill has a page at `.../skills/<name>/index.html` with readable content and a download button
- [ ] Each skill has a downloadable zip at `.../skills/<name>/<name>.zip`
- [ ] Zip structure matches Claude's upload requirement: root folder named after the skill containing `SKILL.md` and any subdirectories
- [ ] Skill directories without a `SKILL.md` are skipped with a build log warning (not a build failure)
- [ ] Skill directories with invalid names (not matching `^[a-z][a-z0-9-]{0,63}$`) are skipped with a warning
- [ ] `viget-lore`'s full multi-line description appears correctly on the root index (not truncated to `>-`)
- [ ] `docs/using-skills-in-claude-web-and-desktop.md` updated to reference the new download URLs
- [ ] `_site/` is in `.gitignore`
- [ ] Verify zip MIME type: `curl -I .../viget-lore.zip` returns `content-type: application/zip` or `application/octet-stream`

## Pre-Deployment Checklist (One-Time Manual Step)

Before pushing the workflow file to `main`:

1. Go to `https://github.com/vigetlabs/viget-agent-skills/settings/pages`
2. Under "Build and deployment" > "Source", select **"GitHub Actions"** (not "Deploy from a branch")
3. Save. If this step is skipped, the `deploy-pages` action fails with a permissions error on the first run.

## Dependencies & Risks

**One-time setup required:** The repository's Pages source must be switched to "GitHub Actions" in Settings > Pages before the first push. See Pre-Deployment Checklist above.

**`viget-brand-guidelines` has no `SKILL.md`:** This directory will be skipped with a warning and will not appear on the published site. This is the correct behavior. Contributors who see it in the source tree but not on the site should interpret the absence as "skeleton in progress."

**`_site/` directory in CLAUDE.md:** Once the pipeline exists, add `_site/` to the project structure comment in `CLAUDE.md` — it is generated output, not source content.

**Rollback:** Revert the offending commit and push to `main`. The workflow re-runs and deploys the reverted content. There is no persistent state to restore — Pages serves static files only.

**pip dependency network:** The workflow fetches `markdown`, `python-frontmatter`, and `bleach` from PyPI on each run (with pip caching for wheel reuse). If PyPI is unreachable, the build fails. Pinned versions in `requirements.txt` prevent silent breakage from new releases.

## References & Research

- Workflow pattern: `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3` (not v1/v2 — those used deprecated artifact internals), `actions/deploy-pages@v4`
- Python `markdown` library docs: https://python-markdown.github.io/ — extension IDs, `reset()` pattern, `output_format` values
- `python-frontmatter` library: handles YAML `>-` block scalars correctly
- `bleach` library: HTML sanitization post-processing
- Per-job permissions: [GitHub Security Hardening docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- SHA pinning: [StepSecurity pinning guide](https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide)
- pip caching: `actions/setup-python` with `cache: "pip"` and `cache-dependency-path`
- Zip structure requirement: `docs/using-skills-in-claude-web-and-desktop.md:72-85`
- Zip MIME type: served as `application/zip` by GitHub Pages by default, no configuration needed
