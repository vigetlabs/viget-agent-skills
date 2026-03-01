#!/usr/bin/env python3
"""Build the GitHub Pages site for viget-agent-skills.

Reads skills/ directory, generates per-skill index.html + zip, and a root
index.html listing all skills. Output goes to _site/.

Run from the repository root:
    python3 .github/scripts/build-site.py
"""

import html
import logging
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import NamedTuple

import frontmatter
import markdown
import nh3

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

SKILLS_DIR = Path("skills")
SITE_DIR = Path("_site")
SKILLS_SITE_DIR = SITE_DIR / "skills"

# Skill name convention from CLAUDE.md: lowercase letters, digits, hyphens, max 64 chars
_VALID_NAME = re.compile(r"^[a-z][a-z0-9-]{0,63}$")

# Reuse one Markdown instance; call .reset() between conversions
_MD = markdown.Markdown(extensions=["fenced_code", "tables"], output_format="html")

# Allowed HTML tags and attributes after nh3 sanitization.
# bleach defaults were: a, abbr, acronym, b, blockquote, code, em, i, li, ol, strong, ul
_ALLOWED_TAGS = {
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol", "strong", "ul",
    "p", "pre", "h1", "h2", "h3", "h4", "h5", "h6",
    "table", "thead", "tbody", "tr", "th", "td",
    "hr", "br", "img",
}
# bleach defaults were: {"a": ["href", "title"], "abbr": ["title"], "acronym": ["title"]}
_ALLOWED_ATTRS = {
    "a": {"href", "title"},
    "abbr": {"title"},
    "acronym": {"title"},
    "img": {"src", "alt"},
    "th": {"align"},
    "td": {"align"},
    "code": {"class"},   # fenced_code adds language-* class
    "pre": {"class"},
}

CSS = """
    body {
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1.5rem;
      color: #333;
      line-height: 1.6;
    }
    h1, h2, h3 { line-height: 1.3; }
    a { color: #0066cc; }
    code {
      background: #f4f4f4;
      padding: 0.15em 0.35em;
      border-radius: 3px;
      font-size: 0.9em;
    }
    pre {
      background: #f4f4f4;
      padding: 1rem;
      border-radius: 6px;
      overflow-x: auto;
    }
    pre code { background: none; padding: 0; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th, td { text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid #ddd; }
    th { background: #f8f8f8; font-weight: 600; }
    .download-btn {
      display: inline-block;
      background: #0066cc;
      color: white;
      padding: 0.5rem 1.25rem;
      border-radius: 6px;
      text-decoration: none;
      font-size: 0.95em;
      margin: 0.5rem 0 1.5rem;
    }
    .download-btn:hover { background: #0052a3; }
    .skill-desc { color: #555; font-size: 0.9em; margin-top: 0.2rem; }
    .back-link { display: block; margin-bottom: 1.5rem; font-size: 0.9em; }
"""


class SkillMeta(NamedTuple):
    name: str
    description: str
    dir_name: str  # filesystem directory name, used for URL paths


def to_html(source: str) -> str:
    """Convert a Markdown string to a sanitized HTML fragment."""
    raw = _MD.convert(source.strip())
    _MD.reset()
    return nh3.clean(raw, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS, strip_comments=True)


def wrap_html(
    title: str,
    body: str,
    *,
    download_url: str | None = None,
    back_link: bool = False,
) -> str:
    """Wrap an HTML fragment in a full document with inline CSS."""
    back = '<a class="back-link" href="../../">\u2190 All Skills</a>\n' if back_link else ""
    dl = f'<a class="download-btn" href="{download_url}">Download .zip</a>\n' if download_url else ""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src https: data:">
  <title>{html.escape(title)}</title>
  <style>{CSS}  </style>
</head>
<body>
{back}{dl}{body}
</body>
</html>
"""


def zip_skill(skill_dir: Path, zip_path: Path) -> None:
    """Write a zip whose root entry is the skill folder (e.g. viget-lore/)."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_dir.rglob("*")):
            if not file_path.is_file():
                continue
            if file_path.is_symlink():
                logger.warning("Skipping symlink %s", file_path)
                continue
            # Arcname keeps the skill folder as the zip root
            arcname = file_path.relative_to(skill_dir.parent)
            zf.write(file_path, arcname)


def build_skill(skill_dir: Path) -> SkillMeta:
    """Build zip + index.html for one skill directory.

    Returns SkillMeta on success, exits with code 1 on failure.
    """
    dir_name = skill_dir.name

    if not _VALID_NAME.match(dir_name):
        logger.error(
            "Skill %r failed — name must match ^[a-z][a-z0-9-]{0,63}$", dir_name
        )
        sys.exit(1)

    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        logger.error("Skill %r failed — no SKILL.md found", dir_name)
        sys.exit(1)

    # python-frontmatter correctly handles multi-line YAML block scalars (>-, |, etc.)
    post = frontmatter.load(skill_md_path)
    display_name = post.get("name", dir_name)
    description = post.get("description", "")

    # HTML source: README.md if present, else the SKILL.md body (frontmatter already stripped)
    readme_path = skill_dir / "README.md"
    source_text = (
        readme_path.read_text(encoding="utf-8")
        if readme_path.exists()
        else post.content
    )

    out_dir = SKILLS_SITE_DIR / dir_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Zip
    zip_name = f"{dir_name}.zip"
    zip_skill(skill_dir, out_dir / zip_name)

    # index.html
    html_body = to_html(source_text)
    page = wrap_html(display_name, html_body, download_url=zip_name, back_link=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")

    logger.info("Built  %s", dir_name)
    return SkillMeta(name=display_name, description=description, dir_name=dir_name)


def build_root_index(skills: list[SkillMeta]) -> None:
    """Generate _site/index.html listing all skills alphabetically."""
    rows = []
    for s in sorted(skills, key=lambda s: s.name.lower()):
        rows.append(
            f"    <tr>\n"
            f'      <td>\n'
            f'        <a href="skills/{s.dir_name}/">{html.escape(s.name)}</a>\n'
            f'        <div class="skill-desc">{html.escape(s.description)}</div>\n'
            f"      </td>\n"
            f'      <td><a class="download-btn" href="skills/{s.dir_name}/{s.dir_name}.zip">'
            f"Download .zip</a></td>\n"
            f"    </tr>"
        )

    body = (
        "<h1>Viget Agent Skills</h1>\n"
        "<p>A collection of reusable skills for AI coding agents. "
        "Download a <code>.zip</code> and upload it to Claude, Cursor, or any compatible tool.</p>\n"
        "<table>\n"
        "  <thead>\n"
        "    <tr><th>Skill</th><th>Download</th></tr>\n"
        "  </thead>\n"
        "  <tbody>\n"
        f"{''.join(rows)}\n"
        "  </tbody>\n"
        "</table>"
    )

    page = wrap_html("Viget Agent Skills", body)
    (SITE_DIR / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SKILLS_SITE_DIR.mkdir(parents=True)

    skills: list[SkillMeta] = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if skill_dir.is_dir():
            skills.append(build_skill(skill_dir))

    if not skills:
        logger.error("No skill directories found in %s/ — aborting.", SKILLS_DIR)
        sys.exit(1)

    build_root_index(skills)
    logger.info("Done — built %d skill(s) into %s/", len(skills), SITE_DIR)


if __name__ == "__main__":
    main()
