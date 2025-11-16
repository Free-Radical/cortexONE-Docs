# Cortex1 Layered Architecture

Type: Layered Architecture Diagram (structural).

How to read:
- Top = user inputs.
- Layers below provide services to layers above.
- This is structure, not time.

LAYERS (top to bottom):

1) User Inputs
   - Emails, tasks, calendar events, notes, files, photos, voice transcripts.

2) Input Adapters
   - Normalize external sources into internal objects (email objects, task objects, document objects, etc.).
   - Examples: IMAP/Maildir reader, calendar API client, file system watcher, photo indexer.

3) Orchestrator + Router
   - Central controller that receives normalized items and decides:
     - Which shared modules to call (sequence is fixed).
     - Which domain module to invoke (Email, Task, Seven Habits, etc.).

4) Shared Pipeline Services
   - Extractor: pulls structured fields out of content.
   - Tagger: adds normalized tags like @time, @energy, @deadline, @context, @owner.
   - PII Scrubber: removes or masks personally identifiable information; generates random placeholders per call.

5) Model Gateway
   - Encapsulates all access to LLMs:
     - Local models (GPU-heavy or CPU-light).
     - Cloud models (Zero Data Retention only).
   - The Router decides which backend to use based on device mode, cost, and complexity.

6) Domain Modules
   - Email Module: triage, reply, schedule, and email-derived tasks.
   - Task Module: generic task engine independent of any productivity framework.
   - Seven Habits Module: Daily Mission and Weekly Compass logic (roles, big rocks, etc.).
   - Future org system modules (e.g., GTD, PARA) plug in at the same level.

7) Knowledge Store Engine
   - Local vector + metadata store (txtai or alternative).
   - Holds emails, docs, tasks, Daily/Weekly history, derived facts and summaries.
   - Acts as Cortex1's "world model".

8) Output Layer
   - Generates paste-ready artifacts:
     - Markdown bundles, mailto links, ICS files, checklists, change-logs, summaries.

