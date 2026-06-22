from schemas.graph_state import GraphState
from utils.logger import logger
import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\b\d+\b\s*$|\bPage\s+\d+\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def response_node(state: GraphState):
    try:
        query = state.get("query") or state.get("original_query", "")
        retrieved_docs = state.get("retrieved_document", [])

        if not retrieved_docs:
            state["response"] = "Sorry, I couldn't find relevant information."
            state["status"] = "No results found at response.py"
            return state

        # context
        context = []
        sources = []
        images = []
        for i, doc in enumerate(retrieved_docs[:5]):
            chunk = clean_text(doc.get("chunk") or doc.get("content", ""))
            meta = doc.get("metadata", {}) if isinstance(doc.get("metadata"), dict) else {}

            if chunk and len(chunk) > 50:
                context.append(chunk)

            sources.append({
                "source": meta.get("source", "Unknown"),
                "page": meta.get("page", "N/A")
            })
            images_path = meta.get("image") or doc.get("image") or ""
            if images_path:
                    images.append(images_path)
        answer = "\n\n---\n\n".join(context)
        response = f"""response for your Query: {query}
answer:

{answer}

Sources:
"""
        for i, src in enumerate(sources, 1):
            response += f"{i}. {src['source']} (Page {src['page']})\n"

        if images:
                response += "\n**Related Images:**\n"
                for img in images[:3]:
                    response += f"- ![Image]({img})\n"
        response += f"\n**Total Documents Used:** {len(retrieved_docs)}"

        state["response"] = response.strip()
        state["status"] = "Response generated successfully"

        logger.info("Response generated successfully")
        return state

    except Exception as e:
        logger.error(f"Response generation failed: {e}", exc_info=True)
        state["response"] = "error occurred while generating the response.py."
        state["error"] = str(e)
        return state
