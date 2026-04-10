import os


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
EMBEDDINGS_BACKEND = os.getenv("EMBEDDINGS_BACKEND", "ollama")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "bge-m3")
PROMPTS = os.getenv("PROMPTS", "default_en")
TOP_K = int(os.getenv("TOP_K", "10"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1100"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
