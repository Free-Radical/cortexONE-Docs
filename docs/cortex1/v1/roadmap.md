# Cortex1 Roadmap

> This is the implementation roadmap for cortex1-core, grounded in the architecture defined in SSOT-Core.md.
> Builder task specs live in `cortex1-forge/specs/`.

Last updated: 2026-05-17

---

## End Goal

A privacy-first personal cognitive assistant that builds a **world model** of the user's information across email, tasks, calendar, notes, and documents — and uses it to reduce cognitive load, surface what matters, and act as a true daily driver.

See [SSOT-Core.md](SSOT-Core.md) for the full world model definition.

---

## Phase 0 — MVP Triage *(in progress)*

**Goal:** Inbox zero assistant. Process unread emails, triage, draft replies.

- ✅ Email ingestion pipeline (extract → tag → PII scrub → LLM → SQLite)
- ✅ Canvas dashboard lifecycle:
  - Needs You: user disposition required before the item can be considered handled.
  - On Your Plate: visible obligations and follow-ups the user owns.
  - Later If Needed: lower-priority items that may matter later but do not need immediate attention.
  - Auto-processed: safe routine items processed without becoming foreground work.
- ✅ Deduplication, user overrides, active learner
- ✅ ZeroVeil gateway (privacy-first LLM routing)
- ✅ Actionability safety/corpus gates for direct action, waiting, security, finance, and legal signals
- ✅ Thunderbird/tbird-sync bridge foundation for MVP email transport
- [ ] FTS5 table wired to ingest
- [ ] Task persistence (SQLite, off in-memory)
- [ ] ZeroVeil proxy model switch

---

## Phase 1 — Agent Registry *(architecture prerequisite)*

**Goal:** Establish the extensible agent abstraction so no future work ever calls a provider directly.

- [ ] `EmailAgent`, `TaskAgent`, `CalendarAgent` protocols
- [ ] `AgentRegistry` loaded from config at startup
- [ ] `InternalTaskAgent` wrapping SQLite task store
- [ ] `GoogleCalendarAgent` wired to registry (implementation exists, not connected)
- [ ] Mock agents for all domains (testing)

See [agent-registry.md](architecture/agent-registry.md) for the full design.

---

## Phase 2 — Tasks + Calendar in Dashboard *(future utility)*

**Goal:** The dashboard shows not just email, but what needs doing and what's coming up.

- [ ] `GoogleTasksAgent` (OAuth, list/create/complete via Google Tasks API)
- [ ] Tasks panel in canvas dashboard (today + overdue, check off, link to source email)
- [ ] Calendar panel in canvas dashboard (next 7 days)
- [ ] "Create event" action on email cards
- [ ] Tasks extracted from email auto-synced to Google Tasks

---

## Phase 3 — Close the Loop *(email → task → calendar)*

**Goal:** The three domains are connected, not siloed.

- [ ] Email → extracted task → appears in Google Tasks + dashboard
- [ ] Email with date/meeting signal → appears in calendar panel
- [ ] Unified "what needs doing today" view across all three domains
- [ ] Cross-domain linking in Knowledge Store (task links to source email, event links to task)

---

## Phase 4 — World Model Foundation *(historical backfill)*

**Goal:** The brain knows your past, not just today's inbox.

- [ ] Background job walks all mail folders (not just unread)
- [ ] Resumable cursor per account/folder (`last_backfill_cursor`)
- [ ] Rate-limited, low priority, doesn't block UI
- [ ] txtai semantic layer implemented (embeddings on ingest)
- [ ] `get_related_items(email_id)` surfaces relevant history in reply drafts

See [knowledge-store.md](modules/knowledge-store.md) for the two-mode ingestion strategy.

---

## Phase 5 — Additional Input Sources

**Goal:** The brain ingests more than email.

- [ ] Obsidian vault notes → Knowledge Store
- [ ] Local documents/PDFs (text extraction)
- [ ] Voice transcripts (future)

---

## Phase 6 — Proactive Intelligence

**Goal:** From reactive (you ask) to proactive (it surfaces).

- [ ] "You haven't replied to 3 emails from this person in 2 weeks"
- [ ] Daily/Weekly digest generated from world model state
- [ ] 7 Habits module fully integrated (Daily Mission, Weekly Compass driven by real data)
- [ ] Pattern detection (recurring senders, task completion rates, habits)
