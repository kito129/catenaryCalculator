# Catenary Calculator

A catenary calculator using the Newton-Raphson method for precision engineering calculations.

**Author:** kito129  
**Version:** 1.1.0  
**Created:** 2023/10/18  
**Last Update:** 2025/09/02

## Change Log

[Changelogs page](https://github.com/kito129/catenaryCalculator/blob/main/changelogs.md)

## Description

A command-line application for calculating catenary parameters using the Newton-Raphson numerical method. The calculator provides precise results for cable sag and tension calculations in engineering applications.

**Features:**
- Interactive command-line interface with input validation
- Default parameter set for quick calculations
- Newton-Raphson method for high precision
- Support for custom parameter input
- Comprehensive development environment with modern Python tooling

**Usage:**
- Run with `make run` or `python main.py`
- Choose 'y' to input custom parameters or 'n' to use default values
- Results include parameter calculations and arrow measurements

## Setup

### Prerequisites
- Python 3.13 or higher
- Make (for running Makefile commands)

### Development Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kito129/catenaryCalculator.git
   cd catenaryCalculator
   ```

2. **Quick setup with make (recommended)**
   ```bash
   make setup
   ```
   This will create the virtual environment, install uv, sync dependencies, and setup pre-commit hooks.

3. **Manual setup (alternative)**
   
   a. **Create and activate a Python virtual environment**
   ```bash
   make venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

   b. **Install uv for package management**
   ```bash
   pip install uv
   ```

   c. **Initialize and sync dependencies with uv**
   ```bash
   # Initialize uv project (if not already done)
   uv init
   
   # Sync dependencies from pyproject.toml
   uv sync
   
   # Or sync with development dependencies
   uv sync --dev
   ```

   d. **Add development tools using uv**
   ```bash
   uv add --dev flake8 pre-commit pytest ruff black
   ```

   e. **Setup pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Makefile Commands

- `make venv` - Create Python virtual environment
- `make venv-clean` - Remove Python virtual environment
- `make setup` - Setup development environment (includes venv)
- `make install` - Install/sync dependencies  
- `make run` - Run the main application
- `make test` - Run tests
- `make lint` - Run linting
- `make format` - Format code
- `make check` - Run all checks (lint + test)
- `make clean` - Clean up temporary files
- `make add PACKAGE=name` - Add dependency
- `make add-dev PACKAGE=name` - Add dev dependency
- `make remove PACKAGE=name` - Remove dependency
- `make update` - Update dependencies
- `make lock` - Create/update lock file
- `make uv-run CMD='command'` - Run any command in project environment

### UV Configuration

This project uses `uv` for fast and reliable package management. Key features:
- Fast dependency resolution and installation
- Lock file support for reproducible builds
- Compatible with pip and standard Python packaging

### Linting with Flake8

Code quality is maintained using flake8. Configuration is in `.flake8` file.
Run linting with:
```bash
make lint
# or
flake8 .
```

### Pre-commit Hooks

Pre-commit hooks ensure code quality before commits:
- Flake8 linting
- Code formatting
- Import sorting
- Trailing whitespace removal

Hooks run automatically on `git commit`, or manually with:
```bash
pre-commit run --all-files
```