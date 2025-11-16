# Device Autodetect

Role:
- Let Cortex1 adapt to whatever machine you are using:
  - RTX 4070 desktop.
  - CPU-only laptop.
  - Mini PC.
  - Or even thin client scenarios.

Signals:
- GPU availability and VRAM.
- CPU capabilities.
- Presence/absence of local model weights.
- User configuration hints (if any).

Modes:
- Mode A: High-power Local
  - GPU found + capable model present.
  - Use large local models (e.g., 8B) for most tasks.
- Mode B: CPU-only Local
  - No GPU or insufficient VRAM.
  - Use small local models (1–3B) for extraction/classification.
  - Use cloud models (with PII-scrubbed text) for heavy planning.
- Mode C: Cloud-dominant
  - No local models available or desired.
  - Use minimal local logic + cloud models for most reasoning.
  - PII Scrubber is still mandatory for all cloud calls.

Interaction:
- ModelGateway queries device status at startup and periodically.
- Routing decisions are made automatically; user does not need to switch profiles manually.
