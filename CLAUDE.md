# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**bt** is a flexible backtesting framework for Python used to test quantitative trading strategies. It emphasizes modularity and reusability through tree structures, algorithm stacks, and composable strategy logic.

- **Language**: Python (3.9+) with optional Cython optimizations
- **License**: MIT
- **Upstream**: https://github.com/pmorissette/bt
- **Documentation**: http://pmorissette.github.io/bt

## Development Setup

### Initial Setup

```bash
# Install in development mode with all dependencies
make develop

# Or manually
python -m pip install -e .[dev]
```

### Build (Cython Extensions)

```bash
# Build Cython extensions in-place (for development)
make build_dev

# Or manually
python setup.py build_ext --inplace
```

## Common Development Commands

### Testing

```bash
# Run all tests with coverage
make test

# Runs: python -m pytest -vvv tests --cov=bt --junitxml=python_junit.xml --cov-report=xml --cov-branch --cov-report term

# Run specific test file
python -m pytest tests/test_core.py -v

# Run specific test
python -m pytest tests/test_core.py::test_node_tree1 -v

# Run tests matching a pattern
python -m pytest -k "test_strategy" -v
```

### Linting and Formatting

```bash
# Check code style (ruff)
make lint

# Auto-fix issues
make fix
```

Configuration in `pyproject.toml`:
- Line length: 180
- Per-file ignores: `__init__.py` allows F401 (unused import) and F403 (star import)

### Distribution

```bash
# Build source distribution
make dist

# Upload to PyPI (maintainers only)
make upload
```

### Documentation

```bash
# Build docs locally
make docs

# Serve docs on http://localhost:9087
make serve

# Launch Jupyter for examples
make notebooks
```

### Cleanup

```bash
make clean
# Removes: build/, dist/, bt.egg-info/, *.so, *.c files
```

## Architecture

### Core Design Principles

bt uses three main architectural patterns:

1. **Tree Structure** (`bt/core.py:24-1940`)
   - Nodes form hierarchical trees representing strategy composition
   - Each Node has: parent, children, prices, value, weight
   - Supports lazy child creation via string references
   - Root node tracks global state (date, stale flags)

2. **Algorithm Stacks** (`bt/core.py:1977-2014`)
   - Algos are modular, reusable logic blocks that operate on strategies
   - AlgoStack runs Algos sequentially until one returns False
   - Algos can be marked with `@run_always` decorator to always execute
   - Data passing: `temp` dict (cleared each run) and `perm` dict (persistent)

3. **Strategy/Security Separation**
   - **StrategyBase** (`bt/core.py:441-1938`): Container nodes that hold capital and children
   - **SecurityBase** (`bt/core.py:1195-1938`): Leaf nodes representing tradeable assets
   - Both inherit from Node, providing consistent tree interface

### Key Classes

- **Node** (`bt/core.py:24`): Base tree node with price tracking and hierarchy management
- **StrategyBase** (`bt/core.py:441`): Extends Node with capital allocation, rebalancing, and position management
- **Strategy** (`bt/core.py:2017`): StrategyBase + AlgoStack for defining trading logic
- **SecurityBase** (`bt/core.py:1195`): Represents a security with price history
- **Algo** (`bt/core.py:1942`): Base class for modular strategy logic
- **AlgoStack** (`bt/core.py:1977`): Chains multiple Algos together
- **Backtest** (`bt/backtest.py:85`): Runs a Strategy over data to produce Results

### Data Flow

```
1. Backtest.run() → iterates through dates
2. Strategy.update(date) → updates prices, values from universe
3. Strategy.run() → clears temp, calls AlgoStack
4. AlgoStack.__call__() → runs each Algo sequentially
5. Algos modify Strategy state (weights, temp data, positions)
6. Strategy.adjust() → allocates capital based on weights
7. Results collected in Strategy.data DataFrame
```

### Fixed Income Support

- **FixedIncomeStrategy** (`bt/core.py:2066`): Uses notional values instead of market values
- **FixedIncomeSecurity** and variants: Support coupon payments and hedging
- Price calculated from additive PnL returns, not multiplicative

## Module Structure

```
bt/
├── __init__.py         # Package exports
├── core.py             # Core tree structure, Strategy, Algo, Security classes (2088 lines)
├── algos.py            # Collection of 50+ pre-built Algos (2421 lines)
└── backtest.py         # Backtesting engine, Result classes (608 lines)

tests/
├── test_core.py        # Node, Strategy, Security tests (78 tests)
├── test_algos.py       # Algo functionality tests (70 tests)
└── test_backtest.py    # Backtest and Result tests (11 tests)

examples/
├── buy_and_hold.py     # Basic monthly rebalancing example
├── pairs_trading.py    # Pairs trading strategy
└── *.ipynb             # Jupyter notebooks for various strategies
```

## Dependencies

