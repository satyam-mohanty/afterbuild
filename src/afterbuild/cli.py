"""Entry point for the afterbuild CLI.

The CLI provides the following sub‑commands:

* ``analyze`` – generate a brief description of the repository.
* ``verify``  – check links and code references in a draft.
* ``export``  – render a draft to markdown, docx or pdf.
* ``modes``   – list available document modes.
* ``doctor``  – run environment checks.
* ``init`` / ``update`` / ``uninstall`` – manage the bundled Claude skill.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from . import analyze, verify, export, modes, init_cmd

@click.group()
def main() -> None:
    """Top‑level command group for afterbuild."""


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".")
def analyze_cmd(path: Path) -> None:
    """Analyze a repository and write a brief.

    ``PATH`` is the root of the project to analyse. The command creates a
    ``.afterbuild`` directory inside ``PATH`` containing ``brief.json`` and
    ``brief.md``.
    """
    result = analyze.run_analyze(path)
    click.echo(result)


@main.command()
@click.argument("draft", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("path", type=click.Path(exists=True, file_okay=False, path_type=Path), required=False)
def verify_cmd(draft: Path, path: Path | None = None) -> None:
    """Verify a draft file.

    ``DRAFT`` is the markdown file to verify. ``PATH`` optionally points to the
    repository the draft refers to; if omitted the current working directory is
    used.
    """
    exit_code = verify.run_verify(draft, path or Path.cwd())
    sys.exit(exit_code)


@main.command()
@click.argument("draft", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--to", "to_format", type=click.Choice(["md", "docx", "pdf"]), required=True, help="Output format")
@click.option("--out", "out_dir", type=click.Path(file_okay=False, path_type=Path), default="docs", help="Output directory")
def export_cmd(draft: Path, to_format: str, out_dir: Path) -> None:
    """Export a draft to the requested format.

    The command writes the result into ``OUT_DIR`` (created if necessary).
    """
    out_path = export.run_export(draft, to_format, out_dir)
    click.echo(f"Exported to {out_path}")


@main.command()
def modes_cmd() -> None:
    """List the document modes shipped with the package."""
    for mode in modes.list_modes():
        click.echo(mode)


@main.command()
def doctor() -> None:
    """Run a quick environment health‑check."""
    click.echo("Running doctor checks…")
    # Very lightweight checks – real implementation lives in ``doctor`` module.
    from . import doctor as doc_mod

    issues = doc_mod.run_checks()
    if not issues:
        click.echo("All checks passed.")
    else:
        click.echo("Issues detected:")
        for i in issues:
            click.echo(f"- {i}")


# Skill management commands – thin wrappers around ``init_cmd``
@main.command(name="init")
@click.argument("target", type=click.Choice(["claude", "agents", "cursor"]))
@click.option("--force", is_flag=True, help="Overwrite existing files.")
def init(target: str, force: bool) -> None:
    """Install the bundled Claude skill into the current project."""
    init_cmd.run_init(Path.cwd(), target, force)


@main.command(name="update")
@click.argument("target", type=click.Choice(["claude", "agents", "cursor"]))
def update(target: str) -> None:
    """Update an existing skill installation to the version shipped with the CLI."""
    init_cmd.run_update(Path.cwd(), target)


@main.command(name="uninstall")
@click.argument("target", type=click.Choice(["claude", "agents", "cursor"]))
def uninstall(target: str) -> None:
    """Remove the installed skill files for ``TARGET``."""
    init_cmd.run_uninstall(Path.cwd(), target)


if __name__ == "__main__":
    main()
