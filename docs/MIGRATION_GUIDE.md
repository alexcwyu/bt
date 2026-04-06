# Migration Guide: bt

**Branch**: `feature/ayu_develop`
**Standard**: See `docs/PYTHON_MODERN_STANDARD.md` in the trading workspace root.

## Overview

This project has been modernized on the `feature/ayu_develop` branch to use the 2026 Python tooling stack. When syncing from upstream (default branch), the following changes must be re-applied if upstream overwrites them.

## What Changed

### 1. Build System (pyproject.toml)
- **Build backend**: `hatchling` (was: `hatchling`)
- **PEP 621 metadata**: All project metadata in `[project]` table
- **Dependencies**: Managed by `uv`, lockfile in `uv.lock`

### 2. Removed Legacy Files
The following files were removed (upstream may re-add them on sync):
- `bt.egg-info/` (legacy setuptools metadata)
- `dist/` (build artifacts)
- `coverage.xml` (CI output)
- `python_junit.xml` (CI output)

If these reappear after a sync, delete them again. All configuration is in `pyproject.toml`.

### 3. Source Layout
- **Layout**: `src/` layout
- **Package moved**: `bt/` -> `src/bt/`
- **Import unchanged**: `import bt` still works

If upstream adds files to the old location, move them to `src/bt/`.

### 4. Tooling Configuration (in pyproject.toml)

#### Ruff (linting + formatting)
```toml
[tool.ruff]
line-length = 180

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM", "C4", "RUF", "PERF", "TC", "PTH"]

[tool.ruff.lint.isort]
known-first-party = ["bt"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "F403"]
```

Changes from initial migration:
- Added `[tool.ruff.lint]` select with full PYTHON_MODERN_STANDARD rule set (was missing entirely)

#### Pyright (type checking)
```toml
[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "basic"
```

#### Pytest
```toml
[tool.pytest.ini_options]
minversion = "9.0"
addopts = ["-ra", "-q", "--strict-markers", "--import-mode=importlib"]
testpaths = ["tests"]
pythonpath = ["src"]
xfail_strict = true
filterwarnings = ["error"]
```

### 5. File Reorganization
- `MIGRATION_GUIDE.md` moved from repo root to `docs/MIGRATION_GUIDE.md`

### 6. Python Version
- `.python-version` set to `3.13`
- `requires-python = ">=3.13"` in pyproject.toml

## After Upstream Sync Checklist

When merging upstream changes into `feature/ayu_develop`:

1. **Delete re-added legacy files**: `setup.py`, `setup.cfg`, `requirements.txt`, `MANIFEST.in`, `poetry.lock`
2. **Check pyproject.toml**: Upstream may modify `[project]` metadata (version bumps, new deps). Merge those changes but keep `[build-system]`, `[tool.ruff]`, `[tool.pyright]`, `[tool.pytest]` sections intact.
3. **Check source layout**: If upstream adds new modules to the old path, move them to `src/bt/`.
4. **Re-lock**: Run `uv lock` to update `uv.lock` with any new/changed dependencies.
5. **Verify**: Run `uv sync && uv run python -c "import bt" && uv run pytest` (if tests exist).

## Quick Commands

```bash
uv sync                                    # Install all deps
uv run python -c "import bt"              # Verify import
uv run pytest                              # Run tests
uv run ruff check .                        # Lint
uv run ruff format .                       # Format
uv lock                                    # Re-generate lockfile
```
