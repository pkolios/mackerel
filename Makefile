# Variables

.DEFAULT_GOAL:=help
.ONESHELL:
ENV_PREFIX = .venv/bin/
VENV_EXISTS = $(shell python3 -c "if __import__('pathlib').Path('.venv/bin/activate').exists(): print('yes')")

.EXPORT_ALL_VARIABLES:


.PHONY: help
help:              ## Display this help text for Makefile
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: upgrade
upgrade:           ## Upgrade all dependencies to the latest stable versions
	@echo "=> Updating all dependencies"
	@uv lock --upgrade
	@echo "=> Updating Pre-commit"
	@uv run pre-commit autoupdate

# Setup & Environment

.PHONY: install
install:           ## Install dependencies
	@echo "=> Installing dependencies"
	uv sync

.PHONY: lock
lock:              ## Regenerate lockfile from pyproject.toml
	@echo "=> Regenerating lockfile"
	uv lock

.PHONY: clean
clean:            ## Clean build, test, and cache artifacts
	@echo "=> Cleaning artifacts"
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name '*.egg' -delete
	find . -name '*.egg-info' -type d -exec rm -rf {} +

.PHONY: destroy
destroy:          ## Remove the virtual environment
	@echo "=> Removing virtual environment"
	rm -rf .venv

# Checks

.PHONY: mypy
mypy:             ## Run mypy type checks
	@echo "=> Running mypy"
	uv run mypy src

.PHONY: pyright
pyright:          ## Run pyright type checks
	@echo "=> Running pyright"
	uv run pyright

.PHONY: type-check
type-check: mypy pyright    ## Run all type checking

.PHONY: pre-commit
pre-commit:       ## Runs pre-commit hooks; includes ruff formatting and linting
	@echo "=> Running pre-commit process"
	@uv run pre-commit run --all-files

.PHONY: deptry
deptry:          ## Run dependency checks with deptry
	@echo "=> Running dependency checks"
	@uv run deptry .

.PHONY: lint
lint: pre-commit type-check deptry     ## Run all linting

# Tests

.PHONY: test
test:            ## Run tests
	@echo "=> Running tests"
	uv run pytest -v --cov=mackerel --cov-report=xml

# Docs

.PHONY: docs
docs: docs-clean  ## Clean and build docs
	@echo "=> Building documentation"
	PYTHONPATH=$$PYTHONPATH:$(pwd) uv run mackerel build --config docs/mackerelconfig.toml

.PHONY: docs-clean
docs-clean:      ## Clean built documentation
	@echo "=> Cleaning docs build artifacts"
	rm -rf docs/_build

# Build

.PHONY: build
build: clean     ## Build the package
	@echo "=> Building the package"
	uv pip install --upgrade build
	uv run python -m build
