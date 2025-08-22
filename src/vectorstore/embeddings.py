from typing import Any
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings(backend: str, ollama_model: str, hf_model: str) -> Any:
    if backend.lower() == "hf":
        return HuggingFaceEmbeddings(model_name=hf_model)
    elif backend.lower() == "ollama":
        return OllamaEmbeddings(model=ollama_model)
    # default - return exception bad config
    raise ValueError(f"Unknown backend: {backend}")
