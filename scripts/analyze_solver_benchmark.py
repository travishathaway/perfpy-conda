#!/usr/bin/env python3
"""Summarize a solver comparison report produced by perfpy."""

from __future__ import annotations

import argparse
import csv
import re
import statistics
from collections import defaultdict
from pathlib import Path

NAME_RE = re.compile(
    r"^(?P<op>create|dryrun|remove|clean)_(?P<solver>libmamba|rattler)_"
    r"(?P<scenario>python|science)(?:_(?P<phase>cold|warm)_(?P<run>\d+)|_(?P<iteration>\d+))?$"
)


def parse_rows(path: Path) -> list[dict]:
    """Load perfpy rows and attach parsed name fields."""
    rows = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            match = NAME_RE.match(row["name"])
            if not match:
                continue
            row.update(match.groupdict())
            row["total_time_s"] = float(row["total_time"]) / 1e9
            row["cpu_s"] = float(row["user_time"]) + float(row["cpu_time"])
            row["rss_mb"] = float(row["max_memory_usage"]) / (1024 * 1024)
            row["recv_mb"] = float(row["bytes_recv"]) / (1024 * 1024)
            row["return_code"] = (
                int(row["return_code"])
                if row["return_code"] not in ("", "None")
                else -1
            )
            rows.append(row)
    return rows


def median(rows: list[dict], key: str) -> float:
    return statistics.median(row[key] for row in rows)


def summarize(rows: list[dict]) -> list[dict]:
    """Aggregate measurements by solver, scenario, operation, and phase."""
    groups: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        phase = row["phase"] or "cold"
        groups[(row["solver"], row["scenario"], row["op"], phase)].append(row)

    summary = []
    for (solver, scenario, op, phase), group in sorted(groups.items()):
        summary.append(
            {
                "solver": solver,
                "scenario": scenario,
                "operation": op,
                "phase": phase,
                "runs": len(group),
                "failed": sum(row["return_code"] != 0 for row in group),
                "total_s_median": round(median(group, "total_time_s"), 3),
                "cpu_s_median": round(median(group, "cpu_s"), 3),
                "rss_mb_median": round(median(group, "rss_mb"), 1),
                "recv_mb_median": round(median(group, "recv_mb"), 1),
            }
        )
    return summary


def print_table(summary: list[dict]) -> None:
    headers = (
        "solver",
        "scenario",
        "operation",
        "phase",
        "runs",
        "failed",
        "total_s_median",
        "cpu_s_median",
        "rss_mb_median",
        "recv_mb_median",
    )
    print(" ".join(f"{header:>14}" for header in headers))
    for row in summary:
        print(" ".join(f"{row[header]:>14}" for header in headers))


def print_comparison(summary: list[dict], operation: str, phase: str) -> None:
    """Print per-scenario ratios for one operation/phase pair."""
    by_key = {
        (row["solver"], row["scenario"]): row["total_s_median"]
        for row in summary
        if row["operation"] == operation and row["phase"] == phase
    }
    scenarios = sorted({scenario for _, scenario in by_key})
    print(f"\n{operation} ({phase}) comparison")
    print(f"{'scenario':>12} {'libmamba_s':>12} {'rattler_s':>12} {'ratio':>8}")
    for scenario in scenarios:
        libmamba = by_key.get(("libmamba", scenario))
        rattler = by_key.get(("rattler", scenario))
        if libmamba is None or rattler is None:
            continue
        print(
            f"{scenario:>12} {libmamba:>12.3f} {rattler:>12.3f} {rattler / libmamba:>8.2f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "report", nargs="?", type=Path, default=Path("data/solver_comparison.csv")
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("data/solver_comparison_summary.csv"),
    )
    args = parser.parse_args()

    rows = parse_rows(args.report)
    if not rows:
        raise SystemExit(f"no benchmark rows found in {args.report}")

    summary = summarize(rows)
    print_table(summary)

    with args.summary.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)

    print_comparison(summary, "create", "cold")
    print_comparison(summary, "create", "warm")
    print_comparison(summary, "dryrun", "warm")
    print(f"\nWrote {args.summary}")


if __name__ == "__main__":
    main()
