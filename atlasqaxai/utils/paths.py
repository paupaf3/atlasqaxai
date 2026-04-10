import os
from pathlib import Path


DATA_DIR = Path(os.getenv("DATA_DIR", "./data/files"))
DATA_DOCS_PATHS_TEXT_FILE = Path(
    os.getenv("DATA_DOCS_PATHS_TEXT_FILE", "./data/docs_paths.txt"))
DATA_WEBS_PATHS_TEXT_FILE = Path(
    os.getenv("DATA_WEBS_PATHS_TEXT_FILE", "./data/webs_paths.txt"))
PERSIST_DIR = Path(os.getenv("PERSIST_DIR", "./index"))

# Make sure folders exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# Manifest to track incremental ingest
MANIFEST_PATH = PERSIST_DIR / "manifest.json"
