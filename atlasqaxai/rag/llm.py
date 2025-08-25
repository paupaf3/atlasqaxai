from langchain_ollama import ChatOllama


def get_llm(model: str = "llama3.1:8b"):
    # temperature=0 always pick the max-prob token
    # That should give the same output for the same prompt and model state.
    # But a few things can still introduce variation

    # So temperature=0 makes the model """"""""deterministic""""""""", hence the """"""""""

    # There also some other important params like top_k or top_p, to adjust answers to more conservative or more creative and diverse ways
    # Read more at:
    # https://python.langchain.com/api_reference/ollama/chat_models/langchain_ollama.chat_models.ChatOllama.html#langchain_ollama.chat_models.ChatOllama.temperature
    return ChatOllama(model=model, temperature=0.4)
