# AutoSeachLib

Automated research library for optimizing damage detection models at CarScan.ai.

> 🚧 **Status: Under Active Development**

## Overview

AutoSeachLib is designed to transition model optimization from manual analysis to an autonomous research loop. The library systematically evaluates and tunes model architectures, hyperparameters, and training strategies to improve accuracy and performance.

### Primary Objectives

- **Architectural Optimization** — Identify and resolve structural flaws in damage detection models.
- **Autonomous Tuning** — Implement a systematic loop for hyperparameter and training strategy refinement.
- **Precision Improvement** — Specifically targeting high false-positive rates in chip detection.
- **Small Object Resolution** — Enhancing feature resolution for subtle or small-scale damage features.

## Installation

### Using pip

```bash
pip install git+https://github.com/carscan/autoseachlib.git
```

### Using uv

```bash
# Install into the current environment
uv pip install git+https://github.com/carscan/autoseachlib.git

# Or add as a dependency to your project
uv add git+https://github.com/carscan/autoseachlib.git

# Or run the CLI directly without installing (ephemeral)
uvx --from git+https://github.com/carscan/autoseachlib.git autoseachlib hello
```

### In a Jupyter Notebook

```python
# pip
!pip install --upgrade git+https://github.com/carscan/autoseachlib.git

# uv (faster)
!uv pip install --upgrade git+https://github.com/carscan/autoseachlib.git
```

### For Development

```bash
git clone https://github.com/carscan/autoseachlib.git
cd autoseachlib

# Using pip
pip install -e ".[dev]"

# Using uv
uv pip install -e ".[dev]"
```

## Quick Start

```python
import autoseachlib

# Hello world
autoseachlib.hello_world()
# → Hello World from AutoSeachLib!

# String concatenation
result = autoseachlib.add_strings("Hello, ", "World!")
print(result)
# → Hello, World!
```

## CLI Usage

After installation, the `autoseachlib` command is available in your terminal:

```bash
# Show version
autoseachlib --version

# Print hello world
autoseachlib hello

# Concatenate two strings
autoseachlib add "Hello, " "World!"

# Show help
autoseachlib --help
```

## Project Structure

```
autoseachlib/
├── pyproject.toml             # Package config (PEP 621)
├── LICENSE
├── README.md
├── .gitignore
├── src/
│   └── autoseachlib/          # Package source code
│       ├── __init__.py        # Public API exports
│       ├── core.py            # Core functions
│       └── cli.py             # CLI entry point
├── tests/
│   ├── test_core.py           # Unit tests (pytest)
│   └── test_cli.py            # CLI tests
└── notebooks/
    └── demo.ipynb             # Demo notebook
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Contributing

This project is under active development. Please reach out to the development team for contribution guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
