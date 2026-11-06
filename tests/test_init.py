from pathlib import Path

from click.testing import CliRunner

from afterbuild.cli import main


def test_init_claude(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["init", "claude", "--force"])
    assert result.exit_code == 0, result.output
    skill_dir = tmp_path / ".claude/skills/afterbuild"
    assert skill_dir.is_dir()
    assert (skill_dir / "SKILL.md").is_file()

def test_init_agents(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["init", "agents", "--force"])
    assert result.exit_code == 0
    assert (tmp_path / "AGENTS.md").is_file()

def test_init_cursor(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["init", "cursor", "--force"])
    assert result.exit_code == 0
    assert (tmp_path / ".cursor/rules/afterbuild.mdc").is_file()

def test_init_no_force(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    # Create an empty file in the target path
    (tmp_path / ".claude/skills/afterbuild").mkdir(parents=True)
    (tmp_path / ".claude/skills/afterbuild/dummy").touch()
    runner = CliRunner()
    result = runner.invoke(main, ["init", "claude"])
    assert result.exit_code != 0
    assert "already exists" in result.output

def test_uninstall(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    # Install first
    runner = CliRunner()
    runner.invoke(main, ["init", "claude", "--force"])
    skill_dir = tmp_path / ".claude/skills/afterbuild"
    assert skill_dir.is_dir()
    # Uninstall
    result = runner.invoke(main, ["uninstall", "claude"])
    assert result.exit_code == 0
    assert not skill_dir.exists()
