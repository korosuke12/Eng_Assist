import re
from typing import List, Dict

def clean_query(query: str) -> str:
    # Clean the query
    query = re.sub(r'\s+', ' ', query.strip())
    query = re.sub(r'[^\w\s\?\.\,\-]', '', query)
    return query


def extract_keywords(doc) -> List[str]:
    # Extract important keywords
    return [token.text.lower() for token in doc
            if token.pos_ in ["NOUN", "PROPN", "ADJ"] and not token.is_stop]