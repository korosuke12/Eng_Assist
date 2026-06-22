from utils.logger import logger
from schemas.graph_state import GraphState

def citation_builder_node(state: GraphState):
    try:
        retrieved_docs = state.get("retrieved_document", [])
        
        citations = []
        for i, doc in enumerate(retrieved_docs):
            source = doc.get("metadata", {}).get("source", "unknown")
            page = doc.get("metadata", {}).get("page", "?")
            chunk_id = doc.get("chunk_id", i)
            
            citations.append({
                "citation_id": f"[{i+1}]",
                "source": source,
                "page": page,
                "chunk_id": chunk_id,
                "final_score": round(doc.get("final_score", 0.0), 4),
                "rerank_score": round(doc.get("rerank_score", 0.0), 4),
            })

        state["citations"] = citations
        state["status"] = f"Built {len(citations)} citations"
        logger.info(f"Citation builder completed: {len(citations)} citations")

    except Exception as e:
        logger.error(f"Citation builder failed: {e}")
        state["citations"] = []
        state["error"] = str(e)
        return state
