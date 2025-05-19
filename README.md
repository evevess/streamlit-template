# Streamlit App Template

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![UV](https://img.shields.io/badge/powered%20by-uv-black)](https://github.com/astral-sh/uv)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [UV installed](https://github.com/astral-sh/uv#installation)

### 1. Installation (with UV)

```bash
uv python install 3.12
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r pyproject.toml
```

# Run the Streamlit App
```bash
streamlit run streamlit/📋 proposal_form_app.py
```

# Add OneDrive Location
```bash
export OneDrive="/path/to/your/OneDrive/folder"
```

# Linting & Formatting
# Run Ruff linter
```bash
ruff check .
```
# Auto-fix lint errors
```bash
ruff check --fix .
```
# Format code (Ruff replaces Black)
```bash
ruff format .
```

# Setup Pre-commit Hooks
```bash
uv pip install pre-commit
uv run pre-commit install
```
