from rank_bm25 import BM25Okapi
from database.vector_store import vector_store
from utils.logger import logger
from schemas.graph_state import GraphState

def hybrid_retrieval_node(state: GraphState) -> GraphState:
    try:
        query = (state.get("query") or state.get("processed_query", "")).strip()
        if not query:
            state["retrieved_document"] = []
            return state

        alpha = 0.65
        logger.info(f"Starting Hybrid Retrieval")

        retrieved = []

        # ==================== DENSE RETRIEVAL (ChromaDB) ====================
        try:
            vector_results = vector_store.query(query_text=query, top_k=40)
            dense_docs = vector_results.get("documents", [[]])[0]
            dense_metadatas = vector_results.get("metadatas", [[]])[0]
            dense_distances = vector_results.get("distances", [[]])[0]

            for i, doc in enumerate(dense_docs):
                meta = dense_metadatas[i] if i < len(dense_metadatas) else {}
                distance = dense_distances[i] if i < len(dense_distances) else 1.0
                dense_score = 1.0 / (1.0 + distance)
                retrieved.append({
                    "chunk": doc,
                    "metadata": meta,
                    "dense_score": dense_score,
                    "bm25_score": 0.0
                })
            logger.info(f"Dense retrieval: {len(dense_docs)} results")
        except Exception as e:
            logger.warning(f"Dense retrieval failed: {e}")

        # ==================== BM25  ====================
        try:
          doc_data = vector_store.get_collection().get()['documents']
          if doc_data and len(doc_data) > 0:
            tokenized = [doc.lower().split() for doc in doc]
            query_tokens = query.lower().split()
            bm25 = BM25Okapi(tokenized)
            bm25_scores = bm25.get_scores(query_tokens)
            metadatas = vector_store.get_collection().get()['metadatas']
            for i, score in enumerate(bm25_scores):
              if score > 0.5:
                retrieved.append({
                            "chunk": doc_data[i],
                            "metadata": metadatas[i] if i < len(metadatas) else {},
                            "bm25_score": float(score),
                            "dense_score": 0.0
                        })
        except Exception as e:
            logger.warning(f"BM25 retrieval failed: {e}")
        # ==================== FUSION ====================
        combined = {}
        for item in retrieved:
            key = item["chunk"][:250].strip()
            if key not in combined:
                combined[key] = item
            else:
                existing = combined[key]
                existing["dense_score"] = max(existing.get("dense_score", 0), item.get("dense_score", 0))
                existing["bm25_score"] = max(existing.get("bm25_score", 0), item.get("bm25_score", 0))

        # Final Score
        results = []
        for item in combined.values():
            final_score = (alpha * item.get("bm25_score", 0)) + ((1 - alpha) * item.get("dense_score", 0))
            item["final_score"] = final_score
            results.append(item)

        results.sort(key=lambda x: x.get("final_score", 0), reverse=True)

        state["retrieved_document"] = results[:15]
        logger.info(f"Hybrid Retrieval Completed → {len(state['retrieved_document'])} documents")

    except Exception as e:
        logger.error(f"Hybrid retrieval failed: {e}", exc_info=True)
        state["retrieved_document"] = []

    return state
