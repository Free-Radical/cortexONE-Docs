# Model Routing

Purpose:
- Define how Cortex1 chooses between local and cloud models under different conditions.

Routing considerations:
- Device mode (GPU, CPU-only, cloud-dominant).
- Complexity of the task:
  - Simple extraction vs long multi-step planning.
- Sensitivity and privacy:
  - Even after PII scrubbing, some items may be kept local by policy.
- Cost and latency:
  - Prefer local or cheaper models for routine tasks.

Typical routing rules:
- Extraction and tagging:
  - Prefer local small models.
  - Fall back to cloud models only when accuracy is clearly insufficient.
- Planning and drafting:
  - Use cloud models in cloud-dominant or CPU-only modes.
  - Use local large models when running on the RTX 4070 desktop.
- Safety:
  - All cloud routes go through PII Scrubber first.
  - Only ZDR-compliant endpoints are used.
