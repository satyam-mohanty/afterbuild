import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from afterbuild.cli import main

def test_verify_valid_links(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("[Valid](https://example.com)\n")
    runner = CliRunner()
    result = runner.invoke(main, ["verify", str(draft)])
    assert result.exit_code == 0, result.output
    assert "All checks passed" in result.output

def test_verify_broken_link(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("[Broken](https://this.url.does.not.exist)\n")
    runner = CliRunner()
    result = runner.invoke(main, ["verify", str(draft)])
    assert result.exit_code == 1
    assert "Broken link" in result.output

def test_verify_missing_file(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("See `src/missing.py`\n")
    runner = CliRunner()
    result = runner.invoke(main, ["verify", str(draft), str(tmp_path)])
    assert result.exit_code == 1
    assert "Referenced file not found" in result.output

def test_verify_missing_function(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src/main.py").write_text("def existing_func():\n    pass\n")
    draft = tmp_path / "draft.md"
    draft.write_text("Call `missing_func()` in `src/main.py`\n")
    runner = CliRunner()
    result = runner.invoke(main, ["verify", str(draft), str(tmp_path)])
    assert result.exit_code == 1
    assert "Referenced function not found" in result.output

def test_verify_valid_function(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src/main.py").write_text("def present_func():\n    pass\n")
    draft = tmp_path / "draft.md"
    draft.write_text("Call `present_func()` in `src/main.py`\n")
    runner = CliRunner()
    result = runner.invoke(main, ["verify", str(draft), str(tmp_path)])
    assert result.exit_code == 0
    assert "All checks passed" in result.output
