import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Load environment variables
#load_dotenv()

# Base directories
BASE_DIR = Path(os.getcwd())
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_PATH = BASE_DIR / "chroma_db"
LOG_DIR = BASE_DIR / "logs"
UPLOAD_DIR = BASE_DIR / "data/uploads"

# Create directories
for directory in [DATA_DIR, CHROMA_DB_PATH, LOG_DIR, UPLOAD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ======================
# Embedding Settings
# ======================
EMBEDDING_MODEL = "mixedbread-ai/mxbai-embed-xsmall-v1"   # Lightweight & fast
EMBEDDING_DIMENSION = 384
DEVICE = "cpu"                                           # Change to "cuda" if GPU available

# ======================
# Retrieval Settings
# ======================
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 10
HYBRID_ALPHA = 0.65                                      # BM25 weight in hybrid search

# ======================
# ChromaDB Settings
# ======================
CHROMA_COLLECTION_NAME = "documents"
CHROMA_HNSW_SPACE = "cosine"

# ======================
# Session & Upload Settings
# ======================
MAX_SESSIONS = 20
MAX_UPLOAD_SIZE_MB = 50

# ======================
# RAG Behavior
# ======================
USE_RERANKER = True
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
ENABLE_HYDE = False                                      
ENABLE_GRAPH_RAG = False                                 

# ======================
# Logging
# ======================
LOG_LEVEL = "INFO"
LOG_FILE = LOG_DIR / "engineering_assist.log"

# ======================
# Environment Variables
# ======================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

print("Settings loaded successfully")
print(f"Embedding Model : {EMBEDDING_MODEL}")
print(f"Chroma Path     : {CHROMA_DB_PATH}")
