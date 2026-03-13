# cortexONE-Docs — Sync TODO

This repo is the architecture SSOT. It has no independent release — its TODO tracks sync obligations to keep docs aligned with implementation repos.

## Sync Required Before System MVP

These docs become wrong when cortex1-core ships Phase 3 + quality contracts. Must update before declaring system MVP complete.

- [ ] Update model-gateway.md — document quality contracts (replaces static tier config with empirical calibration)
- [ ] Update pii-scrubber.md — document baseline PII gate (always-on, unconditional in gateway-pro)
- [ ] Add quality contracts architecture doc under docs/cortex1/v1/
- [ ] Commit .gitignore (blocked by: scanner whitelist entries needed — human must run interactively)

## Post-MVP Sync
- [ ] Add deployment topology doc for Docker stack (proxy + gateway + Open WebUI)
- [ ] Sync cross-repo docs after cortex1-core Phase 3 integration complete

## Up to Date
- [x] Core architecture SSOT (SSOT-Core.md, component-architecture.md)
- [x] Module docs (10 modules)
- [x] Privacy/PII data flow docs
- [x] License (PolyForm Noncommercial)
- [x] INVARIANTS.md, CHANGELOG.md, NOTICE.md
