"""
Hatch build hook for Cython compilation.
"""
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os
import subprocess


class CustomBuildHook(BuildHookInterface):
    """Custom build hook to compile Cython extensions."""

    def initialize(self, version, build_data):
        """Compile Cython extension before building."""
        try:
            # Try to compile with Cython
            print("Compiling bt/core.py with Cython...")
            subprocess.run(
                ["cython", "bt/core.py", "-o", "bt/core.c"],
                check=True,
                cwd=self.root
            )
            print("Cython compilation successful!")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Cython compilation failed or Cython not found: {e}")
            print("Checking if pre-compiled bt/core.c exists...")
            core_c_path = os.path.join(self.root, "bt", "core.c")
            if not os.path.exists(core_c_path):
                raise RuntimeError(
                    "Cython compilation failed and no pre-compiled bt/core.c found. "
                    "Please install Cython: pip install cython"
                )
            print("Using pre-compiled bt/core.c")

