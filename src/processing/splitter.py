from langchain_text_splitters import RecursiveCharacterTextSplitter
from langhcain_core.documents import Document
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
        d.metadata.setdefault("source", d.metadata.get("source") or d.metadata.get(
            "file_path") or d.metadata.get("path") or "unknown")
        if "page" not in d.metadata:
            d.metadata["page"] = d.metadata.get("page_label") or "N/A"
        # keep only filename in source for pretty citations
        # REVIEW I think is a good option for a company to know where the answer comes from
        src = Path(str(d.metadata["source"])).name
        d.metadata["source"] = src
    return chunks
