import re
from bayyina.types import Hit

def verify_citation(quote: str, document: str, start: int, end: int) -> bool:
    if not (0 <= start < end <= len(document)):
        return False
    if not quote or not quote.strip():
        return False

    extracted_span = document[start:end]
    norm_extracted = " ".join(extracted_span.split())
    norm_quote = " ".join(quote.split())

    return norm_quote in norm_extracted

def format_citation(hit: Hit, max_quote: int = 160) -> str:
    norm_text = " ".join(hit.text.split())
    
    if len(norm_text) > max_quote:
        truncated = norm_text[:max_quote]
        last_space = truncated.rfind(" ")
        if last_space != -1:
            norm_text = truncated[:last_space] + " ..."
        else:
            norm_text = truncated + " ..."

    return f"[{hit.doc_id}:{hit.start}-{hit.end}] \"{norm_text}\""