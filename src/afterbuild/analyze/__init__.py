"""Analyze command implementation.

The ``run_analyze`` function walks the repository tree, gathers a brief
summary (languages, dependencies, entry points, git history, README, test
presence) and writes ``.afterbuild/brief.json`` and ``brief.md``.
"""

from __future__ import annotations

import json
from pathlib import Path

import click
import git

# Simple language detection based on file extensions
EXT_LANG_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".go": "Go",
    ".rs": "Rust",
    ".html": "HTML",
    ".css": "CSS",
    ".md": "Markdown",
}

def _detect_languages(root: Path) -> list[str]:
    langs = set()
    for path in root.rglob("*"):
        if path.is_file():
            ext = path.suffix.lower()
            if ext in EXT_LANG_MAP:
                langs.add(EXT_LANG_MAP[ext])
    return sorted(langs)

def _find_entry_points(root: Path) -> list[str]:
    # Look for typical entry scripts (e.g., __main__.py, main.py, index.js)
    candidates = []
    for pattern in ("__main__.py", "main.py", "index.js"):
        for path in root.rglob(pattern):
            candidates.append(path.relative_to(root).as_posix())
    return sorted(candidates)

def _has_tests(root: Path) -> bool:
    return any(p for p in root.rglob("test_*.py") if p.is_file()) or any(p for p in root.rglob("*_test.py") if p.is_file())

def _git_summary(root: Path) -> dict[str, str]:
    try:
        repo = git.Repo(root, search_parent_directories=True)
        latest = repo.head.commit
        author_name = str(latest.author.name) if latest.author and latest.author.name else "Unknown"
        return {
            "latest_commit": latest.hexsha[:7],
            "author": author_name,
            "date": latest.committed_datetime.isoformat(),
        }
    except Exception:
        return {}

def _read_readme(root: Path) -> str:
    for name in ["README.md", "README.rst", "README.txt"]:
        p = root / name
        if p.is_file():
            return p.read_text(encoding="utf-8")[:200]
    return ""

def run_analyze(root: Path) -> str:
    """Perform analysis of ``root`` and write the brief files.

    Returns a short human‑readable summary printed to the console.
    """
    if not root.is_dir():
        raise click.ClickException(f"{root} is not a directory")

    languages = _detect_languages(root)
    entry_points = _find_entry_points(root)
    has_tests = _has_tests(root)
    git_info = _git_summary(root)
    readme_snippet = _read_readme(root)

    brief = {
        "languages": languages,
        "entry_points": entry_points,
        "has_tests": has_tests,
        "git": git_info,
        "readme_snippet": readme_snippet,
    }

    after_dir = root / ".afterbuild"
    after_dir.mkdir(exist_ok=True)
    (after_dir / "brief.json").write_text(json.dumps(brief, indent=2), encoding="utf-8")

    md_lines = ["# Project Brief", ""]
    md_lines.append(f"**Languages**: {', '.join(languages) or 'Unknown'}")
    md_lines.append(f"**Entry points**: {', '.join(entry_points) or 'None detected'}")
    md_lines.append(f"**Tests present**: {'Yes' if has_tests else 'No'}")
    if git_info:
        md_lines.append(f"**Latest commit**: {git_info.get('latest_commit')} by {git_info.get('author')} on {git_info.get('date')}" )
    if readme_snippet:
        md_lines.append("\n## README.md excerpt\n")
        md_lines.append(readme_snippet)
    (after_dir / "brief.md").write_text("\n".join(md_lines), encoding="utf-8")

    return f"Analysis complete. Brief written to {after_dir}"
