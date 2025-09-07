# AtlasQAX.ai
AtlasQAX.ai is an intelligent Question Answering system that delivers **accurate, explainable answers** from multiple data sources.  
Starting with document-based knowledge retrieval, it is designed to scale towards **databases, APIs, and Microsoft Dataverse** integration.

By combining QA, X (Explainability), and AI, AtlasQAX.ai aims to become a data companion that not only answers but also helps users trust and interpret the information it provides.

---
## Project Status
AtlasQAX.ai is currently in an early development phase.
The basic functionality—document ingestion and natural language Q&A—is already working, but many planned features are still in progress.

A lot of improvements can be made in areas such as document ingestion, embeddings generation, and retrieval quality, which are active focus points for future updates.

Over the coming iterations, the project will expand to include:
- More robust multi-language support
- Enhanced explainability and audit logging
- Database and API connectors
- Improved interfaces (streamlined web UI, better CLI experience)
- Performance optimizations for larger document sets
- Working and tuning the 

This repository is actively evolving, and the roadmap involves significant improvements in both functionality and usability. Contributions, feedback, and ideas are welcome!

---
## Key Features
- **Natural Language QA** → Ask questions in plain language.  
- **Explainable AI** → Get not only answers, but also transparent reasoning.  
- **Multi-source Integration** → From unstructured documents, web pages and structured data platforms.  
- **Scalable Design** → Flexible architecture to grow with your data needs.  
- **Multiple Interfaces** → Choose between CLI and web interface (Streamlit).

---
## Usage
### Web Interface (Streamlit)
For a user-friendly web interface:
```bash
#Through the main application
python -m atlasqaxai streamlit
```

The web interface provides:
- Interactive chat interface for asking questions
- System management tools (ingest, rebuild, inspect, summary, wipe index)
- Real-time responses with chat history
- Visual feedback and error handling

### Command Line Interface (CLI)
For traditional command-line usage:
```bash
# Interactive Q&A mode (default)
python -m atlasqaxai

# Ask a single question
python -m atlasqaxai ask "What is the main topic of the documents?"

# System management commands
python -m atlasqaxai ingest     # Index new/changed documents
python -m atlasqaxai rebuild    # Rebuild entire index
python -m atlasqaxai inspect    # Inspect current index (detailed)
python -m atlasqaxai summary    # Show documents summary (user-friendly)
python -m atlasqaxai wipe       # Delete index
```  
---
## Vision
AtlasQAX.ai combines *QA*, *X (Explainability)*, and *AI* to build a **data companion** you can trust, an agent that not only answers, but also helps you **understand and interpret** the information behind each response.

---
## Available Commands
### Data Management
- **`ingest`** - Index new or changed documents from your `data/files/` directory
- **`rebuild`** - Completely rebuild the index from scratch (useful after configuration changes)
- **`wipe`** - Delete the entire index (requires confirmation)

### Information & Inspection
- **`summary`** - Show a user-friendly summary of documents in the index with chunk counts
- **`inspect`** - Display detailed technical information about the index structure

### Question Answering
- **`ask`** - Ask questions about your documents (interactive mode by default)

### Web Interface
- **`app`** - Launch the Streamlit web interface

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

### Web Interface
- **Streamlit** — Modern web framework for creating interactive data applications with Python.  
  Site: [streamlit.io](https://streamlit.io) · PyPI: [streamlit](https://pypi.org/project/streamlit/)

---

## System Requirements
### System Dependencies (not pip packages)
Before installing Python dependencies, make sure to install these system packages:

```bash
sudo apt-get update
sudo apt-get install -y libmagic-dev poppler-utils tesseract-ocr libreoffice tesseract-ocr-spa tesseract-ocr-cat
```

**What these packages provide:**
- **`libmagic-dev`** - File type detection library
- **`poppler-utils`** - PDF processing utilities for better PDF parsing
- **`libreoffice`** - Office document processing capabilities

## Notes
- **Local-only by default:** AtlasQAX.ai runs fully offline using Ollama for both LLM and embeddings.
<!-- - **Swap components easily:** You can switch embeddings (Ollama ↔︎ Sentence-Transformers) or vector stores (FAISS ↔︎ others) with minimal code changes. -->
<!-- - **Incremental ingestion:** The structure supports hashing & manifests so you only re-embed changed files. -->
