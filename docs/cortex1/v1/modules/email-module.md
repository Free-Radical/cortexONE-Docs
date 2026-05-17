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
- Output:
  - Email-specific actions packaged for the Output Bundle:
    - mailto draft links.
    - ICS blobs for calendar holds.
    - Task stubs ready for the Task Module.

Notes:
- EmailModule does not send email by itself.
- It only prepares suggestions; the user remains the final authority.
