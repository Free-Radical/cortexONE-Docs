# Cortex1 SSOT Core (Single Source of Truth)

Version: 1.1
Date: 2025-12-13

---

## PRIVACY-FIRST PRINCIPLE

**Cortex1 is a PRIVACY-FIRST personal productivity system.**

Core privacy guarantees:
1. **Local Processing Preferred**: Use local LLMs when hardware permits
2. **PII Never Leaves Raw**: All PII scrubbed before any cloud call
3. **User Control**: Override routing for maximum privacy (LOCAL_ONLY mode)
4. **Minimal Cloud Exposure**: Only scrubbed, anonymized content to cloud
5. **ZDR Cloud Only**: Cloud providers must support Zero Data Retention

---

## Canonical One-Sentence Definition

Cortex1 is a single linear processing pipeline:

**Input → Extractor → Tagger → PII Scrubber → Router → Model Gateway → Domain Module → Knowledge Store → Output**

with shared global modules (Extractor, Tagger, PII Scrubber, Model Gateway), pluggable domain modules (Email, Tasks, Seven Habits, future org systems), a unified local Knowledge Store, mandatory PII scrubbing before any cloud model call, and automatic device-mode detection (GPU-capable, CPU-only, or cloud-dominant).
