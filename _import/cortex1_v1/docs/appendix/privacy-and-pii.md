# Privacy and PII

Principles:
- Your data stays on your machines by default.
- Cloud calls are minimized and always PII-scrubbed.
- Local Knowledge Store contains full-fidelity data and is not exposed externally.

Key policies:
- No raw PII leaves your local environment.
- PII Scrubber must run before any cloud call.
- Cloud providers must support Zero Data Retention (ZDR).
- Cloud calls are logged for your audit (without sensitive content).

Scope:
- Personal emails, tasks, notes, and documents.
- Not specifically designed for regulated PHI workflows here, but the PII machinery can be extended for that use.

