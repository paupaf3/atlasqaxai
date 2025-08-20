from pathlib import Path
from typing import List
from langhcain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredPowerPointLoader
def load_documents_from_dir(dir_path: Path) -> List[Document]:
    """Load documents from a directory."""
    documents = []

    for file_path in dir_path.glob("*"):
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(str(file_path))

            elif ext in {".txt", ".md"}:
                loader = TextLoader(str(file_path), encoding="utf-8")
            elif ext == ".docx":
                loader = Docx2txtLoader(str(file_path))

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
