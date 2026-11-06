"""Skill installation commands.

The ``run_init`` function copies the bundled skill markdown files into the
target project according to the chosen ``target`` (``claude``, ``agents``
or ``cursor``). ``run_update`` rescues the same files from the package and
overwrites the existing ones. ``run_uninstall`` removes the files that were
installed for the given target.

All file operations respect the ``--force`` flag – without it the command
will abort if any destination already exists.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import click

# Mapping from target to destination relative to the project root
TARGET_PATHS = {
    "claude": Path(".claude/skills/afterbuild"),
    "agents": Path("AGENTS.md"),  # simplified – we will write a section into the file
    "cursor": Path(".cursor/rules/afterbuild.mdc"),
}

def _resource_path(subdir: str) -> Path:
    """Return the path to the packaged skill resources.

    ``subdir`` is relative to the ``afterbuild/skill`` package directory.
    During development we locate the files on disk; when installed as a
    wheel ``importlib.resources`` would be used.
    """
    # The source lives in the repository under ``src/afterbuild/skill``
    base = Path(__file__).parent.parent / "skill"
    return base / subdir

def _copy_skill(src_dir: Path, dest_dir: Path, force: bool) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in src_dir.iterdir():
        dest_path = dest_dir / item.name
        if dest_path.exists() and not force:
            raise click.ClickException(f"{dest_path} already exists – use --force to overwrite")
        if item.is_dir():
            shutil.copytree(item, dest_path, dirs_exist_ok=force)
        else:
            shutil.copy2(item, dest_path)

def run_init(project_root: Path, target: str, force: bool) -> None:
    """Install the skill for ``target`` into ``project_root``.

    ``target`` must be one of ``claude``, ``agents`` or ``cursor``.
    ``force`` allows overwriting existing files.
    """
    if target not in TARGET_PATHS:
        raise click.ClickException(f"Unknown target: {target}")

    dest = project_root / TARGET_PATHS[target]
    if target == "claude":
        src = _resource_path("")
        _copy_skill(src, dest, force)
    elif target == "agents":
        # For agents we just append a section to AGENTS.md (or create it)
        src = _resource_path("SKILL.md")
        dest_parent = project_root
        ag_file = dest_parent / "AGENTS.md"
        if ag_file.exists() and not force:
            raise click.ClickException("AGENTS.md already exists – use --force to append")
        content = src.read_text(encoding="utf-8")
        with ag_file.open("a", encoding="utf-8") as f:
            f.write("\n\n" + content)
    elif target == "cursor":
        src = _resource_path("SKILL.md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not force:
            raise click.ClickException(f"{dest} already exists – use --force to overwrite")
        shutil.copy2(src, dest)

    # Ensure .afterbuild/ is ignored by git
    gitignore = project_root / ".gitignore"
    entry = "/.afterbuild/"
    if gitignore.is_file():
        lines = gitignore.read_text().splitlines()
        if entry not in lines:
            gitignore.write_text("\n".join(lines + [entry]) + "\n", encoding="utf-8")
    else:
        gitignore.write_text(entry + "\n", encoding="utf-8")

    click.echo(f"Skill installed for {target} at {dest}")
    click.echo("Next step: run `afterbuild analyze` and follow the skill prompts.")


def run_update(project_root: Path, target: str) -> None:
    """Refresh an existing installation with the latest packaged files."""
    # For simplicity we delegate to ``run_init`` with ``force=True`` – the user
    # explicitly asked for an update.
    run_init(project_root, target, force=True)


def run_uninstall(project_root: Path, target: str) -> None:
    """Remove the skill files for ``target`` from ``project_root``."""
    if target not in TARGET_PATHS:
        raise click.ClickException(f"Unknown target: {target}")
    dest = project_root / TARGET_PATHS[target]
    if dest.is_dir():
        shutil.rmtree(dest)
        click.echo(f"Removed directory {dest}")
    elif dest.is_file():
        dest.unlink()
        click.echo(f"Removed file {dest}")
    else:
        click.echo(f"Nothing to remove for {target}")
