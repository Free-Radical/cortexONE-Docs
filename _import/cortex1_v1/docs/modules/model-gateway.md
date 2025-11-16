# Model Gateway Module

Role:
- Central abstraction for calling language models (LLMs).
- Hides complexity of:
  - Local vs cloud.
  - Different providers.
  - Different model sizes and capabilities.

Responsibilities:
- Accept structured requests from Orchestrator:
  - classify_item(...)
  - plan_actions(...)
  - generate_reply(...)
- Inspect:
  - Device capabilities (GPU availability, CPU performance).
  - Cost and latency constraints.
  - Sensitivity level (even after PII scrubbing).
- Route requests to:
  - Local high-capacity models (e.g., 8B on RTX 4070) if available.
  - Local small models (1–3B CPU) on weaker machines.
  - Cloud models (ZDR only) when necessary or beneficial.

Device autodetect modes:
- Mode A: High-power Local
  - GPU present and configured.
  - Use 8B (or similar) as default for heavy tasks.
- Mode B: CPU-only Local
  - Laptop or mini PC, small models only.
  - Use 1–3B for extraction/classification; let cloud handle complex planning.
- Mode C: Cloud-dominant
  - No viable local models.
  - Do minimal pre-processing locally, rely on cloud for major reasoning.
  - PII scrubber always runs before sending text to cloud.

Compliance:
- All cloud endpoints must support Zero Data Retention (ZDR).
- ModelGateway must never send raw PII to the cloud.
