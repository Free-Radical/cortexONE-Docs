#!/usr/bin/env python3
"""Check staged files and commit message for AI attribution.

This script is designed to run as a pre-commit hook to prevent
accidental AI attribution from being committed to the repository.

PATTERNS BLOCKED:
- "Generated with [Claude Code]" or similar
- "Co-Authored-By: Claude" or similar AI co-author lines
- "@anthropic.com" email addresses
- "AI-generated" / "AI generated" markers
- References to specific AI tools (Claude, GPT, Copilot attribution)

EXIT CODES:
- 0: No AI attribution found (safe to commit)
- 1: AI attribution detected (block commit)
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

# Patterns that indicate AI attribution (case-insensitive)
AI_PATTERNS = [
    r"Generated with \[?Claude",
    r"Co-Authored-By:.*Claude",
    r"Co-Authored-By:.*GPT",
    r"Co-Authored-By:.*Copilot",
    r"Co-Authored-By:.*Anthropic",
    r"Co-Authored-By:.*OpenAI",
    r"noreply@anthropic\.com",
    r"noreply@openai\.com",
    r"\bAI[- ]generated\b",
    r"\bAI[- ]assisted\b",
    r"Written by Claude",
    r"Written by GPT",
    r"Created by Claude",
    r"Created by GPT",
]

# Compile patterns for efficiency
COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in AI_PATTERNS]

WHITELIST_FILE = ".ai_attribution_whitelist"


def load_whitelist() -> set[str]:
    """Load whitelist entries from .ai_attribution_whitelist if it exists.

    Format: one entry per line as filepath:md5hash
    """
    whitelist: set[str] = set()
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
            for line in f:
                entry = line.strip()
                if entry and not entry.startswith("#"):
                    whitelist.add(entry)
    return whitelist


def line_hash(line: str) -> str:
    """Compute md5 hash of a line (matching shell: echo line | md5sum)."""
    return hashlib.md5((line + "\n").encode()).hexdigest()


def check_content(content: str, source: str, whitelist: set[str] | None = None) -> list[str]:
    """Check content for AI attribution patterns.

    Returns list of violation messages.
    Whitelisted lines (matched by filepath:md5hash in .ai_attribution_whitelist) are skipped.
    """
    if whitelist is None:
        whitelist = set()
    violations = []
    for i, line in enumerate(content.split("\n"), 1):
        for pattern in COMPILED_PATTERNS:
            if pattern.search(line):
                key = f"{source}:{line_hash(line)}"
                if key in whitelist:
                    break  # Whitelisted — skip silently
                violations.append(f"  {source}:{i}: {line.strip()[:80]}")
                break  # One violation per line is enough
    return violations


def get_staged_files() -> list[str]:
    """Get list of staged files."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f for f in result.stdout.strip().split("\n") if f]


def get_staged_content(filepath: str) -> str:
    """Get staged content of a file."""
    result = subprocess.run(
        ["git", "show", f":{filepath}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def get_commit_msg_file() -> str | None:
    """Get path to commit message file if it exists."""
    # Standard git commit message file
    import os
    for path in [".git/COMMIT_EDITMSG", ".git/MERGE_MSG"]:
        if os.path.exists(path):
            return path
    return None


def main() -> int:
    """Main entry point."""
    all_violations: list[str] = []
    whitelist = load_whitelist()

    # Check staged files
    try:
        staged_files = get_staged_files()
    except subprocess.CalledProcessError:
        # Not in a git repo or no staged files
        staged_files = []

    for filepath in staged_files:
        # Skip binary files and certain paths
        if filepath.endswith((".png", ".jpg", ".ico", ".woff", ".ttf", ".pyc")):
            continue
        if "node_modules" in filepath or ".git" in filepath:
            continue

        try:
            content = get_staged_content(filepath)
            violations = check_content(content, filepath, whitelist)
            all_violations.extend(violations)
        except subprocess.CalledProcessError:
            # File might be deleted or binary
            continue

    # Check commit message if available
    commit_msg_file = get_commit_msg_file()
    if commit_msg_file:
        try:
            with open(commit_msg_file, "r", encoding="utf-8") as f:
                commit_msg = f.read()
            violations = check_content(commit_msg, "COMMIT_MSG", whitelist)
            all_violations.extend(violations)
        except (OSError, IOError):
            pass

    if all_violations:
        print("AI ATTRIBUTION DETECTED - COMMIT BLOCKED")
        print("=" * 50)
        print("The following lines contain AI attribution patterns:")
        print()
        for v in all_violations:
            print(v)
        print()
        print("Please remove AI attribution before committing.")
        print("See CLAUDE.md for guidelines.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
