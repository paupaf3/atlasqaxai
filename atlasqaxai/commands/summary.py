from collections import Counter

from ..rag import session


def _iter_indexed_documents(vs):
    """Yield every Document currently held by the FAISS docstore."""
    docstore_dict = getattr(vs.docstore, "_dict", None)
    if docstore_dict:
        yield from docstore_dict.values()
        return

    # Fallback path used by some FAISS configurations.
    for doc_id in getattr(vs, "index_to_docstore_id", {}).values():
        doc = vs.docstore.search(doc_id)
        if doc:
            yield doc


def get_summary() -> str:
    """Return a human-readable summary of the documents in the index."""
    try:
        vs = session.get_session().get_vectorstore()
        docs = list(_iter_indexed_documents(vs))

        if not docs:
            return "No documents found in the index. Please ingest some documents first."

        counts = Counter(d.metadata.get("source", "Unknown") for d in docs)

        lines = [
            f"**Index Summary** ({len(docs)} total chunks across {len(counts)} documents)",
            "",
            "**Documents in index:**",
        ]
        for src, count in counts.most_common():
            lines.append(f"\n• {src} — {count} chunks")
        lines.extend(["", "Ask me anything about these documents!"])
        return "\n".join(lines)

    except Exception as e:
        return (
            f"Could not load index summary: {e}\n\n"
            "Please make sure documents are ingested and the index is properly built."
        )


def run() -> None:
    """Print the index summary to console."""
    print(get_summary())
