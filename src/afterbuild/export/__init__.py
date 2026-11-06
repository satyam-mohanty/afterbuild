"""Export command implementation.

The ``run_export`` function takes a markdown draft and renders it to the
requested format using Pandoc when available. If Pandoc is missing it falls
back to ``python-docx`` for DOCX and ``weasyprint`` for PDF. The output is
written into the supplied ``out_dir`` (created if needed) and the path to
the generated file is returned.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

import click


def _run_pandoc(input_md: Path, out_path: Path, fmt: str) -> bool:
    """Run pandoc to convert ``input_md`` to ``fmt``.

    Returns ``True`` on success, ``False`` otherwise.
    """
    try:
        subprocess.run([
            "pandoc",
            str(input_md),
            "-o",
            str(out_path),
        ], check=True)
        return True
    except Exception:
        return False


def _fallback_docx(input_md: Path, out_path: Path) -> bool:
    try:
        from docx import Document
        doc = Document()
        # Very naive: each line becomes a paragraph
        for line in input_md.read_text(encoding="utf-8").splitlines():
            doc.add_paragraph(line)
        doc.save(out_path)
        return True
    except Exception:
        return False


def _fallback_pdf(input_md: Path, out_path: Path) -> bool:
    try:
        from weasyprint import HTML
        html = HTML(string=markdown_to_html(input_md.read_text(encoding="utf-8")))
        html.write_pdf(out_path)
        return True
    except Exception:
        return False


def markdown_to_html(md: str) -> str:
    """Very small markdown → HTML conversion for PDF fallback.

    Uses the built‑in ``markdown`` module if available, otherwise a trivial
    replacement that wraps the text in ``<pre>``.
    """
    try:
        import markdown
        return markdown.markdown(md)
    except Exception:
        return f"<pre>{md}</pre>"


def run_export(draft: Path, fmt: str, out_dir: Path) -> Path:
    """Export ``draft`` to ``fmt`` (md, docx, pdf) inside ``out_dir``.

    Returns the full path to the generated file.
    """
    if fmt not in {"md", "docx", "pdf"}:
        raise click.ClickException(f"Unsupported format: {fmt}")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{draft.stem}.{fmt}"

    if fmt == "md":
        # Simple copy
        shutil.copyfile(draft, out_path)
        return out_path

    # Try pandoc first
    if shutil.which("pandoc"):
        if _run_pandoc(draft, out_path, fmt):
            return out_path
        click.echo("Pandoc failed – falling back to pure‑Python converters.")

    # Fallbacks
    if fmt == "docx":
        if _fallback_docx(draft, out_path):
            return out_path
    elif fmt == "pdf":
        if _fallback_pdf(draft, out_path):
            return out_path

    raise click.ClickException(f"Could not export to {fmt}. Install pandoc or the required Python packages.")
