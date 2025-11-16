# Extractor Module

Role:
- Given a normalized input item (email, task-like note, Daily Mission entry, document text, etc.), produce a structured representation.

Responsibilities:
- Identify the type of item (email, daily_note, task_stub, doc_snippet).
- Extract fields such as:
  - title/subject
  - sender_name, sender_email (for emails)
  - recipients (for emails)
  - body text
  - explicit asks or instructions
  - explicit deadlines and dates
  - amounts (money or quantities)
  - links and attachments
- Normalize extracted data into a compact JSON-like structure.

Design notes:
- Extractor may use:
  - Regex and heuristics for cheap/fast structure.
  - Small local LLM for ambiguous or complex cases.
  - Cloud LLM (with scrubbed content) only when needed.
- Extractor is domain-agnostic:
  - It does NOT decide what to do with the item.
  - It does NOT implement Seven Habits or task priority.
