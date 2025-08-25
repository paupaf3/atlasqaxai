from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path


# Read system prompt from markdown file
SYSTEM = (Path(__file__).parent / "system_prompt.md").read_text().strip()

USER_TPL = "Question: {question}\n\nCONTEXT:\n{context}\n"

PROMPT = ChatPromptTemplate.from_messages(
    [("system", SYSTEM), ("user", USER_TPL)])
