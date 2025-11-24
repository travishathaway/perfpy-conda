"""
Removes rattler cache for linux-64 for conda-forge and conda-forge-sharded
"""
import os
import shutil
from pathlib import Path


def main():
    shutil.rmtree(
        Path(os.path.expanduser("~")) / ".cache/rattler"
    )


if __name__ == "__main__":
    main()
