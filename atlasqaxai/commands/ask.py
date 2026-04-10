from ..rag import session


def run(question: str) -> dict:
    """Answer a question against the indexed documents.

    Returns the full chain output dict so callers (CLI, Streamlit) can
    surface the retrieved sources, not just the LLM string.
    """
    print(f"Asking question: {question}")

    chain = session.get_session().get_chain()
    result = chain.invoke(question)

    answer = result["answer"]
    docs = result.get("docs", [])

    print("\n" + str(answer.content))

    if docs:
        # Deduplicate by (source, page) so the citation list stays compact.
        seen = []
        for d in docs:
            key = (d.metadata.get("source", "?"), d.metadata.get("page", "N/A"))
            if key not in seen:
                seen.append(key)
        print("\nSources:")
        for src, page in seen:
            print(f"  - [{src}:{page}]")

    return result
