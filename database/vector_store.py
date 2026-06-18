from database.chroma_client import ChromaClient
from embedding_model import embedding_model
from utils.logger import logger
from typing import List, Dict, Optional

class VectorStore:
    def __init__(self):
        self.client = ChromaClient()
        self.collection = self.client.get_or_create_collection("documents")
        logger.info("VectorStore initialized")

    def add_documents(
        self,
        chunks: List[str],
        metadata: List[Dict],
        embeddings: Optional[List[List[float]]] = None,
        ids: Optional[List[str]] = None         
    ):
        """
        Add documents to ChromaDB.
        embeddings can be pre-computed from embedding_model.encode()
        """
        try:
            if not chunks:
                return []

            ids = [f"chunk_{i}" for i in range(len(chunks))]

            # Generate embeddings if not provided
            if embeddings is None:
                logger.info("Generating embeddings...")
                embeddings = embedding_model.encode(chunks)

            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadata,
                ids=ids
            )

            logger.info(f"Successfully stored {len(chunks)} chunks in ChromaDB")
            return ids

        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
            raise

    def query(
        self,
        query_text: str,
        top_k: int = 30,
        filter: Optional[Dict] = None
    ):
        try:
            query_embedding = embedding_model.encode(query_text)

            if isinstance(query_embedding[0], list):
              query_embedding = query_embedding[0]

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter,                  
                include=["documents", "metadatas", "distances"]
            )

            logger.info(f"Vector search returned {len(results.get('documents', [[]])[0])} results")
            return results

        except Exception as e:
            logger.error(f"Vector query failed: {e}")
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }

    def get_collection(self):
        return self.collection

    def count(self) -> int:
        """Return total number of documents in collection"""
        try:
            return self.collection.count()
        except:
            return 0


# Global singleton
vector_store = VectorStore()