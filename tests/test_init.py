import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from afterbuild.cli import main

def test_init_claude(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["init", "claude", "--force"], cwd=tmp_path)
    assert result.exit_code == 0, result.output
    skill_dir = tmp_path / ".claude/skills/afterbuild"
    assert skill_dir.is_dir()
    assert (skill_dir / "SKILL.md").is_file()

def test_init_agents(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["init", "agents", "--force"], cwd=tmp_path)
    assert result.exit_code == 0
    assert (tmp_path / "AGENTS.md").is_file()

def test_init_cursor(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["init", "cursor", "--force"], cwd=tmp_path)
    assert result.exit_code == 0
    assert (tmp_path / ".cursor/rules/afterbuild.mdc").is_file()

def test_init_no_force(tmp_path: Path) -> None:
    # Create an empty file in the target path
    (tmp_path / ".claude/skills/afterbuild").mkdir(parents=True)
    (tmp_path / ".claude/skills/afterbuild/dummy").touch()
    runner = CliRunner()
    result = runner.invoke(main, ["init", "claude"], cwd=tmp_path)
    assert result.exit_code != 0
    assert "already exists" in result.output

def test_uninstall(tmp_path: Path) -> None:
    # Install first
    runner = CliRunner()
    runner.invoke(main, ["init", "claude", "--force"], cwd=tmp_path)
    skill_dir = tmp_path / ".claude/skills/afterbuild"
    assert skill_dir.is_dir()
    # Uninstall
    result = runner.invoke(main, ["uninstall", "claude"], cwd=tmp_path)
    assert result.exit_code == 0
    assert not skill_dir.exists()
