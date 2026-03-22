---
name: trace
description: Track how a specific idea has evolved over time across the Obsidian vault. Use when you want to see the arc of your thinking on a topic, or when an idea keeps coming up and you want to understand why.
---

# /trace

The user wants to trace an idea across their vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault`.

If the user provided a topic, use it. Otherwise ask: "What idea or topic do you want to trace?"

Then:
1. Search the vault for all mentions of the topic:
   ```bash
   obsidian vault=Vault search:context query="[topic]" format=json 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["
   ```
2. Follow backlinks to find related notes: `obsidian vault=Vault backlinks file="[note]"`
3. Check git history for when notes referencing the topic were created or modified:
   ```bash
   cd "/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault" && git log --oneline --all -- "**/*[topic]*"
   ```
4. Read the most relevant notes to understand how the idea developed

Output a timeline showing:
- When the idea first appeared
- How it evolved and shifted over time
- What it's connected to now
- Any notable turning points or contradictions in the thinking
