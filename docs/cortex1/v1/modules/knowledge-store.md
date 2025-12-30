# Knowledge Store Module

Role:
- Provide a unified API for storing and retrieving user data for Cortex1.

Key idea:
- The **Knowledge Store is an API**, not “one database.”
- It may be implemented as a **composition** of multiple local storage engines (metadata + full-text + vectors),
  behind one stable interface.

Backends (examples):
- Vector index: txtai (initial), or Qdrant, Weaviate, pgvector, etc.
- Metadata store: SQLite (recommended default for single-user local deployments), or Postgres (multi-user/remote).
- Keyword search: SQLite FTS5 (recommended), or OpenSearch/Elasticsearch (remote / multi-user).

Responsibilities:
- Document ingestion:
  - Emails (full text + headers).
  - Daily/Weekly files.
  - Notes and tasks.
  - Documents and PDFs (extracted text).
  - Photo captions and OCR (future).
  - Audio/video transcripts (future).
- Indexing:
  - Create embeddings and store vector representations.
  - Maintain metadata (source, timestamps, tags, IDs).
- Query:
  - semantic_search(query, k, filters)
  - get_related_items(item_id, k)
  - fetch_by_metadata(filters)

## Recommended Default Implementation (Future-Proof)

To keep the system scalable (and to avoid the “single giant vector DB” trap), implement the Knowledge Store as:

1) **SQLite as the System of Record (canonical)**
   - Stores all *Cortex-derived* state and cross-links:
     - IDs, timestamps, provenance, tags/queues/buckets, thread links, user corrections.
   - Stores pointers to originals (not copies), via stable `source_uri` fields:
     - `thunderlink://...`, `imap://...` (future), `file:///...`, etc.

2) **SQLite FTS5 for keyword search (rebuildable)**
   - Indexes selected text fields (titles/subjects, summaries, extracted text, transcripts).
   - Consider the FTS index a cache: it can be rebuilt from SQLite + original sources.

3) **txtai for semantic search (rebuildable)**
   - Stores embeddings keyed by the canonical IDs from SQLite.
   - Treat embeddings as an index, not truth: rebuild if models change or corruption occurs.

This composition supports:
- Fast exact search (FTS5)
- Strong semantic retrieval (txtai)
- Durable, queryable state (SQLite)

## Preventing “Database Explosion” (Explicit Guidance)

As Cortex expands to photos, video, and audio, storage can grow without bound unless intentionally constrained.

Rules of thumb:
- **Keep originals where they already live.** The Knowledge Store should store *references* + derived annotations.
- **Do not store large binaries in SQLite or txtai.** Store:
  - `source_uri` (path/URL/protocol link)
  - content hash (for dedupe/integrity)
  - minimal metadata (timestamps, size, mime type)
- **Chunk long text and transcripts** (email threads, documents, audio/video ASR):
  - Store chunk-level records with stable IDs and offsets.
  - Index/search at chunk granularity; summarize upward for UI.
- **Separate “truth” from “indexes”:**
  - SQLite tables: truth (provenance, user edits, canonical classifications)
  - FTS/vectors: indexes (rebuildable)
- **Support retention/compaction policies** (local-only, user-controlled):
  - Keep full derived text for recent/high-priority items; keep only summaries for older low-value items.
  - Keep raw transcripts/OCR optionally, but allow pruning and re-extraction from originals.
- **Consider multiple SQLite files** as the dataset grows:
  - `cortex_core.db` (canonical metadata + user edits)
  - `cortex_fts.db` (rebuildable keyword index)
  - `txtai/` directory (rebuildable vector index)

When to outgrow SQLite:
- Multiple concurrent writers across devices/users, centralized multi-user access, or HA/replication needs.
- Otherwise, SQLite remains a strong default for single-user local “personal brain” workloads.

Design principles:
- The rest of Cortex1 only speaks to the Knowledge Store via a stable API.
- The underlying database/engine can be swapped without breaking higher-level logic.
- The Knowledge Store runs locally; external systems never directly access it.
