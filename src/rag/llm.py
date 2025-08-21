from langchain_ollama import ChatOllama


def get_llm(model: str = "llama3"):
    # temperature=0 always pick the max-prob token
    # That should give the same output for the same prompt and model state.
    # But a few things can still introduce variation

    # So temperature=0 makes the model """"""""deterministic""""""""", hence the """"""""""
    return ChatOllama(model=model, temperature=0)
