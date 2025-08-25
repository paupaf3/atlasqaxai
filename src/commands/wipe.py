from utils import paths
from vectorstore import store


def run() -> None:
    print("Wiping index...")
    store.wipe_index(paths.PERSIST_DIR)
    print("Index wiped.")
