from pathlib import Path
from typing import List
from langhcain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredPowerPointLoader


# TODO from docs, we will only load text, so maybe with should consider
# TODO improving this with some image-to-text processing, or file-relation-text storing

# Review all links, some of the loaders may require installation of extra packages

# https://python.langchain.com/docs/integrations/document_loaders/
def load_documents_from_dir(dir_path: Path) -> List[Document]:
    """Load documents from a directory."""
    documents = []

    for file_path in dir_path.glob("*"):
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()

        try:
            # https://python.langchain.com/docs/how_to/document_loader_pdf/
            if ext == ".pdf":
                loader = PyPDFLoader(str(file_path))

            elif ext in {".txt", ".md"}:
                loader = TextLoader(str(file_path), encoding="utf-8")

            # https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/
            elif ext == ".docx":
                loader = Docx2txtLoader(str(file_path))

            # https://python.langchain.com/docs/integrations/document_loaders/microsoft_powerpoint/
            elif ext in {".pptx", ".ppt"}:
                loader = UnstructuredPowerPointLoader(
                    str(file_path), mode="elements")

            else:
                # Unknown file type, skip
                continue

            documents.extend(loader.load())

        except Exception as e:
            print(f"[loader] Skipping {file_path.name}: {e}")

    return documents
