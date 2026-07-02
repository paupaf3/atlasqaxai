import os
from pathlib import Path
from typing import Optional

from raganything import RAGAnything

from ..utils import config
from . import adapter


class RAGSession:
    def __init__(self) -> None:
        self._rag: Optional[RAGAnything] = None

    def _ensure_rag(self) -> RAGAnything:
        if self._rag is None:
            print("[RAGSession] Initializing RAG-Anything...")
            self._rag = adapter.create_rag(
                working_dir=config.WORKING_DIR,
                parser=config.PARSER,
                parse_method=config.PARSE_METHOD,
                llm_model=config.OLLAMA_MODEL,
                embedding_model=config.EMBEDDINGS_MODEL,
                vision_model=config.VISION_MODEL or None,
                enable_image=config.ENABLE_IMAGE_PROCESSING,
                enable_table=config.ENABLE_TABLE_PROCESSING,
                enable_equation=config.ENABLE_EQUATION_PROCESSING,
                lightrag_kwargs={
                    "chunk_token_size": config.CHUNK_SIZE,
                    "chunk_overlap_token_size": config.CHUNK_OVERLAP,
                },
            )
        return self._rag

    def get_rag(self) -> RAGAnything:
        return self._ensure_rag()

    def force_reload(self) -> None:
        if self._rag is not None:
            self._rag.close()
            self._rag = None
        print("[RAGSession] Forcing reload on next access.")

    def get_status(self) -> dict:
        return {
            "rag_initialized": self._rag is not None,
            "working_dir": config.WORKING_DIR,
        }

    def storage_exists(self) -> bool:
        working = Path(config.WORKING_DIR)
        if not working.exists():
            return False
        return len(list(working.iterdir())) > 0


_session = RAGSession()


def get_session() -> RAGSession:
    return _session
