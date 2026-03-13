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
