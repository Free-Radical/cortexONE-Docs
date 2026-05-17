# cortexONE-Docs — Sync TODO

This repo is the architecture SSOT. It has no independent release — its TODO tracks sync obligations to keep docs aligned with implementation repos.

## Sync Required Before System MVP

These docs become wrong when implementation repos advance without matching public architecture updates. Must update before declaring system MVP complete.

- [ ] Add quality contracts architecture doc under docs/cortex1/v1/
- [ ] Commit .gitignore (blocked by: scanner whitelist entries needed — human must run interactively)

## Post-MVP Sync
- [ ] Keep actionability safety/corpus gates aligned with cortex1-core guarded AI/ML replay coverage
- [ ] Keep tbird-sync leasing and status diagnostics aligned with current bridge behavior
- [ ] Keep deployment topology current as the appliance stack evolves
- [ ] Sync cross-repo docs after cortex1-core Phase 3 integration complete

## Up to Date
- [x] Core architecture SSOT (SSOT-Core.md, component-architecture.md)
- [x] Module docs (10 modules)
- [x] Privacy/PII data flow docs
- [x] Model Gateway quality-contract design/status notes
- [x] Baseline PII gate docs (always-on gateway baseline)
- [x] License (PolyForm Noncommercial)
- [x] INVARIANTS.md, CHANGELOG.md, NOTICE.md
