import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "../data"))
PERSIST_DIR = Path(os.getenv("PERSIST_DIR", "../index"))

# Make sure folders exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# Manifest to track incremental ingest
MANIFEST_PATH = PERSIST_DIR / "manifest.json"
