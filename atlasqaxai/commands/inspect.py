from collections import Counter

from ..rag import session
from .summary import _iter_indexed_documents


def run() -> None:
    print("Inspecting the index...")

    vs = session.get_session().get_vectorstore()
    docs = list(_iter_indexed_documents(vs))

    print(f"Chunks totales en el índice: {len(docs)}")

    if not docs:
        print(
            "No documents found in the index. The index might be empty or there might be an issue loading it.")
        return

    counts = Counter(d.metadata.get("source", "?") for d in docs)
    print("\nChunks por archivo (source):")
    for src, n in counts.most_common():
        print(f"  {src}: {n}")
