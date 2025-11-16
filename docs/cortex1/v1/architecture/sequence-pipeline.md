# Cortex1 Core Processing Sequence

Type: Sequence Diagram (conceptual, expressed in text).

How to read:
- This is the actual order of operations for a single item (e.g., one email or one Daily Mission note).
- Top → bottom = time.

High-level sequence:

1) User input arrives via some source:
   - New email fetched.
   - Daily Mission file opened or updated.
   - Task added manually.

2) InputAdapters normalize the raw input into a standard internal object.

3) Orchestrator receives the object and:
   - Identifies its type (email, daily_note, task, etc.).
   - Selects the appropriate domain module to eventually handle it.

4) Orchestrator calls Extractor:
   - Extractor returns a structured representation (fields, asks, times, etc.).

5) Orchestrator calls Tagger:
   - Tagger adds or refines tags (@time, @energy, @deadline, @context, @owner).

6) Orchestrator calls PIIScrubber:
   - Produces a scrubbed copy of the content for cloud use.
   - The original, unsanitized content stays only on the local machine.

7) Orchestrator calls Router + ModelGateway:
   - Router decides:
     - Use local model (if GPU/CPU capable).
     - Or call cloud LLM with scrubbed content (ZDR only).
   - ModelGateway executes the call and returns a model result.

8) Orchestrator calls the Domain Module:
   Example:
   - EmailModule:
     - Uses extracted fields, tags, and model result to choose:
       - Draft reply text.
       - Whether to propose a calendar event.
       - Whether to create one or more tasks.
   - TaskModule:
     - Determines where the task goes (Today/Tomorrow/Later).
   - SevenHabitsModule:
     - Places tasks into roles and Weekly Compass / Daily Mission context.

9) Domain Module writes context to KnowledgeStore:
   - Add full text, summaries, annotations, and links.

10) Orchestrator assembles an Output Bundle:
    - Markdown for Obsidian.
    - mailto links for replies.
    - ICS data for calendar holds.
    - Checklists and change-log entries.

11) Output is presented to the user for review and manual application.

