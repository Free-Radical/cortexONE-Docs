# Cortex1 Data Flow: PII-Safe Path

Type: Data Flow Diagram (described in text).

Goal:
- Show exactly how raw data, PII-scrubbed data, and model calls are separated.

Key flows:

1) RAW DATA (Local Only)
   - Raw emails, Daily Missions, docs, notes, etc. live on your machines.
   - This data is:
     - Ingested by InputAdapters.
     - Passed to Extractor and Tagger.
   - Raw content is NEVER sent directly to cloud LLMs.

2) PII SCRUBBING
   - Before any cloud model call:
     - PII Scrubber scans the content.
     - Replaces:
       - Names, emails, phone numbers, addresses, organizations, IDs, and similar.
     - with random tokens like USER_x9kf, ORG_7pz3, etc.
     - Mapping is not persisted; it is kept only in memory for that single call, then discarded.

3) LOCAL MODEL CALLS
   - For local models:
     - Orchestrator and ModelGateway can use either:
       - Full raw text, OR
       - Partially scrubbed text (if you ever want that).
   - For privacy and simplicity, the baseline assumption is:
     - Local models can see unsanitized content because they run entirely under your control.

4) CLOUD MODEL CALLS (ZDR)
   - Cloud LLMs receive ONLY scrubbed text:
     - No real names, no true emails, no direct identifiers.
   - Providers must support Zero Data Retention (ZDR) so they:
     - Do not store prompts or responses.
     - Do not train on your data.
   - The combination of:
     - Local PII Scrubbing + ZDR
     - means correlation and re-identification risk is minimized.

5) KNOWLEDGE STORE
   - The Knowledge Store sees raw content and structured metadata:
     - Stored locally.
     - Indexed by txtai or similar.
   - Cloud LLMs never directly query the Knowledge Store.
     - Orchestrator retrieves context from the Knowledge Store and passes it (scrubbed or summarized) to cloud models as needed.

Summary:
- Local path handles sensitive data fully.
- Cloud path sees only scrubbed, non-deterministically anonymized content.
- Knowledge Store is local and not exposed to cloud providers.
