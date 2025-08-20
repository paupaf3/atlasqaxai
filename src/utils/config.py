import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
EMBEDDINGS_BACKEND = os.getenv("EMBEDDINGS_BACKEND", "ollama")
