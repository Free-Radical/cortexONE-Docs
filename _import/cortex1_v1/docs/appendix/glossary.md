# Glossary

- Cortex1:
  The overall personal cognitive assistant system described in this repo.

- Orchestrator:
  Central controller that coordinates the pipeline and domain modules.

- Extractor:
  Shared component that pulls structured data out of raw text.

- Tagger:
  Shared component that assigns normalized tags like @time, @energy, @deadline.

- PII Scrubber:
  Shared component that replaces personal identifiers with random placeholders before any cloud call.

- Model Gateway:
  Shared component responsible for choosing and calling local or cloud LLMs.

- Domain Module:
  A module that applies domain-specific logic (Email, Task, Seven Habits).

- Knowledge Store:
  Local system holding all content and embeddings (e.g., txtai).

- ZDR (Zero Data Retention):
  Cloud model policy where prompts and responses are not stored or used for training.

- Device Autodetect:
  Logic that detects available compute resources and adjusts model routing accordingly.
