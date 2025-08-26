from typing import List
from bs4 import SoupStrainer
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader

# https://python.langchain.com/docs/how_to/document_loader_web/


DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def load_documents_from_webs(urls: List[str], user_agent: str = DEFAULT_UA) -> List[Document]:
    """Load and clean webpages into Documents."""
    docs: List[Document] = []

    for url in urls:
        try:
            loader = WebBaseLoader(
                web_paths=[url],

                # Adds a desktop User-Agent (many sites 403 otherwise)
                header_template={"User-Agent": user_agent},

                # Avoid loading unnecessary content like headers, footers, etc.
                # TODO this could be an input param to control and adapat to different page structures
                # bs_kwargs={"parse_only": SoupStrainer(
                #     name=("article", "main"))}
            )
            page_docs = loader.load()

            # Normalize metadata for nicer citations
            for d in page_docs:
                d.metadata["source"] = d.metadata.get("source", url)
                # keep citation shape [file:page]
                d.metadata.setdefault("page", "N/A")
            docs.extend(page_docs)

        except Exception as e:
            print(f"[loader] Skipping {url}: {e}")

    return docs
