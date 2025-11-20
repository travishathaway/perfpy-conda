"""
Benchmarking for repodata fetching with py-rattler
"""
import asyncio
import sys
import tempfile
from rattler import Gateway, SourceConfig


def main():
    if len(sys.argv) < 3:
        print("Please pass a channel and one or more package names")
        sys.exit(1)

    # Retrieve arguments
    load_channel = sys.argv[1]
    requested = sys.argv[2:]

    gateway = Gateway(
        default_config=SourceConfig(
            sharded_enabled=load_channel == "conda-forge-sharded"
        )
    )
    records = asyncio.run(gateway.query([load_channel], ["linux-64"], requested))
    assert len(records) == 1


if __name__ == "__main__":
    main()