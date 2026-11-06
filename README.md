# afterbuild

[![CI](https://github.com/satyam-mohanty/afterbuild/actions/workflows/ci.yml/badge.svg)](https://github.com/satyam-mohanty/afterbuild/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Turn finished codebases into polished docs, reports, and case studies.**

`afterbuild` inspects a finished codebase and guides you (or your AI agent) through generating publication-ready documentation, architecture overviews, developer guides, research reports, engineering case studies, or dev narratives.

---

## Features

- 🧠 **Agent & Skill Native**: Integrates seamlessly with Claude Code, Cursor Rules, or custom agent setups.
- 🔍 **Automated Codebase Analysis**: Deep-scans language stats, entrypoints, Git history, modules, and config flags.
- 🎭 **Targeted Output Modes**: Switch between developer docs, end-user manuals, technical post-mortems, and engineering storytelling.
- ✅ **Built-in Fact Verification (`afterbuild verify`)**: Validates hyperlinks, CLI flags, and ensures referenced files and symbols actually exist in the codebase.
- 📦 **Multi-Format Export**: Export drafts cleanly to Markdown, HTML, PDF, or DOCX.

---

## Installation & Agent Setup

### ⚡ Zero-Install Prompt (Use directly with your LLM / Agent)

You don't even need to install the CLI command. Just copy and paste this prompt directly into your AI chat (Claude Code, Cursor, Windsurf, Copilot, or ChatGPT):

```text
Please read the afterbuild skill directly from GitHub and install it into this workspace:
- Fetch and copy the skill files from https://github.com/satyam-mohanty/afterbuild/tree/main/src/afterbuild/skill
- For Claude Code: place under .claude/skills/afterbuild/
- For Cursor: place under .cursor/rules/afterbuild.mdc
- For other agents: append the SKILL.md content into AGENTS.md

Once added, guide me through creating documentation for this repository.
```

---

### 🤖 LLM Prompt (With CLI & Verification Support)

If you want the full power of `afterbuild verify` (checks for hallucinated code references, broken links, and missing flags) and document export:

```text
Please install the afterbuild tool and initialize it for this project:
1. Run: pip install git+https://github.com/satyam-mohanty/afterbuild
2. Initialize the skill for our editor: afterbuild init --target claude (or cursor/agents)
3. Run: afterbuild analyze
```

---

### 💻 Manual CLI Installation

If you prefer installing the CLI yourself:

**pip**
```bash
pip install git+https://github.com/satyam-mohanty/afterbuild
```

**pipx** (recommended for isolated CLI usage)
```bash
pipx install git+https://github.com/satyam-mohanty/afterbuild
```

**uv / uvx**
```bash
uvx --from git+https://github.com/satyam-mohanty/afterbuild install afterbuild
```

---

## Quickstart

### 1. Initialize for your AI workflow

Run this in your target project root to attach the `afterbuild` skill:

```bash
cd your-project

# For Claude Code (.claude/skills/afterbuild/)
afterbuild init --target claude

# For Cursor (.cursor/rules/afterbuild.mdc)
afterbuild init --target cursor

# For generic agent specs (appends to AGENTS.md)
afterbuild init --target agents
```

### 2. Analyze the project

Extract codebase structure, key components, dependencies, and metadata:

```bash
afterbuild analyze
```

### 3. Draft with your AI agent

Use the installed skill in your editor/terminal to create a draft tailored to your chosen mode.

### 4. Verify references

Ensure the generated documentation didn't hallucinate non-existent files, broken links, or missing CLI arguments:

```bash
afterbuild verify draft.md
```

### 5. Export

Convert the draft into your desired format:

```bash
# Export to Markdown, HTML, PDF, or DOCX
afterbuild export draft.md --to md --out docs/
afterbuild export draft.md --to html --out dist/
afterbuild export draft.md --to pdf --out dist/
```

---

## Supported Modes

| Mode | Description | Target Audience |
| :--- | :--- | :--- |
| `product-docs` | Clear, user-friendly guides and manuals | End users & customers |
| `technical-docs` | Architecture deep-dives, APIs, and workflows | Developers & contributors |
| `research-report` | Structured scientific / algorithmic write-ups | Researchers & engineers |
| `storytelling` | The narrative behind building the project | Community & blog readers |
| `case-study` | Retrospective, engineering trade-offs, and outcomes | Leaders & professionals |

---

## Adding Custom Modes

1. Add a new markdown template in `src/afterbuild/skill/modes/`.
2. Follow the structure in `src/afterbuild/skill/modes/_template.md`.
3. The filename automatically defines the new mode name.

---

## Development

```bash
git clone https://github.com/satyam-mohanty/afterbuild.git
cd afterbuild
pip install -e ".[dev]"

# Run tests
pytest

# Lint and format
ruff check .
```

---

## Contributing

Contributions, issues, and feature suggestions are welcome! Check out [CONTRIBUTING.md](CONTRIBUTING.md) and our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Distributed under the [MIT License](LICENSE).
