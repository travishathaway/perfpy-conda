# perfpy-conda
A repository for tracking conda performance using the perfpy CLI

## Solver comparison benchmark

`profiles/solver_comparison.json` compares `conda-libmamba-solver` against
`conda-rattler-solver` end to end. The runner needs `perfpy` on `PATH` and a
conda 26.10 or later install with both solvers. Set `CONDA_BENCH_PREFIX` to that install:

```bash
CONDA_BENCH_PREFIX=/path/to/conda-install scripts/run_solver_benchmark.sh
python scripts/analyze_solver_benchmark.py
```

The profile creates a small Python environment and a small science environment
(`python=3.13 numpy pandas scipy matplotlib`) from `conda-forge`. It runs three
repetitions per scenario, alternating solver order. Each repetition performs
one cold create, one warm create, and one warm dry-run per solver. The runner
isolates the conda package and repodata caches under
`/tmp/perfpy-conda-solver-bench`. 
The benchmark writes `data/solver_comparison.csv`; the analysis writes
`data/solver_comparison_summary.csv`.
