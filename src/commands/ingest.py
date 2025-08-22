from typing import List
from pathlib import Path

from loaders import files, webs
from utils import paths


def _get_lines_text_file(file_path: Path) -> List[str]:
    """Read lines from a text file and return them as a list of strings."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return f.read().splitlines()
    except Exception as e:
        print(f"[loader] Error reading {file_path.name}: {e}")
        return []


def run() -> None:
    print("Ingesting documents...")

    # Process files/docs from DATA_DIR
    docs_data_dir = files.load_documents_path(paths.DATA_DIR)

    if not docs_data_dir:
        print(f"[loader] No documents found in {paths.DATA_DIR}")

    # Process files/docs from DATA_DOCS_PATHS
    # Read DATA_DOCS_PATHS from txt file
    docs_paths = _get_lines_text_file(paths.DATA_DOCS_PATHS_TEXT_FILE)
    docs_paths = files.load_documents_paths(
        [Path(path) for path in docs_paths])

    if not docs_paths:
        print(
            f"[loader] No documents found in {paths.DATA_DOCS_PATHS_TEXT_FILE}")

    # Process webs from DATA_WEBS_PATHS
    webs_urls = _get_lines_text_file(paths.DATA_WEBS_PATHS_TEXT_FILE)
    docs_webs = webs.load_documents_from_webs(webs_urls)

    if not docs_webs:
        print(
            f"[loader] No documents found in {paths.DATA_WEBS_PATHS_TEXT_FILE}")

    docs = docs_data_dir + docs_paths + docs_webs

    if not docs:
        print("[loader] No documents to ingest. Add files, paths or URLs, and retry.")
        return

    # Splitter

    # Embeddings

    # Manifest
