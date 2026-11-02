import numpy as np
from bayyina.types import Chunk, Hit, Embedder, Reranker
from bayyina.bm25 import BM25Index

def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for rank_list in rankings:
        for rank, item_id in enumerate(rank_list, start=1):
            scores[item_id] = scores.get(item_id, 0.0) + (1.0 / (k + rank))
    
    # Sort by score descending, then ID ascending
    res = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return res

class HybridRetriever:
    def __init__(self, chunks: list[Chunk], embedder: Embedder, *, k1: float = 1.5, b: float = 0.75, reranker: Reranker | None = None):
        self.chunks = chunks
        self.chunk_map = {c.chunk_id: c for c in chunks}
        self.embedder = embedder
        self.reranker = reranker
        
        self.bm25 = BM25Index(k1=k1, b=b)
        self.bm25.add(chunks)

        # Precompute chunk embeddings
        texts = [c.text for c in chunks]
        self.chunk_embeddings = embedder.embed(texts) if chunks else np.array([])

    def search(self, query: str, top_k: int = 5, candidates: int = 50) -> list[Hit]:
        if not query or not self.chunks:
            return []

        # 1. BM25 candidate IDs
        bm25_res = self.bm25.search(query, top_k=candidates)
        bm25_ids = [item_id for item_id, _ in bm25_res]

        # 2. Dense candidate IDs
        q_emb = self.embedder.embed([query])[0]
        dots = np.dot(self.chunk_embeddings, q_emb)
        dense_pairs = [(self.chunks[i].chunk_id, float(dots[i])) for i in range(len(self.chunks))]
        dense_pairs.sort(key=lambda x: (-x[1], x[0]))
        dense_ids = [item_id for item_id, _ in dense_pairs[:candidates]]

        # 3. Fuse with RRF
        fused = rrf([bm25_ids, dense_ids])[:candidates]

        # 4. Construct Hits positionally
        hits = []
        for chunk_id, rrf_score in fused:
            c = self.chunk_map[chunk_id]
            hits.append(Hit(c.chunk_id, c.doc_id, c.start, c.end, c.text, rrf_score))

        # 5. Rerank if reranker present
        if self.reranker and hits:
            scores = self.reranker.score(query, [h.text for h in hits])
            for hit, s in zip(hits, scores):
                hit.score = float(s)
            hits.sort(key=lambda x: (-x.score, x.chunk_id if hasattr(x, 'chunk_id') else x.doc_id))

        return hits[:top_k]