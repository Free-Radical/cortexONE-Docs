# Email Module

Role:
- Apply domain-specific logic to emails after generic extraction and tagging.

Inputs:
- Structured email object from Extractor.
- Tags from Tagger.
- Optional model outputs (classification, suggestions).
- Context from Knowledge Store (similar past threads, related tasks).

Key behaviors:
- Triage:
  - Determine if email should be:
    - Replied to.
    - Ignored.
    - Archived.
    - Marked as spam-like or suspicious.
- Actionability safety:
  - Credible direct action, waiting-on-someone, security, finance, or legal signals fail visible.
  - These items remain visible until the user explicitly disposes them or the system can safely convert them into a user-reviewable lower-risk state.
  - LLM/ML ranking may prioritize, group, and suggest dispositions, but must not bury protected actionable mail.
- Action decisions:
  - Propose reply drafts (text only, via mailto).
  - Propose calendar events when a clear meeting window exists.
  - Propose new tasks for follow-ups or obligations embedded in the email.
  - Structured action suggestions remain user-approved; the module does not execute them automatically.
- Source/body recovery:
  - When C1 has a local email record but Thunderbird no longer resolves the saved Message-ID, C1 owns recovery before showing a terminal missing state.
  - Message-ID candidates are tried first, then `cortex.messages.findByLocator` receives a metadata-only locator with sender, subject, received-time window, account/folder hints, recipient/CC tie-breakers, bounded scan limits, and explicit folder-then-account-wide/all-mail/trash recovery intent.
  - Locator payloads must not include body text, raw MIME, full headers, or full message parts.
  - The Thunderbird sync bridge may honor recovery windows up to seven days and must fail closed on ambiguous matches rather than guessing.
  - User-facing copy should expose calm recovery state, while raw Thunderbird/RPC errors stay in diagnostics and audit trails.
- Output:
  - Email-specific actions packaged for the Output Bundle:
    - mailto draft links.
    - ICS blobs for calendar holds.
    - Task stubs ready for the Task Module.

Notes:
- EmailModule does not send email by itself.
- It only prepares suggestions; the user remains the final authority.
