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

---

## End Goal: Personal World Model

Cortex1's end goal is to build a **personal world model** — a comprehensive, privacy-preserving local index of the user's information across all inputs (email, tasks, calendar, notes, documents, voice) that enables the system to act as a true cognitive assistant over time.

A world model is what separates a triage tool from a cognitive assistant:
- A triage tool processes what's in front of you now.
- A world model knows your history, your patterns, your relationships, and your context — and uses that to make better decisions on every new item.

This shapes two important design constraints:
1. **Comprehensive indexing matters**: The Knowledge Store should eventually hold all personal inputs, not just the current inbox. Historical context improves triage, reply quality, and task extraction.
2. **Ingestion is continuous, not one-shot**: Auto-ingest on startup handles the current inbox (action-oriented). Background historical backfill builds the world model (intelligence-oriented). Both are required.

---

## Agent Extensibility

All external integrations (email providers, task managers, calendar services) are accessed exclusively through the **Agent Registry** — a single dispatch layer that maps domain protocols to concrete implementations. No server code calls provider SDKs directly.

This means:
- Swapping providers requires only a config change
- New integrations require only a new implementation file
- The server is infinitely extensible without architectural changes

See [architecture/agent-registry.md](architecture/agent-registry.md) for the full design.

---

## Roadmap

See [roadmap.md](roadmap.md) for the phased implementation plan from MVP triage to full world model.

---

## Model Tier Assignment

The Model Gateway uses a 3-tier cloud escalation strategy (T1 cheapest → T3 best). Tier assignment is moving from static model name configuration to empirically-calibrated **quality contracts**: apps define golden examples per task type, and the gateway discovers the cheapest model that meets the quality bar. Static tier config entries will be replaced by this mechanism. See `docs/cortex1/v1/modules/model-gateway.md` for the full quality contracts design.
