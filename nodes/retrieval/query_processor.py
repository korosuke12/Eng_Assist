import spacy
import re
from typing import Dict, List
from utils.helpers import clean_query,extract_keywords
from utils.logger import logger
from schemas.graph_state import GraphState

# Load spaCy once (outside the function)
nlp = spacy.load("en_core_web_sm")

def query_processing_node(state: GraphState):
    try:
        query = state.get("query", "").strip()
        if not query:
            state["error"] = "No query provided"
            return state

        # Query Cleaning
        cleaned = clean_query(query)

        # spaCy Processing
        doc = nlp(cleaned)

        # Keyword Extraction
        keywords = extract_keywords(doc)


        # Store everything in state
        state.update({
            "original_query": query,
            "cleaned_query": cleaned,
            "keywords": keywords,
            "status": "Query processed successfully"
        })
        logger.info(f"Query processed: {cleaned}")

    except Exception as e:
        state["error"] = str(e)
        state["status"] = "Query processing failed"

    return state