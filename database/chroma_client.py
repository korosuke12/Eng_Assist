import chromadb
from chromadb.config import Settings
from pathlib import Path
from utils.logger import logger

class ChromaClient:
    _instance = None
    client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.client is None:
            db_path = Path("./chroma_db")
            db_path.mkdir(parents=True, exist_ok=True)

            self.client = chromadb.PersistentClient(
                path=str(db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )
            )
            logger.info("ChromaDB PersistentClient initialized")

    def get_client(self):
        return self.client

    def get_or_create_collection(self, name="documents"):
        try:
            # Try to get existing collection
            collection = self.client.get_or_create_collection(name=name)
            logger.info(f"Retrieved existing collection: {name}")
            return collection
        except Exception:
            # Create new collection with cosine similarity
            collection = self.client.get_or_create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(f"Created new collection: {name}")
            return collection

    def delete_collection(self, name = "documents"):
        try:
            self.client.delete_collection(name)
            logger.info(f"Deleted collection: {name}")
        except Exception as e:
            logger.warning(f"Collection {name} not found {e}")
