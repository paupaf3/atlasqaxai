import faiss
import time
from pathlib import Path
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore


def _empty_faiss(embeddings) -> FAISS:
    dim = len(embeddings.embed_query("dim probe"))  # probe once
    index = faiss.IndexFlatL2(dim)
    return FAISS(embedding_function=embeddings, index=index,
                 docstore=InMemoryDocstore({}), index_to_docstore_id={})


def load_or_create_faiss(persist_dir: Path, embeddings) -> FAISS:
    faiss_path, pkl_path = persist_dir / "index.faiss", persist_dir / "index.pkl"
    if faiss_path.exists() and pkl_path.exists():
        return FAISS.load_local(str(persist_dir), embeddings, allow_dangerous_deserialization=True)
    return _empty_faiss(embeddings)


def _sanitize_documents(docs: List[Document]) -> Tuple[List[Document], int]:
    sanitized_docs: List[Document] = []
    skipped_empty = 0

    for doc in docs:
        content = (doc.page_content or "").replace("\x00", " ").strip()
        if not content:
            skipped_empty += 1
            continue

        if content != doc.page_content:
            sanitized_docs.append(
                Document(page_content=content, metadata=doc.metadata))
        else:
            sanitized_docs.append(doc)

    return sanitized_docs, skipped_empty


def upsert_documents(vs: FAISS, docs: List[Document], persist_dir: Path, batch_size: int = 64) -> None:
    if not docs:
        return
    docs, skipped_empty = _sanitize_documents(docs)
    if skipped_empty:
        print(
            f"[ingest] Skipped {skipped_empty} empty chunks before embedding")
    if not docs:
        print("[ingest] No valid chunks to upsert after sanitization")
        return

    total = len(docs)
    start = time.time()
    added = 0
    skipped_failed = 0

    for offset in range(0, total, batch_size):
        batch = docs[offset:offset + batch_size]
        batch_num = (offset // batch_size) + 1
        batch_total = (total + batch_size - 1) // batch_size
        print(
            f"[ingest] Upserting batch {batch_num}/{batch_total} ({len(batch)} chunks)")
        try:
            vs.add_documents(batch)
            added += len(batch)
        except Exception as batch_error:
            print(
                f"[ingest] Batch {batch_num} failed, retrying per chunk: {batch_error}")
            for doc in batch:
                try:
                    vs.add_documents([doc])
                    added += 1
                except Exception as doc_error:
                    skipped_failed += 1
                    src = doc.metadata.get("source", "unknown")
                    page = doc.metadata.get("page", "N/A")
                    print(
                        f"[ingest] Skipped chunk {src}:{page} due to embedding error: {doc_error}")

    elapsed = time.time() - start
    print(
        f"[ingest] Vector upsert done: added={added}, skipped={skipped_failed}, total={total}, time={elapsed:.1f}s")

    if added > 0:
        vs.save_local(str(persist_dir))
    else:
        print("[ingest] No vectors were added; skipping FAISS save")


def wipe_index(persist_dir: Path) -> None:
    for p in [persist_dir / "index.faiss", persist_dir / "index.pkl", persist_dir / "manifest.json"]:
        if p.exists():
            p.unlink()
