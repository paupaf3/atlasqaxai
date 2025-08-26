from ..utils import paths
from ..vectorstore import store
from ..rag import session


def run() -> None:
    print("Wiping index...")
    store.wipe_index(paths.PERSIST_DIR)

    # Invalidate the session cache since the index has been wiped
    session.get_session().force_reload()

    print("Index wiped.")
