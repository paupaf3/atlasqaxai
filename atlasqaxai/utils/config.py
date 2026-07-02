import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "bge-m3")
VISION_MODEL = os.getenv("VISION_MODEL", "")

WORKING_DIR = os.getenv("WORKING_DIR", "./rag_storage")
PARSER = os.getenv("PARSER", "mineru")
PARSE_METHOD = os.getenv("PARSE_METHOD", "auto")

ENABLE_IMAGE_PROCESSING = os.getenv("ENABLE_IMAGE_PROCESSING", "true").lower() == "true"
ENABLE_TABLE_PROCESSING = os.getenv("ENABLE_TABLE_PROCESSING", "true").lower() == "true"
ENABLE_EQUATION_PROCESSING = os.getenv("ENABLE_EQUATION_PROCESSING", "true").lower() == "true"

QUERY_MODE = os.getenv("QUERY_MODE", "hybrid")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

DATA_DIR = os.getenv("DATA_DIR", "./data/files")
DATA_DOCS_PATHS_TEXT_FILE = os.getenv("DATA_DOCS_PATHS_TEXT_FILE", "./data/docs_paths.txt")
DATA_WEBS_PATHS_TEXT_FILE = os.getenv("DATA_WEBS_PATHS_TEXT_FILE", "./data/webs_paths.txt")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
