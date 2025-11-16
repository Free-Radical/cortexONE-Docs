# Cortex1 v1.0

Version: 1.0
Date: 2025-11-16

This repository snapshot describes the **finalized high-level architecture** of Cortex1 as agreed in chat up to 2025-11-16.

Cortex1 is a **personal cognitive assistant** built around a single linear processing pipeline with:
- Shared modules (Extractor, Tagger, PII Scrubber, Model Gateway)
- Pluggable domain modules (Email, Tasks, Seven Habits, future org systems)
- A unified local Knowledge Store (txtai or equivalent)
- Mandatory PII scrubbing before any cloud model call
- Automatic detection of available compute (RTX 4070 desktop, smaller local machines, or cloud-only)

See `docs/SSOT-Core.md` for the canonical summary.
