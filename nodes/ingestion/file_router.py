import os
from utils.logger import logger
from schemas.graph_state import GraphState

def file_router_node(state: GraphState):
    try:
        file_paths = state.get("file_paths") or ([state.get("file_path")] if state.get("file_path") else [])
        file_paths = [fp for fp in file_paths if fp]

        if not file_paths:
            state["error"] = "No file paths provided"
            return state

        state["file_paths"] = file_paths
        state["file_types"] = []

        for fp in file_paths:
            ext = os.path.splitext(fp)[1].lower()
            if ext == ".pdf":
                ftype = "pdf"
            elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".webp"]:
                ftype = "image"
            elif ext in [".txt", ".md", ".docx"]:
                ftype = "text"
            else:
                ftype = "unknown"
            state["file_types"].append(ftype)

        logger.info(f"Routed {len(state['file_paths'])} files: {state['file_types']}")
        state["status"] = f"Detected {len(state['file_paths'])} files"
        return state

    except Exception as e:
        logger.error(f"Router error: {e}")
        state["error"] = str(e)
        return state
