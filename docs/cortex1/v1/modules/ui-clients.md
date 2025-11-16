# UI Client Adapters (e.g., Obsidian)

Purpose:
- Provide a thin UX layer that sends user input into Cortex1 and renders outputs.
- Keep all business logic in the shared pipeline and domain modules.

Responsibilities:
- Collect input (commands, prompts, selections) and call local API endpoints.
- Render outputs (summaries, drafts, action items) returned by the pipeline.
- Handle authentication/permissions and basic error handling/diagnostics.
- Support bidirectional flow: user input → pipeline; pipeline output → UI surfaces.

Non-responsibilities:
- No business logic (routing, scrubbing, classification, planning).
- No model calls; only use the ModelGateway via the pipeline APIs.
- No direct database or Knowledge Store access; use the orchestration API.

Initial client: Obsidian plugin
- Uses the local API/daemon to submit notes/emails/snippets for processing.
- Renders summaries, drafts, and task/action-item extractions inline.
- Leaves room for future clients (other note apps or apps) reusing the same API.

Interface expectations
- Stable local API surface for submit/process/fetch operations.
- Idempotent requests where possible; resumable operations for longer jobs.
- Clear error messages and telemetry hooks for UX debugging.
