from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from . import prompt


def build_chain(vectorstore, llm, top_k: int):
    """Build a RAG chain that returns both the answer and the source docs.

    Invoking with a string question yields a dict:
        {
            "question": <str>,
            "docs":     <list[Document]>,   # what the retriever returned
            "answer":   <AIMessage>,        # the LLM response
        }
    Surfacing the docs alongside the answer is what makes the "X" in
    AtlasQAX (explainability) actually meaningful — callers can render
    citations from real metadata instead of trusting the model to do it.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    def _format_inputs(inputs: dict) -> dict:
        return {
            "question": inputs["question"],
            "context": prompt.format_docs(inputs["docs"]),
        }

    answer_chain = RunnableLambda(_format_inputs) | prompt.PROMPT | llm

    return (
        RunnableParallel(
            question=RunnablePassthrough(),
            docs=retriever,
        )
        | RunnablePassthrough.assign(answer=answer_chain)
    )
