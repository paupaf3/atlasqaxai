import aiohttp
from lightrag.utils import EmbeddingFunc

OLLAMA_BASE_URL = "http://localhost:11434"


def create_llm_model_func(
    model: str = "llama3.1:8b",
    base_url: str = OLLAMA_BASE_URL,
    temperature: float = 0.4,
):
    async def llm_model_func(
        prompt, system_prompt=None, history_messages=None, **kwargs
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": temperature},
                },
            ) as resp:
                data = await resp.json()
                return data["message"]["content"]

    return llm_model_func


def create_embedding_func(
    model: str = "bge-m3",
    base_url: str = OLLAMA_BASE_URL,
    embedding_dim: int = 1024,
):
    async def embed_func(texts):
        if isinstance(texts, str):
            texts = [texts]
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/api/embed",
                json={"model": model, "input": texts},
            ) as resp:
                data = await resp.json()
                return data["embeddings"]

    return EmbeddingFunc(
        embedding_dim=embedding_dim,
        max_token_size=8192,
        func=embed_func,
    )


def create_vision_model_func(
    model: str = "llama3.2-vision",
    base_url: str = OLLAMA_BASE_URL,
    temperature: float = 0.4,
):
    async def vision_model_func(
        prompt,
        system_prompt=None,
        history_messages=None,
        image_data=None,
        messages=None,
        **kwargs,
    ):
        if messages:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/api/chat",
                    json={
                        "model": model,
                        "messages": messages,
                        "stream": False,
                        "options": {"temperature": temperature},
                    },
                ) as resp:
                    data = await resp.json()
                    return data["message"]["content"]
        elif image_data:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/api/chat",
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt or ""},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_data}"
                                        },
                                    },
                                ],
                            },
                        ],
                        "stream": False,
                        "options": {"temperature": temperature},
                    },
                ) as resp:
                    data = await resp.json()
                    return data["message"]["content"]
        else:
            return await create_llm_model_func(model, base_url, temperature)(
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                **kwargs,
            )

    return vision_model_func
