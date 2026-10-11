# Validation evidence: bt

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
| `uv lock --upgrade --python 3.15` | 0 | 0.56 | [log](../../docs/maintenance-2026-10-12/bt-lock-3.15.log) |
| `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | 2 | 5.59 | [log](../../docs/maintenance-2026-10-12/bt-wheel-probe-3.15.log) |
| `uv lock --upgrade --python 3.14` | 0 | 0.88 | [log](../../docs/maintenance-2026-10-12/bt-lock-3.14.log) |
| `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | 0 | 0.75 | [log](../../docs/maintenance-2026-10-12/bt-wheel-probe-3.14.log) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 26.35 | [log](../../docs/maintenance-2026-10-12/bt-sync-3.14.log) |
| `uv build --python 3.14` | 0 | 14.68 | [log](../../docs/maintenance-2026-10-12/bt-build.log) |
| `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | 0 | 0.08 | [log](../../docs/maintenance-2026-10-12/bt-compile.log) |
| `uv run --no-sync python -m pytest` | 1 | 18.26 | [log](../../docs/maintenance-2026-10-12/bt-tests.log) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/bt-sync-pandas-compatibility.log) |
| `uv run --no-sync python -m pytest` | 1 | 45.11 | [log](../../docs/maintenance-2026-10-12/bt-tests-pandas-compatibility.log) |
| `uv run --no-sync python -m pytest` | 0 | 23.55 | [log](../../docs/maintenance-2026-10-12/bt-tests-numeric-boundaries.log) |
| `uv lock --upgrade --python 3.14` | 0 | 0.4 | [log](../../docs/maintenance-2026-10-12/bt-lock-ffn-numeric-boundary.log) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 16.53 | [log](../../docs/maintenance-2026-10-12/bt-sync-ffn-numeric-boundary.log) |
| `uv run --no-sync python -m pytest` | 0 | 16.13 | [log](../../docs/maintenance-2026-10-12/bt-tests-ffn-numeric-boundary.log) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.07 | [log](../../docs/maintenance-2026-10-12/bt-compile-final.log) |
| `uv build --python 3.14` | 0 | 10.67 | [log](../../docs/maintenance-2026-10-12/bt-build-final.log) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.24 | [log](../../docs/maintenance-2026-10-12/bt-versions-final.log) |
| `uv sync --directory /tmp/trading-python315-probes/bt --all-extras --all-groups --python 3.15` | 0 | 48.14 | [log](../../docs/maintenance-2026-10-12/bt-python315-source-probe.log) |
| `uv lock --upgrade --python 3.15` | 0 | 0.98 | [log](../../docs/maintenance-2026-10-12/bt-lock-python315-source-supported.log) |
| `uv sync --all-extras --all-groups --python 3.15` | 0 | 41.24 | [log](../../docs/maintenance-2026-10-12/bt-sync-python315-source-supported.log) |
| `uv run --no-sync python -m pytest` | 0 | 41.82 | [log](../../docs/maintenance-2026-10-12/bt-tests-python315-source-supported.log) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.14 | [log](../../docs/maintenance-2026-10-12/bt-compile-selected-python.log) |
| `uv build --python 3.15` | 0 | 30.19 | [log](../../docs/maintenance-2026-10-12/bt-build-selected-python.log) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]:d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.25 | [log](../../docs/maintenance-2026-10-12/bt-versions-final.log) |
| `uv build --python 3.15` | 0 | 21.95 | [log](../../docs/maintenance-2026-10-12/bt-build-vendor-source-archive.log) |
| `uv run --no-sync python -c import bt,bt.core; print(bt.__file__); print(bt.core.__file__)` | 0 | 4.65 | [log](../../docs/maintenance-2026-10-12/bt-artifact-import.log) |

The versions-final log records the exact interpreter patch release and every installed dependency version. The machine-readable [result](../../docs/maintenance-2026-10-12/bt-result.json) includes branch/default ancestry, status, artifacts and unresolved checks.

## Dependency floor refresh

| Before | After |
|---|---|

The table records the initial metadata refresh. Later compatibility constraints and vendor sources are explained above and the final authoritative requirements are in [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). No test cases were added, removed or disabled. Existing deprecated-API cases retain their assertions while explicitly checking the documented warning.
