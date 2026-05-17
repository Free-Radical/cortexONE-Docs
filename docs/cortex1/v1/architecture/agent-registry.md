# Agent Registry

## Purpose

The Agent Registry is the intended single wiring point between the Cortex1 server and external agents (email transports, task managers, calendar services, and any future integration).

**Rule: No code above the Agent Registry layer may call any provider SDK or API directly. All provider access goes through the registry.**

This keeps the server extensible: swapping Google Calendar for Outlook Calendar, or adding a Todoist task agent, should require a new implementation and config change rather than provider-specific server routes.

---

## Architecture

```
c1server / Dashboard
        ↓
  AgentRegistry          ← single point of dispatch, loaded once at startup
  ├── email_agent   →    EmailAgent (Protocol)
  │                          └── Thunderbird/tbird-sync bridge | GmailAgent | ...
  ├── task_agent    →    TaskAgent (Protocol)
  │                          └── GoogleTasksAgent | InternalTaskAgent | TodoistAgent | ...
  └── calendar_agent →   CalendarAgent (Protocol)
                             └── GoogleCalendarAgent | OutlookCalendarAgent | ...
        ↓
  Provider SDKs / APIs   ← only accessed from within agent implementations
```

---

## Agent Protocols

Each domain defines a Protocol (structural typing). Implementations must satisfy the protocol — there is no required base class.

### EmailAgent
- `list_unread(limit, days_back) -> list[EmailMessage]`
- `mark_read(message_id) -> None`
- `move(message_id, folder) -> None`
- `send_reply(message_id, body) -> None`
- `get_body(message_id) -> str`

### TaskAgent
- `list_tasks(filters) -> list[Task]`
- `create_task(task: Task) -> Task`
- `update_task(task_id, updates: dict) -> Task`
- `complete_task(task_id) -> None`
- `delete_task(task_id) -> None`

### CalendarAgent
- `get_events(start, end) -> list[CalendarEvent]`
- `create_event(event: CalendarEvent) -> CalendarEvent`
- `delete_event(event_id) -> None`
- `get_busy_times(start, end) -> list[tuple[datetime, datetime]]`

---

## Agent Registry

```python
@dataclass
class AgentRegistry:
    email_agent: EmailAgent
    task_agent: TaskAgent
    calendar_agent: CalendarAgent
```

- Instantiated once at server startup from config
- All server routes and domain modules receive the registry via dependency injection
- Config declares which implementation to load per domain:

```yaml
agents:
  email: thunderbird          # or: gmail
  tasks: google_tasks         # or: internal, todoist
  calendar: google_calendar   # or: outlook, apple
```

---

## Extensibility Rules

1. **New provider = new implementation file.** Never modify existing implementations.
2. **No direct imports of provider SDKs outside the agent implementation.** `google-api-python-client` is only imported inside `GoogleCalendarAgent`, never in server routes.
3. **Agents are stateless where possible.** State lives in the Knowledge Store or the provider, not in the agent.
4. **All agents must handle unavailability gracefully** — return empty list or raise `AgentUnavailableError`, never crash the server.
5. **Mock implementations required for all agents** — used in tests and when a provider is not configured.

---

## Current Implementations

| Domain | Implementation | Status |
|--------|---------------|--------|
| Email | Thunderbird/tbird-sync bridge | ✅ MVP bridge/client transport via WebSocket |
| Calendar | `GoogleCalendarAgent` | ⚠️ Infrastructure exists, not wired to registry |
| Calendar | `OutlookCalendarAgent` | ⚠️ Infrastructure exists, not wired |
| Tasks | `GoogleTasksAgent` | ❌ Not yet implemented |
| Tasks | `InternalTaskAgent` | ⚠️ In-memory only, needs SQLite persistence |

Current email status: Thunderbird plus tbird-sync is the MVP client/transport bridge. It should not be read as a fully generalized all-provider abstraction yet.

---

## Adding a New Agent

1. Create `src/cortex1/agents/<domain>/<provider>_agent.py`
2. Implement the relevant Protocol (EmailAgent, TaskAgent, or CalendarAgent)
3. Add a mock implementation in `src/cortex1/agents/<domain>/mock_agent.py`
4. Register in `AgentRegistry` factory under a config key
5. Add golden tests covering the protocol contract

See `docs/cortex1/v1/modules/knowledge-store.md` for how agents interact with the Knowledge Store.
