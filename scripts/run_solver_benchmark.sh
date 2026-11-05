#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

prefix="${CONDA_BENCH_PREFIX:-}"
bench_root="${CONDA_BENCH_ROOT:-/tmp/perfpy-conda-solver-bench}"
perfpy_bin="${PERFPY_BIN:-$(command -v perfpy || true)}"
profile="${1:-profiles/solver_comparison.json}"
output="${2:-data/solver_comparison.csv}"

if [[ -z "$prefix" ]]; then
    echo "set CONDA_BENCH_PREFIX to a conda 26.10 install with both solvers" >&2
    exit 1
fi

if [[ -z "$perfpy_bin" ]]; then
    echo "perfpy not found; install it or set PERFPY_BIN" >&2
    exit 1
fi

unset CONDA_PREFIX CONDA_DEFAULT_ENV CONDA_SHLVL CONDA_PYTHON_EXE
export CONDA_EXE="$prefix/bin/conda"
export CONDA_BENCH_ROOT="$bench_root"
export CONDA_PKGS_DIRS="$bench_root/pkgs"
export XDG_CACHE_HOME="$bench_root/cache"
export PATH="$prefix/bin:$HOME/.local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

exec "$perfpy_bin" "$profile" --output "$output"
