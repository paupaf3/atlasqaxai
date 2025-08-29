from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, UnstructuredPowerPointLoader, UnstructuredPDFLoader
import re

# https://python.langchain.com/docs/integrations/document_loaders/


def _extract_language_from_filename(file_path: Path) -> str:
    """Extract language code from filename pattern like 'nombre ES.pdf', 'nombre CA.docx', etc.

    Examples:
        'MANUAL HUESO 2025 ES.pdf' -> 'es'
        'documento CA.docx' -> 'ca' 
        'report EN.pptx' -> 'en'
        'archivo.pdf' -> 'es' (default)

    Returns:
        Language code (es, ca, en) or 'es' as default if no pattern found.
    """
    # Get filename without extension
    filename_without_ext = file_path.stem

    # Look for language pattern at the end of filename (space + 2 letters)
    # Pattern matches: " ES", " CA", " EN" at the end of filename
    pattern = r'\s+(ES|CA|EN)$'
    match = re.search(pattern, filename_without_ext, re.IGNORECASE)

    if match:
        lang_code = match.group(1).upper()
        # Map to standard language codes
        lang_mapping = {
            'ES': 'es',
            'CA': 'ca',
            'EN': 'en'
        }
        return lang_mapping.get(lang_code, 'es')

    # Default to Spanish if no language pattern found
    return 'es'


def _extract_pdf_with_tables(file_path: Path) -> List[Document]:
    """Extract PDF content with better table handling."""
    documents = []

    # Unstructured pdf
    try:
        # Detect language from filename
        language = _extract_language_from_filename(file_path)
        print(
            f"[loader] Detected language '{language}' for file: {file_path.name}")

        loader = UnstructuredPDFLoader(
            str(file_path),
            mode="elements",
            strategy="hi_res",  # Better for tables
            languages=[language]  # Specify language based on filename
        )
        return loader.load()
    except Exception as e:
        print(
            f"[loader] UnstructuredPDFLoader failed for {file_path.name}: {e}")


def _get_loader_for_file(file_path: Path):
    """Get the appropriate loader for a file based on its extension."""
    ext = file_path.suffix.lower()

    # https://python.langchain.com/docs/how_to/document_loader_pdf/
    if ext == ".pdf":
        # Use custom table-aware PDF extraction
        return None  # Will be handled by _extract_pdf_with_tables

    elif ext in {".txt", ".md"}:
        return TextLoader(str(file_path), encoding="utf-8")

    # https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/
    elif ext == ".docx":
        return Docx2txtLoader(str(file_path))

    # https://python.langchain.com/docs/integrations/document_loaders/microsoft_powerpoint/
    elif ext in {".pptx", ".ppt"}:
        # Detect language from filename
        language = _extract_language_from_filename(file_path)
        print(
            f"[loader] Detected language '{language}' for file: {file_path.name}")
        return UnstructuredPowerPointLoader(str(file_path), mode="elements", languages=[language])

    else:
        # Unknown file type
        return None


def _load_document(file_path: Path) -> List[Document]:
    """Load document from a file path."""
    try:
        # Special handling for PDFs with table extraction
        if file_path.suffix.lower() == ".pdf":
            return _extract_pdf_with_tables(file_path)

        # For other file types, use standard loaders
        loader = _get_loader_for_file(file_path)
        if loader is None:
            return []

        return loader.load()

    except Exception as e:
        print(f"[loader] Error loading {file_path.name}: {e}")
        return []


def _load_documents_from_dir(dir_path: Path) -> List[Document]:
    """Load documents from a directory."""
    documents = []

    for file_path in dir_path.glob("*"):
        if not file_path.is_file():
            continue

        try:
            # Special handling for PDFs with table extraction
            if file_path.suffix.lower() == ".pdf":
                documents.extend(_extract_pdf_with_tables(file_path))
                continue

            # For other file types, use standard loaders
            loader = _get_loader_for_file(file_path)
            if loader is None:
                # Unknown file type, skip
                continue

            documents.extend(loader.load())

        except Exception as e:
            print(f"[loader] Skipping {file_path.name}: {e}")

    return documents


def load_documents_path(path: Path) -> List[Document]:
    """Load documents from a path, and check if a path is a directory or a file path."""
    if path.is_dir():
        return _load_documents_from_dir(path)
    elif path.is_file():
        return _load_document(path)
    else:
        return []


def load_documents_from_paths(paths: List[Path]) -> List[Document]:
    """Load documents from a list of paths."""
    documents = []
    for path in paths:
        documents.extend(load_documents_path(path))
    return documents
