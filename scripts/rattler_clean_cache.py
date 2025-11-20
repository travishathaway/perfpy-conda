"""
Removes rattler cache for linux-64 for conda-forge and conda-forge-sharded
"""
from rattler import Gateway


def main():
    gateway = Gateway()
    gateway.clear_repodata_cache("conda-forge", ["linux-64"])
    gateway.clear_repodata_cache("conda-forge-sharded", ["linux-64"])


if __name__ == "__main__":
    main()
