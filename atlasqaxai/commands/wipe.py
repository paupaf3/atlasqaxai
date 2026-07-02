import shutil
from pathlib import Path

from ..rag import session
from ..utils import config


def run() -> None:
    print("Wiping index...")
    working_dir = Path(config.WORKING_DIR)
    if working_dir.exists():
        shutil.rmtree(working_dir)
        print(f"Deleted {working_dir}")

    output_dir = Path(config.OUTPUT_DIR)
    if output_dir.exists():
        shutil.rmtree(output_dir)
        print(f"Deleted {output_dir}")

    session.get_session().force_reload()
    print("Index wiped.")
