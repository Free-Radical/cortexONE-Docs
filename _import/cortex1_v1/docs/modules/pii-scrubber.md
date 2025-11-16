# PII Scrubber Module

Role:
- Protect privacy by ensuring that any text sent to cloud LLMs does not contain raw personally identifiable information (PII).

Key behavior:
- Scans text for:
  - Names, emails, phone numbers, physical addresses.
  - Organization names, domain names, usernames, IDs.
  - Account numbers and other obvious identifiers.
- Replaces them with random, non-deterministic placeholders on each call:
  - USER_x9kf, ORG_7pz3, EMAIL_4tqa, etc.
- Does NOT preserve a long-term mapping:
  - Mapping from original → placeholder exists only in memory for that function call and is then destroyed.

Non-determinism requirement:
- Same name or email must result in different placeholder IDs across different calls.
- This makes it much harder for an adversary or remote observer to correlate activity.

Interaction with local vs cloud:
- For local models:
  - Cortex1 can safely use raw content (at your option).
- For cloud models:
  - Cortex1 must always use PII-scrubbed text.
  - Scrubbing happens before any network call is made.

Output:
- Returns a pair:
  - scrubbed_text
  - optionally, a short "scrub metadata" structure for internal debugging (not stored long-term).
