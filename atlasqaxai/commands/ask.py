from ..utils import config
from ..rag import session


def run(question: str) -> None:
    print(f"Asking question: {question}")

    # Get the session and chain (will load/reload if necessary)
    rag_session = session.get_session()
    chain = rag_session.get_chain()

    if False:  # DEBUG
        vectorstore = rag_session.get_vectorstore()
        docs = vectorstore.similarity_search(question, k=config.TOP_K)
        print(f"[debug] retrieved {len(docs)} chunks")
        for d in docs[:3]:
            print(
                f"[{d.metadata.get('source')}:{d.metadata.get('page')}] {d.page_content[:200]}")

    response = chain.invoke(question)
    print("\n" + str(response.content))
    return response
