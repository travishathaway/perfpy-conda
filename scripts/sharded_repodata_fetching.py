"""
Benchmark previous and new repodata fetching methods
"""
import tempfile
import sys
from pathlib import Path

from conda.base.context import context
from conda.models.channel import Channel
from conda_libmamba_solver.index import LibMambaIndexHelper
from conda_libmamba_solver.state import SolverInputState


def main() -> None:
    if len(sys.argv) < 3:
        print("Please pass a channel and one or more package names")
        sys.exit(1)

    # Retrieve arguments
    load_channel = sys.argv[1]
    requested = sys.argv[2:]

    # Need to load environment configuration
    context.__init__()

    print(f"Running benchmarking for {load_channel} {' '.join(requested)}")
    print(f"Shards enabled: {context.plugins.use_sharded_repodata}")

    with tempfile.TemporaryDirectory() as tmp_path:
        in_state = SolverInputState(str(Path(tmp_path) / "env"), requested=requested)
        index = LibMambaIndexHelper(
            # this is expanded to noarch, linux-64 for shards.
            channels=[Channel(f"{load_channel}/linux-64")],
            subdirs=(
                "noarch",
                "linux-64",
            ),
            installed_records=(),  # do not load installed
            pkgs_dirs=(),  # do not load local cache as a channel
            in_state=in_state,
        )
        # Make sure we generated something valid
        assert len(index.repos) == 2
        assert index.search("python")


if __name__ == "__main__":
    main()
