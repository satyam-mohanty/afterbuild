"""Utility to list available document modes.

The modes are stored as markdown files inside the package data directory
``afterbuild/skill/modes/``. ``list_modes`` returns the stem (file name
without extension) of each ``*.md`` file found there.
"""

from __future__ import annotations

import importlib.resources as pkg_resources
from pathlib import Path

def list_modes() -> list[str]:
    """Return a list of mode names shipped with the package."""
    try:
        # ``afterbuild.skill.modes`` is a package containing the markdown files
        with pkg_resources.files("afterbuild.skill.modes").as_file() as modes_path:
            return [p.stem for p in Path(modes_path).glob("*.md")]
    except Exception:
        # If resources are not available (e.g., during development) fall back to a static list
        return ["product-docs", "technical-docs", "research-report", "storytelling", "case-study"]
