
from . import prompt
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


def build_chain(vectorstore, llm, top_k: int):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    chain = (
        {
            "question": RunnablePassthrough(),
            "context": retriever | RunnableLambda(prompt.format_docs),
        }
        | prompt.PROMPT
        | llm
    )

    return chain
