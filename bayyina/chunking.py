import re
from bayyina.types import Chunk

def chunk_text(doc_id: str, text: str, max_chars: int = 500, overlap: int = 50) -> list[Chunk]:
    if max_chars <= 0 or not (0 <= overlap < max_chars):
        raise ValueError("Invalid max_chars or overlap parameter")

    if not text or not text.strip():
        return []

    chunks = []
    n = len(text)
    s = 0
    chunk_idx = 0

    while s < n:
        # Skip leading whitespace for start position
        while s < n and text[s].isspace():
            s += 1
        if s >= n:
            break

        # Check if remaining text fits in window
        if n - s <= max_chars:
            e = n
            # Strip trailing whitespace from end pointer
            while e > s and text[e - 1].isspace():
                e -= 1
            chunk_text_str = text[s:e]
            if chunk_text_str:
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc_id}#{chunk_idx}",
                        doc_id=doc_id,
                        start=s,
                        end=e,
                        text=chunk_text_str
                    )
                )
            break

        # Cut point selection within window text[s : s + max_chars]
        window_end = s + max_chars
        window = text[s:window_end]

        cut = -1
        # 1. Just after last paragraph break \n\n
        matches = [m.end() for m in re.finditer(r'\n\n', window)]
        if matches and matches[-1] >= max_chars // 2:
            cut = matches[-1]
        
        # 2. Just after last sentence end (. ! ? ؟ or \n)
        if cut == -1:
            matches = [m.end() for m in re.finditer(r'[\.\!\?؟\n]', window)]
            if matches and matches[-1] >= max_chars // 2:
                cut = matches[-1]

        # 3. Just after last space
        if cut == -1:
            matches = [m.end() for m in re.finditer(r'\s', window)]
            if matches and matches[-1] >= max_chars // 2:
                cut = matches[-1]

        # 4. Hard cut mid-word at window boundary
        if cut == -1:
            cut = max_chars

        c_end = s + cut
        # Strip trailing whitespace for chunk text
        actual_end = c_end
        while actual_end > s and text[actual_end - 1].isspace():
            actual_end -= 1

        chunk_text_str = text[s:actual_end]
        if chunk_text_str:
            chunks.append(
                Chunk(
                    chunk_id=f"{doc_id}#{chunk_idx}",
                    doc_id=doc_id,
                    start=s,
                    end=actual_end,
                    text=chunk_text_str
                )
            )
            chunk_idx += 1

        # Advance s considering max overlap
        next_s = max(s + 1, c_end - overlap)
        s = next_s

    return chunks