from schemas.graph_state import GraphState
from utils.logger import logger

def reranker_node(state: GraphState):
    try:
        retrieved_docs = state.get("retrieved_document", [])
        
        if not retrieved_docs:
            logger.warning("No documents to rerank")
            return state

        query = state.get("query").strip()
        if not query:
            # Skip reranking if no query
            state["retrieved_document"] = retrieved_docs[:15]
            return state

        query_words = set(query.lower().split())

        for item in retrieved_docs:
            chunk = item.get("chunk") or item.get("content", "")
            chunk_words = set(chunk.lower().split())

            # Keyword overlap ratio
            overlap = len(query_words & chunk_words) / max(len(query_words), 1)

            original_score = item.get("final_score", item.get("score", 0.0))
            item["rerank_score"] = original_score * (0.7 + 0.3 * overlap)

        # Sort by rerank score
        retrieved_docs = sorted(retrieved_docs,key=lambda x: x.get("rerank_score", 0.0), reverse=True)

        # Keep top results
        state["retrieved_document"] = retrieved_docs[:15]
        top_score = retrieved_docs[0].get("score", 0)
        if top_score < 0.5:  # adjust threshold
            state["response"] = "No relevant information found in the uploaded documents."
            state["status"] = "Low relevance"
            return state

        logger.info(f"Simple reranking applied → Top {len(retrieved_docs)} results")
        
    except Exception as e:
        logger.error(f"Reranker failed: {e}")
        # Fallback: keep original results
        retrieved_docs = state.get("retrieved_document", [])
        state["retrieved_document"] = retrieved_docs[:15]
    return state