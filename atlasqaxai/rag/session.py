from typing import Optional
from ..utils import config, paths
from ..vectorstore import embeddings, store
from . import llm, pipeline


class RAGSession:
    """Manages RAG components with intelligent caching and reloading."""

    def __init__(self):
        self._embeddings = None
        self._vectorstore = None
        self._llm_model = None
        self._chain = None
        self._last_index_mtime = None
        self._last_config_hash = None

    def _get_index_mtime(self) -> Optional[float]:
        """Get the modification time of the index files."""
        faiss_path = paths.PERSIST_DIR / "index.faiss"
        pkl_path = paths.PERSIST_DIR / "index.pkl"

        if faiss_path.exists() and pkl_path.exists():
            return max(faiss_path.stat().st_mtime, pkl_path.stat().st_mtime)
        return None

    def _get_config_hash(self) -> str:
        """Get a hash of the current configuration."""
        config_str = f"{config.EMBEDDINGS_BACKEND}:{config.EMBEDDINGS_MODEL}:{config.OLLAMA_MODEL}:{config.TOP_K}"
        return str(hash(config_str))

    def _needs_reload(self) -> bool:
        """Check if components need to be reloaded."""
        current_mtime = self._get_index_mtime()
        current_config_hash = self._get_config_hash()

        # Check if index files changed
        if current_mtime != self._last_index_mtime:
            return True

        # Check if configuration changed
        if current_config_hash != self._last_config_hash:
            return True

        # Check if any component is missing
        if (self._embeddings is None or
            self._vectorstore is None or
            self._llm_model is None or
                self._chain is None):
            return True

        return False

    def _load_components(self):
        """Load or reload all RAG components."""
        print("[RAGSession] Loading/reloading components...")

        # Load embeddings
        print("[RAGSession] Loading embeddings...")
        self._embeddings = embeddings.get_embeddings(
            config.EMBEDDINGS_BACKEND, config.EMBEDDINGS_MODEL)

        # Load vectorstore
        print("[RAGSession] Loading vectorstore...")
        self._vectorstore = store.load_or_create_faiss(
            paths.PERSIST_DIR, self._embeddings)

        # Load LLM
        print("[RAGSession] Loading LLM...")
        self._llm_model = llm.get_llm(config.OLLAMA_MODEL)

        # Build chain
        print("[RAGSession] Building RAG chain...")
        self._chain = pipeline.build_chain(
            self._vectorstore, self._llm_model, config.TOP_K)

        # Update state tracking
        self._last_index_mtime = self._get_index_mtime()
        self._last_config_hash = self._get_config_hash()

        print("[RAGSession] Components loaded successfully.")

    def get_chain(self):
        """Get the RAG chain, loading/reloading if necessary."""
        if self._needs_reload():
            self._load_components()
        return self._chain

    def get_vectorstore(self):
        """Get the vectorstore, loading/reloading if necessary."""
        if self._needs_reload():
            self._load_components()
        return self._vectorstore

    def force_reload(self):
        """Force a reload of all components."""
        print("[RAGSession] Forcing reload of all components...")
        self._embeddings = None
        self._vectorstore = None
        self._llm_model = None
        self._chain = None
        self._last_index_mtime = None
        self._last_config_hash = None

    def get_status(self) -> dict:
        """Get the current status of the session."""
        return {
            "components_loaded": all([
                self._embeddings is not None,
                self._vectorstore is not None,
                self._llm_model is not None,
                self._chain is not None
            ]),
            "last_index_mtime": self._last_index_mtime,
            "last_config_hash": self._last_config_hash,
            "needs_reload": self._needs_reload()
        }


# Global session instance
_session = RAGSession()


def get_session() -> RAGSession:
    """Get the global RAG session instance."""
    return _session
