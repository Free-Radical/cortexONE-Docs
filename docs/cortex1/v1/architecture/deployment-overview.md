# Cortex1 Deployment Overview

Type: Deployment Diagram (described in text).

Goal:
- Show where each major component runs in a realistic environment.

Primary environments:

1) Local Desktop with GPU (RTX 4070)
   - Components:
     - Local LLM server (Llama 3.x 8B or similar).
     - txtai (or alternative) Knowledge Store.
     - Orchestrator and Pipeline services.
   - Here, Cortex1 can use high-capacity local models for most tasks and only occasionally call cloud models.

2) Laptop or Mini PC (CPU-only or modest GPU)
   - Components:
     - Smaller local models (1–3B).
     - Same Orchestrator, Pipeline, and Knowledge Store (or a lighter version).
   - Cloud models will be used more often for heavy reasoning, but:
     - PII Scrubber still runs locally before cloud calls.

3) Cloud Providers (ZDR models)
   - Components:
     - Third-party LLM endpoints with Zero Data Retention.
   - Accessed only through the ModelGateway.
   - Receive only scrubbed content.

Network view (conceptual):

- Local Machine (any of your devices):
  - Runs Orchestrator, Extractor, Tagger, PII Scrubber, Knowledge Store.
  - Optionally runs local LLMs (depending on hardware).

- Cloud LLM endpoints:
  - Called only via HTTPS.
  - Receive scrubbed prompts.
  - Must honor ZDR policies.

Device Auto-detect:
- ModelGateway detects runtime mode:
  - High-power local mode (GPU desktop).
  - CPU-only local mode (laptop/mini PC).
  - Cloud-dominant mode (if no viable local models are available).
- Routes requests accordingly without requiring manual configuration each time.
