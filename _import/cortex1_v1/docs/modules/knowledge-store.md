# Knowledge Store Module

Role:
- Provide a unified API for storing and retrieving user data for Cortex1.

Backends:
- Initially: txtai.
- Future alternatives: Qdrant, Weaviate, pgvector, etc.

Responsibilities:
- Document ingestion:
  - Emails (full text + headers).
  - Daily/Weekly files.
  - Notes and tasks.
  - Documents and PDFs (extracted text).
  - Photo captions and OCR (future).
- Indexing:
  - Create embeddings and store vector representations.
  - Maintain metadata (source, timestamps, tags, IDs).
- Query:
  - semantic_search(query, k, filters)
  - get_related_items(item_id, k)
  - fetch_by_metadata(filters)

Design principles:
- The rest of Cortex1 only speaks to the Knowledge Store via a stable API.
- The underlying database/engine can be swapped without breaking higher-level logic.
- The Knowledge Store runs locally; external systems never directly access it.