**Core Runtime**:
- `ffn>=1.1.2` - Financial functions library (data fetching, statistics)
- `pandas>=0.19` - Data structures
- `numpy>=1` - Numerical operations
- `pyprind>=2.11`, `tqdm>=4` - Progress bars

**Optional Performance**:
- `cython>=0.29.25` - Compiles core.py for speed (setup.py handles fallback to C)

**Development**:
- `pytest`, `pytest-cov` - Testing
- `ruff>=0.5.0,<0.15` - Linting and formatting
- `matplotlib>=2` - Charting (for Result plotting)
- `scikit-learn` - Used by some Algos (e.g., covariance estimation)

## Cython Integration

`bt/core.py` can be compiled with Cython for performance:

- Source: `bt/core.py` (pure Python with type hints)
- Compiled: `bt/core.so` (or `.pyd` on Windows)
- Fallback: `bt/core.c` pre-generated for environments without Cython

Type hints use Cython decorators:
```python
@cy.locals(x=cy.double)
def is_zero(x):
    return abs(x) < TOL
```

Build process (in `setup.py`):
1. Try to import Cython → compile `bt/core.py`
2. If Cython unavailable → use pre-built `bt/core.c`

## Testing Strategy

- **159 tests** across 3 test files (test_core.py, test_algos.py, test_backtest.py)
- Tests use `pytest` with fixtures and parametrization
- Mock objects (`unittest.mock`) for data isolation
- Coverage reporting enabled by default in `make test`

Common test patterns:
```python
# Create test data
dates = pd.date_range('2020-01-01', '2020-12-31')
prices = pd.DataFrame({'asset1': 100, 'asset2': 200}, index=dates)

# Build strategy
strategy = bt.Strategy('test', [algo1, algo2, algo3])

# Run backtest
backtest = bt.Backtest(strategy, prices)
result = bt.run(backtest)

# Assert results
assert result.stats['total_return'] > 0
```

## Common Patterns

### Creating a Strategy

```python
import bt

# Define algos (logic executed in order)
algos = [
    bt.algos.RunMonthly(),          # Run on month end
    bt.algos.SelectAll(),            # Select all securities
    bt.algos.WeighEqually(),         # Equal weight
    bt.algos.Rebalance()             # Execute rebalance
]

# Create strategy
strategy = bt.Strategy('my_strategy', algos)

# Run backtest with price data (DataFrame with DatetimeIndex)
backtest = bt.Backtest(strategy, price_data)
result = bt.run(backtest)

# Analyze results
result.display()
result.plot()
```

### Running a Single Test

```python
# From command line
python -m pytest tests/test_core.py::test_node_tree1 -v

# With coverage for specific module
python -m pytest tests/test_algos.py --cov=bt.algos -v
```

## CI/CD

GitHub Actions workflows (`.github/workflows/`):
- **build.yml**: Runs on push to master and PRs
  - Tests across Ubuntu, macOS, Windows with Python 3.11
  - Steps: develop → lint → test → dist → build wheels
- **deploy.yml**: Publishes to PyPI on release tags
- **regression.yml**: Additional regression testing

## Git Workflow

- **Main branch**: `master`
- **Upstream**: `git@github.com:pmorissette/bt.git`
- Fork workflow: origin (your fork) + upstream (main repo)

## Key Implementation Details

### Strategy Execution
- Strategies maintain a `data` DataFrame with columns: `price`, `value`, `notional_value`, `cash`, `fees`, `flows`
- `update()` method called each date to refresh prices and values
- `run()` method executes AlgoStack, which modifies strategy state
- `adjust()` method allocates capital based on weights set by Algos

### Position Tracking
- `integer_positions` flag (default: True) forces whole unit positions
- Positions tracked in `_positions` dict: `{security_name: quantity}`
- Capital allocated via `allocate()` method on children
- Rebalancing calculates difference between target and current weights

### Price and Value Semantics
- **price**: Normalized index value (Strategy) or market price (Security)
- **value**: Total market value (price × quantity for strategies)
- **notional_value**: Used for fixed income (position × notional per unit)
- **weight**: Child's value / parent's value

### Algo Communication
- `temp` dict: Cleared before each `run()`, used to pass data between Algos in same run
- `perm` dict: Persists across runs, used for stateful Algos
- Common temp keys: `weights`, `selected`, `price_target`, `stat`

### Universe and Data
- Universe: DataFrame passed to `Strategy.setup()`, typically price data
- Algos access universe via `target.universe` or `target.get_data('key')`
- Additional data sources passed as kwargs to `Backtest`, accessible via `strategy.get_data('key')`

## Performance Considerations

- Cython compilation of `core.py` provides ~2-5x speedup for large backtests
- Tree structure allows efficient hierarchical strategy composition
- Use `integer_positions=False` for strategies that don't need integer constraints (faster)
- Progress bars can be disabled: `bt.run(backtest, progress_bar=False)`
