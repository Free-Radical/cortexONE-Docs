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

## ZeroVeil Gateway Integration

When cloud routing goes through ZeroVeil Gateway, the gateway provides additional DLP controls (PII rejection, model allowlists, rate limits, audit logging) and optionally mixer-based correlation resistance.

ZeroVeil ships five product tiers across SDKs and Gateways:
- **SDK / SDK Pro** — Client-side PII scrubbing (local). SDK Pro adds reversible tokens, multiple backends, audit logging.
- **Gateway Community / Gateway Pro** — Server-side policy enforcement. Pro adds tier escalation, SSO, SIEM, signed audit logs.
- **Gateway Relay** — Hosted-only. Mixer + shared relay identity. Provider cannot identify individual tenants.

For interactive chat, **Open WebUI** (MIT, 126k+ GitHub stars) is the recommended frontend. It speaks OpenAI-compatible API natively — point it at the gateway and all DLP controls apply transparently. Works on any device including iPhone (PWA).

See `zeroveil-gateway-pro/docs/editions.md` for the full product matrix, use cases, and trust model.

## 3-Tier Cloud Model Escalation

For cloud routing, implement cost-optimized tiered escalation:

| Tier | Purpose | Characteristics |
|------|---------|-----------------|
| Tier 1 | Default processing | Cheapest, fastest, handles routine items (~80%) |
| Tier 2 | Validation failures | Better structured output, moderate cost |
| Tier 3 | VIP/Critical items | Best reasoning, highest cost |

**Escalation Strategy:**
1. VIP/Critical items → Tier 3 directly (no cost-cutting on important items)
2. Normal items → Tier 1, retry once on failure, then Tier 2
3. Tier 2 failure → Tier 3
4. Tier 3 failure → Flag for human review

**Design Rationale:**
- Most items are routine → cheap tier handles them
- Structured output models (coder variants) excel at JSON generation
- Graceful degradation prevents returning garbage
- Monthly pricing review ensures optimal model selection

**Implementation Notes:**
- Model selection is implementation-specific (changes with market pricing)
- See implementation repo's `docs/llm-pricing-review.md` for current recommendations
- Review pricing monthly (5th of each month) to capture market changes
