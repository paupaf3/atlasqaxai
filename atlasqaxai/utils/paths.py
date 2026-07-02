import os
from pathlib import Path

from .config import DATA_DIR, DATA_DOCS_PATHS_TEXT_FILE, DATA_WEBS_PATHS_TEXT_FILE

DATA_DIR = Path(DATA_DIR)
DATA_DOCS_PATHS = Path(DATA_DOCS_PATHS_TEXT_FILE)
DATA_WEBS_PATHS = Path(DATA_WEBS_PATHS_TEXT_FILE)

DATA_DIR.mkdir(parents=True, exist_ok=True)
