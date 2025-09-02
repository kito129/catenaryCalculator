# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-09-02

### Added
- Complete development environment setup with Makefile
- Python virtual environment management (`make venv`, `make venv-clean`)
- UV package manager integration for fast dependency management
- Pre-commit hooks for code quality (flake8, black, ruff, mypy)
- Comprehensive pyproject.toml configuration
- Development tools integration (pytest, black, ruff, flake8)
- Automated setup command (`make setup`) for one-command environment setup
- **Semantic versioning support** with commitizen integration
- **Conventional commit validation** through pre-commit hooks
- **Version bumping commands** (`make bump-patch`, `make bump-minor`, `make bump-major`)
- **Guided commit creation** with `make commit` command

### Changed
- Updated Python requirement to 3.13+
- Virtual environment folder changed from `venv` to `.venv` (hidden)
- Simplified README with concise Makefile command list
- Enhanced development workflow with UV commands wrapped in Makefile
- **Removed all GUI dependencies**: Converted from tkinter GUI to command-line interface
- **Removed Excel functionality**: Eliminated openpyxl dependency for simpler deployment

### Fixed
- Build configuration for single-file Python project structure
- UV sync now works properly with hatchling build backend
- Test suite handles missing tkinter dependency gracefully
- Added missing openpyxl dependency to project configuration
- **Updated ruff configuration**: Migrated to modern `lint` section format to eliminate deprecation warnings

### Technical
- Added tool configurations for black, ruff, mypy, pytest, and coverage
- Set up proper exclusions for virtual environments and cache directories
- Configured pre-commit hooks for automated code quality checks
- Fixed hatchling build configuration for main.py script

## [1.0.0] - 2023-10-19

### Added
- Initial version: funeCalculatorv1_0_0.exe
- Catenary calculator using Newton-Raphson method
- Text-based input interface
- Default calculation parameters with option to customize
