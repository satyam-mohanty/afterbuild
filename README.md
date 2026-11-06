# afterbuild

Turn a finished codebase into a polished document (docs, technical report, storytelling, case study).


## Install

```bash
pip install git+https://github.com/satyam-mohanty/afterbuild
# or
pipx install git+https://github.com/satyam-mohanty/afterbuild
# or
uvx --from git+https://github.com/satyam-mohanty/afterbuild install afterbuild
```

## Usage

### 1. Initialize the skill

```bash
cd your-project
afterbuild init --target claude
```

### 2. Analyze your project

```bash
afterbuild analyze
```

### 3. Follow the skill prompts

The skill will guide you through choosing a document type and crafting your document.

### 4. Export your document

```bash
afterbuild export draft.md --to md --out docs/
```

## Supported Modes

| Mode               | Description                          | Target Audience          |
|--------------------|--------------------------------------|--------------------------|
| product-docs      | User-friendly documentation  | End users              |
| technical-docs    | Developer-focused documentation | Developers             |
| research-report    | Structured research report       | Researchers             |
| storytelling       | Narrative journey of building    | General audience        |
| case-study         | Retrospective analysis           | Professionals           |

## How Verify Works

The ``afterbuild verify`` command checks:

- All hyperlinks are reachable
- Code references (file paths, function names) exist in the repo
- CLI flags are documented in config files

## Supported Targets

| Target   | Description                          |
|----------|--------------------------------------|
| claude   | Installs into `.claude/skills/afterbuild/` |
| agents   | Adds a section to `AGENTS.md`       |
| cursor   | Writes to `.cursor/rules/afterbuild.mdc` |

## How to Add a Mode

1. Add a new markdown file in `src/afterbuild/skill/modes/`
2. Follow the template in `_template.md`
3. The file name becomes the mode name

## Roadmap

- [ ] Add more exporter backends
- [ ] Support more programming languages
- [ ] Add interactive mode selection
- [ ] Improve verification for complex code references

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
