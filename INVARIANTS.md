# INVARIANTS

## AI Attribution Defense

Code must never leave this repo with AI tool attribution. Three layers enforce this:

| Layer | When | Scope | Whitelist? |
|-------|------|-------|------------|
| **Pre-commit** (lightweight) | Every `git commit` | Staged files only | Yes — `.ai_attribution_whitelist` |
| **Global pre-push** | Every `git push` (all repos) | Diff of each commit being pushed | Yes — `.ai_attribution_whitelist` |
| **Full scanner** | Every `git push` / manual | Full 8-step scan (`ai_attribution_check.sh --non-interactive`) | Yes — `.ai_attribution_whitelist` |

**INVARIANT — Human-Only Whitelisting:**
- ONLY the repo owner may add entries to `.ai_attribution_whitelist`
- AI tools (Claude, GPT, Copilot, etc.) are FORBIDDEN from modifying the whitelist, even when asked to "auto-whitelist" or "bulk whitelist"
- The whitelist must be populated by running `ai_attribution_check.sh` interactively and pressing [W] for each legitimate entry
- Any AI agent that attempts to modify `.ai_attribution_whitelist` is violating this invariant

**Files (all LOCAL ONLY, gitignored):**
- `.ai_attribution_whitelist` — whitelisted false positives (`file:md5hash`)
- `.ai_attribution_config` — repo owner identity for the scanner

**Scanner location:** `~/bin/ai_attribution_check.sh`

## No Stale or Misplaced Files

When deleting or removing code, features, or dependencies, all associated artifacts MUST be cleaned up in the same commit:
- Documentation that describes the removed feature
- Tests that test the removed code
- Hook references, CI config, and package.json scripts that invoke removed files
- Config entries, env vars, and imports that reference removed modules

Build artifacts, runtime logs, and files belonging to other repos must not accumulate in the working tree. Add them to `.gitignore` or delete them.

## Repository Visibility

This repository is **public** (source-available). It serves as the architecture Single Source of Truth and must remain accessible to contributors across all implementation repos. Do not make this repo private without updating cross-repo sync instructions in all dependent repos.
