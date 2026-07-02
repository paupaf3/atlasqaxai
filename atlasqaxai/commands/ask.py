from ..rag import session
from ..utils import config


def run(question: str, mode: str | None = None) -> str:
    query_mode = mode or config.QUERY_MODE
    print(f"Query mode: {query_mode}")
    print(f"Question: {question}")

    rag = session.get_session().get_rag()
    answer = rag.query(question, mode=query_mode)

    print(f"\n{answer}")
    return answer
