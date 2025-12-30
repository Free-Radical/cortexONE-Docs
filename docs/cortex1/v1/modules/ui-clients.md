# UI Client Adapters (e.g., Obsidian)

Purpose:
- Provide a thin UX layer that sends user input into Cortex1 and renders outputs.
- Keep all business logic in the shared pipeline and domain modules.

Design note:
- UI outputs (e.g., Obsidian markdown) are best treated as **materialized views** that can be regenerated.
- Originals (emails/files/media) remain in their native stores; Cortex persists only derived state and references locally.

Responsibilities:
- Collect input (commands, prompts, selections) and call local API endpoints.
- Render outputs (summaries, drafts, action items) returned by the pipeline.
- Handle authentication/permissions and basic error handling/diagnostics.
- Support bidirectional flow: user input → pipeline; pipeline output → UI surfaces.

Non-responsibilities:
- No business logic (routing, scrubbing, classification, planning).
- No model calls; only use the ModelGateway via the pipeline APIs.
- No direct database or Knowledge Store access; use the orchestration API.
- Do not rely on the UI vault as a system of record (avoid using markdown files as the primary datastore).

## Obsidian as Interim Multi-Platform UI (Including iOS)

Obsidian is a pragmatic early UI client because it already provides:
- Cross-platform desktop clients
- Mobile clients (iOS/Android)
- Established sync options

However, to keep the system scalable and future-proof:
- Treat Obsidian content as **rendered outputs + user annotations**, not the canonical dataset.
- Avoid syncing tens of thousands of per-email markdown files to mobile devices.
  - Prefer dashboards/digests + “active set” views (P0/P1 + recent) for mobile.
  - Keep deep links to originals (e.g., `thunderlink://` / provider URLs) as the primary way to access full-fidelity content.
- Ensure any user edits in the UI (e.g., queue/bucket overrides, “reply needed” toggles) are captured as durable, syncable annotations
  that can be reconciled back into the local Knowledge Store / metadata DB.

Initial client: Obsidian plugin
- Uses the local API/daemon to submit notes/emails/snippets for processing.
- Renders summaries, drafts, and task/action-item extractions inline.
- Leaves room for future clients (other note apps or apps) reusing the same API.

Interface expectations
- Stable local API surface for submit/process/fetch operations.
- Idempotent requests where possible; resumable operations for longer jobs.
- Clear error messages and telemetry hooks for UX debugging.
