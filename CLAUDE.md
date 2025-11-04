# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a conda performance profiling project that uses Docker to generate performance metrics and Jupyter notebooks to analyze/visualize them. The workflow is:

1. **Data Generation** (Docker): Run conda operations via `perfpy` CLI → outputs `data/report.csv`
2. **Analysis** (Jupyter): Load CSV → create interactive visualizations with Plotly → export for web

## Key Commands

### Dependency Management (uv)
```bash
uv sync                    # Install/sync all dependencies from uv.lock
uv add <package>          # Add a new dependency
uv run <command>          # Run command in the project environment
```

### Generate Performance Data
```bash
docker build -t perfpy-conda .
docker run -v $(pwd)/data:/app/data perfpy-conda
```

This runs the commands defined in `to_profile.json` and outputs performance metrics to `data/report.csv`.

### Analysis & Visualization
```bash
uv run jupyter lab        # Launch Jupyter Lab
```

Navigate to `nb/analysis.ipynb` to analyze the performance data.

## Architecture

### Performance Data Pipeline

- **`to_profile.json`**: Defines conda commands to profile (config changes, package installs, cold/warm runs)
- **Docker container**: Isolated environment running `perfpy` CLI to execute and profile commands
- **`data/report.csv`**: Output with columns: `name`, `command`, `bytes_recv`, `bytes_sent`, `user_time`, `cpu_time`, `total_time`, `max_memory_usage`, `return_code`

### Analysis Workflow

- **`nb/analysis.ipynb`**: Jupyter notebook with pre-built visualizations:
  - Execution time comparisons
  - Memory usage analysis
  - Network activity (bytes sent/received)
  - Cold vs warm performance comparisons
  - CPU vs user time relationships

- **Plotly for visualization**: Creates interactive graphs that can be exported as:
  - Standalone HTML files (`fig.write_html()`)
  - HTML divs for embedding (`fig.to_html(full_html=False)`)
  - Static images (`fig.write_image()` - requires kaleido)

- **`exports/` directory**: Target for exported graphs (created during analysis)

## Project Structure

```
.
├── Dockerfile              # Builds perfpy environment
├── to_profile.json         # Commands to profile
├── data/report.csv         # Generated performance metrics
├── nb/analysis.ipynb       # Analysis notebook
└── exports/                # Exported visualizations (created on-demand)
```

## Important Notes

- The project uses **uv** for dependency management (not pip)
- All time metrics in the CSV are in **nanoseconds** (convert to seconds for readability)
- Memory metrics are in **bytes** (convert to MB for readability)
- The notebook includes conversion code for these units
- Cold runs = first execution with cleared cache; Warm runs = subsequent executions
