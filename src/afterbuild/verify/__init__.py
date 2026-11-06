"""Verification command implementation.

The ``run_verify`` function checks a draft markdown file for:

1. Hyperlinks – whether they are reachable (HTTP 200) and not redirected
   to an error page.
2. Inline code references – simple ``file_path`` patterns and ``function``
   names. The function confirms that the referenced file exists in the
   repository and, for a function name, that the name appears in the file.
3. CLI flags – patterns like ``--flag`` are looked up in the project's
   ``setup.cfg``/``pyproject.toml`` or ``package.json`` where applicable.

The function prints a short report and returns ``0`` on success or ``1``
if any problem was found. It is deliberately lightweight – a full
production‑grade verifier would need more sophisticated parsing.
"""

from __future__ import annotations

import re
from pathlib import Path

import click
import requests

# Simple regexes
_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
_CODE_REF_RE = re.compile(r"`([^`]+)`")  # back‑ticked snippets
_FLAG_RE = re.compile(r"--[A-Za-z0-9_-]+")


def _check_link(url: str) -> tuple[bool, str]:
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        if resp.status_code == 200:
            return True, ""
        return False, f"Status {resp.status_code}"
    except Exception as e:
        return False, str(e)


def _file_exists(repo_root: Path, path_str: str) -> bool:
    return (repo_root / path_str).exists()


def _function_in_file(file_path: Path, func_name: str) -> bool:
    if not file_path.is_file():
        return False
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return False
    # Very naive: look for "def name" or "function name" patterns
    pattern = re.compile(r"(def|function)\s+" + re.escape(func_name) + r"\b")
    return bool(pattern.search(content))


def run_verify(draft_path: Path, repo_root: Path) -> int:
    """Verify a markdown draft.

    Returns ``0`` if everything looks good, ``1`` otherwise.
    """
    if not draft_path.is_file():
        raise click.ClickException(f"Draft file {draft_path} not found")

    text = draft_path.read_text(encoding="utf-8")
    issues: list[str] = []

    # 1. Links
    for label, url in _LINK_RE.findall(text):
        ok, msg = _check_link(url)
        if not ok:
            issues.append(f"Broken link [{label}]({url}): {msg}")

    # 2. Code references – we treat any back‑ticked token that looks like a path or function
    for token in _CODE_REF_RE.findall(text):
        # Path detection – contains a slash or ends with a known extension
        if "/" in token or any(token.endswith(ext) for ext in [".py", ".js", ".ts", ".java", ".go"]):
            if not _file_exists(repo_root, token):
                issues.append(f"Referenced file not found: `{token}`")
        else:
            # Check if this looks like a function name or function call (e.g. `foo()` or `foo_bar`)
            func_name = token.removesuffix("()")
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", func_name):
                continue
            # Assume function name – search in all source files
            found = False
            for p in repo_root.rglob("*.*"):
                if p.suffix.lower() in {".py", ".js", ".ts", ".java", ".go", ".cpp", ".c", ".rs"}:
                    if _function_in_file(p, func_name):
                        found = True
                        break
            if not found:
                issues.append(f"Referenced function not found: `{token}`")

    # 3. CLI flags – very naive check against common config files
    flags = set(_FLAG_RE.findall(text))
    if flags:
        # Look for flags in pyproject.toml or package.json as a simple heuristic
        config_files = [repo_root / "pyproject.toml", repo_root / "package.json"]
        config_text = "\n".join([cf.read_text(errors="ignore") for cf in config_files if cf.is_file()])
        for flag in flags:
            if flag not in config_text:
                issues.append(f"Flag {flag} not documented in config files")

    if issues:
        click.echo("Verification issues found:")
        for i in issues:
            click.echo(f"- {i}")
        return 1
    else:
        click.echo("All checks passed.")
        return 0
