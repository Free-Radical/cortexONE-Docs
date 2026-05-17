# Cortex1 Deployment Overview

Type: Deployment Diagram (described in text).

Goal:
- Show where each major component runs in a realistic environment.

Current appliance-style topology:

- Cortex server container:
  - Runs the application server, orchestrator, email triage pipeline, Knowledge Store, and dashboard API.
  - Owns local state and remains the system of record for Cortex data.
- ZeroVeil router/gateway:
  - Provides the strict model-routing path for cloud or local model calls.
  - Enforces privacy controls, model policy, and routing decisions before any provider request.
- Thunderbird email client:
  - Remains the user-facing mail client for the MVP email workflow.
  - Connects to Cortex through the tbird-sync bridge over WebSocket rather than acting as a generalized provider abstraction.
- Remote UI:
  - Exposes the desktop/browser experience through an Xpra or browser bridge when the appliance is accessed remotely.
  - Keeps the UI thin; persistent state remains on the Cortex server.
- LAN proxy:
  - Provides local-network access to the appliance services.
  - Should expose only the intended UI/API surfaces and avoid direct access to internal services.

Primary environments:

1) Local Desktop with GPU (RTX 4070)
   - Components:
     - Local LLM server (Llama 3.x 8B or similar).
     - Local Knowledge Store service (e.g., SQLite + FTS5 + txtai).
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

4) Mobile Device (iOS/Android)
   - Components:
     - UI client only (e.g., Obsidian, or a dedicated mobile app).
     - Optional offline cache of recent dashboards/summaries.
   - Best practice:
     - The phone should not be the system of record and should not host large indexes.
     - It connects to a local “hub” machine running Cortex services (directly or via a secure tunnel/VPN).

Network view (conceptual):

- Local Machine (any of your devices):
  - Runs Orchestrator, Extractor, Tagger, PII Scrubber, Knowledge Store.
  - Optionally runs local LLMs (depending on hardware).
  - Acts as the local “hub” for thin clients (desktop UI, mobile UI, email-client extensions).

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
