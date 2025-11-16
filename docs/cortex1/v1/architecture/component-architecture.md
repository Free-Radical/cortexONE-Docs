# Cortex1 Component Architecture

Type: Component Diagram (UML-style).

How to read:
- Boxes = components (subsystems).
- Lines = dependencies / calls.
- This is structural, not a time-based sequence.

Core components:

- InputAdapters
  - Knows how to talk to email servers, calendar APIs, file systems, etc.

- Orchestrator
  - Entry point for processing a new item.
  - Calls shared services in order, then calls a domain module.

- Extractor (Shared)
  - Does structural parsing across all content types.
  - Example responsibilities:
    - From email: sender, recipients, subject, body, links, attachments, asks, deadlines.
    - From Daily Mission: tasks, roles, energy/time hints.
    - From documents: titles, sections, key facts.

- Tagger (Shared)
  - Adds normalized tags:
    - @time (rough effort)
    - @energy (Low/Medium/High)
    - @deadline
    - @context (Work, Home, Personal, etc.)
    - @owner (typically "Saq").

- PIIScrubber (Shared)
  - Rewrites text so that:
    - Names, emails, phone numbers, addresses, IDs, company names, etc. are replaced with random placeholders.
    - Placeholders are re-generated for every call (non-deterministic).
    - Mapping from original → placeholder is kept only in memory and destroyed after the call.

- ModelGateway (Shared)
  - Abstracts model calls:
    - Local LLMs (Llama 3.x 8B or smaller 1–3B models).
    - Cloud LLMs (ZDR: Zero Data Retention).
  - Exposes consistent methods like:
    - generate_reply(context)
    - classify_item(context)
    - plan_day(context)

- Domain Modules (Pluggable)
  - EmailModule:
    - Uses Extractor output + Knowledge Store context to decide
      reply / schedule / create task / ignore / quarantine.
  - TaskModule:
    - Receives tasks from any source (email, Daily Mission, manual).
    - Normalizes, scores, and organizes them (Today, Tomorrow, Later).
  - SevenHabitsModule:
    - Implements your 7 Habits framework:
      Daily Mission, Weekly Compass, roles, big rocks.
    - Uses generic TaskModule for actual task execution.

- KnowledgeStore
  - Provides an API:
    - add_documents(docs)
    - search(query, filters)
    - link_entities(...)
  - Backed by txtai or any other vector+metadata engine.

