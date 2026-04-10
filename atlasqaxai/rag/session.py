import hashlib
from typing import Optional

from ..utils import config, paths
from ..vectorstore import embeddings, store
from . import llm, pipeline


class RAGSession:
    """Manages RAG components with lazy loading and on-demand reload.

    Components are split so that lightweight callers (e.g. `summary`,
    `inspect`) can grab the vectorstore without paying for LLM startup,
    while `ask` lazily promotes the session to a full chain.
    """

    def __init__(self) -> None:
        self._embeddings = None
        self._vectorstore = None
        self._llm_model = None
        self._chain = None
        self._last_index_mtime: Optional[float] = None
        self._last_config_hash: Optional[str] = None

    # ---------- internal helpers ----------

    def _get_index_mtime(self) -> Optional[float]:
        faiss_path = paths.PERSIST_DIR / "index.faiss"
        pkl_path = paths.PERSIST_DIR / "index.pkl"
        if faiss_path.exists() and pkl_path.exists():
            return max(faiss_path.stat().st_mtime, pkl_path.stat().st_mtime)
        return None

    def _get_config_hash(self) -> str:
        # Stable across processes (unlike the built-in hash() which is
        # randomized by PYTHONHASHSEED).
        config_str = (
            f"{config.EMBEDDINGS_BACKEND}:{config.EMBEDDINGS_MODEL}:"
            f"{config.OLLAMA_MODEL}:{config.TOP_K}"
        )
        return hashlib.sha256(config_str.encode("utf-8")).hexdigest()

    def _invalidate_if_stale(self) -> None:
        """Drop cached components if the index file or config changed."""
        current_mtime = self._get_index_mtime()
        current_hash = self._get_config_hash()
        if (current_mtime != self._last_index_mtime
                or current_hash != self._last_config_hash):
            self._embeddings = None
            self._vectorstore = None
            self._llm_model = None
            self._chain = None
            self._last_index_mtime = current_mtime
            self._last_config_hash = current_hash

    def _ensure_embeddings(self):
        if self._embeddings is None:
            print("[RAGSession] Loading embeddings...")
            self._embeddings = embeddings.get_embeddings(
                config.EMBEDDINGS_BACKEND, config.EMBEDDINGS_MODEL)
        return self._embeddings

    def _ensure_vectorstore(self):
        if self._vectorstore is None:
            embeds = self._ensure_embeddings()
            print("[RAGSession] Loading vectorstore...")
            self._vectorstore = store.load_or_create_faiss(
                paths.PERSIST_DIR, embeds)
        return self._vectorstore

    def _ensure_llm(self):
        if self._llm_model is None:
            print("[RAGSession] Loading LLM...")
            self._llm_model = llm.get_llm(config.OLLAMA_MODEL)
        return self._llm_model

    def _ensure_chain(self):
        if self._chain is None:
            vs = self._ensure_vectorstore()
            llm_model = self._ensure_llm()
            print("[RAGSession] Building RAG chain...")
            self._chain = pipeline.build_chain(vs, llm_model, config.TOP_K)
        return self._chain

    # ---------- public API ----------

    def get_chain(self):
        """Get the RAG chain (loads embeddings + vectorstore + LLM lazily)."""
        self._invalidate_if_stale()
        return self._ensure_chain()

    def get_vectorstore(self):
        """Get the vectorstore without paying for LLM init."""
        self._invalidate_if_stale()
        return self._ensure_vectorstore()

    def force_reload(self) -> None:
        """Force a reload of all components on next access."""
        print("[RAGSession] Forcing reload of all components...")
        self._embeddings = None
        self._vectorstore = None
        self._llm_model = None
        self._chain = None
        self._last_index_mtime = None
        self._last_config_hash = None

    def get_status(self) -> dict:
        return {
            "embeddings_loaded": self._embeddings is not None,
            "vectorstore_loaded": self._vectorstore is not None,
            "llm_loaded": self._llm_model is not None,
            "chain_loaded": self._chain is not None,
            "last_index_mtime": self._last_index_mtime,
            "last_config_hash": self._last_config_hash,
        }


# Global session instance
_session = RAGSession()


def get_session() -> RAGSession:
    """Get the global RAG session instance."""
    return _session
