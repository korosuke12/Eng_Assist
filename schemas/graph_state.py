from typing import List, Any, TypedDict, Dict, Union

class GraphState(TypedDict):
  query: str
  file_paths: list[str]
  file_types: list[str]
  query: str
  raw_text: str
  structured_pages : List[Dict]
  chunks: List[str]
  chunk_metadata: List[Dict[str, Any]]
  embeddings: List[List[float]]
  retrieved_document: list[dict]
  processed_query: str
  use_reranker: bool
  response: str
  status: str
  error: str
