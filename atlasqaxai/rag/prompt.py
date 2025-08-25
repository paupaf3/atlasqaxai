from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path


# Read system prompt from markdown file
SYSTEM = (Path(__file__).parent / "system_prompt.md").read_text().strip()

USER_TPL = "Question: {question}\n\nCONTEXT:\n{context}\n"

PROMPT = ChatPromptTemplate.from_messages(
    [("system", SYSTEM), ("user", USER_TPL)])


def format_docs(docs):
    parts = []
    for d in docs:
        parts.append(
            f"[{d.metadata.get('source', '?')}:{d.metadata.get('page', 'N/A')}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)
