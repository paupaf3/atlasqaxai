from typing import List
from pathlib import Path
from langchain_core.documents import Document

from ..loaders import files, webs
from ..utils import paths, config
from ..processing import splitter, hashing
from ..vectorstore import store, embeddings
from ..rag import session


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
    if not config.EMBEDDINGS_BACKEND or not config.EMBEDDINGS_MODEL:
        raise ValueError(
            "Missing EMBEDDINGS_BACKEND or EMBEDDINGS_MODEL in environment. Check your .env file."
        )

    embeds = embeddings.get_embeddings(
        config.EMBEDDINGS_BACKEND, config.EMBEDDINGS_MODEL)
    vs = store.load_or_create_faiss(paths.PERSIST_DIR, embeds)
    manifest = hashing.load_manifest(paths.MANIFEST_PATH)

    print(f"[ingest] Chunks totales para el índice: {len(chunks)}")

    # Determine which sources are new/changed since last ingest.
    # We key the manifest by `source` (basename for files / URL for webs) and
    # use `source_path` (full path) only to locate the file for hashing.
    changed_files: set[str] = set()
    unique_sources: set[tuple[str, str]] = {
        (ch.metadata.get("source", "unknown"),
         ch.metadata.get("source_path", ""))
        for ch in chunks
    }
    print(f"[ingest] Unique sources to check: {len(unique_sources)}")

    for src, src_path in unique_sources:
        # Web sources: hashing the URL is meaningless; treat as always changed.
        # Old vectors are deleted below, so re-ingest is idempotent.
        if src_path.startswith(("http://", "https://")):
            changed_files.add(src)
            continue

        candidate = Path(src_path) if src_path else Path(paths.DATA_DIR) / src
        if not candidate.exists():
            candidate = Path(paths.DATA_DIR) / src
        if not candidate.exists():
            # Can't hash it; treat as changed so we don't silently miss updates.
            changed_files.add(src)
            continue

        h = hashing.file_sha256(candidate)
        if manifest["files"].get(src) != h:
            changed_files.add(src)
            manifest["files"][src] = h

    new_chunks: List[Document] = [
        ch for ch in chunks
        if ch.metadata.get("source", "unknown") in changed_files
    ]

    print(f"[ingest] New/updated chunks to write: {len(new_chunks)}")

    # Delete stale vectors for the files that changed BEFORE adding new ones.
    # Without this step, every re-ingest of an updated file would leave
    # outdated chunks in the index alongside the new ones.
    if changed_files:
        deleted = store.delete_by_sources(vs, changed_files)
        if deleted:
            print(f"[ingest] Removed {deleted} stale vectors for changed sources")

    print("[ingest] Writing vectors to FAISS index...")
    store.upsert_documents(vs, new_chunks, paths.PERSIST_DIR)
    print("[ingest] Saving manifest...")
    hashing.save_manifest(paths.MANIFEST_PATH, manifest)
    print("[ingest] Manifest saved.")

    # Invalidate the session cache since the index has been updated
    if new_chunks:
        session.get_session().force_reload()

    print(f"→ Ingest complete. {len(new_chunks)} chunks added/updated.")
