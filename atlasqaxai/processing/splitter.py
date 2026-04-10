from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
from typing import List


def make_splitter(chunk_size: int, chunk_overlap: int) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""],
    )


def apply_metadata_defaults(chunks: List[Document]) -> List[Document]:
    for d in chunks:
        original_source = (
            d.metadata.get("source")
            or d.metadata.get("file_path")
            or d.metadata.get("path")
            or "unknown"
        )
        # Preserve the full original location (path or URL) so ingest can
        # locate the file for hash-based change detection.
        d.metadata["source_path"] = str(original_source)

        if "page" not in d.metadata:
            d.metadata["page"] = d.metadata.get("page_label") or "N/A"

        # `source` is the user-facing citation key: full URL for web sources,
        # filename only for file sources.
        src_str = str(original_source)
        if src_str.startswith(("http://", "https://")):
            d.metadata["source"] = src_str
        else:
            d.metadata["source"] = Path(src_str).name
    return chunks
