import faiss
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore


def _empty_faiss(embeddings) -> FAISS:
    dim = len(embeddings.embed_query("dim probe"))  # probe once
    index = faiss.IndexFlatL2(dim)
    return FAISS(embedding_function=embeddings, index=index,
                 docstore=InMemoryDocstore({}), index_to_docstore_id={})


def load_or_create_faiss(persist_dir: Path, embeddings) -> FAISS:
    faiss_path, pkl_path = persist_dir / "faiss.index", persist_dir / "faiss.pkl"
    if faiss_path.exists() and pkl_path.exists():
        return FAISS.load_local(str(persist_dir), embeddings, allow_dangerous_deserialization=True)
    return _empty_faiss(embeddings)


def upsert_documents(vs: FAISS, docs: List[Document], persist_dir: Path) -> None:
    if not docs:
        return
    vs.add_documents(docs)
    vs.save_local(str(persist_dir))


def wipe_index(persist_dir: Path) -> None:
    for p in [persist_dir / "faiss.index", persist_dir / "faiss.pkl", persist_dir / "manifest.json"]:
        if p.exists():
            p.unlink()
