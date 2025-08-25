import os
from pathlib import Path


DATA_DIR = Path(os.getenv("DATA_DIR"))
DATA_DOCS_PATHS_TEXT_FILE = Path(os.getenv("DATA_DOCS_PATHS_TEXT_FILE"))
DATA_WEBS_PATHS_TEXT_FILE = Path(os.getenv("DATA_WEBS_PATHS_TEXT_FILE"))
PERSIST_DIR = Path(os.getenv("PERSIST_DIR"))

# Make sure folders exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# Manifest to track incremental ingest
MANIFEST_PATH = PERSIST_DIR / "manifest.json"
