from raganything import RAGAnything, RAGAnythingConfig
from .ollama import (
    create_llm_model_func,
    create_embedding_func,
    create_vision_model_func,
)


def create_rag(
    working_dir: str = "./rag_storage",
    parser: str = "mineru",
    parse_method: str = "auto",
    llm_model: str = "llama3.1:8b",
    embedding_model: str = "bge-m3",
    vision_model: str | None = None,
    enable_image: bool = True,
    enable_table: bool = True,
    enable_equation: bool = True,
    lightrag_kwargs: dict | None = None,
) -> RAGAnything:
    config = RAGAnythingConfig(
        working_dir=working_dir,
        parser=parser,
        parse_method=parse_method,
        enable_image_processing=enable_image,
        enable_table_processing=enable_table,
        enable_equation_processing=enable_equation,
    )

    llm_func = create_llm_model_func(model=llm_model)

    emb_func = create_embedding_func(model=embedding_model)

    vision_func = None
    if vision_model:
        vision_func = create_vision_model_func(model=vision_model)

    return RAGAnything(
        config=config,
        llm_model_func=llm_func,
        embedding_func=emb_func,
        vision_model_func=vision_func,
        lightrag_kwargs=lightrag_kwargs or {},
    )
