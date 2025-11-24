"""
Benchmarking for repodata fetching with py-rattler
"""
import asyncio
import sys
from rattler import Gateway, SourceConfig

# boop

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
    records = asyncio.run(gateway.query([load_channel], ["linux-64", "noarch"], requested))
    assert len(records) == 2


if __name__ == "__main__":
    main()