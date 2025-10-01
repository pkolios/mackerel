# Mackerel

[![PyPI](https://img.shields.io/pypi/v/mackerel.svg)](https://pypi.org/project/mackerel/)
[![CI](https://github.com/pkolios/mackerel/actions/workflows/ci.yml/badge.svg)](https://github.com/pkolios/mackerel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![codecov](https://codecov.io/gh/pkolios/mackerel/branch/main/graph/badge.svg)](https://codecov.io/gh/pkolios/mackerel)

A minimal static site generator written in typed Python.
This README is for **developers** contributing to Mackerel. For end-user documentation, see [docs](https://mackerel.sh).

---

## Development Setup

Clone the repo and set up dependencies:

```bash
git clone https://github.com/pkolios/mackerel.git
cd mackerel
uv sync
````

Run tests:

```bash
make test
```

Lint & type check:

```bash
make lint
```

Build docs:

```bash
make docs
```

---

## Codebase Structure

```
src/mackerel/
├── build.py        # Build logic
├── cli.py          # CLI (init, build, develop)
├── config.py       # Configuration loading
├── parsers.py      # Front matter parsing
├── renderers.py    # Markdown + Jinja2 rendering
├── site/           # Starter site (templates + content)
└── types.py        # Typed core types & protocols
```

* **Functional Core, Imperative Shell**: Business logic is pure and typed, orchestration happens in CLI.
* **Minimal dependencies**: Keeping the cli installation time as fast as possible.

---

## Contributing

1. Fork the repo & create a branch.
2. Write tests for new features.
3. Ensure `make lint test` passes.
4. Submit a PR.

We follow **strict typing** (`mypy`, `pyright`) and **ruff** for linting.
Docs are in `docs/`.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

---

## License

MIT © Paris Kolios
