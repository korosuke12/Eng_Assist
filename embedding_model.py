from sentence_transformers import SentenceTransformer
from utils.logger import logger
import os

class EmbeddingModel:
    
    def __init__(self):
        self.model_name = "mixedbread-ai/mxbai-embed-xsmall-v1"
        self.model = None

    def load(self):
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.model_name, device="cpu")
                logger.info(f"Successfully loaded {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to load model {self.model_name}: {e}")
                raise
        return self.model

    def encode(self, texts):
        """Safe encode method"""
        if not texts:
            return []
        
        try:
            model = self.load()
            embeddings = model.encode(
                texts, 
                convert_to_numpy=True, 
                show_progress_bar=False,
                batch_size=32
            )
            return embeddings
        except Exception as e:
            logger.error(f"Encoding failed: {e}")
            raise

# Global instance
embedding_model = EmbeddingModel()