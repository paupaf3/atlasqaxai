from collections import Counter
from ..vectorstore import store, embeddings
from ..utils import config, paths


def run() -> None:
    print("Inspecting the index...")

    # Add your inspection logic here
    embeds = embeddings.get_embeddings(
        config.EMBEDDINGS_BACKEND,
        config.EMBEDDINGS_MODEL,
    )

    vs = store.load_or_create_faiss(paths.PERSIST_DIR, embeds)

    # Get documents from FAISS vectorstore
    # Try different ways to access the documents
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

    print(f"Chunks totales en el índice: {len(docs)}")

    if docs:
        counts = Counter([d.metadata.get("source", "?") for d in docs])
        print("\nChunks por archivo (source):")
        for src, n in counts.most_common():
            print(f"  {src}: {n}")
    else:
        print("No documents found in the index. The index might be empty or there might be an issue loading it.")
