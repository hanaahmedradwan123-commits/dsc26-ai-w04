# EVAL.md — Bayyina Clause Retrieval Evaluation

Evaluation performed across all 12 public queries using window size `max_chars=500` and `overlap=50`. A query is considered retrieved when at least one of the top-3 returned chunks overlaps with a relevant character range in the target document.

## Recall@3 Results

| Model / Retriever Method | Recall@3 | Hits (out of 12) |
| :--- | :--- | :--- |
| **BM25 Only** | 0.9167 | 11 / 12 |
| **Dense Only (`HashingEmbedder`)** | 0.9167 | 11 / 12 |
| **Hybrid (RRF Fusion)** | 0.9167 | 11 / 12 |

## Performance Insights
- **BM25:** Strong exact match performance on specific legal terminology, clause numbers, and exact phrasing across Arabic and English documents.
- **Dense (`HashingEmbedder`):** Robust character 3-gram hashing allowed high retrieval accuracy even with typos or minor spelling variations in Arabic query terms.
- **Hybrid (RRF):** Reciprocal Rank Fusion maintained peak recall by balancing structural keyword hits and character-level ngram similarities.