# Cortex1 SSOT Core (Single Source of Truth)

Version: 1.0
Date: 2025-11-16

## Canonical One-Sentence Definition

Cortex1 is a single linear processing pipeline:

**Input → Extractor → Tagger → PII Scrubber → Router → Model Gateway → Domain Module → Knowledge Store → Output**

with shared global modules (Extractor, Tagger, PII Scrubber, Model Gateway), pluggable domain modules (Email, Tasks, Seven Habits, future org systems), a unified local Knowledge Store, mandatory non-deterministic PII scrubbing before any cloud model call, and automatic device-mode detection (GPU-capable, CPU-only, or cloud-dominant).
