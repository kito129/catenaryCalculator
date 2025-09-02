.PHONY: help venv venv-clean setup install run test lint format check clean add add-dev remove update lock uv-run commit bump-patch bump-minor bump-major

# Default target
help:
	@echo "Available commands:"
	@echo "  venv      - Create Python virtual environment"
	@echo "  venv-clean- Remove Python virtual environment"
	@echo "  setup     - Setup development environment"
	@echo "  install   - Install/sync dependencies"
	@echo "  run       - Run the main application"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting with flake8"
	@echo "  format    - Format code with black"
	@echo "  check     - Run all checks (lint + test)"
	@echo "  clean     - Clean up temporary files and cache"
	@echo "  add       - Add a new dependency (use: make add PACKAGE=package_name)"
	@echo "  add-dev   - Add a development dependency (use: make add-dev PACKAGE=package_name)"
	@echo "  remove    - Remove a dependency (use: make remove PACKAGE=package_name)"
	@echo "  update    - Update dependencies"
	@echo "  lock      - Create/update lock file"
	@echo "  uv-run    - Run any command in project environment (use: make uv-run CMD='command')"
	@echo "  commit    - Create a conventional commit using commitizen"
	@echo "  bump-patch- Bump patch version (1.1.0 -> 1.1.1)"
	@echo "  bump-minor- Bump minor version (1.1.0 -> 1.2.0)"
	@echo "  bump-major- Bump major version (1.1.0 -> 2.0.0)"
	@echo "  uv-run    - Run any command in project environment (use: make uv-run CMD='command')"

# Create Python virtual environment
venv:
	@echo "Creating Python virtual environment..."
	@if [ -d ".venv" ]; then \
		echo "Virtual environment already exists. Use 'make venv-clean' to remove it first."; \
	else \
		python3.13 -m venv .venv; \
		echo "Virtual environment created successfully!"; \
		echo "To activate it, run: source .venv/bin/activate"; \
	fi

# Remove Python virtual environment
venv-clean:
	@echo "Removing Python virtual environment..."
	@if [ -d ".venv" ]; then \
		rm -rf .venv; \
		echo "Virtual environment removed successfully!"; \
	else \
		echo "No virtual environment found."; \
	fi

# Setup development environment
setup: venv
	@echo "Setting up development environment..."
	@echo "Installing uv..."
	@if [ -f ".venv/bin/python" ]; then \
		.venv/bin/pip install uv; \
	else \
		pip install uv; \
	fi
	uv init --no-readme --no-workspace
	uv add --dev flake8 pre-commit pytest ruff black
	uv run pre-commit install
	@echo ""
	@echo "Development environment setup complete!"
	@echo "To activate the virtual environment, run: source .venv/bin/activate"
	@echo "Or use uv commands directly: uv run <command>"

# Install/sync dependencies
install:
	@echo "Installing dependencies..."
	uv sync --dev

# Run the main application
run:
	@echo "Running the catenary calculator..."
	uv run python main.py

# Run tests
test:
	@echo "Running tests..."
	uv run pytest -v

# Run linting
lint:
	@echo "Running linting checks..."
	uv run flake8 .
	uv run ruff check .

# Format code
format:
	@echo "Formatting code..."
	uv run black .
	uv run ruff format .

# Run all checks
check: lint test
	@echo "All checks completed!"

# Clean up temporary files and cache
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete!"

# Add a new dependency
add:
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make add PACKAGE=package_name"; \
		exit 1; \
	fi
	@echo "Adding package: $(PACKAGE)"
	uv add $(PACKAGE)

# Add a development dependency
add-dev:
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make add-dev PACKAGE=package_name"; \
		exit 1; \
	fi
	@echo "Adding development package: $(PACKAGE)"
	uv add --dev $(PACKAGE)

# Remove a dependency
remove:
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make remove PACKAGE=package_name"; \
		exit 1; \
	fi
	@echo "Removing package: $(PACKAGE)"
	uv remove $(PACKAGE)

# Update dependencies
update:
	@echo "Updating dependencies..."
	uv sync --upgrade

# Create/update lock file
lock:
	@echo "Creating/updating lock file..."
	uv lock

# Run any command in the project environment
uv-run:
	@if [ -z "$(CMD)" ]; then \
		echo "Usage: make uv-run CMD='command'"; \
		echo "Example: make uv-run CMD='python -c \"print(1+1)\"'"; \
		exit 1; \
	fi
	@echo "Running: $(CMD)"
	uv run $(CMD)

# Semantic versioning and commit commands
commit:
	@echo "Creating conventional commit..."
	uv run cz commit

# Bump patch version (1.1.0 -> 1.1.1)
bump-patch:
	@echo "Bumping patch version..."
	uv run cz bump --increment PATCH
	@echo "Version bumped! Don't forget to push tags: git push --tags"

# Bump minor version (1.1.0 -> 1.2.0)
bump-minor:
	@echo "Bumping minor version..."
	uv run cz bump --increment MINOR
	@echo "Version bumped! Don't forget to push tags: git push --tags"

# Bump major version (1.1.0 -> 2.0.0)
bump-major:
	@echo "Bumping major version..."
	uv run cz bump --increment MAJOR
	@echo "Version bumped! Don't forget to push tags: git push --tags"
