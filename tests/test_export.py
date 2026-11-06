import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from afterbuild.cli import main

def test_export_md(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("# Test\n")
    runner = CliRunner()
    result = runner.invoke(main, ["export", str(draft), "--to", "md", "--out", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / "draft.md").exists()

def test_export_docx(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("# Test\n")
    runner = CliRunner()
    result = runner.invoke(main, ["export", str(draft), "--to", "docx", "--out", str(tmp_path)])
    assert result.exit_code == 0 or "pandoc" in result.output
    if result.exit_code == 0:
        assert (tmp_path / "draft.docx").exists()

def test_export_pdf(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("# Test\n")
    runner = CliRunner()
    result = runner.invoke(main, ["export", str(draft), "--to", "pdf", "--out", str(tmp_path)])
    assert result.exit_code == 0 or "pandoc" in result.output

def test_export_invalid_format(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("# Test\n")
    runner = CliRunner()
    result = runner.invoke(main, ["export", str(draft), "--to", "html", "--out", str(tmp_path)])
    assert result.exit_code != 0
    assert "Unsupported format" in result.output
