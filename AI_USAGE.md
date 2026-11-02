# AI Usage Report

- **Tools Used:** Gemini
- **Purpose:** Assisting with string slicing logic for chunking offsets, standard BM25 scoring formulation, and Reciprocal Rank Fusion (RRF) implementation.
- **Spec Compliance / Edge Cases Caught:**
  - AI initial suggestion used `id` instead of `chunk_id` in `Chunk` and `Hit` dataclasses, which was caught during local `pytest` executions.
  - Ensured Arabic normalization retains original character offsets in original text for exact citation bounds.
- **Hybrid Performance Insights:**
  - Hybrid retrieval combining BM25 and HashingEmbedder via RRF achieved higher recall than either single retriever because BM25 excels at precise keyword match (e.g., exact clause numbers) while HashingEmbedder handles phrase variations.# AI Usage Report

- **Tools Used:** Gemini
- **Purpose:** Assisting with string slicing logic for chunking offsets, standard BM25 scoring formulation, and Reciprocal Rank Fusion (RRF) implementation.
- **Spec Compliance / Edge Cases Caught:**
  - AI initial suggestion used `id` instead of `chunk_id` in `Chunk` and `Hit` dataclasses, which was caught during local `pytest` executions.
  - Ensured Arabic normalization retains original character offsets in original text for exact citation bounds.
- **Hybrid Performance Insights:**
  - Hybrid retrieval combining BM25 and HashingEmbedder via RRF achieved higher recall than either single retriever because BM25 excels at precise keyword match (e.g., exact clause numbers) while HashingEmbedder handles phrase variations.