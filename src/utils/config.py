import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
EMBEDDINGS_BACKEND = os.getenv("EMBEDDINGS_BACKEND")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")
TOP_K = int(os.getenv("TOP_K"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
