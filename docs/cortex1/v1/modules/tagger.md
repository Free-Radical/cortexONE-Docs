# Tagger Module

Role:
- Add standardized tags to structured items to help downstream logic.

Tags:
- @time: Approximate effort (e.g., "5m", "15m", "30m", "60m").
- @energy: "Low", "Medium", or "High" cognitive/mental effort.
- @deadline: A normalized date/time if one exists.
- @context: Short label describing where/how the task is done:
  - Examples: "Work", "Home", "Online", "Errand".
- @owner: Usually "Saq", but can support multiple identities in future.

Design notes:
- Tagger can use:
  - Lightweight rules (e.g., "email replies under N words = 5–15m, Low energy").
  - Small local or cloud LLMs for nuance, but results must be simple and predictable.
- Tagger is also domain-agnostic:
  - Does not make high-level planning decisions.
  - Feeds consistent tags into domain modules like TaskModule and SevenHabitsModule.
