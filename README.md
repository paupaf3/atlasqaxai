# AtlasQAX.ai
AtlasQAX.ai is an intelligent Question Answering system that delivers **accurate, explainable answers** from multiple data sources.  
Starting with document-based knowledge retrieval, it is designed to scale towards **databases, APIs, and Microsoft Dataverse** integration.

By combining QA, X (Explainability), and AI, AtlasQAX.ai aims to become a data companion that not only answers but also helps users trust and interpret the information it provides.

## Key Features
- **Natural Language QA** → Ask questions in plain language.  
- **Explainable AI** → Get not only answers, but also transparent reasoning.  
- **Multi-source Integration** → From unstructured documents to structured data platforms.  
- **Scalable Design** → Flexible architecture to grow with your data needs.  

## Vision
AtlasQAX.ai combines *QA*, *X (Explainability)*, and *AI* to build a **data companion** you can trust, an agent that not only answers, but also helps you **understand and interpret** the information behind each response.

---

## Tech Stack & Libraries
### Core Orchestration
- **LangChain** — High-level framework to compose LLM/RAG pipelines (load → split → embed → retrieve → generate).  
  Docs: [python.langchain.com](https://python.langchain.com) · GitHub: [langchain-ai/langchain](https://github.com/langchain-ai/langchain)

<!-- - **langchain-community** — Community integrations (document loaders, vector stores, retrievers) used by the project.  
  PyPI: [langchain-community](https://pypi.org/project/langchain-community/) · Source: [monorepo packages](https://github.com/langchain-ai/langchain/tree/master/libs)

- **langchain-ollama** — LangChain bindings for **Ollama**: `ChatOllama` (LLM) and `OllamaEmbeddings` (local embeddings).  
  Docs: [Ollama in LangChain](https://python.langchain.com/docs/integrations/llms/ollama) · PyPI: [langchain-ollama](https://pypi.org/project/langchain-ollama/) -->

### Text Processing
<!-- - **langchain-text-splitters** — Robust chunking utilities (e.g., `RecursiveCharacterTextSplitter`) to keep context coherent.  
  Docs: [Text splitters](https://python.langchain.com/docs/how_to#text-splitters) · PyPI: [langchain-text-splitters](https://pypi.org/project/langchain-text-splitters/) -->

- **pypdf** — PDF parsing/extraction used by the PDF loader.  
  Docs: [pypdf.readthedocs.io](https://pypdf.readthedocs.io/) · PyPI: [pypdf](https://pypi.org/project/pypdf/)

- **python-docx** — DOCX reader to extract text from Word documents.  
  Docs: [python-docx.readthedocs.io](https://python-docx.readthedocs.io/) · PyPI: [python-docx](https://pypi.org/project/python-docx/)

### Embeddings & Retrieval
- **FAISS (faiss-cpu)** — Fast vector index for similarity search; persisted locally in `index/`.  
  GitHub: [facebookresearch/faiss](https://github.com/facebookresearch/faiss) · PyPI: [faiss-cpu](https://pypi.org/project/faiss-cpu/)

<!-- - **sentence-transformers** *(optional)* — Local embedding & reranking models (e.g., `all-MiniLM-L6-v2`, `BAAI/bge-small-en-v1.5`).  
  Website: [sbert.net](https://www.sbert.net/) · PyPI: [sentence-transformers](https://pypi.org/project/sentence-transformers/) -->

### Local LLM Runtime
- **Ollama** — Local model runner that serves chat models (e.g., Llama 3) and embedding models (e.g., `nomic-embed-text`) entirely offline.  
  Site: [ollama.com](https://ollama.com) · Models: [ollama.com/library](https://ollama.com/library)

### Configuration & Utilities
- **python-dotenv** — Loads settings from `.env` (e.g., model names, chunk sizes) to keep code clean and configurable.  
  PyPI: [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Notes
- **Local-only by default:** AtlasQAX.ai runs fully offline using Ollama for both LLM and (optionally) embeddings.
<!-- - **Swap components easily:** You can switch embeddings (Ollama ↔︎ Sentence-Transformers) or vector stores (FAISS ↔︎ others) with minimal code changes. -->
<!-- - **Incremental ingestion:** The structure supports hashing & manifests so you only re-embed changed files. -->

