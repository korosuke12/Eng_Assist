from config.settings import *
from workflow import build_graph
from schemas.graph_state import GraphState
from utils.logger import logger

def ingest_documents(file_paths: list):
    logger.info(f"Starting ingestion for {len(file_paths)} files")
    
    initial_state: GraphState = {
        "file_paths": file_paths,
        "file_types": [],
        "query": "",
        "structured_pages": [],
        "raw_text": "",
        "chunks": [],
        "chunk_metadata": [],
        "retrieved_docs": [],
        "use_reranker": True,
        "status": "",
        "error": None
    }

    app = build_graph()
    result = app.invoke(initial_state)
    
    print(f"Ingestion Status: {result.get('status')}")
    print(f"Chunks created: {len(result.get('chunks', []))}")
    return result


def ask_question(query: str,file_paths :list = None,use_reranker: bool = True):
    logger.info(f"Processing query: {query}...")

    initial_state: GraphState = {
        "query": query,
        "file_paths": file_paths or [],
        "use_reranker": use_reranker,
    }

    app = build_graph()
    result = app.invoke(initial_state)

    print(f"\n🔍 Query: {query}")
    print(f"Status: {result.get('status')}")
    
    if result.get("retrieved_document"):
        print(f"Retrieved {len(result['retrieved_document'])} documents")
        print(result.get("response", "No response generated")[:500] + "...")
    else:
        print("No relevant documents found.")

    return result


if __name__ == "__main__":
    print("Assist - Started\n")
    
    #Example 1: Ingest a document
   #files = ["F:\Eng_Assist\SOLIDWORKS_Introduction_EN.pdf"]
   #ingest_documents(files)

    # Example 2: Ask a question
    ask_question("how to perform stress analysis")