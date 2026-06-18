from langgraph.graph import StateGraph, END
from schemas.graph_state import GraphState

# Ingestion Nodes
from nodes.ingestion.file_router import file_router_node
from nodes.ingestion.parser import parser_node
from nodes.ingestion.chunking import chunking_node
from nodes.ingestion.embedding_storage import embedding_storage_node

# Retrieval
from nodes.retrieval.hybrid_retriever import hybrid_retrieval_node
from nodes.retrieval.query_processor import query_processing_node
from nodes.retrieval.reranker import reranker_node

# Response
from nodes.response.citation import citation_builder_node
from nodes.response.generator import response_generator


def build_graph():
    workflow = StateGraph(GraphState)

    # Add Nodes
    workflow.add_node("file_router", file_router_node)
    workflow.add_node("parser", parser_node)
    workflow.add_node("chunking", chunking_node)
    workflow.add_node("embedding_storage", embedding_storage_node)
    workflow.add_node("query_processor", query_processing_node)
    workflow.add_node("hybrid_retrieval", hybrid_retrieval_node)
    workflow.add_node("reranker", reranker_node)
    workflow.add_node("citation", citation_builder_node)
    workflow.add_node("generator", response_generator)

    # Conditional Routing
    def routing(state):
        if state.get("file_paths") and len(state.get("file_paths", [])) > 0:
            return "parser"          # Do ingestion
        else:
            return "query_processor" # Direct query

    workflow.add_conditional_edges(
        "file_router",
        routing,
        {
            "parser": "parser",
            "query_processor": "query_processor"
        }
    )    

    # Define Flow
    workflow.add_edge("parser", "chunking")
    workflow.add_edge("chunking", "embedding_storage")
    workflow.add_edge("embedding_storage", "query_processor")
    workflow.add_edge("query_processor", "hybrid_retrieval")
    workflow.add_edge("hybrid_retrieval","reranker")
    workflow.add_edge("reranker", "citation")
    workflow.add_edge("citation", "generator")
    workflow.add_edge("generator", END)

    workflow.set_entry_point("file_router")

    return workflow.compile()
