import math
from collections import Counter
from bayyina.normalize import tokenize
from bayyina.types import Chunk

class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks: list[Chunk] = []
        self.doc_tokens: list[list[str]] = []
        self.doc_lens: list[int] = []
        self.avgdl: float = 0.0
        self.df: dict[str, int] = Counter()
        self.N: int = 0

    def add(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.N = len(chunks)
        if self.N == 0:
            return

        self.doc_tokens = [tokenize(c.text) for c in chunks]
        self.doc_lens = [len(toks) for toks in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / self.N if self.N > 0 else 0.0

        self.df = Counter()
        for toks in self.doc_tokens:
            unique_terms = set(toks)
            for t in unique_terms:
                self.df[t] += 1

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        if not query or self.N == 0:
            return []

        query_terms = set(tokenize(query))
        scores: list[tuple[str, float]] = []

        for idx, chunk in enumerate(self.chunks):
            doc_toks = self.doc_tokens[idx]
            doc_len = self.doc_lens[idx]
            tf_counts = Counter(doc_toks)
            score = 0.0

            for term in query_terms:
                if term in tf_counts:
                    df_t = self.df.get(term, 0)
                    # Natural logarithm math.log() per spec formula: ln(1 + (N - df + 0.5)/(df + 0.5))
                    idf = math.log(1 + (self.N - df_t + 0.5) / (df_t + 0.5))
                    tf = tf_counts[term]
                    denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
                    score += idf * (tf * (self.k1 + 1)) / denom

            if score > 0:
                scores.append((chunk.chunk_id, score))

        scores.sort(key=lambda x: (-x[1], x[0]))
        return scores[:top_k]