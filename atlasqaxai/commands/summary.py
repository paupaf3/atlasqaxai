from collections import Counter
from ..vectorstore import store, embeddings
from ..utils import config, paths


def get_summary() -> str:
    """Get a summary of documents in the index."""
    try:
        # Load the vectorstore
        embeds = embeddings.get_embeddings(
            config.EMBEDDINGS_BACKEND,
            config.EMBEDDINGS_MODEL,
        )
        vs = store.load_or_create_faiss(paths.PERSIST_DIR, embeds)

        # Get documents from FAISS vectorstore
        docs = []

        # Method 1: Check if docstore has documents
        if hasattr(vs.docstore, '_dict') and vs.docstore._dict:
            docs = list(vs.docstore._dict.values())

        # Method 2: If _dict is empty, try to get documents via index_to_docstore_id
        elif hasattr(vs, 'index_to_docstore_id') and vs.index_to_docstore_id:
            for doc_id in vs.index_to_docstore_id.values():
                doc = vs.docstore.search(doc_id)
                if doc:
                    docs.append(doc)

        if not docs:
            return "No documents found in the index. Please ingest some documents first."

        # Count chunks by source
        counts = Counter([d.metadata.get("source", "Unknown") for d in docs])

        # Build summary message
        summary_lines = [
            f"**Index Summary** ({len(docs)} total chunks)",
            "",
            "**Documents in index:**"
        ]

        for src, count in counts.most_common():
            summary_lines.append(f"\n• {src}")

        summary_lines.extend([
            "",
            "Ask me anything about these documents!"
        ])

        return "\n".join(summary_lines)

    except Exception as e:
        return f"Could not load index summary: {e}\n\nPlease make sure documents are ingested and the index is properly built."


def run() -> None:
    """Print the index summary to console."""
    summary = get_summary()
    print(summary)
