"""Environment health‑checks for afterbuild.

The ``run_checks`` function verifies that all required tools and Python
packages are installed and available. Returns a list of issue strings.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

def run_checks() -> list[str]:
    """Run a quick environment check and return any issues found."""
    issues = []

    # Python version
    if sys.version_info < (3, 10):
        issues.append("Python 3.10+ required")

    # Required Python packages
    required = ["click", "rich", "requests", "GitPython", "pydantic"]
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            issues.append(f"Missing Python package: {pkg}")

    # External tools
    tools = ["pandoc"]
    for tool in tools:
        if shutil.which(tool) is None:
            issues.append(f"Missing command: {tool}")

    return issues

# Import shutil here to avoid early import if not needed
import shutil