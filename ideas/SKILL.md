---
name: ideas
description: Scan the vault and generate a full idea report — tools to build, people to meet, topics to investigate, things to write. Use when you want fresh ideas grounded in your actual interests and patterns.
---

# /ideas

Scan the user's Obsidian vault at `/Users/merc/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault` for emerging patterns and generate a full idea report.

Steps:
1. Get a vault overview: `obsidian vault=Vault vault 2>&1 | grep -v "representedObject\|Loading updated\|out of date\|installer\|Loaded main\|Ignored\|Checking\|Success\|Latest version\|App is up\|Obsidian\["`
2. Check tags for recurring themes: `obsidian vault=Vault tags counts format=json 2>&1 | ...`
3. Read recent daily notes (past 14 days) for mentions of ideas, questions, things to try
4. Scan Zettlekasten/ for underdeveloped notes that point outward
5. Look for notes with lots of backlinks — high-gravity ideas that keep attracting connections
6. Check `Projects/` for anything stalled or aspirational

Generate a structured idea report with four sections:
- **Tools to build** — software, systems, or automations the user has hinted at wanting
- **People to reach out to** — names mentioned in notes with potential for collaboration or conversation
- **Topics to investigate** — subjects that keep appearing but haven't been fully explored
- **Things to write** — essays, posts, or notes that are almost ready to exist

For each idea, cite the notes that suggested it.
