---
name: drift
description: Surface loosely connected ideas that keep appearing across notes without a clear thread. Use when you sense something emerging but can't name it, or want to see what your subconscious is circling.
---

# /drift

Scan the user's Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault` for recurring themes or phrases that appear across unrelated notes — the ideas the user keeps returning to without realizing it.

Steps:
1. Get all tags and their counts to spot recurring themes:
   ```bash
   obsidian vault=Vault tags counts format=json 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Search for repeated words or phrases that appear across multiple unrelated folders (Daily, Zettlekasten, Projects, TaskNotes) — look for semantic overlap, not just exact matches
3. Find notes that have no obvious home — orphaned notes or notes linked from many different contexts:
   ```bash
   obsidian vault=Vault deadends format=json 2>&1 | grep -v ...
   ```
4. Look at the past 30 days of daily notes for words and ideas that recur

Output: what ideas is the user drifting toward without realizing it?
- Name the theme or phrase
- Show where it appears (cite notes across different contexts)
- Describe the pattern: is this growing? consistent? recently spiking?
- Ask: is this something worth naming and pursuing intentionally?

The goal is to make the unconscious visible.
