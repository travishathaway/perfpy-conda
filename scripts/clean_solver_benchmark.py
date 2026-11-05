"""Reset the benchmark's run-local caches and prefixes."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

BENCH_ROOT = Path(os.environ.get("CONDA_BENCH_ROOT", "/tmp/perfpy-conda-solver-bench"))


def main() -> None:
    """Remove the run-local package cache, repodata cache, and prefixes."""
    if not os.environ.get("CONDA_PKGS_DIRS"):
        raise SystemExit("run this through scripts/run_solver_benchmark.sh")

    shutil.rmtree(BENCH_ROOT, ignore_errors=True)
    BENCH_ROOT.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
