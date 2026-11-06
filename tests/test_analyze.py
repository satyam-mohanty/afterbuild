import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from afterbuild.cli import main

def test_analyze_basic(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["analyze", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert (tmp_path / ".afterbuild").is_dir()
    assert (tmp_path / ".afterbuild/brief.json").is_file()
    assert (tmp_path / ".afterbuild/brief.md").is_file()

def test_analyze_empty_dir(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["analyze", str(tmp_path)])
    assert result.exit_code == 0
    brief_json = (tmp_path / ".afterbuild/brief.json").read_text()
    assert "Unknown" in brief_json

def test_analyze_with_files(tmp_path: Path) -> None:
    # Add some files
    (tmp_path / "src").mkdir()
    (tmp_path / "src/main.py").write_text("print('Hello')\n")
    (tmp_path / "README.md").write_text("# My Project\n")

    runner = CliRunner()
    result = runner.invoke(main, ["analyze", str(tmp_path)])
    assert result.exit_code == 0
    brief_md = (tmp_path / ".afterbuild/brief.md").read_text()
    assert "Python" in brief_md
    assert "src/main.py" in brief_md
    assert "README.md" in brief_md

def test_analyze_no_git(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["analyze", str(tmp_path)])
    assert result.exit_code == 0
    brief_json = (tmp_path / ".afterbuild/brief.json").read_text()
    assert "git" not in brief_json or not brief_json["git"]

def test_analyze_with_git(tmp_path: Path) -> None:
    from git import Repo
    Repo.init(tmp_path)
    (tmp_path / "test_file.txt").write_text("content")
    repo = Repo(tmp_path)
    repo.index.add(["test_file.txt"])
    repo.index.commit("Initial commit")

    runner = CliRunner()
    result = runner.invoke(main, ["analyze", str(tmp_path)])
    assert result.exit_code == 0
    brief_json = (tmp_path / ".afterbuild/brief.json").read_text()
    assert "git" in brief_json
    assert "latest_commit" in brief_json["git"]
