# Contributing to afterbuild

Thanks for your interest in contributing to afterbuild! Here's how you can help.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Install the development dependencies:

```bash
pip install -e ".[dev]"
```

## Development Workflow

1. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

2. Make your changes
3. Run the tests:

```bash
pytest
```

4. Run the linter:

```bash
ruff check .
```

5. Run type checking:

```bash
mypy .
```

## Testing

We use pytest for testing. All tests should pass before submitting a pull request.

### Test Structure

- ``tests/test_analyze.py`` – tests for the analyze command
- ``tests/test_verify.py`` – tests for the verify command
- ``tests/test_export.py`` – tests for the export command
- ``tests/test_init.py`` – tests for the init command

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Keep functions small and focused
- Write clear docstrings

## Adding a New Mode

1. Add a new markdown file in ``src/afterbuild/skill/modes/``
2. Follow the template in ``_template.md``
3. Update the ``list_modes`` function in ``modes.py`` if needed

## Adding a New Exporter

1. Add a new function in ``export/__init__.py``
2. Update the ``run_export`` function to handle the new format
3. Add tests in ``tests/test_export.py``

## Commit Messages

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Reporting Issues

If you encounter a bug or have a feature request, please open an issue on GitHub.

## Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines on conduct.
