# RAG System Optimization - Session Management

## Initial Problem

The original code in `ask.py` was inefficient because for each question it was loading embeddings from scratch, loading the vectorstore from disk initializing the LLM model and building the RAG chain.

This meant that each question had high latency and unnecessary resource usage.

## Implemented Solution

### 1. Session System with Intelligent Caching

A new `RAGSession` class has been created in `atlasqaxai/rag/session.py` that:

- **Keeps in memory** all loaded RAG components
- **Automatically detects** when components need to be reloaded
- **Invalidates the cache** when necessary

### 2. Automatic Change Detection

The session detects changes in:

- **Index files**: Monitors `index.faiss` and `index.pkl` by modification time
- **Configuration**: Detects changes in environment variables (models, parameters)
- **Component state**: Verifies if any component is missing

### 3. Manual Invalidation

Commands that modify the index now invalidate the session:

- **`ingest.py`**: Invalidates after adding new documents
- **`wipe.py`**: Invalidates after deleting the index
- **`rebuild.py`**: Already uses `wipe` + `ingest`, so it invalidates automatically

## Benefits

### **Improved Performance**
- **First question**: Initial loading (normal time)
- **Subsequent questions**: Immediate use of cached components
- **Significant reduction** in latency for consecutive questions

### **Automatic Change Detection**
- No need to restart the application after indexing
- Automatic reload when index changes are detected
- Maintains data consistency

### **Flexibility**
- Works with CLI and Streamlit interfaces
- Manual invalidation available if needed
- Detailed logging for debugging

### **Full Compatibility**
- No changes required in existing UI code
- Existing commands work the same as before
- Backward-compatible API

## Usage

### Automatic (Recommended)
```python
# In ask.py - now optimized
from ..rag import session

def run(question: str):
    rag_session = session.get_session()
    chain = rag_session.get_chain()  # Automatic caching
    response = chain.invoke(question)
    return response
```

### Manual (For special cases)
```python
from atlasqaxai.rag import session

# Force reload if necessary
session.get_session().force_reload()

# Check status
status = session.get_session().get_status()
print(status)
```