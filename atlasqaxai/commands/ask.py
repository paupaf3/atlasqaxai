from ..utils import config, paths
from ..vectorstore import embeddings, store
from ..rag import llm, pipeline


def run(question: str) -> None:
    print(f"Asking question: {question}")
    embeds = embeddings.get_embeddings(
        config.EMBEDDINGS_BACKEND, config.EMBEDDINGS_MODEL)
    vectorstore = store.load_or_create_faiss(paths.PERSIST_DIR, embeds)
    llm_model = llm.get_llm(config.OLLAMA_MODEL)
    chain = pipeline.build_chain(vectorstore, llm_model, config.TOP_K)

    if False:  # DEBUG
        docs = vectorstore.similarity_search(question, k=config.TOP_K)
        print(f"[debug] retrieved {len(docs)} chunks")
        for d in docs[:3]:
            print(
                f"[{d.metadata.get('source')}:{d.metadata.get('page')}] {d.page_content[:200]}")

    response = chain.invoke(question)
    print("\n" + str(response.content))
