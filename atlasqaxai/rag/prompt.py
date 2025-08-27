from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
from ..utils import config


# Read system prompt from markdown file
SYSTEM = (Path(__file__).parent.parent / "prompts" /
          config.PROMPTS / "system_prompt.md").read_text().strip()

USER = (Path(__file__).parent.parent / "prompts" /
        config.PROMPTS / "user_prompt.md").read_text().strip()

PROMPT = ChatPromptTemplate.from_messages(
    [("system", SYSTEM), ("user", USER)])


def format_docs(docs):
    parts = []
    for d in docs:
        parts.append(
            f"[{d.metadata.get('source', '?')}:{d.metadata.get('page', 'N/A')}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)
