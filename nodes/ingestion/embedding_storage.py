import os
from utils.logger import logger
from schemas.graph_state import GraphState
from database.vector_store import vector_store
from embedding_model import embedding_model

def embedding_storage_node(state: GraphState):
    try:
        chunks = state.get("chunks", [])
        chunk_metadata = state.get("chunk_metadata", [])

        if not chunks:
            state["status"] = "No chunks available for embedding"
            logger.warning("No chunks to embed")
            return state

        logger.info(f"Embedding {len(chunks)}")

        cleaned_metadata = []
        for meta in chunk_metadata:
            clean_meta = {}
            for k, v in meta.items():
                if v is None:
                    if k in ["image"]:
                        clean_meta[k] = ""
                    else:
                        clean_meta[k] = 0 if isinstance(v, (int, float)) else ""
                else:
                    clean_meta[k] = v
            cleaned_metadata.append(clean_meta)
        metadata = []
        for i, chunk in enumerate(chunks):
          meta = chunk_metadata[i] if i < len(chunk_metadata) and isinstance(chunk_metadata[i], dict) else {}
          source = meta.get("source", "unknown")
          metadata.append({
                "chunk_id": i,
                "source": source,
                "doc_name": os.path.basename(source),
                "page": meta.get("page", 1),
                "type": meta.get("type","text"),
                "image": meta.get("image") or "",
                "chunk_length": len(chunk)
            })
          # Store using updated vector_store
        embeddings = embedding_model.encode(chunks)
        vector_store.add_documents(
            chunks=chunks,
            metadata=metadata,
            embeddings=embeddings
            )
        state["status"] = f"Successfully embedded and stored {len(chunks)} chunks"
        logger.info(state["status"])
        return state

    except Exception as e:
        logger.error(f"Embedding storage node failed: {e}", exc_info=True)
        state["error"] = str(e)
        return state
