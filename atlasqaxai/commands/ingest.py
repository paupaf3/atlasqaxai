from typing import List
from pathlib import Path
from langchain_core.documents import Document

from ..loaders import files, webs
from ..utils import paths, config
from ..processing import splitter, hashing
from ..vectorstore import store, embeddings


def _get_lines_text_file(file_path: Path) -> List[str]:
    """Read lines from a text file and return them as a list of strings."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return f.read().splitlines()
    except Exception as e:
        print(f"[loader] Error reading {file_path.name}: {e}")
        return []


def _load_documents():
    # Process files/docs from DATA_DIR
    docs_data_dir = files.load_documents_path(paths.DATA_DIR)

    if not docs_data_dir:
        print(f"[loader] No documents found in {paths.DATA_DIR}")

    # Process files/docs from DATA_DOCS_PATHS
    # Read DATA_DOCS_PATHS from txt file
    docs_paths = _get_lines_text_file(paths.DATA_DOCS_PATHS_TEXT_FILE)
    docs_paths = files.load_documents_from_paths(
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

    return docs_data_dir + docs_paths + docs_webs


def run() -> None:
    print("Ingesting documents...")

    # Load documents
    docs = _load_documents()

    # If no documents, log and return
    if not docs:
        print("[loader] No documents to ingest. Add files, paths or URLs, and retry.")
        return

    # Splitter
    text_splitter = splitter.make_splitter(
        config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    chunks: List[Document] = text_splitter.split_documents(docs)
    chunks = splitter.apply_metadata_defaults(chunks)

    # Embeddings
    embeds = embeddings.get_embeddings(
        config.EMBEDDINGS_BACKEND, config.EMBEDDINGS_MODEL)
    vs = store.load_or_create_faiss(paths.PERSIST_DIR, embeds)
    manifest = hashing.load_manifest(paths.MANIFEST_PATH)
    new_chunks = []
    seen = set()

    for ch in chunks:
        src = ch.metadata.get("source", "unknown")
        seen.add(src)
        # Only hash original files once (page chunks share same source name)
        # Use file path from doc metadata if available; fall back to DATA_DIR/src
        path = Path(paths.DATA_DIR) / src
        if not path.exists():  # for safety with loaders that embed full path
            # skip incremental check if unknown
            new_chunks.append(ch)
            continue
        h = hashing.file_sha256(path)
        if manifest["files"].get(src) != h:
            new_chunks.append(ch)
            manifest["files"][src] = h

    store.upsert_documents(vs, new_chunks, paths.PERSIST_DIR)
    hashing.save_manifest(paths.MANIFEST_PATH, manifest)
    print(f"→ Ingest complete. {len(new_chunks)} chunks added/updated.")
