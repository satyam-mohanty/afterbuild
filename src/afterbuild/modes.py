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
        modes_ref = pkg_resources.files("afterbuild.skill.modes")
        with pkg_resources.as_file(modes_ref) as modes_path:
            return sorted(
                p.stem
                for p in Path(modes_path).glob("*.md")
                if not p.name.startswith("_")
            )
    except Exception:
        # If resources are not available (e.g., during development) fall back to a static list
        return ["case-study", "product-docs", "research-report", "storytelling", "technical-docs"]
