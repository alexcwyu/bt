# Validation evidence: bt

<!-- current-documentation-provenance -->
Documentation reviewed: 2026-10-13 · Git source base: `63075945aa2c51b5aeef66e6b118c1f8b4ec7190` · [Current architecture and feature guide](ayu-develop.md).
Historical execution commands/results below retain their original dates and scope; this metadata update is not a new application test run.
<!-- /current-documentation-provenance -->


Run date: 2026-10-12. Branch: `feature/ayu_develop`. Interpreter: `3.15.0 (main, Oct  9 2026, 15:11:47) [Clang 22.1.3 ]`.

| Check | Result |
|---|---|
| lock | passed |
| sync | passed |
| compile | passed |
| build | passed |
| tests | passed |

## Current result and compatibility decisions

- The current Cython wheel hook discovers src/bt via setuptools package-dir. Pandas column initialization uses loc to avoid copy-on-write chained-assignment warnings.
- Empty/all-NaN benchmark histogram data is explicitly rejected with ValueError before density normalization; the existing cases preserve that behavior.
- Verified licensed ffn 1.4.1 source handles total-loss log returns as -inf and undefined below-total-loss values as NaN without warning filters. See vendor/ffn/PROVENANCE.md.
- mdformat is capped below0.8 because current mdformat-tables 1.0.0 requires that API family. Python 3.15 actual source installation succeeds.

Current unresolved checks:

All supplied checks recorded below passed.

## Latest full-suite output

```text
$ uv run --no-sync python -m pytest
........................................................................ [  8%]
........................................................................ [ 17%]
........................................................................ [ 26%]
........................................................................ [ 35%]
........................................................................ [ 44%]
........................................................................ [ 53%]
........................................................................ [ 62%]
........................................................................ [ 71%]
........................................................................ [ 80%]
........................................................................ [ 88%]
........................................................................ [ 97%]
.................                                                        [100%]
809 passed in 38.62s

```

## Exact commands and exit codes

Unsuccessful rows are retained as historical compatibility attempts; they are not claims that a current passing check remains blocked. Source-build probes use isolated temporary copies to preserve the selected repository environment.

| Command | Exit | Seconds | Evidence |
|---|---:|---:|---|
| `uv lock --upgrade --python 3.15` | 0 | 0.56 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | 2 | 5.59 | [check record](maintenance/index.html) |
| `uv lock --upgrade --python 3.14` | 0 | 0.88 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | 0 | 0.75 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 26.35 | [check record](maintenance/index.html) |
| `uv build --python 3.14` | 0 | 14.68 | [check record](maintenance/index.html) |
| `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | 0 | 0.08 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 1 | 18.26 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 0.13 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 1 | 45.11 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 0 | 23.55 | [check record](maintenance/index.html) |
| `uv lock --upgrade --python 3.14` | 0 | 0.4 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 16.53 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 0 | 16.13 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.07 | [check record](maintenance/index.html) |
| `uv build --python 3.14` | 0 | 10.67 | [check record](maintenance/index.html) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.24 | [check record](maintenance/index.html) |
| `uv sync --directory /tmp/trading-python315-probes/bt --all-extras --all-groups --python 3.15` | 0 | 48.14 | [check record](maintenance/index.html) |
| `uv lock --upgrade --python 3.15` | 0 | 0.98 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.15` | 0 | 41.24 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 0 | 41.82 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.14 | [check record](maintenance/index.html) |
| `uv build --python 3.15` | 0 | 30.19 | [check record](maintenance/index.html) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]:d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.25 | [check record](maintenance/index.html) |
| `uv build --python 3.15` | 0 | 21.95 | [check record](maintenance/index.html) |
| `uv run --no-sync python -c import bt,bt.core; print(bt.__file__); print(bt.core.__file__)` | 0 | 4.65 | [check record](maintenance/index.html) |

The versions-final log records the exact interpreter patch release and every installed dependency version. The machine-readable [verification record](maintenance/verification.json) includes branch/default ancestry, status, artifacts and unresolved checks.

## Dependency floor refresh

| Before | After |
|---|---|

The table records the initial metadata refresh. Later compatibility constraints and vendor sources are explained above and the final authoritative requirements are in [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). No test cases were added, removed or disabled. Existing deprecated-API cases retain their assertions while explicitly checking the documented warning.
