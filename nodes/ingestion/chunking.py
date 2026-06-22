from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from schemas.graph_state import GraphState
from utils.logger import logger

def chunking_node(state: GraphState):
  try:
      structured_pages = state.get("structured_pages") or []

      if not state.get("structured_pages"):
            state["error"] = "No parsed content for chunking"
            return state

      chunks = []
      chunk_metadata = []
      chunk_id = 0
      
      recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=900, chunk_overlap=180,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            length_function=len
        )
      for page in structured_pages:
            text = page.get("text", "").strip()
            if not text:
                continue
            page_chunks = recursive_splitter.split_text(text)
            for chunk in page_chunks:
              if len(chunk.strip()) < 80:
                continue
              chunks.append(chunk)
              chunk_metadata.append({
                  "chunk_id": chunk_id,
                  "page": page.get("page", 1),
                  "source": page.get("source", "unknown"),
                  "type": page.get("type", "text"),
                  "image": page.get("images")or "",
                  "chunk_length": len(chunk)
              })
              chunk_id += 1
      state["chunks"] = chunks
      state["chunk_metadata"] = chunk_metadata
      state["status"] = f"Created {len(chunks)} chunks"
      logger.info(f"Chunking completed: {len(chunks)} chunks")
      return state
  except Exception as e:
    logger.error(f"Chunking failed: {e}")
    state["error"] = str(e)
    return state
