# catenary Calculator
catenary calculator using Netwon-Raphson method.

# catenary Calculator
    author: kito129
    date: 2023/10/18
    last update: 2023/10/19
    version: 1.0.0

## Change Log:

[Changelogs page](https://github.com/kito129/catenaryCalculator/blob/main/changelogs.md)

## Description

- 10/19/20223 - Create first version funeCalculatorv1_0_0.exe

For now it takes in input from text, then I will make graphical interface.
Do "ENTER" or "n" at first question it does calculations with default data.If you do "S" then it asks for parameters, you put them one by one by pressing "ENTER", after Arrow it shows you results.
To make new calculation launch the file again

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