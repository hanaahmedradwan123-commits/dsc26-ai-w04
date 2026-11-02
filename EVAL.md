# Evaluation Results

## Recall@3 Comparison (12 Public Queries)

| Retriever Method | Recall@3 |
| :--- | :--- |
| BM25 Only | 0.8333 (10/12) |
| Dense Only (HashingEmbedder) | 0.7500 (9/12) |
| Hybrid (RRF) | 0.9167 (11/12) |

*Note: A query counts as found when one of the top 3 hits overlaps one of its relevant ranges in the same document.*