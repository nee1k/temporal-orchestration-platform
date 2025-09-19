# Contributing

Thanks for your interest in contributing! This repository demonstrates a production-grade Temporal platform.

## Development Setup
- Python 3.11+
- Create a virtualenv: `python3.11 -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -e workflows[dev]`
- Lint/type/test: `make lint type test`

## Commit Structure
- Small, single-purpose commits with clear messages
- Conventional commits are encouraged: `feat:`, `fix:`, `docs:`, `chore:`, etc.

## Pull Requests
- Include tests for changes
- Ensure CI is green (ruff, mypy, pytest)
- Update docs if behavior changes

## Security
- Don’t commit secrets. See SECURITY.md for reporting vulnerabilities.
